# Career Navigator

An AI-powered end-to-end job search companion built as a Claude Cowork plugin (also compatible with Claude Code). Combines the functions of a recruiter, career coach, reverse recruiter, and market analyst into a single intelligent platform that learns what works for you over time.

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

1. Download the zip: **Code → Download ZIP** on this page (or [direct link](https://github.com/tmargolis/career-navigator/archive/refs/heads/main.zip))
2. Click **Customize** → **Browse plugins → Personal** → **Upload a plugin** → select the ZIP
3. Click the **Customize** button on the Career Navigator plugin card to launch setup

### Install via Claude Code (CLI)

```bash
git clone https://github.com/tmargolis/career-navigator.git
cd career-navigator
claude plugin install .
```

Then run `/career-navigator:setup`.

---

## Plugin Marketplace

Career Navigator will be submitted to the official Claude plugin marketplace at [claude.com/plugins](https://claude.com/plugins) at the end of Phase 1. Once listed, installation will be a single click from the Browse plugins directory — no download required.

---

## Quick Start

### 1. Run setup

```
/career-navigator:setup
```

Reads everything in your job search folder — resumes, cover letters, past applications — and automatically builds your profile and corpus. Also configures JobSearch for live job search and optionally Google Drive.

### 2. Drop documents in your folder

Career Navigator monitors your job search folder automatically. Add a resume or cover letter, and it's ingested at the next startup or midnight sync — no command needed.

### 3. Search for matching roles

```
/career-navigator:search-jobs
```

With JobSearch configured: searches live job listings automatically and returns ranked results. Without it: generates optimized search strings for Indeed, LinkedIn, and Google Jobs, then ranks the results you bring back.

### 4. Tailor your first resume

```
/career-navigator:tailor-resume
```

Paste a job description. Career Navigator assembles the optimal resume from your corpus, scores it for ATS compatibility, and saves it to your artifact inventory.

---

## All Phase 1A Commands

| Command | Purpose |
|---------|---------|
| `/career-navigator:setup` | Configure JobSearch and Google Drive (run first) |
| `/career-navigator:add-source` | Add a resume or CV to your experience corpus |
| `/career-navigator:tailor-resume` | Build an optimized resume for a specific role |
| `/career-navigator:cover-letter` | Generate a targeted cover letter |
| `/career-navigator:resume-score` | Score any resume against a job description |
| `/career-navigator:list-artifacts` | View all generated resumes and cover letters |
| `/career-navigator:search-jobs` | Find and rank job opportunities |
| `/career-navigator:track-application` | Log or update a job application |

You can also trigger commands conversationally — if you say "I just applied to Acme for a PM role," Career Navigator recognizes the intent and logs it automatically.

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

**Job search (JobSearch):** Career Navigator uses [JobSearch](https://jobsearch.com/) to fetch live job listings from Indeed, LinkedIn, and other boards. A free tier is available. `/career-navigator:setup` opens the signup page, waits for you to paste your API key, validates it, and writes the config automatically. Without a key, `/career-navigator:search-jobs` works in assisted-manual mode (you paste in search results; Career Navigator ranks them).

**Cloud storage (Google Drive):** By default, all data is stored locally in `data/`. To sync to Google Drive, run `/career-navigator:setup` — it walks through creating OAuth credentials and handles all configuration. See [CONNECTORS.md](CONNECTORS.md) for details on the connector interface.

---

## Session Start Hook

Every time you open Claude Cowork (or Claude Code) with this plugin active, Career Navigator runs a brief session-start check. If you have application data, it surfaces:

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

**Phase 1A (current):** Resume corpus, artifact inventory, application tracker, ATS scoring, job search, session hook.

**Phase 1B:** Insight engine and feedback loop. Benchmarking against industry norms by role, level, and geography. Follow-up timeline intelligence. D3 pipeline dashboard (`/career-navigator:pipeline`, `/career-navigator:follow-up`, `/career-navigator:market-brief`).

**Phase 1C:** Honest advisor agent with three-step norm/exception/strategy pattern. Market researcher tracking role demand trends and AI/automation displacement. Skills self-assessment, gap analysis, and training ROI engine (`/career-navigator:suggest-roles`).

**Phase 1D:** Job scout with full outcome-driven scoring and proactive opportunity alerts. Non-obvious role suggestions based on transferable skills. Market trend monitoring with proactive notifications.

**Phase 1E:** Full mock interview system — guided, random, and adaptive modes across all stages (recruiter screen, hiring manager, technical, panel, executive) and vibes (supportive, neutral, challenging, antagonistic, bored). Morning brief with company news and interviewer research. Post-interview debrief flow. (`/career-navigator:prep-interview`, `/career-navigator:mock-interview`, `/career-navigator:morning-brief`, `/career-navigator:interview-debrief`).

**Phase 1F:** Networking strategy agent and network map. Event radar with local, national, and international discovery. LinkedIn content advisor and post evaluator with cultural risk assessment. (`/career-navigator:network-map`, `/career-navigator:draft-outreach`, `/career-navigator:content-suggest`, `/career-navigator:evaluate-post`, `/career-navigator:event-radar`).

### Phase 2 — Integrations

**Phase 2A:** Gmail and Outlook connectors (read-only, OAuth). Google Calendar and Outlook Calendar integration. Contact correspondence history for warm outreach context.

**Phase 2B:** Interview audio capture via Whisper transcription. Full privacy framework, consent model, and cross-jurisdiction recording guidance. Local processing option for privacy-sensitive users.

**Phase 2C:** OneDrive, Dropbox, and local filesystem storage connectors. IllinoisJobLink job board connector. ATS read-only connectors for Greenhouse, Workday, and Lever.

**Phase 2D:** Power BI streaming dataset connector. Qlik Engine API connector. D3 data export. LinkedIn automation for job search and connection graph access.

### Phase 3 — Platform Expansion

Hosted API proxy with per-user key management and usage tracking (removes the need for each user to obtain their own JobSearch key; enables monetization). Multi-user and team mode for staffing agencies and career coaches. Plugin marketplace publication. Mobile companion app for on-the-go tracker updates. Salary negotiation and offer evaluation module. Skills gap training integrations with Coursera and LinkedIn Learning.

### Phase 4 — Enterprise & Ecosystem

White-label version for career coaching practices and staffing agencies. API for third-party integrations. Anonymized aggregate benchmarking data. Government employment program integrations and American Job Center partnerships. Veteran and disability-specific pathway modules.

---

## Specification

See [career-navigator-spec.md](career-navigator-spec.md) for the full product specification covering all agents, skills, hooks, data model, and design philosophy.

## Contributing

Contributions welcome. Please open an issue before submitting a pull request for significant changes. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.
```
