---
name: setup
command: /career-navigator:setup
description: >
  Conversational setup wizard. Configures HasData for automated job search and
  optionally sets up Google Drive for cloud storage. Handles all file writes
  automatically — no manual JSON editing required. Re-runnable at any time to
  update keys or switch connectors.
triggers:
  - "Customize the career-navigator plugin"
  - "customize career navigator"
  - "set up career navigator"
  - "configure career navigator"
  - "get started with career navigator"
---

# /career-navigator:setup

First-run configuration wizard. Walks through each integration step-by-step, validates credentials before saving, and writes everything to config automatically. Run this before using `/career-navigator:search-jobs` (for automated mode) or to switch storage connectors.

## Usage

```
/career-navigator:setup
```

Re-run any time to update a key, re-validate a connector, or add a new integration.

Throughout this command, `{user_dir}` refers to the user's configured job search directory. All data — profile, corpus, tracker, generated artifacts — lives in subdirectories of this single folder alongside the user's raw documents.

## Workflow

### 0. Confirm job search directory

**If the user provided a directory path in their message**: use it. Skip to step 0b.

**If no path was provided**: ask:
> "What folder should Career Navigator use for your job search? This is where your resumes and cover letters live, and where I'll save everything I generate. Share the full path."

#### 0b. Register and verify

Run `python3 scripts/init.py {user_dir}` to:
- Save the path to `~/Library/Application Support/Claude/cowork_plugins/career-navigator/config.json` (used by hooks at startup)
- Register the directory with Claude Desktop's filesystem MCP server

If the Bash tool is unavailable, instruct the user:
> "Run this once from the plugin directory, then restart Claude Desktop:
> ```
> python3 scripts/init.py /your/path/here
> ```"

Attempt to read or list `{user_dir}` to confirm filesystem access. If it fails, stop and surface the above instructions.

---

### 1. Check current configuration

Read `.mcp.json` and report what's already active vs. what's missing:

```
CAREER NAVIGATOR SETUP
──────────────────────────────────────────
HasData (job search)     [ ] Not configured
Google Drive (storage)   [ ] Not configured
──────────────────────────────────────────
Let's get you set up. This will take about 2 minutes.
```

If everything is already configured:
```
HasData (job search)     [✓] Active
Google Drive (storage)   [✓] Active
──────────────────────────────────────────
Everything looks good. Want to re-validate a key or switch a connector?
```

Only walk through unconfigured items, or items the user explicitly asks to reconfigure.

---

### 2. HasData setup (job search)

**Step 1 — Introduce HasData**

> "HasData gives Career Navigator access to live job listings from Indeed, LinkedIn, and other boards — no copy-pasting required. The free tier covers plenty of searches for an active job search."
>
> "Opening the signup page now — create a free account and then paste your API key back here."

Open the signup page using a Bash call:
- macOS: `open https://app.hasdata.com/sign-up`
- Linux: `xdg-open https://app.hasdata.com/sign-up`
- Windows: `start https://app.hasdata.com/sign-up`

If the Bash tool is unavailable, display the URL directly:
> "Please open this URL to create your free HasData account: https://app.hasdata.com/sign-up"

**Step 2 — Wait for the key**

> "Once you're signed in, copy your API key from the HasData dashboard and paste it here."

Accept any string that looks like an API key (typically a long alphanumeric string). If the user pastes something clearly wrong (e.g., a URL, very short string), say so and ask again.

**Step 3 — Validate the key**

Before saving, make a test API call to confirm the key works. Use a minimal, low-cost request (e.g., a single-result search for a common term). If the call succeeds:

> "Key validated successfully."

If the call fails:
> "That key didn't work — the API returned [error]. Double-check you copied the full key from the HasData dashboard and try again."

Do not save an invalid key.

**Step 4 — Write to config**

Update `.mcp.json`:
- Move the `hasdata` entry from `_inactive_services` into `mcpServers`
- Set `HASDATA_API_KEY` to the validated key in the `env` block

Confirm:
> "HasData configured. `/career-navigator:search-jobs` will now search live job listings automatically."

---

### 3. Google Drive setup (optional)

> "Would you like to store your resumes, cover letters, and application data in Google Drive? This keeps everything backed up and accessible from any device. (You can skip this and use local storage — your data stays in your job search folder.)"

If the user says yes:

**Step 1 — Create credentials**

> "You'll need to create a Google Cloud project and OAuth credentials. Here are the steps:"
>
> "1. Go to https://console.cloud.google.com/ — create a project (any name)"
> "2. In the left menu: APIs & Services → Library → search 'Google Drive API' → Enable"
> "3. APIs & Services → Credentials → Create Credentials → OAuth client ID"
> "4. Application type: Desktop app → Create"
> "5. Download the credentials JSON file"

Open the Cloud Console if possible:
- macOS: `open https://console.cloud.google.com/`

**Step 2 — Get the credentials file path**

