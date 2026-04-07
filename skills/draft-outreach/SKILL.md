---
name: draft-outreach
description: "Produces send-ready outreach copy (LinkedIn, email, InMail) from user intent and optional networking-strategist handoffs. Invokes writer. Prior communication history is folded in by default when mail/calendar connectors exist—via contact-context and ContactContextBrief—unless the user skips or the message is truly generic/cold with no named recipient."
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

0. **Prior communication history (enrichment — default for named recipients):** Outreach to a **specific person** or **known contact at a company** should be **grounded in real mail/calendar context** when the host allows—not guesswork.

   1. If a **ContactContextBrief** is **already** in chat → use it as-is (full block to **`writer`**).
   2. Else if **Gmail/M365 inbox** and/or **calendar** tools appear in **this session** → run **`contact-context`** end-to-end **before** invoking **`writer`**, unless the user explicitly says to **skip** history (“no prior thread,” “brand-new contact,” “template only”) or the ask is purely generic with **no** named recipient yet. **Do not** invent threads.
   3. Else (**no** mail/calendar tools in session) → still invoke **`writer`**, but pass a single line: **`Prior communication:`** *not retrieved — inbox/calendar tools not available in this session; do not imply prior email or meetings.*

   If the user says they **sent** mail but the address was wrong or search is empty, follow **`contact-context`** **“User said they sent”**; **`email_address_notes`** carries address candidates. Include **`calendar_notes`**, **`upcoming_meetings`**, and **`warm_networking`** in the handoff when present—if **`upcoming_meetings`** is non-empty, outreach should **not** read as a cold first touch.

1. Read `{user_dir}/CareerNavigator/profile.md` and **`{user_dir}/CareerNavigator/voice-profile.md`** (create stub if missing).
2. **Voice preflight:** If `voice-profile.md` has **no** user-pasted block under **`## User writing samples`** or **`## User writing samples (launch)`** (substantive excerpts), **ask before** invoking **`writer`**: paste **2–5 LinkedIn posts** or short professional writing; mention optional **launch voice harvest** (résumé/CV/cover text from disk); user may reply **skip** (**low** voice match). If they paste, append a dated **`## User writing samples`** section. If samples already exist, skip this ask.
3. From conversation, capture: **channel**, **recipient archetype** (title/company if known), **objective** (info chat, referral check-in, post-event ping), and any **StrategistHandoff**, **ContactContextBrief**, or facts the user pasted.
4. Pass a structured brief to **`writer`** in **`draft-outreach`** mode. **Required:** include the full **`## ContactContextBrief`** markdown block when available, **or** the **`Prior communication:`** fallback from step **0**. **`writer`** must thread **summary**, **open_loops**, **hooks_for_writer**, **calendar_notes**, **upcoming_meetings**, and **warm_networking** into the draft when present—see **`agents/writer/AGENT.md`**. **Do not** draft final copy in this skill—delegate.
5. Present **`writer`** output (variants if offered). Remind: connectors support warm threading when available.
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
