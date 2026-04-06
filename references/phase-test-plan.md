# Career Navigator Phase Test Plan

This document defines practical validation checks for each delivery phase.
Use it as a release gate before tagging a phase complete.

## Convention: example prompts (copy/paste)

**Whenever functionality ships or changes**, extend this file with a **`### Example prompts (copy/paste)`** subsection under that phase (or the closest phase that owns the feature). Each subsection should include at least:

- One **slash-command** style prompt (`/career-navigator:…`) where applicable.
- One **natural-language** variant that triggers the same skill intent.
- **Expected result** notes where behavior is non-obvious (boundaries, Phase 2A limits, etc.).

Keep prompts aligned with **`skills/*/`** triggers and **`references/career-navigator-spec.md`**. Phase **1E** is where networking + **`writer`** prompts live; refresh them when those agents or orchestration change.

## Test Data Prerequisites

- A valid `{user_dir}` with `CareerNavigator/profile.md`.
- At least one source resume/CV in `{user_dir}`.
- `CareerNavigator/tracker.json` with a mix of open and resolved applications.
- `CareerNavigator/artifacts-index.json` populated with at least one resume and one cover letter.

---

## Phase 1A — Core Platform

### Scope
- Launch wizard (`/career-navigator:launch`), profile creation, ExperienceLibrary initialization, focus-career behavior, live job search.

### Tests
- Run `/career-navigator:launch`; verify all core files are created in `CareerNavigator/`.
- Confirm the launch wizard handles existing docs and builds ExperienceLibrary units.
- Start a fresh session; verify `focus-career` behavior (first-run onboarding vs critical-only alerts).
- Run `/career-navigator:search-jobs`; confirm results return from Indeed and include apply links.

### Pass Criteria
- Core files are valid and readable.
- Job search works with profile-driven defaults.
- Session behavior is correct for both first-run and returning-user states.

### Example prompts (copy/paste)

```text
/career-navigator:launch
```

```text
Set up Career Navigator using my job search folder. Build profile and ExperienceLibrary from the resumes already in this directory.
```

```text
Search for jobs matching my profile—top 5 with apply links.
```

```text
/career-navigator:search-jobs
```

```text
Session just started—run focus-career for critical-only alerts using my CareerNavigator data.
```

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

### Example prompts (copy/paste)

```text
/career-navigator:add-source
```
```text
Ingest my latest resume PDF in this folder into the ExperienceLibrary.
```

```text
Here's the job description [paste JD]. Tailor my resume for this role.
```

```text
/career-navigator:tailor-resume
```

```text
/career-navigator:cover-letter
```
```text
Write the cover letter for the role whose JD I just used—use my tailored resume artifact if it exists.
```

```text
Score my resume against this JD and tell me ATS gaps: [paste resume + JD].
```

```text
/career-navigator:resume-score
```

```text
I just applied to [Company] for [Role] on [date]. Log it in the tracker.
```

```text
/career-navigator:track-application
```

```text
What's converting in my pipeline? Run pattern-analysis and update weights.
```

```text
/career-navigator:pattern-analysis
```

```text
/career-navigator:list-artifacts
```

```text
List my generated resumes and cover letters with dates and linked applications.
```

```text
This resume has bad ATS structure—run ats-optimization and give me prioritized fixes.
```

```text
Run the full analyst report and point me to the dashboard for charts I shouldn't miss.
```

```text
Run full career analysis / pipeline dashboard generation so I can open the HTML dashboard.
```

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

### Example prompts (copy/paste)

```text
/career-navigator:assessment
```
```text
Give me an honest assessment vs my target role using my tracker and ExperienceLibrary—norm, exceptions, and strategy.
```

```text
/career-navigator:training-roi
```
```text
Is a part-time MBA worth it for my target role in the next 18 months? Compare to self-study and a certificate.
```

