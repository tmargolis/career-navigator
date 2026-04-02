---
name: daily-schedule
description: "Runs on the daily scheduler. Delivers the routine operating brief (pipeline digest, overdue follow-ups, interview context, conditional pre-interview brief for today, market summary, and action prompts). /career-navigator:morning-brief triggers a focused day-of prep slice only—no separate morning-brief skill."
triggers:
  - "daily job search brief"
  - "career navigator daily digest"
  - "pipeline summary for my applications"
  - "morning job search summary"
  - "run my daily career brief"
  - "/daily-schedule"
  - "/career-navigator:daily-schedule"
  - "/career-navigator:morning-brief"
  - "/morning-brief"
  - "morning brief before my interview"
  - "interviews today brief"
  - "what do I need for my interviews today"
  - "day of interview brief"
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

### 2.6 Monthly career-plan checkpoint (Phase 1F)
If `{user_dir}/CareerNavigator/career-trajectory.md` exists, determine whether it
is stale:
- Prefer to parse the report `as_of` date from the `career_trajectory_v1` JSON
  block, or a heading like `## Career trajectory analysis ({YYYY-MM-DD})`.
- Consider the file "stale" when:
  - the file is missing (first run), OR
  - it was generated more than 30 days ago, OR
  - the tracker has 5 or more new outcome events since the file's `as_of`
    (rejections, offers, accepted completions; do not count `pending`).

If stale, set `career_plan_refresh_due = true`.

### 2.7 Offer evaluation nudge (Phase 1F)
Check tracker for any active application where:
- `status` is `"offer"`
- and `{user_dir}/CareerNavigator/offer-context-{application_id}.json` does
  not exist (offer evaluation has not been run yet)

If any exist, set `offer_evaluation_due = true` and capture up to 3 items
with company, role, and deadline (if present).

### 3. Build the daily operating brief

Read `{user_dir}/CareerNavigator/tracker.json` and `{user_dir}/CareerNavigator/artifacts-index.json`.

Compute:
- Pipeline counts by status (`considering`, `applied`, `phone_screen`, `interview`, `offer`, `accepted`, `rejected`, `withdrew`, `ghosted`)
- Overdue follow-up count (using `follow_up_date` if present)
- **Meetings today** — count `stage_history` entries where **`date` is today** (local) and **`stage`** matches the allowlist below (case-insensitive substring on `stage` string)
- Artifact counts by type (`resume`, `cover_letter`)

#### 3.1 Stage allowlist — interview / recruiter / screen today

Treat a `stage_history` row as **“meeting today”** when `date` equals **today** and any substring match holds:

`interview`, `recruiter`, `phone screen`, `phone_screen`, `hiring manager`, `hm `, `hm interview`, `technical`, `panel`, `onsite`, `executive`, `final round`, `final interview`

Build the list of **applications** that have **at least one** such row today (dedupe by `application id`).

#### 3.2 Pre-interview brief subsection (Phase 2B)

- **If no applications** qualify for meetings today: **omit** the entire **Pre-interview brief** subsection from the output (no placeholder).
- **If one or more qualify:** append a subsection **after** the pipeline block (see §5) titled **`Pre-interview brief (today)`**. For **each** qualifying application, produce **short** bullets only (strict brevity — this is not a full prep doc):
  - One **news or company hook** (only if grounded via tracker/artifacts or verifiable web; else say “no verified headline—run `/career-navigator:prep-interview` for depth”)
  - **2–3 talking points** from `ExperienceLibrary` + role fit
  - **Interviewer** reminder if `contacts[]` or `stage_history[].interviewers` has a name
  - One **watch** line (risk, gap, or follow-up to confirm)

Follow **`agents/interview-coach/AGENT.md`** in **`morning_section`** mode for tone and limits. You are implementing that mode **inline** in this skill (no separate skill file).

### 3.3 `/career-navigator:morning-brief` — focused run

If the user’s message is **primarily** a day-of interview request (triggers include `/career-navigator:morning-brief`, “morning brief before my interview”, etc.):

1. Still perform **§1** validation and, when appropriate, **§2** artifact reconciliation (lightweight).
2. **Skip** the full pipeline table and artifact counts unless the user also asked for a full digest.
3. Output **only**:
   - A one-line header: **`Career Navigator — Pre-interview brief`** [{today}]
   - The **Pre-interview brief (today)** content per **§3.2**, or a clear line that **no** qualifying meetings appear in `tracker.json` for today—then suggest `/career-navigator:track-application` to log scheduled screens and `/career-navigator:prep-interview` for deep prep.

If the user runs a **general daily** trigger, produce the **full** template in **§5**, including **Pre-interview brief** when **§3.2** applies.

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
Meetings today     {n from §3.1 or "None scheduled"}

Artifacts
  Resumes          {n}
  Cover letters    {n}
```

If **§3.2** applies, append:

```
Pre-interview brief (today)
  {per-application concise bullets — see §3.2}
```

Then append at most 3 concise action bullets, highest urgency first. Include:
- If `offer_evaluation_due`: an "Offer evaluation due" bullet with the top item(s)
  and prompt to run `/career-navigator:evaluate-offer`.
- If `career_plan_refresh_due`: a "Career plan refresh due" bullet prompting
  the user to run `/career-navigator:career-plan`.

## Guardrails

- Keep this as the primary place for routine summaries; do not duplicate in `focus-career`
- If data is sparse, say so explicitly and keep recommendations lightweight
- Do not fabricate market news, dates, or deadlines
