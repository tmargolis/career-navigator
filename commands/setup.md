---
name: setup
command: /career-navigator:setup
description: >
  The single entry point for all Career Navigator configuration. Sets up the
  job search folder, builds the user profile and corpus from existing documents,
  configures JobSearch for live job search, and optionally connects Google Drive.
  No Customize button required — run this command to do everything.
triggers:
  - "set up career navigator"
  - "configure career navigator"
  - "get started with career navigator"
  - "career navigator setup"
---

# /career-navigator:setup

**This is the only setup step.** There is no Customize button to click. Run this command once after installing the plugin — it handles everything: registering your job search folder, reading your existing documents, building your profile and corpus, and configuring integrations. Re-run any time to update a key, add Google Drive, or reconfigure from scratch.

## Usage

```
/career-navigator:setup
```

Throughout this command, `{user_dir}` refers to the user's configured job search directory. All data — profile, corpus, tracker, generated artifacts — lives in subdirectories of this single folder alongside the user's raw documents.

## Workflow

### 0. Confirm job search directory

**If the user provided a directory path in their message**: use it.

**If no path was provided**: ask:
> "What folder should Career Navigator use for your job search? This is where your resumes and cover letters live, and where I'll save everything I generate. Share the full path."

Once you have the path, expand `~` if present and confirm the directory exists. If it doesn't exist, offer to create it.

#### 0b. Save the directory to config

Run `python3 scripts/init.py {user_dir}` via the Bash tool. This saves the path so session-start and sync hooks can find it at runtime. No restart required.

If the Bash tool is unavailable, write the config directly using the Write tool:
- Path (macOS): `~/Library/Application Support/Claude/cowork_plugins/career-navigator/config.json`
- Path (Linux): `~/.config/Claude/cowork_plugins/career-navigator/config.json`
- Content: `{"user_dir": "{user_dir}"}`

Then continue to step 1.

---

### 1. Check current configuration

Read `.mcp.json` and report what's already active vs. what's missing:

```
CAREER NAVIGATOR SETUP
──────────────────────────────────────────
JobSearch (job search)     [ ] Not configured
──────────────────────────────────────────
Let's get you set up. This will take about 2 minutes.
```

If already configured:
```
JobSearch (job search)     [✓] Active
──────────────────────────────────────────
Everything looks good. Want to re-validate a key or switch a connector?
```

Only walk through unconfigured items, or items the user explicitly asks to reconfigure.

---

<!-- STEPS 2–6 COMMENTED OUT FOR INCREMENTAL TESTING — restore once step 0/1 confirmed working

### 2. JobSearch setup (job search)

**Step 1 — Introduce JobSearch**

> "JobSearch gives Career Navigator access to live job listings from Indeed, LinkedIn, and other boards — no copy-pasting required. The free tier covers plenty of searches for an active job search."
>
> "Opening the signup page now — create a free account and then paste your API key back here."

Open the signup page using a Bash call:
- macOS: `open https://app.hasdata.com/sign-up`
- Linux: `xdg-open https://app.hasdata.com/sign-up`
- Windows: `start https://app.hasdata.com/sign-up`

If the Bash tool is unavailable, display the URL directly:
> "Please open this URL to create your free JobSearch account: https://app.hasdata.com/sign-up"

**Step 2 — Wait for the key**

> "Once you're signed in, copy your API key from the JobSearch dashboard and paste it here."

Accept any string that looks like an API key (typically a long alphanumeric string). If the user pastes something clearly wrong (e.g., a URL, very short string), say so and ask again.

**Step 3 — Validate the key**

Before saving, make a test API call to confirm the key works. Use a minimal, low-cost request (e.g., a single-result search for a common term). If the call succeeds:

> "Key validated successfully."

If the call fails:
> "That key didn't work — the API returned [error]. Double-check you copied the full key from the JobSearch dashboard and try again."

Do not save an invalid key.

**Step 4 — Write to config**

Update `.mcp.json`:
- Move the `jobsearch` entry from `_inactive_services` into `mcpServers`
- Set `HASDATA_API_KEY` to the validated key in the `env` block

Confirm:
> "JobSearch configured. `/career-navigator:search-jobs` will now search live job listings automatically."

---

### 3. Scan local job search folder

