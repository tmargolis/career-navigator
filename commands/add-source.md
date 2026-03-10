---
name: add-source
command: /career-navigator:add-source
description: >
  Adds a source document (resume, CV, portfolio) to the resume corpus.
  Extracts experience units, normalizes skill tags, and makes the content
  available for future tailored resume assembly.
agent: resume-coach
---

# /career-navigator:add-source

## Preflight

Before doing anything else, resolve `{user_dir}` by reading the Career Navigator config (`~/Library/Application Support/Claude/cowork_plugins/career-navigator/config.json` on macOS, `~/.config/Claude/cowork_plugins/career-navigator/config.json` on Linux). If the config is missing or `user_dir` is empty, ask:
> "It looks like Career Navigator hasn't been set up yet. What folder would you like to use for your job search? Share the path and I'll get everything configured."
Then run through `/career-navigator:setup` with that path before continuing.

---

Adds a source document to your resume corpus. The corpus is not a collection of resumes — it's a structured pool of experience units that can be recombined to build the optimal resume for any specific role.

## Usage

```
/career-navigator:add-source
/career-navigator:add-source [file path]
```

## Workflow

### 1. Get the source document

If a file path was provided, acknowledge it. Otherwise, prompt:

> "Please share your resume or source document. You can:
> - Paste the content directly into the chat
> - Provide a file path (e.g., `/Users/you/Documents/resume.docx`)"

If a file path is given, read the file. If Claude cannot access the file, ask the user to paste the content instead.

### 2. Invoke resume-coach agent

Hand off to the **resume-coach** agent with the source content. The agent will:
- Extract individual experience units (roles, bullets, achievements, projects, education, certifications)
- Assign normalized skill tags to each unit
- Assign default performance weights (1.0)
- Append all units and the source document record to `{user_dir}/corpus/index.json`

If `{user_dir}/corpus/index.json` doesn't exist, the agent initializes it from `templates/corpus.json.template`.

### 3. Record the source document in the artifact index

The source document is already in the user's job search directory — do not copy or re-save it. Just record it in `{user_dir}/artifacts-index.json` (initialize from `templates/artifacts.json.template` if the file doesn't exist yet):
```json
{
  "artifact_id": "[uuid]",
  "type": "Source Resume",
  "application_id": null,
  "source_units": ["[all unit IDs extracted from this document]"],
  "jd_keywords": null,
  "ats_score": null,
  "created_at": "[timestamp]",
  "storage_path": "{user_dir}/[filename]",
  "source_filename": "[original filename, or 'pasted-content' if pasted]"
}
```

### 4. Confirm addition

Report back with:
- Number of experience units extracted
- Skill tags identified (list the top 10 most relevant)
- Total corpus size after addition (unit count and skill count)

Example confirmation:
> "Added 23 experience units from resume.pdf. I found skills including: Python, data analysis, stakeholder management, Agile, SQL, Tableau, cross-functional leadership, and 14 others. Your corpus now contains 23 units covering 21 skills."

### 5. Suggest next step

If this is the first source document:
> "Your corpus is ready. You can now run /career-navigator:tailor-resume with a job description to generate your first targeted resume."

If corpus already had content:
> "Corpus updated. If any of the new content is more recent than existing units for the same roles, it will be preferred in future assemblies."

## Notes

- You can add multiple source documents — the corpus accumulates all of them
- Adding duplicates is safe; the agent will note overlap but won't double-count units
- Performance weights start at 1.0 and are adjusted over time by the insight engine as application outcome data accumulates
