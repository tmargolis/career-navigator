---
name: mock-interview
description: >
  Starts a mock interview session with configurable mode (guided, random,
  adaptive), stage (recruiter, hiring manager, technical, panel, executive,
  final), and vibe (supportive through bored). If mode or vibe are omitted,
  the system selects defaults and announces them. Delegates to interview-coach;
  optional mcp-voice MCP TTS/STT when tools are present. Also invocable via
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

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

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
- **`interview_stage` (if user omitted):** infer from the **`tracker.json` summary row** for the active application — its `status`, `latest_stage`, and `latest_stage_date` give the next likely stage without opening anything (e.g. `phone_screen` / `latest_stage: "recruiter"` → **`recruiter`**; otherwise **`hiring_manager`**). Read the row's `detail_file` (`applications/<application_id>.json`) only when the user asks to practice against the actual interview history, and only for that one application. If no application context, default **`hiring_manager`**.
- **Announce** in one line before the first question, e.g.:  
  `Selected: mode=adaptive, vibe=neutral, stage=hiring_manager (defaults — say if you want different).`

**Recruiter practice:** When the user asks to practice for a **recruiter** or **phone screen**, set `interview_stage` to **`recruiter`**.

### 3. Audio (**mcp-voice** Extension)

**Discover** session tools: if **`speak`** (TTS) or **`listen`** (STT) from the **`mcp-voice`** extension are present, **prefer** them for mock practice per **`agents/interview-coach/AGENT.md`**. Otherwise **text-only**. Never require audio.

### 4. Invoke **interview-coach**

Read and follow **`agents/interview-coach/AGENT.md`** with:

- `mode`: **`mock`**
- `mock_mode`, `vibe`, `interview_stage`
- Target context (application id, company, role, JD if any)

Run the mock **turn-by-turn** in chat until the user ends or you reach a natural wrap-up per the agent.

### 5. Optional tracker note

Only when the user asks for a log (or it clearly aids follow-up), write the **multi-file
transaction** for appending a note, per [references/tracker-schema.md](../../references/tracker-schema.md) — never edit one file and skip the other:

1. Find the application's summary row in `tracker.json` (match on `id`; check `previous_ids` if the id came from an older brief) and take its `detail_file`.
2. Append to that file's `notes[]` — never overwrite or reorder existing entries:
   ```json
   { "date": "YYYY-MM-DD", "text": "[mock] {interview_stage} mock — {mode}/{vibe}, {one-line takeaway}" }
   ```
3. Set the summary row's `notes_count` to the new array length.

A mock is not a real interview: do **not** append to `stage_history[]`, and do not touch
`status`, `latest_stage`, or `latest_stage_date`.

Load and re-dump both files programmatically (`json.load` / `json.dump` with `indent=2`,
`ensure_ascii=False`) and reload to validate — hand-editing this JSON has corrupted files before.
