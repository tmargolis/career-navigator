---
name: follow-up
description: >
  Surfaces follow-up priorities across all active applications using
  company-specific response window data. Classifies each application as
  within window, approaching, overdue, or critical. Researches and stores
  response window data for any company not yet on file. Builds FollowUpBrief
  entries and invokes writer for send-ready messages. Phase 2A
  enriches briefs with email/calendar context.
triggers:
  - "follow up on my applications"
  - "what needs a follow-up"
  - "should I follow up"
  - "what should I follow up on"
  - "follow-up queue"
  - "any follow-ups due"
  - "check my follow-ups"
  - "should I follow up on"
  - "how long has it been since I applied"
  - "am I being ghosted"
  - "any overdue applications"
  - "what's taking so long"
---

Surface follow-up priorities for all active applications using company-specific response window data.

## Data files

| File | Purpose |
|---|---|
| `{user_dir}/CareerNavigator/tracker.json` | Active applications with stage history and dates |
| `{user_dir}/CareerNavigator/company-windows.json` | Per-user company response window data, researched on demand |
| `{user_dir}/CareerNavigator/profile.md` | Target companies, industries, and role context |

---

## Workflow

### 1. Load active applications

Read `tracker.json`. Collect all applications where `status` is not `accepted`, `rejected`, `withdrew`, or `ghosted`. These are the applications that need follow-up tracking.

For each active application, extract: `company`, `role`, `date_applied`, `status`, `stage_history` (most recent entry date), `follow_up_date`, `contacts`.

### 2. Load or initialize company-windows.json

Read `{user_dir}/CareerNavigator/company-windows.json`. If it does not exist, initialize it:

```json
{
  "meta": {
    "created": "{today}",
    "version": "1.0",
    "description": "Company-specific hiring response windows for {user's name} — researched from public sources and stored per session"
  },
  "companies": {},
  "size_tier_fallbacks": {
    "startup": {
      "typical_first_response_days": { "min": 3, "max": 14 },
      "follow_up_after_days": 10,
      "notes": "Startups move fast; silence beyond 2 weeks usually means no."
    },
    "mid_market": {
      "typical_first_response_days": { "min": 7, "max": 21 },
      "follow_up_after_days": 14,
      "notes": "Mid-market timelines vary; a single polite follow-up at 2 weeks is standard."
    },
    "enterprise": {
      "typical_first_response_days": { "min": 14, "max": 42 },
      "follow_up_after_days": 21,
      "notes": "Large companies have multi-layer review queues; 3–6 weeks before initial screen is normal."
    }
  }
}
```

### 3. Research missing companies

For each active application's company that is **not already present** in `company-windows.json.companies`, research it now.

**Research method:**

Use web search to find candidate-reported hiring timelines for this specific company and role level. Search for:
- `"{company name}" hiring process response time site:glassdoor.com`
- `"{company name}" recruiter response time PM OR director site:linkedin.com`
- `"{company name}" interview process how long Blind OR Reddit`

