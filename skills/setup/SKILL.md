---
name: setup
description: >
  The single entry point for all Career Navigator configuration. Sets up the
  job search folder, builds the user profile, ExperienceLibrary and application tracker from existing documents,
  configures JobSearch for live job search, and optionally connects Google Drive.
  No Customize button required — run this command to do everything.
triggers:
  - "launch career"
  - "set up career"
  - "set up career navigator"
  - "configure career navigator"
  - "get started with career navigator"
---

Use this after installing the plugin — it handles everything: registering your job search folder, reading your existing documents, building your profile and ExperienceLibrary, and configuring integrations. 

The working directory (or relevant sub-directory) should be configured as the user's job search directory to be referred to as `{user_dir}`. All data this plugin produces— profile, ExperienceLibrary, tracker, generated artifacts — lives in subdirectories of the `{user_dir}` folder alongside the user's raw documents.

## Workflow

### 1. Confirm job search directory

**If the user provided a directory path**: use it. inform the user of the path to `{user_dir}`

**If no path was provided**: ask:
> "What folder should Career Navigator use for your job search? This is where your resumes and cover letters live, and where I'll save everything I generate. Start a new chat and click the "+" icon in the text box to add that folder to our chat"

### 2. Check for existing data files

After confirming `{user_dir}`, check whether each of the four core data files exists. Handle each independently.

#### Files to check

| File | Path |
|---|---|
| Profile | `{user_dir}/CareerNavigator/profile.md` |
| ExperienceLibrary | `{user_dir}/CareerNavigator/ExperienceLibrary.json` |
| Tracker | `{user_dir}/CareerNavigator/tracker.json` |
| Artifacts index | `{user_dir}/CareerNavigator/artifacts-index.json` |

#### For each file: two paths

**If the file exists** — validate its format and content:

- **`CareerNavigator/profile.md`**: Must contain sections for target roles, compensation floor, location, and key differentiators. If any section is missing or empty, fill it in from other available sources (ExperienceLibrary, resume documents in `{user_dir}`). Inform the user of any gaps found and how they were resolved.

- **`CareerNavigator/ExperienceLibrary.json`**: Must be valid JSON with a `meta` object and a non-empty `units` array. Each unit must have `id`, `type`, `company` (or `institution`), `title`, and `dates`. Flag any units missing required fields and prompt the user to supply them. If the array is empty, treat the file as missing and rebuild it.

- **`CareerNavigator/tracker.json`**: Must be valid JSON with `meta`, `applications` array, and `pipeline_summary`. Each application entry must have at minimum `id`, `company`, `role`, and `status`. Recalculate `pipeline_summary` counts from the actual `applications` array and update if stale.

- **`artifacts-index.json`**: Must be valid JSON with a `meta` object and an `artifacts` array. Cross-check the listed artifact filenames against files actually present in `{user_dir}`. Remove entries for files that no longer exist. Add entries for PDF/DOCX files found in `{user_dir}` that are not yet indexed.

After validation, report to the user:
> - What was found and whether it passed validation
> - Any corrections made automatically
> - Any gaps that need the user's input

**If the file does not exist** — create it from documents in `{user_dir}`:

1. Scan `{user_dir}` (non-recursively) for readable documents: PDF, DOCX, TXT, MD files.
2. Read each document and extract relevant content.
3. Build the missing file(s) following the schemas below.
4. Create any missing subdirectories (`profile/`, `tracker/`) before writing.
5. Inform the user which documents were used and what was created.

If no source documents exist in `{user_dir}` at all, create minimal placeholder files and prompt the user to add their resume:
> "I didn't find any resumes or documents in your job search folder. Add a resume (PDF or DOCX) and run `/career-navigator:setup` again to build your profile and ExperienceLibrary."

#### Schemas for newly created files

