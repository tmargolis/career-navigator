---
description: Show critical-only job search alerts at session start.
---

Run the critical-only session-start workflow for Career Navigator.

Execution requirements:
- Read and follow `skills/focus-career/SKILL.md` as the source of truth.
- Resolve `{user_dir}` from current working directory or user-provided folder.
- If `CareerNavigator` files are missing, provide first-run guidance to run launch.
- Otherwise read tracker data and surface only critical alerts (offer deadlines, follow-up due today, interview-day urgent actions).
- Do not include the full daily digest in this command.
