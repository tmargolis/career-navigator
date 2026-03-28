---
name: contact-context
description: >
  Surfaces prior email (and meeting/calendar context when tools allow) for a named contact or company before outreach—read-only, user-approved. Feeds draft-outreach and writer with a ContactContextBrief.
triggers:
  - "contact context"
  - "prior emails with"
  - "what did I last email"
  - "email history with"
  - "before I reach out"
  - "thread context"
  - "/career-navigator:contact-context"
---

Gather **evidence-backed** context from **Gmail** / **Microsoft 365** (and **calendar** when the host exposes it) so **`draft-outreach`** and **`writer`** do not guess about prior conversations.

## Gate (run first)

1. **Connectors:** If **no** Gmail/M365 (or inbox) tools appear in **this session**, **stop** and point to [CONNECTORS.md](CONNECTORS.md) and **`/career-navigator:launch`** Step 6—do **not** invent inbox access.
2. **Explicit approval:** **Ask once** before any search, e.g.  
   > “I can search your mail for threads involving **{name or company}**. Approve **read-only** search for this request?”  
   If **no**, exit with a short note—**no** fabricated summaries.

## Inputs (ask if missing)

- **Contact:** name, email, or LinkedIn-style identifier; **company** (optional but helps disambiguate).
- **Scope:** default = relevant threads in the **last ~12 months**; user may narrow or widen.

## Workflow

1. Read `{user_dir}/CareerNavigator/profile.md` and **`tracker.json`** (`applications[].contacts[]`, `networking[]`) for any **known** facts about this person—do not contradict tracker evidence.
2. With **approval**, use host **Gmail** / **Microsoft 365** / **calendar** tools (names vary) to **search** and **read** relevant threads or events. **Read-only:** do not send, draft, or delete mail.
3. **Summarize** neutrally: who wrote last, dates, **commitments** (“I’ll send X by Friday”), **open loops**, tone. **Quote** sparingly; prefer bullets. **Citations:** link or identify messages when the host provides them.
4. Emit a **ContactContextBrief** (markdown block below) for **`writer`** / **`draft-outreach`**.
5. **Offer:** “Want **`draft-outreach`** next with this context folded in?” If **yes**, pass the brief into the next step (user can run **`/career-navigator:draft-outreach`** or continue in chat).

## ContactContextBrief (output block)

```markdown
## ContactContextBrief
- **contact:** {name or best label}
- **company:** {company or "—"}
- **sources_used:** gmail | microsoft_365 | calendar | none
- **as_of:** {YYYY-MM-DD}
- **summary:** {2–6 bullets: substance of prior exchanges}
- **open_loops:** {promises, unanswered threads, deadlines mentioned}
- **hooks_for_writer:** {3 bullets—factual, safe to reference in outreach}
- **caveats:** {e.g. partial search, old threads only}
```

## Constraints

- **Honest:** If search returns **nothing**, say so—do not invent rapport.
- **Privacy:** do not paste full bodies unless needed; respect sensitive content.
- **Phase 2A:** Calendar enrichment only when tools exist **and** the user approved search scope (or a separate approval for calendar if your host requires it).

## Scheduling

Optional **`/schedule`** before high-stakes outreach weeks; usually **on-demand** before **`draft-outreach`**.
