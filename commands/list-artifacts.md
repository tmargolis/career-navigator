---
name: list-artifacts
command: /cn:list-artifacts
description: >
  Lists all generated artifacts (resumes, cover letters) in the inventory
  with metadata. Supports filtering by type, date range, or outcome.
---

# /cn:list-artifacts

Lists all resumes, cover letters, and other generated documents in your artifact inventory with metadata. Shows ATS scores at time of generation and links outcomes where known.

## Usage

```
/cn:list-artifacts
/cn:list-artifacts resumes
/cn:list-artifacts [company name]
/cn:list-artifacts since [date]
```

## Workflow

### 1. Read the artifact inventory

Read `data/artifacts/index.json`. If it doesn't exist or has no artifacts:
> "No artifacts yet. Run /cn:tailor-resume or /cn:cover-letter to generate your first one."

### 2. Cross-reference with application tracker

Read `data/applications/tracker.json` to look up outcome data for any applications that used these artifacts. This enriches the artifact list with real-world outcomes.

### 3. Render the artifact table

Format as a clean table. Apply any filters specified in the command invocation (type, date, company, outcome).

```
ARTIFACT INVENTORY
────────────────────────────────────────────────────────────────────────────
 #   Type          Date        Role / Target                ATS   Outcome
────────────────────────────────────────────────────────────────────────────
 1   Resume        2026-02-10  Sr. PM @ Acme Corp           88    Rejected
 2   Cover Letter  2026-02-10  Sr. PM @ Acme Corp            —    Rejected
 3   Resume        2026-02-14  Staff Eng @ WidgetCo          92    Applied
 4   Cover Letter  2026-02-14  Staff Eng @ WidgetCo          —    Applied
 5   Resume        2026-02-20  Product Lead @ StartupX       79    Applied
────────────────────────────────────────────────────────────────────────────
Total: 5 artifacts  |  3 resumes  |  2 cover letters
```

For outcomes: show "Applied" (submitted, no response yet), "Phone Screen", "Interview", "Offer", "Rejected", "Withdrawn", "Pending" (artifact created but not submitted), or "—" (not linked to an application).

### 4. Filter options

If the user didn't specify a filter, offer:
> "Filter options:
> - `resumes` — show only resumes
> - `cover-letters` — show only cover letters
> - `[company name]` — show artifacts for a specific company
> - `pending` — show artifacts not yet submitted
> - `since [date]` — show artifacts from a date forward
> - `outcome [hired/rejected/applied]` — filter by outcome"

### 5. Artifact actions

After the table, offer:
> "What would you like to do?
> - View a specific artifact: tell me the number or filename
> - Compare two resume versions side-by-side
> - See which experience units have the best track record across artifacts
> - Score an artifact against a new JD (/cn:resume-score)"

### 6. Performance insight (if outcome data exists)

If any artifacts have outcome data:

```
PERFORMANCE INSIGHT
────────────────────────────────
Resumes scoring 85+: [N] generated, [X]% reached phone screen
Resumes scoring 70–84: [N] generated, [X]% reached phone screen
```

This is an early version of the intelligence feedback loop — more detailed analytics come in Phase 1B with the insight engine and `/cn:pipeline`.