```text
/career-navigator:market-brief
```
```text
Market brief for my primary target role and location—demand, AI displacement, geography.
```

```text
/career-navigator:suggest-roles
```
```text
What non-obvious roles should I apply to based on transferable skills? Update job-scout signals if you can.
```

---

## Phase 1D — Proactive Discovery

### Scope
- Tuned `job-scout` scoring, confidence-aware weighting, proactive recommendation tiers, schedule-ready operations.

### Tests
- Run `search-jobs` with low and higher outcome-history datasets; confirm confidence tiers and adaptive behavior.
- Validate recommendation tiers (`critical`, `high`, `watch`, `none`) and priority summary output.
- Run `daily-schedule`; confirm artifact reconciliation and digest output.
- Add a new PDF/DOCX source file, run `daily-schedule`; verify auto-ingest path (`add-source`) and index consistency.
- Run `suggest-roles` and `market-brief`; verify agent invocations succeed using exact agent names.

### Pass Criteria
- Ranking is stable, explainable, and confidence-aware.
- Daily workflow handles new source files automatically.
- Agent invocation failures are retried/fallbacked as defined.

### Example prompts (copy/paste)

```text
Find jobs for my target role and rank them—call out critical and high alerts if any.
```

```text
/career-navigator:search-jobs
```

```text
Run my daily brief: reconcile artifacts if needed, pipeline summary, follow-ups due.
```

```text
/career-navigator:daily-schedule
```

```text
I added a new resume PDF to my job search folder—run daily-schedule and confirm add-source ran if a new source appeared.
```

```text
/career-navigator:market-brief
```
```text
/career-navigator:suggest-roles
```
**Expect:** Exact agent names **`market-researcher`** and **`honest-advisor`** (retry-once behavior per skills).

---

## Phase 1E — Professional Presence

### Scope
- **`networking-strategist`** agent, invoked by skills **`networking-strategy`**, **`network-map`**, **`event-intelligence`**, and **`event-radar`**.
- **`writer`** agent, invoked by **`draft-outreach`**, **`content-suggest`**, **`evaluate-post`**, and orchestrated from **`cover-letter`**, **`follow-up`**, and optional **`tailor-resume`** Summary polish; consumes handoffs from **`networking-strategist`** and **`voice-profile.md`** (user-supplied posts).

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

**Expect:** Handoff brief + direction to **`writer`** or **`/career-navigator:draft-outreach`**, not a finished DM from **`networking-strategist`**.

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

#### **`cover-letter`** (orchestrates **`writer`**)

```text
/career-navigator:cover-letter
```
```text
Write a cover letter for this role. [paste job description]. Use my tailored resume from artifacts if available.
```

#### **`follow-up`** (orchestrates **`writer`**)

```text
What needs a follow-up? Show the queue and draft messages for anything overdue or critical.
```
```text
/career-navigator:follow-up
```

#### **`writer`** — direct skills

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

```text
Review this draft for political or reputational risk against my target employers in profile.md—risk tier and safer paraphrases only, don't tell me what to believe: [paste draft].
```

```text
/career-navigator:evaluate-post
```

#### **`writer`** — voice profile (seed + refresh)

```text
I'm going to use you for outreach and posts. Here are 3 LinkedIn posts I've written—capture my voice in CareerNavigator/voice-profile.md and give me a voice_profile_v1 JSON block.

[paste posts]
```

```text
Before drafting anything else, read my voice-profile.md and tell me your confidence in matching my tone (high/medium/low).
```

#### **`tailor-resume`** — optional voice-aligned Summary (orchestrates **`writer`**)

```text
Tailor my resume for this JD, and for the Summary section only, match the voice in my voice-profile.md / pasted LinkedIn samples—use resume-coach ResumeSummaryBrief then writer resume-summary.

[paste JD]
```

#### **End-to-end: strategist handoff → outreach**

