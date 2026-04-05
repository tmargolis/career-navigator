---
name: prep-interview
description: >
  Full interview preparation for a specific application or role: company and
  news context, stage-specific questions (recruiter, hiring manager, technical,
  panel, executive, final), talking points from ExperienceLibrary, optional
  voice/STT via interview-coach. Saves a brief under CareerNavigator/interview-prep/
  and logs a [prep] note in tracker.json. Also invocable via
  /career-navigator:prep-interview.
triggers:
  - "/prep-interview"
  - "/career-navigator:prep-interview"
  - "prep me for my interview"
  - "prep for my interview"
  - "interview prep for"
  - "prepare for my interview"
  - "recruiter call tomorrow"
  - "recruiter screen with"
  - "phone screen with"
  - "hiring manager interview"
  - "HM interview"
  - "mock prep for"
---

## Workflow

### 1. Resolve `{user_dir}` and gate

Require `CareerNavigator/profile.md`, `ExperienceLibrary.json`, and `tracker.json`. If missing:

> Run `/career-navigator:launch` first to initialize Career Navigator.

### 2. Identify target

From user message or tracker:

- Prefer **`application_id`** if given; else match **company** + **role** against `tracker.json` `applications[]`.
- If ambiguous, ask one short disambiguation question.

Collect if missing:

- **`interview_stage`:** `recruiter` | `hiring_manager` | `technical` | `panel` | `executive` | `final` (default: infer from wording; recruiter call / phone screen → `recruiter`).
- Optional: **interviewer** name/title, **interview date**, JD text or paste.

### 3. Optional STT / voice

If the **`mcp-voice`** MCP exposes **`speak`** / **`listen`**, use them per **`agents/interview-coach/AGENT.md`**. If the user is **speaking** or pastes a **transcript** from host STT, pass it as `user_audio_transcript` in the handoff to **`interview-coach`**.

### 4. Invoke **interview-coach**

Read and follow **`agents/interview-coach/AGENT.md`** with:

- `mode`: **`prep`**
- `interview_stage` (required)
- `application_id` or `company` + `role`
- Optional: `interviewer`, JD, `interview_date`, `user_audio_transcript`

Use the exact agent name **`interview-coach`**.

### 5. Persist outputs

After the coach content is produced:

1. **Directory:** Ensure `{user_dir}/CareerNavigator/interview-prep/` exists.
2. **File:** Save the full prep brief as markdown using the path convention from the agent (company-slug, stage, date = today in local context unless user specified interview date for filename suffix).
3. **Tracker:** Append to the matched `applications[].notes` an object:

```json
{
  "date": "YYYY-MM-DD",
  "text": "[prep] Interview prep brief saved: CareerNavigator/interview-prep/{filename}.md (stage: {stage})."
}
```

Update `tracker.json` in place. If no application matched, skip tracker write but still save the file under `interview-prep/` with a clear filename and tell the user to link it via `/career-navigator:track-application` if needed.

### 6. Close

Offer **`/career-navigator:mock-interview`** for a voice or text practice session. Do not claim other Phase 2B features (e.g. **`interview-debrief`**) unless shipped.
