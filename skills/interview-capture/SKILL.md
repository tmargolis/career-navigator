---
name: interview-capture
description: >
  Opt-in post-interview capture: transcribe the user's own audio (user audio
  only), extract structured takeaways, and update tracker.json. Surfaces
  employer policy warning once; jurisdiction/retention per spec §13.1. Uses
  the local mcp-voice MCP (faster-whisper STT) when available. Not an
  agent—a skill orchestrating tools and track-application patterns. Also
  invocable via /career-navigator:interview-capture.
triggers:
  - "/interview-capture"
  - "/career-navigator:interview-capture"
  - "capture my interview"
  - "transcribe my interview notes"
  - "log interview from audio"
  - "interview audio capture"
---

## Scope (§13.1)

- **User audio only.** Do not capture or transcribe the employer’s side without appropriate consent and product scope—that remains **out of scope**.
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

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

Require `CareerNavigator/profile.md` and `tracker.json`. If missing, send user to **`/career-navigator:launch`**.

### 2. Opt-in and warning

- If **`interview-capture-settings.json`** does not exist or **`employer_warning_acknowledged`** is false: print the **employer policy warning**; on user acknowledgment, write the settings file.
- If user has not **opted in** to capture for this session, confirm before processing audio.

### 3. Match application

Identify **`application_id`** (or company + role) for the interview being logged. Match it against `tracker.json` → `applications[]` on `id`, falling back to each row's `previous_ids`. Hold onto the matched row's `detail_file`, `contacts_file`, and `application` label — the writes in step 5 need all three. If unknown, ask before writing tracker updates.

### 4. Transcription (STT)

- **Discover** tools: if the **`mcp-voice`** MCP exposes **`listen`**, invoke it to record the user speaking their recap aloud (prompt them to speak naturally). If the user has a pre-recorded audio file, ask for its path and note that `listen` records live — for file-based transcription, the user should paste the transcript manually.
- If **no** STT tools: fall back to **user-pasted transcript** or **`/career-navigator:interview-debrief`** when shipped; do **not** invent transcripts.

### 5. Structure and write tracker

From the transcript (user side only), extract:

- Overall tone / how it went
- Stage, participants (from user statements)
- Topics, surprises, red flags / positive signals
- Committed follow-ups
- Next-round or outcome hints

Write as a multi-file transaction, following the same patterns as **`track-application`**:

1. **Note** — append `{ "date": "YYYY-MM-DD", "text": "[capture] ..." }` to the detail file **`CareerNavigator/applications/<application_id>.json`** → `notes[]`. Never overwrite existing entries. Then set the summary row's **`notes_count`** to the new array length.
2. **Stage** — when the capture records an interview that is not yet in the detail file's `stage_history[]`, append the stage entry there (or populate `post_notes` on the matching existing entry). Then set the summary row's **`stage_count`**, **`latest_stage`**, and **`latest_stage_date`**, and update **`status`** if the stage moves it.
3. **Contacts** — if the user names interviewers, add or update them in **`CareerNavigator/contacts/<company-slug>.json`** with the row's `application` label on each entry, then recompute that file's `contact_count` and the summary row's `contact_count`. Set `contacts_file` on the row if it was absent.
4. **Row fields** — update **`next_step`** and **`follow_up_date`** on the `tracker.json` summary row when the user committed to a follow-up.

Load and re-dump each JSON file programmatically (`json.load` / `json.dump`, `indent=2`, `ensure_ascii=False`) and reload to verify. After the write, confirm `notes_count` and `stage_count` match the detail arrays and `latest_stage` matches the last `stage_history` entry.

### 6. Artifacts (optional)

Save transcript text to **`{user_dir}/CareerNavigator/interview-capture/`** as `{application_id}-{YYYY-MM-DD}-transcript.txt` if the user wants a file copy.

## Guardrails

- **Honest over encouraging** when summarizing performance.
- **No** multi-party recording claims; label transcript as **user channel only** when other speakers are quoted from user recall.