```text
Run networking-strategy from my profile and tracker, then I'll paste your handoff bullets into draft-outreach—don't draft my DM in the strategist step.
```
*(Then in a follow-up turn:)*
```text
/career-navigator:draft-outreach — use this StrategistHandoff: [paste bullets from prior turn]
```

#### **Thank-you follow-up** (validates **`follow-up`** + **`writer`**)

```text
I had a phone screen for [Role] at [Company] three days ago—what's my follow-up status and draft a thank-you if I'm due.
```

#### **Agent invocation / retry** (host-dependent)

Retry behavior is validated by observing logs or the host’s agent tool—not a single user prompt. Optionally run the same **`network-map`** or **`event-radar`** prompt twice after a transient failure to confirm recovery after one retry per skill rules.

### Agent: **`networking-strategist`**

#### Invocation and orchestration
- From each skill body, confirm the model uses the **exact** agent name **`networking-strategist`** (no aliases such as “network” or “strategy agent”).
- Simulate or observe one failed subagent call; confirm **one retry** with the same name before surfacing an error (per skill instructions).

#### Role boundary (outreach vs strategy)
- Run **`networking-strategy`** with an explicit ask to “write my LinkedIn message” in the same turn.
  - **Expect:** no ready-to-send DM/email body from **`networking-strategist`**; instead a **handoff brief** (objective, audience archetype, evidence-backed hooks, tone, avoid list) and explicit pointer to **`writer`** or **`/career-navigator:draft-outreach`** for final copy.
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

### **`writer`**

#### Voice and persistence
- First run: confirm the agent **asks for 2–5 sample posts** (or similar professional writing) and offers to append to **`CareerNavigator/voice-profile.md`** with optional **`voice_profile_v1`** JSON.
- Re-run **`evaluate-post`** after adding samples; confirm **voice match** confidence label updates or rationale references samples.

#### Skills
- **`draft-outreach`:** send-ready copy; **no** invented shared history; accepts **StrategistHandoff** when user pastes it; **Phase 2A** note when inbox context is missing.
- **`content-suggest`:** topics tied to profile/ExperienceLibrary; optional full draft path + **`evaluate-post`** nudge.
- **`evaluate-post`:** **risk tier** + rationale vs **target companies** in profile; optional safer paraphrases; no prescriptive “what you should believe.”
- **`cover-letter`:** verify **CoverLetterBrief** is built first, then **`writer`** (`cover-letter` mode) produces final letter; artifact save unchanged.
- **`follow-up`:** verify **FollowUpBrief** objects only in the skill; message body comes from **`writer`** (`follow-up` mode).
- **`tailor-resume`** (optional): request “match my LinkedIn voice for the Summary only”; confirm **`ResumeSummaryBrief`** → **`writer`** (`resume-summary`) → merged Summary before save.

### Pass Criteria
- **`networking-strategist`** outputs are evidence-grounded, confidence-labeled, and **do not** substitute for **`writer`** on outreach copy.
- Event outputs avoid hallucinated logistics; uncertainty is stated explicitly.
- **`writer`** owns user-facing prose (outreach, cover letter, follow-up, optional Summary polish); briefs stay in orchestrating skills; **`voice-profile.md`** updates are explicit and opt-in.

---

## Phase 1F — Career planning, offer evaluation & compensation negotiation

### Scope
- New skills: `career-plan`, `evaluate-offer`, `negotiate-offer`, `compare-offers`
- Artifact outputs:
  - `{user_dir}/CareerNavigator/career-trajectory.md` + `career_trajectory_v1`
  - `{user_dir}/CareerNavigator/offer-context-{application_id}.json`
- Integration:
  - `job-scout` reads `career_trajectory_v1` and applies trajectory alignment bonus
  - `daily-schedule` monthly career-plan refresh nudge
  - `daily-schedule` offer-evaluation due nudge
  - `focus-career` critical-only offer evaluation due when deadline is imminent

