---
name: search-jobs
description: >
  Search and rank relevant job listings using connector-first discovery.
  Uses Indeed MCP when available, then browser/manual fallback for
  state/federal boards, niche boards, and company/ATS career pages.
triggers:
  - "/search-jobs"
  - "search for jobs"
  - "find jobs"
  - "search jobs"
  - "look for job listings"
  - "find me jobs"
  - "search indeed"
  - "search wellfound"
  - "search state jobs"
  - "search company careers"
  - "what jobs are out there"
  - "show me job listings"
---

Search and rank job listings that match the user's profile using a connector-first strategy.

## Source model and normalization

Use a hybrid source model in this order:

1. **Connector-native MCP (preferred)** for any available source (Indeed first in current implementation).
2. **Browser-assisted capture** (Claude in Chrome / computer use) only when MCP is missing or the flow is browser-only.
3. **Assisted-manual ingestion** as guaranteed fallback.

Normalize all listings into this schema before ranking:

- `title` (required)
- `company` (required)
- `location` (required)
- `apply_url` (required)
- `source` (required; examples: `indeed`, `illinoisjoblink`, `wellfound`, `company_direct`, `ats_greenhouse`)
- `retrieval_mode` (required; `mcp` | `browser` | `manual`)
- `salary` (optional, raw text if no structured range)
- `posted_date` (optional)
- `close_date` (optional; common on public-sector postings)
- `employment_type` (optional)
- `job_id_or_requisition` (optional but preferred for dedupe)
- `raw_description` (optional but preferred for stronger scoring)

If required fields are missing, ask for only the missing fields before ranking.

## Preflight (connector-first)

**Live path:** If **`search_jobs`** and **`get_job_details`** are available, use them as the primary lane and follow **§1–§5** below.

**No Indeed MCP in this session:** Do **not** invent tool results. Do both of the following:

1. Explain how to enable live search on **Claude Desktop**: **Customize → Connectors** → **Indeed** → **Connect** → complete **Grant access to Indeed** in the browser (Indeed OAuth on **secure.indeed.com** — sign in and **Continue**), then a **new chat**. Point to **`/career-navigator:launch` Step 3** for the full walkthrough.

2. **Assisted manual:** Skip **`search_jobs`** / **`get_job_details`**. After loading parameters from **§1**, provide 2-3 targeted query/link packs for each channel requested:
   - state/federal boards (e.g., IllinoisJobLink, USAJobs),
   - niche boards (e.g., Wellfound, Welcome to the Jungle),
   - company-direct/ATS pages (company careers, Greenhouse/Lever/Workday).
   Ask the user to paste listings using the normalized schema from **Source model and normalization**. Pass what they provide to **`job-scout`** for ranking; present with the **§5** layout where links exist. Footer: note listings were **user-provided** (not live MCP) until connectors are connected.

## Workflow

### 1. Load search parameters

Read `{user_dir}/CareerNavigator/profile.md` and extract:
- **Role/query** — use the first 1–2 entries from `## Target Roles` as the search query
- **Location preferences** — parse `## Location` into:
  - primary mode preference (for example: remote-first)
  - acceptable work modes (remote, hybrid, on-site)
  - geography constraints (cities/states user is open to, plus avoid/deprioritize geographies if stated)
  - relocation/travel willingness

If the profile only implies "remote-first" and does not clearly define secondary flexibility, ask one brief clarification before searching:
> "I can keep remote as priority and include selective hybrid/relocation options. Which locations should I include as secondary targets (for example NYC, SF), and are any locations off-limits?"

If the user provided explicit search terms in their request (e.g., "find AI PM jobs in New York"), use those instead of — or in addition to — the profile values. Always prefer the user's explicit intent.

If `profile.md` does not exist or has no target roles, ask:
> "What role and location should I search for?"

Capture optional source preferences when provided:
- preferred channels (`state/federal`, `niche`, `company_direct`, `aggregator`)
- target companies list (for company-direct and ATS discovery)
- off-limit sources the user does not want

### 1.25 Assisted-manual playbooks (when MCP is missing or user requests extra channels)

If any requested channel cannot be searched live via MCP in-session, generate concise playbooks:

1. **State/federal boards**
   - Provide source-specific query strings using role + location + grade/seniority hints.
   - Ask for `close_date` when present.
   - Example boards: IllinoisJobLink, USAJobs.

2. **Niche boards**
   - Provide board-specific queries with role synonyms and remote/on-site variants.
   - Ask for salary text and equity details when available.
   - Example boards: Wellfound, Welcome to the Jungle.

3. **Company-direct and ATS**
   - For each target company, provide one direct careers query and one ATS query variant (`site:boards.greenhouse.io`, `site:jobs.lever.co`, `site:myworkdayjobs.com`).
   - Ask for canonical `apply_url` and requisition ID when visible.

### 1.5 Load trajectory context (for scoring)

Before searching, check for `{user_dir}/CareerNavigator/career-trajectory.md`.

- If present, read it and extract the fenced `career_trajectory_v1` JSON (especially `as_of`, `near_term_roles`, `medium_term_roles`).
- If missing, continue with no trajectory context.
- If present but JSON cannot be parsed, continue and mark trajectory as unavailable due to parse error (do not silently drop this signal).

When presenting results, include a one-line trajectory note after the scoring header:
- `Trajectory context: used (as_of {YYYY-MM-DD})`
- or `Trajectory context: unavailable (missing or unparseable)`

### 2. Search Indeed

