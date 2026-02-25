---
name: cover-letter
command: /cn:cover-letter
description: >
  Generates a targeted cover letter for a specific role. Draws on the tailored
  resume artifact if it exists, conducts company research, and links to the
  application record if one is active.
agent: resume-coach
---

# /cn:cover-letter

Generates a targeted cover letter for a specific role. A good cover letter does not summarize the resume — it makes a specific argument for why you are the right person for this role, in this company, at this moment.

## Usage

```
/cn:cover-letter
/cn:cover-letter [company] [role title]
```

## Workflow

### 1. Gather inputs

Ask for anything not already provided:

> "To write a strong cover letter, I need:
> 1. The company name and role title
> 2. The job description (or key requirements)
> 3. Anything you know about the company, team, or role that isn't in the JD (optional but valuable)
> 4. The name of the hiring manager or recruiter, if known"

If a tailored resume artifact already exists for this role in `data/artifacts/index.json`, use it as the source of selected experience units. If not, assemble one first (runs tailor-resume workflow internally).

### 2. Research the company

Before drafting, perform or ask the user to provide:
- What the company actually does (not just their marketing description)
- Recent news, product launches, or challenges (anything in the last 6–12 months)
- The team or department context for this role
- The company's apparent culture signals (from JD language, Glassdoor, or public statements)

Use this research to make the letter specific. Generic cover letters are immediately obvious and largely ignored.

### 3. Draft the cover letter

Structure:

**Opening paragraph** (2–3 sentences):
- State the role you're applying for
- Lead with a specific, substantive hook — a result you achieved, a problem you've solved that's directly relevant, or a concrete reason you're drawn to this company (not "I've always admired your values")
- Avoid: "I am writing to express my interest in..." — this is a waste of the reader's first impression

**Middle paragraph(s)** (1–2 paragraphs):
- Make 2–3 specific claims about fit, each backed by a concrete example from the corpus
- Reference JD language where it matches your experience — this signals attention and helps ATS
- Address any obvious tension head-on if it exists (career pivot, unconventional background) — ignoring it doesn't make it invisible

**Closing paragraph** (2–3 sentences):
- Restate enthusiasm specifically (why this company, this role, this moment)
- State a clear next step ("I'd welcome the opportunity to discuss...")
- No "Thank you for your consideration" as the final sentence — end with energy, not deference

**Length**: 3–4 paragraphs. Never more than one page. Recruiters read cover letters in 30 seconds or not at all.

### 4. Save the artifact

Save the cover letter to `data/artifacts/[company]-[role]-cover-letter-[timestamp].md`.

Append to `data/artifacts/index.json`:
```json
{
  "artifact_id": "[uuid]",
  "type": "Cover Letter",
  "application_id": "[linked application UUID, or null]",
  "source_units": ["[unit IDs referenced in the letter]"],
  "jd_keywords": ["[keywords targeted]"],
  "ats_score": null,
  "created_at": "[timestamp]",
  "storage_path": "data/artifacts/[filename]"
}
```

Note: Cover letters are not ATS-scored (most ATS systems parse resumes only). `ats_score` is null.

### 5. Link to application record

If an application record exists for this company + role in `tracker.json`, add this artifact's ID to `artifacts_used[]`.

If no application record exists:
> "Would you like to log this as an application? Run /cn:track-application to track it."

### 6. Review prompt

After drafting:
> "Here's the cover letter. Read it as a skeptic: does every sentence earn its place? Is the hook strong enough to keep reading? Let me know what you'd like to change."