### Test data prerequisites
- `CareerNavigator/profile.md` populated with target roles + target location.
- `CareerNavigator/ExperienceLibrary.json` with at least a few non-empty `units`.
- `CareerNavigator/tracker.json` containing:
  - At least one application with `status: "offer"` (and `offer.deadline` if possible).
  - A mix of outcomes so `honest-advisor` can label confidence tier.

### Tests
- Run `/career-navigator:career-plan`
  - Confirm `career-trajectory.md` is created and includes `career_trajectory_v1`.
- Run `/career-navigator:evaluate-offer`
  - Confirm `offer-context-{application_id}.json` is created for the correct offer app.
  - Confirm the offer evaluation includes scenario classification and a direct recommendation.
- Run `/career-navigator:negotiate`
  - Confirm it loads OfferContext (no redundant re-collection) and produces a draft via `writer`.
- Run `/career-navigator:compare-offers` when multiple offers exist
  - Confirm it compares side-by-side and prompts negotiation handoff.
- Run `/career-navigator:search-jobs`
  - Confirm `job-scout` output includes trajectory alignment and that scores reflect it.
  - Confirm trajectory evidence is explicit: `trajectory_context_status` and `trajectory_as_of` are returned, and the user-facing output includes a trajectory context line.
- Run `/career-navigator:daily-schedule`
  - Confirm it prompts for monthly career-plan refresh when `career-trajectory.md` is missing/stale.
  - Confirm it prompts offer evaluation due when an active offer exists with missing OfferContext.
- Run `focus-career` for a deadline edge case
  - Create/prepare a tracker offer with deadline within 24h and missing OfferContext.
  - Confirm `focus-career` includes "Offer evaluation due" critical alert.

### Pass Criteria
- All new slash commands exist with correct triggers.
- Required artifacts are written to the specified `{user_dir}` paths (or manual-save fallback is shown).
- `job-scout` trajectory bonus is present when `career-trajectory.md` exists and explicitly absent when it does not.
- Nudges appear in `daily-schedule` and (for imminent deadlines) in `focus-career`.

### Example prompts (copy/paste)

#### `career-plan` (baseline)
```text
/career-navigator:career-plan
```

#### `career-plan` (targeted ideal role)
```text
/career-navigator:career-plan
Ideal role: Senior Product Manager
```

#### `evaluate-offer` (single offer)
```text
/career-navigator:evaluate-offer
I received an offer from Acme for a Senior PM role. Deadline is 2026-04-02.
Base: $150k, bonus: $20k, equity: $60k. Location: Chicago.
```

#### `negotiate-offer`
```text
/career-navigator:negotiate
Use my last OfferEvaluation to draft a counter. Keep it assertive but respectful.
```

#### `compare-offers` (multi-offer)
```text
/career-navigator:compare-offers
Compare these two offers and tell me which one best matches my near-term trajectory.
```

#### Daily nudges
```text
/career-navigator:daily-schedule
```

### Round 1 fixes — repackage regression pass

Use this focused pass after repackaging to confirm the recent naming, orchestration,
and startup-behavior fixes.

#### Scope checks
- `focus-career` naming + backward alias (`/career-navigator:session-start`) still works.
- Session-start hook fallback guidance is clear when auto-hook does not fire.
- `search-jobs` uses **Recommendation** label (not Alert).
- `search-jobs`/`job-scout` trajectory consumption is explicit in output.

#### Tests
- Run startup manually with new command:
  - Confirm skill invoked is `focus-career`.
  - Confirm critical-only output format is unchanged.
- Run startup with backward alias:
  - Confirm `/career-navigator:session-start` still maps to the same behavior.
- Run `search-jobs` with a valid `career-trajectory.md` present:
  - Confirm output includes a trajectory context line:
    - `Trajectory context: used (as_of YYYY-MM-DD)` (or unavailable reason)
  - Confirm listing line uses `Recommendation: {critical|high|watch|none}`.
