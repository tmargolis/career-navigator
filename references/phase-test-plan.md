# Career Navigator Phase Test Plan

This document defines practical validation checks for each delivery phase.
Use it as a release gate before tagging a phase complete.

## Test Data Prerequisites

- A valid `{user_dir}` with `CareerNavigator/profile.md`.
- At least one source resume/CV in `{user_dir}`.
- `CareerNavigator/tracker.json` with a mix of open and resolved applications.
- `CareerNavigator/artifacts-index.json` populated with at least one resume and one cover letter.

---

## Phase 1A — Core Platform

### Scope
- Setup, profile creation, ExperienceLibrary initialization, session-start behavior, live job search.

### Tests
- Run `/career-navigator:setup`; verify all core files are created in `CareerNavigator/`.
- Confirm setup handles existing docs and builds ExperienceLibrary units.
- Start a fresh session; verify `session-start` behavior (first-run onboarding vs critical-only alerts).
- Run `/career-navigator:search-jobs`; confirm results return from Indeed and include apply links.

### Pass Criteria
- Core files are valid and readable.
- Job search works with profile-driven defaults.
- Session behavior is correct for both first-run and returning-user states.

---

## Phase 1B — Skill Layer and Intelligence

### Scope
- Workflow skills, tracker lifecycle, ATS scoring, analyst feedback loop, `job-scout` baseline.

### Tests
- Run `tailor-resume` and `cover-letter`; verify artifacts are written and indexed.
- Run `resume-score` and `ats-optimization`; verify ATS output and fix guidance.
- Run `track-application` across stage transitions (applied -> interview -> offer/rejected).
- Run `pattern-analysis`; verify `search_performance` and ExperienceLibrary weight updates.
- Run `search-jobs`; verify ranking changes after pattern-analysis updates.

### Pass Criteria
- Artifacts and tracker updates remain schema-consistent.
- Analyst outputs feed downstream ranking inputs.

---

## Phase 1C — Advisor Layer

### Scope
- Honest assessment, market intelligence, training ROI, role strategy signals.

### Tests
- Run `/career-navigator:assessment`; verify norm/exception/strategy output and confidence tier.
- Run `/career-navigator:training-roi`; verify option matrix + primary/fallback recommendation.
- Run `/career-navigator:market-brief`; verify demand/displacement/geography sections.
- Run `/career-navigator:suggest-roles`; verify `strategy_signals` is written to tracker.
- Re-run `search-jobs`; verify strategy signal dimension appears in rationale/score behavior.

### Pass Criteria
- Advisor outputs are evidence-grounded and connected to ranking strategy.
- `strategy_signals` is present and consumable by `job-scout`.

---

## Phase 1D — Proactive Discovery

### Scope
- Tuned `job-scout` scoring, confidence-aware weighting, proactive alert tiers, schedule-ready operations.

### Tests
- Run `search-jobs` with low and higher outcome-history datasets; confirm confidence tiers and adaptive behavior.
- Validate alert tiers (`critical`, `high`, `watch`, `none`) and priority summary output.
- Run `daily-schedule`; confirm artifact reconciliation and digest output.
- Add a new PDF/DOCX source file, run `daily-schedule`; verify auto-ingest path (`add-source`) and index consistency.
- Run `suggest-roles` and `market-brief`; verify agent invocations succeed using exact agent names.

### Pass Criteria
- Ranking is stable, explainable, and confidence-aware.
- Daily workflow handles new source files automatically.
- Agent invocation failures are retried/fallbacked as defined.

---

## Phase 1E — Professional Presence

### Scope
- Networking strategy, event radar, content advisor workflows.

### Tests
- Run network-mapping workflow and confirm gap identification output quality.
- Run outreach drafting with and without prior context; verify context-aware output handling.
- Run content suggestion and post evaluation; verify risk flags and audience-fit rationale.
- Run event radar and verify event prioritization logic.

### Pass Criteria
- Presence workflows produce actionable outputs with explicit rationale and risk notes.

---

## Phase 2A — Email and Calendar Integration

### Scope
- OAuth connectors for correspondence and calendar context.

### Tests
- Validate connector setup and permission prompts.
- Verify contact-context enrichment appears only when user-approved.
- Validate morning/day-of context from calendar data.

### Pass Criteria
- Read-only integrations work reliably with explicit consent boundaries.

---

## Phase 2B — Interview Intelligence

### Scope
- Interview prep, mock interview modes, capture/debrief pipeline.

### Tests
- Run prep + mock interview across multiple stages/vibes.
- Validate morning brief generation for interview-day scenarios.
- Validate debrief logging into tracker.
- If audio capture enabled, verify consent flow and transcript handling.

### Pass Criteria
- Interview workflows are coherent end-to-end and privacy constraints are respected.

---

## Phase 2C — Extended Integrations

### Scope
- Cloud storage and ATS/job-board connectors.

### Tests
- Validate storage connector switching and artifact read/write consistency.
- Validate ATS read connectors return statuses without write side effects.
- Validate additional job-board source ingestion and deduping behavior.

### Pass Criteria
- Connectors are reliable, scoped, and do not break local-first behavior.

---

## Phase 2D — Advanced Analytics and Automation

### Scope
- BI connector exports, advanced analytics, LinkedIn automation surface.

### Tests
- Validate export payloads for configured BI targets.
- Validate dashboard/report parity between local and exported datasets.
- Validate LinkedIn-related workflows honor policy/risk guardrails.

### Pass Criteria
- Analytics outputs are consistent and automation features remain policy-safe.

---

## Regression Checklist (Run Every Phase)

- Validate SKILL frontmatter (`name`, `description`, `triggers`) parses for all changed skills.
- Validate core JSON files remain valid (`tracker.json`, `ExperienceLibrary.json`, `artifacts-index.json`).
- Re-run `search-jobs`, `track-application`, `tailor-resume`, and `daily-schedule` as smoke tests.
- Confirm docs match actual behavior (README + spec).
