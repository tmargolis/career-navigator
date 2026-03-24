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
3. In a new chat with Career Navigator active, run the /setup for the career navigator plugin

---

## Plugin Marketplace

Career Navigator will be submitted to the official Claude plugin marketplace at [claude.com/plugins](https://claude.com/plugins) at the end of Phase 1. Once listed, installation will be a single click from the Browse plugins directory — no download required.

---

## Quick Start

### 1. Add your job search folder to the chat

In CoWork, click the **+** button (or the folder icon) and add the local folder where your resumes and cover letters live. This gives Career Navigator file access for the session.

### 2. Run setup

```
/career-navigator:setup
```

Reads everything in your job search folder — resumes, cover letters, past applications — and automatically builds your profile and ExperienceLibrary. Also configures JobSearch for live job search.

### 3. Drop documents in your folder

Career Navigator monitors your job search folder automatically. Add a resume or cover letter, and it's ingested at the next startup or midnight sync — no command needed.

### 4. Search for matching roles

```
/career-navigator:search-jobs
```

With JobSearch configured: searches live job listings automatically and returns ranked results. Without it: generates optimized search strings for Indeed, LinkedIn, and Google Jobs, then ranks the results you bring back.

### 5. Tailor your first resume

```
/career-navigator:tailor-resume
```

Paste a job description. Career Navigator assembles the optimal resume from your ExperienceLibrary, scores it for ATS compatibility, and saves it to your artifact inventory.

---

## All Phase 1ABC Skills

Career Navigator is designed skill-first: most workflows trigger automatically from conversational context — paste a job description and a resume is assembled; say "I just applied to Acme" and the tracker updates. Commands are available for users who prefer explicit invocation.

| Skill / Command | Trigger | Purpose |
|---------|---------|---------|
| `/career-navigator:setup` | Explicit (run first) | Configure job search folder and initialize `CareerNavigator` data files |
| `session-start` | Session open (or user-scheduled via Cowork `/schedule`) | Surface only critical, time-sensitive alerts (for example: offer/follow-up due today) |
| `daily-schedule` | **Recommended:** daily via Cowork `/schedule` | Routine digest; first reconcile artifact inventory with `artifact-saved` when PDF/DOCX files exist in `{user_dir}` |
| `application-update` | After `track-application` writes `tracker.json` | Flag whether job-scout refresh is needed and nudge pattern-analysis at key outcome milestones |
| `artifact-saved` | After saves or from `daily-schedule` | Reconcile `artifacts-index.json` with files present in `{user_dir}`; prepare analytics handoff summary |
| `add-source` | Upload or reference a resume/CV | Add source documents into `CareerNavigator/ExperienceLibrary.json` |
| `tailor-resume` | Paste a job description, or say "I want to apply to X" | Assemble an optimized resume from your ExperienceLibrary for a specific role |
| `cover-letter` | After tailoring a resume, or "write me a cover letter for X" | Generate a targeted cover letter |
| `resume-score` | Share a resume + job description together | Score ATS match, formatting, and narrative strength |
| `ats-optimization` | "optimize for ATS", "fix ATS issues" | Surface ATS-hostile formatting/keyword issues with prioritized fixes |
| `/career-navigator:list-artifacts` | Explicit | View generated resumes/cover letters and linked outcomes |
| `track-application` | "I just applied to X", "log this application" | Log or update a job application |
| `search-jobs` | "find jobs", "search for X roles" | Find and rank job opportunities with outcome + strategy signals |
| `follow-up` | "follow up with X", "is this overdue?" | Generate contextual follow-up messaging based on company response windows |
| `pattern-analysis` | "what's converting?", "analyze my search" | Update ExperienceLibrary performance weights from outcome patterns |
| `skill-transfer` | "what else could I do?" | Map transferable strengths to adjacent role/industry opportunities |
| `ai-analysis` | "AI risk", "future-proof my career" | Assess task-level AI displacement risk and durable differentiators |
| `benchmark` | "how am I doing vs market?" | Compare funnel metrics against role/market/company-size norms |
| `report` | "run full analysis" | Generate integrated analyst report + dashboard data |
| `pipeline-dashboard` | Dashboard generation | Build/open interactive pipeline dashboard |
| `salary-research` | "salary range for X in Y" | Pull live compensation benchmarks via Apify MCP |
| `market-brief` | "market brief", "is this role in demand", "/career-navigator:market-brief" | Surface role demand trends, AI/automation displacement signals, and geographic competitiveness |
| `suggest-roles` | "suggest roles", "what else could I apply to", "/career-navigator:suggest-roles" | Suggest non-obvious role opportunities and write strategy signals that improve job-scout ranking |
| `training-roi` | "training roi", "what should I learn next", "is a bootcamp/certification/degree worth it" | Compare certifications, degrees, bootcamps, and self-study with cost-benefit-time ROI analysis |

All skills are also invocable as explicit commands using the `/career-navigator:` prefix.

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
│   ├── analyst-graph-data.json  — graph-ready analyst output for dashboard rendering
│   └── pipeline-dashboard.html  — generated interactive dashboard artifact
```

No data leaves your machine unless you configure a cloud connector (see [CONNECTORS.md](CONNECTORS.md)).

**To back up**: copy your entire job search folder.

---

## Job Search & Storage Setup

Run `/career-navigator:setup` to configure integrations. The wizard handles everything conversationally — no file editing required.

**Job search:** Career Navigator uses the built-in **Indeed connector** (Claude Cowork integration) for live job listings. No token or configuration required — job search works out of the box.

**Storage:** All data is stored locally in your job search folder (`{user_dir}`). Nothing leaves your machine by default. Cloud storage connectors (Google Drive, OneDrive, Dropbox) are available in Phase 2. See [CONNECTORS.md](CONNECTORS.md) for the connector interface.

### Apify MCP for salary benchmarking (optional manual setup)

`/career-navigator:salary-research` uses Apify via MCP. It is **currently not in the plugin `.mcp.json`** — add the connector in **Claude Desktop Local MCP servers** (or your environment’s MCP settings) when you want salary benchmarking.

1. Create an account at [apify.com](https://apify.com).
2. In Apify, copy your API token from **Console -> Settings -> Integrations**.
3. In Claude Desktop, open **Settings -> Developer -> Local MCP servers** and add Apify (or edit your config file directly).
4. Use a config like:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search",
        "--header",
        "Authorization: Bearer APIFY_API_KEY"
      ]
    }
  }
}
```

5. Restart Claude Desktop (or start a new Cowork chat), then run `/career-navigator:salary-research`.

Use your own token and never commit it to this repository.

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
- Phase 1D: In progress
- Phase 1E: Not started

**Phase 1A ([Release v1.1.0](https://github.com/tmargolis/career-navigator/releases/tag/v1.1.0)):** Plugin scaffold, setup wizard (builds profile and ExperienceLibrary from existing documents), live job search via Indeed, and session-start automation.

**Phase 1B ([Release v1.2](https://github.com/tmargolis/career-navigator/releases/tag/v1.2)):** Application tracker, ATS scoring, and core workflow skills (tailor-resume, cover-letter, add-source, resume-score) — all auto-triggered from conversational context. `resume-coach`, `analyst`, and `job-scout` agents. `job-scout` performs full outcome-weighted job ranking, proactive opportunity alerts, and transferable skills analysis. Feedback loop connecting outcomes to ExperienceLibrary weights. AI displacement assessment via Anthropic Economic Index. Follow-up timeline intelligence. Pipeline dashboard.

**Phase 1C ([Release v1.3](https://github.com/tmargolis/career-navigator/releases/tag/v1.3)):** `honest-advisor` and `market-researcher` agents. Candid role competitiveness assessment. Skills gap analysis and training ROI engine. Market trend and AI/automation displacement signals (`/career-navigator:suggest-roles`).

**Phase 1D (in progress):** Expanded `job-scout` outcome weighting and alert quality calibration using growing outcome data. Non-obvious role suggestions based on transferable skills. Market trend monitoring with proactive notifications.

**Phase 1E:** `networking-strategist`, `content-advisor`, and `event-intelligence` agents. Network map and gap analysis. Event radar. LinkedIn content advisor and post evaluator with cultural risk assessment.

### Phase 2 — Integrations

Phase 2 connects Career Navigator to the external services that complete the full job search experience. Email and calendar history power warm networking intelligence. The complete interview layer — mock interviews, morning brief, audio capture, and debrief — ships together in Phase 2B so prep and capture are developed as a unified experience. Cloud storage connectors and ATS read-access make the platform portable and employer-system-aware. Advanced analytics and LinkedIn automation close the loop for power users. Sub-phases are independently deployable.

**Phase 2A:** Gmail and Outlook connectors (read-only, OAuth). Google Calendar and Outlook Calendar integration. Contact correspondence history for warm outreach context.

**Phase 2B:** `interview-coach` and `interview-capture` agents. Full mock interview system across all stages and vibes. Morning brief with company news and interviewer research. Post-interview debrief flow. Audio capture via Whisper with full privacy framework, consent model, and cross-jurisdiction recording guidance.

**Phase 2C:** Google Drive, OneDrive, and Dropbox storage connectors. IllinoisJobLink job board connector. ATS read-only connectors for Greenhouse, Workday, and Lever.

**Phase 2D:** Power BI streaming dataset connector. Qlik Engine API connector. D3 data export. LinkedIn automation for job search and connection graph access.

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
