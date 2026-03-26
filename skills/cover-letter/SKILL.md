---
name: cover-letter
description: >
  Produces a targeted cover letter via a CoverLetterBrief and writer
  final prose—honest, specific, voice-matched. Saves to the artifact inventory.
  Fires after tailoring or on request. Also /career-navigator:cover-letter.
triggers:
  - "write a cover letter"
  - "cover letter for"
  - "draft a cover letter"
  - "generate a cover letter"
  - "I need a cover letter"
  - "/cover-letter"
  - "cover letter for this role"
  - "cover letter for this job"
---

Build a **CoverLetterBrief**, then invoke **`writer`** for final letter prose. Do not write the full letter in this skill—**`writer`** owns send-ready copy.

## Workflow

### 1. Collect inputs

**Job description** — required. If not already in context, ask the user to provide it.

**Tailored resume** — check `{user_dir}/CareerNavigator/artifacts-index.json` for a resume artifact for this company and role. If one exists, use it as the primary source for experience framing. If none exists:
> "I don't see a tailored resume for this role yet. Want me to tailor one first, or build the brief from your ExperienceLibrary directly?"

**Profile** — read `{user_dir}/CareerNavigator/profile.md` for differentiators, tone preferences, and any standing instructions.

**Contact context** — check `tracker.json` for any known contacts at the company. If a contact is present, note it for the brief (do not draft named flattery unless accurate).

### 2. Research the company

Before briefing, identify 1–2 **specific, verifiable** things about the company relevant to fit:
- Recent product launches, initiatives, or strategic direction
- Team/culture signals from the JD
- Notes in `tracker.json` or profile about this company

Do not use generic praise. If no specific signals, say so in the brief—**`writer`** will omit flattery.

### 2.5 Voice preflight (before the brief)

Read `{user_dir}/CareerNavigator/voice-profile.md`.

- If there is **no** user-pasted block under **`## User writing samples`** or **`## User writing samples (launch)`** (substantive excerpts), **ask before** building the CoverLetterBrief:

> "Before I draft your cover letter: paste **2–5 recent LinkedIn posts** or other short professional writing so **`writer`** can match your voice. I may already have **launch voice harvest** hints (résumés/CVs/cover letters scanned during **`/career-navigator:launch`**)—LinkedIn still sharpens tone. Reply **skip** for a neutral tone (**low** voice match) if you’re fine with harvest-only signal."

- If the user **pastes** samples, append a dated **`## User writing samples`** section to `voice-profile.md` (trimmed excerpts + one-line source note).
- If the user says **skip**, continue and pass **`voice_match: low`** intent into the brief for **`writer`**.

If either **`## User writing samples`** or **`## User writing samples (launch)`** already has substantive pasted excerpts, skip this ask.

### 3. Build CoverLetterBrief (no full letter here)

Assemble a structured brief for **`writer`**:

```markdown
## CoverLetterBrief
- **company**: …
- **role**: …
- **opening_hook_facts**: bullet list (why this role+company—facts only)
- **core_case_bullets**: 4–8 bullets mapping EL achievements to JD competencies (each bullet: fact + metric if any)
- **close_intent**: one line (conversation, not desperation)
- **tone**: confident, direct; honest-over-encouraging
- **banned**: padding, unverified claims, generic “innovative leader” phrasing
- **mirrored_jd_terms**: list keywords to include naturally (ATS)
- **length_target**: 3–4 short paragraphs, <400 words
- **optional_contact_reference**: name/role only if in tracker and user confirmed
```

### 4. Invoke writer

- Use the exact agent name **`writer`** with mode **`cover-letter`**. Pass the full **CoverLetterBrief** and paths to **`voice-profile.md`** / **`profile.md`**. Retry once on failure.

### 5. Present and confirm

Show the letter from **`writer`** in full. Ask:
> "Does this look right? I can ask writer to adjust tone, swap examples, or shorten."

### 6. Save the artifact

After confirmation, save the letter (the **`writer`** output).

**Filenames (avoid host / MCP validation errors):** use **ASCII-safe** names only—hyphens `-`, no em dashes or smart quotes. **Sanitize** company and role: remove `\ / : * ? " < > |` and newlines; collapse whitespace; limit basename length (~100 chars).  
**Example:** `Anthropic-PM-Claude-Code-Cover-Letter-2026-03-24.md`

- **Filename format:** `{SanitizedCompany}-{SanitizedRole}-Cover-Letter-{YYYY-MM-DD}.md`
- **Path:** `{user_dir}/` (same path style the host expects—usually relative to the attached job-search folder)
- **Write the markdown file in its own tool call**; **update `artifacts-index.json` in a separate call** with valid JSON (escape `"` inside strings).

**If the file tool fails** (e.g. MCP `-32602` / invalid args): **do not** create a file whose name is the error message. Output the **full letter** in a fenced markdown code block and tell the user to save manually; still update `artifacts-index.json` only if the file was saved successfully.
- **Write to `{user_dir}/CareerNavigator/artifacts-index.json`**:

```json
{
  "id": "{uuid}",
  "type": "cover_letter",
  "filename": "{filename}",
  "path": "{user_dir}/{filename}",
  "target_company": "{company}",
  "target_role": "{role}",
  "date_created": "{today}",
  "source": "generated",
  "linked_resume": "{filename of tailored resume if used, else null}",
  "notes": "Assembled via CoverLetterBrief + writer"
}
```

If other artifact files (PDF/DOCX) exist in `{user_dir}`, run the **`artifact-saved`** workflow once after saving.

Confirm:
> "Saved as **{filename}**."

### 7. Suggest next step

If the user has not yet logged an application for this role:
> "Ready to track this application? Say 'yes' or `/career-navigator:track-application`."
