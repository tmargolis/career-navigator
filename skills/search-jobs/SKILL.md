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

## Workflow

### 1. Load search parameters

Read `{user_dir}/profile/profile.md` and extract:
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
- Read `search_performance` from `tracker.json` and `performance_weights` from `corpus/index.json`
- Score each listing across outcome signals, corpus fit, and profile fit
- Return the listings in ranked order with composite scores and per-factor rationale

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
Score: {composite}/100 · {corpus fit %}% corpus fit{avoid signal warning if present}

> {2–3 sentence summary of the role drawn from the job description — focus on scope, key responsibilities, and what makes it notable}

---

After all listings, add:
> Listings sourced from Indeed on {today's date}. Run `/career-navigator:track-application` to log any you apply to.

**If `search_jobs` returns no results:**
> "Indeed returned no results for '{query}' in '{location}'. Try a broader title or a different location."

**If fewer than 5 listings are returned**, present what was found — do not pad or fabricate results.
