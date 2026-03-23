---
name: session-start
description: >
  Runs automatically at the start of every session. Surfaces a brief pipeline
  status check if job search data exists, or delivers onboarding instructions
  on first run.
triggers: []
---

This skill runs automatically on `SessionStart`. Announce that you are running the Career Navigator session startup.

## Workflow

### 1. Find the job search directory

**Look at the current working directory and what the user provided as a directory path**: use it. inform the user of the path to `{user_dir}`

**If no path is found**: go to **First Run**

2. Check for existing data files

After confirming `{user_dir}`, check whether each of the four core data files exists. Handle each independently.

#### Files to check

| File | Path |
|---|---|
| Profile | `{user_dir}/CareerNavigator/profile.md` |
| ExperienceLibrary | `{user_dir}/CareerNavigator/ExperienceLibrary.json` |
| Tracker | `{user_dir}/CareerNavigator/tracker.json` |
| Artifacts index | `{user_dir}/CareerNavigator/artifacts-index.json` |

If none of these can be found, treat this as a first-run session (no data) and go to **First Run**.

### 2. Branch: data exists vs. first run

---

#### First Run (no valid working directory or configs found)

Output this onboarding message:

> **Welcome to Career Navigator**
>
> Your job search companion is installed and ready. To get started:
>
> 1. Run `/career-navigator:setup` — reads your existing resumes and cover letters, builds your profile and ExperienceLibrary, and configures live job search.
>
> That's it. Once setup is complete, every session will open with a live pipeline brief.

---

#### Returning Session (configs found)

Read `CareerNavigator/tracker.json` and `artifacts-index.json` from `{user_dir}`. Then output a brief using the format below.

**Pipeline counts** — count `applications` entries by `status`. Recognized statuses: `considering`, `applied`, `phone_screen`, `interview`, `offer`, `accepted`, `declined`, `inactive`. Group anything unrecognized under `other`.

**Overdue follow-up** — read `{user_dir}/CareerNavigator/company-windows.json` to determine overdue status per application. An application is overdue if:
- `days elapsed since date_applied` exceeds the company's `typical_first_response_days.max` (from `company-windows.json`), AND
- Its `status` is not `accepted`, `declined`, `rejected`, or `inactive`

If `company-windows.json` does not exist or a company is not yet researched, fall back to size-tier defaults: startup = 14d, mid-market = 21d, enterprise = 42d. Do not use a flat 7-day rule.

Applications at `phone_screen` or `interview` stage are overdue if `days_since_last_stage_history_entry` > 7 days (shorter cadence expected at active stages).

**Interviews today** — check `stage_history` entries across all applications for any entry whose `stage` contains "interview" and whose `date` matches today's date (YYYY-MM-DD).

**Artifact inventory** — count entries in `artifacts-index.json` by `type` (`resume` vs. `cover_letter`).

**Output format:**

```
**Career Navigator — Session Brief**  [{today's date}]

Pipeline
  Considering      {n}
  Applied          {n}
  Phone screen     {n}
  Interview        {n}
  Offer            {n}

Overdue follow-up  {n application(s) — list company + role inline if ≤3, otherwise just the count}
Interviews today   {n, or "None scheduled"}

Artifacts
  Resumes          {n}
  Cover letters    {n}
```

Keep it tight — no extra commentary unless there are overdue items, in which case append one line per overdue application:
> ⚠ Overdue: {Company — Role} ({n}d elapsed · window was {window_max}d) — run `/career-navigator:follow-up`

If everything is clean (no overdue, no interviews today, pipeline counts all zero), output:
> **Career Navigator** — No active applications. Run `/career-navigator:search-jobs` to find new opportunities.
```
