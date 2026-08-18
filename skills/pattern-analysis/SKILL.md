---
name: pattern-analysis
description: >
  Analyzes application outcome data to find what's working and what isn't.
  Cross-references tracker history with artifact performance to update ExperienceLibrary
  weights and surface search_performance signals. Invokes the analyst agent.
triggers:
  - "analyze my search"
  - "what's working in my search"
  - "analyze my applications"
  - "what patterns do you see"
  - "update my weights"
  - "how is my search going"
  - "what's converting"
  - "where am I getting stuck"
---

Invoke the `analyst` agent to run an outcome pattern analysis on the user's application history.

## Workflow

### 1. Confirm data exists

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

Read `{user_dir}/CareerNavigator/tracker.json`. The threshold check runs on the summary rows' `outcome` field alone — do not open detail files yet. If the `applications` array is empty or has fewer than 3 entries with a resolved outcome (phone_screen, interview, offer, rejected, or inactive):

> "You don't have enough outcome data yet for pattern analysis — I need at least a few applications with known results. Keep logging updates via `/career-navigator:track-application` and run this again once you have more history."

Otherwise, proceed.

### 2. Load the full history

This analysis needs stage history and note text, and **`tracker.json` alone contains none of it** — `stage_history[]` and `notes[]` moved to the per-application detail files. Computing conversion, drop-off, or timeline patterns from `tracker.json` by itself silently produces zeros and reports "no patterns found" when patterns exist.

1. Read `{user_dir}/CareerNavigator/tracker.json` and take `applications[]`.
2. Iterate every row and load its `detail_file` (relative to `CareerNavigator/`) to get that application's `stage_history[]` and `notes[]`. Skip a row only when `stage_count` and `notes_count` are both `0`.
3. Where a summary field already answers the question — current stage (`latest_stage`), date of the last stage change (`latest_stage_date`), or a count (`stage_count`, `notes_count`, `contact_count`) — use it instead of re-deriving from the detail file.

### 3. Invoke analyst — Operation 1

Hand off to the `analyst` agent with:
- `CareerNavigator/tracker.json` (summary rows) **plus** the loaded `applications/<application_id>.json` detail files — pass both; the summary rows alone are not a sufficient input for this operation
- The full `artifacts-index.json`
- The full `CareerNavigator/ExperienceLibrary.json`

The agent will:
- Cross-reference artifact performance with application outcomes
- Identify patterns in variant performance, experience unit performance, role/market fit, and timelines
- Update `performance_weights` in `CareerNavigator/ExperienceLibrary.json`
- Write a `weight_update_log` entry for each change
- Write a `search_performance` summary to `tracker.json` (a top-level key — not into any detail file)

### 4. Confirm updates

After the agent completes, report what changed:

```
Pattern analysis complete.

ExperienceLibrary weights updated
  {n} unit(s) increased  — {role titles, brief rationale}
  {n} unit(s) decreased  — {role titles, brief rationale}
  {n} unit(s) unchanged  (insufficient data)

Search performance summary written to tracker.json
  Top converting role types: {list}
  Top converting industries:  {list}
  Signals to avoid:           {list}

Data confidence: {Preliminary / Directional / Moderate / High} ({n} applications with outcomes)
```

If weights could not be updated for any unit due to insufficient data, note it. Do not suppress this — the user should know when the dataset is too small to support a change.

### 5. Suggest next step

> "Run `/career-navigator:report` for the full analyst report, or `/career-navigator:tailor-resume` to use the updated weights in your next resume."
