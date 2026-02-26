# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

Career Navigator has completed **Phase 1A implementation**. The plugin scaffold, commands, agents, skills, and SessionStart hook are all in place. The authoritative product specification is in `career-navigator-spec.md`. All future implementation should be driven by that document.

### Phase 1A — Implemented (2026-02-25)

**Plugin scaffold**: `.claude-plugin/plugin.json`, `.mcp.json`, `.gitignore`, `CONNECTORS.md`

**Data layer** (all gitignored user data with template scaffolding):
- `data/corpus/` — resume corpus (`index.json.template`)
- `data/applications/` — application tracker (`tracker.json.template`)
- `data/artifacts/` — artifact inventory (`index.json.template`)

**Hooks**: `hooks/hooks.json` + `hooks/session-start.sh` (SessionStart; DailySchedule deferred to Phase 1B)

**Skills**: `skills/ats-optimization/SKILL.md`, `skills/salary-research/SKILL.md`

**Agents**: `agents/resume-coach.md`, `agents/job-scout.md`

**Commands** (8): `setup`, `add-source`, `tailor-resume`, `cover-letter`, `resume-score`, `list-artifacts`, `track-application`, `search-jobs`

### Phase 1A Decisions Locked

- **Setup**: `/cn:setup` wizard handles all integration configuration (HasData, Google Drive). No manual `.mcp.json` editing required.
- **Storage**: Local file storage in `data/` (gitignored) by default. Google Drive configurable via `/cn:setup`.
- **Job search**: HasData for automated live job listings (configured via `/cn:setup`). Falls back to assisted-manual mode without a key.
- **Scheduling**: SessionStart hook only. node-cron DailySchedule deferred to Phase 1B.
- **Analytics**: No SQLite yet. Phase 1B adds insight engine and `/cn:pipeline` dashboard.

## What This Is

A **Claude Cowork plugin** (also compatible with Claude Code) that serves as an AI-powered end-to-end job search companion. It replaces the functions of a recruiter, career coach, reverse recruiter, and market analyst in a single platform.

## Design Principles

These are non-negotiable and must be preserved in all implementation decisions:

- **Honest over encouraging** — the system provides candid assessments, not false reassurance
- **Intelligent over mechanical** — outputs adapt based on outcomes, not just inputs
- **Connector-based** — storage, analytics, and external services are pluggable adapters; components call interface methods without knowing which backend is active
- **Privacy-first** — sensitive features like audio capture (Phase 2B) require explicit opt-in; email/calendar access requires user approval before each use
- **Cross-platform** — scheduling via `node-cron`, notifications via `node-notifier` (macOS, Windows, Linux)

## Architecture

### Directory Structure (Phase 1A actual)

```
career-navigator/
├── .claude-plugin/plugin.json     # Plugin manifest
├── commands/                      # Slash commands (/cn:* namespace)
│   ├── setup.md
│   ├── add-source.md
│   ├── tailor-resume.md
│   ├── cover-letter.md
│   ├── resume-score.md
│   ├── list-artifacts.md
│   ├── track-application.md
│   └── search-jobs.md
├── agents/                        # Specialized Claude instances
│   ├── resume-coach.md
│   └── job-scout.md
├── skills/                        # Auto-triggered capabilities
│   ├── ats-optimization/SKILL.md
│   └── salary-research/SKILL.md
├── hooks/                         # Event-driven triggers
│   ├── hooks.json
│   └── session-start.sh
├── data/                          # Gitignored user data
│   ├── corpus/                    # index.json (created on first /cn:add-source)
│   ├── applications/              # tracker.json (created on first /cn:track-application)
│   └── artifacts/                 # index.json + artifact files
├── services/
│   ├── scheduler/                 # node-cron jobs (Phase 1B)
│   ├── connectors/                # Storage adapters (Phase 1B+)
│   └── notifications/             # node-notifier (Phase 1B)
├── CONNECTORS.md                  # Storage connector documentation
└── .mcp.json                      # External service integrations (placeholders)
```

### Core Abstractions

**Agents** are specialized Claude instances invoked by commands or orchestrated together. Multiple agents collaborate on complex tasks. Key agents: `resume-coach`, `job-scout`, `market-researcher`, `honest-advisor`, `interview-coach`, `networking-strategist`, `content-advisor`, `event-intelligence`, `insight-engine`.

**Skills** are auto-triggered capabilities that fire when relevant context is detected — no explicit command needed. Key skills: `ats-optimization`, `salary-research`, `follow-up-timing`, `cultural-risk-flag`, `contact-context`.

**Hooks** are event-driven triggers: `SessionStart`, `DailySchedule` (node-cron), `ApplicationUpdate`, `ArtifactSaved`.

**Storage Connectors** implement a standard interface (`save_artifact`, `list_artifacts`, `get_artifact`, `save_event`, `query_events`). Phase 1 default: Google Drive. All plugin components call the interface — never the specific backend directly.

**Analytics Connectors** consume structured event data. Phase 1 default: SQLite with built-in query engine powering the `/cn:pipeline` dashboard.

### Command Namespace

All slash commands are prefixed `/cn:`. See `career-navigator-spec.md` Section 3 for the full command list and their descriptions. Commands also fire when Claude recognizes matching natural language intent.

### Core Data Model

- **Resume Corpus**: Not a collection of discrete resumes — a structured pool of experience units with `performance_weights` adjusted by the insight engine over time. Units have `skill_tags` and are drawn from `source_documents`.
- **Application Record**: Tracks full lifecycle with `stage_history[]`, `artifacts_used[]`, `contacts[]`, and outcome data.
- **Artifact Record**: Links generated documents to the experience units and JD keywords used, with ATS score and storage path.

### The Intelligence Feedback Loop

The core differentiator: every application outcome feeds back into `performance_weights` on experience units → job-scout scoring → resume-coach assembly recommendations. The system builds a personalized model of what works for the specific user, not generic best practices.

## Phased Delivery

Implementation follows the phased plan in `career-navigator-spec.md` Section 15. **Phase 1A is complete.** Next target: **Phase 1B** — insight engine, feedback loop, `/cn:pipeline` dashboard, follow-up intelligence, and DailySchedule hook via node-cron.

## External Integrations

Configured via `.mcp.json`. Each integration is optional — activates relevant agents/skills when present. Phase 1 integrations: Indeed (primary job search), Google Drive (storage). LinkedIn Phase 1 is assisted-manual workflow only; API automation is deferred to Phase 2D due to API restrictions.

## Open Questions

Before implementing these features, consult `career-navigator-spec.md` Section 16:
- Interview audio capture (Phase 2B) requires full privacy/legal review before any implementation
- LinkedIn automation approach is unresolved
- Antagonistic interview mode calibration needs user testing
- Training ROI data sources for Phase 1C are not yet identified
