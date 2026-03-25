---
name: draft-outreach
description: "Produces send-ready outreach copy (LinkedIn, email, InMail) from user intent and optional networking-strategist handoffs. Invokes content-advisor. Phase 2A enriches with email/calendar context."
triggers:
  - "draft outreach"
  - "write a linkedin message"
  - "cold email to"
  - "connection request note"
  - "inmail draft"
  - "/career-navigator:draft-outreach"
---

Invoke **`content-advisor`** in **`draft-outreach`** mode.

## Invocation

- Use the exact agent name **`content-advisor`**. Retry once with the same name if invocation fails.

## Workflow

1. Read `{user_dir}/CareerNavigator/profile.md` and **`{user_dir}/CareerNavigator/voice-profile.md`** (create stub if missing).
2. **Voice preflight:** If `voice-profile.md` has **no** user-pasted block under **`## User writing samples`** or **`## User writing samples (launch)`** (substantive excerpts), **ask before** invoking **`content-advisor`**: paste **2–5 LinkedIn posts** or short professional writing; mention optional **launch voice harvest** (résumé/CV/cover text from disk); user may reply **skip** (**low** voice match). If they paste, append a dated **`## User writing samples`** section. If samples already exist, skip this ask.
3. From conversation, capture: **channel**, **recipient archetype** (title/company if known), **objective** (info chat, referral check-in, post-event ping), and any **StrategistHandoff** or facts the user pasted.
4. Pass a structured brief to **`content-advisor`** (see `agents/content-advisor/AGENT.md`). **Do not** draft final copy in this skill—delegate.
5. Present **`content-advisor`** output (variants if offered). Remind: **Phase 2A** adds email/calendar enrichment for warm threading when connectors exist.

## Notes

- If the user only has strategy questions, point them to **`networking-strategy`** / **`network-map`** first, then return here for copy.
