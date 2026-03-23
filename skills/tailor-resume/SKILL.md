---
name: tailor-resume
description: >
  Assembles an optimized resume for a specific role from the ExperienceLibrary,
  scores it for ATS compatibility, and saves it to the artifact inventory.
  Fires automatically when the user shares or pastes a job description, or
  expresses intent to apply to a specific role. Also invocable via
  /career-navigator:tailor-resume.
triggers:
  - "tailor my resume"
  - "tailor resume for"
  - "customize my resume"
  - "optimize my resume for"
  - "I want to apply to"
  - "I'm applying to"
  - "help me apply for"
  - "write a resume for"
  - "build a resume for"
  - "here's the job description"
  - "here's a JD"
  - "I found a job posting"
---

Assemble the best possible resume for a specific role, drawn from the user's ExperienceLibrary. Invoke the `resume-coach` agent to do the work.

## Workflow

### 1. Collect inputs

**Job description** — required. If the user has not provided one:
> "Paste the job description and I'll tailor your resume for it."

**Target role and company** — extract from the JD if not stated explicitly.

**ExperienceLibrary** — read `{user_dir}/CareerNavigator/ExperienceLibrary.json`. If the file is missing or the `units` array is empty:
> "Your ExperienceLibrary is empty. Run `/career-navigator:add-source` to add a resume first, then I can tailor one for this role."

**Profile** — read `{user_dir}/CareerNavigator/profile.md` for differentiators, skills, and target preferences. Do not ask the user for anything that is already in the profile.

### 2. Invoke resume-coach

Hand off to the `resume-coach` agent with:
- The full job description text
- The full ExperienceLibrary (`CareerNavigator/ExperienceLibrary.json`)
- The user profile (`CareerNavigator/profile.md`)
- Any specific instructions the user provided (emphasis, exclusions, tone)

`resume-coach` will:
- Select the most relevant experience units using `performance_weights`
- Assemble and rewrite them for the target role
- Ensure all required JD keywords are present (ATS pass)
- Return the completed resume text and an ATS score

### 3. Score and review

Present the full assessment returned by `resume-coach` before saving:

```
Resume assembled for {Role} at {Company}

ATS score: {n}/100
Keyword coverage: {matched_keywords} / {total_required} must-have keywords matched

Strengths
- {What the ExperienceLibrary covers well for this role}

Gaps (honest)
- {Requirements with no or weak ExperienceLibrary coverage}
- {Achievements that need metrics or sharpening}
```

If the score is below 70, ask before saving:
> "This resume scores {n}/100 for ATS. The main gaps are {keywords}. Do you want me to address them before saving?"

### 4. Save the artifact

Once the user confirms (or if the score is ≥ 70 with no gaps flagged), save the resume:

- **Filename format**: `{Company} — {Role Title} Resume ({YYYY-MM-DD}).md`
- **Path**: `{user_dir}/`
- **Write to `{user_dir}/CareerNavigator/artifacts-index.json`**:

```json
{
  "id": "{uuid}",
  "type": "resume",
  "filename": "{filename}",
  "path": "{user_dir}/{filename}",
  "target_company": "{company}",
  "target_role": "{role}",
  "date_created": "{today}",
  "source": "generated",
  "ats_score": {n},
  "source_units": ["{unit_ids used}"],
  "jd_keywords": ["{keywords matched}"],
  "notes": ""
}
```

Confirm to the user:
> "Saved as **{filename}**. Run `/career-navigator:cover-letter` to generate a matching cover letter."

### 5. Suggest next step

If the user hasn't already logged an application for this role, prompt:
> "Want me to add this to your tracker? Just say 'yes' or tell me the application details."
