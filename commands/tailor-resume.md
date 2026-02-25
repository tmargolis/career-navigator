---
name: tailor-resume
command: /cn:tailor-resume
description: >
  Assembles the optimal resume for a specific role from the corpus, scores it
  for ATS compatibility, saves it to the artifact inventory, and optionally
  links it to an application record.
agent: resume-coach
skill: ats-optimization
---

# /cn:tailor-resume

Builds the best possible resume for a specific job from your experience corpus. Each resume is assembled — not copied — from the experience units most relevant to the target role, weighted by outcome history.

## Usage

```
/cn:tailor-resume
/cn:tailor-resume [company] [role title]
```

## Workflow

### 1. Get the job description

If not provided, ask:

> "Please share the job description. You can:
> - Paste the full JD text
> - Paste the job title, company, and key requirements if you don't have the full text"

The more complete the JD, the better the keyword targeting. If only partial info is provided, note that ATS scores may be lower.

### 2. Confirm corpus is ready

Check that `data/corpus/index.json` exists and has at least one experience unit. If not:
> "Your corpus is empty. Run /cn:add-source first to add your resume or experience."

### 3. Invoke resume-coach agent

Hand off to the **resume-coach** agent with:
- The full JD text
- The current corpus

The agent will:
1. Extract and rank keywords from the JD
2. Score each corpus unit against the JD by relevance and performance weight
3. Select the optimal set of units (targeting ~4–6 roles, 3–5 bullets each)
4. Assemble a structured resume (Contact → Summary → Skills → Experience → Education → Certifications)
5. Write a role-specific summary (2–3 sentences, keyword-targeted)
6. Apply the **ats-optimization** skill — score the assembled resume
7. Iterate if ATS score < 75 (adjust keywords and phrasing, re-score)
8. Save the artifact to `data/artifacts/`

### 4. Report results

After the agent completes:

```
RESUME ASSEMBLED
────────────────────────────────────────
Role:         [Job title] at [Company]
ATS score:    [X]/100
Saved to:     data/artifacts/[filename]

Keywords matched: [list]
Keywords missing: [list — only show if any]

Experience units used: [N] of [total in corpus]
```

### 5. Offer next steps

> "What would you like to do next?
> - Track this as an application (/cn:track-application)
> - Generate a cover letter (/cn:cover-letter)
> - Review the resume with me before submitting
> - Save to cloud storage (requires connector — see CONNECTORS.md)"

## Notes

- Every resume artifact records which experience units it used (`source_units[]`). This provenance enables the insight engine to learn which units correlate with positive outcomes.
- If you have already applied and have outcome data, the agent prioritizes units with higher performance weights.
- The assembled resume is saved as Markdown. For submission, convert to `.docx` or export to PDF with a text layer.
