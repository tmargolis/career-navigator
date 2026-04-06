# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~project tracker` might mean Asana, Linear, Jira, or any other project tracker with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (chat, project tracker, knowledge base, etc.) rather than specific products.

**`.mcp.json` in this repo** may declare Anthropic **HTTP MCP** servers for **Google** mail/calendar (**Gmail**, **Google Calendar**) or **Microsoft 365** as an **alternate** channel (e.g. `https://gmail.mcp.claude.com/mcp`, `https://gcal.mcp.claude.com/mcp`, `https://microsoft365.mcp.claude.com/mcp` under the key **`ms365`**) so hosts that read the project file can load tools the same way as **Connectors**—still **no** tokens in JSON. Pick **either** the Google pair **or** **`ms365`** for Outlook mail and M365 calendar surfaces when you do not use Google workspace connectors. Other host-native connectors (**Indeed**, **Apify**) are added in the **Claude** app **Settings / Customize → Connectors** UI when not wired via project MCP. **Indeed** uses **OAuth in the browser** (Indeed on **secure.indeed.com**); **Apify** uses a token + **Enabled tools** in its connector form. **Gmail**, **Microsoft 365**, and **Google Calendar** use **OAuth** to the user’s (or org’s) account per Anthropic’s integration docs.

## Three-step pattern (every integration)

Use this order for **Indeed**, **Apify**, **Gmail**, **Microsoft 365**, **Google Calendar**, **LinkedIn** (where applicable), and **future** connectors documented in this plugin:

1. **Discover** — **First**, check whether **this chat session** already exposes host tools for that integration (tool names vary). If tools are present and working, the service is **connected** for this session: **stop** for that integration—**do not** ask about setup, OAuth, or browser access unless the user says something is broken.

2. **Configure** — **Only if** step 1 shows tools **missing** or the user confirms the connector is **off / not signed in**: **ask** whether they want to **install or fix** it. **Guide** them through **Connectors** + OAuth or token setup; **they** complete clicks and sign-in **themselves**. **Do not** use **Claude in Chrome** or **computer use** to install, enable, or OAuth connectors.

3. **Browser access** — **Only when** the integration is **not** adequately available via MCP in this session (no tools after configure, or the workflow is **browser-only**, e.g. **LinkedIn** post analytics with no LinkedIn MCP). **Ask** whether to allow **Claude in Chrome** and/or **computer use** for that access (**neither** / Chrome / computer use / both). **Do not** ask step 3 for services that are **already connected** via host tools (e.g. **Indeed** `search_jobs` present—no extra questions).

**Skills** (`skills/launch/SKILL.md`, **`draft-outreach`**, **`linkedin-post-analytics`**, etc.) follow this pattern unless a skill states a narrower exception.

## Connectors for this plugin

