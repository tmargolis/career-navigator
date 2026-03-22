---
name: track-application
description: >
  Logs a new application or updates an existing one in tracker.json. Accepts
  conversational input and structures it automatically. Fires when the user
  mentions applying to a job, receiving a callback, scheduling an interview,
  or any other application status event. Also invocable via
  /career-navigator:track-application.
triggers:
  - "I just applied to"
  - "I applied to"
  - "I submitted an application"
  - "log an application"
  - "track this application"
  - "add to my tracker"
  - "I got a callback"
  - "I got a call from"
  - "they reached out"
  - "I have an interview"
  - "I got an interview"
  - "I got rejected"
  - "they rejected me"
  - "I withdrew"
  - "I got an offer"
  - "update my application"
  - "update the status"
---

Log or update an application record in `tracker.json`. Extract as much as possible from what the user said before asking for anything.

## Workflow

### 1. Determine: new record or update?

**If the user is reporting a new application** — check `tracker.json` for an existing entry with the same company name. If a match exists, confirm before creating a duplicate:
> "I see an existing application to {Company} for {Role}. Is this a new application for a different role, or an update to that one?"

**If the user is reporting a status change** (callback, interview, offer, rejection) — find the matching record in `tracker.json` by company and role. If no match exists, create a new record with the reported status.

### 2. Extract fields from conversational input

Parse the user's message for:

| Field | What to look for |
|---|---|
| `company` | Company name |
| `role` | Job title |
| `job_link` | URL if provided |
| `salary_range` | Any comp mention |
| `location` | City, state, remote/hybrid |
| `date_applied` | "today", "yesterday", specific date — convert to YYYY-MM-DD |
| `status` | New status (applied, phone_screen, interview, offer, rejected, etc.) |
| `notes` | Any details the user mentioned (recruiter name, how they found it, impressions) |
| `next_step` | Any follow-up the user mentioned |

Do not ask for fields the user hasn't mentioned unless they are required. Required fields for a new record: `company`, `role`, `status`. Everything else is optional.

### 3. Ask only what's missing (for new records)

If company or role is missing, ask for them concisely:
> "What company and role should I log this for?"

Do not ask for salary, location, or job link unless the user brings them up.

### 4. Write the record

**New application** — append to `applications[]` in `tracker.json`:

```json
{
  "id": "{uuid}",
  "company": "...",
  "role": "...",
  "job_link": "...",
  "salary_range": "...",
  "location": "...",
  "resume_version": null,
  "date_applied": "YYYY-MM-DD",
  "status": "applied",
  "stage_history": [
    { "stage": "applied", "date": "YYYY-MM-DD", "notes": "..." }
  ],
  "contacts": [],
  "notes": "...",
  "next_step": "...",
  "priority": null,
  "artifacts": []
}
```

**Status update** — find the existing record and:
- Update `status` to the new value
- Append a new entry to `stage_history`
- Update `notes` or `next_step` if the user provided new information

**After writing**, recalculate and update `pipeline_summary` counts in `tracker.json`.

### 5. Link artifacts

If the user mentions a resume or cover letter used for this application, find the matching entry in `artifacts-index.json` by filename and link it in the `artifacts[]` array of the application record.

### 6. Confirm

```
Logged: {Company} — {Role}
Status: {status}
{Any next_step or notes worth surfacing}
```

Keep the confirmation to 2–3 lines. Do not echo back every field.
