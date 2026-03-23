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

Read `{user_dir}/CareerNavigator/tracker.json`. If the `applications` array is empty or has fewer than 3 entries with a resolved outcome (phone_screen, interview, offer, rejected, or inactive):

> "You don't have enough outcome data yet for pattern analysis — I need at least a few applications with known results. Keep logging updates via `/career-navigator:track-application` and run this again once you have more history."

Otherwise, proceed.

### 2. Invoke analyst — Operation 1

Hand off to the `analyst` agent with:
- The full `CareerNavigator/tracker.json`
- The full `artifacts-index.json`
- The full `CareerNavigator/ExperienceLibrary.json`

The agent will:
- Cross-reference artifact performance with application outcomes
- Identify patterns in variant performance, experience unit performance, role/market fit, and timelines
- Update `performance_weights` in `CareerNavigator/ExperienceLibrary.json`
- Write a `weight_update_log` entry for each change
- Write a `search_performance` summary to `tracker.json`

### 3. Confirm updates

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

### 4. Suggest next step

> "Run `/career-navigator:report` for the full analyst report, or `/career-navigator:tailor-resume` to use the updated weights in your next resume."
