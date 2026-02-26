**CAREER NAVIGATOR**

Claude Cowork Plugin — Full Product Specification

Version 0.2 — February 2026

An AI-powered job search companion that combines the capabilities of

recruiters, career coaches, reverse recruiters, and market analysts into a single intelligent platform.

# **Table of Contents**

[**Table of Contents	2**](#heading=)

[**1\. Overview	3**](#heading=)

[1.1 Design Principles	3](#heading=)

[1.2 Plugin Architecture	3](#heading=)

[**2\. Plugin File Structure	4**](#heading=)

[**3\. Slash Commands	5**](#heading=)

[3.1 Resume & Cover Letter Commands	5](#heading=)

[3.2 Job Search & Tracking Commands	5](#heading=)

[3.3 Interview Prep Commands	6](#heading=)

[3.4 Networking Commands	6](#heading=)

[**4\. Agents	7**](#heading=)

[**5\. Skills	9**](#heading=)

[**6\. Hooks	10**](#heading=)

[**7\. Storage Connectors	11**](#heading=)

[7.1 Interface	11](#heading=)

[7.2 Available Connectors	11](#heading=)

[**8\. Analytics Connectors	12**](#heading=)

[**9\. External Service Integrations (.mcp.json)	13**](#heading=)

[**10\. Core Data Model	14**](#heading=)

[10.1 Resume Corpus	14](#heading=)

[10.2 Application Record	14](#heading=)

[10.3 Artifact Record	14](#heading=)

[**11\. The Intelligence Feedback Loop	16**](#heading=)

[**12\. Daily Rhythm & Scheduling	17**](#heading=)

[12.1 Scheduled Events (node-cron)	17](#heading=)

[12.2 Event-Driven Notifications (node-notifier)	17](#heading=)

[**13\. Interview Capture (Phase 2B)	18**](#heading=)

[13.1 Privacy Considerations (To Be Discussed)	18](#heading=)

[13.2 Fallback: Post-Interview Q\&A Flow	18](#heading=)

[**14\. The Honest Advisor Design Philosophy	19**](#heading=)

[**15\. Phased Delivery Plan	20**](#heading=)

[Phase 1A — "I built a Claude plugin that replaces a career coach" (MVP)	20](#heading=)

[Phase 1B — "It now tracks your entire job search and tells you what's working"	20](#heading=)

[Phase 1C — "It now gives you an honest assessment of your skills, your gaps, and exactly what training is worth your time and money"	20](#heading=)

[Phase 1D — "It now finds your next opportunity before you even know to look for it"	20](#heading=)

[Phase 1E — "It now preps you for every interview, at every level, in every mood"	21](#heading=)

[Phase 1F — "It now builds your professional brand while you search"	21](#heading=)

[Phase 2A — Email & Calendar Integration	21](#heading=)

[Phase 2B — Interview Audio Capture	22](#heading=)

[Phase 2C — Extended Integrations	22](#heading=)

[Phase 2D — Advanced Analytics & LinkedIn Automation	22](#heading=)

[Phase 3 — Platform Expansion	22](#heading=)

[Phase 4 — Enterprise & Ecosystem	22](#heading=)

[**16\. Open Questions & Deferred Decisions	24**](#heading=)

[**Appendix: Command Quick Reference	25**](#heading=)

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
| **Version** | 1.0.0 |
| **Platform** | Claude Cowork (macOS / Windows / Linux) (also compatible with Claude Code) |
| **Scheduling** | node-cron (cross-platform) |
| **Notifications** | node-notifier (cross-platform native notifications) |
| **Storage Layer (Phase 1\)** | Google Drive (additional connectors in Phase 2C) |
| **Analytics Layer (Phase 1\)** | SQLite \+ D3 visualization (additional connectors in Phase 2D) |
| **AI Services** | Claude API (via MCP), Whisper (audio transcription — Phase 2B) |
| **Job Search (Phase 1\)** | HasData (primary, via `/cn:setup`) \+ assisted-manual fallback |

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
| **/cn:setup** | Command | Conversational setup wizard. Configures HasData for automated job search and optionally sets up Google Drive for cloud storage. Validates credentials before saving, writes all config automatically. Re-runnable to update keys or switch connectors. |

## **3.1 Resume & Cover Letter Commands**

| Name | Type | Description |
| :---- | :---- | :---- |
| **/cn:tailor-resume** | Command | Takes one or more source documents from the corpus and a job description, assembles and rewrites the best possible resume for that specific role, scores it for ATS compatibility, and saves it to the artifact inventory. |
| **/cn:cover-letter** | Command | Generates a targeted cover letter for a specific role, drawing on the tailored resume, company research, and any known contact context. Saves to artifact inventory. |
| **/cn:resume-score** | Command | Scores an existing resume or cover letter against a job description for ATS keyword match, formatting compliance, and narrative strength. |
| **/cn:add-source** | Command | Adds a new source document (resume, CV, portfolio) to the resume corpus for use in future tailoring. |
| **/cn:list-artifacts** | Command | Lists all generated artifacts in the inventory with metadata: date created, job applied for, outcome if known. |

## **3.2 Job Search & Tracking Commands**

| Name | Type | Description |
| :---- | :---- | :---- |
| **/cn:search-jobs** | Command | Searches configured job boards and returns ranked results. Ranking incorporates skill match, outcome history, and market intelligence. Supports filters for role, location, company size, industry, and salary range. |
| **/cn:track-application** | Command | Logs a new application or updates an existing one. Accepts conversational input and structures it automatically into the tracker database. |
| **/cn:pipeline** | Command | Displays the full application pipeline dashboard with timeline view, benchmark comparisons, and action items flagged by stage age. |
| **/cn:follow-up** | Command | Generates a contextual follow-up message for a specific application based on elapsed time, last communication, and company norms. |
| **/cn:market-brief** | Command | Generates a current market intelligence report for the user's target roles and industries, including trend data, competition levels, and AI/automation impact assessment. |
| **/cn:suggest-roles** | Command | Analyzes the user's full experience corpus and suggests non-obvious role types their skills could be applied to, with rationale for each suggestion. |

## **3.3 Interview Prep Commands**

| Name | Type | Description |
| :---- | :---- | :---- |
| **/cn:prep-interview** | Command | Launches a full interview preparation session for a specific role. Pulls in company research, generates predicted questions, and optionally launches a mock interview. |
| **/cn:mock-interview** | Command | Starts a mock interview session. Accepts mode (guided/random/adaptive), stage (recruiter/HM/technical/panel/executive), and vibe (supportive/neutral/challenging/antagonistic/bored) parameters. |
| **/cn:interview-debrief** | Command | Post-interview Q\&A flow that captures the candidate's experience conversationally and structures it into the tracker. Fallback for users who do not use audio capture. |
| **/cn:morning-brief** | Command | Generates a pre-interview briefing for any interview scheduled today: company news, interviewer research, talking points, and current events likely to come up. |

## **3.4 Networking Commands**

| Name | Type | Description |
| :---- | :---- | :---- |
| **/cn:network-map** | Command | Visualizes the user's network relative to target companies, showing direct connections, second-degree paths, and identified gaps. |
| **/cn:draft-outreach** | Command | Drafts a LinkedIn message or email to a specific contact. Searches email and calendar history for prior context and incorporates it with user approval. |
| **/cn:content-suggest** | Command | Suggests LinkedIn post topics based on current industry trends, the user's target roles, and recent activity in their field. |
| **/cn:evaluate-post** | Command | Evaluates a draft LinkedIn post for audience fit, likely algorithmic performance, and cultural alignment with target companies. |
| **/cn:event-radar** | Command | Searches for relevant local, national, and international networking events and conferences. Returns ranked recommendations with ROI assessment and presentation opportunity flags. |

# **4\. Agents**

Agents are specialized Claude instances with focused roles. They can be invoked directly or orchestrated by commands. Multiple agents may collaborate on complex tasks.

| Name | Type | Description |
| :---- | :---- | :---- |
| **resume-coach** | Agent | Analyzes the resume corpus, identifies gaps and strengths, optimizes for ATS compatibility, and provides narrative coaching. Invoked by tailor-resume and resume-score commands. |
| **job-scout** | Agent | Searches and ranks job opportunities across all configured job boards. Incorporates outcome history and market intelligence into scoring. Ranking improves over time as the user logs outcomes. |
| **market-researcher** | Agent | Monitors macro hiring trends, role-specific demand signals, AI/automation displacement risks, geographic demand patterns, and sector-specific cycles. Feeds the market-brief command and the job-scout agent. |
| **honest-advisor** | Agent | Provides candid assessments of the user's competitiveness for specific roles, potential recruiter concerns, and strategies for overcoming barriers. Researches company/industry-specific deviations from general norms. Empathetic but unsparing. |
| **interview-coach** | Agent | Conducts mock interviews across all stages and vibes (supportive, neutral, challenging, antagonistic, bored). Adapts difficulty based on user performance in adaptive mode. Incorporates current events and company-specific research into questions. |
| **networking-strategist** | Agent | Analyzes the user's network relative to their goals, identifies gaps and paths, drafts outreach, and evaluates content strategy. Searches email and calendar history for contact context with user approval. |
| **content-advisor** | Agent | Evaluates LinkedIn content for audience fit, algorithmic performance, and cultural alignment with target companies. Flags political/cultural risks relative to specific employer profiles. Recommends topics proactively. |
| **event-intelligence** | Agent | Continuously discovers and evaluates networking events globally. Assesses ROI using attendee quality, user target overlap, and historical conversion data. Flags high-value presentation opportunities. |
| **insight-engine** | Agent | Analyzes cross-application outcome data to identify patterns: which resume variants, communication styles, and role types are performing best. Feeds recommendations back to job-scout and resume-coach. |
| **interview-capture** | Agent | Phase 2B feature. Processes audio transcription from interviews (via Whisper), extracts structured data, and auto-populates the tracker. Only active with explicit user opt-in. Full privacy framework required before activation. |

# **5\. Skills**

Skills are auto-triggered capabilities that Claude activates when relevant context is detected, without requiring an explicit command invocation.

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
| **google-drive** | Connector | Stores artifacts and event logs in Google Drive via OAuth. Default connector for personal users. |
| **onedrive** | Connector | Stores artifacts and event logs in Microsoft OneDrive via OAuth. Preferred for enterprise/Microsoft environments. |
| **dropbox** | Connector | Stores artifacts and event logs in Dropbox via OAuth. |
| **local** | Connector | Stores all data locally in a configurable directory. No cloud dependency. Suitable for privacy-sensitive users. |

# **8\. Analytics Connectors**

The analytics layer consumes structured event data from the storage connector and produces insights, visualizations, and dashboard views. The plugin ships with a built-in SQLite-based analytics engine for users without a BI tool.

| Name | Type | Description |
| :---- | :---- | :---- |
| **sqlite-builtin** | Connector | Default connector. Local SQLite database with built-in query engine. Powers the /cn:pipeline dashboard and insight engine natively. |
| **power-bi** | Connector | Pushes event data to a Power BI streaming dataset. Enables custom dashboard creation in Power BI Desktop or Service. |
| **qlik** | Connector | Integrates with Qlik Sense or QlikView via the Qlik Engine API. Enables associative analysis across the full application dataset. |
| **d3** | Connector | Exports structured event data in D3-compatible JSON format for custom visualization development. |

# **9\. External Service Integrations (.mcp.json)**

External services are configured via the plugin's .mcp.json file. Run `/cn:setup` to configure integrations — the wizard handles all file edits automatically. Each integration is optional and activates the relevant agents and skills when configured.

| Name | Type | Description |
| :---- | :---- | :---- |
| **LinkedIn** | MCP | Job posting search, connection graph access, InMail drafting, post publishing and analytics. Required for networking strategy features. |
| **HasData** | MCP | Web scraping API providing live job listings from Indeed, LinkedIn, and other boards. Free tier available. Primary source for broad job discovery in Phase 1A. Configured via `/cn:setup`. |
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

Stored at `data/profile/profile.md`. Created by `/cn:setup` (using Google Drive resume data if connected, otherwise conversationally). Read automatically by all agents at the start of every operation — agents must not ask for information that is already in the profile.

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

Interview capture is an opt-in feature that uses local audio recording and Whisper transcription to automatically log interview content. It has been moved to Phase 2B to allow time for a full privacy framework, consent model design, and cross-jurisdiction legal review before implementation. The post-interview Q\&A debrief (/cn:interview-debrief) serves as the Phase 1 alternative.

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

## **Phase 1A — "I built a Claude plugin that replaces a career coach" (MVP)**

* Plugin scaffold: manifest, directory structure, node-cron scheduler, node-notifier

* Resume corpus management and artifact inventory

* /cn:setup conversational configuration wizard — builds user profile from Google Drive if connected, auto-imports existing resumes into corpus, auto-imports past application history into tracker; falls back to conversational Q&A if no Drive access

* /cn:tailor-resume, /cn:cover-letter, /cn:resume-score, /cn:add-source, /cn:list-artifacts

* Basic conversational application tracker with /cn:track-application

* HasData job search (automated); assisted-manual fallback for LinkedIn

* Google Drive storage connector, local file storage default, SQLite data storage

* SessionStart hook with daily digest

## **Phase 1B — "It now tracks your entire job search and tells you what's working"**

* Insight engine and feedback loop

* Benchmarking against industry norms by role, level, company size, and geography

* Follow-up timeline intelligence with company-specific response window data

* D3 pipeline dashboard with timeline view and benchmark comparisons

* /cn:pipeline, /cn:follow-up, /cn:market-brief

## **Phase 1C — "It now gives you an honest assessment of your skills, your gaps, and exactly what training is worth your time and money"**

* Honest advisor agent with three-step norm/exception/strategy pattern

* Market researcher agent: role demand trends, AI/automation displacement, geographic signals

* Skills self-assessment and gap analysis against target role requirements

* Training recommendation engine with cost-benefit-time ROI analysis (certifications, degrees, bootcamps, self-study)

* /cn:suggest-roles, job scout scoring improvements driven by outcome data

* Note: skills assessment becomes significantly richer once Phase 1E mock interview performance data feeds back into the profile

## **Phase 1D — "It now finds your next opportunity before you even know to look for it"**

* Job scout with full outcome-driven scoring and proactive opportunity alerts

* Non-obvious role suggestions based on transferable skills

* Market trend monitoring with proactive notifications for significant shifts

* Role demand forecasting incorporating AI/automation displacement signals

## **Phase 1E — "It now preps you for every interview, at every level, in every mood"**

* Mock interview system: guided, random, and adaptive modes

* All stages: recruiter screen, hiring manager, technical, panel, executive, final

* Full vibe spectrum: supportive, neutral, challenging, antagonistic, bored (calibrated — not demoralizing)

* Current events integration woven into mock interview questions

* Morning brief with company news, interviewer research, and talking points

* Post-interview Q\&A debrief flow (/cn:interview-debrief) — structured conversational capture

* /cn:prep-interview, /cn:mock-interview, /cn:morning-brief

* Mock interview performance feeds back into Phase 1C skills profile

## **Phase 1F — "It now builds your professional brand while you search"**

* Networking strategy agent and /cn:network-map

* Event radar with local, national, and international discovery

* Presentation opportunity flagging with proposal drafting assistance

* LinkedIn content advisor with topic recommendations

* Post evaluator with cultural/political risk assessment against target company profiles

* /cn:draft-outreach, /cn:content-suggest, /cn:evaluate-post, /cn:event-radar

* Note: outreach enrichment with email/calendar history deferred to Phase 2A

## **Phase 2A — Email & Calendar Integration**

* Gmail and Outlook OAuth connectors (read-only scoped)

* Google Calendar and Outlook Calendar read-only access

* Contact correspondence history search for networking context

* Contact context skill: surfaces prior email/meeting history before outreach drafting

* Outreach drafting enriched with prior communication history

* Meeting history awareness for warm networking identification

## **Phase 2B — Interview Audio Capture**

* Full privacy risk assessment and consent model design

* Cross-jurisdiction recording consent guidance

* Local Whisper processing option for privacy-sensitive users

* Employer policy warnings surfaced before recording

* Audio and transcript storage with user-controlled retention and deletion

* Auto-population of tracker from interview transcription

## **Phase 2C — Extended Integrations**

* OneDrive storage connector

* Dropbox storage connector

* Local filesystem storage connector

* IllinoisJobLink job board connector

* ATS read-only connectors for Greenhouse, Workday, and Lever

## **Phase 2D — Advanced Analytics & LinkedIn Automation**

* Power BI streaming dataset connector

* Qlik Engine API connector

* D3 data export connector for custom visualization

* LinkedIn automation for job search and connection graph access (approach TBD)

## **Phase 3 — Platform Expansion**

* Hosted API proxy with per-user key management and usage tracking — enables monetization and removes the need for each user to obtain their own HasData key

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
| **Antagonistic Interview Mode** | UX | Exact calibration of antagonistic vibe — specifically what constitutes appropriately challenging vs. demoralizing. Needs user testing. System must back off when interview is imminent. |
| **Political/Cultural Content Guidance** | Ethics | System should inform not prescribe. Exact framing of cultural risk flags to be designed to avoid appearing to suppress legitimate expression. |
| **Data Retention Policy** | Privacy | How long application data, artifacts, and event logs are retained. User-controlled deletion scope to be specified. |
| **Salary Negotiation** | Scope | Offer evaluation and negotiation guidance mentioned briefly — full scope not yet specified. Candidate for Phase 3\. |
| **Training ROI Data Sources** | Technical | Sources for certification value, bootcamp outcomes, and degree ROI data need to be identified and validated for Phase 1C training recommendation engine. |

# **Appendix: Command Quick Reference**

| Command | Purpose |
| :---- | :---- |
| **/cn:setup** | Configure HasData and Google Drive (run first) |
| **/cn:tailor-resume** | Assemble optimal resume for a specific role from corpus |
| **/cn:cover-letter** | Generate targeted cover letter |
| **/cn:resume-score** | Score resume against a job description |
| **/cn:add-source** | Add source document to corpus |
| **/cn:list-artifacts** | List all generated artifacts |
| **/cn:search-jobs** | Search and rank job opportunities |
| **/cn:track-application** | Log or update an application |
| **/cn:pipeline** | View full application dashboard |
| **/cn:follow-up** | Generate contextual follow-up message |
| **/cn:market-brief** | Current market intelligence report |
| **/cn:suggest-roles** | Discover non-obvious role opportunities |
| **/cn:prep-interview** | Full interview preparation session |
| **/cn:mock-interview** | Mock interview (guided/random/adaptive) |
| **/cn:interview-debrief** | Post-interview Q\&A capture |
| **/cn:morning-brief** | Day-of interview briefing |
| **/cn:network-map** | Visualize network relative to targets |
| **/cn:draft-outreach** | Draft LinkedIn/email outreach message |
| **/cn:content-suggest** | Suggest LinkedIn post topics |
| **/cn:evaluate-post** | Evaluate LinkedIn post before publishing |
| **/cn:event-radar** | Discover relevant networking events |

