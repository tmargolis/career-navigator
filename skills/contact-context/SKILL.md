---
name: contact-context
description: >
  Surfaces prior email and Google Calendar / M365 calendar context when tools allow—read-only, user-approved. If the user says they sent mail but the address was wrong, trust them and help find a better address (Gmail MCP is unreliable for bounces). Feeds draft-outreach and writer with a ContactContextBrief.
triggers:
  - "contact context"
  - "prior emails with"
  - "what did I last email"
  - "email history with"
  - "before I reach out"
  - "thread context"
  - "Address not found"
  - "wasn't delivered"
  - "550 Invalid Recipient"
  - "email bounced"
  - "/career-navigator:contact-context"
---

Gather **evidence-backed** context from **Gmail** / **Microsoft 365** (and **calendar** when the host exposes it) so **`draft-outreach`** and **`writer`** do not guess about prior conversations.

## Gate (run first)

1. **Connectors:** If **no** Gmail/M365 (inbox) tools **and** **no** host **calendar** tools (e.g. **Google Calendar**, Outlook/Teams calendar via **Microsoft 365**) appear in **this session**, **stop** and point to [CONNECTORS.md](CONNECTORS.md) and **`/career-navigator:launch`** Step 6—do **not** invent inbox or calendar access.
2. **Explicit approval:** **Ask once** before calling tools—cover what is available, e.g.  
   > “I can **search your mail** for threads involving **{name or company}** [and **check your calendar** for recent meetings with them / their email]—**read-only**. Approve for this request?”  
   (Include the bracketed calendar sentence only when calendar tools exist and the user wants meeting context.)  
   If the host exposes **only mail** or **only calendar**, ask only for that scope. If **no**, exit with a short note—**no** fabricated summaries.

## Inputs (ask if missing)

- **Contact:** name, email, or LinkedIn-style identifier; **company** (optional but helps disambiguate).
- **Scope:** default = relevant threads in the **last ~12 months**; user may narrow or widen.

## User said they sent — trust them (default)

If the user says they **sent** an email (or it **bounced** / **failed** / **wrong address**), **believe them.** Do **not** spend the session trying to **prove** delivery or **find** a bounce/NDR via the **Gmail MCP** — it is a poor fit for that (operators often don’t apply; results can look like random Inbox/Sent).

**Instead, pivot immediately to helping them find a *correct* email address** (or a short list of **evidence-backed candidates**) for this contact:

1. **`tracker.json`** / **`profile.md`** — any stored email, title, or company for this person.
2. **Mail search that *does* work on MCP:** plain **`Firstname Lastname`**, **`company`**, **`to:`** / **`from:`** with a **simple** address or domain (one clause at a time). Look at **Sent** and **Inbox** for **real threads** (signatures, forwards, calendar invites), not **`mailer-daemon`** unless the user **explicitly** asks you to hunt a bounce.
3. **Reasonable variants** — alternate **domains** (parent vs subsidiary), **`first.last`**, **`firstlast`**, **`flast`** — label each as **guess** vs **cited** from a source.
4. **Ask the user** to paste an address from **LinkedIn**, the company site, or a prior reply when the connector can’t confirm.
5. Put candidates and confidence in **`email_address_notes`**; explain in **`search_method_notes`** that **bounce search was skipped** (MCP limitation) and the user’s send attempt is **taken at their word**.

**Optional bounce lookup:** Only if the user **explicitly** asks you to find the bounce message **and** approves spending time on it: try **`from:mailer-daemon`** (single token) and **read** a few recent system messages for this address/name — but **do not** treat “no result” as proof of anything. Prefer the user pasting the bounce from **Gmail web** if needed.

## Name search (when the thread isn’t found)

If step **2** (below) doesn’t surface a clear thread, search mail for the contact’s **full name** as plain text (e.g. **`Jordan Kim`**), then **name + company**. Prefer **All Mail** / broad scope when the tool allows.

## Workflow

1. Read `{user_dir}/CareerNavigator/profile.md` and **`tracker.json`** (`applications[].contacts[]`, `networking[]`) for any **known** facts about this person—do not contradict tracker evidence. **If inbox tools are missing** in this session, skip mail search below and note in **caveats**. **If calendar tools are missing**, skip the calendar step and set **calendar_notes** to "—".
2. With **approval**, use host **Gmail** / **Microsoft 365** tools to **search** and **read** relevant threads (by address, domain, company, plain name). **Read-only:** do not send, draft, or delete mail. Skip if step **1** determined there are no inbox tools.
3. **Calendar (when tools exist and approval includes calendar):** Use **Google Calendar** and/or **Microsoft 365** calendar tools to find **events** in the agreed window (default ~12 months) where the contact appears as **attendee** (email match) or where **title/description/location** plausibly reference the person or company. Summarize **when**, **meeting title**, and any **notes or descriptions** the host returns—especially **commitments** or **next steps** written in the event. **Read-only:** do not create, move, or delete events unless the user explicitly asks outside this skill’s scope.
4. **If the user says they sent mail** (failed delivery, wrong address, or “I already emailed them”): follow **“User said they sent — trust them (default)”** above — **address resolution first**; **no** mandatory bounce/NDR hunt via MCP.
5. **Name fallback:** If mail search did not surface a **clear** thread and the user did **not** frame this as “I sent / bad address,” run **“Name search (when the thread isn’t found)”** above.
6. **Summarize** neutrally: who wrote last, dates, **commitments**, **open loops**, tone; **plus** any **calendar** findings (prior calls, interviews, promised follow-ups). **Quote** sparingly; prefer bullets.
7. Emit a **ContactContextBrief** (markdown block below) for **`writer`** / **`draft-outreach`**.
8. **Offer:** “Want **`draft-outreach`** next with this context folded in?” If **yes**, pass the brief into the next step (user can run **`/career-navigator:draft-outreach`** or continue in chat).

## ContactContextBrief (output block)

```markdown
## ContactContextBrief
- **contact:** {name or best label}
- **company:** {company or "—"}
- **sources_used:** gmail | microsoft_365 | calendar | none (list all that were actually queried)
- **as_of:** {YYYY-MM-DD}
- **summary:** {2–6 bullets: substance of prior exchanges and, if used, recent meetings}
- **calendar_notes:** {dated meetings with this contact—title, commitments from descriptions—or "—" if not searched or nothing found}
- **open_loops:** {promises, unanswered threads, deadlines mentioned—in mail or calendar}
- **hooks_for_writer:** {3 bullets—factual, safe to reference in outreach}
- **email_address_notes:** {candidate addresses for this contact—evidence-backed vs tentative—or "—"}
- **search_method_notes:** {e.g. user confirmed they sent mail; bounce hunt skipped; MCP limits—or "—"}
- **caveats:** {e.g. partial search, connector limits}
```

## Constraints

- **Honest:** Do not invent threads or addresses. Label guesses clearly.
- **User-sent:** If the user says they sent email, **do not** contradict them for lack of bounce proof via MCP.
- **Privacy:** do not paste full bodies unless needed; respect sensitive content.
- **Phase 2A:** Calendar enrichment only when tools exist **and** the user approved calendar scope (combined approval is fine unless the host requires a separate calendar consent step).

## Scheduling

Optional **`/schedule`** before high-stakes outreach weeks; usually **on-demand** before **`draft-outreach`**.
