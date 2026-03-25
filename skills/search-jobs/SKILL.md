---
name: search-jobs
description: >
  Search Indeed for relevant job listings using the Indeed connector.
  Returns the top 5 results with company, title, location, salary (if
  listed), and a direct apply link for each.
triggers:
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
- **Location** — use the value from `## Location`; if the user is open to remote, run a second search with `location: "remote"`

If the user provided explicit search terms in their request (e.g., "find AI PM jobs in New York"), use those instead of — or in addition to — the profile values. Always prefer the user's explicit intent.

If `profile.md` does not exist or has no target roles, ask:
> "What role and location should I search for?"

### 2. Search Indeed

Call `search_jobs` with the extracted parameters:
- `search` — the role or keyword string (e.g., `"Director of AI Product"`)
- `location` — city and state (e.g., `"Chicago, IL"`) or `"remote"`
- `country_code` — `"US"` unless the user's location indicates otherwise
- `job_type` — omit unless the user specifies (fulltime, parttime, contract, etc.)

If the user's profile shows openness to multiple locations (e.g., Chicago + SF + NYC + remote), run up to two searches in parallel — one for the primary location and one for `"remote"` — and merge the results.

### 3. Get job details

From the search results, identify the top 5 most relevant listings. For each one, call `get_job_details` using the job ID returned by `search_jobs` to retrieve the full description, confirmed salary, and apply link.

Run all 5 `get_job_details` calls in parallel.

### 4. Score and rank with job-scout

Pass all retrieved listings to the `job-scout` agent for outcome-weighted scoring. Job-scout will:
- Read `search_performance` and `strategy_signals` from `tracker.json`, plus `performance_weights` from `CareerNavigator/ExperienceLibrary.json`
- Score each listing across outcome signals, ExperienceLibrary fit, profile fit, and strategy signals using confidence-tier adaptive weights
- Apply bounded calibration (recency, outcome quality, transferability)
- Return the listings in ranked order with composite scores, per-factor rationale, and alert tiers (`critical` | `high` | `watch` | `none`)

Use job-scout's ranked order for the final presentation. If job-scout returns a tie (within 5 points), preserve the original Indeed relevance order within the tied group.

### 5. Present results

Output a formatted summary. **Always embed the apply link in the job title** so the user can click directly to apply — this is required by the Indeed connector.

Open with a one-line header showing the confidence tier from job-scout:

> *Scoring: {Preliminary | Directional | Moderate | High confidence} — {reason, e.g., "based on 3 resolved outcomes" or "no outcome data yet, profile-match only"}*

Use this format for each listing:

---

**{#}. [{Job Title}]({apply_link})**
Company: {Company Name}
Location: {City, State | Remote | Hybrid}
Salary: {range if listed, otherwise "Not listed"}
Score: {composite}/100 · {ExperienceLibrary fit %}% ExperienceLibrary fit · Alert: {critical|high|watch|none}{avoid signal warning if present}

> {2–3 sentence summary of the role drawn from the job description — focus on scope, key responsibilities, and what makes it notable}

---

After all listings, add:
> Listings sourced from Indeed on {today's date}. Run `/career-navigator:track-application` to log any you apply to.

If any listing is `critical` or `high`, append:
> Priority alerts: {critical_count} critical, {high_count} high. Start with the top alert first.

**If `search_jobs` returns no results:**
> "Indeed returned no results for '{query}' in '{location}'. Try a broader title or a different location."

**If fewer than 5 listings are returned**, present what was found — do not pad or fabricate results.
