---
name: add-source
command: /cn:add-source
description: >
  Adds a source document (resume, CV, portfolio) to the resume corpus.
  Extracts experience units, normalizes skill tags, and makes the content
  available for future tailored resume assembly.
agent: resume-coach
---

# /cn:add-source

Adds a source document to your resume corpus. The corpus is not a collection of resumes — it's a structured pool of experience units that can be recombined to build the optimal resume for any specific role.

## Usage

```
/cn:add-source
/cn:add-source [file path]
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
- Append all units and the source document record to `data/corpus/index.json`

If `data/corpus/index.json` doesn't exist, the agent initializes it from `data/corpus/index.json.template`.

### 3. Confirm addition

Report back with:
- Number of experience units extracted
- Skill tags identified (list the top 10 most relevant)
- Total corpus size after addition (unit count and skill count)

Example confirmation:
> "Added 23 experience units from resume.pdf. I found skills including: Python, data analysis, stakeholder management, Agile, SQL, Tableau, cross-functional leadership, and 14 others. Your corpus now contains 23 units covering 21 skills."

### 4. Suggest next step

If this is the first source document:
> "Your corpus is ready. You can now run /cn:tailor-resume with a job description to generate your first targeted resume."

If corpus already had content:
> "Corpus updated. If any of the new content is more recent than existing units for the same roles, it will be preferred in future assemblies."

## Notes

- You can add multiple source documents — the corpus accumulates all of them
- Adding duplicates is safe; the agent will note overlap but won't double-count units
- Performance weights start at 1.0 and are adjusted over time by the insight engine as application outcome data accumulates
