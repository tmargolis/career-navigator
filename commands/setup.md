---
name: setup
command: /cn:setup
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

# /cn:setup

First-run configuration wizard. Walks through each integration step-by-step, validates credentials before saving, and writes everything to config automatically. Run this before using `/cn:search-jobs` (for automated mode) or to switch storage connectors.

## Usage

```
/cn:setup
```

Re-run any time to update a key, re-validate a connector, or add a new integration.

## Workflow

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
> "HasData configured. `/cn:search-jobs` will now search live job listings automatically."

---

### 3. Google Drive setup (optional)

> "Would you like to store your resumes, cover letters, and application data in Google Drive? This keeps everything backed up and accessible from any device. (You can skip this and use local storage — your data stays in the `data/` folder.)"

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
> "No problem. Everything saves to `data/` locally. You can run `/cn:setup` any time to add Google Drive later."

---

### 4. Build user profile

Create or update `data/profile/profile.md` — the permanent reference file all agents read before every operation.

**If Google Drive is connected**: Search Drive for resumes, CVs, and any existing job search materials before asking questions. Extract what you can find, then ask only for what you couldn't determine.

**If no Drive access**: Ask the following conversationally (not as a form):
- Brief professional summary and what makes you distinctive at your level
- Target role titles and minimum seniority
- Target companies (primary, secondary, and types to avoid)
- Industries to prioritize and deprioritize
- Minimum total compensation (base + bonus + equity annualized)
- Location preferences and relocation openness
- Key skills to prioritize for ATS matching
- Any unique differentiators that must appear in every resume

Write the profile using `data/profile/profile.md.template` as the schema. Save to `data/profile/profile.md`.

If a profile already exists, show a summary and ask: "Would you like to update anything, or does this still look right?"

---

### 5. Build corpus from existing resumes

**If Google Drive is connected and resumes were found during profile building**: Do not ask the user to run `/cn:add-source` separately. Import the resumes now.

- Identify the most current and complete resume(s) found in Drive. If there are role-specific tailored versions (e.g., "Resume — Anthropic"), import those too.
- For each, run the full `/cn:add-source` extraction: parse experience units, assign skill tags, set default performance weights, append to `data/corpus/index.json`.
- Confirm: "I've added [N] resumes to your corpus — [X] experience units extracted across [Y] skills."

**If no Drive access**: Skip this step. Remind the user once at the end to run `/cn:add-source`.

---

### 6. Import application history

**If Google Drive is connected**: Search for evidence of existing applications — job hunt folders, tracking spreadsheets, cover letters addressed to specific companies, or any document that implies an application was submitted.

For each application found:
- Extract: company, role title, approximate date applied, any status signals (offer, rejection, interview notes)
- Create a record in `data/applications/tracker.json` using the standard schema
- Set `source_board` to "imported from Google Drive" and `status` to the best available inference (default: "Applied" if uncertain)

Ask before writing: "I found evidence of [N] past applications in your Drive. Want me to import them into your tracker? I'll flag anything I'm uncertain about."

**If no Drive access or no application history found**: Skip this step silently.

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

Suggest the natural next step — never suggest running `/cn:setup` again:
- If HasData is not yet configured: "Run `/cn:setup` again to add your HasData key, or run `/cn:search-jobs` now to use assisted-manual search."
- Otherwise: "Run `/cn:search-jobs` to find matching roles, or `/cn:tailor-resume` with a job description to build your first targeted resume."

---

## Re-run behavior

When invoked on an already-configured system, ask:
> "What would you like to update?
> 1. Replace my HasData key
> 2. Set up or switch to Google Drive
> 3. Switch back to local storage
> 4. Re-validate all active connectors"

Only touch the configuration the user selects. All other settings remain unchanged.
