---
name: search-jobs
description: >
  Search Indeed for relevant job listings using the Indeed connector.
  Returns the top 5 results with company, title, location, salary (if
  listed), and a direct apply link for each.
triggers:
  - "/search-jobs"
  - "search for jobs"
  - "find jobs"
  - "search jobs"
  - "look for job listings"
  - "find me jobs"
  - "search indeed"
  - "what jobs are out there"
  - "show me job listings"
---

Search Indeed for job listings that match the user's profile using the Indeed connector (`search_jobs`).

## Preflight

**Live path:** If **`search_jobs`** and **`get_job_details`** are available, follow **§1–§5** below.

**No Indeed MCP in this session:** Do **not** invent tool results. Do both of the following:

1. Explain how to enable live search on **Claude Desktop**: **Customize → Connectors** → **Indeed** → **Connect** → complete **Grant access to Indeed** in the browser (Indeed OAuth on **secure.indeed.com** — sign in and **Continue**), then a **new chat**. Point to **`/career-navigator:launch` Step 3** for the full walkthrough.

2. **Assisted manual:** Skip **`search_jobs`** / **`get_job_details`**. After loading parameters from **§1**, output 2–3 tight search queries or direct links (Indeed + LinkedIn + Google Jobs) for that role/location. Ask the user to paste back listings (title, company, location, link, optional pay line). Pass what they provide to **`job-scout`** for ranking; present with the **§5** layout where links exist. Footer: note listings were **user-provided** (not live Indeed MCP) until the connector is connected.

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

### 3. Get job details

From the search results, identify the top 5 most relevant listings. For each one, call `get_job_details` using the job ID returned by `search_jobs` to retrieve the full description, confirmed salary, and apply link.

Run all 5 `get_job_details` calls in parallel.

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

Then add:
> Search mix: {remote_count} remote, {hybrid_count} hybrid, {onsite_count} on-site. Prioritized for: {primary preference}; secondary geographies included: {list or "none"}.

If any listing is `critical` or `high`, append:
> Priority recommendations: {critical_count} critical, {high_count} high. Start with the top recommendation first.

**If `search_jobs` returns no results:**
> "Indeed returned no results for '{query}' in '{location}'. Try a broader title or a different location."

**If fewer than 5 listings are returned**, present what was found — do not pad or fabricate results.
