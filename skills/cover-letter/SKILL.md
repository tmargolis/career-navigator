---
name: cover-letter
description: >
  Generates a targeted cover letter for a specific role, drawing on the tailored
  resume, company research, and any known contact context. Saves to the artifact
  inventory. Fires automatically after a resume is tailored, or when the user
  explicitly requests a cover letter for a specific job. Also invocable via
  /career-navigator:cover-letter.
triggers:
  - "write a cover letter"
  - "cover letter for"
  - "draft a cover letter"
  - "generate a cover letter"
  - "I need a cover letter"
  - "cover letter for this role"
  - "cover letter for this job"
---

Generate a targeted, honest cover letter for a specific role. Do not pad, flatter, or overstate. The letter should read like a clear-eyed professional making a specific case — not a template with names swapped in.

## Workflow

### 1. Collect inputs

**Job description** — required. If not already in context, ask the user to provide it.

**Tailored resume** — check `{user_dir}/CareerNavigator/artifacts-index.json` for a resume artifact for this company and role. If one exists, use it as the primary source for experience framing. If none exists:
> "I don't see a tailored resume for this role yet. Want me to tailor one first, or write the cover letter from your ExperienceLibrary directly?"

**Profile** — read `{user_dir}/CareerNavigator/profile.md` for differentiators, tone preferences, and any standing instructions.

**Contact context** — check `tracker.json` for any known contacts at the company. If a contact is present, offer to reference them:
> "I see {Name} at {Company} is in your tracker. Should I reference your connection in the letter?"

### 2. Research the company

Before writing, identify 1–2 specific, concrete things about the company that are genuinely relevant to why the user is a strong fit:
- Recent product launches, initiatives, or strategic direction
- Known team structure or culture signals from the JD itself
- Any notes in `tracker.json` or the user profile about this company

Do not use generic praise ("innovative company", "exciting mission"). If no specific signals are available, omit company-specific flattery entirely and focus on the role itself.

### 3. Write the letter

Structure:
1. **Opening** — specific reason this role and company, not just any job. One sentence max.
2. **Core case** — 2–3 paragraphs. Each makes one concrete point supported by a specific achievement from the ExperienceLibrary. Mirror JD language where it is authentic.
3. **Close** — brief, direct. Express interest in a conversation. Do not beg or hedge.

Tone: confident and specific. Honest-over-encouraging applies here too — do not claim enthusiasm the user hasn't expressed.

Length: 3–4 short paragraphs. Under 400 words.

### 4. Present and confirm

Show the letter in full before saving. Ask:
> "Does this look right? I can adjust the tone, swap in different examples, or cut it shorter."

### 5. Save the artifact

After confirmation, save the letter:

- **Filename format**: `{Company} — {Role Title} Cover Letter ({YYYY-MM-DD}).md`
- **Path**: `{user_dir}/`
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
  "notes": ""
}
```

If other artifact files (PDF/DOCX) exist in `{user_dir}`, run the **`artifact-saved`** workflow once after saving so `artifacts-index.json` stays aligned with disk.

Confirm:
> "Saved as **{filename}**."

### 6. Suggest next step

If the user has not yet logged an application for this role:
> "Ready to track this application? Say 'yes' or `/career-navigator:track-application`."