Build a small search plan from the location preferences, then call `search_jobs`.

Create up to 3 lanes (max), in this order:
1. **Primary lane** — top preference (often `remote`)
2. **Secondary lane** — best-fit hybrid/relocation geography (for example NYC)
3. **Tertiary lane** — optional additional geography (for example SF) only if user is open

Call `search_jobs` for each lane with the extracted parameters:
- `search` — the role or keyword string (e.g., `"Director of AI Product"`)
- `location` — city/state (e.g., `"New York, NY"`) or `"remote"`
- `country_code` — `"US"` unless the user's location indicates otherwise
- `job_type` — omit unless the user specifies (fulltime, parttime, contract, etc.)

Run lanes in parallel, then merge and deduplicate by job ID/link.

If the user requested additional channels and equivalent MCP tools are not present, append the assisted-manual playbooks from **§1.25** and continue once listings are pasted.

### 3. Get job details

From the search results, identify the top 5 most relevant listings. For each one, call `get_job_details` using the job ID returned by `search_jobs` to retrieve the full description, confirmed salary, and apply link.

Run all 5 `get_job_details` calls in parallel.

For non-Indeed/manual listings, treat pasted metadata as the detail payload and mark missing fields explicitly.

### 4. Score and rank with job-scout

Pass all retrieved listings to the `job-scout` agent for outcome-weighted scoring. Job-scout will:
- Read `search_performance` and `strategy_signals` from `tracker.json`, plus `performance_weights` from `CareerNavigator/ExperienceLibrary.json`
- Read `{user_dir}/CareerNavigator/career-trajectory.md` when present and apply trajectory alignment bonus from `career_trajectory_v1`
- Score each listing across outcome signals, ExperienceLibrary fit, profile fit, and strategy signals using confidence-tier adaptive weights
- Apply bounded calibration (recency, outcome quality, transferability)
- Return the listings in ranked order with composite scores, per-factor rationale, and recommendation tiers (`critical` | `high` | `watch` | `none`)

When invoking `job-scout`, explicitly pass:
- full listing payloads (including full JDs/metadata),
- `profile.md`, `tracker.json`, `ExperienceLibrary.json`,
- and `{user_dir}/CareerNavigator/career-trajectory.md` if it exists.

If `career-trajectory.md` exists but cannot be parsed, continue scoring and label trajectory alignment as unavailable rather than dropping `job-scout`.

Use job-scout's ranked order for the final presentation. If job-scout returns a tie (within 5 points), preserve the original Indeed relevance order within the tied group.

Before final ranking, apply provenance + confidence + dedupe policy:

- **Provenance:** every listing must include `source` and `retrieval_mode`.
- **Confidence tier:**
  - `high` when listing has title/company/location/apply URL + description + posted date.
  - `moderate` when required fields exist but description/date are partial.
  - `directional` when required fields exist but multiple optional fields are missing.
- **Deduplication order:** prefer listing with
  1) canonical company-direct URL,
  2) then ATS URL with requisition ID,
  3) then connector-sourced aggregator URL,
  4) then manual copy.
  Use normalized title/company/location plus URL/requisition overlap to detect duplicates.

Before finalizing top results, apply a light location-balance check:
- Keep the highest-ranked jobs overall, but avoid returning a remote-only set when secondary lanes produced strong matches.
- Target mix for top 5 when available: at least 1 result from non-primary lanes if score is within 8 points of the 5th-ranked job.
- Never include locations the user marked off-limits.

### 5. Present results

Output a formatted summary. **Always embed the apply link in the job title** so the user can click directly to apply — this is required by the Indeed connector.

Open with a one-line header showing the confidence tier from job-scout:

> *Scoring: {Preliminary | Directional | Moderate | High confidence} — {reason, e.g., "based on 3 resolved outcomes" or "no outcome data yet, profile-match only"}*

Then include:
> *Trajectory context: {used (as_of YYYY-MM-DD) | unavailable (missing/unparseable)}*

Then include:
> *Source mix: {count by source} · Retrieval modes: {mcp/browser/manual counts}*

Use this format for each listing:

---

**{#}. [{Job Title}]({apply_link})**
Company: {Company Name}
Location: {City, State | Remote | Hybrid}
Salary: {range if listed, otherwise "Not listed"}
Score: {composite}/100 · {ExperienceLibrary fit %}% ExperienceLibrary fit · Recommendation: {critical|high|watch|none}{avoid signal warning if present}

> {2–3 sentence summary of the role drawn from the job description — focus on scope, key responsibilities, and what makes it notable}

---

After all listings, add:
> Listings sourced from Indeed on {today's date}. Run `/career-navigator:track-application` to log any you apply to.

If sources are mixed, replace the line with:
> Listings sourced on {today's date} from: {source list}. Retrieval modes: {mcp/browser/manual counts}. Run `/career-navigator:track-application` to log any you apply to.

Then add:
> Search mix: {remote_count} remote, {hybrid_count} hybrid, {onsite_count} on-site. Prioritized for: {primary preference}; secondary geographies included: {list or "none"}.

If any listing is `critical` or `high`, append:
> Priority recommendations: {critical_count} critical, {high_count} high. Start with the top recommendation first.

**If `search_jobs` returns no results:**
> "Indeed returned no results for '{query}' in '{location}'. Try a broader title or a different location."

**If fewer than 5 listings are returned**, present what was found — do not pad or fabricate results.

If any listing is `directional`, add one line:
> Data quality note: some listings have partial metadata; ranking confidence is lower until missing fields are filled.
