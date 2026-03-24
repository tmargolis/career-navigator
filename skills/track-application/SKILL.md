---
name: track-application
description: >
  Logs a new application or updates an existing one in tracker.json. Handles
  full conversational tracking: stage history, contact management, interview
  logging, offer capture, outcome recording, and follow-up scheduling. Accepts
  any application event conversationally. Also invocable via
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
  - "I scheduled an interview"
  - "I had an interview"
  - "I met with"
  - "I spoke with the recruiter"
  - "I met the hiring manager"
  - "I got rejected"
  - "they rejected me"
  - "they ghosted me"
  - "I withdrew"
  - "I'm withdrawing"
  - "I got an offer"
  - "they made an offer"
  - "I declined the offer"
  - "I accepted the offer"
  - "I accepted"
  - "negotiating an offer"
  - "update my application"
  - "update the status"
  - "add a contact"
  - "log a contact"
---

Log or update an application record in `tracker.json`. Extract as much as possible from what the user said before asking for anything.

## Application Record Schema

Every application record uses this structure:

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
  "status": "considering | applied | phone_screen | interview | offer | accepted | rejected | withdrew | ghosted",
  "stage_history": [
    {
      "stage": "...",
      "date": "YYYY-MM-DD",
      "notes": "...",
      "interview_type": "phone | video | onsite | panel | technical | executive | null",
      "interviewers": [],
      "post_notes": null
    }
  ],
  "contacts": [
    {
      "name": "...",
      "title": "...",
      "email": null,
      "linkedin": null,
      "relationship": "recruiter | hiring_manager | referral | internal_contact | other",
      "notes": "...",
      "interactions": [
        { "date": "YYYY-MM-DD", "type": "call | email | linkedin | in_person", "notes": "..." }
      ]
    }
  ],
  "notes": [
    { "date": "YYYY-MM-DD", "text": "..." }
  ],
  "follow_up_date": "YYYY-MM-DD",
  "next_step": "...",
  "priority": "high | medium | low | null",
  "referral": { "name": "...", "relationship": "colleague | friend | recruiter | other" },
  "offer": {
    "base": "...",
    "bonus": "...",
    "equity": "...",
    "benefits_notes": "...",
    "deadline": "YYYY-MM-DD",
    "decision": null
  },
  "outcome": "pending | hired | rejected | withdrew",
  "outcome_notes": "...",
  "artifacts": []
}
```

`offer` and `referral` are omitted from new records unless relevant data is present. `outcome` defaults to `"pending"` on all new records.

---

## Workflow

### 1. Route the event

Read `tracker.json`. Determine which operation applies based on what the user said:

| Event type | Route to |
|---|---|
| New application | Section 3 — Write the record |
| Status change (callback, screen, interview, rejection) | Section 3 — Write the record |
| Person at the company mentioned | Section 4 — Contact Management |
| Interview scheduled or debriefed | Section 5 — Interview Logging |
| Offer received or negotiation underway | Section 6 — Offer Capture |
| Final result (hired, rejected, withdrew, ghosted) | Section 7 — Outcome Logging |

A single user message may trigger multiple sections — e.g., "I had an interview with Sarah Chen (recruiter) at Acme" triggers both Interview Logging and Contact Management. Handle all that apply.

**Duplicate check for new applications** — if the user is logging a new application and an entry already exists for the same company, confirm before creating another:
> "I see an existing application to {Company} for {Role}. Is this a new role, or an update to that one?"

---

### 2. Extract fields from conversational input

| Field | What to look for |
|---|---|
| `company` | Company name |
| `role` | Job title |
| `job_link` | URL if provided |
| `salary_range` | Any comp mention |
| `location` | City, state, remote/hybrid |
| `date_applied` | "today", "yesterday", specific date — convert to YYYY-MM-DD |
| `status` | Stage keyword |
| `follow_up_date` | "follow up by", "check back in", "deadline" — convert to YYYY-MM-DD |
| `referral` | "referred by", "through a connection" — capture name and relationship |
| `notes` | Impressions, context, how they found the role, recruiter details |
| `next_step` | Any mentioned next action |
| `priority` | Explicit urgency or interest level |

Required for a new record: `company`, `role`, `status`. Ask only for `company` and `role` if missing — do not prompt for optional fields.

---

### 3. Write the record

**New application** — append to `applications[]`:
- Set `outcome` to `"pending"`
- Initialize `stage_history` with one entry for the current stage
- Initialize `notes` as an array; add one entry if the user provided context
- Set `follow_up_date` using company-window intelligence (see below) — only use a user-provided date if they explicitly stated one

**Setting follow_up_date for new applications:**

Read `{user_dir}/CareerNavigator/company-windows.json`. Look up the company:
- If found: `follow_up_date` = `date_applied` + `follow_up_after_days`
- If not found: research the company using web search (same method as the `follow-up` skill — Glassdoor, LinkedIn, Blind) and store the result in `company-windows.json` before setting the date. If research returns no usable data, fall back to the size-tier default (startup: +10d, mid-market: +14d, enterprise: +21d).

After setting the date, note it in the confirmation output.

**Status update** — find the matching record and:
- Update `status`
- Append a new entry to `stage_history[]`
- Append a new entry to `notes[]` if the user provided new information — never overwrite existing note entries
- Update `follow_up_date` and `next_step` if mentioned

**After any write**, recalculate and update `pipeline_summary` counts in `tracker.json`.

**Immediately after the write**, run the **`application-update`** skill workflow (refresh guidance for job-scout / pattern-analysis nudges) before ending the turn.

---

### 4. Contact Management

When the user mentions a person at the company:

**Adding a new contact** — check `contacts[]` for an existing entry with the same name. If not found, append:

```json
{
  "name": "...",
  "title": "...",
  "email": null,
  "linkedin": null,
  "relationship": "recruiter | hiring_manager | referral | internal_contact | other",
  "notes": "...",
  "interactions": []
}
```

**Logging an interaction** — if the user mentions a conversation, call, email, or meeting with a known contact, append to that contact's `interactions[]`:

```json
{ "date": "YYYY-MM-DD", "type": "call | email | linkedin | in_person", "notes": "..." }
```

**Referral** — if the user was referred to the role, add to the record:

```json
"referral": { "name": "...", "relationship": "colleague | friend | recruiter | other" }
```

Do not ask for email or LinkedIn unless the user provides them.

---

### 5. Interview Logging

**Scheduling an upcoming interview** — append to `stage_history[]`:

```json
{
  "stage": "interview",
  "date": "YYYY-MM-DD",
  "notes": "...",
  "interview_type": "phone | video | onsite | panel | technical | executive",
  "interviewers": ["Name — Title", "..."],
  "post_notes": null
}
```

Set `follow_up_date` to the interview date if it's upcoming.

**Post-interview debrief** — if the user is reporting how an interview went, find the matching `stage_history` entry and populate `post_notes`. Append to `notes[]`:

```json
{ "date": "YYYY-MM-DD", "text": "Post-interview: {what the user shared}" }
```

If the user mentions interviewer names or titles not already in `contacts[]`, add them.

After a completed interview, if no follow-up has been sent, set `follow_up_date` to 2 days out and `next_step` to "Send thank-you note".

---

### 6. Offer Capture

When the user reports receiving an offer:

1. Update `status` to `"offer"` and append to `stage_history[]`
2. Extract offer details from what the user said:

```json
"offer": {
  "base": "...",
  "bonus": "...",
  "equity": "...",
  "benefits_notes": "...",
  "deadline": "YYYY-MM-DD",
  "decision": null
}
```

3. Set `follow_up_date` to the offer deadline if one was mentioned
4. Capture only what the user shared — do not probe for every field

After writing, prompt:
> "Want me to pull market salary data for this role and location to compare against the offer?"

---

### 7. Outcome Logging

When the user reports a final result:

| What they said | `status` | `outcome` |
|---|---|---|
| Accepted, got the job | `accepted` | `hired` |
| Rejected | `rejected` | `rejected` |
| Withdrew, pulled out | `withdrew` | `withdrew` |
| Ghosted, no response | `ghosted` | `rejected` |

Update the record:
- Set `status` and `outcome`
- Set `outcome_notes` to whatever reason or context the user provided
- Append a final entry to `stage_history[]`
- Update `pipeline_summary` — move out of active counts

If outcome is `"hired"`:
> "Congratulations. Want me to mark this as accepted and close out your other active applications?"

If outcome is `"rejected"` and a reason was given:
> "Noted. The analyst will factor this in next time you run a pattern analysis."

**Pattern analysis nudge** — after writing any terminal outcome, count the total number of applications in `tracker.json` where `outcome` is not `"pending"`. If that count is exactly 5, 10, 15, or a multiple of 10 thereafter, append:
> "You now have {count} resolved outcomes — enough to run a pattern analysis. `/pattern-analysis` will update your ExperienceLibrary weights and job-scout scoring based on what's worked so far."

---

### 8. Link artifacts

If the user mentions a resume or cover letter used for this application, find the matching entry in `artifacts-index.json` by filename and link it in `artifacts[]`.

---

### 9. Confirm

```
Logged: {Company} — {Role}
Status: {status}
{follow_up_date if set: "Follow-up: {date}"}
{contact added or interaction logged, one line if applicable}
```

Keep the confirmation to 3–4 lines. Do not echo back every field.
