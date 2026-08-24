---
name: interview-capture
description: >
  Opt-in post-interview capture: transcribe the user's own audio (user audio
  only), extract structured takeaways, and update tracker.json. Surfaces
  employer policy warning once; jurisdiction/retention per spec §13.1. Uses
  the local mcp-transcribe MCP (Whisper file STT) when available. Not an
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

Resolve a transcript in this order. Do **not** invent transcripts at any step.

1. **User already has a transcript** — use it. Skip transcription entirely.
2. **Recorded audio file + `mcp-transcribe` MCP available** — the normal path. Call **`transcribe_file`**:
   - Pass **`initial_prompt`** built at run time from the matched tracker row — company, role, and interviewer names from `contacts_file` — plus any product, project, or acronym likely to be spoken. Build this from the user's own data; never hardcode real names into this skill, which ships in a public repository. Cross-cutting terms the tracker does not carry can live in the server's gitignored `vocabulary.local.json` and be selected with `vocabulary_group`.
   - This is not optional. Whisper mangles unfamiliar proper nouns badly without it — expect vendor names to become common English words and surnames to become different surnames.
   - Call **`backend_info`** first only if a prior call failed; it distinguishes a bad file from a backend that never loaded.
3. **Recorded audio file, no MCP** — transcribe in the session sandbox with `faster-whisper`. One pass only, at the model you intend to ship:
   - `medium.en`, `compute_type="int8"`, `cpu_threads=<nproc>`. Roughly 2x realtime on 2 cores — budget ~11 min for a 25-min recording, and start it in the background while reading tracker and prep-brief files.
   - **`vad_filter=False`.** VAD drops speech at silence boundaries; on a real 23-minute screen it silently removed ~28 seconds including the interviewer's answer on process.
   - Seed `initial_prompt` exactly as in step 2.
   - Do **not** run a smaller model first as a recon pass, then re-run larger. That doubles the wall clock and produces nothing you keep.
4. **Live recap instead of a recording** — if the user wants to narrate rather than upload, that needs a live-mic tool. `mcp-transcribe` deliberately has none. Ask the user to record on their phone or Mac and give you the file path.
5. **Nothing available** — ask for a pasted transcript.

**Diarization:** none of these backends label speakers. Attribute turns from content — who asks vs. answers, self-references, names, dialect and idiom tells — and mark low-confidence passages in brackets rather than guessing silently.

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

### 6. Artifacts (required)

Both files below are part of the definition of done. Write them without being asked.

1. **Transcript** — `{user_dir}/CareerNavigator/interview-capture/{application_id}-{YYYY-MM-DD}-transcript.md`
   Speaker-labeled blocks (`**Name:** text`), not timecoded ASR segments. Header carries date, participants, stage, duration, a consent/scope note when the capture covers both channels, and an accuracy note explaining bracketed text. `## Topic: ...` headers where the conversation segments cleanly.
2. **Debrief** — `{user_dir}/interview-debrief/{company}_{interviewer-first-name}_{M.D.YY}.md`
   Five sections: Overall Assessment (with an honest likelihood-of-advancing call), What Went Well, What Could Have Gone Better, Role & Company Intelligence Gathered, Next Steps. Footer: generation date, source transcript path, prep brief path, next action.

Also fold the key intelligence into the matching `interview-prep/` brief as a **Debrief** section when one exists, so the next round starts from it.

## Guardrails

- **Honest over encouraging** when summarizing performance.
- **No** multi-party recording claims; label transcript as **user channel only** when other speakers are quoted from user recall. When the user explicitly authorizes a both-channel recording, say so in the transcript header and mark the file as private working material.
- **Never** deliver the debrief as chat prose instead of the file. The file is the deliverable.
