# Career Navigator

An AI-powered end-to-end job search companion built as a Claude Cowork plugin. Combines the functions of a recruiter, career coach, reverse recruiter, and market analyst into a single intelligent platform that learns what works for you over time.

## What It Does

Career Navigator manages your entire job search in one place:
- Builds targeted resumes from a structured corpus of your experience
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

Reads everything in your job search folder — resumes, cover letters, past applications — and automatically builds your profile and corpus. Also configures JobSearch for live job search.

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

Paste a job description. Career Navigator assembles the optimal resume from your corpus, scores it for ATS compatibility, and saves it to your artifact inventory.

---

## Skills & Commands

Career Navigator is designed skill-first: most workflows trigger automatically from conversational context — paste a job description and a resume is assembled; say "I just applied to Acme" and the tracker updates. Commands are available for users who prefer explicit invocation.

| Skill / Command | Trigger | Purpose |
|---------|---------|---------|
| `tailor-resume` | Paste a job description, or say "I want to apply to X" | Assemble an optimized resume from your corpus for a specific role |
| `cover-letter` | After tailoring a resume, or "write me a cover letter for X" | Generate a targeted cover letter |
| `track-application` | "I just applied to X", "log this application" | Log or update a job application |
| `add-source` | Upload or reference a resume/CV | Add a document to your experience corpus |
| `resume-score` | Share a resume + job description together | Score ATS match, formatting, and narrative strength |
| `search-jobs` | "find jobs", "search for X roles" | Find and rank job opportunities |
| `/career-navigator:setup` | Explicit (run first) | Configure job search folder, build corpus and profile |
| `/career-navigator:list-artifacts` | Explicit | View all generated resumes and cover letters |

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
├── artifacts-index.json         — index of all generated documents
├── profile/
│   └── profile.md               — your profile: targets, comp floor, differentiators
├── corpus/
│   └── index.json               — experience units extracted from your resumes
└── tracker/
    └── tracker.json             — all application records with full stage history
```

No data leaves your machine unless you configure a cloud connector (see [CONNECTORS.md](CONNECTORS.md)).

**To back up**: copy your entire job search folder.

---

## Job Search & Storage Setup

Run `/career-navigator:setup` to configure integrations. The wizard handles everything conversationally — no file editing required.

**Job search:** Career Navigator uses the built-in **Indeed connector** (Claude Cowork integration) for live job listings. No token or configuration required — job search works out of the box.

**Storage:** All data is stored locally in your job search folder (`{user_dir}`). Nothing leaves your machine by default. Cloud storage connectors (Google Drive, OneDrive, Dropbox) are available in Phase 2. See [CONNECTORS.md](CONNECTORS.md) for the connector interface.

---

## Session Start Hook

Every time you open Claude Cowork with this plugin active, Career Navigator runs a brief session-start check. If you have application data, it surfaces:

- Pipeline status counts by stage
- Applications overdue for follow-up (>7 days without a status change)
- Any interviews scheduled today
- A summary of your artifact inventory

On first run (no data yet), it delivers an onboarding welcome with setup instructions.

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

**Phase 1A (shipped — v1.1.0):** Plugin scaffold, setup wizard (builds profile and corpus from existing documents), live job search via Indeed, session start hook with pipeline digest.

**Phase 1B (in progress):** Application tracker, ATS scoring, and core workflow skills (tailor-resume, cover-letter, add-source, resume-score) — all auto-triggered from conversational context. `resume-coach` and `analyst` agents. Feedback loop connecting outcomes to corpus weights. AI displacement assessment via Anthropic Economic Index. Follow-up timeline intelligence. Pipeline dashboard.

**Phase 1C:** `honest-advisor` and `market-researcher` agents. Candid role competitiveness assessment. Skills gap analysis and training ROI engine. Market trend and AI/automation displacement signals (`/career-navigator:suggest-roles`).

**Phase 1D:** `job-scout` agent with full outcome-weighted scoring and proactive opportunity alerts. Non-obvious role suggestions based on transferable skills. Market trend monitoring with proactive notifications.

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

See [career-navigator-spec.md](references/career-navigator-spec.md) for the full product specification covering all agents, skills, hooks, data model, and design philosophy.

## Contributing

Contributions welcome. Please open an issue before submitting a pull request for significant changes. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.
```
