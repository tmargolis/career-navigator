# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

Career Navigator is a **Claude Cowork/Code plugin** — not a runnable application. There is no build step, no package.json, and no compilation required. The plugin loads declaratively into Claude sessions via `.claude-plugin/plugin.json`.

**Installation:**
```bash
# Via Claude Code CLI:
claude plugin install .
# Then in a new chat:
/career-navigator:setup
```

## Plugin Architecture

The plugin is composed of three layers:

1. **Plugin manifest** (`.claude-plugin/plugin.json`) — declares the plugin identity (name, version, author). This is the entry point the Claude plugin system reads.

2. **Skills** (`skills/<skill-name>/SKILL.md`) — each skill is a markdown file with YAML frontmatter defining `name`, `description`, and `triggers` (natural language phrases that auto-invoke the skill). The skill body contains the behavioral instructions Claude follows when executing it.

3. **User data** (`{user_dir}/`) — a user-supplied job search folder (e.g., `career/` in this repo). All plugin outputs are written here. The `{user_dir}` variable is set during `/career-navigator:setup` and is used as the root for all subdirectories.

## Directory Layout

```
.claude-plugin/
  plugin.json          # Plugin identity (name, version, author)
skills/
  <skill-name>/
    SKILL.md           # Skill definition: frontmatter + behavioral instructions
career/                # Example user_dir (live job search data for development/testing)
  profile/
    profile.md         # User's targets, comp floor, differentiators
  corpus/
    index.json         # Experience units extracted from resumes
  tracker/
    tracker.json       # Application records with full stage history
  artifacts-index.json # Index of all generated resumes and cover letters
```

## Phase 1A Commands

| Command | Purpose |
|---|---|
| `/career-navigator:setup` | Configure job search folder, corpus, JobSearch API, optional Google Drive |
| `/career-navigator:add-source` | Ingest a resume/CV into the experience corpus |
| `/career-navigator:tailor-resume` | Assemble an optimized resume for a specific role |
| `/career-navigator:cover-letter` | Generate a targeted cover letter |
| `/career-navigator:resume-score` | Score a resume against a job description (ATS) |
| `/career-navigator:list-artifacts` | View all generated resumes and cover letters |
| `/career-navigator:search-jobs` | Find and rank job opportunities (live with API key, assisted-manual without) |
| `/career-navigator:track-application` | Log or update a job application |

Commands can also be triggered conversationally — e.g., "I just applied to Acme for a PM role" auto-invokes tracking intent.

## Data Model

**`tracker/tracker.json`** is the core database:
```json
{
  "meta": { "created", "version", "description" },
  "applications": [
    {
      "id", "company", "role", "job_link", "salary_range", "location",
      "resume_version", "date_applied", "status", "stage_history",
      "contacts", "notes", "next_step", "priority", "artifacts"
    }
  ],
  "networking": [ { "id", "venue", "link", "notes" } ],
  "pipeline_summary": { "as_of", "applied", "considering", "declined_or_inactive", "overdue_followup" }
}
```

**`corpus/index.json`** stores structured experience units extracted from resumes — the source material for tailored resume generation.

**`profile/profile.md`** stores the user's job targets, compensation floor, and key differentiators.

## Key Conventions

- **`{user_dir}`** is the runtime variable for the user's job search folder — always write outputs here, never elsewhere.
- All plugin outputs (generated resumes, cover letters) are saved directly into `{user_dir}`, alongside the user's raw documents. The `artifacts-index.json` tracks them.
- Skills should be **honest over encouraging** — candid assessments, not false reassurance.
- **No data leaves the machine** unless a cloud connector is explicitly configured. Local filesystem is the default storage backend; Google Drive is opt-in.
- When adding new skills, follow the YAML frontmatter schema in `skills/setup/SKILL.md`: `name`, `description`, and `triggers` fields are required.

## Session Start Behavior

On every session start with the plugin active, Career Navigator surfaces:
- Pipeline status counts by stage
- Applications overdue for follow-up (>7 days without status change)
- Any interviews scheduled today
- Artifact inventory summary

On first run (no data), it delivers onboarding instructions.

## External Integrations

- **Indeed connector** — live job search via the built-in Claude Cowork Indeed integration. No token or configuration required.
- **Google Drive** — optional cloud sync, configured via OAuth during setup. See `CONNECTORS.md` for the connector interface.

## Full Specification

The authoritative product spec is `career-navigator-spec.md` — read it before making architectural changes. It covers all agents, skills, hooks, the full data model, and design philosophy.
