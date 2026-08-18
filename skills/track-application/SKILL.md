---
name: track-application
description: >
  Logs a new application or updates an existing one in tracker.json. Handles
  full conversational tracking: stage history, contact management, interview
  logging, offer capture, outcome recording, and follow-up scheduling. Accepts
  any application event conversationally. Also invocable via
  /career-navigator:track-application.
triggers:
  - "/track-application"
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
  - "I sent the message"
  - "I sent the outreach"
  - "I sent my follow-up"
  - "I reached out to"
  - "I messaged"
  - "I emailed them"
  - "sent it"
  - "outreach sent"
---

Log or update an application record. Extract as much as possible from what the user said before asking for anything.

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

## Application Record Schema

An application lives across three files. Never put `notes`, `stage_history`, or `contacts` inside a `tracker.json` row.

**Summary row** — `tracker.json` → `applications[]`:

```json
{
  "id": "app-<company-slug>-<role-keywords>",
  "application": "<company> — <role>",
  "company": "...",
  "role": "...",
  "job_link": "...",
  "req_id": null,
  "salary_range": "...",
  "location": "...",
  "resume_version": null,
  "date_applied": "YYYY-MM-DD",
  "status": "applied | phone_screen | interview | offer | accepted | rejected | withdrew | ghosted",
  "detail_file": "applications/app-<company-slug>-<role-keywords>.json",
  "contacts_file": "contacts/<company-slug>.json",
  "notes_count": 0,
  "stage_count": 1,
  "contact_count": 0,
  "latest_stage": "applied",
  "latest_stage_date": "YYYY-MM-DD",
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

**Detail file** — `CareerNavigator/applications/<application_id>.json`, one per application:

```json
{
  "schema": "application_detail_v1",
  "application_id": "app-<company-slug>-<role-keywords>",
  "application": "<company> — <role>",
  "company": "...",
  "role": "...",
  "stage_history": [
    {
      "stage": "...",
      "date": "YYYY-MM-DD",
      "notes": "...",
      "interview_type": "recruiter | hiring_manager | technical | panel | executive | final | null",
      "interviewers": [],
      "post_notes": null
    }
  ],
  "notes": [
    { "date": "YYYY-MM-DD", "text": "..." }
  ]
}
```

**Contacts file** — `CareerNavigator/contacts/<company-slug>.json`, one per company, shared by every application at that company:

```json
{
  "company": "...",
  "contacts": [
    {
      "name": "...",
      "application": "<company> — <role>",
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
  "contact_count": 0
}
```

`offer` and `referral` are omitted from new records unless relevant data is present. `outcome` defaults to `"pending"` on all new records. `contacts_file` and `contact_count` are omitted until the application has a contact. `previous_ids` appears on a row only after a rename.

Edit every one of these files by loading and re-dumping JSON programmatically (`json.load` / `json.dump`, `indent=2`, `ensure_ascii=False`), then reload to verify. Hand-editing raw JSON has corrupted files here before.

---

## Workflow

### 1. Route the event

Read `tracker.json` and match the event to a summary row by `id`, then by `previous_ids` if no `id` matches. Load that row's `detail_file` only when notes or stage history are involved, and its `contacts_file` only when contacts are involved. Determine which operation applies based on what the user said:

| Event type | Route to |
|---|---|
| Role the user is **considering** but hasn't applied to | Write to `recommendations.json` (`recommendations[]`), not `tracker.json` — see Section 3a |
| New application (submitted) | Section 3 — Write the record |
| Status change (callback, screen, interview, rejection) | Section 3 — Write the record |
| Person at the company mentioned | Section 4 — Contact Management |
| Interview scheduled or debriefed | Section 5 — Interview Logging |
| Offer received or negotiation underway | Section 6 — Offer Capture |
| Final result (hired, rejected, withdrew, ghosted) | Section 7 — Outcome Logging |
| Outreach or follow-up message sent | Section 4 — Contact Management (log as interaction) + update `follow_up_date` and `next_step` |

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

### 3a. Pre-application roles (considering)

If the user mentions a role they're interested in but **haven't applied to yet**, write to `{user_dir}/CareerNavigator/recommendations.json` instead of `tracker.json`:

- Append a new entry to `recommendations[]` with: `id` (next `rec-NNN`), `company`, `role`, `job_link`, `comp_estimate`, `location`, `status: "considering"`, `priority`, `next_step`, `notes`, `fit_signals` (from user context if available), `gaps` (if mentioned), `decision_notes: null`, `outcome: "pending"`, `artifacts: []`.
- Do **not** add to `applications[]` or update `pipeline_summary` — pre-application roles are tracked separately.
- When the user later says they applied, move the record: remove from `recommendations[]`, run the full new-application write in Section 3 (mint the `app-<company-slug>-<role-keywords>` id, write the detail file, append the summary row) with `status: "applied"`, and update `pipeline_summary`.

---

### 3. Write the record

**New application** — a multi-file transaction. Do every part or none of them.

1. **Mint the `id`** in the form `app-<company-slug>-<role-keywords>` — e.g. `app-hex-senior-pm`, `app-ocrolus-dir-product-platform`. Slug the company by lowercasing, stripping accents, replacing every run of non-alphanumeric characters with a single hyphen, and trimming leading/trailing hyphens. Pick 2–4 keywords from the role title. **Never mint a UUID, never `app-NNN`, never a date suffix.** Add a disambiguating word from the role only when the id would collide with an existing application at the same company for the same role — a distinguishing word, not a number or date.
2. **Build the `application` label** as exactly `"<company> — <role>"` (em dash, spaces around it). This is the join value contacts point back to.
3. **Write `CareerNavigator/applications/<id>.json`** with `schema: "application_detail_v1"`, `application_id`, `application`, `company`, `role`, `stage_history` holding one entry for the current stage, and `notes` — an array with one entry if the user provided context, otherwise empty.
4. **Append the summary row** to `tracker.json` → `applications[]` with the scalars plus `application`, `detail_file: "applications/<id>.json"`, `notes_count`, `stage_count`, `latest_stage`, and `latest_stage_date` matching the detail file. Add `contacts_file` and `contact_count` only if a contact was captured (Section 4).
5. Set `outcome` to `"pending"`.
6. Set `follow_up_date` using company-window intelligence (see below) — only use a user-provided date if they explicitly stated one.

**Setting follow_up_date for new applications:**

Read `{user_dir}/CareerNavigator/company-windows.json`. Look up the company:
- If found: `follow_up_date` = `date_applied` + `follow_up_after_days`
- If not found: research the company using web search (same method as the `follow-up` skill — Glassdoor, LinkedIn, Blind) and store the result in `company-windows.json` before setting the date. If research returns no usable data, fall back to the size-tier default (startup: +10d, mid-market: +14d, enterprise: +21d).

After setting the date, note it in the confirmation output.

**Status update** — find the matching summary row, load its `detail_file`, and:
- Append a new entry to the detail file's `stage_history[]` — never overwrite or reorder existing entries
- Append a new entry to the detail file's `notes[]` if the user provided new information — never overwrite existing note entries
- On the summary row: update `status`, set `stage_count` to the new `stage_history` length, set `latest_stage` and `latest_stage_date` from the entry just appended, and set `notes_count` to the new `notes` length if a note was added
- Update the row's `follow_up_date` and `next_step` if mentioned

**After any write**, recalculate and update `pipeline_summary` counts in `tracker.json`. `pipeline_summary` only reflects submitted applications (`applications[]`); pre-application roles in `recommendations.json` are not counted here.

**Verify before ending the turn:** every summary row's `detail_file` resolves, `notes_count` and `stage_count` match the detail file's arrays, and `latest_stage` / `latest_stage_date` match the last `stage_history` entry.

**Immediately after the write**, run the **`application-update`** skill workflow (refresh guidance for job-scout / pattern-analysis nudges) before ending the turn.

---

### 4. Contact Management

Contacts live in `CareerNavigator/contacts/<company-slug>.json`, one file per company shared by every application at that company. When the user mentions a person at the company:

**Resolve the file first** — take `contacts_file` from the summary row. If the row has none, list `CareerNavigator/contacts/` and reuse the file already there for this company; never invent a second slug for a company that already has one. If no file exists, derive the slug (lowercase, strip accents, collapse non-alphanumeric runs to single hyphens, trim hyphens) and create `contacts/<slug>.json` as `{ "company": "...", "contacts": [], "contact_count": 0 }`. Then set `contacts_file` on the summary row.

**Adding a new contact** — look in that file's `contacts[]` for an entry with the same `name` **and** the same `application` label. If not found, append:

```json
{
  "name": "...",
  "application": "<company> — <role>",
  "title": "...",
  "email": null,
  "linkedin": null,
  "relationship": "recruiter | hiring_manager | referral | internal_contact | other",
  "notes": "...",
  "interactions": []
}
```

`application` must equal the summary row's `application` label exactly. The same person working two applications at one company gets one entry per application.

**Logging an interaction** — if the user mentions a conversation, call, email, or meeting with a known contact, update that entry in place and append to its `interactions[]`:

```json
{ "date": "YYYY-MM-DD", "type": "call | email | linkedin | in_person", "notes": "..." }
```

**After any contact write** — recompute the contacts file's `contact_count` (total entries in the file) and the summary row's `contact_count` (entries whose `application` matches that row).

**Referral** — if the user was referred to the role, add to the summary row in `tracker.json`:

```json
"referral": { "name": "...", "relationship": "colleague | friend | recruiter | other" }
```

Do not ask for email or LinkedIn unless the user provides them.

---

### 5. Interview Logging

**Scheduling an upcoming interview** — append to the detail file's `stage_history[]`:

```json
{
  "stage": "interview",
  "date": "YYYY-MM-DD",
  "notes": "...",
  "interview_type": "recruiter | hiring_manager | technical | panel | executive | final",
  "interviewers": ["Name — Title", "..."],
  "post_notes": null
}
```

Then on the summary row: set `stage_count` to the new array length, set `latest_stage` and `latest_stage_date` from this entry, and update `status` if the stage moves it. Set `follow_up_date` to the interview date if it's upcoming.

**Post-interview debrief** — if the user is reporting how an interview went, open the detail file, find the matching `stage_history` entry, and populate its `post_notes`. Append to the same file's `notes[]`:

```json
{ "date": "YYYY-MM-DD", "text": "Post-interview: {what the user shared}" }
```

Then set the summary row's `notes_count` to the new `notes` length.

If the user mentions interviewer names or titles not already in the company's contacts file, add them via Section 4 — including the `application` label and the `contact_count` bookkeeping.

After a completed interview, if no follow-up has been sent, set the summary row's `follow_up_date` to 2 days out and `next_step` to "Send thank-you note".

---

### 6. Offer Capture

When the user reports receiving an offer:

1. Append an offer stage to the detail file's `stage_history[]`, then on the summary row set `status` to `"offer"` and refresh `stage_count`, `latest_stage`, and `latest_stage_date`
2. Extract offer details from what the user said and write the `offer` object onto the summary row:

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

Update the record — detail file first, then the summary row:
- Append a final entry to the detail file's `stage_history[]`
- Append a `notes[]` entry to the detail file if the user gave context worth keeping
- On the summary row: set `status` and `outcome`, set `outcome_notes` to whatever reason or context the user provided, and refresh `stage_count`, `latest_stage`, `latest_stage_date`, and `notes_count`
- Update `pipeline_summary` — move out of active counts

If outcome is `"hired"`:
> "Congratulations. Want me to mark this as accepted and close out your other active applications?"

If outcome is `"rejected"` and a reason was given:
> "Noted. The analyst will factor this in next time you run a pattern analysis."

**Pattern analysis nudge** — after writing any terminal outcome, count the total number of applications in `tracker.json` where `outcome` is not `"pending"`. If that count is exactly 5, 10, 15, or a multiple of 10 thereafter, append:
> "You now have {count} resolved outcomes — enough to run a pattern analysis. `/pattern-analysis` will update your ExperienceLibrary weights and job-scout scoring based on what's worked so far."

---

### 8. Link artifacts

If the user mentions a resume or cover letter used for this application, find the matching entry in `artifacts-index.json` by filename and link it in the summary row's `artifacts[]` in `tracker.json`.

---

### 9. Confirm

```
Logged: {Company} — {Role}
Status: {status}
{follow_up_date if set: "Follow-up: {date}"}
{contact added or interaction logged, one line if applicable}
```

Keep the confirmation to 3–4 lines. Do not echo back every field.
