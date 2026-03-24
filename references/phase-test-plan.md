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
- **`networking-strategist`** agent, invoked by skills **`networking-strategy`**, **`network-map`**, **`event-intelligence`**, and **`event-radar`**.
- **`content-advisor`** (when shipped): all outreach copy plus LinkedIn topic/evaluation workflows; consumes optional handoff briefs from **`networking-strategist`**.

### Test data (recommended)
- `CareerNavigator/profile.md` with **Target Roles**, **Target Companies** (or infer from `tracker.json`), and **Location** (local-only vs remote/travel-open affects event-radar scope).
- `tracker.json` with at least one application listing **`contacts`** (can be empty) to validate gap/path logic.
- Optional: stale or missing `CareerNavigator/network-map.md` to validate create vs update behavior.

### Example prompts (copy/paste)

Use natural language or the equivalent **`/career-navigator:…`** command. Swap company names, roles, and events to match your **`CareerNavigator`** data.

#### **`networking-strategy`** — baseline plan

```text
I need a networking strategy for my job search. Use my CareerNavigator profile and tracker—prioritize the next 90 days and the top 5 relationship moves I should make.
```

```text
/career-navigator:networking-strategy
```

#### **`networking-strategy`** — outreach boundary (strategist must not draft send-ready copy)

```text
Run my networking strategy using profile + tracker, and in the same answer write the exact LinkedIn DM I should send to a hiring manager at my top target company—ready to paste.
```

**Expect:** Handoff brief + direction to **`content-advisor`** or **`/career-navigator:draft-outreach`**, not a finished DM from **`networking-strategist`**.

#### **`network-map`** — paths, gaps, and JSON

```text
Map my network toward my dream roles and target companies. Label confirmed vs hypothetical paths, call out gaps, and include the network_map_v1 JSON block for later visualization.
```

```text
/career-navigator:network-map
```

#### **`network-map`** — persistence offer

```text
After you produce the network map, save the narrative and the network_map_v1 JSON to CareerNavigator/network-map.md in my job search folder.
```

#### **`event-intelligence`** — named event (ROI + presentation flag)

```text
Should I attend [name a real conference or meetup you are considering] for my job search? Assess ROI, audience quality, whether it's worth travel/time/money, and flag if there's a realistic speaking or visibility opportunity. If you don't have verified dates or prices, tell me exactly what to look up instead of guessing.
```

```text
/career-navigator:event-intelligence
```
*(Then paste the event name and constraints in the same thread.)*

#### **`event-radar`** — multi-scope discovery

```text
Run an event radar for my interests and target roles: local and regional events first, then national, then international if my profile supports travel. Give ROI tiers, presentation flags, and real links—or search queries if links aren't available.
```

```text
I'm only looking locally—no travel. Scan my metro area for the next 3 months for meetups and conferences relevant to my target role. Skip national/international unless virtual.
```

```text
/career-navigator:event-radar
```

#### **Phase 2A honesty** (no inbox unless connected)

```text
Before we draft any outreach, summarize what I last emailed anyone at [Company X] and pull thread context from my inbox.
```

**Expect:** Clear statement that email/calendar access is not available (or requires Phase 2A + user approval)—**no** fabricated thread summaries.

#### **`content-advisor`** — when shipped

**Draft outreach**

```text
/career-navigator:draft-outreach
```
```text
Draft a short LinkedIn note to a [peer IC | recruiter | hiring manager] at [Company]. Goal: informational conversation, not asking for a job in the first message. Tone: direct and respectful. Here's the handoff from my networking strategy: [paste handoff bullets].
```

**Topic ideas**

```text
/career-navigator:content-suggest
```
```text
Suggest three LinkedIn post ideas for the next month that support my target roles without sounding desperate. Flag any that might clash with employers I'm targeting.
```

**Post review**

```text
/career-navigator:evaluate-post
```
```text
Evaluate this draft post for audience fit and cultural risk relative to my target companies: [paste draft].
```

#### **Agent invocation / retry** (host-dependent)

Retry behavior is validated by observing logs or the host’s agent tool—not a single user prompt. Optionally run the same **`network-map`** or **`event-radar`** prompt twice after a transient failure to confirm recovery after one retry per skill rules.

### Agent: **`networking-strategist`**

#### Invocation and orchestration
- From each skill body, confirm the model uses the **exact** agent name **`networking-strategist`** (no aliases such as “network” or “strategy agent”).
- Simulate or observe one failed subagent call; confirm **one retry** with the same name before surfacing an error (per skill instructions).

#### Role boundary (outreach vs strategy)
- Run **`networking-strategy`** with an explicit ask to “write my LinkedIn message” in the same turn.
  - **Expect:** no ready-to-send DM/email body from **`networking-strategist`**; instead a **handoff brief** (objective, audience archetype, evidence-backed hooks, tone, avoid list) and explicit pointer to **`content-advisor`** or **`/career-navigator:draft-outreach`** for final copy.
- Run **`network-map`**; confirm output does not include full outreach drafts—only strategy, path labels, gaps, JSON, and optional handoff bullets.

#### Phase 2A honesty
- Without email/calendar connectors, confirm the agent **does not** claim access to inbox or prior threads; if it mentions Phase 2A, it should describe what would be needed—not invent correspondence.

### Skills

#### **`networking-strategy`**
- Confirm the plan includes a **time-bounded** arc (e.g. 90-day framing), **prioritized moves**, and **what to avoid**.
- If the user saves output, confirm optional persistence to `CareerNavigator/networking-strategy.md` (or equivalent dated section) does not corrupt other `CareerNavigator` files.

#### **`network-map`**
- **confirmed** vs **hypothesis** paths are labeled; bridge **personas** are archetypes unless the user supplied real names.
- A fenced **`network_map_v1`** JSON block is present with `schema`, `as_of`, `nodes`, `edges`, `gaps`, and **`viz_note`** (graph viz deferred).
- Offer to write/update **`CareerNavigator/network-map.md`** when the user agrees; re-read file to ensure narrative + JSON coexist.

#### **`event-intelligence`**
- For a **named** event: ROI assessment, audience/readiness signal, **presentation opportunity** (`yes` / `maybe` / `no`), and **risks** (pay-to-play, low signal).
- **No fabricated** dates, prices, or CFP deadlines—either cite a verifiable source or give **queries/URLs to verify**.

#### **`event-radar`**
- Results grouped or labeled by **local → regional → national → international** as appropriate to profile (skip international when profile is strictly local and user confirms no travel).
- Each candidate has **ROI tier** (e.g. A/B/C), **presentation flag**, and **link or explicit verification step**; no invented conferences.

### **`content-advisor`** (when shipped)

- **`/career-navigator:draft-outreach`:** produces send-ready copy (or clearly marked drafts), respects tone/length asks, and does **not** fabricate shared history; can consume **`networking-strategist`** handoff bullets when pasted or referenced.
- **`/career-navigator:content-suggest`:** topics align with profile targets and are actionable.
- **`/career-navigator:evaluate-post`:** audience-fit + **cultural/political risk** flags with rationale tied to target employer context when provided.

### Pass Criteria
- **`networking-strategist`** outputs are evidence-grounded, confidence-labeled, and **do not** substitute for **`content-advisor`** on outreach copy.
- Event outputs avoid hallucinated logistics; uncertainty is stated explicitly.
- **`content-advisor`** (when present) owns message copy and integrates handoffs cleanly without duplicating strategist scope.

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
