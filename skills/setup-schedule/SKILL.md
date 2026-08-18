---
name: setup-schedule
description: "Creates or updates the Career Navigator daily brief as a Cowork scheduled task. Runs automatically each day at the user's preferred time: pipeline digest, Gmail inbox scan, follow-up alerts, and new job recommendations. Also invocable via /career-navigator:setup-schedule."
triggers:
  - "set up daily brief"
  - "schedule my daily brief"
  - "automate my morning brief"
  - "schedule career navigator"
  - "run my brief every day"
  - "set up the daily schedule"
  - "schedule the daily brief"
  - "create daily brief task"
  - "create scheduled task for daily brief"
  - "/career-navigator:setup-schedule"
  - "/setup-schedule"
---

Create or update the Career Navigator daily brief as a Cowork scheduled task. When the task fires each morning, it delivers a full operating brief: pipeline digest, Gmail inbox scan (two-pass strategy to catch missed status emails), follow-up alerts, and top new job recommendations appended to `recommendations.json`.

---

## 1. Verify Career Navigator setup

Read `{user_dir}/CareerNavigator/profile.md`.

If the profile is missing, output:
> Daily schedule not set up: run `/career-navigator:launch` first to initialize Career Navigator.

Then stop.

---

## 2. Check for an existing scheduled task

Load and call `mcp__scheduled-tasks__list_scheduled_tasks`. Look for any task whose `taskName` contains `career-navigator` or whose prompt mentions Career Navigator.

**If a matching task is found:**
- Display its current schedule and a one-line summary of its prompt
- Ask: "A daily brief is already scheduled. Would you like to update the time, update the prompt, or keep it as-is?"
- If the user wants to update: follow Steps 3–5 but use `mcp__scheduled-tasks__update_scheduled_task` with the existing task's ID instead of creating a new one
- If the user wants to keep it: confirm "Your daily brief is already scheduled." and stop

---

## 3. Confirm preferred schedule

Ask: "What time would you like your daily brief? Default is **7:00 AM daily**."

Accept natural language and convert to a cron expression:

| Input | Cron |
|---|---|
| "7am" / "7:00 AM" / default | `0 7 * * *` |
| "6:30am" | `30 6 * * *` |
| "8am weekdays" | `0 8 * * 1-5` |
| "6am every day" | `0 6 * * *` |

If the user confirms the default, proceed without further prompting.

---

## 4. Build the self-contained task prompt

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write. The task prompt below carries its own copy of that instruction, because each scheduled run starts in a fresh session.

Resolve `{user_dir}` to its actual absolute path on disk (e.g. `/Users/jane/career`).

Build the following prompt, substituting the real path everywhere `{actual_user_dir}` appears:

---

