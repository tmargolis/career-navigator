**CAREER NAVIGATOR**

Claude Cowork Plugin — Full Product Specification

Version 0.2 — February 2026

An AI-powered job search companion that combines the capabilities of

recruiters, career coaches, reverse recruiters, and market analysts into a single intelligent platform.

# **Table of Contents**

[**Table of Contents	2**](#table-of-contents)

[**1\. Overview	3**](#1-overview)

[1.1 Design Principles	3](#11-design-principles)

[1.2 Plugin Architecture	3](#12-plugin-architecture)

[**2\. Plugin File Structure	4**](#2-plugin-file-structure)

[**3\. Slash Commands	5**](#3-slash-commands)

[3.1 Resume & Cover Letter Commands	5](#31-resume--cover-letter-commands)

[3.2 Job Search & Tracking Commands	5](#32-job-search--tracking-commands)

[3.3 Interview Prep Commands	6](#33-interview-prep-commands)

[3.4 Networking Commands	6](#34-networking-commands)

[**4\. Agents	7**](#4-agents)

[**5\. Skills	9**](#5-skills)

[**6\. Hooks	10**](#6-hooks)

[**7\. Storage Connectors	11**](#7-storage-connectors)

[7.1 Interface	11](#71-interface)

[7.2 Available Connectors	11](#72-available-connectors)

[**8\. Analytics Connectors	12**](#8-analytics-connectors)

[**9\. External Service Integrations (.mcp.json)	13**](#9-external-service-integrations-mcpjson)

[**10\. Core Data Model	14**](#10-core-data-model)

[10.1 Resume Corpus	14](#101-resume-corpus)

[10.2 Application Record	14](#102-application-record)

[10.3 Artifact Record	14](#103-artifact-record)

[**11\. The Intelligence Feedback Loop	16**](#11-the-intelligence-feedback-loop)

[**12\. Daily Rhythm & Scheduling	17**](#12-daily-rhythm--scheduling)

[12.1 Scheduled Events (node-cron)	17](#121-scheduled-events-node-cron)

[12.2 Event-Driven Notifications (node-notifier)	17](#122-event-driven-notifications-node-notifier)

[**13\. Interview Capture (Phase 2B)	18**](#phase-2b--interview-audio-capture)

[13.1 Privacy Considerations (To Be Discussed)	18](#131-privacy-considerations-to-be-discussed)

[13.2 Fallback: Post-Interview Q\&A Flow	18](#132-fallback-post-interview-qa-flow)

[**14\. The Honest Advisor Design Philosophy	19**](#14-the-honest-advisor-design-philosophy)

[**15\. Phased Delivery Plan	20**](#15-phased-delivery-plan)

[Phase 1 — Core Platform	20](#phase-1--core-platform)

[&nbsp;&nbsp;&nbsp;&nbsp;Phase 1A — Core platform: plugin scaffold, setup, session start, and live job search	20](#phase-1a--core-platform-plugin-scaffold-setup-session-start-and-live-job-search)

[&nbsp;&nbsp;&nbsp;&nbsp;Phase 1B — Skill layer and intelligence: workflow skills, application tracker, ATS scoring, and insight engine	20](#phase-1b--skill-layer-and-intelligence-workflow-skills-application-tracker-ats-scoring-and-insight-engine)

[&nbsp;&nbsp;&nbsp;&nbsp;Phase 1C — Advisor layer: honest role assessment, skills gap analysis, and training ROI	20](#phase-1c--advisor-layer-honest-role-assessment-skills-gap-analysis-and-training-roi)

[&nbsp;&nbsp;&nbsp;&nbsp;Phase 1D — Proactive discovery: outcome-weighted job scoring and market trend monitoring	20](#phase-1d--proactive-discovery-outcome-weighted-job-scoring-and-market-trend-monitoring)

[&nbsp;&nbsp;&nbsp;&nbsp;Phase 1E — Professional presence: networking strategy, event radar, and LinkedIn content advisor	21](#phase-1e--professional-presence-networking-strategy-event-radar-and-linkedin-content-advisor)

[Phase 2 — Integrations	21](#phase-2--integrations)

[&nbsp;&nbsp;&nbsp;&nbsp;Phase 2A — Email & Calendar Integration	21](#phase-2a--email--calendar-integration)

[&nbsp;&nbsp;&nbsp;&nbsp;Phase 2B — Interview intelligence: mock interview system, morning brief, audio capture, and post-interview debrief	22](#phase-2b--interview-intelligence-mock-interview-system-morning-brief-audio-capture-and-post-interview-debrief)

[&nbsp;&nbsp;&nbsp;&nbsp;Phase 2C — Extended Integrations	22](#phase-2c--extended-integrations)

[&nbsp;&nbsp;&nbsp;&nbsp;Phase 2D — Advanced Analytics & LinkedIn Automation	22](#phase-2d--advanced-analytics--linkedin-automation)

[Phase 3 — Platform Expansion	22](#phase-3--platform-expansion)

[Phase 4 — Enterprise & Ecosystem	22](#phase-4--enterprise--ecosystem)

[**16\. Open Questions & Deferred Decisions	24**](#16-open-questions--deferred-decisions)

[**Appendix: Command Quick Reference	25**](#appendix-command-quick-reference)

# **1\. Overview**

Career Navigator is a Claude Cowork plugin that provides end-to-end job search intelligence — from discovering roles and tailoring application materials, through interview preparation and networking strategy, to tracking outcomes and learning from results. It is designed to serve any job seeker regardless of experience level, target industry, or geographic location.

The plugin is architected around a feedback loop: every action taken and outcome observed feeds back into the system to make future recommendations smarter. Over time, Career Navigator learns what works for the individual user and adjusts its guidance accordingly.

## **1.1 Design Principles**

* Honest over encouraging — the system provides candid assessments, not false reassurance

* Intelligent over mechanical — outputs adapt based on outcomes, not just inputs

* Connector-based — storage, analytics, and external services are pluggable adapters

* Privacy-first — sensitive features like audio capture require explicit opt-in

* Cross-platform — all scheduling, notifications, and services work on macOS, Windows, and Linux

* Empathetic — the system understands job searching is stressful and calibrates tone accordingly

## **1.2 Plugin Architecture**

| Plugin Name | career-navigator |
| :---- | :---- |
| **Version** | 1.1.0 |
| **Platform** | Claude Cowork (macOS / Windows / Linux) (also compatible with Claude Code) |
| **Architecture** | Skill-first — behavioral intelligence lives in skills with conversational triggers; commands are explicit invocation aliases for key workflows |
| **Scheduling** | node-cron (cross-platform) |
| **Notifications** | node-notifier (cross-platform native notifications) |
| **Storage Layer (Phase 1\)** | Local filesystem — `{user_dir}` (cloud connectors in Phase 2C) |
| **Analytics Layer (Phase 1\)** | SQLite \+ D3 visualization (additional connectors in Phase 2D) |
| **AI Services** | Claude API (via MCP), Whisper (audio transcription — Phase 2B) |
| **Job Search (Phase 1\)** | Indeed connector (built-in, no token required) \+ assisted-manual fallback |

# **2\. Plugin File Structure**

**career-navigator/**

**├── .claude-plugin/**

**│   └── plugin.json**

**├── commands/**

**├── agents/**

**├── skills/**

**├── hooks/**

**├── .mcp.json**

**├── services/**

**│   ├── scheduler/**

**│   ├── connectors/**

**│   └── notifications/**

**└── README.md**

# **3\. Slash Commands**

All commands are namespaced under career-navigator: and accessible via Claude Cowork's slash command interface (and Claude Code). Commands can also be triggered conversationally — the plugin recognizes natural language prompts that match command intent and invokes the appropriate command automatically.

## **3.0 Setup & Configuration**

| Name | Type | Description |
| :---- | :---- | :---- |
| **/career-navigator:setup** | Command | Conversational setup wizard. Reads existing documents in the job search folder, builds the user profile and experience corpus, and configures JobSearch for live job search. Validates all inputs before saving, writes config automatically. Re-runnable to update keys or reconfigure. |

## **3.1 Resume & Cover Letter Commands**

| Name | Type | Description |
| :---- | :---- | :---- |
| **/career-navigator:tailor-resume** | Command | Takes one or more source documents from the corpus and a job description, assembles and rewrites the best possible resume for that specific role, scores it for ATS compatibility, and saves it to the artifact inventory. |
| **/career-navigator:cover-letter** | Command | Generates a targeted cover letter for a specific role, drawing on the tailored resume, company research, and any known contact context. Saves to artifact inventory. |
| **/career-navigator:resume-score** | Command | Scores an existing resume or cover letter against a job description for ATS keyword match, formatting compliance, and narrative strength. |
| **/career-navigator:add-source** | Command | Adds a new source document (resume, CV, portfolio) to the resume corpus for use in future tailoring. |
| **/career-navigator:list-artifacts** | Command | Lists all generated artifacts in the inventory with metadata: date created, job applied for, outcome if known. |

## **3.2 Job Search & Tracking Commands**

| Name | Type | Description |
| :---- | :---- | :---- |
| **/career-navigator:search-jobs** | Command | Searches configured job boards and returns ranked results. Ranking incorporates skill match, outcome history, and market intelligence. Supports filters for role, location, company size, industry, and salary range. |
| **/career-navigator:track-application** | Command | Logs a new application or updates an existing one. Accepts conversational input and structures it automatically into the tracker database. |
| **/career-navigator:pipeline** | Command | Displays the full application pipeline dashboard with timeline view, benchmark comparisons, and action items flagged by stage age. |
| **/career-navigator:follow-up** | Command | Generates a contextual follow-up message for a specific application based on elapsed time, last communication, and company norms. |
| **/career-navigator:market-brief** | Command | Generates a current market intelligence report for the user's target roles and industries, including trend data, competition levels, and AI/automation impact assessment. |
| **/career-navigator:suggest-roles** | Command | Analyzes the user's full experience corpus and suggests non-obvious role types their skills could be applied to, with rationale for each suggestion. |

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
| **/career-navigator:network-map** | Command | Visualizes the user's network relative to target companies, showing direct connections, second-degree paths, and identified gaps. |
| **/career-navigator:draft-outreach** | Command | Drafts a LinkedIn message or email to a specific contact. Searches email and calendar history for prior context and incorporates it with user approval. |
| **/career-navigator:content-suggest** | Command | Suggests LinkedIn post topics based on current industry trends, the user's target roles, and recent activity in their field. |
| **/career-navigator:evaluate-post** | Command | Evaluates a draft LinkedIn post for audience fit, likely algorithmic performance, and cultural alignment with target companies. |
| **/career-navigator:event-radar** | Command | Searches for relevant local, national, and international networking events and conferences. Returns ranked recommendations with ROI assessment and presentation opportunity flags. |

# **4\. Agents**

Agents are specialized Claude instances with focused roles. They can be invoked directly or orchestrated by commands. Multiple agents may collaborate on complex tasks.

| Name | Phase | Description |
| :---- | :---- | :---- |
| **resume-coach** | 1B | Analyzes the resume corpus, identifies gaps and strengths, optimizes for ATS compatibility, and provides narrative coaching. Invoked by the `tailor-resume` and `resume-score` skills. |
| **insight-engine** | 1B | Analyzes cross-application outcome data to identify patterns: which resume variants, communication styles, and role types are performing best. Updates corpus performance weights and feeds recommendations back to `job-scout` and `resume-coach`. |
| **honest-advisor** | 1C | Provides candid assessments of the user's competitiveness for specific roles, potential recruiter concerns, and strategies for overcoming barriers. Researches company/industry-specific deviations from general norms. Empathetic but unsparing. |
| **market-researcher** | 1C | Monitors macro hiring trends, role-specific demand signals, AI/automation displacement risks, geographic demand patterns, and sector-specific cycles. Feeds the `market-brief` command and the `job-scout` agent. |
| **job-scout** | 1D | Searches and ranks job opportunities across all configured job boards. Incorporates outcome history and market intelligence into scoring. Ranking improves over time as the user logs outcomes. Proactively surfaces high-match opportunities. |
| **interview-coach** | 2B | Conducts mock interviews across all stages and vibes (supportive, neutral, challenging, antagonistic, bored). Adapts difficulty based on user performance in adaptive mode. Incorporates current events and company-specific research into questions. |
| **networking-strategist** | 1F | Analyzes the user's network relative to their goals, identifies gaps and paths, drafts outreach, and evaluates content strategy. Searches email and calendar history for contact context with user approval. |
| **content-advisor** | 1F | Evaluates LinkedIn content for audience fit, algorithmic performance, and cultural alignment with target companies. Flags political/cultural risks relative to specific employer profiles. Recommends topics proactively. |
| **event-intelligence** | 1F | Continuously discovers and evaluates networking events globally. Assesses ROI using attendee quality, user target overlap, and historical conversion data. Flags high-value presentation opportunities. |
| **interview-capture** | 2B | Processes audio transcription from interviews (via Whisper), extracts structured data, and auto-populates the tracker. Only active with explicit user opt-in. Full privacy framework required before activation. |

# **5\. Skills**

Skills are auto-triggered capabilities that Claude activates when relevant context is detected, without requiring an explicit command invocation. This is the primary interaction model for Career Navigator — commands serve as explicit aliases for users who prefer them, but skills carry the behavioral intelligence.

**Workflow skills** handle the core job search operations and fire from conversational intent:

| Name | Type | Description |
| :---- | :---- | :---- |
| **tailor-resume** | Skill | Fires when the user shares or pastes a job description, or expresses intent to apply to a specific role. Reads the corpus, assembles an optimized resume for the target role, scores it for ATS compatibility, and saves it to the artifact inventory. Also invocable via `/career-navigator:tailor-resume`. |
| **cover-letter** | Skill | Fires after a resume is tailored for a role, or when the user explicitly requests a cover letter for a specific job. Draws on the tailored resume, company research, and any known contact context. Saves to artifact inventory. Also invocable via `/career-navigator:cover-letter`. |
| **track-application** | Skill | Fires when the user mentions applying to a job, logging a new application, or updating an existing one (e.g., "I just applied to Acme" or "I got a callback from Google"). Structures conversational input into the tracker database automatically. Also invocable via `/career-navigator:track-application`. |
| **add-source** | Skill | Fires when the user uploads or references a new resume, CV, or portfolio document. Extracts experience units and adds them to the corpus. Also invocable via `/career-navigator:add-source`. |
| **resume-score** | Skill | Fires when the user shares a resume alongside a job description without explicitly requesting tailoring. Scores ATS keyword match, formatting compliance, and narrative strength. Also invocable via `/career-navigator:resume-score`. |
| **list-artifacts** | Skill | Fires when the user asks to see their generated documents, artifact history, or what has been created so far. Also invocable via `/career-navigator:list-artifacts`. |

**Context skills** fire on ambient signals throughout any session:

| Name | Type | Description |
| :---- | :---- | :---- |
| **ats-optimization** | Skill | Fires automatically when a resume is being edited or generated. Checks for ATS-hostile formatting, missing keywords, and structural issues. Suggests fixes inline. |
| **salary-research** | Skill | Fires when compensation is mentioned in any context. Pulls current market data for the role, level, and geography under discussion. |
| **follow-up-timing** | Skill | Fires when an application is viewed in the tracker. Evaluates elapsed time against company-specific norms and flags if a follow-up action is warranted. |
| **cultural-risk-flag** | Skill | Fires when drafting LinkedIn content or outreach messages. Cross-references content against known company cultural profiles and flags potential misalignments. |
| **contact-context** | Skill | Fires when a contact at a target company is identified. Searches email and calendar history for prior correspondence and surfaces relevant context for outreach drafting. Requires user approval before use. |

# **6\. Hooks**

| Name | Type | Description |
| :---- | :---- | :---- |
| **SessionStart** | Hook | On every Claude Cowork (or Claude Code) session start, checks for: interviews scheduled today (triggers morning-brief), applications requiring follow-up (notifies user), and any pending daily insights from the insight engine. |
| **DailySchedule** | Hook | Triggered by node-cron at user-configured time. Delivers daily pipeline digest, market brief summary, and prompts for any application updates needed. Sends cross-platform notification via node-notifier. |
| **ApplicationUpdate** | Hook | Fires whenever an application record is updated. Triggers the insight engine to re-evaluate patterns and updates job-scout scoring weights if outcome data has been added. |
| **ArtifactSaved** | Hook | Fires when a new artifact is saved. Logs metadata to the artifact inventory and pushes the record to the configured analytics connector. |

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

External services are configured via the plugin's .mcp.json file. Run `/career-navigator:setup` to configure integrations — the wizard handles all file edits automatically. Each integration is optional and activates the relevant agents and skills when configured.

| Name | Type | Description |
| :---- | :---- | :---- |
| **LinkedIn** | MCP | Job posting search, connection graph access, InMail drafting, post publishing and analytics. Required for networking strategy features. |
| **JobSearch** | MCP | Web scraping API providing live job listings from Indeed, LinkedIn, and other boards. Free tier available. Primary source for broad job discovery in Phase 1A. Configured via `/career-navigator:setup`. |
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

Stored at `{user_dir}/profile/profile.md`. Created by `/career-navigator:setup` — scans documents in `{user_dir}` and builds the profile from existing resumes and cover letters; falls back to conversational Q&A if no documents are found. Read automatically by all agents at the start of every operation — agents must not ask for information that is already in the profile.

* **identity** — name, location, contact info, professional summary, core differentiator
* **target\_roles** — preferred titles, minimum seniority level
* **target\_companies** — primary, secondary, and tertiary targets; industries to prioritize and avoid
* **compensation\_floor** — minimum total comp (base + bonus + equity annualized); expected ranges by company type
* **location** — geographic preferences, relocation openness, remote/hybrid preference
* **key\_skills** — prioritized skill list for ATS matching and corpus tagging
* **differentiators** — named, high-value elements that must appear in every tailored resume
* **search\_notes** — standing instructions for agents: preferred channels, company-specific notes, anything static that should inform every search and application

## **10.1 Resume Corpus**

The corpus is not a collection of discrete resumes — it is a structured pool of experience units that can be recombined. Each unit has metadata indicating source document, role type relevance, industry tags, and performance history.

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
| **type** | Enum | Resume / Cover Letter / Portfolio / Other |
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

## **12.1 Scheduled Events (node-cron)**

| Name | Type | Description |
| :---- | :---- | :---- |
| **Morning Digest** | Daily (configurable time) | Pipeline status, benchmark comparison, action items, interview brief if applicable, market news summary |
| **Follow-up Alerts** | Daily | Applications exceeding normal response window for their stage and company type |
| **Weekly Market Brief** | Weekly (configurable day) | Deeper market intelligence report: role trend shifts, new opportunity signals, event radar updates |
| **Insight Report** | Weekly | Pattern analysis from outcome data with specific recommendations for adjusting strategy |

## **12.2 Event-Driven Notifications (node-notifier)**

| Name | Type | Description |
| :---- | :---- | :---- |
| **High-Value Event Alert** | Immediate | Fires when event radar identifies a conference or meetup with strong match and presentation opportunity |
| **Application Action Due** | Same-day | Follow-up or thank-you note due based on timeline intelligence |
| **Interview Today** | Morning of | Triggers morning-brief generation and delivery |
| **Offer Received** | Immediate | Prompts offer evaluation flow with market salary data and negotiation guidance |

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

Phase 1 builds the complete local-first job search intelligence platform. The foundation in Phase 1A establishes the plugin scaffold, setup flow, and live job search. Phase 1B constructs the full skill layer — workflow skills that activate from conversational context, a closed feedback loop connecting application outcomes to future recommendations, and a pipeline dashboard. Phase 1C adds candid role assessment and skills gap analysis. Phase 1D extends the job-scout agent with outcome-weighted scoring and proactive opportunity discovery. Phase 1E completes the platform with professional presence tools: networking strategy, event radar, and LinkedIn content advising. At the end of Phase 1, all core job search workflows are intelligent, locally self-contained, and require no external service dependencies.

### **Phase 1A — Core platform: plugin scaffold, setup, session start, and live job search**

* Plugin scaffold: manifest, directory structure

* `setup` skill and conversational configuration wizard — scans the job search folder, auto-imports existing resumes into corpus, builds user profile from available documents; falls back to conversational Q&A if no source documents found; initializes all data schemas (corpus, tracker, artifacts index)

* `search-jobs` skill — live job search via Indeed connector; assisted-manual fallback

* `session-start` skill — `SessionStart` hook with pipeline digest on every session open; onboarding on first run

* Local filesystem storage — all data written to `{user_dir}`; no cloud dependency

### **Phase 1B — Skill layer and intelligence: workflow skills, application tracker, ATS scoring, and insight engine**

* **Agents introduced:** `resume-coach` (resume assembly, ATS optimization, narrative coaching), `insight-engine` (outcome pattern analysis, performance weight updates)

* Workflow skills built and auto-triggered: `tailor-resume`, `cover-letter`, `track-application`, `add-source`, `resume-score`, `list-artifacts` — activate from conversational intent; also invocable via explicit commands

* Application tracker — full conversational tracking with stage history, contacts, notes, and outcome logging

* ATS scoring — keyword match, formatting compliance, and narrative strength scoring on generated and existing resumes

* `ats-optimization` and `salary-research` context skills

* Insight engine and feedback loop — outcome data feeds back into corpus performance weights and job-scout scoring

* Benchmarking against industry norms by role, level, company size, and geography

* Follow-up timeline intelligence with company-specific response window data

* D3 pipeline dashboard with timeline view and benchmark comparisons

* `/career-navigator:pipeline`, `/career-navigator:follow-up`, `/career-navigator:market-brief`

### **Phase 1C — Advisor layer: honest role assessment, skills gap analysis, and training ROI**

* **Agents introduced:** `honest-advisor` (candid role competitiveness assessment, norm/exception/strategy pattern), `market-researcher` (role demand trends, AI/automation displacement, geographic signals)

* Honest advisor integration with three-step norm/exception/strategy pattern

* Market researcher: role demand trends, AI/automation displacement, geographic signals

* Skills self-assessment and gap analysis against target role requirements

* Training recommendation engine with cost-benefit-time ROI analysis (certifications, degrees, bootcamps, self-study)

* `/career-navigator:suggest-roles`, job scout scoring improvements driven by outcome data

* Note: skills assessment becomes significantly richer once Phase 2B mock interview performance data feeds back into the profile

### **Phase 1D — Proactive discovery: outcome-weighted job scoring and market trend monitoring**

* **Agent introduced:** `job-scout` (full outcome-weighted job ranking, proactive opportunity alerts, transferable skills analysis)

* Job scout with full outcome-driven scoring and proactive opportunity alerts

* Non-obvious role suggestions based on transferable skills

* Market trend monitoring with proactive notifications for significant shifts

* Role demand forecasting incorporating AI/automation displacement signals

### **Phase 1E — Professional presence: networking strategy, event radar, and LinkedIn content advisor**

* **Agents introduced:** `networking-strategist` (network analysis, gap identification, outreach drafting), `content-advisor` (LinkedIn content evaluation, cultural risk flagging, topic recommendations), `event-intelligence` (global event discovery, ROI assessment, presentation opportunity flagging)

* Networking strategy and `/career-navigator:network-map`

* Event radar with local, national, and international discovery

* Presentation opportunity flagging with proposal drafting assistance

* LinkedIn content advisor with topic recommendations

* Post evaluator with cultural/political risk assessment against target company profiles

* `/career-navigator:draft-outreach`, `/career-navigator:content-suggest`, `/career-navigator:evaluate-post`, `/career-navigator:event-radar`

* Note: outreach enrichment with email/calendar history deferred to Phase 2A

## **Phase 2 — Integrations**

Phase 2 extends Career Navigator beyond the local filesystem by connecting it to the external services that complete the full job search experience. Phase 2A unlocks the email and calendar history that powers warm networking intelligence — surfacing prior contact relationships before outreach is drafted. Phase 2B brings the complete interview layer: a full mock interview system with audio capture and automated debrief logging, combined into a single release to avoid shipping the prep experience without the capture infrastructure. Phase 2C adds cloud storage connectors and ATS read-access, making the platform portable and enabling users to track applications submitted through employer systems. Phase 2D closes the analytics loop with BI connectors and LinkedIn automation for deeper pipeline visibility. Each sub-phase is independently deployable — users can adopt what's relevant to their workflow without requiring all of Phase 2 to be complete.

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

### **Phase 2D — Advanced Analytics & LinkedIn Automation**

* Power BI streaming dataset connector

* Qlik Engine API connector

* D3 data export connector for custom visualization

* LinkedIn automation for job search and connection graph access (approach TBD)

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

# **Appendix: Command Quick Reference**

| Command | Purpose |
| :---- | :---- |
| **/career-navigator:setup** | Configure job search folder, build corpus and profile, set up JobSearch (run first) |
| **/career-navigator:tailor-resume** | Assemble optimal resume for a specific role from corpus |
| **/career-navigator:cover-letter** | Generate targeted cover letter |
| **/career-navigator:resume-score** | Score resume against a job description |
| **/career-navigator:add-source** | Add source document to corpus |
| **/career-navigator:list-artifacts** | List all generated artifacts |
| **/career-navigator:search-jobs** | Search and rank job opportunities |
| **/career-navigator:track-application** | Log or update an application |
| **/career-navigator:pipeline** | View full application dashboard |
| **/career-navigator:follow-up** | Generate contextual follow-up message |
| **/career-navigator:market-brief** | Current market intelligence report |
| **/career-navigator:suggest-roles** | Discover non-obvious role opportunities |
| **/career-navigator:prep-interview** | Full interview preparation session |
| **/career-navigator:mock-interview** | Mock interview (guided/random/adaptive) |
| **/career-navigator:interview-debrief** | Post-interview Q\&A capture |
| **/career-navigator:morning-brief** | Day-of interview briefing |
| **/career-navigator:network-map** | Visualize network relative to targets |
| **/career-navigator:draft-outreach** | Draft LinkedIn/email outreach message |
| **/career-navigator:content-suggest** | Suggest LinkedIn post topics |
| **/career-navigator:evaluate-post** | Evaluate LinkedIn post before publishing |
| **/career-navigator:event-radar** | Discover relevant networking events |

