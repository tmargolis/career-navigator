---
name: interview-capture
description: >
  Opt-in post-interview capture: transcribe the user's own audio (user audio
  only), extract structured takeaways, and update tracker.json. Surfaces
  employer policy warning once; jurisdiction/retention per spec §13.1. Uses
  Google Cloud STT via the voice MCP when available. Not an agent—a skill
  orchestrating tools and track-application patterns. Also invocable via
  /career-navigator:interview-capture.
triggers:
  - "/interview-capture"
  - "/career-navigator:interview-capture"
  - "capture my interview"
  - "transcribe my interview notes"
  - "log interview from audio"
  - "interview audio capture"
---

## Scope (§13.1)

- **User audio only.** Do not capture or transcribe the employer’s side without appropriate consent and product scope—that remains **out of scope** for Phase 2B MVP.
- **Opt-in:** Run this skill **only** when the user **explicitly** asks to capture/log from audio or runs **`/career-navigator:interview-capture`**.
- **Employer policy warning (once):** Some employers prohibit **any** recording of interviews. Before the first capture session, show the warning from spec **§13.1** and require acknowledgment. Persist to **`{user_dir}/CareerNavigator/interview-capture-settings.json`**:

```json
{
  "employer_warning_acknowledged": true,
  "acknowledged_at": "YYYY-MM-DD",
  "user_opted_in": true
}
```

If **`employer_warning_acknowledged`** is already **true**, do **not** repeat the full warning—one line reminder max.

- **Retention / jurisdiction:** Use **`profile.md`** `location` for GDPR/CCPA framing per spec. If unclear, ask once which retention stance applies and store under **`interview-capture-settings.json`** as **`retention_note`**.

## Workflow

### 1. Resolve `{user_dir}` and gate

Require `CareerNavigator/profile.md` and `tracker.json`. If missing, send user to **`/career-navigator:launch`**.

### 2. Opt-in and warning

- If **`interview-capture-settings.json`** does not exist or **`employer_warning_acknowledged`** is false: print the **employer policy warning**; on user acknowledgment, write the settings file.
- If user has not **opted in** to capture for this session, confirm before processing audio.

### 3. Match application

Identify **`application_id`** (or company + role) for the interview being logged. If unknown, ask before writing tracker updates.

### 4. Transcription (STT)

- **Discover** tools: if the **`voice`** MCP (or equivalent) exposes **`transcribe_audio_file`**, use it for audio the user provides (**path** to a file under `{user_dir}` or absolute path they supply).
- If **no** STT tools: fall back to **user-pasted transcript** or **`/career-navigator:interview-debrief`** when shipped; do **not** invent transcripts.

### 5. Structure and write tracker

From the transcript (user side only), extract:

- Overall tone / how it went
- Stage, participants (from user statements)
- Topics, surprises, red flags / positive signals
- Committed follow-ups
- Next-round or outcome hints

Append to **`applications[].notes`** with prefix **`[capture]`** and date; update **`stage_history`** or **`next_step`** via the same patterns as **`track-application`** when appropriate.

### 6. Artifacts (optional)

Save transcript text to **`{user_dir}/CareerNavigator/interview-capture/`** as `{application_id}-{YYYY-MM-DD}-transcript.txt` if the user wants a file copy.

## Guardrails

- **Honest over encouraging** when summarizing performance.
- **No** multi-party recording claims; label transcript as **user channel only** when other speakers are quoted from user recall.
