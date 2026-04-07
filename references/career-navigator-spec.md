# **CAREER NAVIGATOR**

Claude Cowork Plugin — Full Product Specification

Version 0.31 — April 2026

An AI-powered job search companion that combines the capabilities of
recruiters, career coaches, reverse recruiters, and market analysts into a single intelligent platform.

# **Table of Contents**

[Chapter 1. Overview](#1-overview)
>[1.1 Design Principles](#11-design-principles)
>[1.2 Plugin Architecture](#12-plugin-architecture)

[Chapter 2. Plugin File Structure](#2-plugin-file-structure)

[Chapter 3. Slash Commands](#3-slash-commands)
>[3.0 Launch & configuration](#30-launch--configuration)
>[3.1 Resume & Cover Letter Commands](#31-resume--cover-letter-commands)
>[3.2 Job Search & Tracking Commands](#32-job-search--tracking-commands)
>[3.3 Interview Prep Commands](#33-interview-prep-commands)
>[3.4 Networking Commands](#34-networking-commands)

[Chapter 4. Agents](#4-agents)

[Chapter 5. Skills](#5-skills)

[Chapter 6. Scheduling & recurring runs](#6-scheduling--recurring-runs)
>[6.1 Host hooks (`hooks/hooks.json`)](#61-host-hooks-hookshooksjson)

[Chapter 7. Storage Connectors](#7-storage-connectors)
>[7.1 Interface](#71-interface)
>[7.2 Available Connectors](#72-available-connectors)

[Chapter 8. Analytics Connectors](#8-analytics-connectors)

[Chapter 9. External Service Integrations (.mcp.json)](#9-external-service-integrations-mcpjson)

[Chapter 10. Core Data Model](#10-core-data-model)
>[10.1 ExperienceLibrary](#101-experiencelibrary)
>[10.2 Application Record](#102-application-record)
>[10.3 Artifact Record](#103-artifact-record)
>[10.4 Networking entries & LinkedIn post analytics](#104-networking-entries--linkedin-post-analytics)
>[10.5 Story Corpus](#105-story-corpus)
>[10.6 Career trajectory & offer context artifacts](#106-career-trajectory--offer-context-artifacts)

[Chapter 11. The Intelligence Feedback Loop](#11-the-intelligence-feedback-loop)

[Chapter 12. Daily Rhythm & Scheduling](#12-daily-rhythm--scheduling)
>[12.1 Recommended cadences (Cowork `/schedule`)](#121-recommended-cadences-cowork-schedule)
>[12.2 Time-sensitive vs routine surfacing](#122-time-sensitive-vs-routine-surfacing)

[Chapter 13. Interview Capture (Phase 2B)](#13-interview-capture-phase-2b)
>[13.1 MVP Audio Scope](#131-mvp-audio-scope)
>[13.2 Fallback: Post-Interview Q&A Flow](#132-fallback-post-interview-qa-flow)

[Chapter 14. The Honest Advisor Design Philosophy](#14-the-honest-advisor-design-philosophy)

[Chapter 15. Phased Delivery Plan](#15-phased-delivery-plan)
- [Phase 1 — Core Platform](#phase-1--core-platform)
  - [Phase 1A — Core platform: plugin scaffold, setup, session start, and live job search](#phase-1a--core-platform-plugin-scaffold-setup-session-start-and-live-job-search)
  - [Phase 1B — Skill layer and intelligence: workflow skills, application tracker, ATS scoring, and analyst agent](#phase-1b--skill-layer-and-intelligence-workflow-skills-application-tracker-ats-scoring-and-analyst-agent)
  - [Phase 1C — Advisor layer: honest role assessment, skills gap analysis, and training ROI](#phase-1c--advisor-layer-honest-role-assessment-skills-gap-analysis-and-training-roi)
  - [Phase 1D — Proactive discovery: outcome-weighted job scoring and market trend monitoring](#phase-1d--proactive-discovery-outcome-weighted-job-scoring-and-market-trend-monitoring)
  - [Phase 1E — Professional presence: networking strategy, event radar, and LinkedIn writer](#phase-1e--professional-presence-networking-strategy-event-radar-and-linkedin-writer)
  - [Phase 1F — Career planning, offer evaluation & compensation negotiation](#phase-1f--career-planning-offer-evaluation--compensation-negotiation)
  - [Phase 1G — Marketplace publication](#phase-1g--marketplace-publication)

- [Phase 2 — Integrations](#phase-2--integrations)
  - [Phase 2A — Email & Calendar Integration](#phase-2a--email--calendar-integration)
  - [Phase 2B — Interview intelligence](#phase-2b--interview-intelligence)
  - [Phase 2C — Extended Integrations](#phase-2c--extended-integrations)
  - [Phase 2D — Event Intelligence & Interview Story Intelligence](#phase-2d--event-intelligence--interview-story-intelligence)

- [Phase 3 — Always-On Career Agent](#phase-3--always-on-career-agent)

- [Phase 4 — Enterprise & Ecosystem](#phase-4--enterprise--ecosystem)

[Chapter 16. Open Questions & Deferred Decisions](#16-open-questions--deferred-decisions)

[Appendix: Command Quick Reference](#appendix-command-quick-reference)

# **1. Overview**

*Entry points:* `README.md`, `CLAUDE.md`.

Career Navigator is a Claude Cowork plugin that provides end-to-end job search intelligence — from discovering roles and tailoring application materials, through interview preparation and networking strategy, to tracking outcomes and learning from results. It is designed to serve any job seeker regardless of experience level, target industry, or geographic location.

The plugin is architected around a feedback loop: every action taken and outcome observed feeds back into the system to make future recommendations smarter. Over time, Career Navigator learns what works for the individual user and adjusts its guidance accordingly.

## **1.1 Design Principles**

* Honest over encouraging — the system provides candid assessments, not false reassurance
* Intelligent over mechanical — outputs adapt based on outcomes, not just inputs
* Connector-based — storage, analytics, and external services are pluggable adapters
* Privacy-first — sensitive features like audio capture require explicit opt-in
* Cross-platform — skills and data work on macOS, Windows, and Linux; recurring runs are configured by the user in Claude Cowork via `/schedule` (or equivalent), not by a plugin-shipped daemon
* Empathetic — the system understands job searching is stressful and calibrates tone accordingly

## **1.2 Plugin Architecture**

| Plugin Name | career-navigator |
| --- | --- |
| **Version** | 2.4.0 |
| **Platform** | Claude Cowork (macOS / Windows / Linux) (also compatible with Claude Code) |
| **Architecture** | Skill-first — behavioral intelligence lives in skills with conversational triggers; commands are explicit invocation aliases for key workflows |
| **Scheduling** | User-configured in Claude Cowork — skills are the payload; recommended cadences are documented in skill files (e.g. run `daily-schedule` daily via `/schedule`) |
| **Notifications / surfacing** | In-session UX (e.g. `focus-career` for critical items) plus whatever Cowork provides when a scheduled task runs — the plugin does not ship a separate notification daemon |
| **Storage Layer (Phase 1)** | Local filesystem — `{user_dir}` (cloud connectors in Phase 2C) |
| **Analytics Layer (Phase 1)** | SQLite + D3 visualization (additional connectors in Phase 3) |
| **AI Services** | Claude API (via MCP); optional **local** TTS/STT via **`mcp-voice`** MCP (Claude Desktop Extension **`mcp-voice.mcpb`** — tools **`speak`**, **`listen`**); optional Whisper or other STT MCP |
| **Job Search (Phase 1)** | **Indeed** MCP via Claude Desktop **Customize → Connectors** — **Connect** → browser OAuth on **secure.indeed.com**; tools **`search_jobs`**, **`get_job_details`** (connector `https://mcp.indeed.com/claude/mcp`). User must complete OAuth; assisted-manual fallback when connector unavailable |
| **Salary benchmarks (Phase 1, optional)** | Apify MCP added in Claude Desktop **Customize → Connectors → Desktop → Apify** (token + **Enabled tools** list in connector UI); not stored in project **`.mcp.json`** |

# **2. Plugin File Structure**

**career-navigator/**

**├── .claude-plugin/**

**│ └── plugin.json**

**├── .mcp.json** — may include Anthropic **HTTP MCP** entries for **Gmail** / **Google Calendar** and/or **`ms365`** (Outlook / Microsoft 365) as an alternate channel (no secrets); other MCPs (e.g. Apify for salary) are configured in the host app. **Does not** include local voice — see **`mcp-voice/`**.

**├── mcp-voice/** — Claude Desktop **Extension** bundle (`.mcpb`) for optional **`mcp-voice`** MCP (`speak`, `listen`); published via GitHub Releases
**├── mcp-luma/** — Claude Desktop **Extension** bundle (`.mcpb`) for optional **`mcp-luma`** event discovery MCP; published via GitHub Releases

**├── agents/**

**├── skills/**

**├── hooks/**

**│ ├── hooks.json**

**│ └── context/** — e.g. `session-start.md` injected on `SessionStart`

**├── references/**

**├── career/** *(example `{user_dir}` — gitignored when personal)*\*\*

**└── README.md**

# **3. Slash Commands**

*Implementation:* each command’s behavior and triggers live in `skills/<skill-name>/SKILL.md` (see subsections below); plugin manifest `.claude-plugin/plugin.json` registers the skills directory.

All commands are namespaced under career-navigator: and accessible via Claude Cowork's slash command interface (and Claude Code). Commands can also be triggered conversationally — the plugin recognizes natural language prompts that match command intent and invokes the appropriate command automatically.

## **3.0 Launch & configuration**

*Skill file:* `skills/launch/SKILL.md`.

| Name | Type | Description |
| --- | --- | --- |
| **/career-navigator:launch** | Command | **Launch** the user's job search workspace: conversational wizard that configures `{user_dir}`, reads existing documents, builds the user profile and ExperienceLibrary, and walks through connectors for live job search (Indeed, optional Apify, etc.). **Offers** optional **`linkedin-post-analytics`** when the user wants a first run—read-only own-post snapshots into **`tracker.json`**, subject to host browser automation and explicit consent. Same setup responsibilities as before; framed as the entry point to start searching. Validates inputs before saving; re-runnable to update keys or reconfigure. |

## **3.1 Resume & Cover Letter Commands**

| Name | Type | Description |
| --- | --- | --- |
| **/career-navigator:tailor-resume** | Command | Takes one or more source documents from the ExperienceLibrary and a job description, assembles and rewrites the best possible resume for that specific role, scores it for ATS compatibility, and saves it to the artifact inventory. |
| **/career-navigator:cover-letter** | Command | Builds a **CoverLetterBrief**, then invokes **`writer`** for final prose (voice-aware). Saves to artifact inventory. |
| **/career-navigator:resume-score** | Command | Scores an existing resume or cover letter against a job description for ATS keyword match, formatting compliance, and narrative strength. |
| **/career-navigator:add-source** | Command | Adds a new source document (resume, CV, portfolio) to the ExperienceLibrary for use in future tailoring. |
| **/career-navigator:list-artifacts** | Command | Lists all generated artifacts in the inventory with metadata: date created, job applied for, outcome if known. |

## **3.2 Job Search & Tracking Commands**

| Name | Type | Description |
| --- | --- | --- |
| **/career-navigator:search-jobs** | Command | Searches configured job boards and returns ranked results. Ranking incorporates skill match, outcome history, and market intelligence. Supports filters for role, location, company size, industry, and salary range. |
| **/career-navigator:track-application** | Command | Logs a new application or updates an existing one. Accepts conversational input and structures it automatically into the tracker database. |
| **/career-navigator:pipeline** | Command | Displays the full application pipeline dashboard with timeline view, benchmark comparisons, and action items flagged by stage age. **Roadmap:** **forecast** overlay and **voice cadence** on the timeline—see **Phase 3 — Dashboard & visualization enhancements** in §15. |
| **/career-navigator:follow-up** | Command | Classifies applications by response windows, builds **FollowUpBrief** entries, invokes **`writer`** for send-ready messages. Email/calendar enrichment Phase 2A. |
| **/career-navigator:market-brief** | Command | Generates a current market intelligence report for the user's target roles and industries, including trend data, competition levels, and AI/automation impact assessment. |
| **/career-navigator:suggest-roles** | Command | Analyzes the user's full ExperienceLibrary and suggests non-obvious role types their skills could be applied to, with rationale for each suggestion. |
| **/career-navigator:career-plan** | Command | Generates a realistic career trajectory plan (near/mid/long horizon) with ROI-ranked gap priorities and saves `career_trajectory_v1` to `career-trajectory.md`. |
| **/career-navigator:evaluate-offer** | Command | Performs scenario-aware offer evaluation (employed/unemployed context), role-fit/utilization analysis, and compensation fairness determination. Persists `offer-context-{application_id}.json` for downstream use. |
| **/career-navigator:compare-offers** | Command | Compares active offers side-by-side on compensation, fit, trajectory alignment, and risk, then returns an honest ranking. |
| **/career-navigator:negotiate** | Command | Builds negotiation strategy and leverage points, then hands off a `NegotiationHandoffBrief` to `writer` for a send-ready draft. |

## **3.3 Interview Prep Commands**

| Name | Type | Description |
| --- | --- | --- |
| **/career-navigator:prep-interview** | Command | Launches a full interview preparation session for a specific role. Pulls in company research, generates predicted questions, and optionally launches a mock interview. |
| **/career-navigator:mock-interview** | Command | Starts a mock interview session. Accepts mode (guided/random/adaptive), stage (recruiter/HM/technical/panel/executive), and vibe (supportive/neutral/challenging/antagonistic/bored). **If mode or vibe omitted, the system selects defaults** (see `skills/mock-interview/SKILL.md` §2.1). |
| **/career-navigator:interview-capture** | Command | Opt-in **skill** (not an agent): transcribe **user** audio, extract takeaways, update **`tracker.json`**; employer warning once; §13.1 retention. Uses **`mcp-voice`** **`listen`** when the extension is installed. |
| **/career-navigator:interview-debrief** | Command | Post-interview Q&A flow that captures the candidate's experience conversationally and structures it into the tracker. Fallback for users who do not use audio capture. |
| **/career-navigator:morning-brief** | Command | **Alias** for the **`daily-schedule`** skill: focused output = **Pre-interview brief (today)** only (see `skills/daily-schedule/SKILL.md` §3.3). No separate `morning-brief` skill. |

## **3.4 Networking Commands**

| Name | Type | Description |
| --- | --- | --- |
| **/career-navigator:networking-strategy** | Command | Builds an evidence-based networking plan (priorities, sequencing, gaps). Optional handoff brief for **`writer`** when messaging is needed. Invokes **`networking-strategist`**. |
| **/career-navigator:network-map** | Command | Maps plausible paths and gaps to target employers; outputs narrative plus **`network_map_v1`** JSON (and may persist to `network-map.md`). **Interactive graph UI** is **Phase 3**—see §15. |
| **/career-navigator:draft-outreach** | Command | Drafts outreach copy (LinkedIn, email, InMail, etc.). Invokes **`writer`**. Prefer **`contact-context`** first when warm threading matters; or searches email and calendar history for prior context with user approval when Phase 2A connectors exist. |
| **/career-navigator:contact-context** | Command | Read-only search of email (and calendar when tools allow) for a named contact or company—**past** and **upcoming** calendar events; emits **ContactContextBrief** (**upcoming_meetings**, **warm_networking**) for **`draft-outreach`** / **`writer`**. Requires explicit user approval before lookup. |
| **/career-navigator:event-intelligence** | Command | Deep evaluation of specific events: ROI, audience fit, cost/time, and **presentation / speaking** opportunity flagging. Invokes **`networking-strategist`**. |
| **/career-navigator:content-suggest** | Command | Suggests LinkedIn post topics based on current industry trends, the user's target roles, and recent activity in their field. Invokes **`writer`**. |
| **/career-navigator:evaluate-post** | Command | Evaluates a draft post for audience fit, algorithmic performance, and **cultural / political / reputational** risk vs target companies. Invokes **`writer`** and **`market-researcher`** for target-profile-specific risk evaluation. |
| **/career-navigator:linkedin-post-analytics** | Command | **Read-only** snapshot of the user’s **own** LinkedIn post analytics into **`tracker.json`** `networking[]` (per-post **`analytics_history`**). Requires host **browser control** (e.g. **Claude in Chrome** MCP or **computer / browser use**) and **explicit user approval** before navigation; see **`linkedin-post-analytics`** skill. |
| **/career-navigator:event-radar** | Command | Discovers events across **local, regional, national, and international** scopes (as appropriate); ranked with ROI tiers and presentation flags. Invokes **`networking-strategist`**. |

# **4. Agents**

Agents are specialized Claude instances with focused roles. They can be invoked directly or orchestrated by commands. Multiple agents may collaborate on complex tasks.

**Model selection (cost vs reasoning):** By default, the system assumes a fast, cost-efficient reasoning model (e.g., Sonnet-class) for routine workflows and scheduled runs. For complex tasks (multi-step strategy, ambiguous trade-offs, heavy synthesis, or high-stakes messaging), a stronger reasoning model (e.g., Opus-class) can be enabled. Users should have a clear way to control this (global default + per-run override) so they can manage costs intentionally while still “spending” higher reasoning when it matters.

| Name | Phase | Description |
| --- | --- | --- |
| **resume-coach** | 1B | Analyzes the ExperienceLibrary, identifies gaps and strengths, optimizes for ATS compatibility, and provides narrative coaching. Invoked by the `tailor-resume` and `resume-score` skills. May emit a **ResumeSummaryBrief** for **`writer`** when **`tailor-resume`** requests voice-aligned Summary polish. |
| **analyst** | 1B | Analyzes application outcome data to identify patterns in what's advancing and what isn't. Identifies transferable strengths and core capabilities in the user's experience that apply across roles and industries. Assesses AI and automation displacement risk for current and target roles using the Anthropic Economic Index. Updates ExperienceLibrary performance weights and feeds recommendations to `job-scout` and `resume-coach`. |
| **honest-advisor** | 1C | Provides candid assessments of the user's competitiveness for specific roles, potential recruiter concerns, and strategies for overcoming barriers. Researches company/industry-specific deviations from general norms. Empathetic but unsparing. |
| **market-researcher** | 1C | Monitors macro hiring trends, role-specific demand signals, AI/automation displacement risks, geographic demand patterns, and sector-specific cycles. Feeds the `market-brief` command and the `job-scout` agent. Also invoked by `writer` during post evaluation to provide target-company- and industry-specific cultural/political risk context — making risk assessment dynamic rather than based on a static rubric. |
| **job-scout** | 1D | Searches and ranks job opportunities across all configured job boards. Incorporates outcome history and market intelligence into scoring. Ranking improves over time as the user logs outcomes. Proactively surfaces high-match opportunities. |
| **networking-strategist** | 1E | Network analysis, gap identification, and warm-path planning. Event discovery and evaluation with ROI assessment, **presentation-opportunity** flagging, and multi-scope **event radar** (via **`event-intelligence`** and **`event-radar`** skills). Recommends the **`linkedin-post-analytics`** skill (weekly/biweekly or **`/schedule`**) when the user is building LinkedIn visibility—subject to host browser automation and explicit consent. May emit a structured **handoff brief** for **`writer`** when messaging is needed; does **not** draft outreach copy. |
| **writer** | 1E | Owns **Career Navigator user-facing copy**: outreach (LinkedIn, email, InMail), **cover letters** (from **CoverLetterBrief**), **follow-ups** (from **FollowUpBrief**), optional **resume Summary** polish (**ResumeSummaryBrief**), post drafts (saved under **`{user_dir}/LinkedIn Posts/`** + **`artifacts-index.json`** as **`linkedin_post`**), **`/career-navigator:draft-outreach`**, **`content-suggest`**, **`evaluate-post`**. Maintains **`voice-profile.md`** (and optional **`voice_profile_v1`**) for tone matching; **timeline surfacing** of voice metadata is **Phase 3**. Consumes handoffs from **`networking-strategist`**, **`resume-coach`** (summary path), **`cover-letter`**, **`follow-up`**. For post risk evaluation, consumes a **`market-researcher`** brief on target-company/industry norms before assessing cultural or political risk. Outreach email/calendar enrichment **Phase 2A**. |
| **interview-coach** | 2B | Interview **prep**, **mock interviews**, and **`morning_section`** day-of bullets for `daily-schedule`. Stages include **recruiter** (first-class), hiring manager, technical, panel, executive, final. Modes: guided / random / adaptive; vibes: supportive through bored. Optional **`mcp-voice`** MCP (**`speak`** / **`listen`**) or host **TTS/STT** for questions and user answers (**user audio only**—see §13.1 spirit). For prep and mocks, story evidence is sourced primarily from **`StoryCorpus.json`** via **`story-retrieval`** (ExperienceLibrary fallback). Spec file: `agents/interview-coach/AGENT.md`. |

# **5. Skills**

Skills are auto-triggered capabilities that Claude activates when relevant context is detected, without requiring an explicit command invocation. This is the primary interaction model for Career Navigator — commands serve as explicit aliases for users who prefer them, but skills carry the behavioral intelligence.

**Workflow skills** handle the core job search operations and fire from conversational intent:

| Name | Type | Description |
| --- | --- | --- |
| **tailor-resume** | Skill | Fires when the user shares or pastes a job description, or expresses intent to apply to a specific role. Reads the ExperienceLibrary, invokes **`resume-coach`** to assemble an ATS-optimized resume; may invoke **`writer`** (**`resume-summary`** mode) when the user requests **voice-aligned Summary** prose. Saves to the artifact inventory. Also invocable via `/career-navigator:tailor-resume`. |
| **cover-letter** | Skill | Fires after a resume is tailored for a role, or when the user explicitly requests a cover letter for a specific job. Builds **CoverLetterBrief**; invokes **`writer`** for final letter. Saves to artifact inventory. Also invocable via `/career-navigator:cover-letter`. |
| **track-application** | Skill | Fires when the user mentions applying to a job, logging a new application, or updating an existing one (e.g., "I just applied to Acme" or "I got a callback from Google"). Structures conversational input into the tracker database automatically. Also invocable via `/career-navigator:track-application`. |
| **add-source** | Skill | Fires when the user uploads or references a new resume, CV, or portfolio document. Extracts experience units and adds them to the ExperienceLibrary. Also invocable via `/career-navigator:add-source`. |
| **resume-score** | Skill | Fires when the user shares a resume alongside a job description without explicitly requesting tailoring. Scores ATS keyword match, formatting compliance, and narrative strength. Also invocable via `/career-navigator:resume-score`. |
| **list-artifacts** | Skill | Fires when the user asks to see their generated documents, artifact history, or what has been created so far. Also invocable via `/career-navigator:list-artifacts`. |
| **assessment** | Skill | Fires when the user asks for an honest assessment and gap analysis vs. their target role requirements. Uses the `honest-advisor` agent's norm/exception/strategy pattern to surface evidence-based gaps and repositioning options. |
| **market-brief** | Skill | Fires when the user asks for current market conditions. Invokes `market-researcher` to summarize role demand trends, AI/automation displacement signals, and geography-specific competitiveness. Also invocable via `/career-navigator:market-brief`. |
| **suggest-roles** | Skill | Fires when the user asks what adjacent or non-obvious roles they should target. Invokes `honest-advisor` and `market-researcher`, then writes `strategy_signals` to `tracker.json` for job-scout scoring improvements. Also invocable via `/career-navigator:suggest-roles`. |
| **training-roi** | Skill | Fires when the user asks what to learn next. Compares certifications, degrees, bootcamps, and self-study using a cost-benefit-time ROI framework and recommends a primary and fallback path. Queries available MCPs (including CareerOneStop DOL API if connected) for live certification-value and labor-market outcome data before falling back to static knowledge. See Phase 1C note in §15. |
| **career-plan** | Skill | Produces `CareerTrajectoryReport` (near/mid/long horizon + ROI-ranked gaps) and persists `career_trajectory_v1` to `{user_dir}/CareerNavigator/career-trajectory.md`. Also invocable via `/career-navigator:career-plan`. |
| **evaluate-offer** | Skill | Produces `OfferEvaluationReport` with scenario-aware context, role fit/utilization, and compensation fairness; persists `offer-context-{application_id}.json` for downstream negotiation/comparison. Also invocable via `/career-navigator:evaluate-offer`. |
| **compare-offers** | Skill | Produces `OfferComparisonReport` across active offers and outputs an honest ranking with tiebreakers when needed. Also invocable via `/career-navigator:compare-offers`. |
| **negotiate-offer** | Skill | Produces `NegotiationBrief` and emits `NegotiationHandoffBrief` for `writer` to draft send-ready negotiation messaging. Also invocable via `/career-navigator:negotiate`. |
| **networking-strategy** | Skill | Fires when the user wants a networking plan for their search. Invokes **`networking-strategist`** in **networking-strategy** mode (strategy and handoff bullets only; outreach copy via **`writer`**). Also invocable via `/career-navigator:networking-strategy`. |
| **network-map** | Skill | Fires when the user wants a structured map of paths and gaps toward target employers (including dream-job leverage). Produces **`network_map_v1`** JSON for downstream **Phase 3** graph visualization. Invokes **`networking-strategist`**. Also invocable via `/career-navigator:network-map`. |
| **event-intelligence** | Skill | Fires when the user asks whether to attend specific events, wants ROI or speaker/CFP assessment, or asks about presentation opportunities. Invokes **`networking-strategist`** in **event-intelligence** mode. Also invocable via `/career-navigator:event-intelligence`. |
| **event-radar** | Skill | Fires when the user wants ongoing discovery of events across local, regional, national, and international scope. Invokes **`networking-strategist`** in **event-radar** mode. Also invocable via `/career-navigator:event-radar`. |
| **follow-up** | Skill | Surfaces follow-up queue using **company-windows.json**, builds **FollowUpBrief** entries, invokes **`writer`** for send-ready messages. Also invocable via `/career-navigator:follow-up`. |
| **draft-outreach** | Skill | Invokes **`writer`** for outreach copy (LinkedIn, email, InMail). Also invocable via `/career-navigator:draft-outreach`. |
| **content-suggest** | Skill | Invokes **`writer`** for LinkedIn/professional topic recommendations. Also invocable via `/career-navigator:content-suggest`. |
| **evaluate-post** | Skill | Invokes **`writer`** for audience fit and **cultural / political / reputational risk** vs target company profiles. Risk evaluation is dynamic: **`market-researcher`** is queried for target-company/industry-specific norms before assessment. The system informs the user of risk context; it does not suppress or prescribe content decisions. Also invocable via `/career-navigator:evaluate-post`. |
| **linkedin-post-analytics** | Skill | **Read-only** capture of the user’s **own** LinkedIn post analytics from the live site UI, appended to **`tracker.json`** `networking[]` as **`type: "linkedin_post"`** entries with an **`analytics_history`** array (dated snapshots). **Does not** post, like, or comment. **Requires** host browser automation (**Claude in Chrome** or **computer / browser use**) and **explicit user approval** before running; if unavailable, the skill instructs the model to stop and ask the user to enable tooling. Also invocable via `/career-navigator:linkedin-post-analytics`. |
| **prep-interview** | Skill | Full interview preparation for a tracked (or specified) role: company/news context, **stage-specific** questions (**recruiter** through **final**), talking points from ExperienceLibrary, saved brief under **`CareerNavigator/interview-prep/`**, **`[prep]`** note in **`tracker.json`**. Invokes **`interview-coach`** (`prep` mode). Also invocable via `/career-navigator:prep-interview`. |
| **mock-interview** | Skill | Mock session: **guided** / **random** / **adaptive**; **stage** + **vibe**; **selects defaults** when mode/vibe omitted (see skill §2.1). Invokes **`interview-coach`** (`mock` mode). Optional **`mcp-voice`** MCP (**`speak`**, **`listen`**). Also invocable via `/career-navigator:mock-interview`. |
| **interview-capture** | Skill | **Not an agent.** Opt-in post-interview **user-audio** transcription (e.g. **`mcp-voice`** **`listen`** or compatible STT), structured takeaways, **`tracker.json`** updates; employer warning once; §13.1 retention. Also invocable via `/career-navigator:interview-capture`. |
| **mine-stories** | Skill | Offline/cheap extraction pass over journals, PKM notes, debriefs, and related sources to build/update **`StoryCorpus.json`**. Runs at launch/setup and as incremental refresh when new source documents appear in `{user_dir}`. |
| **story-retrieval** | Skill | Retrieves a small competency-matched subset (typically 8-12) from **`StoryCorpus.json`** for interview prep/mock STAR mapping. This is the default interview story selection layer; raw journal rereads are avoided at query time. |

**Context skills** fire on ambient signals throughout any session:

| Name | Type | Description |
| --- | --- | --- |
| **ats-optimization** | Skill | Fires automatically when a resume is being edited or generated. Checks for ATS-hostile formatting, missing keywords, and structural issues. Suggests fixes inline. |
| **salary-research** | Skill | Fires when compensation is mentioned in any context. Pulls current market data for the role, level, and geography under discussion. |
| **follow-up-timing** | Skill | Fires when an application is viewed in the tracker. Evaluates elapsed time against company-specific norms and flags if a follow-up action is warranted. |
| **cultural-risk-flag** | Skill | Fires when drafting LinkedIn content or outreach messages. Routes evaluation through **`evaluate-post`** / **`writer`** + **`market-researcher`** for a single, target-specific risk rubric; may nudge the user to run **`evaluate-post`** before publishing. |
| **contact-context** | Skill | Fires when a contact at a target company is identified or the user asks for prior-thread context before outreach. Searches email and calendar (**past** + **scheduled** meetings) for correspondence and warm-networking signals; surfaces **ContactContextBrief** for **`writer`** / **`draft-outreach`** (Phase 2A). Requires user approval before use. Also invocable via **`/career-navigator:contact-context`**. |

# **6. Scheduling & recurring runs**

Career Navigator does **not** ship its own cron daemon or hook runtime inside the plugin repo. In **Claude Cowork**, the practical pattern is:

1. **Skills are the payload** — each skill (`daily-schedule`, `focus-career`, etc.) defines what to do and where to read data (`{user_dir}/CareerNavigator/...`).
2. **The user schedules execution** — e.g. create a recurring task that runs `/career-navigator:daily-schedule` (or natural language that invokes the `daily-schedule` skill) on a cadence using Cowork's **`/schedule`** (or equivalent scheduling UI).
3. **Cowork learns the prompt** — after the first successful run, the host refines the scheduled prompt with resolved paths, connectors, and context. That is Cowork's analogue to a traditional "hook."

| Name | Type | Description |
| --- | --- | --- |
| **focus-career** | Skill | Run when the user opens a session (or on a tight cadence via `/schedule` if they want proactive critical checks). Surfaces **critical-only** alerts (imminent deadlines, same-day follow-ups, urgent interview-day actions). |
| **daily-schedule** | Skill | **Recommended daily** via `/schedule`. Before the digest, checks `{user_dir}` for artifact files and runs `artifact-saved` when present; then pipeline digest, follow-ups, **meetings today** (interview/recruiter/screen — see skill §3.1), **conditional Pre-interview brief** when applicable, market/strategy prompts. **`/career-navigator:morning-brief`** triggers a **focused** run (pre-interview slice only). |
| **application-update** | Skill | Run **after** `track-application` writes to `tracker.json` (same turn). Classifies refresh priority for outcome-weighted scoring and nudges `pattern-analysis` at milestones. |
| **artifact-saved** | Skill | Run **after** new resumes/cover letters are saved, and/or from `daily-schedule` when PDF/DOCX artifacts exist. Reconciles `artifacts-index.json` with files on disk; prepares analytics handoff metadata when connectors exist. |

## **6.1 Host hooks (`hooks/hooks.json`)**

Claude Cowork supports a plugin-level **`hooks/hooks.json`** (see **cowork-plugin-management**). Available host events include `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `Stop`, `PreToolUse`, `PostToolUse`, `SubagentStop`, `PreCompact`, `Notification`, and others as documented by the host.

Career Navigator ships a minimal configuration:

* **`SessionStart`** — `command` hook runs `cat "${CLAUDE_PLUGIN_ROOT}/hooks/context/session-start.md"` to inject instructions so the model runs the **`focus-career`** skill (`skills/focus-career/SKILL.md`) for critical-only alerts.

**Prompt-based** hooks (`type: "prompt"`) are supported on a subset of events per host docs; **command-based** hooks work for deterministic context injection (as in the `SessionStart` example above).

This is **orthogonal** to **`/schedule`**: host hooks fire on session/tool lifecycle events; the **`daily-schedule`** skill remains the recommended **daily** payload for recurring tasks the user configures in Cowork.

# **7. Storage Connectors**

*Specification:* this section (interface + roadmap). *Related doc:* `CONNECTORS.md` (OAuth / host connectors). Cloud storage backends are Phase **2C**.

The plugin defines a standard artifact storage interface. Users configure a single active connector in plugin settings. All plugin components call the interface methods without knowing which backend is active.

## **7.1 Interface**

| Name | Type | Description |
| --- | --- | --- |
| **save\_artifact()** | Method | Saves a generated document (resume, cover letter, etc.) with metadata to the configured storage backend. |
| **list\_artifacts()** | Method | Returns a filterable list of all artifacts with metadata: type, date, associated job, outcome. |
| **get\_artifact()** | Method | Retrieves a specific artifact by ID for display or reuse. |
| **save\_event()** | Method | Logs a tracker event (application update, interview outcome, etc.) to the structured event database. |
| **query\_events()** | Method | Returns structured event data for analytics consumption. Supports filtering by date range, role type, company, and outcome. |

## **7.2 Available Connectors**

| Name | Type | Description |
| --- | --- | --- |
| **local** | Connector | Default connector. Stores all data locally in `{user_dir}`. No cloud dependency, no credentials required. All Phase 1 functionality uses this connector. |

Cloud storage connectors (Google Drive, OneDrive, Dropbox) are introduced in Phase 2C. For **Google Drive, OneDrive or Dropbox**, portability is handled via **Google Drive application sync** or manual backup/restore (not the host connector for typical job files).\.

# **8. Analytics Connectors**

*Specification:* this section. *Closest shipped behavior:* `skills/pipeline-dashboard/SKILL.md` for pipeline/dashboard flows using local data.

The analytics layer consumes structured event data from the storage connector and produces insights, visualizations, and dashboard views. The plugin ships with a built-in SQLite-based analytics engine for users without a BI tool.

| Name | Type | Description |
| --- | --- | --- |
| **sqlite-builtin** | Connector | Default connector. Local SQLite database with built-in query engine. Powers the /career-navigator:pipeline dashboard and insight engine natively. |
| **power-bi** | Connector | Pushes event data to a Power BI streaming dataset. Enables custom dashboard creation in Power BI Desktop or Service. |
| **qlik** | Connector | Integrates with Qlik Sense or QlikView via the Qlik Engine API. Enables associative analysis across the full application dataset. |
| **d3** | Connector | Exports structured event data in D3-compatible JSON format for custom visualization development. |

# **9. External Service Integrations (.mcp.json)**

The plugin ships **`.mcp.json`** with optional Anthropic **HTTP MCP** servers for **Gmail**, **Google Calendar**, and/or **`ms365`** (Microsoft 365 / Outlook—alternate to Google for inbox and calendar context; see file); other connectors are configured in the **client** where the user runs Claude. For **`search-jobs`**, users add the **Indeed** connector under **Claude Desktop → Customize → Connectors**, click **Connect**, and complete **browser OAuth** on **secure.indeed.com** (**Grant access to Indeed** in-app; tools **`search_jobs`**, **`get_job_details`**). For **salary-research**, users add the **Apify** **Desktop** connector, paste their **Apify token**, set **Enabled tools** to **`call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search`**, save, enable, and start a new session. This avoids brittle `npx mcp-remote` configs where **`${APIFY_TOKEN}`** in JSON args is passed literally and never expanded. For **inbox and calendar context** (**`draft-outreach`**, **`follow-up`**, **`contact-context`**), users add Anthropic’s **Gmail** and/or **Microsoft 365** connectors and/or **Google Calendar** (**OAuth** in the browser—no passwords or refresh tokens in repo JSON); see table below and **`CONNECTORS.md`**. **Google Calendar** is a separate connector from **Gmail** in the Connectors catalog. For **PKM-backed interview story mining** (**`mine-stories`**), users can connect **Notion** via first-party connector and/or use **Capacities** through an available MCP integration in the host session; if unavailable, the workflow falls back to file-based exports in `{user_dir}`.

Run `/career-navigator:launch` for a conversational walkthrough. Each integration is optional; skills degrade when a connector is absent.

**Multi-channel sourcing policy (implementation guidance):**
- Use a connector-first sequence: MCP tools first, then browser-assisted capture if needed, then assisted-manual ingestion fallback.
- Normalize listings across all channels before ranking with required fields: `title`, `company`, `location`, `apply_url`, `source`, `retrieval_mode`.
- Apply source-aware confidence tiers (`high`, `moderate`, `directional`) and cross-channel dedupe precedence: company-direct URL > ATS requisition URL > connector-sourced aggregator > manual entry.
- Keep provenance explicit in outputs so users can see which results are live connector data versus browser/manual captures.

| Name | Type | Description |
| --- | --- | --- |
| **Apify** | MCP (Desktop connector) | Powers **`salary-research`** via **cheapget/best-job-search** and related tools. Configured in Claude Desktop connector UI, not committed in `.mcp.json`. |
| **Indeed** | MCP (Claude connector) | Official **`search-jobs`** path: **`search_jobs`**, **`get_job_details`**; OAuth at **secure.indeed.com** after **Connect** in **Customize → Connectors**. Connector endpoint `https://mcp.indeed.com/claude/mcp`. Walkthrough in `/career-navigator:launch` Step 3. |
| **LinkedIn** | MCP | Job posting search, connection graph access, InMail drafting, post publishing and analytics. Required for networking strategy features. |
| **JobSearch** | MCP | Broader job-data integrations (scraping APIs, additional boards). Phase 1A primary live search is **Indeed** MCP above; this row covers alternate/future sources. |
| **Glassdoor** | MCP | Company culture research, interview experience data, salary benchmarks, and recruiter process timelines. |
| **CareerOneStop** | MCP | U.S. Department of Labor API. Free. Provides labor market data, salary ranges, occupation outlook, and American Job Center locations. Also a candidate live data source for the `training-roi` skill — see Phase 1C note in §15. |
| **IllinoisJobLink** | MCP | Illinois-specific job board. State employment resources and local posting discovery. |
| **Gmail** | Claude first-party connector | **Settings / Customize → Connectors → Gmail → Connect** — Google **OAuth** in the browser; do not commit tokens in `.mcp.json`. Anthropic documents **search and analyze** mail; **no create/send/modify** via this integration. **Pro / Max / Team / Enterprise** per Claude docs (confirm in-product). Career Navigator: **`draft-outreach`**, **`follow-up`**, **`contact-context`** use mail only after **explicit user approval** per lookup. See `CONNECTORS.md`, [Gmail integration](https://claude.com/docs/connectors/google/gmail). |
| **Microsoft 365** (Outlook mail, SharePoint, OneDrive, Teams per product scope) | Claude first-party connector | **Connectors → Microsoft 365 → Connect** — Microsoft **OAuth**; **Team/Enterprise** and often **tenant admin** setup per Anthropic. Documented as **read-only** (no modify/delete/create through the connector). Outlook thread search supports the same Career Navigator skills as Gmail. See `CONNECTORS.md`, [Microsoft 365 connector](https://claude.com/docs/connectors/microsoft/365). |
| **Google Calendar** | Claude first-party connector (Google) | **Settings / Customize → Connectors → Google Calendar → Connect** — Google **OAuth** in the browser (separate card from **Gmail**). Anthropic documents schedule and event access per [Google Calendar integration](https://claude.com/docs/connectors/google/calendar). Career Navigator: **`contact-context`** (and downstream drafting) uses **read-only** **past** and **upcoming** meeting context **after explicit user approval** per lookup—**warm** identification when a meeting is scheduled; do not create or move events unless the user asks. See `CONNECTORS.md`. |
| **Notion** | Claude first-party connector | Optional PKM source for interview story mining. When connected, `mine-stories` may read eligible notes/pages for story candidate extraction into `StoryCorpus.json` (connector-permission scope applies). |
| **Outlook Calendar / Teams Calendar** | Microsoft 365 connector | Covered under **Microsoft 365** row where enabled. |
| **Capacities** | MCP (host extension/server) | Optional PKM source for interview story mining. Can be connected through a Capacities MCP integration in hosts that support it; if unavailable, export notes into `{user_dir}` and mine from files. |
| **Greenhouse / Workday / Lever** | MCP | ATS status tracking for applications submitted through these platforms. Read-only access to application status. |
| **mcp-voice** (local MCP bundle) | Claude Desktop **Extension** (`.mcpb`) | **Local** TTS and STT for **`prep-interview`**, **`mock-interview`**, **`interview-capture`**. Install **`mcp-voice.mcpb`** from [GitHub Releases](https://github.com/tmargolis/career-navigator/releases): **Settings** (⌘/Ctrl + comma) → **Extensions** → drag bundle → **Install** → enable. Source: **`mcp-voice/`**; tools **`speak`**, **`listen`**. Not declared in project **`.mcp.json`**. |
| **Whisper (OpenAI)** | MCP | Alternate STT when **`mcp-voice`** is unavailable or user prefers another host. Phase 2B. MVP scope: user audio only. |
| **Meetup / Eventbrite / Luma** | MCP + host browser/manual fallback | Event discovery for networking radar. For Luma, install local **`mcp-luma.mcpb`** from [GitHub Releases](https://github.com/tmargolis/career-navigator/releases) (source: **`mcp-luma/`**). For Meetup/Eventbrite, use optional **Claude in Chrome**, **computer use**, or **manual copy/paste** fallback. |
| **Host browser automation** | Host capability (not plugin MCP) | **Claude in Chrome**, **computer use**, or equivalent: enables **`linkedin-post-analytics`** to navigate a logged-in browser **read-only** and record own-post metrics into **`tracker.json`**. User must opt in per session or schedule; distinct from the **LinkedIn** MCP row (which describes optional connector features such as search and messaging). |

# **10. Core Data Model**

## **10.0 User Profile**

Stored at `{user_dir}/CareerNavigator/profile.md`. Created by `/career-navigator:launch` — scans documents in `{user_dir}` and builds the profile from existing resumes and cover letters; falls back to conversational Q&A if no documents are found. Read automatically by all agents at the start of every operation — agents must not ask for information that is already in the profile.

* **identity** — name, location, contact info, professional summary, core differentiator
* **target\_roles** — preferred titles, minimum seniority level
* **target\_companies** — primary, secondary, and tertiary targets; industries to prioritize and avoid
* **compensation\_floor** — minimum total comp (base + bonus + equity annualized); expected ranges by company type
* **location** — geographic preferences, relocation openness, remote/hybrid preference. The `location` field also drives jurisdiction detection for data retention policy (see §13.1 and Phase 2B). If jurisdiction cannot be determined, the user is prompted to select a policy at first recording session.
* **key\_skills** — prioritized skill list for ATS matching and ExperienceLibrary tagging
* **differentiators** — named, high-value elements that must appear in every tailored resume
* **search\_notes** — standing instructions for agents: preferred channels, company-specific notes, anything static that should inform every search and application

**Optional companion file — `{user_dir}/CareerNavigator/voice-profile.md`**

**`/career-navigator:launch`** seeds or refreshes this file via **launch voice harvest**: scans **PDF/DOCX/MD/TXT** résumés, CVs, and cover letters (tiered vs plugin-generated artifacts), prompts for **LinkedIn** (paste, drop files, or skip), may record **`## Voice by context`** when tones diverge, and **`## Voice quality flags (launch)`** for pragmatic risks (tone, "AI slop" tells, snark, etc.). **`writer`** then maintains user-pasted **`## User writing samples`** blocks, **`voice_profile_v1`**, and respects multi-context + flags when drafting.

## **10.1 ExperienceLibrary**

*Primary file:* `{user_dir}/CareerNavigator/ExperienceLibrary.json`.

The ExperienceLibrary is not a collection of discrete resumes — it is a structured pool of experience units that can be recombined. Each unit has metadata indicating source document, role type relevance, industry tags, and performance history.

* source\_documents[ ] — original uploaded files (resumes, CVs, portfolios)
* experience\_units[ ] — individual bullets, accomplishments, roles extracted from source documents
* skill\_tags[ ] — normalized skill taxonomy mapped across all units
* performance\_weights{ } — outcome-adjusted weights per unit, updated by insight engine

## **10.2 Application Record**

*Stored in:* `{user_dir}/CareerNavigator/tracker.json` → `applications[]`.

| Name | Type | Description |
| --- | --- | --- |
| **application\_id** | UUID | Unique identifier |
| **company** | String | Company name |
| **role\_title** | String | Job title applied for |
| **jd\_text** | Text | Full job description text |
| **source\_board** | String | Where the posting was found |
| **date\_applied** | Date | Application submission date |
| **status** | Enum | Applied / Phone Screen / HM Interview / Panel / Final / Offer / Rejected / Withdrawn / Ghosted |
| **stage\_history[ ]** | Array | Timestamped log of every status change |
| **artifacts\_used[ ]** | Array | IDs of resume and cover letter artifacts submitted |
| **contacts[ ]** | Array | Known contacts at the company with relationship strength |
| **notes** | Text | Freeform notes from conversational input or interview debrief |
| **outcome** | Enum | Pending / Hired / Rejected / Withdrew |
| **outcome\_notes** | Text | Reason for outcome if known |

## **10.3 Artifact Record**

*Index:* `{user_dir}/CareerNavigator/artifacts-index.json`.

| Name | Type | Description |
| --- | --- | --- |
| **artifact\_id** | UUID | Unique identifier |
| **type** | Enum | Resume / Cover Letter / LinkedIn post draft (`linkedin_post`) / Portfolio / Other |
| **application\_id** | UUID | Associated application (nullable for templates) |
| **source\_units[ ]** | Array | Experience unit IDs included in this artifact |
| **jd\_keywords[ ]** | Array | Keywords targeted in this artifact |
| **ats\_score** | Float | ATS compatibility score at time of generation |
| **created\_at** | Timestamp | Creation date |
| **storage\_path** | String | Path or URL in configured storage connector |

## **10.4 Networking entries & LinkedIn post analytics**

*Data:* `{user_dir}/CareerNavigator/tracker.json` → `networking[]`. *Capture behavior:* `skills/linkedin-post-analytics/SKILL.md`.

`{user_dir}/CareerNavigator/tracker.json` includes a **`networking`** array (alongside **`applications`**) for relationship and visibility artifacts. The **`linkedin-post-analytics`** skill may add or update entries with **`type: "linkedin_post"`**, a stable **`url`** (LinkedIn activity URN URL), optional **`description`** / **`date_posted`**, and **`analytics_history`**: an array of dated objects capturing impressions, reach, reactions, comments, reposts, saves, sends, profile viewers attributed to the post, followers gained, link visits, optional **`links`**, and optional **`top_audience`** (industry, seniority, company size) when the UI exposes them. **`networking-strategist`** recommends this cadence for users who publish on LinkedIn; schema details are defined in **`skills/linkedin-post-analytics/SKILL.md`**.

## **10.5 Story Corpus**

*Primary file:* `{user_dir}/CareerNavigator/StoryCorpus.json`.

The story corpus is a persistent, compressed interview-evidence layer extracted from raw journals, PKM notes, debriefs, and related source documents. It exists so interview flows can retrieve focused evidence without re-reading large raw sources on every run.

**Three-layer architecture:**

1. **Extraction (offline/one-time or incremental):** `mine-stories` chunks source entries, runs a low-cost extraction pass, and stores structured candidates.
2. **Persistent corpus:** flattened story records are saved in `StoryCorpus.json` with competency/theme tags and quality/result/ownership signals.
3. **Dynamic mapping (query-time):** `story-retrieval` pulls a small fit-ranked subset for prep/mock workflows (default 8-12 stories).

Suggested record shape:

- `story_id`
- `source` (`journal` | `pkm` | `debrief` | `resume` | `other`)
- `date`
- `raw_summary`
- `themes[]`
- `competencies[]`
- `result_signal`
- `ownership_signal`
- `star_ready`
- optional `embedding[]`

Interview prep/mocks use this corpus as the source of truth for "how have I done things," while ExperienceLibrary remains the core accomplishment inventory for tailoring and broader career workflows.

## **10.6 Career trajectory & offer context artifacts**

Two decision-support artifacts are persisted for reuse across skills:

- **`{user_dir}/CareerNavigator/career-trajectory.md`**  
  Produced by `career-plan`. Includes a human-readable trajectory report plus a `career_trajectory_v1` JSON block used by downstream ranking and scheduling nudges.

- **`{user_dir}/CareerNavigator/offer-context-{application_id}.json`**  
  Produced by `evaluate-offer`. Captures scenario classification, benchmark framing, and leverage context so `negotiate-offer` and `compare-offers` can continue without redundant re-collection.

# **11. The Intelligence Feedback Loop**

*Related implementation:* `agents/analyst/AGENT.md`, `agents/job-scout/AGENT.md`, `agents/resume-coach/AGENT.md`, `skills/pattern-analysis/SKILL.md`, `skills/ai-analysis/SKILL.md` (and tracker writes from `track-application` / tailoring skills).

The core differentiator of Career Navigator is a closed feedback loop that connects every outcome back to future recommendations. The loop operates as follows:

* User applies using artifact A, assembled from experience units X, Y, Z
* Outcome is logged (callback / rejection / silence)
* Insight engine analyzes outcome patterns across all applications
* Patterns are surfaced to the user in the pipeline dashboard and daily digest
* Performance weights on experience units are adjusted based on outcome correlation
* Job scout incorporates updated weights into future role ranking
* Resume coach incorporates updated weights into future artifact assembly recommendations
* Interview coach incorporates current events and company research into mock sessions
* Morning brief incorporates same current events for day-of interview preparation

Over time, the system builds a personalized model of what works for this specific user in their specific market — not generic best practices.

# **12. Daily Rhythm & Scheduling**

*Skill files:* `skills/daily-schedule/SKILL.md`, `skills/focus-career/SKILL.md`, `skills/artifact-saved/SKILL.md`, `skills/follow-up/SKILL.md` (as needed for hygiene).

Scheduling split (single source of truth):

* **`focus-career` skill** = critical-only, time-sensitive surfacing (typically when the user opens a session; optionally on a short cadence via `/schedule` if they want).
* **`daily-schedule` skill** = routine operating brief — **intended to be run daily** via Claude Cowork **`/schedule`** (user configures time/cadence).

The plugin documents **recommended cadences** inside skills; **execution** is owned by Cowork's scheduler.

## **12.1 Recommended cadences (Cowork `/schedule`)**

| Name | Suggested cadence | How to run |
| --- | --- | --- |
| **Daily operating brief** | Daily (user picks time) | Schedule a task whose payload invokes the `daily-schedule` skill (e.g. `/career-navigator:daily-schedule` or natural language equivalent). |
| **Career trajectory refresh check** | Monthly checkpoint inside daily runs | `daily-schedule` checks staleness of `career-trajectory.md` and nudges `/career-navigator:career-plan` when refresh is due. |
| **Follow-up / pipeline hygiene** | Daily (often same task as above) | Covered by `daily-schedule` + conversational `follow-up` as needed. |
| **Market intelligence** | Weekly | Schedule `/career-navigator:market-brief` (or invoke `market-brief` skill). |
| **Outcome pattern refresh** | Weekly or after milestone outcomes | User runs `/career-navigator:pattern-analysis` or schedules it after major tracker updates. |
| **LinkedIn post analytics snapshot** | Weekly or biweekly | Schedule a task that invokes the **`linkedin-post-analytics`** skill (or `/career-navigator:linkedin-post-analytics`) **only after** the user has approved host browser automation and is logged into LinkedIn in that browser. |

## **12.2 Time-sensitive vs routine surfacing**

| Situation | Where it lives |
| --- | --- |
| Imminent deadlines, same-day follow-ups, urgent interview-day actions | `focus-career` skill (critical-only). |
| Pipeline digest, artifact counts, weekly-style prompts | `daily-schedule` skill (scheduled). |
| Post-save inventory drift (PDF/DOCX on disk vs index) | `artifact-saved` skill (from `daily-schedule` when files exist, or after saves). |

Future phases may add richer "event radar" and offer/interview prompts; those remain **skill payloads** scheduled or invoked by the user in Cowork unless the host adds first-class hooks later.

# **13. Interview Capture (Phase 2B)**

*Implementation:* Phase **2B** — `agents/interview-coach/AGENT.md` is present (`prep-interview`, `mock-interview`, `daily-schedule` pre-interview subsection). **`interview-capture`** is implemented as **`skills/interview-capture/SKILL.md`** (not an agent). **`interview-debrief`** remains to be shipped for structured post-interview capture when shipped.

Interview capture is an opt-in feature that uses **user** audio and transcription (e.g. **`mcp-voice`** **`listen`**, or other STT MCP) to log interview content. It is bundled with the full interview preparation system in Phase 2B, shipping together so the prep and capture experiences are developed and tested as a unified layer. The post-interview Q&A debrief (`/career-navigator:interview-debrief`) is the primary debrief path for users who do not use audio capture.

## **13.1 MVP Audio Scope**

The Phase 2B MVP records **user audio only**. Audio from other participants is not captured; the system relies on the user's interview notes (via `/career-navigator:interview-debrief`) for counterparty content. This scoping sidesteps multi-party consent requirements in most jurisdictions for the MVP release.

**Employer policy warning:** Surfaced once — at the user's first recording session — to note that some employers prohibit any recording of interviews. The warning is not repeated on subsequent sessions.

**Data retention:** The user's `location` field in `profile.md` is used to determine the applicable local retention policy (e.g. GDPR for EU users, CCPA for California). If jurisdiction cannot be determined from the profile location, the user is prompted to select a policy at the start of their first recording session. All audio and transcript data remains user-deletable on demand.

**Full two-party capture** (recording both sides of the conversation) is out of scope for Phase 2B MVP and will require a full multi-party consent model, cross-jurisdiction legal review, and storage architecture design before it is considered.

## **13.2 Fallback: Post-Interview Q&A Flow**

For users who do not use audio capture, the interview debrief command provides a conversational Q&A that captures equivalent structured data:

* How did the interview go overall?
* What stage was it? Who did you meet with?
* What topics came up that you weren't expecting?
* Any red flags or particularly positive signals?
* What follow-up actions did you commit to?
* Any intel about the role, team, or company worth noting?

Claude structures the responses into the application record automatically, inferring sentiment and extracting action items.

# **14. The Honest Advisor Design Philosophy**

*Implementation:* `agents/honest-advisor/AGENT.md`; skills `skills/assessment/SKILL.md`, `skills/training-roi/SKILL.md`, `skills/suggest-roles/SKILL.md` (with `market-researcher`).

The honest-advisor agent operates by a specific three-step pattern for any assessment involving barriers or challenges:

* State the general norm — what typically happens in this situation across the market
* Research the exceptions — specific geographies, companies, industries, or contexts where the norm breaks down, and why
* Provide actionable strategy — concrete steps the user can take to position themselves in the exception category rather than the norm

The advisor never tells the user what to believe or what decisions to make. It provides honest information about how the world works, where it works differently, and what options exist. The user decides.

For factors the user cannot change (age, career gaps, unconventional backgrounds), the advisor acknowledges the reality of bias honestly while focusing energy on strategies and contexts where those factors matter less or work as advantages.

The advisor is calibrated to be less confrontational when the user has an interview imminent, a rejection is recent, or other stress signals are present. Honest delivery is adjusted for timing without compromising accuracy.

# **15. Phased Delivery Plan**

*Details:* `references/career-navigator-spec.md` (this doc).
*Test / verification notes:* `references/phase-test-plan.md`.

## **Phase 1 — Core Platform**

Phase status:

* Phase 1A: Completed
* Phase 1B: Completed
* Phase 1C: Completed
* Phase 1D: Completed
* Phase 1E: Completed
* Phase 1F: Completed
* Phase 1G: Completed
* Phase 2A: Completed
* Phase 2B: Completed

Phase 1 builds the complete local-first job search intelligence platform. The foundation in Phase 1A establishes the plugin scaffold, setup flow, and live job search. Phase 1B constructs the full skill layer — workflow skills that activate from conversational context, a closed feedback loop connecting application outcomes to future recommendations, and a pipeline dashboard. Phase 1C adds candid role assessment and skills gap analysis. Phase 1D extends the job-scout agent with outcome-weighted scoring and proactive opportunity discovery. Phase 1E completes the platform with professional presence tools: networking strategy, event radar, and LinkedIn content advising. At the end of Phase 1, all core job search workflows are intelligent, locally self-contained, and require no external service dependencies.

### **Phase 1A — Core platform: plugin scaffold, setup, session start, and live job search**

Status: Completed

* Plugin scaffold: manifest, directory structure
* **`launch` skill** and conversational configuration wizard — scans the job search folder, auto-imports existing resumes into ExperienceLibrary, builds user profile from available documents; falls back to conversational Q&A if no source documents found; initializes all data schemas (ExperienceLibrary, tracker, artifacts index); walks Indeed (and optional Apify); **offers** optional **Gmail** / **Microsoft 365** inbox connectors, optional **Google Calendar**, and optional **`linkedin-post-analytics`** when the user opts in. Slash command: **`/career-navigator:launch`**.
* `search-jobs` skill — live job search via Indeed connector; assisted-manual fallback
* `focus-career` skill — critical-only alerts when the user begins a session (or on a user-scheduled cadence via Cowork `/schedule`); onboarding on first run
* Local filesystem storage — all data written to `{user_dir}`; no cloud dependency

### **Phase 1B — Skill layer and intelligence: workflow skills, application tracker, ATS scoring, and analyst agent**

Status: Completed

* **Agents introduced:** `resume-coach` (resume assembly, ATS optimization, narrative coaching), `analyst` (outcome pattern analysis, transferable strengths identification, AI displacement assessment), `job-scout` (full outcome-weighted job ranking, proactive opportunity alerts, transferable skills analysis)
* Workflow skills built and auto-triggered: `tailor-resume`, `cover-letter`, `track-application`, `add-source`, `resume-score`, `list-artifacts` — activate from conversational intent; also invocable via explicit commands
* Application tracker — full conversational tracking with stage history, contacts, notes, and outcome logging
* ATS scoring — keyword match, formatting compliance, and narrative strength scoring on generated and existing resumes
* `ats-optimization` and `salary-research` context skills
* Insight engine and feedback loop — outcome data feeds back into ExperienceLibrary performance weights and job-scout scoring
* Benchmarking against industry norms by role, level, company size, and geography
* Follow-up timeline intelligence with company-specific response window data
* D3 pipeline dashboard with timeline view and benchmark comparisons *(**forecast** + **voice cadence** overlays are **Phase 3 — Dashboard & visualization enhancements** in §15—not part of Phase 1B scope)*
* `/career-navigator:pipeline`, `/career-navigator:follow-up`

### **Phase 1C — Advisor layer: honest role assessment, skills gap analysis, and training ROI**

Status: Completed

* **Agents introduced:**

  + `honest-advisor` candid role competitiveness assessment, norm/exception/strategy pattern
  + `market-researcher` role demand trends, AI/automation displacement, geographic signals

    triggered through `/career-navigator:market-brief` skill
* Skills assessment and gap analysis against target role requirements
* Training recommendation engine with cost-benefit-time ROI analysis (certifications, degrees, bootcamps, self-study)
  * **Note:** The `training-roi` skill currently runs on static knowledge for certification-value and outcome data. Before this is considered production-quality, live data sources should be evaluated — starting with the CareerOneStop DOL API (already listed in §9) and any available MCPs that surface bootcamp outcomes or labor market projections. If a viable connector is identified, integrate with `training-roi` in the next maintenance pass.
* `/career-navigator:suggest-roles`, job scout scoring improvements driven by outcome data

  + Note: skills assessment becomes significantly richer once Phase 2B mock interview performance data feeds back into the profile

### **Phase 1D — Proactive discovery: outcome-weighted job scoring and market trend monitoring**

Status: Completed

* Expanded/tuned `job-scout` weighting and ranking behavior as outcome history matures
* Non-obvious role suggestions based on transferable skills
* Market trend monitoring with proactive notifications for significant shifts
* Role demand forecasting incorporating AI/automation displacement signals

### **Phase 1E — Professional presence: networking strategy, event radar, and LinkedIn writer**

Status: Completed

**Scope (what 1E is responsible for):** conversational **skills + agents + slash commands** for networking strategy, network mapping (**`network_map_v1`** / optional `network-map.md` persistence), event intelligence and multi-scope **event-radar** (including optional **`event_radar_v1`** / `event-radar.md`), and all **user-facing copy** via **`writer`** (outreach, cover letters, follow-ups, resume Summary polish, topic ideas, post drafts, risk evaluation). **`/career-navigator:launch`** seeds **`voice-profile.md`** from on-disk résumés/CVs/covers and prompts for LinkedIn samples; **`writer`** maintains samples, multi-context tone notes, and quality flags. Full **post drafts** for review are **saved** under **`{user_dir}/LinkedIn Posts/`** and indexed as **`linkedin_post`** in **`artifacts-index.json`**.

**Cultural/political risk evaluation:** `writer` invokes `market-researcher` to assess target-company- and industry-specific norms before evaluating post risk. Risk output informs the user; it does not prescribe content decisions or suppress legitimate expression.

**1E deliverables (target checklist):**

* **Agents:** `networking-strategist`; `writer` (as scoped in §4).
* **Skills:** `networking-strategy`, `network-map`, `event-intelligence`, `event-radar`, `draft-outreach`, `content-suggest`, `evaluate-post`; `cover-letter` and `follow-up` orchestrate **`writer`** via **CoverLetterBrief** / **FollowUpBrief**.
* Event radar with **local, regional, national, and international** discovery where appropriate (within available tools).
* Presentation opportunity flagging; CFP / visibility assessment in **`event-intelligence`**.
* LinkedIn topic recommendations; full **post drafts** persisted to disk; **`evaluate-post`** (cultural/political/reputational risk via `market-researcher` + target profiles).
* **`voice-profile.md`** / **`voice_profile_v1`** for tone matching (launch harvest + user samples).
* Commands: `/career-navigator:networking-strategy`, `/career-navigator:network-map`, `/career-navigator:event-intelligence`, `/career-navigator:event-radar`, `/career-navigator:draft-outreach`, `/career-navigator:content-suggest`, `/career-navigator:evaluate-post`. (**`/career-navigator:contact-context`** ships in Phase **2A** (completed); see §3.4.)

### **Phase 1F — Career planning, offer evaluation & compensation negotiation**

Status: Completed

Phase 1F adds “decision-grade” career planning and offer evaluation / negotiation capabilities into Phase 1 by extending `honest-advisor` + `market-researcher`. It introduces skills and slash commands for realistic trajectory planning, scenario-aware offer evaluation, and negotiation handoffs, and wires `job-scout` / `daily-schedule` to consume the new artifacts on a monthly cadence.

**Critical mechanics shipped:**

- **`career-plan`** writes `career_trajectory_v1` to `career-trajectory.md` for downstream reuse.
- **`evaluate-offer`** writes `offer-context-{application_id}.json` so later workflows can skip repetitive data capture.
- **`compare-offers`** consumes existing offer contexts and runs inline evaluation only when a context is missing.
- **`negotiate-offer`** generates a `NegotiationHandoffBrief` consumed by `writer` for final send-ready negotiation copy.
- **Nudges integrated:** `daily-schedule` performs a monthly trajectory refresh check, and offer-stage hygiene nudges evaluation when no offer context exists.

More detail: `references/phase-1f-spec.md`.

### **Phase 1G — Marketplace publication**

Status: Completed

**Deliverable: Claude Plugin Marketplace Publication**

A laid-off tech worker in Austin finds Career Navigator in a plugin marketplace, installs it in ten minutes, and has a functioning job search agent running by the end of the day — without needing to understand MCP, local tool configuration, or how agent runtimes work.

**Impact:** transforms Career Navigator from a personal tool into a publicly available product with real user validation (downloads and activation become measurable proof of demand).

## **Phase 2 — Integrations**

Phase 2 connects Career Navigator to the external services that complete the full job search experience: inbox + calendar context, interview capture, portable storage, event intelligence, and interview-story intelligence. Each sub-phase is independently deployable.

### **Phase 2A — Email & Calendar Integration**

Status: Completed

**Plugin release:** [v2.1.0](https://github.com/tmargolis/career-navigator/releases/tag/v2.1.0)

**Deliverable: Inbox + Calendar Context**

*You’re about to reach out to a hiring manager, but you can’t remember if you already spoke with them—or what you promised on the last call. Career Navigator pulls the relevant email thread(s) and recent meeting context (with explicit permission), summarizes only what it finds, and feeds that context into outreach and follow-ups so you never accidentally repeat yourself or miss a prior commitment.*

**Impact:** turns “warm outreach” from guesswork into evidence-backed communication grounded in actual history.

**Scope includes:**

* Gmail and Outlook OAuth connectors (read-only scoped)
* Google Calendar and Outlook Calendar read-only access
* Contact correspondence history search for networking context
* Contact context skill: surfaces prior email/meeting history before outreach drafting
* Outreach drafting enriched with prior communication history
* Meeting history awareness for warm networking identification — **past** and **scheduled (upcoming)** calendar events with a contact; **`contact-context`** emits **`upcoming_meetings`** and **`warm_networking`** so outreach does not cold-open when a meeting is already on the calendar
* **`linkedin-post-analytics`** skill and **`/career-navigator:linkedin-post-analytics`** command: **read-only** snapshots of the user’s **own** LinkedIn post analytics into **`tracker.json`** `networking[]` (see §10.4, §12.1). Depends on **host browser automation** (**Claude in Chrome**, **computer / browser use**, or equivalent) and **explicit user approval**; **`networking-strategist`** recommends cadence for visibility-focused users. **`/career-navigator:launch`** **offers** this as an optional step after Indeed/Apify when the user wants a first run.

### **Phase 2B — Interview intelligence**

Status: Completed

**Plugin release:** [v2.2.0](https://github.com/tmargolis/career-navigator/releases/tag/v2.2.0)

**Deliverable: Full Interview Loop (Prep → Practice → Capture → Debrief)**

*You have a hiring manager interview tomorrow. Career Navigator generates a morning brief (company news, interviewer context, talking points), runs an adaptive mock interview tailored to the stage and vibe, and after the interview captures what happened (audio capture if you opted in, otherwise a structured Q&A debrief). The tracker is updated automatically so your follow-ups and next-round prep are always based on what actually occurred—not what you vaguely remember a week later.*

**Impact:** upgrades interviews from “one-off events” into a repeatable, measurable loop that improves with each round.

**Scope includes:**

* **Agents introduced:** `interview-coach` (mock interviews across all stages and vibes, adaptive difficulty, current events integration)
* **Skills introduced / extended:** `interview-capture` (**skill**, not an agent — audio transcription via **`mcp-voice`** **`listen`** or compatible STT, structured tracker population — opt-in only; MVP scope: user audio only)
* Mock interview system: guided, random, and adaptive modes
* All stages: recruiter screen, hiring manager, technical, panel, executive, final
* Full vibe spectrum: supportive, neutral, challenging, antagonistic, bored (calibrated — not demoralizing; exact calibration of antagonistic mode confirmed via user testing before ship)
* Current events integration woven into mock interview questions
* Morning brief with company news, interviewer research, and talking points
* Post-interview Q&A debrief flow (`/career-navigator:interview-debrief`) — structured conversational capture; serves as the primary debrief path for users who do not use audio capture
* `/career-navigator:prep-interview`, `/career-navigator:mock-interview`, `/career-navigator:morning-brief`
* Mock interview performance feeds back into Phase 1C skills profile
* **Audio capture — MVP scope:** user audio only; employer policy warning at first session only; jurisdiction-based retention policy derived from profile `location`; unknown jurisdiction prompts user to select. Full two-party capture deferred pending multi-party consent model and legal review.
* Local Whisper processing option for privacy-sensitive users
* Audio and transcript storage with user-controlled retention and deletion
* Auto-population of tracker from interview transcription

### **Phase 2C — Extended Integrations**

Status: Completed

**Plugin release:** [v2.3.0](https://github.com/tmargolis/career-navigator/releases/tag/v2.3.0)

**Deliverable: Portability + Employer-System Awareness**

*You switch laptops or you want your job search data backed up outside a single folder. Career Navigator can store artifacts in a cloud drive connector, pull read-only status updates from common ATS platforms, and incorporate additional job board sources—so your workflow stays consistent even as postings and employer systems vary.*

**Impact:** makes the system durable across devices and better aligned with the reality that applications live in third-party systems.

**Scope includes:**

* Google Drive, OneDrive or Dropbox portability via Drive app sync or manual backup/restore (recommended for job files)
* IllinoisJobLink job board connector
* ATS read-only connectors for Greenhouse, Workday, and Lever

### **Phase 2D — Event Intelligence & Interview Story Intelligence**

Status: Completed

**Plugin release:** [v2.4.0](https://github.com/tmargolis/career-navigator/releases/tag/v2.4.0)

**Deliverable: Event Intelligence + Story Evidence Loop**

*You’re choosing where to invest your networking time and preparing for interviews where weak stories can sink strong resumes. Phase 2D adds connector-backed event feeds for better opportunity selection and introduces interview-story intelligence that mines journals, notes, and PKM artifacts to identify, refine, and rehearse high-quality stories.*

**Impact:** improves both top-of-funnel networking decisions and late-stage interview performance with evidence-backed preparation.

**Scope includes:**

* **Event intelligence sources** for `event-radar` / `event-intelligence`: Luma via local MCP bundle (`mcp-luma`), with Meetup/Eventbrite handled as optional **Claude in Chrome**, **computer use**, or **manual copy/paste** fallback paths.
* **Event discovery design details:** vendor order, OAuth vs API keys, host packaging, MCP tool names, and deduplication behavior against user-edited `{user_dir}/CareerNavigator/event-radar.md`.
* **Interview story intelligence objective:** identify and prepare strong interview stories by mining user-owned journals, notes, and PKM sources (for example weekly logs, debrief notes, and knowledge base entries), then map stories to role competencies and common interview prompts.
* **PKM connector paths:** official **Notion** connector and optional **Capacities** MCP integration when available in-session; file export fallback remains first-class.
* **Interview story architecture:** three-layer pipeline — extraction via **`mine-stories`**, persistent **`StoryCorpus.json`**, and query-time competency mapping via **`story-retrieval`** to produce compact prep inputs.
* **Interview story prep outputs:** reusable story bank, quality checks (clarity, outcome, ownership, credibility), STAR-readiness flags, and targeted rehearsal prompts tied to upcoming interviews.

## **Phase 3 — Always-On Career Agent**

Status: In progress

Phase 3 evolves Career Navigator from “a powerful assistant you sit down with” into an always-on, context-maintaining career operating layer that runs on a cadence and meets you in the channels you already use.

This phase is explicitly shaped by industry trends kicked off by **OpenClaw** — persistent threads, asynchronous task orchestration (“dispatch”), and event-driven channels — and by the broader “clawification” race across AI products. While the current product is packaged as a plugin for Claude Cowork, the Phase 3 intent is **host-agnostic**: design for any runtime that can support scheduled runs, connector access, and mobile/remote interaction.

**Deliverable: Morning Digest**

*When you wake up, glance at your phone, and see that a recruiter at Stripe responded to your application overnight. The digest has already summarized their email, noted you have a Salesforce follow-up going stale at 6 days with no response, and surfaced that Anthropic posted a new role matching your profile. You walk into your day knowing exactly what to do — before you've opened a laptop.*

**Impact:** eliminates the daily manual check across email, job boards, and your tracker.

**Deliverable: Advanced Analytics Exports**

*Power users and coaches need analytics outside the chat surface. Phase 3 adds export paths to external BI and visualization tools so users can build custom reporting views while preserving Career Navigator as the operational system of record.*

**Impact:** enables external dashboards and deeper longitudinal analysis without changing core in-product workflows.

**Scope includes:**

* Power BI streaming dataset connector
* Qlik Engine API connector
* D3 data export connector for custom visualization

**Dashboard & visualization enhancements** *(deferred from Phase 1E; depends on stable interchange from 1E outputs):*

* **Pipeline timeline — forecast overlay:** extend **`/career-navigator:pipeline`** (D3) so the **timeline** shows a forward-looking **forecast** from **`networking-strategist`** outputs—planned or recommended relationship moves, high-ROI events, visibility milestones—alongside **historical** application stages. Requires persisting or deriving structured data from `networking-strategy`, `event-radar`, **`network_map_v1`**, **`event_radar_v1`**, and related artifacts; refresh cadence and schema TBD.
* **Pipeline timeline — voice cadence:** surface **`voice_profile_v1`** / **`voice-profile.md`** metadata (e.g. last harvest, sample dates, tone summaries) on or beside the timeline so users see how **public-facing cadence** tracks with applications and networking.
* **Network map graph UI:** interactive graph (or export path) consuming persisted **`network_map_v1`**—beyond narrative + JSON in chat / `network-map.md`.

**Deliverable: Weekly Market Brief**

*Every Monday morning a report lands telling you that "Head of AI Product" postings in Chicago jumped 23% this week, that two of your target companies announced hiring freezes, and that there's a relevant conference in two weeks with an open call for speakers. You adjust your outreach priorities accordingly instead of operating on stale assumptions.*

**Impact:** replaces ad-hoc research with a consistent intelligence cadence tied directly to your target list.

**Deliverable: Follow-up Alert**

*Six days after your final-round interview with a company, you haven't heard back. The system detects this, flags it as overdue against standard response benchmarks, and delivers a pre-drafted follow-up to your phone — ready to review and send. You make one edit and fire it off from the train.*

**Impact:** nothing falls through the cracks; the system manages the pipeline clock so you don't have to.

**Deliverable: Weekly Insight Report**

*Every Friday afternoon the system delivers a plain-language read of your week: 4 applications sent, 2 responses, 1 interview booked. It notes that every positive response this month came from roles where you led with AI research experience, and that roles framed around "data science leadership" are generating silence. It recommends one specific positioning adjustment for next week.*

**Impact:** turns a job search from a feelings-based experience into a data-informed one.

**Deliverable: Dispatch Mobile Layer**

*You're at lunch and remember your Anthropic interview is tomorrow. You send a message from your phone: "Prep me for my Anthropic interview tomorrow." By the time you're back at your desk, a full brief is waiting — company news, predicted questions, talking points, a note on something the hiring manager posted on LinkedIn last week.*

**Impact:** the full power of the desktop agent is available from anywhere, without opening a computer.

**Deliverable: Channels (Telegram, Slack)**

*You finish a difficult interview and immediately message your Telegram bot: "Just wrapped my Google interview, it went pretty well but they asked about distributed systems and I fumbled." The system walks you through a structured debrief, captures the details, updates your tracker, and flags a prep gap to address before the next round — all from your phone, while the interview is still fresh.*

**Impact:** replaces the "I'll log this later" promise that never happens with an ambient capture flow that meets you where you are.

**Deliverable: Computer Use (Universal Connector Fallback)**

*You want to do high-leverage actions in tools that don’t have a reliable API/connector — like updating your LinkedIn profile, messaging a recruiter, saving jobs, or checking application status in a proprietary portal. Instead of blocking on a dedicated MCP, the system can (with explicit permission) use “computer use” to operate the real UI: open the browser, navigate, extract the relevant page state, draft a message, and stage the action for your review. You get connector-level outcomes even when the ecosystem doesn’t offer connector-level access.*

**Impact:** removes “no connector” as a hard limitation, enabling end-to-end workflows (especially networking and LinkedIn-adjacent actions) while keeping approvals and guardrails explicit.

**Deliverable: Projects (Artifact & Workspace Organization)**

*You have dozens of roles in motion and hundreds of generated assets: tailored resumes, cover letters, follow-ups, interview briefs, dashboards, and market reports. Projects becomes the organizing layer that groups human-created and machine-generated artifacts by company/role (and links them back to tracker stages), so you can instantly answer “what’s the current resume for this role?” or “what did I send last time?” without hunting across folders or chat history.*

**Impact:** reduces artifact sprawl and makes multi-agent work legible—users can review, approve, and reuse outputs across sessions with clear provenance.

## **Phase 4 — Enterprise & Ecosystem**

**Deliverable: White-Label for Career Coaches**

*A career coach who charges $500/month for one-on-one job search support licenses Career Navigator under their own brand and serves 40 clients simultaneously instead of 8. Their clients get daily briefings, pipeline tracking, and market intelligence. The coach focuses their time on the high-touch conversations that require human judgment.*

**Impact:** multiplies the coach's capacity by 5x while raising the baseline quality of service every client receives.

**Deliverable: Anonymized Benchmark Data**

*After thousands of users run searches through Career Navigator, the system knows that AI research roles in Chicago have an average response window of 11 days at the phone screen stage, and that applications submitted Tuesday through Thursday outperform Monday and Friday sends by a statistically significant margin. Every user's follow-up timing and strategy improves because the system is calibrated against real aggregate outcomes rather than generic advice.*

**Impact:** the advice gets smarter with scale — individual users benefit from patterns they could never see on their own.

**Deliverable: Government / American Job Center Integration**

*A workforce development counselor at a Chicago AJC uses Career Navigator to support 60 displaced workers at once. Each client receives a personalized daily brief and automated follow-up reminders. The counselor reviews exception cases — the ones needing human intervention — rather than manually tracking every application across every client.*

**Impact:** scales high-quality job search support to populations who currently receive generic, under-resourced assistance.

**Deliverable: Veteran & Disability Pathway Modules**

*A veteran leaving the Army after 12 years has a strong record but no civilian job title vocabulary. Career Navigator's veteran module translates their service roles into civilian equivalents, maps their clearance to eligible roles, and generates resume language that hiring managers recognize — without requiring them to figure out the translation themselves.*

**Impact:** removes a structural disadvantage that causes qualified candidates to be overlooked for entirely preventable reasons.

**Deliverable: Early-Career / College Pathway**

*A college junior starts internship recruiting with no real system: a half-finished resume, scattered job links, and missed deadlines. Career Navigator turns their semester into an operating cadence — it builds a clean baseline resume from coursework, projects, and part-time work; generates role-specific variants for internships; tracks applications and recruiting stages; surfaces career fair and on-campus recruiting dates; drafts outreach to alumni and recruiters; and flags when follow-ups are overdue. By finals week, the student knows exactly what to do next without guessing.*

**Impact:** compresses the learning curve of early-career recruiting into repeatable workflows so students don’t miss deadlines, waste cycles on low-fit applications, or lose opportunities due to inconsistent follow-up.

# **16. Open Questions & Deferred Decisions**

*Working notes:* `references/phase-test-plan.md` (checks and open items may overlap this table).

| Name | Type | Description |
| --- | --- | --- |

# **Appendix: Command Quick Reference**

*full tables in §3 and §5.

| Command | Purpose |
| --- | --- |
| **/career-navigator:launch** | Launch job search workspace: configure folder, build ExperienceLibrary and profile, connectors; optional **`linkedin-post-analytics`** offer |
| **/career-navigator:tailor-resume** | Assemble resume via **`resume-coach`**; optional **`writer`** Summary polish |
| **/career-navigator:cover-letter** | **CoverLetterBrief** + **`writer`** final prose |
| **/career-navigator:resume-score** | Score resume against a job description |
| **/career-navigator:add-source** | Add source document to ExperienceLibrary |
| **/career-navigator:list-artifacts** | List all generated artifacts |
| **/career-navigator:search-jobs** | Search and rank job opportunities |
| **/career-navigator:track-application** | Log or update an application |
| **/career-navigator:pipeline** | View full application dashboard (timeline; **Phase 3:** forecast + voice cadence overlays) |
| **/career-navigator:follow-up** | **FollowUpBrief** + **`writer`** messages |
| **/career-navigator:market-brief** | Current market intelligence report |
| **/career-navigator:suggest-roles** | Discover non-obvious role opportunities |
| **/career-navigator:career-plan** | Trajectory analysis + ROI-ranked gap plan (`career_trajectory_v1`) |
| **/career-navigator:evaluate-offer** | Scenario-aware offer evaluation + persisted offer context |
| **/career-navigator:compare-offers** | Side-by-side multi-offer comparison and recommendation |
| **/career-navigator:negotiate** | Negotiation strategy + `writer` handoff for send-ready draft |
| **/career-navigator:networking-strategy** | Networking plan (strategy; outreach via **content-advisor**) |
| **/career-navigator:network-map** | Network paths/gaps + **`network_map_v1`** (Phase 3: graph UI) |
| **/career-navigator:event-intelligence** | Event ROI and presentation opportunity assessment |
| **/career-navigator:event-radar** | Multi-scope event discovery |
| **/career-navigator:prep-interview** | Full interview preparation session |
| **/career-navigator:mock-interview** | Mock interview (guided/random/adaptive); defaults if mode/vibe omitted |
| **/career-navigator:interview-capture** | Opt-in user-audio capture → transcript → tracker (**skill**) |
| **/career-navigator:interview-debrief** | Post-interview Q&A capture |
| **/career-navigator:morning-brief** | **Alias:** **`daily-schedule`** focused run — pre-interview brief for today only (see `skills/daily-schedule/SKILL.md`) |
| **/career-navigator:draft-outreach** | Draft outreach (**`writer`**) |
| **/career-navigator:contact-context** | Prior email/calendar thread summary (**past** + **upcoming** meetings, **warm_networking**) → **ContactContextBrief** (read-only; user approval) |
| **/career-navigator:content-suggest** | LinkedIn topic ideas (**`writer`**) |
| **/career-navigator:evaluate-post** | Post risk review — audience + cultural/political via **`market-researcher`** + **`writer`** |
| **/career-navigator:linkedin-post-analytics** | Read-only own LinkedIn post metrics → **`tracker.json`** `networking[]` (browser automation + user consent) |
