---
name: resume-score
description: >
  Scores a resume against a job description for ATS keyword match, formatting
  compliance, and narrative strength. Fires when the user shares a resume
  alongside a job description without explicitly requesting tailoring, or
  explicitly asks for a score. Also invocable via /career-navigator:resume-score.
triggers:
  - "score my resume"
  - "score this resume"
  - "how does my resume score"
  - "check my resume against"
  - "rate my resume"
  - "evaluate my resume"
  - "ATS score"
  - "how does this resume match"
  - "resume check"
  - "how well does my resume match"
---

Score a resume against a job description. Be candid — a low score is useful information, not something to soften.

Invoke the `resume-coach` agent to perform the scoring analysis.

## Workflow

### 1. Collect inputs

**Resume** — required. Accept:
- A file path to an existing document in `{user_dir}`
- An artifact name from `artifacts-index.json` (look up by filename)
- Content pasted directly into the conversation

**Job description** — required. If not provided:
> "Paste the job description to score against."

If the user only provided a resume with no JD, and there is an active role in context (e.g., from a recent `search-jobs` result or tracker entry), ask:
> "Which job description should I score this against?"

### 2. Invoke resume-coach

Pass the resume text and JD to `resume-coach` for analysis. The agent evaluates:

**ATS keyword match**
- Required keywords: terms that appear in the JD's requirements section (skills, tools, certifications, titles)
- Preferred keywords: terms that appear elsewhere in the JD (nice-to-haves, cultural language)
- Match count and percentage for each category

**Formatting compliance**
- No tables, headers in unusual locations, columns, or other ATS-hostile structures
- Contact info in expected location
- Standard section headings (Experience, Education, Skills)
- No images, graphics, or non-standard fonts

**Narrative strength**
- Summary/objective is specific and role-targeted (not generic)
- Achievements are quantified where possible
- Most recent and relevant experience is appropriately weighted
- No excessive jargon or buzzwords without substance

### 3. Present the score

```
**Resume Score** — {Resume filename} vs. {Company/Role or "provided JD"}

Overall: {n}/100

ATS keyword match    {n}/40
  Required:  {matched}/{total} keywords  ({%})
  Preferred: {matched}/{total} keywords  ({%})

Formatting          {n}/30
  {pass/flag per check, one line each}

Narrative strength  {n}/30
  {2–3 sentences of candid assessment}

---
Top gaps to address
1. {Missing keyword or structural issue} — {why it matters}
2. ...
3. ...
```

Cap the gaps list at 5. Order by impact on ATS pass rate first, narrative second.

### 4. Offer next steps

After the score, offer:
> "Want me to tailor a new version of this resume for the role? Run `/career-navigator:tailor-resume` or just say 'tailor it'."

Do not automatically trigger tailoring — scoring and tailoring are distinct operations. Let the user decide.
