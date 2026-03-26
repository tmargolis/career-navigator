---
name: add-source
description: >
  Ingests a resume, CV, or portfolio document into the ExperienceLibrary.
  Extracts structured experience units and merges them into CareerNavigator/ExperienceLibrary.json.
  Fires when the user uploads or references a new source document. Also
  invocable via /career-navigator:add-source.
triggers:
  - "add this resume"
  - "add my resume"
  - "add this CV"
  - "ingest this document"
  - "add to my ExperienceLibrary"
  - "add a source"
  - "/add-source"
  - "here's my resume"
  - "upload my resume"
  - "I have a new resume"
  - "I have another resume"
  - "add this to the ExperienceLibrary"
---

Extract structured experience units from a source document and merge them into the user's ExperienceLibrary.

## Workflow

### 1. Identify the source document

**If the user has provided a file path or uploaded a document** — use it directly.

**If no document is in context**, ask:
> "Which file should I add? Provide the path or paste the content directly."

Supported formats: PDF, DOCX, TXT, MD, plain text paste.

### 2. Read the current ExperienceLibrary

Read `{user_dir}/CareerNavigator/ExperienceLibrary.json`. Note:
- Existing unit IDs (to avoid collisions)
- Existing companies and roles (to detect duplicates)

If the file does not exist, create it with an empty `units` array before proceeding.

### 3. Extract experience units

Read the source document in full. For each distinct role, education entry, publication, award, or recognition, extract a structured unit:

```json
{
  "id": "exp-{next_available_number}",
  "type": "role",
  "company": "...",
  "title": "...",
  "dates": "...",
  "summary": "1–2 sentence description of scope and context",
  "achievements": [
    {
      "id": "exp-{n}-a1",
      "theme": "impact | leadership | technical | commercial | operational",
      "text": "exact achievement text, preserved from source"
    }
  ],
  "skills": ["skill1", "skill2"],
  "performance_weight": 0.5,
  "source_document": "{filename of source}"
}
```

**Extraction rules:**
- Preserve achievement text as written — do not rephrase or improve at ingest time. Tailoring happens at resume assembly.
- Assign a `theme` to each achievement based on what it primarily demonstrates.
- Extract skills as they appear — normalize capitalization but do not rename or merge technologies.
- Set `performance_weight` to 0.5 (neutral) for all new units. The analyst agent adjusts weights from outcomes.

### 4. Check for duplicates

Before appending, check each extracted unit against existing ExperienceLibrary entries:
- Same company + overlapping date range = likely duplicate
- If a likely duplicate is found, surface it:
> "I see an existing entry for {Role} at {Company} ({dates}) in your ExperienceLibrary. Should I replace it, merge the achievements, or add this as a separate entry?"

### 5. Merge into ExperienceLibrary

Append the new units to the `units` array in `CareerNavigator/ExperienceLibrary.json`. Update the `meta.updated` field to today's date.

Also add the source document to `artifacts-index.json` if it is not already listed:

```json
{
  "id": "{uuid}",
  "type": "resume",
  "filename": "{filename}",
  "path": "{full path}",
  "target_company": null,
  "target_role": null,
  "date_created": "{file date or today}",
  "source": "existing",
  "notes": "Source document added to ExperienceLibrary"
}
```

### 6. Confirm

```
Added to ExperienceLibrary: {n} experience unit(s) from {filename}
  {Role} at {Company} ({dates})
  {Role} at {Company} ({dates})
  ...

ExperienceLibrary total: {total unit count} units
```

If duplicates were merged or skipped, note that inline. Keep the confirmation concise.
