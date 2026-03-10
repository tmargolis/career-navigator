# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

Career Navigator has completed **Phase 1A implementation**. The plugin scaffold, commands, agents, skills, and hooks are all in place. The authoritative product specification is in `career-navigator-spec.md`. All future implementation should be driven by that document.

### Phase 1A — Implemented (2026-02-25)

- **Plugin scaffold**: `.claude-plugin/plugin.json`, `.mcp.json`, `CONNECTORS.md`
- **Data layer**: User profile, corpus, tracker, and artifact index — all stored in the user-provided directory (`{user_dir}`), not inside the plugin. See Data Architecture below.
- **Hooks**: `hooks/hooks.json` → `session-start.sh` (SessionStart) + `sync-watchdir.sh` (Schedule: midnight cron)
- **Skills**: `ats-optimization`, `salary-research`
- **Agents**: `resume-coach`, `job-scout`
- **Commands** (8): `setup`, `add-source`, `tailor-resume`, `cover-letter`, `resume-score`, `list-artifacts`, `track-application`, `search-jobs`
- **Init script**: `scripts/init.py` — one-time registration of the user's job search directory

### Phase 1A Decisions Locked

- **User directory**: All user data lives in the folder the user provides — not inside the plugin repo. The plugin is stateless. `scripts/init.py` registers this path; hooks read it from the Career Navigator `config.json` at runtime.
- **Job search**: JobSearch (HasData API) for automated live listings. Falls back to assisted-manual mode without a key.
- **Storage**: Local filesystem in `{user_dir}` by default. Google Drive configurable via `/career-navigator:setup`.
- **Scheduling**: SessionStart + midnight Schedule hook. node-cron DailySchedule deferred to Phase 1B.
- **Analytics**: No SQLite yet. Phase 1B adds insight engine and `/career-navigator:pipeline`.

## Data Architecture

All user data lives in a single directory the user provides at setup time (`{user_dir}`). The plugin writes nothing to its own directory at runtime.

```
{user_dir}/                          ← wherever the user chooses (e.g. ~/Documents/career)
├── profile/profile.md               ← user profile: targets, comp floor, differentiators
├── corpus/index.json                ← experience units extracted from source resumes
├── tracker/tracker.json             ← application records with full stage history
├── artifacts-index.json             ← index of all generated documents
├── .cn-sync-state.json              ← timestamp used by midnight sync to detect changed files
└── resume-acme-pm-2026.md           ← generated artifacts saved here alongside source docs
```

`templates/` in the plugin repo contains JSON/Markdown schemas showing the expected structure of the above files — documentation and scaffolding only, not read at runtime.

### Career Navigator Config File

`{user_dir}` is persisted by `scripts/init.py` to a platform-specific path:
- **macOS**: `~/Library/Application Support/Claude/cowork_plugins/career-navigator/config.json`
- **Linux**: `$XDG_CONFIG_HOME/Claude/cowork_plugins/career-navigator/config.json`
- **Windows**: `%APPDATA%/Claude/cowork_plugins/career-navigator/config.json`

Both `session-start.sh` and `sync-watchdir.sh` resolve `{user_dir}` by reading `user_dir` from this JSON file. They do not accept the path as an argument.

## Setup (Development)

```bash
# One-time: register your job search directory, then restart Claude Desktop
python3 scripts/init.py /path/to/your/job-search-folder

# Finish configuration via the in-plugin wizard:
/career-navigator:setup
```

`init.py` is idempotent — re-running with the same path makes no changes. Pass a new path to update the registration.

Copy `.env.example` to `.env` for local development; `HASDATA_API_KEY` is the only variable. In production, this key lives in `.mcp.json` under `mcpServers.jobsearch.env.HASDATA_API_KEY`, written automatically by `/career-navigator:setup`.

## Hooks System

`hooks/hooks.json` defines two hooks. The Claude runtime resolves `${CLAUDE_PLUGIN_ROOT}` to the plugin's install directory:

- **SessionStart** → `session-start.sh`: Reads profile, tracker, artifacts index, and corpus on every session open. Outputs a structured digest prompt for Claude to deliver as a morning brief. Detects first-run (no profile or tracker) and shows onboarding instead.
- **Schedule** (cron `0 0 * * *`) → `sync-watchdir.sh`: Midnight sync. Finds files in `{user_dir}` modified since last sync (tracked via `.cn-sync-state.json`). Outputs a structured prompt for Claude to extract new/updated documents into the corpus and tracker. Skips `profile/`, `corpus/`, `tracker/` subdirectories and any file already in `artifacts-index.json`.

## Architecture

### Core Abstractions

**Commands** (`commands/*.md`): Slash command behavior in the `/career-navigator:` namespace. Markdown files with YAML frontmatter (`name`, `command`, `triggers`) followed by natural language workflow instructions. Fire on explicit invocation or matching conversational intent.

**Agents** (`agents/*.md`): Specialized Claude instances invoked by commands or orchestrated together. Currently implemented: `resume-coach`, `job-scout`. Full roster in `career-navigator-spec.md` Section 4.

**Skills** (`skills/*/SKILL.md`): Auto-triggered capabilities that fire when relevant context is detected without an explicit command. Currently implemented: `ats-optimization` (fires on resume editing), `salary-research` (fires when compensation is mentioned).

**Storage Connectors**: Standard interface (`save_artifact`, `list_artifacts`, `get_artifact`, `save_event`, `query_events`). Phase 1 default: local filesystem in `{user_dir}`. All plugin components call the interface — never reference a specific backend directly. See `CONNECTORS.md`.

### Core Data Model

- **Resume Corpus**: A structured pool of experience units with `performance_weights` adjusted by the insight engine over time. Units have `skill_tags` and are drawn from `source_documents`. Not a collection of discrete resumes.
- **Application Record**: Full lifecycle tracking with `stage_history[]`, `artifacts_used[]`, `contacts[]`, and outcome data.
- **Artifact Record**: Links generated documents to the corpus units and JD keywords used, with ATS score and storage path.

### The Intelligence Feedback Loop

Every application outcome feeds back into `performance_weights` on corpus experience units → job-scout scoring → resume-coach assembly recommendations. Implemented fully in Phase 1B (insight engine).

## Phased Delivery

**Phase 1A**: Complete. See above.

**Next: Phase 1B** — insight engine + feedback loop, benchmarking against industry norms, follow-up timeline intelligence, D3 pipeline dashboard, `/career-navigator:pipeline`, `/career-navigator:follow-up`, `/career-navigator:market-brief`, DailySchedule hook via node-cron.

Before implementing anything beyond Phase 1A, read `career-navigator-spec.md` Section 15 for the full phased plan and Section 16 for open questions that must be resolved before certain features can be built (interview audio capture, LinkedIn automation, antagonistic interview mode calibration).

## Workflow Rules

- Always read `{user_dir}/profile/profile.md` before giving career advice — agents must not ask for information already in the profile.
- Always check `{user_dir}/tracker/tracker.json` before referencing application status.
- All plugin components must call the storage connector interface, never write to `{user_dir}` directly outside of the interface.

## Customization

When the user requests plugin customization or runs `/career-navigator:setup`, the wizard asks for the job search folder path and handles all configuration from there — it discovers resumes and prior applications from the folder and Google Drive before asking any questions.
