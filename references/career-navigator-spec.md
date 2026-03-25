**CAREER NAVIGATOR**

Claude Cowork Plugin — Full Product Specification

Version 0.22 — March 2026

An AI-powered job search companion that combines the capabilities of
recruiters, career coaches, reverse recruiters, and market analysts into a single intelligent platform.

# **Table of Contents**

[**1. Overview**](#1-overview)

[1.1 Design Principles](#11-design-principles)

[1.2 Plugin Architecture](#12-plugin-architecture)

[**2. Plugin File Structure**](#2-plugin-file-structure)

[**3. Slash Commands**](#3-slash-commands)

[3.1 Resume & Cover Letter Commands](#31-resume--cover-letter-commands)

[3.2 Job Search & Tracking Commands](#32-job-search--tracking-commands)

[3.3 Interview Prep Commands](#33-interview-prep-commands)

[3.4 Networking Commands](#34-networking-commands)

[**4. Agents**](#4-agents)

[**5. Skills**](#5-skills)

[**6. Scheduling & recurring runs**](#6-scheduling--recurring-runs)

[6.1 Host hooks (`hooks/hooks.json`)](#61-host-hooks-hookshooksjson)

[**7. Storage Connectors**](#7-storage-connectors)

[7.1 Interface](#71-interface)

[7.2 Available Connectors](#72-available-connectors)

[**8. Analytics Connectors**](#8-analytics-connectors)

[**9. External Service Integrations (.mcp.json)**](#9-external-service-integrations-mcpjson)

[**10. Core Data Model**](#10-core-data-model)

[10.1 ExperienceLibrary](#101-experiencelibrary)

[10.2 Application Record](#102-application-record)

[10.3 Artifact Record](#103-artifact-record)

[**11. The Intelligence Feedback Loop**](#11-the-intelligence-feedback-loop)

[**12. Daily Rhythm & Scheduling**](#12-daily-rhythm--scheduling)

[12.1 Recommended cadences (Cowork `/schedule`)](#121-recommended-cadences-cowork-schedule)

[12.2 Time-sensitive vs routine surfacing](#122-time-sensitive-vs-routine-surfacing)

[**13. Interview Capture (Phase 2B)**](#phase-2b--interview-audio-capture)

[13.1 MVP Audio Scope](#131-mvp-audio-scope)

[13.2 Fallback: Post-Interview Q&A Flow](#132-fallback-post-interview-qa-flow)

[**14. The Honest Advisor Design Philosophy**](#14-the-honest-advisor-design-philosophy)

[**15. Phased Delivery Plan**](#15-phased-delivery-plan)

[Phase 1 — Core Platform](#phase-1--core-platform)

[Phase 1A — Core platform: plugin scaffold, setup, session start, and live job search](#phase-1a--core-platform-plugin-scaffold-setup-session-start-and-live-job-search)

[Phase 1B — Skill layer and intelligence: workflow skills, application tracker, ATS scoring, and analyst agent](#phase-1b--skill-layer-and-intelligence-workflow-skills-application-tracker-ats-scoring-and-analyst-agent)

[Phase 1C — Advisor layer: honest role assessment, skills gap analysis, and training ROI](#phase-1c--advisor-layer-honest-role-assessment-skills-gap-analysis-and-training-roi)

[&nbsp;&nbsp;&nbsp;&nbsp;Phase 1C — Advisor layer: honest role assessment, skills gap analysis, and training ROI	20](#phase-1c--advisor-layer-honest-role-assessment-skills-gap-analysis-and-training-roi)

[Phase 1E — Professional presence: networking strategy, event radar, and LinkedIn content advisor](#phase-1e--professional-presence-networking-strategy-event-radar-and-linkedin-content-advisor)

[Phase 2 — Integrations](#phase-2--integrations)

[Phase 2A — Email & Calendar Integration](#phase-2a--email--calendar-integration)

[Phase 2B — Interview intelligence: mock interview system, morning brief, audio capture, and post-interview debrief](#phase-2b--interview-intelligence-mock-interview-system-morning-brief-audio-capture-and-post-interview-debrief)

[Phase 2C — Extended Integrations](#phase-2c--extended-integrations)

[Phase 2D — Advanced Analytics, LinkedIn Automation & Dashboard Enhancements](#phase-2d--advanced-analytics-linkedin-automation--dashboard-enhancements)

[Phase 3 — Platform Expansion](#phase-3--platform-expansion)

[Phase 4 — Enterprise & Ecosystem](#phase-4--enterprise--ecosystem)

[**16. Open Questions & Deferred Decisions**](#16-open-questions--deferred-decisions)

[**Appendix: Command Quick Reference**](#appendix-command-quick-reference)

# **1. Overview**

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
| **Version** | 1.5.0 |
| **Platform** | Claude Cowork (macOS / Windows / Linux) (also compatible with Claude Code) |
| **Architecture** | Skill-first — behavioral intelligence lives in skills with conversational triggers; commands are explicit invocation aliases for key workflows |
| **Scheduling** | User-configured in Claude Cowork — skills are the payload; recommended cadences are documented in skill files (e.g. run `daily-schedule` daily via `/schedule`) |
| **Notifications / surfacing** | In-session UX (e.g. `session-start` for critical items) plus whatever Cowork provides when a scheduled task runs — the plugin does not ship a separate notification daemon |
| **Storage Layer (Phase 1)** | Local filesystem — `{user_dir}` (cloud connectors in Phase 2C) |
| **Analytics Layer (Phase 1)** | SQLite + D3 visualization (additional connectors in Phase 2D) |
| **AI Services** | Claude API (via MCP), Whisper (audio transcription — Phase 2B) |
| **Job Search (Phase 1)** | **Indeed** MCP via Claude Desktop **Customize → Connectors** — **Connect** → browser OAuth on **secure.indeed.com**; tools **`search_jobs`**, **`get_job_details`** (connector `https://mcp.indeed.com/claude/mcp`). User must complete OAuth; assisted-manual fallback when connector unavailable |
| **Salary benchmarks (Phase 1, optional)** | Apify MCP added in Claude Desktop **Customize → Connectors → Desktop → Apify** (token + **Enabled tools** list in connector UI); plugin **`.mcp.json`** ships **`mcpServers: {}`** |

# **2. Plugin File Structure**

**career-navigator/**

**├── .claude-plugin/**

**│ └── plugin.json**

**├── .mcp.json** — ships **`mcpServers: {}`**; optional MCPs (e.g. Apify for salary) are configured in the host app

**├── agents/**

**├── skills/**

**├── hooks/**

**│ ├── hooks.json**

**│ └── context/** — e.g. `session-start.md` injected on `SessionStart`

**├── references/**

**├── career/** *(example `{user_dir}` — gitignored when personal)*\*\*

**└── README.md**

# **3. Slash Commands**

All commands are namespaced under career-navigator: and accessible via Claude Cowork's slash command interface (and Claude Code). Commands can also be triggered conversationally — the plugin recognizes natural language prompts that match command intent and invokes the appropriate command automatically.

## **3.0 Launch & configuration**

| Name | Type | Description |
| --- | --- | --- |
| **/career-navigator:launch** | Command | **Launch** the user's job search workspace: conversational wizard that configures `{user_dir}`, reads existing documents, builds the user profile and ExperienceLibrary, and walks through connectors for live job search (Indeed, optional Apify, etc.). Same setup responsibilities as before; framed as the entry point to start searching. Validates inputs before saving; re-runnable to update keys or reconfigure. |

## **3.1 Resume & Cover Letter Commands**

| Name | Type | Description |
| :---- | :---- | :---- |
| **/career-navigator:tailor-resume** | Command | Takes one or more source documents from the ExperienceLibrary and a job description, assembles and rewrites the best possible resume for that specific role, scores it for ATS compatibility, and saves it to the artifact inventory. |
| **/career-navigator:cover-letter** | Command | Builds a **CoverLetterBrief**, then invokes **`content-advisor`** for final prose (voice-aware). Saves to artifact inventory. |
| **/career-navigator:resume-score** | Command | Scores an existing resume or cover letter against a job description for ATS keyword match, formatting compliance, and narrative strength. |
| **/career-navigator:add-source** | Command | Adds a new source document (resume, CV, portfolio) to the ExperienceLibrary for use in future tailoring. |
| **/career-navigator:list-artifacts** | Command | Lists all generated artifacts in the inventory with metadata: date created, job applied for, outcome if known. |

## **3.2 Job Search & Tracking Commands**

| Name | Type | Description |
| :---- | :---- | :---- |
| **/career-navigator:search-jobs** | Command | Searches configured job boards and returns ranked results. Ranking incorporates skill match, outcome history, and market intelligence. Supports filters for role, location, company size, industry, and salary range. |
| **/career-navigator:track-application** | Command | Logs a new application or updates an existing one. Accepts conversational input and structures it automatically into the tracker database. |
| **/career-navigator:pipeline** | Command | Displays the full application pipeline dashboard with timeline view, benchmark comparisons, and action items flagged by stage age. **Roadmap:** **forecast** overlay and **voice cadence** on the timeline—see **Phase 2D — Dashboard & visualization enhancements** in §15. |
| **/career-navigator:follow-up** | Command | Classifies applications by response windows, builds **FollowUpBrief** entries, invokes **`content-advisor`** for send-ready messages. Email/calendar enrichment Phase 2A. |
| **/career-navigator:market-brief** | Command | Generates a current market intelligence report for the user's target roles and industries, including trend data, competition levels, and AI/automation impact assessment. |
| **/career-navigator:suggest-roles** | Command | Analyzes the user's full ExperienceLibrary and suggests non-obvious role types their skills could be applied to, with rationale for each suggestion. |

## **3.3 Interview Prep Commands**

| Name | Type | Description |
| :---- | :---- | :---- |
| **/career-navigator:prep-interview** | Command | Launches a full interview preparation session for a specific role. Pulls in company research, generates predicted questions, and optionally launches a mock interview. |
| **/career-navigator:mock-interview** | Command | Starts a mock interview session. Accepts mode (guided/random/adaptive), stage (recruiter/HM/technical/panel/executive), and vibe (supportive/neutral/challenging/antagonistic/bored) parameters. |
| **/career-navigator:interview-debrief** | Command | Post-interview Q\&A flow that captures the candidate's experience conversationally and structures it into the tracker. Fallback for users who do not use audio capture. |
| **/career-navigator:morning-brief** | Command | Generates a pre-interview briefing for any interview scheduled today: company news, interviewer research, talking points, and current events likely to come up. |

## **3.4 Networking Commands**

| Name | Type | Description |
| :---- | :---- | :---- |
| **/career-navigator:networking-strategy** | Command | Builds an evidence-based networking plan (priorities, sequencing, gaps). Optional handoff brief for **`content-advisor`** when messaging is needed. Invokes **`networking-strategist`**. |
| **/career-navigator:network-map** | Command | Maps plausible paths and gaps to target employers; outputs narrative plus **`network_map_v1`** JSON (and may persist to `network-map.md`). **Interactive graph UI** is **Phase 2D**—see §15. |
| **/career-navigator:draft-outreach** | Command | Drafts outreach copy (LinkedIn, email, InMail, etc.). Invokes **`content-advisor`**. Searches email and calendar history for prior context with user approval when Phase 2A connectors exist. |
| **/career-navigator:event-intelligence** | Command | Deep evaluation of specific events: ROI, audience fit, cost/time, and **presentation / speaking** opportunity flagging. Invokes **`networking-strategist`**. |
| **/career-navigator:content-suggest** | Command | Suggests LinkedIn post topics based on current industry trends, the user's target roles, and recent activity in their field. Invokes **`content-advisor`**. |
| **/career-navigator:evaluate-post** | Command | Evaluates a draft post for audience fit, algorithmic performance, and **cultural / political / reputational** risk vs target companies. Invokes **`content-advisor`**. |
| **/career-navigator:event-radar** | Command | Discovers events across **local, regional, national, and international** scopes (as appropriate); ranked with ROI tiers and presentation flags. Invokes **`networking-strategist`**. |

# **4\. Agents**

Agents are specialized Claude instances with focused roles. They can be invoked directly or orchestrated by commands. Multiple agents may collaborate on complex tasks.

| Name | Phase | Description |
| :---- | :---- | :---- |
| **resume-coach** | 1B | Analyzes the ExperienceLibrary, identifies gaps and strengths, optimizes for ATS compatibility, and provides narrative coaching. Invoked by the `tailor-resume` and `resume-score` skills. May emit a **ResumeSummaryBrief** for **`content-advisor`** when **`tailor-resume`** requests voice-aligned Summary polish. |
| **analyst** | 1B | Analyzes application outcome data to identify patterns in what's advancing and what isn't. Identifies transferable strengths and core capabilities in the user's experience that apply across roles and industries. Assesses AI and automation displacement risk for current and target roles using the Anthropic Economic Index. Updates ExperienceLibrary performance weights and feeds recommendations to `job-scout` and `resume-coach`. |
| **honest-advisor** | 1C | Provides candid assessments of the user's competitiveness for specific roles, potential recruiter concerns, and strategies for overcoming barriers. Researches company/industry-specific deviations from general norms. Empathetic but unsparing. |
| **market-researcher** | 1C | Monitors macro hiring trends, role-specific demand signals, AI/automation displacement risks, geographic demand patterns, and sector-specific cycles. Feeds the `market-brief` command and the `job-scout` agent. |
| **job-scout** | 1D | Searches and ranks job opportunities across all configured job boards. Incorporates outcome history and market intelligence into scoring. Ranking improves over time as the user logs outcomes. Proactively surfaces high-match opportunities. |
| **networking-strategist** | 1E | Network analysis, gap identification, and warm-path planning. Event discovery and evaluation with ROI assessment, **presentation-opportunity** flagging, and multi-scope **event radar** (via **`event-intelligence`** and **`event-radar`** skills). May emit a structured **handoff brief** for **`content-advisor`** when messaging is needed; does **not** draft outreach copy. |
| **content-advisor** | 1E | Owns **Career Navigator user-facing copy**: outreach (LinkedIn, email, InMail), **cover letters** (from **CoverLetterBrief**), **follow-ups** (from **FollowUpBrief**), optional **resume Summary** polish (**ResumeSummaryBrief**), post drafts (saved under **`{user_dir}/LinkedIn Posts/`** + **`artifacts-index.json`** as **`linkedin_post`**), **`/career-navigator:draft-outreach`**, **`content-suggest`**, **`evaluate-post`**. Maintains **`voice-profile.md`** (and optional **`voice_profile_v1`**) for tone matching; **timeline surfacing** of voice metadata is **Phase 2D**. Consumes handoffs from **`networking-strategist`**, **`resume-coach`** (summary path), **`cover-letter`**, **`follow-up`**. Outreach email/calendar enrichment **Phase 2A**. |
| **interview-coach** | 2B | Conducts mock interviews across all stages and vibes (supportive, neutral, challenging, antagonistic, bored). Adapts difficulty based on user performance in adaptive mode. Incorporates current events and company-specific research into questions. |
| **interview-capture** | 2B | Processes audio transcription from interviews (via Whisper), extracts structured data, and auto-populates the tracker. Only active with explicit user opt-in. Full privacy framework required before activation. |

# **5\. Skills**

Skills are auto-triggered capabilities that Claude activates when relevant context is detected, without requiring an explicit command invocation. This is the primary interaction model for Career Navigator — commands serve as explicit aliases for users who prefer them, but skills carry the behavioral intelligence.

**Workflow skills** handle the core job search operations and fire from conversational intent:

| Name | Type | Description |
| :---- | :---- | :---- |
| **tailor-resume** | Skill | Fires when the user shares or pastes a job description, or expresses intent to apply to a specific role. Reads the ExperienceLibrary, invokes **`resume-coach`** to assemble an ATS-optimized resume; may invoke **`content-advisor`** (**`resume-summary`** mode) when the user requests **voice-aligned Summary** prose. Saves to the artifact inventory. Also invocable via `/career-navigator:tailor-resume`. |
| **cover-letter** | Skill | Fires after a resume is tailored for a role, or when the user explicitly requests a cover letter for a specific job. Builds **CoverLetterBrief**; invokes **`content-advisor`** for final letter. Saves to artifact inventory. Also invocable via `/career-navigator:cover-letter`. |
| **track-application** | Skill | Fires when the user mentions applying to a job, logging a new application, or updating an existing one (e.g., "I just applied to Acme" or "I got a callback from Google"). Structures conversational input into the tracker database automatically. Also invocable via `/career-navigator:track-application`. |
| **add-source** | Skill | Fires when the user uploads or references a new resume, CV, or portfolio document. Extracts experience units and adds them to the ExperienceLibrary. Also invocable via `/career-navigator:add-source`. |
| **resume-score** | Skill | Fires when the user shares a resume alongside a job description without explicitly requesting tailoring. Scores ATS keyword match, formatting compliance, and narrative strength. Also invocable via `/career-navigator:resume-score`. |
| **list-artifacts** | Skill | Fires when the user asks to see their generated documents, artifact history, or what has been created so far. Also invocable via `/career-navigator:list-artifacts`. |
| **assessment** | Skill | Fires when the user asks for an honest assessment and gap analysis vs. their target role requirements. Uses the `honest-advisor` agent's norm/exception/strategy pattern to surface evidence-based gaps and repositioning options. |
| **market-brief** | Skill | Fires when the user asks for current market conditions. Invokes `market-researcher` to summarize role demand trends, AI/automation displacement signals, and geography-specific competitiveness. Also invocable via `/career-navigator:market-brief`. |
| **suggest-roles** | Skill | Fires when the user asks what adjacent or non-obvious roles they should target. Invokes `honest-advisor` and `market-researcher`, then writes `strategy_signals` to `tracker.json` for job-scout scoring improvements. Also invocable via `/career-navigator:suggest-roles`. |
| **training-roi** | Skill | Fires when the user asks what to learn next. Compares certifications, degrees, bootcamps, and self-study using a cost-benefit-time ROI framework and recommends a primary and fallback path. |
| **networking-strategy** | Skill | Fires when the user wants a networking plan for their search. Invokes **`networking-strategist`** in **networking-strategy** mode (strategy and handoff bullets only; outreach copy via **`content-advisor`**). Also invocable via `/career-navigator:networking-strategy`. |
| **network-map** | Skill | Fires when the user wants a structured map of paths and gaps toward target employers (including dream-job leverage). Produces **`network_map_v1`** JSON for downstream **Phase 2D** graph visualization. Invokes **`networking-strategist`**. Also invocable via `/career-navigator:network-map`. |
| **event-intelligence** | Skill | Fires when the user asks whether to attend specific events, wants ROI or speaker/CFP assessment, or asks about presentation opportunities. Invokes **`networking-strategist`** in **event-intelligence** mode. Also invocable via `/career-navigator:event-intelligence`. |
| **event-radar** | Skill | Fires when the user wants ongoing discovery of events across local, regional, national, and international scope. Invokes **`networking-strategist`** in **event-radar** mode. Also invocable via `/career-navigator:event-radar`. |
| **follow-up** | Skill | Surfaces follow-up queue using **company-windows.json**, builds **FollowUpBrief** entries, invokes **`content-advisor`** for send-ready messages. Also invocable via `/career-navigator:follow-up`. |
| **draft-outreach** | Skill | Invokes **`content-advisor`** for outreach copy (LinkedIn, email, InMail). Also invocable via `/career-navigator:draft-outreach`. |
| **content-suggest** | Skill | Invokes **`content-advisor`** for LinkedIn/professional topic recommendations. Also invocable via `/career-navigator:content-suggest`. |
| **evaluate-post** | Skill | Invokes **`content-advisor`** for audience fit and **cultural / political / reputational risk** vs target company profiles. Also invocable via `/career-navigator:evaluate-post`. |

**Context skills** fire on ambient signals throughout any session:

| Name | Type | Description |
| :---- | :---- | :---- |
| **ats-optimization** | Skill | Fires automatically when a resume is being edited or generated. Checks for ATS-hostile formatting, missing keywords, and structural issues. Suggests fixes inline. |
| **salary-research** | Skill | Fires when compensation is mentioned in any context. Pulls current market data for the role, level, and geography under discussion. |
| **follow-up-timing** | Skill | Fires when an application is viewed in the tracker. Evaluates elapsed time against company-specific norms and flags if a follow-up action is warranted. |
| **cultural-risk-flag** | Skill | Fires when drafting LinkedIn content or outreach messages. Prefer routing evaluation through **`evaluate-post`** / **`content-advisor`** for a single risk rubric; may nudge the user to run **`evaluate-post`** before publishing. |
| **contact-context** | Skill | Fires when a contact at a target company is identified. Searches email and calendar history for prior correspondence and surfaces relevant context for **`content-advisor`** / **`draft-outreach`** (Phase 2A). Requires user approval before use. |

# **6\. Scheduling & recurring runs**

Career Navigator does **not** ship its own cron daemon or hook runtime inside the plugin repo. In **Claude Cowork**, the practical pattern is:

1. **Skills are the payload** — each skill (`daily-schedule`, `session-start`, etc.) defines what to do and where to read data (`{user_dir}/CareerNavigator/...`).
2. **The user schedules execution** — e.g. create a recurring task that runs `/career-navigator:daily-schedule` (or natural language that invokes the `daily-schedule` skill) on a cadence using Cowork’s **`/schedule`** (or equivalent scheduling UI).
3. **Cowork learns the prompt** — after the first successful run, the host refines the scheduled prompt with resolved paths, connectors, and context. That is Cowork’s analogue to a traditional “hook.”

| Name | Type | Description |
| :---- | :---- | :---- |
| **session-start** | Skill | Run when the user opens a session (or on a tight cadence via `/schedule` if they want proactive critical checks). Surfaces **critical-only** alerts (imminent deadlines, same-day follow-ups, urgent interview-day actions). |
| **daily-schedule** | Skill | **Recommended daily** via `/schedule`. Before the digest, checks `{user_dir}` for artifact files and runs `artifact-saved` when present; then pipeline digest, follow-ups, interviews today, market/strategy prompts. |
| **application-update** | Skill | Run **after** `track-application` writes to `tracker.json` (same turn). Classifies refresh priority for outcome-weighted scoring and nudges `pattern-analysis` at milestones. |
| **artifact-saved** | Skill | Run **after** new resumes/cover letters are saved, and/or from `daily-schedule` when PDF/DOCX artifacts exist. Reconciles `artifacts-index.json` with files on disk; prepares analytics handoff metadata when connectors exist. |

## **6.1 Host hooks (`hooks/hooks.json`)**

Claude Cowork supports a plugin-level **`hooks/hooks.json`** (see **cowork-plugin-management**). Available host events include `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `Stop`, `PreToolUse`, `PostToolUse`, `SubagentStop`, `PreCompact`, `Notification`, and others as documented by the host.

Career Navigator ships a minimal configuration:

* **`SessionStart`** — `command` hook runs `cat "${CLAUDE_PLUGIN_ROOT}/hooks/context/session-start.md"` to inject instructions so the model runs the **`session-start`** skill (`skills/session-start/SKILL.md`) for critical-only alerts.

**Prompt-based** hooks (`type: "prompt"`) are supported on a subset of events per host docs; **command-based** hooks work for deterministic context injection (as in the `SessionStart` example above).

This is **orthogonal** to **`/schedule`**: host hooks fire on session/tool lifecycle events; the **`daily-schedule`** skill remains the recommended **daily** payload for recurring tasks the user configures in Cowork.

# **7\. Storage Connectors**

The plugin defines a standard artifact storage interface. Users configure a single active connector in plugin settings. All plugin components call the interface methods without knowing which backend is active.

## **7.1 Interface**

| Name | Type | Description |
| :---- | :---- | :---- |
| **save\_artifact()** | Method | Saves a generated document (resume, cover letter, etc.) with metadata to the configured storage backend. |
| **list\_artifacts()** | Method | Returns a filterable list of all artifacts with metadata: type, date, associated job, outcome. |
| **get\_artifact()** | Method | Retrieves a specific artifact by ID for display or reuse. |
| **save\_event()** | Method | Logs a tracker event (application update, interview outcome, etc.) to the structured event database. |
| **query\_events()** | Method | Returns structured event data for analytics consumption. Supports filtering by date range, role type, company, and outcome. |

## **7.2 Available Connectors**

| Name | Type | Description |
| :---- | :---- | :---- |
| **local** | Connector | Default connector. Stores all data locally in `{user_dir}`. No cloud dependency, no credentials required. All Phase 1 functionality uses this connector. |

Cloud storage connectors (Google Drive, OneDrive, Dropbox) are introduced in Phase 2C. See [Phase 2C](#phase-2c--extended-integrations) for details.

# **8\. Analytics Connectors**

The analytics layer consumes structured event data from the storage connector and produces insights, visualizations, and dashboard views. The plugin ships with a built-in SQLite-based analytics engine for users without a BI tool.

| Name | Type | Description |
| :---- | :---- | :---- |
| **sqlite-builtin** | Connector | Default connector. Local SQLite database with built-in query engine. Powers the /career-navigator:pipeline dashboard and insight engine natively. |
| **power-bi** | Connector | Pushes event data to a Power BI streaming dataset. Enables custom dashboard creation in Power BI Desktop or Service. |
| **qlik** | Connector | Integrates with Qlik Sense or QlikView via the Qlik Engine API. Enables associative analysis across the full application dataset. |
| **d3** | Connector | Exports structured event data in D3-compatible JSON format for custom visualization development. |

# **9\. External Service Integrations (.mcp.json)**

The plugin ships **`.mcp.json`** with **`mcpServers: {}`**. Host-specific MCP setup belongs in the **client** where the user runs Claude. For **`search-jobs`**, users add the **Indeed** connector under **Claude Desktop → Customize → Connectors**, click **Connect**, and complete **browser OAuth** on **secure.indeed.com** (**Grant access to Indeed** in-app; tools **`search_jobs`**, **`get_job_details`**). For **salary-research**, users add the **Apify** **Desktop** connector, paste their **Apify token**, set **Enabled tools** to **`call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search`**, save, enable, and start a new session. This avoids brittle `npx mcp-remote` configs where **`${APIFY_TOKEN}`** in JSON args is passed literally and never expanded.

Run `/career-navigator:launch` for a conversational walkthrough. Each integration is optional; skills degrade when a connector is absent.

| Name | Type | Description |
| :---- | :---- | :---- |
| **Apify** | MCP (Desktop connector) | Powers **`salary-research`** via **cheapget/best-job-search** and related tools. Configured in Claude Desktop connector UI, not committed in `.mcp.json`. |
| **Indeed** | MCP (Claude connector) | Official **`search-jobs`** path: **`search_jobs`**, **`get_job_details`**; OAuth at **secure.indeed.com** after **Connect** in **Customize → Connectors**. Connector endpoint `https://mcp.indeed.com/claude/mcp`. Walkthrough in `/career-navigator:launch` Step 3. |
| **LinkedIn** | MCP | Job posting search, connection graph access, InMail drafting, post publishing and analytics. Required for networking strategy features. |
| **JobSearch** | MCP | Broader job-data integrations (scraping APIs, additional boards). Phase 1A primary live search is **Indeed** MCP above; this row covers alternate/future sources. |
| **Glassdoor** | MCP | Company culture research, interview experience data, salary benchmarks, and recruiter process timelines. |
| **CareerOneStop** | MCP | U.S. Department of Labor API. Free. Provides labor market data, salary ranges, occupation outlook, and American Job Center locations. |
| **IllinoisJobLink** | MCP | Illinois-specific job board. State employment resources and local posting discovery. |
| **Gmail / Outlook** | MCP | Contact history search for networking context. OAuth-based. Requires explicit user opt-in. Scoped to search only — no send access without separate permission. |
| **Google Calendar / Outlook Calendar** | MCP | Interview scheduling awareness, contact meeting history, and daily briefing triggers. OAuth-based. Read-only by default. |
| **Greenhouse / Workday / Lever** | MCP | ATS status tracking for applications submitted through these platforms. Read-only access to application status. |
| **Whisper (OpenAI)** | MCP | Audio transcription for interview capture feature. Phase 1B. Local processing option available for privacy-sensitive users. |
| **Meetup / Eventbrite / Luma** | MCP | Event discovery for networking radar. Searches for relevant professional events by location, industry, and role type. |

# **10\. Core Data Model**

## **10.0 User Profile**

Stored at `{user_dir}/CareerNavigator/profile.md`. Created by `/career-navigator:launch` — scans documents in `{user_dir}` and builds the profile from existing resumes and cover letters; falls back to conversational Q&A if no documents are found. Read automatically by all agents at the start of every operation — agents must not ask for information that is already in the profile.

* **identity** — name, location, contact info, professional summary, core differentiator
* **target\_roles** — preferred titles, minimum seniority level
* **target\_companies** — primary, secondary, and tertiary targets; industries to prioritize and avoid
* **compensation\_floor** — minimum total comp (base + bonus + equity annualized); expected ranges by company type
* **location** — geographic preferences, relocation openness, remote/hybrid preference
* **key\_skills** — prioritized skill list for ATS matching and ExperienceLibrary tagging
* **differentiators** — named, high-value elements that must appear in every tailored resume
* **search\_notes** — standing instructions for agents: preferred channels, company-specific notes, anything static that should inform every search and application

**Optional companion file — `{user_dir}/CareerNavigator/voice-profile.md`**

**`/career-navigator:launch`** seeds or refreshes this file via **launch voice harvest**: scans **PDF/DOCX/MD/TXT** résumés, CVs, and cover letters (tiered vs plugin-generated artifacts), prompts for **LinkedIn** (paste, drop files, or skip), may record **`## Voice by context`** when tones diverge, and **`## Voice quality flags (launch)`** for pragmatic risks (tone, “AI slop” tells, snark, etc.). **`content-advisor`** then maintains user-pasted **`## User writing samples`** blocks, **`voice_profile_v1`**, and respects multi-context + flags when drafting.

## **10.1 ExperienceLibrary**

The ExperienceLibrary is not a collection of discrete resumes — it is a structured pool of experience units that can be recombined. Each unit has metadata indicating source document, role type relevance, industry tags, and performance history.

* source\_documents\[ \] — original uploaded files (resumes, CVs, portfolios)

* experience\_units\[ \] — individual bullets, accomplishments, roles extracted from source documents

* skill\_tags\[ \] — normalized skill taxonomy mapped across all units

* performance\_weights{ } — outcome-adjusted weights per unit, updated by insight engine

## **10.2 Application Record**

| Name | Type | Description |
| :---- | :---- | :---- |
| **application\_id** | UUID | Unique identifier |
| **company** | String | Company name |
| **role\_title** | String | Job title applied for |
| **jd\_text** | Text | Full job description text |
| **source\_board** | String | Where the posting was found |
| **date\_applied** | Date | Application submission date |
| **status** | Enum | Applied / Phone Screen / HM Interview / Panel / Final / Offer / Rejected / Withdrawn / Ghosted |
| **stage\_history\[ \]** | Array | Timestamped log of every status change |
| **artifacts\_used\[ \]** | Array | IDs of resume and cover letter artifacts submitted |
| **contacts\[ \]** | Array | Known contacts at the company with relationship strength |
| **notes** | Text | Freeform notes from conversational input or interview debrief |
| **outcome** | Enum | Pending / Hired / Rejected / Withdrew |
| **outcome\_notes** | Text | Reason for outcome if known |

## **10.3 Artifact Record**

| Name | Type | Description |
| :---- | :---- | :---- |
| **artifact\_id** | UUID | Unique identifier |
| **type** | Enum | Resume / Cover Letter / LinkedIn post draft (`linkedin_post`) / Portfolio / Other |
| **application\_id** | UUID | Associated application (nullable for templates) |
| **source\_units\[ \]** | Array | Experience unit IDs included in this artifact |
| **jd\_keywords\[ \]** | Array | Keywords targeted in this artifact |
| **ats\_score** | Float | ATS compatibility score at time of generation |
| **created\_at** | Timestamp | Creation date |
| **storage\_path** | String | Path or URL in configured storage connector |

# **11\. The Intelligence Feedback Loop**

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

# **12\. Daily Rhythm & Scheduling**

Scheduling split (single source of truth):
- **`session-start` skill** = critical-only, time-sensitive surfacing (typically when the user opens a session; optionally on a short cadence via `/schedule` if they want).
- **`daily-schedule` skill** = routine operating brief — **intended to be run daily** via Claude Cowork **`/schedule`** (user configures time/cadence).

The plugin documents **recommended cadences** inside skills; **execution** is owned by Cowork’s scheduler.

## **12.1 Recommended cadences (Cowork `/schedule`)**

| Name | Suggested cadence | How to run |
| :---- | :---- | :---- |
| **Daily operating brief** | Daily (user picks time) | Schedule a task whose payload invokes the `daily-schedule` skill (e.g. `/career-navigator:daily-schedule` or natural language equivalent). |
| **Follow-up / pipeline hygiene** | Daily (often same task as above) | Covered by `daily-schedule` + conversational `follow-up` as needed. |
| **Market intelligence** | Weekly | Schedule `/career-navigator:market-brief` (or invoke `market-brief` skill). |
| **Outcome pattern refresh** | Weekly or after milestone outcomes | User runs `/career-navigator:pattern-analysis` or schedules it after major tracker updates. |

## **12.2 Time-sensitive vs routine surfacing**

| Situation | Where it lives |
| :---- | :---- |
| Imminent deadlines, same-day follow-ups, urgent interview-day actions | `session-start` skill (critical-only). |
| Pipeline digest, artifact counts, weekly-style prompts | `daily-schedule` skill (scheduled). |
| Post-save inventory drift (PDF/DOCX on disk vs index) | `artifact-saved` skill (from `daily-schedule` when files exist, or after saves). |

Future phases may add richer “event radar” and offer/interview prompts; those remain **skill payloads** scheduled or invoked by the user in Cowork unless the host adds first-class hooks later.

# **13\. Interview Capture (Phase 2B)**

Interview capture is an opt-in feature that uses local audio recording and Whisper transcription to automatically log interview content. It is bundled with the full interview preparation system in Phase 2B, shipping together so the prep and capture experiences are developed and tested as a unified layer. The post-interview Q\&A debrief (`/career-navigator:interview-debrief`) is the primary debrief path for users who do not use audio capture.

## **13.1 Privacy Considerations (To Be Discussed)**

The following privacy topics require explicit user guidance and consent design before implementation:

* Consent from all parties — many jurisdictions require all-party consent for recording. The system must warn users clearly.

* Storage of audio and transcripts — where they are stored, for how long, and who can access them

* Local vs. cloud processing — local Whisper processing vs. API-based transcription and the privacy tradeoffs of each

* Employer policies — some employers prohibit recording interviews. The system should surface this risk.

* Data retention and deletion — user must be able to purge all audio and transcript data on demand

## **13.2 Fallback: Post-Interview Q\&A Flow**

For users who do not use audio capture, the interview debrief command provides a conversational Q\&A that captures equivalent structured data:

* How did the interview go overall?

* What stage was it? Who did you meet with?

* What topics came up that you weren't expecting?

* Any red flags or particularly positive signals?

* What follow-up actions did you commit to?

* Any intel about the role, team, or company worth noting?

Claude structures the responses into the application record automatically, inferring sentiment and extracting action items.

# **14\. The Honest Advisor Design Philosophy**

The honest-advisor agent operates by a specific three-step pattern for any assessment involving barriers or challenges:

* State the general norm — what typically happens in this situation across the market

* Research the exceptions — specific geographies, companies, industries, or contexts where the norm breaks down, and why

* Provide actionable strategy — concrete steps the user can take to position themselves in the exception category rather than the norm

The advisor never tells the user what to believe or what decisions to make. It provides honest information about how the world works, where it works differently, and what options exist. The user decides.

For factors the user cannot change (age, career gaps, unconventional backgrounds), the advisor acknowledges the reality of bias honestly while focusing energy on strategies and contexts where those factors matter less or work as advantages.

The advisor is calibrated to be less confrontational when the user has an interview imminent, a rejection is recent, or other stress signals are present. Honest delivery is adjusted for timing without compromising accuracy.

# **15\. Phased Delivery Plan**

## **Phase 1 — Core Platform**

Phase status:
- Phase 1A: Completed
- Phase 1B: Completed
- Phase 1C: Completed
- Phase 1D: Completed
- Phase 1E: Completed

Phase 1 builds the complete local-first job search intelligence platform. The foundation in Phase 1A establishes the plugin scaffold, setup flow, and live job search. Phase 1B constructs the full skill layer — workflow skills that activate from conversational context, a closed feedback loop connecting application outcomes to future recommendations, and a pipeline dashboard. Phase 1C adds candid role assessment and skills gap analysis. Phase 1D extends the job-scout agent with outcome-weighted scoring and proactive opportunity discovery. Phase 1E completes the platform with professional presence tools: networking strategy, event radar, and LinkedIn content advising. At the end of Phase 1, all core job search workflows are intelligent, locally self-contained, and require no external service dependencies.

### **Phase 1A — Core platform: plugin scaffold, setup, session start, and live job search**

Status: Completed

* Plugin scaffold: manifest, directory structure

* **`launch` skill** and conversational configuration wizard — scans the job search folder, auto-imports existing resumes into ExperienceLibrary, builds user profile from available documents; falls back to conversational Q&A if no source documents found; initializes all data schemas (ExperienceLibrary, tracker, artifacts index). Slash command: **`/career-navigator:launch`**.

* `search-jobs` skill — live job search via Indeed connector; assisted-manual fallback

* `session-start` skill — critical-only alerts when the user begins a session (or on a user-scheduled cadence via Cowork `/schedule`); onboarding on first run

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

* D3 pipeline dashboard with timeline view and benchmark comparisons _(**forecast** + **voice cadence** overlays are **Phase 2D — Dashboard & visualization enhancements** in §15—not part of Phase 1B scope)_

* `/career-navigator:pipeline`, `/career-navigator:follow-up`

### **Phase 1C — Advisor layer: honest role assessment, skills gap analysis, and training ROI**

Status: Completed

* **Agents introduced:** 

    * `honest-advisor` candid role competitiveness assessment, norm/exception/strategy pattern

    * `market-researcher` role demand trends, AI/automation displacement, geographic signals

        triggered through `/career-navigator:market-brief` skill

* Skills assessment and gap analysis against target role requirements

* Training recommendation engine with cost-benefit-time ROI analysis (certifications, degrees, bootcamps, self-study)

* `/career-navigator:suggest-roles`, job scout scoring improvements driven by outcome data

    * Note: skills assessment becomes significantly richer once Phase 2B mock interview performance data feeds back into the profile

### **Phase 1D — Proactive discovery: outcome-weighted job scoring and market trend monitoring**

Status: Completed

* Expanded/tuned `job-scout` weighting and ranking behavior as outcome history matures

* Non-obvious role suggestions based on transferable skills

* Market trend monitoring with proactive notifications for significant shifts

* Role demand forecasting incorporating AI/automation displacement signals

### **Phase 1E — Professional presence: networking strategy, event radar, and LinkedIn content advisor**

Status: Completed

**Scope (what 1E is responsible for):** conversational **skills + agents + slash commands** for networking strategy, network mapping (**`network_map_v1`** / optional `network-map.md` persistence), event intelligence and multi-scope **event-radar** (including optional **`event_radar_v1`** / `event-radar.md`), and all **user-facing copy** via **`content-advisor`** (outreach, cover letters, follow-ups, resume Summary polish, topic ideas, post drafts, risk evaluation). **`/career-navigator:launch`** seeds **`voice-profile.md`** from on-disk résumés/CVs/covers and prompts for LinkedIn samples; **`content-advisor`** maintains samples, multi-context tone notes, and quality flags. Full **post drafts** for review are **saved** under **`{user_dir}/LinkedIn Posts/`** and indexed as **`linkedin_post`** in **`artifacts-index.json`**.

**1E deliverables (target checklist):**

* **Agents:** `networking-strategist`; `content-advisor` (as scoped in §4).

* **Skills:** `networking-strategy`, `network-map`, `event-intelligence`, `event-radar`, `draft-outreach`, `content-suggest`, `evaluate-post`; `cover-letter` and `follow-up` orchestrate **`content-advisor`** via **CoverLetterBrief** / **FollowUpBrief**.

* Event radar with **local, regional, national, and international** discovery where appropriate (within available tools).

* Presentation opportunity flagging; CFP / visibility assessment in **`event-intelligence`**.

* LinkedIn topic recommendations; full **post drafts** persisted to disk; **`evaluate-post`** (cultural/political/reputational risk vs target profiles).

* **`voice-profile.md`** / **`voice_profile_v1`** for tone matching (launch harvest + user samples).

* Commands: `/career-navigator:networking-strategy`, `/career-navigator:network-map`, `/career-navigator:event-intelligence`, `/career-navigator:event-radar`, `/career-navigator:draft-outreach`, `/career-navigator:content-suggest`, `/career-navigator:evaluate-post`.

## **Phase 2 — Integrations**

Phase 2 extends Career Navigator beyond the local filesystem by connecting it to the external services that complete the full job search experience. Phase 2A unlocks the email and calendar history that powers warm networking intelligence — surfacing prior contact relationships before outreach is drafted. Phase 2B brings the complete interview layer: a full mock interview system with audio capture and automated debrief logging, combined into a single release to avoid shipping the prep experience without the capture infrastructure. Phase 2C adds cloud storage connectors and ATS read-access, making the platform portable and enabling users to track applications submitted through employer systems. **Event discovery** (connector-backed feeds for **`event-radar`**) is scoped here as a **placeholder**—see **Phase 2C — Event discovery** below. Phase 2D closes the analytics loop with BI connectors, LinkedIn automation, and **dashboard/visualization upgrades** (pipeline forecast, voice cadence, network graph) deferred from Phase 1E. Each sub-phase is independently deployable — users can adopt what's relevant to their workflow without requiring all of Phase 2 to be complete.

### **Phase 2A — Email & Calendar Integration**

* Gmail and Outlook OAuth connectors (read-only scoped)

* Google Calendar and Outlook Calendar read-only access

* Contact correspondence history search for networking context

* Contact context skill: surfaces prior email/meeting history before outreach drafting

* Outreach drafting enriched with prior communication history

* Meeting history awareness for warm networking identification

### **Phase 2B — Interview intelligence: mock interview system, morning brief, audio capture, and post-interview debrief**

* **Agents introduced:** `interview-coach` (mock interviews across all stages and vibes, adaptive difficulty, current events integration), `interview-capture` (audio transcription via Whisper, structured tracker population — opt-in only)

* Mock interview system: guided, random, and adaptive modes

* All stages: recruiter screen, hiring manager, technical, panel, executive, final

* Full vibe spectrum: supportive, neutral, challenging, antagonistic, bored (calibrated — not demoralizing)

* Current events integration woven into mock interview questions

* Morning brief with company news, interviewer research, and talking points

* Post-interview Q\&A debrief flow (`/career-navigator:interview-debrief`) — structured conversational capture; serves as the primary debrief path for users who do not use audio capture

* `/career-navigator:prep-interview`, `/career-navigator:mock-interview`, `/career-navigator:morning-brief`

* Mock interview performance feeds back into Phase 1C skills profile

* Full privacy risk assessment and consent model design for audio capture

* Cross-jurisdiction recording consent guidance

* Local Whisper processing option for privacy-sensitive users

* Employer policy warnings surfaced before recording

* Audio and transcript storage with user-controlled retention and deletion

* Auto-population of tracker from interview transcription

### **Phase 2C — Extended Integrations**

* Google Drive storage connector (OAuth)

* OneDrive storage connector (OAuth)

* Dropbox storage connector (OAuth)

* IllinoisJobLink job board connector

* ATS read-only connectors for Greenhouse, Workday, and Lever

**Event discovery (placeholder — Phase 2C)**

* **Status:** _Placeholder — not implemented._ Phase 1E **`event-radar`** / **`event-intelligence`** may use **web-assisted** discovery until this ships.

* **Goal:** First-class **event feeds** (structured listings, stable IDs where possible) so **`event-radar`** and **`networking-strategist`** spend less time on brittle scraping and **`event_radar_v1`** / `event-radar.md` can refresh from connector output.

* **Candidate integrations:** Meetup, Eventbrite, Luma, and similar (see §9 **External Service Integrations**). Exact vendor order, OAuth vs API keys, host packaging (e.g. Claude Connectors), and **MCP tool names** are **TBD**.

* **Open design (TBD):** deduplication vs user-edited **`{user_dir}/CareerNavigator/event-radar.md`**; geographic / paid-event coverage; rate limits and cost; fallback when a connector is off (keep web-assisted path).

### **Phase 2D — Advanced Analytics, LinkedIn Automation & Dashboard Enhancements**

* Power BI streaming dataset connector

* Qlik Engine API connector

* D3 data export connector for custom visualization

* LinkedIn automation for job search and connection graph access (approach TBD)

**Dashboard & visualization enhancements** _(deferred from Phase 1E; depends on stable interchange from 1E outputs):_

* **Pipeline timeline — forecast overlay:** extend **`/career-navigator:pipeline`** (D3) so the **timeline** shows a forward-looking **forecast** from **`networking-strategist`** outputs—planned or recommended relationship moves, high-ROI events, visibility milestones—alongside **historical** application stages. Requires persisting or deriving structured data from `networking-strategy`, `event-radar`, **`network_map_v1`**, **`event_radar_v1`**, and related artifacts; refresh cadence and schema TBD.

* **Pipeline timeline — voice cadence:** surface **`voice_profile_v1`** / **`voice-profile.md`** metadata (e.g. last harvest, sample dates, tone summaries) on or beside the timeline so users see how **public-facing cadence** tracks with applications and networking.

* **Network map graph UI:** interactive graph (or export path) consuming persisted **`network_map_v1`**—beyond narrative + JSON in chat / `network-map.md`.

## **Phase 3 — Platform Expansion**

* Hosted API proxy with per-user key management and usage tracking — enables monetization and removes the need for each user to obtain their own JobSearch key

* Multi-user and team mode for staffing agencies and career coaches

* Plugin marketplace publication

* Mobile companion app for on-the-go tracker updates and notifications

* Salary negotiation and offer evaluation module

* Skills gap training integrations with Coursera and LinkedIn Learning

## **Phase 4 — Enterprise & Ecosystem**

* White-label version for career coaching practices and staffing agencies

* API for third-party integrations

* Anonymized aggregate outcome data for benchmarking improvements

* Government employment program integrations and American Job Center partnerships

* Veteran and disability-specific pathway modules

# **16\. Open Questions & Deferred Decisions**

| Name | Type | Description |
| :---- | :---- | :---- |
| **Interview Audio Privacy** | Privacy & Legal | Full privacy risk assessment needed before Phase 2B implementation. Consent model, storage location, retention policy, employer policy warnings, and cross-jurisdiction recording consent to be designed. |
| **LinkedIn API Access** | Technical | LinkedIn's official API is highly restricted. Phase 1 uses assisted-manual workflow. Phase 2D will assess automation options including third-party providers like Proxycurl. |
| **Antagonistic Interview Mode** | UX | Exact calibration of antagonistic vibe — specifically what constitutes appropriately challenging vs. demoralizing. Needs user testing before Phase 2B ships. System must back off when interview is imminent. |
| **Political/Cultural Content Guidance** | Ethics | System should inform not prescribe. Exact framing of cultural risk flags to be designed to avoid appearing to suppress legitimate expression. |
| **Data Retention Policy** | Privacy | How long application data, artifacts, and event logs are retained. User-controlled deletion scope to be specified. |
| **Salary Negotiation** | Scope | Offer evaluation and negotiation guidance mentioned briefly — full scope not yet specified. Candidate for Phase 3\. |
| **Training ROI Data Sources** | Technical | Sources for certification value, bootcamp outcomes, and degree ROI data need to be identified and validated for Phase 1C training recommendation engine. |
| **Pipeline timeline + strategist forecast** | UX / Data | **Routed to Phase 2D** — see **§15 Phase 2D — Dashboard & visualization enhancements**. Open details: interchange format, refresh cadence, persistence of strategist outputs. |
| **Timeline + voice cadence** | UX / Data | **Routed to Phase 2D** — same subsection. Open details: which metadata fields to show and how they align with application dates. |
| **Network graph visualization** | UX / Data | **Routed to Phase 2D** — interactive (or export) graph from **`network_map_v1`**; was previously “future phase” under 1E/network-map only. |

# **Appendix: Command Quick Reference**

| Command | Purpose |
| :---- | :---- |
| **/career-navigator:launch** | Launch job search workspace: configure folder, build ExperienceLibrary and profile, set up job search connectors (run first) |
| **/career-navigator:tailor-resume** | Assemble resume via **`resume-coach`**; optional **`content-advisor`** Summary polish |
| **/career-navigator:cover-letter** | **CoverLetterBrief** + **`content-advisor`** final prose |
| **/career-navigator:resume-score** | Score resume against a job description |
| **/career-navigator:add-source** | Add source document to ExperienceLibrary |
| **/career-navigator:list-artifacts** | List all generated artifacts |
| **/career-navigator:search-jobs** | Search and rank job opportunities |
| **/career-navigator:track-application** | Log or update an application |
| **/career-navigator:pipeline** | View full application dashboard (timeline; **Phase 2D:** forecast + voice cadence overlays) |
| **/career-navigator:follow-up** | **FollowUpBrief** + **`content-advisor`** messages |
| **/career-navigator:market-brief** | Current market intelligence report |
| **/career-navigator:suggest-roles** | Discover non-obvious role opportunities |
| **/career-navigator:networking-strategy** | Networking plan (strategy; outreach via **content-advisor**) |
| **/career-navigator:network-map** | Network paths/gaps + **`network_map_v1`** (Phase 2D: graph UI) |
| **/career-navigator:event-intelligence** | Event ROI and presentation opportunity assessment |
| **/career-navigator:event-radar** | Multi-scope event discovery |
| **/career-navigator:prep-interview** | Full interview preparation session |
| **/career-navigator:mock-interview** | Mock interview (guided/random/adaptive) |
| **/career-navigator:interview-debrief** | Post-interview Q\&A capture |
| **/career-navigator:morning-brief** | Day-of interview briefing |
| **/career-navigator:draft-outreach** | Draft outreach (**`content-advisor`**) |
| **/career-navigator:content-suggest** | LinkedIn topic ideas (**`content-advisor`**) |
| **/career-navigator:evaluate-post** | Post risk review — audience + cultural/political (**`content-advisor`**) |