From the results, extract:
- Typical days from application to first recruiter contact (range)
- The point at which following up is appropriate (not too early to seem anxious, not so late it's futile)
- Any ATS or process notes specific to this company (e.g., uses Greenhouse, has structured panels, known for slow enterprise hiring)

Store the result in `company-windows.json`:

```json
"Anthropic": {
  "researched_at": "{today}",
  "typical_first_response_days": { "min": 14, "max": 35 },
  "follow_up_after_days": 21,
  "size_tier": "startup",
  "process_notes": "Uses Greenhouse. High application volume for PM/research roles. Recruiter screen typically 3–5 weeks. Structured multi-round process. Following up via Greenhouse portal or LinkedIn is appropriate at 3 weeks.",
  "sources": ["Glassdoor reviews", "LinkedIn recruiter posts", "Blind threads"]
}
```

If web search returns insufficient data for a specific company, fall back to the matching `size_tier_fallbacks` entry and note it:

```json
"Acme Corp": {
  "researched_at": "{today}",
  "typical_first_response_days": null,
  "follow_up_after_days": 14,
  "size_tier": "mid_market",
  "process_notes": "No company-specific data found — using mid-market defaults.",
  "sources": ["size_tier_fallback"]
}
```

Write the updated `company-windows.json` before proceeding.

### 4. Classify each application

For each active application, calculate:
- `days_elapsed` = today − `date_applied`
- `last_activity` = date of the most recent `stage_history` entry
- `days_since_activity` = today − `last_activity`
- `window_max` = `company-windows.json` → `typical_first_response_days.max` for this company

Classify:

| Status | Condition |
|---|---|
| `within_window` | `days_elapsed` ≤ `window_max` |
| `approaching` | `days_elapsed` > 75% of `window_max` and ≤ `window_max` |
| `overdue` | `days_elapsed` > `window_max` and ≤ 1.5× `window_max` |
| `critical` | `days_elapsed` > 1.5× `window_max` |

Applications at `phone_screen` or `interview` stage use `days_since_activity` for the overdue check rather than `days_elapsed` from application — these have a shorter expected cadence (typically 3–7 days between touches).

### 5. Check interview-specific follow-ups

For any application with a `stage_history` entry where `stage` contains "interview" and the entry date is within the last 7 days, check whether a thank-you note has been logged (look for a notes entry with "thank-you" or "thank you" or "follow-up" after the interview date). If not:

- If interview was 0–2 days ago: flag as `thank_you_due`
- If interview was 3–7 days ago: flag as `thank_you_overdue`

### 6. Check offer deadlines

For any application where `offer.deadline` is set, calculate days remaining. Flag as `offer_deadline_approaching` if ≤ 3 days remain.

### 7. Output the follow-up report

Order: critical → offer deadlines → thank-you due/overdue → overdue → approaching → within window.

```
**Follow-up Queue** — {today's date}

{critical count} critical  ·  {overdue count} overdue  ·  {approaching count} approaching

---

🔴 CRITICAL  ({days_elapsed}d elapsed · window was {window_max}d)
  {Company} — {Role}
  Applied {date_applied}. Last activity: {last_activity_description}.
  {1 sentence on what action makes sense now — follow up, move on, or both}

🟡 OVERDUE  ({days_elapsed}d · window {window_min}–{window_max}d)
  {Company} — {Role}
  {1 sentence context}

📬 THANK-YOU DUE
  {Company} — {Role}  (interview {n} days ago)

🟢 APPROACHING  ({days_elapsed}d · window closes in ~{n}d)
  {Company} — {Role}
  {follow_up_after_days} day follow-up point: {follow_up_date}

✓ WITHIN WINDOW
  {Company} — {Role}  (day {days_elapsed} of {window_max})
```

If the queue is empty (all active applications are within window and no thank-yous outstanding):
> "All active applications are within their expected response windows. Nothing to follow up on yet."

### 8. Follow-up copy via writer

For each application classified as `overdue` or `critical` (and `thank_you_due` / `thank_you_overdue`), **do not draft send-ready text in this skill.**

#### 8a. Build FollowUpBrief entries

For each row that needs a message, add an object to a list:

- `company`, `role`
- `stage_kind`: `post_application` | `thank_you_post_interview` | `offer_nudge` | other (infer from `stage_history`)
- `channel`: `email` default; `linkedin` if user or notes indicate
- `recipient_name`, `recipient_title` from `contacts[]` if present—else `null` and use neutral greeting instruction
- `applied_or_event_date`, `days_elapsed` (or interview date for thank-yous)
- `facts_hooks`: 1–3 bullets from `notes` / `stage_history.post_notes`—**no invention**
- `tone`: direct, not sycophantic; 3–5 sentences target for email body
- `phase_2a_context`: `null` — **Phase 2A** will allow inbox/calendar snippets here

Read `{user_dir}/CareerNavigator/profile.md` and **`voice-profile.md`** for sign-off name and voice.

**Voice preflight (once per session before 8b):** If you will invoke **`writer`** and `voice-profile.md` lacks substantive pasted prose under **`## User writing samples`** or **`## User writing samples (launch)`**, ask the user for **2–5 LinkedIn posts** or short writing (or **skip** for neutral tone). Append pastes to `voice-profile.md`. If samples already exist or the user skips, proceed.

#### 8b. Invoke writer

- Use the exact agent name **`writer`** with mode **`follow-up`**. Pass all **FollowUpBrief** objects in one invocation when possible. Retry once on failure.

#### 8c. Present output

Under each application entry, show **`writer`** output (subject line if email, body, LinkedIn variant if requested).

**Phase 2A:** When email/calendar connectors exist, enrich briefs with approved prior-thread context before invoking **`writer`**.

---

## What You Never Do

- Do not mark an application as overdue before its research-backed window has elapsed — do not use the flat 7-day rule
- Do not draft **send-ready** follow-up prose in this skill—only **FollowUpBrief** objects; **`writer`** writes the message
- Do not draft a follow-up for an application still within its window
- Do not fabricate contact names — use "there" if no contact is on file
- Do not store company window data outside of `{user_dir}/CareerNavigator/company-windows.json`
- Do not re-research a company already present in `company-windows.json` unless the entry is more than 90 days old
