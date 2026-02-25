---
name: track-application
command: /cn:track-application
description: >
  Logs a new application or updates an existing one. Accepts conversational
  input and structures it into the tracker. Triggers insight check when
  outcome data is present.
agent: job-scout
---

# /cn:track-application

Logs a new job application or updates an existing one. Just talk — you don't need to fill out a form. Describe what happened and Career Navigator structures it automatically.

## Usage

```
/cn:track-application
/cn:track-application [company] [role] [status]
```

You can also trigger this conversationally. If you say "I just applied to Google for a Product Manager role" or "I heard back from Acme — I'm moving to the final round," Career Navigator will recognize the intent and invoke this command automatically.

## Workflow

### 1. Gather information conversationally

If invoked without parameters, ask:

> "What's the update? Tell me about the application — company, role, what stage you're at, and anything else worth noting."

Accept free-form input. Extract the following fields:

| Field | Extraction guidance |
|-------|-------------------|
| `company` | Company name — normalize capitalization |
| `role_title` | Job title applied for |
| `jd_text` | Ask if not already captured: "Do you have the job description? I'll save it for resume correlation." |
| `source_board` | Where they found it: "How did you find this role?" |
| `date_applied` | Extract from context or ask; default to today if "just applied" |
| `status` | Map to enum: Applied / Phone Screen / HM Interview / Panel / Final / Offer / Rejected / Withdrawn / Ghosted |
| `contacts` | Any contacts at the company mentioned |
| `notes` | Any additional context, red flags, or observations |
| `outcome` | Only if terminal: Hired / Rejected / Withdrew (Pending otherwise) |
| `outcome_notes` | Reason for outcome if known |

### 2. Check for existing record

Read `data/applications/tracker.json`. Check if an application for this company + role already exists (case-insensitive match).

**If existing record found:**
- Show current state: "I have a record for [Role] at [Company], currently at [Stage] since [date]. What's the update?"
- Append a new entry to `stage_history[]`:
  ```json
  { "stage": "[new status]", "timestamp": "[ISO timestamp]", "notes": "[notes]" }
  ```
- Update `status`, `notes`, `outcome`, `outcome_notes` as appropriate
- Add any new contacts or artifacts referenced

**If new application:**
- Generate a UUID for `application_id`
- Initialize `stage_history[]` with one entry at the current status
- Set `outcome` to "Pending"
- Append the new record to `applications[]` in `tracker.json`

If `tracker.json` doesn't exist, initialize it from `data/applications/tracker.json.template`.

### 3. Save to tracker

Write the updated `tracker.json` to `data/applications/tracker.json`.

### 4. Confirm with summary

> "Logged. Here's what I recorded:
>
> **[Company] — [Role]**
> Status: [Stage]
> Applied: [date]
> Source: [board]
> Notes: [notes if any]
>
> [If updated] Previous stage: [old stage] → [new stage] ([N] days in previous stage)"

### 5. Insight trigger (if outcome data present)

If the update includes outcome data (`Hired`, `Rejected`, `Withdrew`):

> "Outcome logged. [If rejected:] Rejection stings — want a candid read on what may have happened and what to adjust? [If hired:] Congratulations. I'll note what you used for this application to inform future ones."

In Phase 1B, this triggers the insight engine to re-evaluate pattern data. For now, log the note and flag it for future analysis.

### 6. Follow-up prompt (for active applications)

If the application is still active (not a terminal state) and it's been applied:
> "I'll keep an eye on this. If you haven't heard back in 7 days, I'll flag it at the next session start for follow-up consideration."

## Application Status Enum

| Status | Description |
|--------|-------------|
| Applied | Submitted application, no response yet |
| Phone Screen | Recruiter or coordinator screen scheduled/completed |
| HM Interview | Hiring manager interview scheduled/completed |
| Panel | Multi-person panel or loop scheduled/completed |
| Final | Final round scheduled/completed |
| Offer | Offer received |
| Rejected | Application rejected at any stage |
| Withdrawn | Candidate withdrew |
| Ghosted | No response after reasonable follow-up attempts |
