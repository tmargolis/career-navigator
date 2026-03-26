---
description: Launch Career Navigator setup and initialization workflow.
---

Run the launch workflow for Career Navigator.

Execution requirements:
- Read and follow `skills/launch/SKILL.md` as the source of truth.
- Treat the current working directory (or user-provided folder) as `{user_dir}`.
- Create/validate `CareerNavigator` data files exactly as described by the launch skill.
- If integrations are not configured, provide the connector guidance from the launch skill.
- Do not invent external access; be explicit when tools/connectors are missing.

When complete, provide:
- What was validated/created
- Any data gaps requiring user input
- The exact next command the user should run