> "Where did you save the credentials JSON file? Paste the file path here."

Read the file at that path to verify it's a valid Google OAuth credentials file (check for `client_id`, `client_secret`, `redirect_uris` fields). If invalid, say so.

**Step 3 — Write to config**

Copy the credentials file to `services/connectors/google-drive/credentials.json` (create the directory if needed).

Update `.mcp.json`:
- Move the `google-drive` entry from `_inactive_services` into `mcpServers`
- Set `GOOGLE_CREDENTIALS_PATH` in the `env` block

> "Google Drive configured. On your next command that saves an artifact, you'll be prompted to authorize access — this only happens once."

If the user skips Google Drive:
> "No problem. Everything saves to your job search folder locally. You can run `/career-navigator:setup` any time to add Google Drive later."

---

### 4. Configure watch directory

The watch directory is where the user keeps their job search documents — resumes, cover letters, application notes, etc. Career Navigator reads it on startup and at midnight to automatically ingest new and updated files.

Ask:
> "Where do you keep your job search documents? Share the folder path and I'll watch it for changes automatically — any resume or cover letter you add there will be imported without you having to run a command."

Accept any valid directory path. Confirm it exists before saving. If the user doesn't have one yet:
> "No problem — create a folder anywhere you'd like (for example, `~/Documents/Job Search/`) and paste any resumes or cover letters into it. Give me the path and we'll go from there."

Save the path to the `## Watch Directory` section of `{user_dir}/profile/profile.md`.

---

### 5. Build user profile and corpus

**Rule: Do not ask any questions until all available sources have been read.** Discovery first, questions only to fill genuine gaps.

#### 5a. Discover

Run all of the following before asking anything:

1. **Existing profile**: Read `{user_dir}/profile/profile.md` if it exists. If complete, show a summary and skip to 5c.
2. **Watch directory**: Read every resume, CV, and job search document in the configured watch directory. This is the primary source.
3. **Existing corpus**: Read `{user_dir}/corpus/index.json` — skill tags, titles, and company names already contain significant profile signal.
4. **Google Drive** (if connected): Search for resumes, CVs, and any additional job search materials not already in the watch directory.

#### 5b. Extract into corpus

For each resume or CV found in 5a:
- Check `{user_dir}/corpus/index.json` → `source_documents[]` — skip if already imported by filename/path.
- If new: extract experience units, assign skill tags, set performance weights (1.0), append to `{user_dir}/corpus/index.json`. Initialize from template if it doesn't exist.

#### 5c. Build profile

Consolidate all discovered sources into a draft profile using `templates/profile.md.template`. Prefer the most recent and specific data when sources conflict. Profile fields:
- Professional summary and level
- Target role titles and minimum seniority
- Target companies (primary, secondary, types to avoid)
- Industries to prioritize and deprioritize
- Minimum total compensation (base + bonus + equity annualized)
- Location preferences and relocation openness
- Key skills (for ATS prioritization)
- Unique differentiators that must appear in every resume

Show the draft and ask only about fields that couldn't be determined:
> "Here's what I've put together from your documents. Does this look right? Let me know what to change or add."

Save to `{user_dir}/profile/profile.md`. Confirm corpus:
> "Corpus updated — [X] experience units across [Y] skills from [N] resume(s)."

---

### 6. Import application history

Scan the watch directory and Google Drive (if connected) for evidence of existing applications — cover letters addressed to specific companies, application confirmation emails, tracking spreadsheets, or any document implying a submission.

For each application found:
- Extract: company, role title, approximate date applied, any status signals
- Create a record in `{user_dir}/tracker/tracker.json` using the standard schema
- Set `status` to the best available inference (default: "Applied" if uncertain)

Ask before writing:
> "I found evidence of [N] past applications. Want me to import them into your tracker? I'll flag anything I'm uncertain about."

If nothing found: skip silently.

---

### 7. Completion summary

```
SETUP COMPLETE
──────────────────────────────────────────
Profile                  [✓] Created
Corpus                   [✓] [N] experience units from [X] resumes
Applications             [✓] [N] imported  (or [ ] None found)
HasData (job search)     [✓] Active        (or [ ] Not configured)
Google Drive (storage)   [✓] Active        (or [ ] Using local storage)
──────────────────────────────────────────
```

Suggest the natural next step — never suggest running `/career-navigator:setup` again:
- If HasData is not yet configured: "Run `/career-navigator:setup` again to add your HasData key, or run `/career-navigator:search-jobs` now to use assisted-manual search."
- Otherwise: "Run `/career-navigator:search-jobs` to find matching roles, or `/career-navigator:tailor-resume` with a job description to build your first targeted resume."

---

## Re-run behavior

When invoked on an already-configured system, ask:
> "What would you like to update?
> 1. Replace my HasData key
> 2. Set up or switch to Google Drive
> 3. Switch back to local storage
> 4. Re-validate all active connectors"

Only touch the configuration the user selects. All other settings remain unchanged.