**Rule: Always scan the local folder before asking about any other source (Google Drive, Gmail, etc.).**

#### 3a. Get the folder path

The job search directory was confirmed in step 0. That is the primary local source — read every resume, CV, cover letter, and job search document in it (recursively, skipping the `profile/`, `corpus/`, and `tracker/` managed subdirs).

If the user hasn't provided a folder path yet, ask now before proceeding:
> "Where do you keep your job search documents — resumes, cover letters, and anything else related to your search? Share the full folder path."

Accept any valid directory path. Confirm it exists before continuing. If the user doesn't have one yet:
> "No problem — create a folder anywhere you'd like (for example, `~/Documents/Job Search/`) and move any resumes or cover letters into it. Give me the path and we'll go from there."

Save the path to the `## Watch Directory` section of `{user_dir}/profile/profile.md`.

#### 3b. Discover locally

**Do not ask any questions until all local sources have been read.**

Run all of the following before asking anything:

1. **Existing profile**: Read `{user_dir}/profile/profile.md` if it exists. If complete and recent, show a summary and skip to step 4.
2. **Job search folder**: Read every resume, CV, and job search document in the folder. This is the primary source.
3. **Existing corpus**: Read `{user_dir}/corpus/index.json` — skill tags, titles, and company names already contain significant profile signal.

#### 3c. Extract into corpus

For each resume or CV found:
- Check `{user_dir}/corpus/index.json` → `source_documents[]` — skip if already imported by filename/path (per-document deduplication, not all-or-nothing).
- If new: extract experience units, assign skill tags, set performance weights (1.0), append to `{user_dir}/corpus/index.json`. Initialize from template if it doesn't exist.

#### 3d. Ask about additional sources

After fully scanning the local folder, ask:
> "I've read everything in your local folder. Would you also like me to check Google Drive, Gmail, or anywhere else for additional resumes or application history?"

If the user says yes to **Google Drive**:

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

**Step 3 — Write to config and search**

Copy the credentials file to `services/connectors/google-drive/credentials.json` (create the directory if needed).

Update `.mcp.json`:
- Move the `google-drive` entry from `_inactive_services` into `mcpServers`
- Set `GOOGLE_CREDENTIALS_PATH` in the `env` block

Search Google Drive for resumes, CVs, and job search materials not already found locally. Extract and add any new documents to the corpus (same deduplication rules as 3c).

> "Google Drive connected and scanned."

If the user says no or skips:
> "Got it — working from your local folder only. You can add Google Drive any time by running `/career-navigator:setup` again."

---

### 4. Build user profile

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

### 5. Import application history

Scan the job search folder and Google Drive (if connected) for evidence of existing applications — cover letters addressed to specific companies, application confirmation emails, tracking spreadsheets, or any document implying a submission.

For each application found:
- Extract: company, role title, approximate date applied, any status signals
- Create a record in `{user_dir}/tracker/tracker.json` using the standard schema
- Set `status` to the best available inference (default: "Applied" if uncertain)

Ask before writing:
> "I found evidence of [N] past applications. Want me to import them into your tracker? I'll flag anything I'm uncertain about."

If nothing found: skip silently.

---

### 6. Completion summary

```
SETUP COMPLETE
──────────────────────────────────────────
Profile                  [✓] Created
Corpus                   [✓] [N] experience units from [X] resumes
Applications             [✓] [N] imported  (or [ ] None found)
JobSearch (job search)     [✓] Active        (or [ ] Not configured)
Google Drive (storage)   [✓] Active        (or [ ] Using local storage)
──────────────────────────────────────────
```

Suggest the natural next step — never suggest running `/career-navigator:setup` again:
- If JobSearch is not yet configured: "Run `/career-navigator:setup` again to add your JobSearch key, or run `/career-navigator:search-jobs` now to use assisted-manual search."
- Otherwise: "Run `/career-navigator:search-jobs` to find matching roles, or `/career-navigator:tailor-resume` with a job description to build your first targeted resume."

END COMMENTED-OUT SECTION -->

---

## Re-run behavior

When invoked on an already-configured system, ask:
> "What would you like to update?
> 1. Replace my JobSearch key
> 2. Set up or switch to Google Drive
> 3. Switch back to local storage
> 4. Re-validate all active connectors"

Only touch the configuration the user selects. All other settings remain unchanged.