**`CareerNavigator/profile.md`**
```markdown
# {Name} — Job Search Profile

## Contact
- Email, Phone, Website (extracted from resume)

## Target Roles
(extracted from resume objective/summary or left as placeholder)

## Target Companies
(leave blank if not determinable)

## Compensation Floor
(leave blank — ask the user)

## Location
(extracted from resume or left as placeholder)

## Key Differentiators
(extracted from resume summary/highlights)

## Current Search Status
- Actively searching as of {today's date}
```

**`CareerNavigator/ExperienceLibrary.json`**
```json
{
  "meta": { "created": "{today}", "version": "1.0", "description": "..." },
  "units": [
    {
      "id": "exp-001",
      "type": "role",          // "role" | "education" | "publications_and_recognition"
      "company": "...",
      "title": "...",
      "dates": "...",
      "summary": "...",
      "achievements": [
        { "id": "exp-001-a1", "theme": "...", "text": "..." }
      ],
      "skills": ["..."]
    }
  ]
}
```

**`CareerNavigator/tracker.json`**
```json
{
  "meta": { "created": "{today}", "version": "1.0", "description": "..." },
  "applications": [],
  "networking": [],
  "pipeline_summary": {
    "as_of": "{today}",
    "applied": 0,
    "considering": 0,
    "declined_or_inactive": 0,
    "overdue_followup": 0
  }
}
```

**`artifacts-index.json`**
```json
{
  "meta": { "created": "{today}", "version": "1.0", "description": "..." },
  "artifacts": [
    {
      "id": "artifact-001",
      "type": "resume",          // "resume" | "cover_letter"
      "filename": "...",
      "path": "...",
      "target_company": "...",   // null if generic/base resume
      "target_role": "...",      // null if generic/base resume
      "date_created": "...",
      "source": "existing",      // "existing" | "generated"
      "notes": "..."
    }
  ]
}
```

### 3. Confirm job search integration

Career Navigator uses the **Indeed connector** (built-in Claude Cowork integration) for live job search. No token or configuration is required — confirm it's available and continue:

> "Job search is powered by the Indeed connector. No additional setup needed — run `/career-navigator:search-jobs` any time to find live listings."

### 4. Configure Apify for salary benchmarking (optional)

The `salary-research` skill uses the **Apify** MCP tools to pull live compensation data. This step is optional — skip it if the user doesn't need salary benchmarking.

**Do not** ask the user to paste their Apify token into chat, edit `claude_desktop_config.json`, or rely on `.env` / `APIFY_TOKEN` for MCP startup — Claude Desktop does not expand `${APIFY_TOKEN}` inside MCP `args` the way a shell would.

Ask the user:
> "Would you like to set up salary benchmarking? It uses Apify's free tier ($5/month in credits — enough for personal job search use) to pull live salary data by role and location."

**If yes — Claude Desktop connector flow:**

1. Direct them to sign up at **https://apify.com** (free account).

2. They copy their **Personal API token** from **Console → Settings → Integrations** (they keep it private — **do not** ask them to paste it into this conversation).

3. Walk them through the host UI:
   - Open **Customize** (or **Settings**) → **Connectors**
   - Under **Desktop**, choose **Apify** (may show as **apify-mcp-server**)
   - Open **Configure**
   - Paste the token into **Apify token (Required)**
   - Set **Enabled tools** to this exact string (comma-separated, no spaces):

     `call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search`

   - **Save**, turn the connector **on**, start a **new chat** so MCP tools load

4. Validation: in a new session, confirm Apify tools are available (e.g. **Call Actor**, **Get Actor run**, **Get dataset items**). If they are, suggest they run `/career-navigator:salary-research` for a role and location from their profile. If tools are missing, summarize what they should double-check (token, enabled tools string, connector enabled, new session).

**Cowork / other hosts:** If the user is not on Claude Desktop, tell them to add Apify MCP the way their host documents (same **Enabled tools** string and a secure token field if the UI offers one). Do not invent a JSON config that embeds the token.

**If no or skipped:**

> "No problem — salary benchmarking is off for now. You can set it up any time by running `/career-navigator:setup` again."
