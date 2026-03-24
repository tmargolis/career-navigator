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

---

## Plugin Marketplace

Career Navigator will be submitted to the official Claude plugin marketplace at [claude.com/plugins](https://claude.com/plugins) at the end of Phase 1. Once listed, installation will be a single click from the Browse plugins directory — no download required.

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
| **`/career-navigator:launch`** | Run once (or again to reconfigure) | Configure `{user_dir}`, core `CareerNavigator/` files, connectors walkthrough, voice harvest |
| **`session-start`** | New session (hook) or `/schedule` | Critical-only: deadlines, same-day follow-ups, urgent interview actions |
| **`daily-schedule`** | **Recommended:** daily via Cowork **`/schedule`** | Routine digest; runs **`artifact-saved`** when PDF/DOCX artifacts need reconciling |
| **`artifact-saved`** | After saves or from **`daily-schedule`** | Sync **`artifacts-index.json`** with files on disk; analytics handoff stub |

---

### 2. Documents, letters & ATS

| Skill / command | When it runs | Purpose |
|-----------------|--------------|---------|
| **`add-source`** | New resume/CV uploaded or referenced | Ingest into **`ExperienceLibrary.json`** |
| **`tailor-resume`** | JD pasted or “apply to X” intent | Assemble resume via **`resume-coach`**; optional **`content-advisor`** Summary voice |
| **`cover-letter`** | After tailoring or explicit ask | **CoverLetterBrief** → **`content-advisor`** final letter |
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
| **`follow-up`** | Queue / overdue / “ghosted?” | Company windows → **FollowUpBrief** → **`content-advisor`** messages (Phase **2A**: inbox context) |
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
| **`assessment`** | Honest competitiveness vs a role | **`honest-advisor`** gap / repositioning read |

---

### 5. Networking, events & public voice

| Skill / command | When it runs | Purpose |
|-----------------|--------------|---------|
| **`networking-strategy`** | Plan who/when/how to engage | **`networking-strategist`**; messaging handoff → **`content-advisor`** |
| **`network-map`** | Paths to target employers | Narrative + **`network_map_v1`** (graph UI = Phase **2D**) |
| **`event-intelligence`** | Specific event ROI, speaking/CFP | Deep evaluation |
| **`event-radar`** | Ongoing discovery | Local → international, ROI tiers |
| **`draft-outreach`** | DMs, email, InMail drafts | **`content-advisor`** |
| **`content-suggest`** | Post ideas, full drafts | Topics + saved **`linkedin_post`** drafts under **`LinkedIn Posts/`** |
| **`evaluate-post`** | Before publish | Audience + cultural/political/reputational risk vs **`profile.md`** targets |

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
│   ├── tracker.json             — application records with full stage history
│   ├── artifacts-index.json     — index of generated resumes and cover letters
│   ├── company-windows.json     — company-specific response windows for follow-up timing
│   ├── voice-profile.md         — optional: pasted posts + **`content-advisor`** voice notes / `voice_profile_v1`
│   ├── analyst-graph-data.json  — graph-ready analyst output for dashboard rendering
│   └── pipeline-dashboard.html  — generated interactive dashboard artifact
```

No data leaves your machine unless you configure a cloud connector (see [CONNECTORS.md](CONNECTORS.md)).

**To back up**: copy your entire job search folder.

---

## Job Search & Storage Setup

Run `/career-navigator:launch` to configure integrations. The wizard handles everything conversationally — no file editing required.

**Job search:** Career Navigator uses the **Indeed** MCP connector for live listings (`search_jobs`, `get_job_details`). In **Claude Desktop**, add it under **Customize → Connectors**, open **Indeed**, click **Connect**, then complete **Grant access to Indeed** in the browser (Indeed OAuth on **secure.indeed.com** — sign in and **Continue**). Start a **new chat** if tools don’t load. See `/career-navigator:launch` Step 3 for the full walkthrough.

**Storage:** All data is stored locally in your job search folder (`{user_dir}`). Nothing leaves your machine by default. Cloud storage connectors (Google Drive, OneDrive, Dropbox) are available in Phase 2. See [CONNECTORS.md](CONNECTORS.md) for the connector interface.

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

---

## Scheduling & session behavior

**Skills are the payload; Cowork runs them on a cadence you choose.**

- **`session-start`** — Use when you open a session (or schedule a tight cadence with `/schedule` if you want proactive critical checks). Surfaces only urgent items: imminent offer deadlines, follow-ups due today, same-day interview actions.
- **`daily-schedule`** — **Recommended daily** via Claude Cowork **`/schedule`**. Delivers the routine digest (pipeline, follow-ups, interviews today, artifacts). Before counts, it runs **`artifact-saved`** when PDF/DOCX artifacts exist in `{user_dir}` so `artifacts-index.json` stays aligned with disk.
- **`application-update`** — After **`track-application`** updates `tracker.json`, run this workflow in the same turn for refresh guidance and pattern-analysis nudges.
- **`artifact-saved`** — After saving tailored resumes/cover letters, or when `daily-schedule` detects artifact files on disk.

**Cowork host hooks:** `hooks/hooks.json` uses Claude Cowork’s native hook events (per cowork-plugin-management). This repo wires **`SessionStart`** to inject `hooks/context/session-start.md` so the **`session-start`** skill runs at session open.

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

**Phase 1A ([Release v1.1.0](https://github.com/tmargolis/career-navigator/releases/tag/v1.1.0)):** Plugin scaffold, **`/career-navigator:launch`** wizard (builds profile and ExperienceLibrary from existing documents), live job search via Indeed, and session-start automation.

**Phase 1B ([Release v1.2](https://github.com/tmargolis/career-navigator/releases/tag/v1.2)):** Application tracker, ATS scoring, and core workflow skills (tailor-resume, cover-letter, add-source, resume-score) — all auto-triggered from conversational context. `resume-coach`, `analyst`, and `job-scout` agents. `job-scout` performs full outcome-weighted job ranking, proactive opportunity alerts, and transferable skills analysis. Feedback loop connecting outcomes to ExperienceLibrary weights. AI displacement assessment via Anthropic Economic Index. Follow-up timeline intelligence. Pipeline dashboard.

**Phase 1C ([Release v1.3](https://github.com/tmargolis/career-navigator/releases/tag/v1.3)):** `honest-advisor` and `market-researcher` agents. Candid role competitiveness assessment. Skills gap analysis and training ROI engine. Market trend and AI/automation displacement signals (`/career-navigator:suggest-roles`).

**Phase 1D ([Release v1.4](https://github.com/tmargolis/career-navigator/releases/tag/v1.4)):** Expanded `job-scout` outcome weighting and alert quality calibration using growing outcome data. Non-obvious role suggestions based on transferable skills. Market trend monitoring with proactive notifications.

**Phase 1E ([Release v1.5](https://github.com/tmargolis/career-navigator/releases/tag/v1.5)):** **`networking-strategist`** (strategy, maps, events; messaging handoffs only) and **`content-advisor`** (outreach, cover letters, follow-ups, optional resume Summary polish, LinkedIn topics + **saved post drafts** on disk, **`evaluate-post`**; **`voice-profile.md`** via launch + samples).

### Phase 2 — Integrations

Phase 2 connects Career Navigator to the external services that complete the full job search experience. Email and calendar history power warm networking intelligence. The complete interview layer — mock interviews, morning brief, audio capture, and debrief — ships together in Phase 2B so prep and capture are developed as a unified experience. Cloud storage connectors and ATS read-access make the platform portable and employer-system-aware. **Phase 2D** adds BI connectors, LinkedIn automation, and **dashboard/visualization** work deferred from 1E. Sub-phases are independently deployable.

**Phase 2A:** Gmail and Outlook connectors (read-only, OAuth). Google Calendar and Outlook Calendar integration. Contact correspondence history for warm outreach context.

**Phase 2B:** `interview-coach` and `interview-capture` agents. Full mock interview system across all stages and vibes. Morning brief with company news and interviewer research. Post-interview debrief flow. Audio capture via Whisper with full privacy framework, consent model, and cross-jurisdiction recording guidance.

**Phase 2C:** Google Drive, OneDrive, and Dropbox storage connectors. IllinoisJobLink job board connector. ATS read-only connectors for Greenhouse, Workday, and Lever. **Event discovery (placeholder):** connector-backed feeds for **`event-radar`** (Meetup, Eventbrite, Luma, etc.) — spec §15 Phase 2C; not implemented yet.

**Phase 2D:** Power BI streaming dataset connector. Qlik Engine API connector. D3 data export. LinkedIn automation for job search and connection graph access. **Dashboard enhancements:** D3 pipeline **forecast** overlay from **`networking-strategist`** outputs; **voice cadence** metadata on the timeline; **interactive network graph** (or export) from **`network_map_v1`**.

### Phase 3 — Platform Expansion

Hosted API proxy with per-user key management and usage tracking (removes the need for each user to obtain their own JobSearch key; enables monetization). Multi-user and team mode for staffing agencies and career coaches. Plugin marketplace publication. Mobile companion app for on-the-go tracker updates. Salary negotiation and offer evaluation module. Skills gap training integrations with Coursera and LinkedIn Learning.

### Phase 4 — Enterprise & Ecosystem

White-label version for career coaching practices and staffing agencies. API for third-party integrations. Anonymized aggregate benchmarking data. Government employment program integrations and American Job Center partnerships. Veteran and disability-specific pathway modules.

---

## Specification

See [career-navigator-spec.md](references/career-navigator-spec.md) for the full product specification covering all agents, skills, scheduling, data model, and design philosophy.

## Contributing

Contributions welcome. Please open an issue before submitting a pull request for significant changes. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.
```
