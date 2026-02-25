# Career Navigator

An AI-powered end-to-end job search companion built as a Claude Code plugin. Combines the functions of a recruiter, career coach, reverse recruiter, and market analyst into a single intelligent platform that learns what works for you over time.

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

### Prerequisites

- [Claude Code](https://claude.ai/code) installed and running
- Git (to clone this repository)

### Install the plugin

```bash
git clone https://github.com/your-username/career-navigator.git
cd career-navigator
```

Then in Claude Code, install the plugin:

```
/plugin install /path/to/career-navigator
```

Or if Claude Code supports automatic plugin discovery, place the `career-navigator/` directory in your Claude plugins folder.

---

## Quick Start

Run these three commands to get fully set up:

### 1. Add your resume to the corpus

```
/cn:add-source
```

Paste your existing resume or provide a file path. Career Navigator extracts your experience into a structured corpus of reusable units.

### 2. Search for matching roles

```
/cn:search-jobs
```

Describe your target role and location. Career Navigator generates optimized search strings for Indeed, LinkedIn, and Google Jobs, then ranks the results you bring back.

### 3. Tailor your first resume

```
/cn:tailor-resume
```

Paste a job description. Career Navigator assembles the optimal resume from your corpus, scores it for ATS compatibility, and saves it to your artifact inventory.

---

## All Phase 1A Commands

| Command | Purpose |
|---------|---------|
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
│   └── index.json          — Your experience corpus
├── applications/
│   └── tracker.json        — All application records
└── artifacts/
    └── index.json           — Artifact inventory + generated files
```

No data leaves your machine unless you configure a cloud connector (see [CONNECTORS.md](CONNECTORS.md)).

**To back up your data**: copy the `data/` directory to a safe location. These files are the heart of the system — back them up regularly.

---

## Indeed API Setup

By default, `/cn:search-jobs` runs in assisted-manual mode: it generates optimized search strings you paste into job boards, then ranks the results you bring back.

To enable fully automated job search:

1. **Register for the Indeed Publisher Program**
   - Go to [https://publisher.indeed.com/publisher/](https://publisher.indeed.com/publisher/)
   - Registration is free for personal/non-commercial use
   - You will receive a **Publisher ID** (a numeric string, not a traditional API key)

2. **Add your Publisher ID to `.mcp.json`**
   - Open `.mcp.json` in the project root
   - Move the `indeed` entry from `_inactive_services` into `mcpServers`
   - Replace `YOUR_PUBLISHER_ID` with your actual Publisher ID

3. **Restart Claude Code**
   - The Indeed connector activates on next session start
   - `/cn:search-jobs` switches to automated mode automatically

**Note on the Indeed API**: Indeed's Publisher API uses a search endpoint at `api.indeed.com/ads/apisearch`. It does not have an official MCP server yet. Phase 2 will include a local stdio MCP wrapper for richer integration. For Phase 1A, the assisted-manual workflow covers all the core use cases.

---

## Google Drive Setup

To store artifacts and tracker data in Google Drive instead of locally:

1. Go to [https://console.cloud.google.com/](https://console.cloud.google.com/) and create a project
2. Enable the Google Drive API
3. Create OAuth 2.0 credentials (Desktop app type)
4. Download `credentials.json` and place it in `services/connectors/google-drive/`
5. In `.mcp.json`, move `google-drive` from `_inactive_services` to `mcpServers`
6. Restart Claude Code — on first use, you'll be prompted to authorize access

See [CONNECTORS.md](CONNECTORS.md) for full details on the connector interface and available backends.

---

## Session Start Hook

Every time you open Claude Code with this plugin active, Career Navigator runs a brief session-start check. If you have application data, it surfaces:

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

Phase 1A (current): Resume corpus, application tracker, ATS scoring, job search, session hook.

Coming next:
- **Phase 1B**: Insight engine, feedback loop, pipeline dashboard (`/cn:pipeline`), follow-up intelligence
- **Phase 1C**: Market researcher, skills gap analysis, honest advisor agent
- **Phase 1D**: Proactive job alerts, non-obvious role suggestions
- **Phase 1E**: Mock interviews, morning brief, interview debrief
- **Phase 1F**: Networking strategy, LinkedIn content advisor, event radar

See [career-navigator-spec.md](career-navigator-spec.md) for the full product specification.
