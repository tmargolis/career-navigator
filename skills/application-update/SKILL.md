---
name: application-update
description: >
  Runs whenever tracker records change. Re-checks outcome freshness, flags when
  job-scout signals should be refreshed, and triggers pattern-analysis nudges at
  key resolved-outcome milestones.
triggers: []
---

Run **immediately after** the `track-application` skill writes or updates `{user_dir}/CareerNavigator/tracker.json` (same conversation turn). There is no separate plugin hook file — orchestration is conversational or host-defined.

## Workflow

### 1. Read tracker state

Read `{user_dir}/CareerNavigator/tracker.json` and inspect:
- latest application updates
- `outcome` distribution
- whether `search_performance` exists and has `as_of`

### 2. Determine refresh needs

Set refresh guidance based on change type:
- If a terminal outcome changed (`hired`, `rejected`, `withdrew`), mark as **high-priority refresh**
- If stage/status changed without terminal outcome, mark as **standard refresh**
- If no scoring-relevant fields changed, mark as **no refresh needed**

### 3. Milestone nudges for analyst refresh

Count resolved outcomes (`outcome != "pending"`). If count is:
- `5`, `10`, `15`, or a multiple of `10`: append a nudge to run `/career-navigator:pattern-analysis`

If `search_performance.as_of` is older than 14 days and new outcomes were logged, append:
> Outcome data changed since last scoring refresh. Run `/career-navigator:pattern-analysis` to update job-scout weights.

### 4. Output format

Keep this short:
```
Application update processed.
Refresh: {high-priority | standard | none}
Resolved outcomes: {n}
{optional one-line nudge}
```

## Guardrails

- Do not overwrite tracker records from this workflow; this skill is advisory/orchestration only
- Do not claim refreshed weights unless analyst/pattern-analysis has actually run
- Keep output concise and action-oriented