- Temporarily force trajectory parse failure (or remove JSON block):
  - Confirm search still works and reports trajectory as unavailable/unparseable.

#### Pass criteria
- `focus-career` is the primary startup skill name in context/output.
- Manual fallback works in sessions where auto SessionStart hook does not fire.
- No user-facing `Alert:` label remains in search results.
- Trajectory usage is auditable in response text and scoring rationale.

#### Example prompts (copy/paste)

```text
/career-navigator:focus-career
```

```text
/career-navigator:session-start
```

```text
/career-navigator:search-jobs
Use my current profile targets and show top 5.
```

```text
For each result, include the scoring header plus trajectory context status and recommendation tier.
```

```text
I got an offer from Stripe for Senior Product Manager, and the decision deadline is tomorrow at 10am. Please update my tracker.
Then run /career-navigator:focus-career.
```

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

### Example prompts (copy/paste)

```text
Search my Gmail for prior threads with [Name] at [Company] and summarize only what you find—I approve access for this session.
```
**Expect:** Works only when Phase 2A connectors are configured and user explicitly approves; otherwise clear **no access** message.

```text
Before /career-navigator:draft-outreach to [recruiter], pull last email exchange from calendar/email context and fold into the brief.
```

---

## Phase 2B — Interview Intelligence

### Scope
- Interview prep (`prep-interview`, **`interview-coach`**), mock interview modes (**defaults** when mode/vibe omitted), **`interview-capture`** **skill** (not agent), optional **`mcp-voice`** MCP (`speak`, `listen`) per **`CONNECTORS.md`**, **Pre-interview brief** as part of **`daily-schedule`** ( **`/career-navigator:morning-brief`** = focused alias). **`interview-debrief`** may remain deferred.

### Tests
- Run prep + mock interview across multiple stages/vibes.
- **`mock-interview` with no mode/vibe:** model **announces** selected `mock_mode` + `vibe` (defaults per §2.1) before first question.
- Validate **daily-schedule** includes **Pre-interview brief** when `stage_history` has a meeting **today**; validate **omitted** when none.
- Validate **`/career-navigator:morning-brief`** focused output (pre-interview slice only when applicable).
- **`[prep]`** tracker note + file under `CareerNavigator/interview-prep/` after prep.
- **`mcp-voice` MCP (Claude Desktop Extension `mcp-voice.mcpb`):** **TTS** — call **`speak`** with a short string; expect audio playback through local speaker and `"Speech complete."` response. **STT** — call **`listen`** and speak a short phrase; expect returned transcript matching spoken content.
- **`interview-capture`:** opt-in flow; employer warning once; **`[capture]`** or structured note in tracker when transcript processed.
- **Deferred until shipped:** full **`interview-debrief`** automation if not yet present.

### Pass Criteria
- Interview prep and mock workflows are coherent; **user-audio-only** assumptions for voice/STT; no standalone **`morning-brief`** skill.

### Structured test cases (IDs)

| ID | Scenario | Pass hint |
| --- | --- | --- |
| 2B-P1 | `/career-navigator:prep-interview` for HM + company in tracker | Brief file + `[prep]` note; cites ExperienceLibrary |
| 2B-P2 | Prep for **recruiter screen** | Emphasizes process, comp, timeline, fit-to-role |
| 2B-D1 | `/career-navigator:daily-schedule` with **no** meeting today per §3.1 allowlist | Output **lacks** **Pre-interview brief** subsection |
| 2B-D2 | `daily-schedule` with interview/recruiter stage **today** in `stage_history` | **Pre-interview brief (today)** present; ≥1 company covered |
| 2B-D3 | `/career-navigator:morning-brief` | Same pre-interview behavior as 2B-D2 when applicable; no full pipeline table unless user asked |
| 2B-M1 | `mock-interview` adaptive, neutral, **recruiter** | Session runs **without** requiring audio |
| 2B-M2 | `mock-interview` challenging vibe, **hiring_manager** | Observable tougher tone / pressure |
| 2B-M3 | `mock-interview` with **no** mode/vibe specified | **Announces** selected mode + vibe (e.g. adaptive + neutral) before first question |
| 2B-A1 | Prep with **audio unavailable** | Completes text-only; states limitation once |
| 2B-A2 | Prep/mock with **STT** (`listen`) | Mic recording → transcript text matches spoken content |
| 2B-A3 | **TTS** (`speak`) | Audio plays through local speaker; `"Speech complete."` returned |
| 2B-V1 | **End-to-end voice** (optional) | `speak` delivers question aloud; `listen` captures spoken answer; transcript used in next mock turn |
| 2B-C1 | `/career-navigator:interview-capture` with opt-in | Warning once; `interview-capture-settings.json`; tracker update after STT |

