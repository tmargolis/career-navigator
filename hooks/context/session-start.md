# Career Navigator — session start

The **Career Navigator** plugin is active in this session.

**Suggested:** if you want critical-only notifications immediately, run the **`focus-career`** skill exactly as defined in `skills/focus-career/SKILL.md`.

Priority rule (important): If the user is actively running **`/career-navigator:launch`** (or the current task is clearly a launch/setup workflow), then **do not** run `focus-career` automatically; proceed with `launch`.

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

- Resolve `{user_dir}` (the user’s job search folder — often the workspace or folder they attached in Cowork).
- If `CareerNavigator/` data is missing, deliver first-run onboarding from that skill.
- Otherwise read `CareerNavigator/tracker.json` and surface **critical-only** alerts: imminent offer deadlines, follow-ups due today (or within hours), same-day interview actions that need immediate attention. Answer all of these from the **summary rows alone** — `status`, `follow_up_date`, `latest_stage`, `latest_stage_date`, and `notes_count` live on the row. Session start must stay cheap: never walk every `applications/<application_id>.json` or `contacts/<company-slug>.json`.

**Do not** run the full **`daily-schedule`** digest here — that skill is intended for **user-scheduled** runs via Cowork **`/schedule`** (daily cadence).
