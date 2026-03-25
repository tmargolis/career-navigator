---
name: list-artifacts
description: >
  Lists all generated artifacts in the artifact inventory with metadata: type,
  date created, target role and company, ATS score if available, and linked
  application outcome if known. Fires when the user asks to see their generated
  documents or artifact history. Also invocable via /career-navigator:list-artifacts.
triggers:
  - "list my artifacts"
  - "show my artifacts"
  - "what have I generated"
  - "what resumes have I created"
  - "show my resumes"
  - "list my cover letters"
  - "what documents have I made"
  - "show my generated documents"
  - "what's in my artifact inventory"
  - "what have I created"
---

Display the user's artifact inventory in a readable format.

## Workflow

### 1. Read the inventory

Read `{user_dir}/CareerNavigator/artifacts-index.json`. If the file does not exist or the `artifacts` array is empty:
> "No artifacts yet. Run `/career-navigator:tailor-resume` for a resume, or `/career-navigator:content-suggest` and ask for a full post draft to save a LinkedIn draft to disk."

### 2. Cross-reference with tracker

Read `{user_dir}/CareerNavigator/tracker.json`. For each artifact, check whether it appears in any application's `artifacts[]` array. If so, note the application's current `status` — this lets the user see which resumes and cover letters are attached to live applications and what outcome (if any) they produced.

### 3. Organize the output

Group artifacts by type: **resumes** first, then **cover letters**, then **`linkedin_post`** (saved post drafts from **`writer`**), then any other types. Within each group, sort by `date_created` descending (most recent first).

**Format for each artifact:**

```
{n}. {filename}
   Target:   {Company} — {Role}  (or "Base / unattached" if no target; for linkedin_post use "—" or notes topic)
   Created:  {date_created}
   ATS score: {ats_score}/100  (omit if not available or not applicable)
   Used in:  {Company — Role, status: {status}}  (omit if not linked to any application)
```

For **`type: "linkedin_post"`**, omit ATS and usually **Used in**; show **`notes`** or path if helpful so the user can find the draft on disk.

**Summary line at the top** (before the list):

```
Artifacts: {total_resume_count} resume(s), {total_cover_letter_count} cover letter(s), {total_linkedin_post_count} LinkedIn post draft(s)
```

### 4. Offer next steps

After the list, show relevant actions based on what's there:

- If there are resumes with no linked application:
  > "Some resumes aren't linked to an application yet — run `/career-navigator:track-application` to log them."
- If there are no cover letters for roles that have resumes:
  > "No cover letter on file for some roles — run `/career-navigator:cover-letter` to generate one."
- If the list is empty: omit this section entirely.
