---
name: daily-schedule
description: "Runs on the daily scheduler. Delivers the routine operating brief (pipeline digest, overdue follow-ups, interview context, market summary, and action prompts)."
triggers:
  - "daily job search brief"
  - "career navigator daily digest"
  - "pipeline summary for my applications"
  - "morning job search summary"
  - "run my daily career brief"
  - "/career-navigator:daily-schedule"
---

### Scheduling (Claude Cowork)

This skill is designed to run as a **daily scheduled task** using Cowork’s **`/schedule`** (or equivalent). Example payload the user might schedule:

> Run the Career Navigator `daily-schedule` skill for my job search folder. Deliver the daily brief per `skills/daily-schedule/SKILL.md`.

After the first successful run, Cowork typically refines the scheduled prompt with learned paths, connectors, and context.

## Workflow

### 1. Resolve `{user_dir}` and validate data files

Check:
- `{user_dir}/CareerNavigator/profile.md`
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`
- `{user_dir}/CareerNavigator/tracker.json`
- `{user_dir}/CareerNavigator/artifacts-index.json`

If missing, output:
> Daily brief skipped: run `/career-navigator:launch` to initialize Career Navigator.

### 2. Reconcile artifacts before summary

Before computing the brief, scan `{user_dir}` for any PDF/DOCX artifacts.

If one or more artifact files are present, run `artifact-saved` first so
`artifacts-index.json` is synchronized before counts are calculated.

If no artifacts are found, continue without running `artifact-saved`.

### 2.5 Auto-ingest new source documents

Before finalizing the brief, detect whether newly discovered resume/CV-style files are present in `{user_dir}` but not yet represented as source entries in `ExperienceLibrary`.

When such files are found:
- Automatically run `add-source` for each newly discovered source document (no manual prompt required).
- After each successful ingest, re-run `artifact-saved` once to keep `artifacts-index.json` consistent.
- In the final brief, include a one-line note listing how many files were auto-ingested.

If an ingest fails for any file:
- Continue with the daily brief.
- List failed filenames under a short "Needs attention" line.
- Recommend rerunning `/career-navigator:add-source` for those specific files.

### 3. Build the daily operating brief

Read `{user_dir}/CareerNavigator/tracker.json` and `{user_dir}/CareerNavigator/artifacts-index.json`.

Compute:
- Pipeline counts by status (`considering`, `applied`, `phone_screen`, `interview`, `offer`, `accepted`, `rejected`, `withdrew`, `ghosted`)
- Overdue follow-up count (using `follow_up_date` if present)
- Interviews today (`stage_history` entries where stage contains "interview" and date is today)
- Artifact counts by type (`resume`, `cover_letter`)

### 4. Add market and strategy prompts

If user has run market workflows recently, summarize top signal in one line.
If no recent strategy signals exist in tracker data, append:
> Run `/career-navigator:suggest-roles` to refresh strategy signals for job-scout ranking.

If no market brief has been generated recently, append:
> Run `/career-navigator:market-brief` for weekly demand and displacement updates.

### 5. Output format

```
**Career Navigator — Daily Brief** [{today}]

Pipeline
  Considering      {n}
  Applied          {n}
  Phone screen     {n}
  Interview        {n}
  Offer            {n}

Follow-up due      {n}
Interviews today   {n or "None scheduled"}

Artifacts
  Resumes          {n}
  Cover letters    {n}
```

Then append at most 3 concise action bullets, highest urgency first.

## Guardrails

- Keep this as the primary place for routine summaries; do not duplicate in `session-start`
- If data is sparse, say so explicitly and keep recommendations lightweight
- Do not fabricate market news, dates, or deadlines
