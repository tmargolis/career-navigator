---
name: mock-interview
description: >
  Starts a mock interview session with configurable mode (guided, random,
  adaptive), stage (recruiter, hiring manager, technical, panel, executive,
  final), and vibe (supportive through bored). If mode or vibe are omitted,
  the system selects defaults and announces them. Delegates to interview-coach;
  optional Google voice MCP TTS/STT when tools are present. Also invocable via
  /career-navigator:mock-interview.
triggers:
  - "/mock-interview"
  - "/career-navigator:mock-interview"
  - "mock interview"
  - "practice interview"
  - "run a mock interview"
  - "interview practice"
---

## Workflow

### 1. Resolve `{user_dir}` and gate

Same as `prep-interview`: require `CareerNavigator/profile.md`, `ExperienceLibrary.json`, and `tracker.json` unless the user only wants a generic mock with pasted JD (then still need profile + EL minimum; create minimal context note if tracker empty).

### 2. Parameters (ask once if missing)

| Parameter | Values |
| --- | --- |
| **mock_mode** | `guided` \| `random` \| `adaptive` |
| **interview_stage** | `recruiter` \| `hiring_manager` \| `technical` \| `panel` \| `executive` \| `final` |
| **vibe** | `supportive` \| `neutral` \| `challenging` \| `antagonistic` \| `bored` |
| **target** | `application_id` or company + role (optional for generic practice) |

#### 2.1 When mode or vibe are **not** specified — **system selection**

The model **must** choose a concrete `mock_mode` and `vibe` before starting—**never** leave them implicit in the opening line.

- **`mock_mode` (if user omitted):** use **`adaptive`** (default for learning and feedback). If the user asked for “surprise me,” “mix it up,” or equivalent, pick `random` **at random** and state that you did.
- **`vibe` (if user omitted):** use **`neutral`**. If the user asked for “surprise” / “mix it up,” pick **one** vibe **at random** from the five allowed values and state it.
- **`interview_stage` (if user omitted):** infer from **`tracker.json`** (next likely stage for the active application—e.g. `phone_screen` / recruiter → **`recruiter`**; otherwise **`hiring_manager`**). If no application context, default **`hiring_manager`**.
- **Announce** in one line before the first question, e.g.:  
  `Selected: mode=adaptive, vibe=neutral, stage=hiring_manager (defaults — say if you want different).`

**Recruiter practice:** When the user asks to practice for a **recruiter** or **phone screen**, set `interview_stage` to **`recruiter`**.

### 3. Audio (Google voice MCP)

**Discover** session tools: if **`speak_text`** (TTS) or **`transcribe_audio_file`** (STT) from the **`voice`** MCP are present, **prefer** them for mock practice per **`agents/interview-coach/AGENT.md`**. Otherwise **text-only**. Never require audio.

### 4. Invoke **interview-coach**

Read and follow **`agents/interview-coach/AGENT.md`** with:

- `mode`: **`mock`**
- `mock_mode`, `vibe`, `interview_stage`
- Target context (application id, company, role, JD if any)

Run the mock **turn-by-turn** in chat until the user ends or you reach a natural wrap-up per the agent.

### 5. Optional tracker note

If the user wants a log: append a short `applications[].notes` entry (no `[prep]` required) e.g. `[mock]` with date and stage—only when they ask or when it aids follow-up.
