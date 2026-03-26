---
name: focus-career
description: "Surfaces only critical, time-sensitive notifications when the user begins a session or runs this skill on a cadence they configured in Cowork. Routine summaries belong in daily-schedule."
triggers:
  - "career navigator critical alerts"
  - "any urgent job search deadlines"
  - "critical application alerts"
  - "session start job search"
  - "focus career"
  - "/career-navigator:focus-career"
  - "/focus-career"
  - "start a new session with career navigator"
---

Run when the user opens a new Cowork session with Career Navigator, **or** when they have scheduled this skill via Cowork **`/schedule`** (optional — for tighter proactive critical checks).

**Host integration:** Claude Cowork’s **`SessionStart`** hook (see `hooks/hooks.json`) injects `hooks/context/session-start.md` so this workflow is explicitly requested at session open. If the user invokes this skill manually without that hook, follow the same steps below.

**Manual fallback:** In environments where the `SessionStart` hook does not auto-fire reliably, run `/career-navigator:focus-career` at the start of the task/session.

This skill is the **critical-only** counterpart to `daily-schedule`. It does **not** replace the daily digest.

## Workflow

### 1. Locate `{user_dir}` and core files

Look at the current working directory and any user-provided path. Use that as `{user_dir}`.

Check for:
- `{user_dir}/CareerNavigator/profile.md`
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`
- `{user_dir}/CareerNavigator/tracker.json`
- `{user_dir}/CareerNavigator/artifacts-index.json`

If these are missing, treat as first run and output:

> **Welcome to Career Navigator**
>
> Run `/career-navigator:launch` to initialize your `CareerNavigator` data files and enable automation.

### 2. Returning session: critical-only checks

Read `{user_dir}/CareerNavigator/tracker.json`.

Only surface **critical** notifications:

1. **Imminent offer deadline**
   - Any application with `status: "offer"` and `offer.deadline` within the next 24 hours.
   - If `{user_dir}/CareerNavigator/offer-context-{application_id}.json` is
     not present for that application, label the critical reason as:
     "Offer evaluation due (run `/career-navigator:evaluate-offer`)."

2. **Imminent follow-up deadline**
   - Any application with `follow_up_date` equal to today.
   - If current local time is within the last 6 hours of the day, mark as critical "due in a few hours."

3. **Interview starting today with no prep logged**
   - Interview-stage entry dated today and no recent prep/debrief notes in the last 48 hours.

Do **not** output full pipeline digest, overdue rollups, or artifact counts here. Those belong to `daily-schedule`.

### 3. Output format

If no critical items:
> **Career Navigator — Session Start**: no critical alerts right now.

If critical items exist:
```
**Career Navigator — Critical Alerts** [{today}]

- {Company} — {Role}: {critical reason} ({time remaining})
- {Company} — {Role}: {critical reason} ({time remaining})
```

After listing alerts, add one action line:
> Run `/career-navigator:track-application` or `/career-navigator:follow-up` to update next steps (or `/career-navigator:evaluate-offer` if an offer evaluation due item appeared).
