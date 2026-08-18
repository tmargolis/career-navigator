---
name: prep-interview
description: >
  Full interview preparation for a specific application or role: company and
  news context, stage-specific questions (recruiter, hiring manager, technical,
  panel, executive, final), and story evidence retrieved from StoryCorpus
  (with ExperienceLibrary fallback), optional voice/STT via interview-coach.
  Saves a brief under CareerNavigator/interview-prep/ and logs a [prep] note in
  tracker.json. Also invocable via /career-navigator:prep-interview.
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

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

Require `CareerNavigator/profile.md`, `ExperienceLibrary.json`, and `tracker.json`. If missing:

> Run `/career-navigator:launch` first to initialize Career Navigator.

Story corpus gate:
- Preferred source: `CareerNavigator/StoryCorpus.json`.
- If missing, run or suggest `mine-stories` first.
- If user wants to continue immediately, proceed with `ExperienceLibrary.json` fallback and clearly label lower story-specific confidence.

### 2. Identify target

From user message or tracker:

- Prefer **`application_id`** if given; else match **company** + **role** against `tracker.json` `applications[]`. If an `application_id` matches no row's `id`, check each row's `previous_ids` before declaring no match — prep briefs saved under earlier ids still resolve.
- Keep the matched row's `detail_file`, `contacts_file`, and `application` label; the write in step 6 needs them.
- Pull prior stage history and notes from the row's `detail_file` (`CareerNavigator/applications/<application_id>.json`) — `tracker.json` holds only `latest_stage` and `latest_stage_date`. Load the `contacts_file` only if interviewer background is needed, filtering its `contacts[]` to entries whose `application` equals the row's `application`.
- If ambiguous, ask one short disambiguation question.

Collect if missing:

- **`interview_stage`:** `recruiter` | `hiring_manager` | `technical` | `panel` | `executive` | `final` (default: infer from wording; recruiter call / phone screen → `recruiter`).
- Optional: **interviewer** name/title, **interview date**, JD text or paste.

### 3. Optional STT / voice

If the **`mcp-voice`** MCP exposes **`speak`** / **`listen`**, use them per **`agents/interview-coach/AGENT.md`**. If the user is **speaking** or pastes a **transcript** from host STT, pass it as `user_audio_transcript` in the handoff to **`interview-coach`**.

### 4. Retrieve targeted stories

Before invoking interview-coach, run `story-retrieval` with:

- `application_id` or `company` + `role`
- `interview_stage`
- optional JD and interviewer context

Use the returned 8-12 selected stories as the primary interview evidence payload.

### 5. Invoke **interview-coach**

Read and follow **`agents/interview-coach/AGENT.md`** with:

- `mode`: **`prep`**
- `interview_stage` (required)
- `application_id` or `company` + `role`
- Optional: `interviewer`, JD, `interview_date`, `user_audio_transcript`
- `selected_stories` payload from `story-retrieval`

Use the exact agent name **`interview-coach`**.

### 6. Persist outputs

After the coach content is produced:

1. **Directory:** Ensure `{user_dir}/CareerNavigator/interview-prep/` exists.
2. **File:** Save the full prep brief as markdown using the path convention from the agent (company-slug, stage, date = today in local context unless user specified interview date for filename suffix).
3. **Detail file:** Append to `notes[]` in the matched row's `detail_file` — `{user_dir}/CareerNavigator/applications/<application_id>.json` — an object:

```json
{
  "date": "YYYY-MM-DD",
  "text": "[prep] Interview prep brief saved: CareerNavigator/interview-prep/{filename}.md (stage: {stage})."
}
```

Never overwrite or reorder existing note entries.

4. **Summary row:** Set the matching `tracker.json` → `applications[]` row's `notes_count` to the detail file's new `notes[]` length. This note does not add a stage, so leave `stage_count`, `latest_stage`, `latest_stage_date`, and `status` untouched.

Load and re-dump both JSON files programmatically (`json.load` / `json.dump`, `indent=2`, `ensure_ascii=False`), then reload to verify `notes_count` matches the detail array. If no application matched, skip both writes but still save the file under `interview-prep/` with a clear filename and tell the user to link it via `/career-navigator:track-application` if needed.

### 7. Close

Offer **`/career-navigator:mock-interview`** for a voice or text practice session. Do not claim features that are not shipped.
