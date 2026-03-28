---
name: draft-outreach
description: "Produces send-ready outreach copy (LinkedIn, email, InMail) from user intent and optional networking-strategist handoffs. Invokes writer. Phase 2A enriches with email/calendar context."
triggers:
  - "draft outreach"
  - "write a linkedin message"
  - "cold email to"
  - "connection request note"
  - "inmail draft"
  - "/career-navigator:draft-outreach"
---

Invoke **`writer`** in **`draft-outreach`** mode.

## Invocation

- Use the exact agent name **`writer`**. Retry once with the same name if invocation fails.

## Workflow

0. **Prior-thread context:** If the user needs **what you already said** to this person or company—or **recent meetings** (calls, interviews) with them—run **`contact-context`** first (or ask them to)—**do not** guess inbox or calendar history. If a **ContactContextBrief** is already in chat, fold it into the brief to **`writer`** (**`calendar_notes`** when present). If the user says they **sent** mail but the address was wrong or thread search is empty, **`contact-context`** should **trust their send** and focus on **correct recipient email** (not hunting bounces via Gmail MCP)—see that skill’s **“User said they sent”** section; **`email_address_notes`** carries address candidates.
1. Read `{user_dir}/CareerNavigator/profile.md` and **`{user_dir}/CareerNavigator/voice-profile.md`** (create stub if missing).
2. **Voice preflight:** If `voice-profile.md` has **no** user-pasted block under **`## User writing samples`** or **`## User writing samples (launch)`** (substantive excerpts), **ask before** invoking **`writer`**: paste **2–5 LinkedIn posts** or short professional writing; mention optional **launch voice harvest** (résumé/CV/cover text from disk); user may reply **skip** (**low** voice match). If they paste, append a dated **`## User writing samples`** section. If samples already exist, skip this ask.
3. From conversation, capture: **channel**, **recipient archetype** (title/company if known), **objective** (info chat, referral check-in, post-event ping), and any **StrategistHandoff**, **ContactContextBrief**, or facts the user pasted.
4. Pass a structured brief to **`writer`** (see the writer agent instructions). **Do not** draft final copy in this skill—delegate.
5. Present **`writer`** output (variants if offered). Remind: **Phase 2A** adds email/calendar enrichment for warm threading when connectors exist.
6. **Sent confirmation + auto-track:** After presenting the copy, say:
   > "Let me know when you've sent this and I'll log it to your tracker."

   When the user confirms (e.g. "sent", "I sent it", "done", "sent it just now"):
   - Read `{user_dir}/CareerNavigator/tracker.json`
   - If a matching application exists (same company): append to `contacts[].interactions[]`:
     ```json
     { "date": "YYYY-MM-DD", "type": "linkedin | email", "notes": "Sent outreach: {one-line summary of message objective}" }
     ```
     Also append to `notes[]`: `{ "date": "YYYY-MM-DD", "text": "Outreach sent via {channel} to {recipient} — {objective}" }`
     Update `next_step` to "Await response"
   - If no matching application exists but the recipient is at a target company: offer to log a new networking entry in `tracker.json` under `networking[]`
   - Confirm: `Logged: outreach to {recipient} at {company} ({channel}) — {date}`

## Notes

- If the user only has strategy questions, point them to **`networking-strategy`** / **`network-map`** first, then return here for copy.
