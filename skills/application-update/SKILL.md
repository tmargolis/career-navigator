---
name: application-update
description: "Runs whenever tracker records change. Re-checks outcome freshness, flags when job-scout signals should be refreshed, and triggers pattern-analysis nudges at key resolved-outcome milestones."
triggers:
  - "application update"
  - "after I logged an application"
  - "tracker updated"
  - "just updated my application tracker"
  - "after track application"
---

Run **immediately after** the `track-application` skill writes or updates `{user_dir}/CareerNavigator/tracker.json` (same conversation turn). There is no separate plugin hook file — orchestration is conversational or host-defined.

## Workflow

### 1. Read tracker state

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

Read `{user_dir}/CareerNavigator/tracker.json` and inspect the **summary rows only**:
- latest application updates — `status`, `latest_stage`, `latest_stage_date`, and the
  `notes_count` / `stage_count` / `contact_count` counters show what changed without
  opening a single detail file
- `outcome` distribution
- whether `search_performance` exists and has `as_of`

Do not walk `applications/<application_id>.json` or `contacts/<company-slug>.json` here.
Open one detail file only when a specific application's consistency check in **§1.5**
fails and you need to see the underlying array.

### 1.5 Verify the write that just ran

`track-application` writes a **multi-file transaction**. Before advising anything,
confirm it completed for the applications that just changed:
- the row's `detail_file` resolves under `{user_dir}/CareerNavigator/`
- `notes_count` and `stage_count` equal the lengths of the detail file's `notes[]` and
  `stage_history[]`
- `latest_stage` and `latest_stage_date` match the **last** `stage_history` entry
- if the row has a `contacts_file`, its `contact_count` matches the number of entries in
  that file whose `application` equals the row's `application` label

If a check fails, say exactly which file and field are out of sync and tell the user to
re-run `/career-navigator:track-application` for that application. Repair it only per the
write rules in [references/tracker-schema.md](../../references/tracker-schema.md) —
recompute the counters from the detail and contacts files and write every affected file
in the same pass; never patch `tracker.json` alone.

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

- Do not overwrite application records from this workflow; this skill is advisory/orchestration only. The one exception is the consistency repair in §1.5, which recomputes counters and must be written as the full multi-file transaction defined in [references/tracker-schema.md](../../references/tracker-schema.md) — tracker row, detail file, and contacts file together
- Never hand-edit these JSON files; load and re-dump them programmatically (`json.load` / `json.dump` with `indent=2`, `ensure_ascii=False`) and reload to validate
- Do not claim refreshed weights unless analyst/pattern-analysis has actually run
- Keep output concise and action-oriented
