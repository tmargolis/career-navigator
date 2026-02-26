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

### Install via Claude Desktop (GUI)

1. Open **Claude Desktop**
2. Go to **Settings → Plugins**
3. Click **Add Plugin**
4. Enter the repository URL: `https://github.com/tmargolis/career-navigator`
5. Click **Install** — Career Navigator activates on next session start

### Install via Git

```bash
git clone https://github.com/tmargolis/career-navigator.git
```

Then point Claude Cowork or Claude Code at the directory:

```
/plugin install /path/to/career-navigator
```

Or place the `career-navigator/` directory in your Claude plugins folder for automatic discovery.

---

## Quick Start

### 1. Run setup

```
/cn:setup
```

Walks you through configuring HasData (for automated job search) and optionally Google Drive (for cloud storage). Opens signup pages, validates your credentials, and writes all config automatically — no file editing required. Skip this and everything still works in assisted-manual mode.

### 2. Add your resume to the corpus

```
/cn:add-source
```

Paste your existing resume or provide a file path. Career Navigator extracts your experience into a structured corpus of reusable units.

### 3. Search for matching roles

```
/cn:search-jobs
```

With HasData configured: searches live job listings automatically and returns ranked results. Without it: generates optimized search strings for Indeed, LinkedIn, and Google Jobs, then ranks the results you bring back.

### 4. Tailor your first resume

```
/cn:tailor-resume
```

Paste a job description. Career Navigator assembles the optimal resume from your corpus, scores it for ATS compatibility, and saves it to your artifact inventory.

---

## All Phase 1A Commands

| Command | Purpose |
|---------|---------|
| `/cn:setup` | Configure HasData and Google Drive (run first) |
| `/cn:add-source` | Add a resume or CV to your experience corpus |
| `/cn:tailor-resume` | Build an optimized resume for a specific role |
| `/cn:cover-letter` | Generate a targeted cover letter |
| `/cn:resume-score` | Score any resume against a job description |
| `/cn:list-artifacts` | View all generated resumes and cover letters |
| `/cn:search-jobs` | Find and rank job opportunities |
| `/cn:track-application` | Log or update a job application |

You can also trigger commands conversationally — if you say "I just applied to Acme for a PM role," Career Navigator recognizes the intent and logs it automatically.

---

## Data Storage

All your data lives locally in the `data/` directory and is gitignored:

```
data/
├── corpus/
│   └── index.json              — Your experience corpus
├── applications/
│   └── tracker.json            — All application records
└── artifacts/
    ├── index.json              — Artifact inventory and metadata
    ├── resume-acme-pm-2026-02.md          — Tailored resume, Acme Corp PM role
    ├── cover-letter-acme-pm-2026-02.md    — Matching cover letter
    ├── resume-stripe-eng-mgr-2026-02.md   — Tailored resume, Stripe EM role
    └── resume-score-stripe-eng-mgr.json   — ATS score report
```

No data leaves your machine unless you configure a cloud connector (see [CONNECTORS.md](CONNECTORS.md)).

**To back up your data**: copy the `data/` directory to a safe location. These files are the heart of the system — back them up regularly.

---

## Job Search & Storage Setup

Run `/cn:setup` to configure integrations. The wizard handles everything conversationally — no file editing required.

**Job search (HasData):** Career Navigator uses [HasData](https://hasdata.com/) to fetch live job listings from Indeed, LinkedIn, and other boards. A free tier is available. `/cn:setup` opens the signup page, waits for you to paste your API key, validates it, and writes the config automatically. Without a key, `/cn:search-jobs` works in assisted-manual mode (you paste in search results; Career Navigator ranks them).

**Cloud storage (Google Drive):** By default, all data is stored locally in `data/`. To sync to Google Drive, run `/cn:setup` — it walks through creating OAuth credentials and handles all configuration. See [CONNECTORS.md](CONNECTORS.md) for details on the connector interface.

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

**Phase 1B:** Insight engine and feedback loop. Benchmarking against industry norms by role, level, and geography. Follow-up timeline intelligence. D3 pipeline dashboard (`/cn:pipeline`, `/cn:follow-up`, `/cn:market-brief`).

**Phase 1C:** Honest advisor agent with three-step norm/exception/strategy pattern. Market researcher tracking role demand trends and AI/automation displacement. Skills self-assessment, gap analysis, and training ROI engine (`/cn:suggest-roles`).

**Phase 1D:** Job scout with full outcome-driven scoring and proactive opportunity alerts. Non-obvious role suggestions based on transferable skills. Market trend monitoring with proactive notifications.

**Phase 1E:** Full mock interview system — guided, random, and adaptive modes across all stages (recruiter screen, hiring manager, technical, panel, executive) and vibes (supportive, neutral, challenging, antagonistic, bored). Morning brief with company news and interviewer research. Post-interview debrief flow. (`/cn:prep-interview`, `/cn:mock-interview`, `/cn:morning-brief`, `/cn:interview-debrief`).

**Phase 1F:** Networking strategy agent and network map. Event radar with local, national, and international discovery. LinkedIn content advisor and post evaluator with cultural risk assessment. (`/cn:network-map`, `/cn:draft-outreach`, `/cn:content-suggest`, `/cn:evaluate-post`, `/cn:event-radar`).

### Phase 2 — Integrations

**Phase 2A:** Gmail and Outlook connectors (read-only, OAuth). Google Calendar and Outlook Calendar integration. Contact correspondence history for warm outreach context.

**Phase 2B:** Interview audio capture via Whisper transcription. Full privacy framework, consent model, and cross-jurisdiction recording guidance. Local processing option for privacy-sensitive users.

**Phase 2C:** OneDrive, Dropbox, and local filesystem storage connectors. IllinoisJobLink job board connector. ATS read-only connectors for Greenhouse, Workday, and Lever.

**Phase 2D:** Power BI streaming dataset connector. Qlik Engine API connector. D3 data export. LinkedIn automation for job search and connection graph access.

### Phase 3 — Platform Expansion

Hosted API proxy with per-user key management and usage tracking (removes the need for each user to obtain their own HasData key; enables monetization). Multi-user and team mode for staffing agencies and career coaches. Plugin marketplace publication. Mobile companion app for on-the-go tracker updates. Salary negotiation and offer evaluation module. Skills gap training integrations with Coursera and LinkedIn Learning.

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
