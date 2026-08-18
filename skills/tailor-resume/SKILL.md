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
  - "/tailor-resume"
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

**Verify the JD against the canonical source — always.** Before handing anything to `resume-coach`, fetch the posting from the company's own careers page or ATS (Greenhouse, Lever, Ashby, Workday, SmartRecruiters). Aggregator listings — Indeed, LinkedIn, Ladders, ZipRecruiter, Jobgether, BuiltIn — are frequently truncated, stale, or reworded, and any `job_link` stored in `recommendations.json` may point at one.

How to find the canonical post: search `{Company} {Role} careers` or `{Company} greenhouse OR lever OR ashby {Role}`, then fetch it. If the aggregator link is a shortlink (e.g. `to.indeed.com/...`), it will usually not resolve to usable text — go find the real posting instead of retrying the fetch.

Then diff the canonical JD against whatever the user or `recommendations.json` supplied, and **flag every contradiction to the user before building the resume**. Report them plainly:

> "The full JD on {source} differs from the listing we had on file: {contradiction}. That changes {what it changes}. Want me to proceed on the canonical version?"

Contradictions that matter most, because they change targeting or disqualify the role:

- **People-management scope** — "lead a team of PMs" vs. an IC/individual-contributor framing
- **Seniority or title** — Director vs. Senior PM vs. Principal
- **Location and work model** — onsite/hybrid/remote, and which office
- **Compensation band** — especially where a pay-transparency disclosure appears only on the canonical post
- **Hard requirements** — degree filters, years of experience, clearance, work authorization
- **Required application materials** — essays, work samples, portfolios, take-homes that aggregators drop entirely

If a contradiction invalidates the original fit rationale, say so directly and correct the stored `fit_signals` or `gaps` in `recommendations.json` — do not let a wrong signal survive into the tracker. If the canonical posting cannot be found or fetched, tell the user the JD is unverified and name the specific risk, rather than proceeding silently.

**Target role and company** — extract from the canonical JD if not stated explicitly.

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

**Voice-aligned Summary (optional):** If the user explicitly asks to match their **LinkedIn voice** / **`voice-profile.md`** for the **Summary only**, ask `resume-coach` for a **ResumeSummaryBrief** per `agents/resume-coach/AGENT.md`. **Before** invoking **`writer`**, run the same **voice preflight** as **`draft-outreach`** (ask for **`## User writing samples`** / **`## User writing samples (launch)`** or **skip**). Then invoke **`writer`** in **`resume-summary`** mode, substitute the returned **## Summary** into the draft, then continue to ATS presentation below.

### 3. Score and review

Present the full assessment returned by `resume-coach` before saving:

```
Resume assembled for {Role} at {Company}
JD source: {canonical URL} {(verified against the listing on file | CONTRADICTIONS FOUND — see below)}

ATS score: {n}/100
Keyword coverage: {matched_keywords} / {total_required} must-have keywords matched

JD contradictions (omit this block if none)
- {What the listing on file said} → {what the canonical JD actually says} → {what it changes}

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

**Filenames (avoid host / MCP validation errors):** use **ASCII-safe** names only—hyphens `-`, no em dashes or smart quotes. **Sanitize** company and role: remove `\ / : * ? " < > |` and newlines; collapse whitespace; limit basename (~100 chars).
**Example:** `Anthropic-PM-Claude-Code-Resume-2026-03-24.md`

- **Filename format:** `{SanitizedCompany}-{SanitizedRole}-Resume-{YYYY-MM-DD}.md`
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
  "jd_source_url": "{canonical careers-page or ATS URL the JD was verified against}",
  "notes": "{record any JD contradictions found during verification}"
}
```

If other artifact files (PDF/DOCX) exist in `{user_dir}`, run the **`artifact-saved`** workflow once after saving so `artifacts-index.json` stays aligned with disk.

Confirm to the user:
> "Saved as **{filename}**. Run `/career-navigator:cover-letter` to generate a matching cover letter."

### 5. Suggest next step

If the user hasn't already logged an application for this role, prompt:
> "Want me to add this to your tracker? Just say 'yes' or tell me the application details."
