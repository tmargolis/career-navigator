# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~project tracker` might mean Asana, Linear, Jira, or any other project tracker with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (chat, project tracker, knowledge base, etc.) rather than specific products.

**`.mcp.json` in this repo** ships with an empty `mcpServers` object. Host-native connectors (**Indeed** for job search, **Apify** for salary, **Gmail** / **Microsoft 365** for inbox context) are added in the **Claude** app **Settings / Customize → Connectors** UI—not by committing secrets to JSON. **Indeed** uses **OAuth in the browser** (Indeed on **secure.indeed.com**); **Apify** uses a token + **Enabled tools** in its connector form. **Gmail** and **Microsoft 365** use **OAuth** to the user’s (or org’s) account per Anthropic’s integration docs.

## Three-step pattern (every integration)

Use this order for **Indeed**, **Apify**, **Gmail**, **Microsoft 365**, **LinkedIn** (where applicable), and **future** connectors documented in this plugin:

1. **Discover** — **First**, check whether **this chat session** already exposes host tools for that integration (tool names vary). If tools are present and working, the service is **connected** for this session: **stop** for that integration—**do not** ask about setup, OAuth, or browser access unless the user says something is broken.

2. **Configure** — **Only if** step 1 shows tools **missing** or the user confirms the connector is **off / not signed in**: **ask** whether they want to **install or fix** it. **Guide** them through **Connectors** + OAuth or token setup; **they** complete clicks and sign-in **themselves**. **Do not** use **Claude in Chrome** or **computer use** to install, enable, or OAuth connectors.

3. **Browser access** — **Only when** the integration is **not** adequately available via MCP in this session (no tools after configure, or the workflow is **browser-only**, e.g. **LinkedIn** post analytics with no LinkedIn MCP). **Ask** whether to allow **Claude in Chrome** and/or **computer use** for that access (**neither** / Chrome / computer use / both). **Do not** ask step 3 for services that are **already connected** via host tools (e.g. **Indeed** `search_jobs` present—no extra questions).

**Skills** (`skills/launch/SKILL.md`, **`draft-outreach`**, **`linkedin-post-analytics`**, etc.) follow this pattern unless a skill states a narrower exception.

## Connectors for this plugin

| Category | Placeholder | Primary in-repo / host path | Other options |
|----------|-------------|----------------------------|---------------|
| Career | `~~career` | **Indeed** MCP — Claude **Connectors** → **Indeed** → **Connect** → browser OAuth (`search_jobs`, `get_job_details`; connector URL `https://mcp.indeed.com/claude/mcp`) | LinkedIn, Glassdoor, Monster, ZipRecruiter, Dice, Handshake |
| Salary benchmarks | — | **Apify** MCP via Claude **Desktop** connector; **Enabled tools:** `call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search` | Future MCPs; skills should degrade gracefully if Apify is off |
| Inbox / Outlook (read) | `~~inbox` | **Gmail** and/or **Microsoft 365** first-party connectors (below) | Future: other hosts’ email MCPs if documented |

---

## Inbox context — Gmail & Microsoft 365 (Phase 2A)

**Goal:** Before **`draft-outreach`**, **`follow-up`**, or **`contact-context`**, the model can search **your** mail for threads with a hiring manager or recruiter—**only after you explicitly approve** that lookup for the session or question. That turns warm outreach into **evidence-backed** messages instead of guesswork.

**Best practice (Anthropic):** Use the **first-party connectors** in the Claude app. They authenticate with **OAuth** (you sign in in the browser; Claude does not ask you to paste Google or Microsoft passwords into chat). Permissions are **delegated**—Claude can only reach mail you can already access. Do **not** configure Gmail or Microsoft 365 by embedding long-lived tokens in `.mcp.json` for this plugin.

### Gmail

- **Already added but off?** In **Connectors**, if **Gmail** appears but the **toggle is off** or it shows **Connect** / **Reconnect**, **`/career-navigator:launch`** Step 6 asks whether to **enable** or **finish OAuth** for **read-only** thread search (no send on the user’s behalf). If Gmail tools already appear in the chat, no need to reinstall.
- **Where:** Claude **Settings** / **Customize** → **Connectors** → **Gmail** → **Connect** → complete **Google** sign-in and consent in the browser.
- **Docs:** [Gmail integration (Claude Docs)](https://claude.com/docs/connectors/google/gmail) · [Google Workspace connectors (Help Center)](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)
- **Behavior (per Anthropic):** Search and analyze email content; citations back to sources. **Claude cannot create, send, or modify emails** through this integration—aligned with Career Navigator’s **read-only** use (summarize threads for drafting in the chat; you send from your client).
- **Plans:** Described as available on **Pro, Max, Team, and Enterprise** in Claude’s Gmail docs (confirm current plan requirements in-product).
- **Org / Workspace:** On **Team / Enterprise**, an **Owner** or **Primary Owner** may need to enable the integration for the workspace before individuals can connect.

### Microsoft 365 (Outlook mail and related)

Outlook mail for Career Navigator is provided through Anthropic’s **Microsoft 365** connector (Outlook, SharePoint, OneDrive, Teams, etc., per product docs).

- **Where:** Admin enablement may be required for **Team / Enterprise**; then each user **Settings** → **Connectors** → **Microsoft 365** → **Connect** → **Microsoft** OAuth.
- **Docs:** [Microsoft 365 connector (Claude Docs)](https://claude.com/docs/connectors/microsoft/365) · [Enabling and using the Microsoft 365 connector (Help Center)](https://support.claude.com/en/articles/12542951-enabling-and-using-the-microsoft-365-connector) · [Microsoft 365 connector: Security Guide](https://support.claude.com/en/articles/12684923-microsoft-365-connector-security-guide)
- **Behavior (per Anthropic):** **Read-only** access—Claude **cannot** modify, delete, or create content in Outlook (or other M365 surfaces) through the connector; search and analyze email threads and related context you already have access to.
- **Plans:** Claude’s Microsoft 365 documentation states availability for **Team and Enterprise** users; **Global Administrator** setup may be required for the tenant. **Consumer / Pro-only** users who rely on **Outlook.com** should verify whether their host offers a connector path or use **Gmail** if applicable.

### Career Navigator usage rules

1. **Three-step pattern:** **Discover** → **Configure** only if **not** connected → **Browser access** only if MCP is still missing or the flow is browser-only. **Do not** re-prompt for services already connected in-session. See **§ Three-step pattern** above.
2. **Explicit approval:** Skills (**`draft-outreach`**, **`follow-up`**, **`contact-context`**) must **ask once** whether to search mail for a named person or company before calling tools—consistent with **`agents/networking-strategist/AGENT.md`** Phase 2A boundary and **`agents/writer/AGENT.md`**.
3. **No fabrication:** If connectors are off or the user declines, **do not** invent thread summaries; write copy that stands alone.
4. **Minimum disclosure:** Summarize only what is needed for the outreach or follow-up; prefer thread excerpts and dates over dumping full bodies.
5. **New chat after connect:** If tools do not appear after OAuth, start a **new chat** (same pattern as **Indeed** / **Apify**).

See also **`skills/launch/SKILL.md`** Step 6 for a conversational setup offer during **`/career-navigator:launch`**.