| Category | Placeholder | Primary in-repo / host path | Other options |
|----------|-------------|----------------------------|---------------|
| Career | `~~career` | **Indeed** MCP — Claude **Connectors** → **Indeed** → **Connect** → browser OAuth (`search_jobs`, `get_job_details`; connector URL `https://mcp.indeed.com/claude/mcp`) | LinkedIn, Glassdoor, Monster, ZipRecruiter, Dice, Handshake |
| Salary benchmarks | — | **Apify** MCP via Claude **Desktop** connector; **Enabled tools:** `call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search` | Future MCPs; skills should degrade gracefully if Apify is off |
| Storage | `~~storage` | **Google Drive:** recommended **Drive app sync** (or manual backup/restore) for job files (PDF/DOCX/etc.). **OneDrive:** recommended **OneDrive app sync** (or manual backup/restore) for job files (plugin JSON artifacts aren’t reliably file-accessible via Claude’s Microsoft 365 connector). **Dropbox:** recommended **Dropbox app sync** (or manual backup/restore) for job files. | Local filesystem fallback in `{user_dir}` |
| Inbox / Outlook (read) | `~~inbox` | **Gmail** and/or **Microsoft 365** first-party connectors (below) | Future: other hosts’ email MCPs if documented |
| Calendar (Google) | — | **Google Calendar** first-party connector (below) | Outlook/Teams calendar via **Microsoft 365** where enabled |
| Voice (TTS/STT) | — | Optional **Claude Desktop Extension** — install the **`mcp-voice.mcpb`** bundle from the repo’s [GitHub Releases](https://github.com/tmargolis/career-navigator/releases) (see **README.md**). Exposes **`mcp-voice`** MCP tools **`speak`**, **`listen`**. Fully local (Kokoro TTS + faster-whisper STT + webrtcvad). | Text only |

---

## Email & calendar context — Gmail, Microsoft 365, Google Calendar (Phase 2A)

**Goal:** Before **`draft-outreach`**, **`follow-up`**, or **`contact-context`**, the model can search **your** mail for threads with a hiring manager or recruiter and, when **Google Calendar** (or M365 calendar surfaces) is connected, **read past and upcoming meetings** involving that contact—**only after you explicitly approve** each mail or calendar lookup. That turns warm outreach into **evidence-backed** messages (you remember what you promised on a call, and you do not cold-open when a meeting is **already scheduled**).

**Best practice (Anthropic):** Use the **first-party connectors** in the Claude app. They authenticate with **OAuth** (you sign in in the browser; Claude does not ask you to paste Google or Microsoft passwords into chat). Permissions are **delegated**—Claude can only reach mail you can already access. Do **not** configure Gmail or Microsoft 365 by embedding long-lived tokens in `.mcp.json` for this plugin.

### Gmail

- **Already added but off?** In **Connectors**, if **Gmail** appears but the **toggle is off** or it shows **Connect** / **Reconnect**, **`/career-navigator:launch`** Step 6 asks whether to **enable** or **finish OAuth** for **read-only** thread search (no send on the user’s behalf). If Gmail tools already appear in the chat, no need to reinstall.
- **Where:** Claude **Settings** / **Customize** → **Connectors** → **Gmail** → **Connect** → complete **Google** sign-in and consent in the browser.
- **Docs:** [Gmail integration (Claude Docs)](https://claude.com/docs/connectors/google/gmail) · [Google Workspace connectors (Help Center)](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)
- **Behavior (per Anthropic):** Search and analyze email content; citations back to sources. **Claude cannot create, send, or modify emails** through this integration—aligned with Career Navigator’s **read-only** use (summarize threads for drafting in the chat; you send from your client).
- **Plans:** Described as available on **Pro, Max, Team, and Enterprise** in Claude’s Gmail docs (confirm current plan requirements in-product).
- **Org / Workspace:** On **Team / Enterprise**, an **Owner** or **Primary Owner** may need to enable the integration for the workspace before individuals can connect.

### Google Calendar

- **Already added but off?** In **Connectors**, if **Google Calendar** appears but the **toggle is off** or it shows **Connect** / **Reconnect**, **`/career-navigator:launch`** Step 6 asks whether to **enable** or **finish OAuth**. If calendar-related tools already appear in the chat, no need to reinstall.
- **Where:** Claude **Settings** / **Customize** → **Connectors** → **Google Calendar** → **Connect** → complete **Google** sign-in and consent in the browser (same host flow as **Gmail**—separate connector card in the catalog).
- **Docs:** [Google Calendar integration (Claude Docs)](https://claude.com/docs/connectors/google/calendar) · [Google Workspace connectors (Help Center)](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)
- **Behavior (per Anthropic):** Claude can read and reason about your schedule, events, attendees, and availability. **Career Navigator** uses this **only** to summarize **past** and **upcoming** events with a named contact (titles, times, attendees, notes/description fields the host exposes) for **`contact-context`** / **`draft-outreach`**—**after explicit approval** per lookup. **Scheduled** meetings support **warm networking identification** (the relationship is not cold if a future event exists with that contact). Prefer **read-only** framing in chat; do not create or reschedule events on the user’s behalf unless they explicitly ask for that in the session.
- **Plans:** Described as available on **Pro, Max, Team, and Enterprise** in Claude’s Google Calendar docs (confirm in-product).
- **Org / Workspace:** On **Team / Enterprise**, an **Owner** or **Primary Owner** may need to enable the integration for the workspace before individuals can connect (same pattern as Gmail).

### Microsoft 365 (Outlook mail and related)

Outlook mail for Career Navigator is provided through Anthropic’s **Microsoft 365** connector (Outlook, SharePoint, OneDrive, Teams, etc., per product docs).

- **Optional HTTP MCP (same integration, alternate to Connectors UI):** Project **`.mcp.json`** may declare **`ms365`** → **`https://microsoft365.mcp.claude.com/mcp`** so hosts that read the file load M365 tools like **Gmail** / **Google Calendar** HTTP MCP—still **no** secrets in JSON; OAuth in the host when connecting.
- **Where:** Admin enablement may be required for **Team / Enterprise**; then each user **Settings** → **Connectors** → **Microsoft 365** → **Connect** → **Microsoft** OAuth.
- **Docs:** [Microsoft 365 connector (Claude Docs)](https://claude.com/docs/connectors/microsoft/365) · [Enabling and using the Microsoft 365 connector (Help Center)](https://support.claude.com/en/articles/12542951-enabling-and-using-the-microsoft-365-connector) · [Microsoft 365 connector: Security Guide](https://support.claude.com/en/articles/12684923-microsoft-365-connector-security-guide)
- **Behavior (per Anthropic):** **Read-only** access—Claude **cannot** modify, delete, or create content in Outlook (or other M365 surfaces) through the connector; search and analyze email threads and related context you already have access to.
- **Plans:** Claude’s Microsoft 365 documentation states availability for **Team and Enterprise** users; **Global Administrator** setup may be required for the tenant. **Consumer / Pro-only** users who rely on **Outlook.com** should verify whether their host offers a connector path or use **Gmail** if applicable.

### Career Navigator usage rules

1. **Three-step pattern:** **Discover** → **Configure** only if **not** connected → **Browser access** only if MCP is still missing or the flow is browser-only. **Do not** re-prompt for services already connected in-session. See **§ Three-step pattern** above.
2. **Explicit approval:** Skills (**`draft-outreach`**, **`follow-up`**, **`contact-context`**) must **ask once** whether to search **mail** and/or **calendar** for a named person or company before calling tools—consistent with **`agents/networking-strategist/AGENT.md`** Phase 2A boundary and **`agents/writer/AGENT.md`**. If only one connector is available, only ask for that scope.
3. **No fabrication:** If connectors are off or the user declines, **do not** invent thread summaries; write copy that stands alone.
4. **Minimum disclosure:** Summarize only what is needed for the outreach or follow-up; prefer thread excerpts and dates over dumping full bodies.
5. **New chat after connect:** If tools do not appear after OAuth, start a **new chat** (same pattern as **Indeed** / **Apify**).

See also **`skills/launch/SKILL.md`** Step 6 for a conversational setup offer during **`/career-navigator:launch`**.

---

## Cloud storage connectors — Google Drive, OneDrive, Dropbox

**Goal:** Keep artifact storage portable across devices while preserving local-first behavior.

**Reality check (important):** Claude Desktop’s **official Google Drive** connector is primarily intended for **native Google Doc files**. For typical job files you’ll store (PDFs, DOCs,  screenshots, resumes, cover letters), Career Navigator recommends portability via:
- Google Drive **application sync** (recommended), or
- manual **backup/restore** of your job search folder.

For **OneDrive**, use **OneDrive application sync** (or manual backup/restore) instead of relying on Claude’s Microsoft 365/OneDrive file access connector, which is geared toward native Microsoft formats (Word/PowerPoint/PDF) rather than the plugin’s JSON artifacts.

For **Dropbox**, use **Dropbox application sync** (or manual backup/restore) instead of relying on host connector file access.

### Three-step pattern (storage)

1. **Discover:** Confirm whether the user already has local cloud-sync enabled for their chosen provider and whether `{user_dir}` is currently available.
2. **Configure:** Only when tools are missing or the user says the connector is off:
   - **Google Drive, OneDrive or Dropbox:** use **application sync** (recommended) or manual backup/restore of the job-search folder, so the folder contents are available locally on every device.
3. **Browser access:** Not required for storage setup in this path. Never use browser automation to click through connector installation or sign-in.

### Career Navigator storage behavior rules

1. **Single active storage choice:** Offer Google Drive, OneDrive, Dropbox, or local-only; avoid forcing multiple cloud connectors in one setup pass.
2. **Local-first fallback:** If storage tools are unavailable, disconnected, or declined, continue using `{user_dir}` local files with no workflow break.
3. **Artifact operation parity:** `save_artifact`, `list_artifacts`, and `get_artifact` behavior should remain consistent from the user perspective regardless of storage backend.
4. **No fabricated sync state:** If a cloud connector is off, state that clearly; do not imply cloud writes or reads occurred.

See also **`skills/launch/SKILL.md`** Step 7 for conversational setup during **`/career-navigator:launch`**.

---

## Voice — Local TTS & STT (Phase 2B, optional MCP bundle)

The **`mcp-voice`** MCP ships as a **Claude Desktop Extension** (`.mcpb`) built from the **`mcp-voice/`** directory in this repository. It uses **Kokoro** for TTS, **faster-whisper** for STT, and **webrtcvad** for end-of-utterance detection on **`listen`**. No cloud credentials — audio stays on the machine.

**Install (end users):**

1. Download **`mcp-voice.mcpb`** from the latest **[GitHub Release](https://github.com/tmargolis/career-navigator/releases)** for this repository (release workflow publishes the bundle when `mcp-voice/` changes).
2. Open **Claude Desktop** → **Settings** (macOS: **⌘ Command + comma**; Windows: **Ctrl + comma**).
3. Open **Extensions**.
4. Drag **`mcp-voice.mcpb`** into that window.
5. Click **Install**.
6. Ensure the **mcp-voice** extension is **enabled**.

Start a **new chat** if **`speak`** / **`listen`** do not appear immediately.

| Step | Action |
| --- | --- |
| **1 — Discover** | If **`speak`** and **`listen`** appear in **this session**, **mcp-voice** is available—**do not** prompt for setup. |
| **2 — Configure** | **Only if** tools are missing: walk through the install steps above (Releases → `.mcpb` → Settings → Extensions → drag → Install → enabled). |
| **3 — Tools** | **`speak(text, voice?, speed?)`** — Kokoro TTS → sounddevice playback. Default voice: `af_heart`. **`listen(duration_seconds?, pause_seconds?, vad_mode?)`** — microphone stream → faster-whisper STT; trailing silence ends recording early. Returns transcript or `"(no speech detected)"`. |

**Prep / mock:** **`interview-coach`** prefers **`speak`** / **`listen`** when present for reading questions aloud and transcribing user answers.

**Fallback:** **`prep-interview`** / **`mock-interview`** work **text-only** when **`mcp-voice`** is not loaded.

**Post-interview capture:** The **`interview-capture`** skill uses **`listen`** to log **user** audio into structured notes; it does **not** replace **`interview-debrief`** for users who skip audio.

**Developers:** The extension entrypoint is **`mcp-voice/server/main.py`** (run via **`uv`** per the bundle manifest). Voice is optional and installed through **Extensions**.