```
Run the Career Navigator daily brief.

## Job search folder
{actual_user_dir}

## Data files (all under {actual_user_dir}/CareerNavigator/)
- tracker.json        — one summary row per submitted application: status, outcome,
                        follow_up_date, next_step, plus application, detail_file,
                        contacts_file, notes_count, stage_count, contact_count,
                        latest_stage, latest_stage_date
- applications/<application_id>.json — stage_history[] and notes[] for one application
- contacts/<company-slug>.json       — every contact at one company, each tagged with
                        the application label it belongs to
- recommendations.json — pre-application pipeline: status values considering / pending_decision / pass
- networking.json     — recruiter relationships and LinkedIn post analytics
- artifacts-index.json — resume and cover letter inventory
- profile.md          — target roles, companies, compensation floor

Application data uses the split layout defined in the Career Navigator plugin's
references/tracker-schema.md — read it before any read or write. tracker.json no
longer contains notes, stage_history, or contacts inside applications[]. Compute the
digest from the summary rows alone and open a detail or contacts file only for the
few applications that need one.

## Step 1 — Reconcile artifacts

Before computing the brief, scan {actual_user_dir} for any PDF or DOCX files not yet
in artifacts-index.json. If found, reconcile the index (add missing entries, remove
stale ones) before computing artifact counts.

## Step 2 — Gmail inbox scan (COMPREHENSIVE — run every day without exception)

Run TWO separate Gmail searches to avoid missing application updates:

**Search A — 7-day catch-all:**
Query: newer_than:7d (recruiter OR "your application" OR "thank you for applying" OR
"interview" OR "next steps" OR "we have reviewed" OR "application status" OR
"not moving forward" OR "decided not to" OR "unfortunately" OR "other candidates" OR
"process completed") in:inbox

**Search B — 30-day company backfill:**
Read tracker.json; collect company names from the summary rows whose status is NOT a terminal state
(rejected, withdrawn, expired, declined_by_candidate, ghosted). Build and run:
Query: newer_than:30d ({company_1} OR {company_2} OR ...) (application OR position OR
role OR interview OR recruiter OR "next steps" OR "not moving forward" OR "other
candidates" OR "process completed") in:inbox

For each email found in either search:
- Submission confirmed (thank you / application received) → note as ✅ confirmed;
  cross-check against tracker.json
- Moves forward (interview invite, screen request, assessment link) → flag as
  🔔 ACTION REQUIRED and surface prominently
- Rejection or "process completed" → immediately write the multi-file transaction
  from references/tracker-schema.md; never update one file and leave the others stale:
    - In applications/<application_id>.json (the row's detail_file): append the
      stage_history entry with the EMAIL's date (not today) as the date, and append
      a notes[] entry recording both the email received date AND today's discovery date
    - In tracker.json, on that summary row: set status to "rejected", set
      latest_stage and latest_stage_date from the new stage, bump stage_count and
      notes_count to the new array lengths, and clear follow_up_date (set to null)
    - Recalculate pipeline_summary
- Other recruiter outreach → flag for review

CRITICAL: Always use the DATE OF THE EMAIL (not today) as the rejection/event date
on the stage_history entry (and therefore in latest_stage_date). Note the discovery
gap explicitly (e.g. "Rejection email received
2026-04-24, discovered 2026-05-08").

If Gmail is unavailable: note "Gmail check skipped — run /career-navigator:follow-up
to review manually."

## Step 3 — Compute pipeline counts

From tracker.json summary rows — count by status:
- Applied | Phone screen | Interview | Offer

From recommendations.json — count records where status = "considering":
- Considering (report separately, not inside the applied funnel)

Also compute:
- Follow-up due: summary rows where follow_up_date is today or past
- Meetings today: summary rows where latest_stage_date = today (local) and
  latest_stage matches (case-insensitive substring) any of: interview, recruiter,
  phone screen, phone_screen, hiring manager, hm, hm interview, technical, panel,
  onsite, executive, final round, final interview. Skip rows with stage_count 0.
  Only for a row whose latest_stage_date is LATER than today, read its detail_file
  and scan stage_history[] for a today-dated match — future-dated scheduled stages
  hide today's entry. Never load every detail file for this count.

From artifacts-index.json — count by type: resume | cover_letter

## Step 4 — Search for new job listings

Run /career-navigator:search-jobs. Find the top 2 roles not already in tracker.json
or recommendations.json.

For each new recommendation, append to {actual_user_dir}/CareerNavigator/recommendations.json:
- id: next rec-NNN (increment from max existing)
- status: "considering"
- company, role, job_link, comp_estimate, location, fit_signals, gaps (from search)
- decision_notes: null
- priority, next_step, outcome: "pending"
- artifacts: []

Do NOT add pre-application roles to tracker.json.

## Step 5 — Output format

Career Navigator — Daily Brief  [{today}]

Pipeline
  Considering      {n}  ← recommendations.json, status = "considering"
  Applied          {n}
  Phone screen     {n}
  Interview        {n}
  Offer            {n}

Follow-up due      {n}
Meetings today     {n or "None scheduled"}

Artifacts
  Resumes          {n}
  Cover letters    {n}

Inbox
  {Actionable emails: confirmations ✅, interview requests 🔔, rejections caught,
  other outreach. If nothing actionable: "No new recruiter emails."}

New Recommendations
  {Top 2 new roles added to recommendations.json, with comp estimate and fit signals.
  If none found: "No new roles matched criteria today."}

Then append at most 3 action bullets, highest urgency first, based on:
- Actual follow_up_date values from the tracker.json summary rows
- Approaching response windows (check company-windows.json if present)
- Pending next_step values on the tracker.json summary rows

Append if no strategy_signals key in tracker.json:
> Run /career-navigator:suggest-roles to refresh strategy signals for job-scout ranking.

Append if no market brief in the past 7 days:
> Run /career-navigator:market-brief for weekly demand and displacement updates.

## Constraints
- Do not fabricate dates, deadlines, or market data
- If any data file is missing, note it and skip that section rather than erroring
- Gmail search is read-only — never send, draft, or modify emails
- The 30-day company backfill search MUST run every day — this is the primary
  safeguard against missed rejection or status emails
- New job discoveries go to recommendations.json only — never tracker.json
- Any write that changes application data is a multi-file transaction: tracker.json
  summary row plus the detail file (and contacts file when contacts change)
```

---

## 5. Create (or update) the scheduled task

Load `mcp__scheduled-tasks__create_scheduled_task`.

Create the task with:
- `taskName`: `career-navigator-daily-brief`
- `description`: `Career Navigator daily brief — pipeline digest, Gmail inbox scan, follow-up alerts, and new job recommendations`
- `prompt`: the task prompt built in Step 4 (fully resolved paths, no placeholders)
- `cronExpression`: the cron expression from Step 3

---

## 6. Confirm to the user

```
✅ Daily brief scheduled — runs every day at {time}.

  Skill:    career-navigator:daily-schedule
  Folder:   {user_dir}
  Task:     career-navigator-daily-brief

To adjust the schedule or prompt, say "reschedule my daily brief"
or run /career-navigator:setup-schedule again.
```

---

## Guardrails

- Always use `update_scheduled_task` (not `create`) when a matching task already exists — avoids duplicates
- Prompt must be fully self-contained: no references to "the current session," "above context," or ephemeral state
- Paths in the prompt must be absolute and fully resolved — `{user_dir}` must be replaced before saving
- Gmail search is read-only; never include send/draft/delete instructions in the task prompt
