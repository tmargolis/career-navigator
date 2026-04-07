# Career Navigator

An AI-powered end-to-end job search companion built as a Claude Cowork plugin. Combines the functions of a recruiter, career coach, reverse recruiter, and market analyst into a single intelligent platform that learns what works for you over time.

## What It Does

Career Navigator manages your entire job search in one place:
- Builds targeted resumes from a structured Library of your Experiences
- Scores and optimizes every resume for ATS systems
- Tracks every application with full stage history
- Ranks job opportunities against your skills and outcome history
- Provides candid, honest assessments — not false encouragement

The core differentiator: every application outcome feeds back into the system. Over time, it learns which experience units, resume variants, and communication styles actually work for you.

---

## Installation

### Install via Claude Desktop

1. Download the zip: [direct link](https://github.com/tmargolis/career-navigator/archive/refs/heads/main.zip)
2. In Claude Desktop: **Browse plugins → Personal → Upload a plugin** → select the ZIP
3. Add the directory where your resumes, cover letters, applications, etc. are stored
4. In a new chat with Career Navigator active, run **`/career-navigator:launch`** to start your job search workspace (configuration wizard)

> **Note (Claude Code vs Desktop Cowork):** Career Navigator is designed for **Claude Desktop Cowork** usage. We also maintain a **Claude Code terminal compatibility test surface** so marketplace install/load can be validated in CLI. If you see command-bridge entries in Claude Code, that is expected for testing and does not change the intended Desktop Cowork experience.

---

## Plugin Marketplace

Career Navigator is now published through a GitHub-backed marketplace feed as part of **Phase 1G — Marketplace publication**. For non-technical users, installation remains one click from **Browse plugins** in Claude Desktop.

---

## Quick Start

### 1. Add your job search folder to the chat

In CoWork, click the **+** button (or the folder icon) and add the local folder where your resumes and cover letters live. This gives Career Navigator file access for the session.

### 2. Launch

```
/career-navigator:launch
```

Reads everything in your job search folder — resumes, cover letters, past applications — and automatically builds your profile and ExperienceLibrary. Also configures JobSearch for live job search.

### 3. Drop documents in your folder

Career Navigator monitors your job search folder automatically. Add a resume or cover letter, and it's ingested at the next startup or midnight sync — no command needed.

### 4. Search for matching roles

```
/career-navigator:search-jobs
```

With the **Indeed** MCP connector connected (see **Job Search & Storage Setup** below): live search and ranked results. Without it: `search-jobs` explains how to **Connect** Indeed (browser OAuth) and can fall back to **assisted manual** search strings until the connector is available (`/career-navigator:launch` Step 3).

### 5. Tailor your first resume

```
/career-navigator:tailor-resume
```

Paste a job description. Career Navigator assembles the optimal resume from your ExperienceLibrary, scores it for ATS compatibility, and saves it to your artifact inventory.

---

## Phase 1 skills

Career Navigator is **skill-first**: most workflows start from normal conversation (paste a job description, say you applied somewhere, ask for a market read). Slash commands exist where listed below.

**How the pieces fit** — six domains, roughly in lifecycle order:

```text
Launch & rhythm          →  keep {user_dir} healthy and time-sensitive items visible
        ↓
Documents & ATS          →  ingest sources, tailor résumés/letters, score and fix ATS
        ↓
Discovery & pipeline     →  search roles, log applications, learn from outcomes
        ↓
Market & role strategy   →  demand, salary, adjacent roles, AI risk, training ROI
        ↓
Networking & presence    →  plan, map paths, events, outreach & LinkedIn content
        ↓
Insight & dashboard      →  full analyst report + pipeline visualization
```

---

### 1. Launch & session rhythm

| Skill / command | When it runs | Purpose |
|-----------------|--------------|---------|
| **`/career-navigator:launch`** | Run once (or again to reconfigure) | Configure `{user_dir}`, core `CareerNavigator/` files, connectors walkthrough (Indeed, Apify, Gmail/M365/Google Calendar, LinkedIn analytics), voice harvest; **offers** optional **`linkedin-post-analytics`** if you want a first snapshot |
| **`focus-career`** | New session (hook) or `/schedule` | Critical-only: deadlines, same-day follow-ups, urgent interview actions |
| **`daily-schedule`** | **Recommended:** daily via Cowork **`/schedule`** | Routine digest; runs **`artifact-saved`** when PDF/DOCX artifacts need reconciling; **Pre-interview brief (today)** when tracker shows interview/recruiter/screen **today** |
| **`/career-navigator:morning-brief`** | Day-of only | Same **`daily-schedule`** skill — **focused** output: pre-interview slice only (see `skills/daily-schedule/SKILL.md` §3.3) |
| **`prep-interview`** | “Prep me for…”, recruiter/HM/technical, `/career-navigator:prep-interview` | Full prep via **`interview-coach`**; saves `CareerNavigator/interview-prep/*.md` + **`[prep]`** note in **`tracker.json`** |
| **`mock-interview`** | “Mock interview…”, `/career-navigator:mock-interview` | Practice session: guided/random/adaptive, stage + vibe; **if mode/vibe omitted, defaults are selected** (see skill §2.1); optional **`mcp-voice`** MCP (`speak`, `listen`) per **`CONNECTORS.md`** |
| **`interview-capture`** | Opt-in, `/career-navigator:interview-capture` | **Skill** (not an agent): user-audio STT → structured notes + **`tracker.json`**; §13.1 warning; uses **`mcp-voice`** **`listen`** when the extension is installed |
| **`mine-stories`** | Setup or when new notes/journals appear | One-time/incremental extraction pipeline that builds **`StoryCorpus.json`** from journals, PKM, debriefs, and related documents |
| **`story-retrieval`** | During prep/mock flow | Retrieves competency-matched stories (typically 8-12) from **`StoryCorpus.json`** for STAR mapping without loading full journals |
| **`artifact-saved`** | After saves or from **`daily-schedule`** | Sync **`artifacts-index.json`** with files on disk; analytics handoff stub |

---

### 2. Documents, letters & ATS

| Skill / command | When it runs | Purpose |
|-----------------|--------------|---------|
| **`add-source`** | New resume/CV uploaded or referenced | Ingest into **`ExperienceLibrary.json`** |
| **`tailor-resume`** | JD pasted or “apply to X” intent | Assemble resume via **`resume-coach`**; optional **`writer`** Summary voice |
| **`cover-letter`** | After tailoring or explicit ask | **CoverLetterBrief** → **`writer`** final letter |
| **`resume-score`** | Resume + JD together, no tailor ask | ATS + narrative score |
| **`ats-optimization`** | “Fix ATS”, formatting/keyword issues | Prioritized ATS fixes |
| **`/career-navigator:list-artifacts`** | Explicit | List generated résumés, cover letters, LinkedIn drafts, linked outcomes |

---

### 3. Job discovery, applications & learning loop

| Skill / command | When it runs | Purpose |
|-----------------|--------------|---------|
| **`search-jobs`** | “Find jobs…”, `/career-navigator:search-jobs` | Ranked search (Indeed MCP when connected) |
| **`track-application`** | “I applied…”, status updates | **`tracker.json`** application records |
| **`application-update`** | Right after **`track-application`** writes | Nudge job-scout refresh / **pattern-analysis** at milestones |
| **`follow-up`** | Queue / overdue / “ghosted?” | Company windows → **FollowUpBrief** → **`writer`** messages |
| **`pattern-analysis`** | “What’s converting?”, outcome review | Refresh ExperienceLibrary **performance_weights** from your history |

---

### 4. Market, roles & “what should I do?”

| Skill / command | When it runs | Purpose |
|-----------------|--------------|---------|
| **`market-brief`** | Demand, trends, `/career-navigator:market-brief` | **`market-researcher`**: role demand, displacement, geography |
| **`suggest-roles`** | Adjacent / non-obvious targets, `/career-navigator:suggest-roles` | Role ideas + **`strategy_signals`** for **`job-scout`** |
| **`salary-research`** | Comp questions | Benchmarks via Apify MCP (when connected) |
| **`benchmark`** | “Vs market”, funnel health | Norms by role / level / company size |
| **`ai-analysis`** | AI displacement, future-proofing | Task-level risk + differentiators (**`analyst`**) |
| **`skill-transfer`** | “What else could I do?” | Transferable strengths → adjacent roles/industries |
| **`training-roi`** | Certs, bootcamps, degrees | Cost–time–benefit learning paths |
| **`career-plan`** | “What should my path look like?” | Trajectory planning with near/mid/long horizon + ROI-ranked gap plan |
| **`assessment`** | Honest competitiveness vs a role | **`honest-advisor`** gap / repositioning read |
| **`evaluate-offer`** | Offer decision support | Scenario-aware offer evaluation (employed vs unemployed context) + market fairness check |
| **`compare-offers`** | Multi-offer decisions | Side-by-side offer comparison across comp, fit, trajectory, and risk |
| **`negotiate-offer`** | Compensation negotiation prep | Negotiation strategy + leverage inventory + handoff brief to **`writer`** for final message draft |

---

### 5. Networking, events & public voice

| Skill / command | When it runs | Purpose |
|-----------------|--------------|---------|
| **`networking-strategy`** | Plan who/when/how to engage | **`networking-strategist`**; messaging handoff → **`writer`** |
| **`network-map`** | Paths to target employers | Narrative + **`network_map_v1`** (graph UI = Phase **3**) |
| **`event-intelligence`** | Specific event ROI, speaking/CFP | Deep evaluation |
| **`event-radar`** | Ongoing discovery | Local → international, ROI tiers |
| **`draft-outreach`** | DMs, email, InMail drafts | **`writer`** |
| **`contact-context`** | Before warm outreach | Read-only Gmail/M365 + calendar (when connected): past + **scheduled** meetings → **ContactContextBrief** (**warm_networking**, **upcoming_meetings**) for **`draft-outreach`** / **`writer`** |
| **`content-suggest`** | Post ideas, full drafts | Topics + saved **`linkedin_post`** drafts under **`LinkedIn Posts/`** |
| **`evaluate-post`** | Before publish | Audience + cultural/political/reputational risk vs **`profile.md`** targets |
| **`linkedin-post-analytics`** | Weekly/biweekly or **`/schedule`** | Read-only snapshots of **your** LinkedIn post metrics → **`tracker.json`** `networking[]` (needs **Claude in Chrome** or **computer/browser use** + explicit approval) |

---

### 6. Insight & dashboard

| Skill / command | When it runs | Purpose |
|-----------------|--------------|---------|
| **`report`** | “Full analysis”, integrated read | **`analyst`** + tracker + EL + artifacts |
| **`pipeline-dashboard`** | Dashboard refresh | **`pipeline-dashboard.html`** + graph data |

---

**Slash commands:** Only some skills have a **`/career-navigator:…`** alias (shown above). The rest are invoked by **natural language** matching each skill’s triggers in `skills/<name>/SKILL.md`, or by naming the skill in chat.

---

## Data Storage

Everything lives in one folder — the job search directory you provide. Career Navigator reads your documents from it and saves everything back into it:

```
~/Documents/Job Search/          ← your folder (wherever you choose)
│
├── resume-2026.pdf              ← your source documents
├── resume-staff-eng.docx
├── cover-letter-acme.pdf
│
├── resume-acme-pm-2026-03.md    ← Career Navigator outputs (saved here directly)
├── cover-letter-acme-pm-2026-03.md
│
├── CareerNavigator/
│   ├── profile.md               — your targets, comp floor, differentiators
│   ├── ExperienceLibrary.json   — experience units extracted from source resumes/CVs
│   ├── StoryCorpus.json         — extracted interview story corpus from journals/PKM/debriefs
│   ├── tracker.json             — applications + stage history; optional **`networking[]`** (e.g. **`linkedin_post`** + **`analytics_history`** from **`linkedin-post-analytics`**)
│   ├── artifacts-index.json     — index of generated resumes and cover letters
│   ├── company-windows.json     — company-specific response windows for follow-up timing
│   ├── career-trajectory.md     — career_trajectory_v1 artifact from `career-plan`
│   ├── offer-context-*.json     — persisted offer evaluation context for negotiation/comparison workflows
│   ├── voice-profile.md         — optional: pasted posts + **`writer`** voice notes / `voice_profile_v1`
│   ├── analyst-graph-data.json  — graph-ready analyst output for dashboard rendering
│   ├── interview-prep/          — markdown briefs from **`prep-interview`**
│   └── pipeline-dashboard.html  — generated interactive dashboard artifact
```

No data leaves your machine unless you configure a cloud connector (see [CONNECTORS.md](CONNECTORS.md)).

**To back up**: copy your entire job search folder.

---

## Job Search & Storage Setup

Run `/career-navigator:launch` to configure integrations. The wizard handles everything conversationally — no file editing required.

**Job search (connector-first):** Career Navigator uses the **Indeed** MCP connector for live listings today (`search_jobs`, `get_job_details`), and supports browser/manual fallback for other channels (state/federal boards, niche boards, company-direct/ATS portals). In **Claude Desktop**, add Indeed under **Customize → Connectors**, open **Indeed**, click **Connect**, then complete **Grant access to Indeed** in the browser (Indeed OAuth on **secure.indeed.com** — sign in and **Continue**). Start a **new chat** if tools don’t load. See `/career-navigator:launch` Step 3 for the full walkthrough.

When non-Indeed connectors are unavailable in-session, `search-jobs` can still run via assisted-manual ingestion with normalized fields (`title`, `company`, `location`, `apply_url`, `source`, `retrieval_mode`) and source-aware deduplication/confidence labeling. See [CONNECTORS.md](CONNECTORS.md) and `skills/search-jobs/SKILL.md`.

**Email & calendar context (optional — warm outreach):** Connect **Gmail** and/or **Microsoft 365** and/or **Google Calendar** under **Connectors** so **`draft-outreach`**, **`follow-up`**, **`contact-context`**, and related skills can search **your** mail and summarize **past and upcoming** meetings with a contact **only when you approve** each lookup (upcoming meetings help **warm** identification—avoid cold-open when a call is already scheduled). Anthropic provides **OAuth** in the browser (no passwords in chat). **Microsoft 365** may require **Team/Enterprise** and admin setup. Full steps, plan notes, and official doc links: [CONNECTORS.md](CONNECTORS.md) and `/career-navigator:launch` Step 6.

**PKM story sources (optional — interview story intelligence):** For `mine-stories`, you can pull from PKM systems in addition to local files. Supported paths include the **official Notion connector** and **Capacities via MCP** when available in your host session, with local export/file mining as fallback. See [CONNECTORS.md](CONNECTORS.md) for setup pattern and provenance rules.

**Storage:** All data is stored locally in your job search folder (`{user_dir}`). Nothing leaves your machine by default. You can use cloud-backed storage for portability:
- **Google Drive, OneDrive, Dropbox, etc.:** recommended via **application sync** (or manual backup/restore), since Claude’s native connectors are not reliable for typical job files (JSON/DOCX/etc.).
See [CONNECTORS.md](CONNECTORS.md) for setup and fallback behavior.

### Apify MCP for salary benchmarking (optional — Claude Desktop connector)

`/career-navigator:salary-research` uses **Apify** over MCP. The plugin does **not** put your token in `.mcp.json` (environment variable substitution in MCP `args` is not expanded reliably). Instead, add Apify as a **Desktop connector** in Claude so the app stores your token and tool list for you.

1. Create an account at [apify.com](https://apify.com) and copy your **Personal API token** from **Console → Settings → Integrations**.
2. In Claude Desktop, open **Customize** (or **Settings**) and go to **Connectors**.
3. Under **Desktop**, select **Apify** (may appear as **apify-mcp-server**).
4. Click **Configure** (or open the connector’s settings).
5. Paste your token into **Apify token (Required)**.
6. In **Enabled tools**, replace the default with this exact comma-separated list (no spaces):

   `call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search`

7. Click **Save**, ensure the connector is **enabled**, then **start a new chat** so tools load.

8. Run `/career-navigator:salary-research` or ask for a salary range for a role and location.

Never paste your token into this repository or into chat logs you do not trust. Tool permission prompts (e.g. “needs approval”) are normal — approve when you intend to run salary research.

### Optional: Local voice — TTS & STT (`mcp-voice` MCP bundle)

Mock interviews and **`interview-capture`** can use **local** text-to-speech and speech-to-text via the **`mcp-voice`** Claude Desktop Extension (no Google Cloud account). The server runs on your machine (**Kokoro** + **faster-whisper**).

1. Download **`mcp-voice.mcpb`** from the latest **[GitHub Release](https://github.com/tmargolis/career-navigator/releases)** (the release workflow publishes this asset when anything under **`mcp-voice/`** changes).
2. In **Claude Desktop**, open **Settings** (macOS: **⌘ Command + comma**; Windows: **Ctrl + comma**).
3. Open **Extensions**.
4. Drag **`mcp-voice.mcpb`** into the Extensions window.
5. Click **Install**.
6. Confirm the extension is **enabled**, then start a **new chat** if **`speak`** and **`listen`** tools do not show up.

Details and tool behavior: [CONNECTORS.md](CONNECTORS.md) (Voice section). The repo’s **`.mcp.json`** is only for optional HTTP connectors (e.g. Gmail, Calendar, Microsoft 365); it does **not** include the voice server.

### Optional: Local events — Luma discovery (`mcp-luma` MCP bundle)

For event intelligence workflows (**`event-radar`**, **`event-intelligence`**), you can install the local **`mcp-luma`** Claude Desktop Extension. This provides connector-style Luma event discovery tools from a local MCP bundle.

1. Download **`mcp-luma.mcpb`** from the latest **[GitHub Release](https://github.com/tmargolis/career-navigator/releases)** (published when files under **`mcp-luma/`** change).
2. In **Claude Desktop**, open **Settings** (macOS: **⌘ Command + comma**; Windows: **Ctrl + comma**).
3. Open **Extensions**.
4. Drag **`mcp-luma.mcpb`** into the Extensions window.
5. Click **Install**.
6. Confirm the extension is **enabled**, then start a **new chat** if the Luma tools do not show up.

Details and tool behavior: [CONNECTORS.md](CONNECTORS.md) (Event intelligence section). Like `mcp-voice`, this is a local extension bundle and is not declared in project **`.mcp.json`**.

---

## Scheduling & session behavior

**Skills are the payload; Cowork runs them on a cadence you choose.**

- **`focus-career`** — Use when you open a session (or schedule a tight cadence with `/schedule` if you want proactive critical checks). Surfaces only urgent items: imminent offer deadlines, follow-ups due today, same-day interview actions.
- **`daily-schedule`** — **Recommended daily** via Claude Cowork **`/schedule`**. Delivers the routine digest (pipeline, follow-ups, interviews today, artifacts). Before counts, it runs **`artifact-saved`** when PDF/DOCX artifacts exist in `{user_dir}` so `artifacts-index.json` stays aligned with disk.
- **`daily-schedule`** — also performs a monthly career-plan staleness check and nudges `/career-navigator:career-plan` when trajectory data is outdated.
- **`application-update`** — After **`track-application`** updates `tracker.json`, run this workflow in the same turn for refresh guidance and pattern-analysis nudges.
- **`follow-up-timing`** — when an application reaches offer stage and no evaluation context exists yet, nudge `/career-navigator:evaluate-offer` before deadline pressure compounds.
- **`artifact-saved`** — After saving tailored resumes/cover letters, or when `daily-schedule` detects artifact files on disk.

**Cowork host hooks:** `hooks/hooks.json` uses Claude Cowork’s native hook events (per cowork-plugin-management). This repo wires **`SessionStart`** to inject `hooks/context/session-start.md` so the **`focus-career`** skill runs at session open.

**Important (current behavior):** The `SessionStart` hook is currently **disabled** while reliability issues are investigated. Run **`/career-navigator:focus-career`** manually at the start of each session to get your critical-only briefing.

**recurring** digests are **user-configured in Cowork** (e.g. **`/schedule`** for `daily-schedule`). After the first successful scheduled run, Cowork refines the prompt from what it learned (paths, connectors, context).

---

## Design Principles

- **Honest over encouraging** — candid assessments, not false reassurance
- **Intelligent over mechanical** — outputs adapt based on outcomes, not just inputs
- **Connector-based** — storage and analytics are pluggable; swap backends without changing commands
- **Privacy-first** — all data stays local by default; sensitive features require explicit opt-in
- **Cross-platform** — works on macOS, Windows, and Linux

---

## Roadmap

### Phase 1 — Core Platform

**Phase status tracker**
- Phase 1A: Completed
- Phase 1B: Completed
- Phase 1C: Completed
- Phase 1D: Completed
- Phase 1E: Completed
- Phase 1F: Completed
- Phase 1G: Completed
- Phase 2A: Completed
- Phase 2B: Completed
- Phase 2C: Completed
- Phase 2D: Completed

**Phase 1A ([Release v1.1.0](https://github.com/tmargolis/career-navigator/releases/tag/v1.1.0)):** Plugin scaffold, **`/career-navigator:launch`** wizard (builds profile and ExperienceLibrary from existing documents), live job search via Indeed, and focus-career automation.

**Phase 1B ([Release v1.2](https://github.com/tmargolis/career-navigator/releases/tag/v1.2)):** Application tracker, ATS scoring, and core workflow skills (tailor-resume, cover-letter, add-source, resume-score) — all auto-triggered from conversational context. `resume-coach`, `analyst`, and `job-scout` agents. `job-scout` performs full outcome-weighted job ranking, proactive opportunity alerts, and transferable skills analysis. Feedback loop connecting outcomes to ExperienceLibrary weights. AI displacement assessment via Anthropic Economic Index. Follow-up timeline intelligence. Pipeline dashboard.

**Phase 1C ([Release v1.3](https://github.com/tmargolis/career-navigator/releases/tag/v1.3)):** `honest-advisor` and `market-researcher` agents. Candid role competitiveness assessment. Skills gap analysis and training ROI engine. Market trend and AI/automation displacement signals (`/career-navigator:suggest-roles`).

**Phase 1D ([Release v1.4](https://github.com/tmargolis/career-navigator/releases/tag/v1.4)):** Expanded `job-scout` outcome weighting and alert quality calibration using growing outcome data. Non-obvious role suggestions based on transferable skills. Market trend monitoring with proactive notifications.

**Phase 1E ([Release v1.5.0-alpha.1](https://github.com/tmargolis/career-navigator/releases/tag/v1.5.0-alpha.1)):** **`networking-strategist`** (strategy, maps, events; messaging handoffs only) and **`writer`** (outreach, cover letters, follow-ups, optional resume Summary polish, LinkedIn topics + **saved post drafts** on disk, **`evaluate-post`**; **`voice-profile.md`** via launch + samples).

**Phase 1F ([Release v1.5 alpha 2](https://github.com/tmargolis/career-navigator/releases/tag/v1.5.0-alpha.2)):** `honest-advisor` + `market-researcher` add career planning and decision-grade offer evaluation + negotiation workflows (trajectory planning, scenario-aware evaluation, negotiation handoffs), with `job-scout` + `daily-schedule` consuming the new artifacts on a monthly cadence.

**Phase 1G ([Release v1.5](https://github.com/tmargolis/career-navigator/releases/tag/v1.5.0)):** **Plugin marketplace publication.** Career Navigator becomes installable for non-technical users without requiring them to understand MCP, local tool configuration, or agent runtimes. **Impact:** transforms Career Navigator from a personal tool into a publicly available product with real user validation.

### Phase 2 — Integrations

Phase 2 connects Career Navigator to the external services that complete the full job search experience. Sub-phases are independently deployable.

- **Phase 2A ([Release v2.1.0](https://github.com/tmargolis/career-navigator/releases/tag/v2.1.0)) — Inbox + Calendar Context (Completed):** *before you draft outreach, Career Navigator can (with explicit permission) pull and summarize the relevant email threads and meeting history so your messages are grounded in real context—not guesswork.* **Impact:** warm outreach becomes evidence-based and consistent.
  - **Scope includes**: Gmail/Outlook OAuth (read-only), Google/Outlook Calendar (read-only), optional HTTP MCP entries in **`.mcp.json`** (`gmail`, `google-calendar`, `ms365`), **`contact-context`** + **`draft-outreach`** / **`writer`** enrichment; past and **upcoming** meetings (**`warm_networking`**); **`linkedin-post-analytics`** (read-only own LinkedIn post metrics → **`tracker.json`** via host browser automation + explicit consent; **`networking-strategist`** recommends cadence).

- **Phase 2B ([Release v2.2.0](https://github.com/tmargolis/career-navigator/releases/tag/v2.2.0)) — Full Interview Loop (Prep → Practice → Capture → Debrief) (Completed):** *a single integrated layer for morning brief + mock interviews + post-interview capture so each interview round improves the next.* **Impact:** interviews become a repeatable feedback loop instead of isolated events.
  - **Scope includes**: `interview-coach`, **`interview-capture`** (**skill**), guided/random/adaptive mocks across stages/vibes, morning brief (via **`daily-schedule`**), debrief flow; optional local **`mcp-voice`** MCP extension (**`speak`** / **`listen`**) + opt-in capture with retention/consent framework (see spec §13).

- **Phase 2C ([Release v2.3.0](https://github.com/tmargolis/career-navigator/releases/tag/v2.3.0)) — Portability + Employer-System Awareness (Completed):** *cloud storage connectors and ATS read-only status syncing keep your search durable across devices and aligned with where applications actually live.* **Impact:** fewer manual updates and less “lost state.”
  - **Scope includes**: Google Drive, OneDrive or Dropbox portability via **app sync or manual backup/restore** for job files, IllinoisJobLink connector, Greenhouse/Workday/Lever read-only connectors.

- **Phase 2D ([Release v2.4.0](https://github.com/tmargolis/career-navigator/releases/tag/v2.4.0)) — Event Intelligence + Interview Story Intelligence (Completed):** *event discovery matures into refreshable feeds while interview prep gains stronger story mining from journals, notes, and PKM sources.* **Impact:** better opportunity selection and sharper interview narratives grounded in the user’s own evidence.
  - **Scope includes**: Luma event discovery via local MCP bundle (`mcp-luma`), plus optional Meetup/Eventbrite sourcing through **Claude in Chrome**, **computer use**, or **manual copy/paste**, and interview-story intelligence with a three-layer pipeline: one-time extraction (`mine-stories`), persistent `StoryCorpus.json`, and on-demand competency mapping (`story-retrieval`) for prep/mock workflows.

### Phase 3 — Always-On Career Agent

Phase 3 evolves Career Navigator from “a powerful assistant you sit down with” into an always-on, context-maintaining career operating layer that runs on a cadence and meets you in the channels you already use. This direction reflects industry trends kicked off by **OpenClaw** (persistent threads, async dispatch, event-driven channels) while remaining host-agnostic (Anthropic/Claude and NemoClaw are examples, not dependencies).

- **Morning Digest**: *overnight recruiter replies summarized, stale follow-ups flagged, new matching roles surfaced before you open a laptop.* **Impact:** eliminates daily manual checks across email, job boards, and your tracker.
- **Weekly Market Brief**: *Monday report on role demand shifts, target-company hiring signals, and events/CFPs tied to your targets.* **Impact:** replaces ad-hoc research with a consistent intelligence cadence.
- **Follow-up Alert**: *overdue response detected against benchmarks with a pre-drafted follow-up ready to review and send from mobile.* **Impact:** nothing falls through the cracks; the system manages the pipeline clock.
- **Weekly Insight Report**: *Friday plain-language funnel summary plus one specific positioning adjustment based on what’s converting.* **Impact:** turns a job search from feelings-based to data-informed.
- **Advanced Analytics Exports**: *Power BI, Qlik, and D3 export surfaces for custom reporting and deeper analysis.* **Impact:** gives power users and coaches flexible external dashboards without changing core workflows.
- **Dashboard & Visualization Enhancements**: *pipeline forecast overlay, voice cadence surfacing, and network graph UI upgrades move into Phase 3 delivery.* **Impact:** users get richer planning and relationship visibility in the same always-on operating layer.
- **Dispatch Mobile Layer**: *one message from your phone (“Prep me for my interview tomorrow”) yields a full brief waiting on desktop.* **Impact:** desktop-grade capability from anywhere.
- **Channels (Telegram, Slack)**: *immediate interview debrief and tracker updates from chat, plus flagged prep gaps for next round.* **Impact:** ambient capture replaces “I’ll log this later.”
- **Computer Use (Universal Connector Fallback)**: *when a first-class connector doesn’t exist (or is too restricted) — e.g. LinkedIn workflows — the agent can use UI automation (with explicit approval) to navigate, extract state, draft messages, and stage actions for review.* **Impact:** removes “no connector” as a hard blocker for end-to-end workflows.
- **Projects (Artifact & Workspace Organization)**: *human-created and machine-generated artifacts are grouped by company/role and linked to tracker stages, so it’s always obvious what you sent, what changed, and what to reuse—without hunting across folders or chat history.* **Impact:** reduces artifact sprawl and makes multi-agent work legible across sessions.

### Phase 4 — Enterprise & Ecosystem

- **White-Label for Career Coaches**: *coaches serve 40 clients instead of 8 with daily briefings, pipeline tracking, and market intelligence under their brand.* **Impact:** 5x capacity with higher baseline service quality.
- **Anonymized Benchmark Data**: *aggregate patterns (response windows by stage/role/geo, best days to apply) improve every user’s timing and strategy.* **Impact:** advice gets smarter with scale.
- **Government / American Job Center Integration**: *counselors support large caseloads with automated briefs and follow-up reminders, focusing human time on exceptions.* **Impact:** scales high-quality support to under-resourced populations.
- **Veteran & Disability Pathway Modules**: *translate service roles and constraints into civilian equivalents, map clearance/eligibility, generate hiring-manager-recognizable language.* **Impact:** removes structural translation disadvantages.
- **Early-Career / College Pathway**: *students get a semester-long operating cadence: baseline resume from coursework/projects, internship-specific variants, application tracking, career fair/on-campus recruiting date surfacing, alumni/recruiter outreach drafts, and overdue follow-up alerts.* **Impact:** compresses the early-career recruiting learning curve into repeatable workflows so students don’t miss deadlines or lose opportunities due to inconsistent follow-up.

---

## Specification

See [career-navigator-spec.md](references/career-navigator-spec.md) for the full product specification covering all agents, skills, scheduling, data model, and design philosophy.

## Contributing

Contributions welcome. Please open an issue before submitting a pull request for significant changes. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.
```