### Example prompts (copy/paste)

```text
/career-navigator:prep-interview
```
```text
Prep me for my upcoming HM interview at [Company] for [Role]—questions, stories, company angles.
```
```text
Prep me for a recruiter phone screen at [Company] for [Role].
```

```text
/career-navigator:mock-interview
```
```text
Mock interview: recruiter stage, neutral vibe, adaptive difficulty. Company: [Company], role: [Role].
```
```text
/career-navigator:mock-interview
```
```text
Mock interview for my Acme PM application — no other preferences.
```
**Expect:** Announces selected **mode** + **vibe** (defaults) before the first question.

```text
/career-navigator:interview-capture
```
```text
I want to log my interview from this WAV file: [path under job search folder]. I opt in for this session.
```

```text
/career-navigator:morning-brief
```
```text
I have interviews today—give me the morning brief with news and talking points.
```

```text
/career-navigator:daily-schedule
```
```text
Run my full daily brief (expect Pre-interview section only if something is scheduled today in the tracker).
```

#### `mcp-voice` MCP — TTS smoke test (2B-A3)

```text
Say this aloud: "Your mock interview for Acme will begin in 10 seconds. Take a breath and get ready."
```
**Expect:** Audio plays through local speaker immediately; response is `"Speech complete."` No link, no file — sound only.

#### `mcp-voice` MCP — STT smoke test (2B-A2)

```text
Listen for 10 seconds. I'll say my name and target role — then confirm you heard me correctly.
```
**Expect:** `listen` tool is called with `duration_seconds=10`; returned transcript matches what was spoken; model echoes it back for confirmation.

#### `mcp-voice` MCP — end-to-end voice turn (2B-V1)

```text
Ask me the first behavioral question for my [Company] HM interview using voice, then listen for my answer and give feedback.
```
**Expect:** Model calls `speak` to deliver the question aloud, then calls `listen` to capture the response, then provides coaching feedback in text.

```text
/career-navigator:interview-debrief
```
```text
Interview debrief: I just finished a panel at [Company]. [paste notes].
```
**Expect:** Not implemented until **`interview-debrief`** skill ships; may no-op or instruct user to use **`track-application`** notes for now.

---

## Phase 2C — Extended Integrations

### Scope
- Cloud storage and ATS/job-board connectors.

### Tests
- **2C-S1 (Google Drive, OneDrive or Dropbox portability via app sync/manual backup):** Use a desktop app to sync the local `{user_dir}` job-search folder (or manually back up/restore the folder) so the folder contents are available locally. Then run `/career-navigator:launch` and confirm the assistant does not ask to connect a connector for job files and that storage behavior remains local-first.
- **2C-F1 (No connector/sync fallback):** With no cloud storage sync/connector configured, run launch and confirm storage behavior remains local-first with no fabricated cloud state.
- **2C-F2 (Disconnect degradation):** Turn off application sync. Then re-run launch/list flows, and confirm graceful fallback to local behavior.
- **2C-R1 (Artifact listing parity):** After selecting any storage option, run `/career-navigator:list-artifacts` and verify listings remain consistent with local index semantics.
- Validate ATS read connectors return statuses without write side effects.
- Validate additional job-board source ingestion and deduping behavior.

