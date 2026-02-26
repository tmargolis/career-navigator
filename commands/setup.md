---
name: setup
command: /cn:setup
description: >
  Conversational setup wizard. Configures HasData for automated job search and
  optionally sets up Google Drive for cloud storage. Handles all file writes
  automatically — no manual JSON editing required. Re-runnable at any time to
  update keys or switch connectors.
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

### 4. Completion summary

```
SETUP COMPLETE
──────────────────────────────────────────
HasData (job search)     [✓] Active
Google Drive (storage)   [✓] Active   (or [ ] Using local storage)
──────────────────────────────────────────
```

Suggest the natural next step:
- If corpus is empty: "Run `/cn:add-source` to add your resume and get started."
- If corpus exists but no searches run: "Run `/cn:search-jobs` to find matching roles — it's now fully automated."
- If fully active: "You're all set. What would you like to work on?"

---

## Re-run behavior

When invoked on an already-configured system, ask:
> "What would you like to update?
> 1. Replace my HasData key
> 2. Set up or switch to Google Drive
> 3. Switch back to local storage
> 4. Re-validate all active connectors"

Only touch the configuration the user selects. All other settings remain unchanged.
