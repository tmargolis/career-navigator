---
name: mock-interview
description: >
  Starts a mock interview session with configurable mode (guided, random,
  adaptive), stage (recruiter, hiring manager, technical, panel, executive,
  final), and vibe (supportive through bored). Delegates to interview-coach;
  optional TTS for questions and STT for answers when the host supports it.
  Also invocable via /career-navigator:mock-interview.
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

Defaults if user does not specify: `adaptive`, `neutral`, `hiring_manager`, and best-matching tracker application if single active interview-stage app exists.

**Recruiter practice:** When the user asks to practice for a **recruiter** or **phone screen**, set `interview_stage` to **`recruiter`**.

### 3. Audio

Per **`agents/interview-coach/AGENT.md`**: offer **TTS** for reading questions when available; use **STT** for user answers when available; otherwise **text-only**. Never require audio.

### 4. Invoke **interview-coach**

Read and follow **`agents/interview-coach/AGENT.md`** with:

- `mode`: **`mock`**
- `mock_mode`, `vibe`, `interview_stage`
- Target context (application id, company, role, JD if any)

Run the mock **turn-by-turn** in chat until the user ends or you reach a natural wrap-up per the agent.

### 5. Optional tracker note

If the user wants a log: append a short `applications[].notes` entry (no `[prep]` required) e.g. `[mock]` with date and stage—only when they ask or when it aids follow-up.