### Pass Criteria
- Storage onboarding is reliable and scoped per provider:
  - Google Drive uses Drive app sync or manual backup/restore (no Drive connector reliance for typical job files).
  - OneDrive uses OneDrive app sync or manual backup/restore (no reliance on Claude’s Microsoft 365/OneDrive file-access connector for plugin JSON artifacts).
  - Dropbox uses Dropbox app sync or manual backup/restore.
- Local-first behavior remains intact when cloud storage sync/connector is absent or disconnected.
- No docs or launch prompts route Google Drive/OneDrive/Dropbox setup through `.mcp.json`.

### Example prompts (copy/paste)

```text
/career-navigator:launch
```

```text
Use Google Drive for portability for this workspace via Drive app sync (sync the local job-search folder to Google Drive). Do not rely on connecting a Drive connector for job files.
```
**Expect:** Assistant recommends Drive app sync or manual backup/restore steps and continues local-first behavior.

```text
/career-navigator:launch
```
```text
Use OneDrive for portability for this workspace via OneDrive application sync (sync the local job-search folder to OneDrive) or manual backup/restore. Do not rely on connecting a OneDrive connector for job files.
```
**Expect:** Assistant recommends OneDrive app sync/manual backup/restore steps and continues local-first behavior.

```text
/career-navigator:launch
```
```text
Set up cloud storage with Dropbox for this workspace. If it's already connected in this chat, acknowledge and skip setup steps.
```
**Expect:** Assistant recommends Dropbox app sync/manual backup/restore steps and continues local-first behavior.

```text
Run launch with local-only storage. Do not configure any cloud connector right now.
```
**Expect:** Assistant keeps local `{user_dir}` storage and does not claim cloud sync.

```text
I turned off Drive app sync (for Google Drive), paused OneDrive application sync (for OneDrive), or paused Dropbox application sync (for Dropbox). Re-run launch and confirm fallback behavior.
```
**Expect:** Clear disconnected/disabled-state message and local-first continuation.

```text
/career-navigator:list-artifacts
```
```text
List artifacts after connector selection and confirm index consistency.
```
**Expect:** Artifact list remains consistent and usable regardless of storage choice.

```text
Show me how to set up Google Drive (Drive app sync or manual backup/restore), OneDrive (OneDrive app sync or manual backup/restore), and Dropbox (Dropbox app sync or manual backup/restore) for storage in Claude Desktop. Do not use `.mcp.json`.
```
**Expect:** Google Drive, OneDrive, and Dropbox instructions all point to app sync or manual backup/restore.

```text
Sync application status from Greenhouse for applications I logged—read-only, no writes to employer ATS.
```

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

### Example prompts (copy/paste)

```text
Export my pipeline and analyst graph data in the format expected by our BI connector and show me the payload shape.
```

```text
/career-navigator:pipeline
```
```text
Open the dashboard and confirm exported metrics match the local tracker counts for applied vs interview stages.
```

```text
Run a LinkedIn-automation workflow only if it complies with policy—show guardrails before executing.
```

---

## Regression Checklist (Run Every Phase)

- Validate SKILL frontmatter (`name`, `description`, `triggers`) parses for all changed skills (including **`draft-outreach`**, **`content-suggest`**, **`evaluate-post`**).
- Validate core JSON files remain valid (`tracker.json`, `ExperienceLibrary.json`, `artifacts-index.json`).
- Re-run `search-jobs`, `track-application`, `tailor-resume`, and `daily-schedule` as smoke tests.
- Confirm docs match actual behavior (README + spec).
- **If you shipped or changed user-facing behavior**, add or update **`### Example prompts (copy/paste)`** under the owning phase (see convention at top of this file).
