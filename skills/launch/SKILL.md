---
name: launch
description: >
  Launch your job search with Career Navigator: the single entry point for configuration.
  Sets up the job search folder, builds the user profile, ExperienceLibrary and application tracker from existing documents,
  walks through the Indeed MCP connector (browser OAuth) for live job search, optional Apify for salary data, and Google Drive when applicable.
  No Customize button required — run this command to do everything.
triggers:
  - "/career-navigator:launch"
  - "launch career"
  - "launch career navigator"
  - "begin my job search with career navigator"
  - "set up career"
  - "set up career navigator"
  - "configure career navigator"
  - "get started with career navigator"
---

Use this after installing the plugin — it is how you **launch** Career Navigator: registering your job search folder, reading your existing documents, building your profile and ExperienceLibrary, and configuring integrations (the same setup flow as before, framed as starting your search).

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
- **`CareerNavigator/profile.md`**: Must contain sections for target roles, compensation floor, location, and key differentiators. If any section is missing or empty, fill it in from other available sources (ExperienceLibrary, resume documents in `{user_dir}`). Also ensure Phase 1F support sections exist or are empty-but-ready to fill:
  - `## Employment Context`
  - `## Certifications & Credentials`
  If they are missing or empty, resolve from documents and then ask the user to confirm/add missing details.

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
> "I didn't find any resumes or documents in your job search folder. Add a resume (PDF or DOCX) and run `/career-navigator:launch` again to build your profile and ExperienceLibrary."

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

## Employment Context
- Employment status: employed | unemployed | unknown
- If employed: current comp package (base/bonus/equity/benefits if available) and what issues might make you open to a new role (bullets).
- If unemployed: last job (title/company/end date if known), income sources (unemployment/severance/other), and runway until you need a new job (weeks/months).
- Notes / assumptions (no invention).

## Certifications & Credentials
- Degrees:
- Certifications / professional licenses:
- Clearance / security clearance:
- Other credentials:
- Notes (e.g., expiration/renewal if known).

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
      "type": "resume",          // "resume" | "cover_letter" | "linkedin_post"
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

### 2.4 Phase 1F intake: employment situation + credentials (persist to profile.md)

After core files exist (or after they are created/repaired), ensure your
`{user_dir}/CareerNavigator/profile.md` has usable Phase 1F context:

1. Read `{user_dir}/CareerNavigator/profile.md` and check whether:
   - `## Employment Context` is present and not just placeholders, and
   - `## Certifications & Credentials` is present and not just placeholders.

2. Attempt to fill from documents already found in `{user_dir}`:
   - From CV/resume/cover letter text: extract degrees, certifications,
     professional licenses, and any clearance/security mentions.
   - Extract employment clues (current employer, if they’re between roles,
     unemployment/severance mentions, etc.).

3. If `Employment Context` is missing/unclear, ask targeted questions and
   then write the answers back into `profile.md` under:
   - `## Employment Context`
   - Scenario A (employed): ask current comp package and what issues/constraints might make a job change attractive.
   - Scenario B (unemployed): ask unemployment benefits/severance/income sources,
     last job (title/company/end date if known), and runway until you need a new job.
   - Scenario C (unknown): ask one minimal clarifier question to distinguish employed vs unemployed.

4. If `Certifications & Credentials` are missing/unclear, present what you found
   (as a short list) and ask the user to confirm and add anything missing.

5. Persistence rules:
   - Do not overwrite other sections (Target Roles, Key Differentiators, etc.).
   - Only update the content under the two Phase 1F headings.
   - If the user says “not sure”, record `unknown` explicitly instead of inventing.

### 2.5 Voice profile (launch)

After core files exist, build or refresh `{user_dir}/CareerNavigator/voice-profile.md` so **`writer`** has real tone signal—not a single auto-generated markdown artifact when résumés/CVs/letters live elsewhere.

**Order:** Run **2.5b** first (inventory + read Tier A PDFs/DOCX), then **2.5a** (LinkedIn prompt), then incorporate paste or a **continue** re-scan into **2.5c**. If the user adds new files after **2.5a**, re-run **2.5b** before writing.

#### 2.5a Ask for LinkedIn / social writing (same session)

After **2.5b** (and any re-scan if the user drops new files), prompt once before writing **2.5c**:

> **Voice & tone:** To match how you sound on LinkedIn and in messages—not only on résumés—please choose one:
> 1. **Paste** 2–5 recent LinkedIn posts (or other short professional writing) here, **or**
> 2. **Add** them as files in this folder (e.g. `linkedin-posts.md`, `.txt`, or a PDF export), then tell me when they’re saved **or** say **continue** so I can re-read the folder, **or**
> 3. Reply **skip** and I’ll rely on résumés/cover letters only (**weaker match** for social and DMs).

If they **paste**: append a dated **`## User writing samples (launch)`** section with excerpts (trimmed), label **source: user paste (launch)**.

If they **skip**: record one line under **`## Launch — LinkedIn prompt`**: *User skipped LinkedIn samples at launch; writer may ask again before drafting.*

#### 2.5b Gather prose from disk (priority order)

**Goal:** Use **CVs, résumés, and cover letters** as primary voice sources, not stray `.md` alone.

1. **Scope:** Walk **`{user_dir}`** recursively (or top level **plus** all non-hidden subfolders—minimum depth that finds `Documents/`, `resumes/`, etc.). **Skip:** `.git`, `node_modules`, `.Trash`, and anything that is clearly not user documents.

2. **Always ignore as corpus input:**
   - `{user_dir}/CareerNavigator/voice-profile.md` (don’t read this file to infer voice).
   - All **`CareerNavigator/*.json`** (schemas/data, not voice).

3. **Classify every candidate file** (by path + name + `artifacts-index.json` when present):
   - **Tier A — Raw career documents (prefer):** `*.pdf`, `*.docx`, `*.txt`, `*.md` whose names/paths suggest **resume**, **cv**, **curriculum vitae**, **cover**, **letter**, **bio**, **about**, or obvious user-upload basenames. **You must read PDF and DOCX** the same way you do when building `profile.md` / ExperienceLibrary—extract **professional summary / profile**, **cover letter body** (if present in file), and **representative bullet lines** (not the entire work history). If a file is only bullet lists with no narrative, note register (density, metrics, voice in bullets).
   - **Tier B — Other prose:** remaining `.md` / `.txt` that look like user writing (not changelogs, not unrelated repo readmes).
   - **Tier C — Plugin-generated artifacts (use with care):** entries in **`artifacts-index.json`** with `"source": "generated"` (and matching files on disk). **Do not** let Tier C be the **only** narrative basis if any **Tier A** file exists. If only Tier C supplies paragraph prose, use it but label **Source: generated artifact** and flag **lower confidence** for “natural” voice.

4. **Minimum bar:** If you find **multiple sources** with **clearly different tone** (e.g. formal cover letter vs casual LinkedIn paste), **do not** flatten into one voice—use **2.5c** multi-context sections and/or **Open questions**.

5. **If no narrative at all:** only bullets and structure—still write voice notes (brevity, metrics, keyword density); flag that **`writer`** needs pasted prose for paragraph-level match.

#### 2.5c Write `voice-profile.md` (structure)

Create or update with dated sections (you may keep older dated blocks below for history).

1. **`## Launch voice harvest (YYYY-MM-DD)`** (or retain **`## Setup scan (YYYY-MM-DD)`** if you prefer that heading—but use one dated harvest per run):
   - Table **Source files scanned**: **Path** (relative to `{user_dir}`), **Tier** (A/B/C), **Doc type** (résumé / CV / cover / LinkedIn file / other), **Voice notes** (short).
   - **Include every qualifying file** you found—not only the first markdown file.

2. **`## Voice by context`** (when tones diverge or user supplied formal + casual samples):
   - Subsections e.g. **`### Applications (résumé / cover letter)`**, **`### Public (LinkedIn)`**, **`### Other`**. Register, sentence length, humor, CTAs per subsection.
   - If tones conflict and intent is unclear, add **`## Open questions`** (1–4 bullets): default voice for cover letter vs DM vs post; intentional **multiple personas** for different audiences; etc.

3. **`## Voice quality flags (launch)`** — candid risks (job-search pragmatism, not personal attack):
   - Examples: **snark / sarcasm** that may read poorly to conservative employers; **try-hard** or overselling; **generic “AI slop” tells** (empty grandiosity, filler transitions, buzzword stacks without proof); **apology / hedging** loops; **political or divisive edge** in public samples; **over-share**. For each: **low / medium / high** concern + **why**. If clean: *No major flags from available samples.*

4. **Optional `voice_profile_v1` JSON** at end: include `"tones": { "applications": "…", "public": "…" }` when multi-context sections exist.

5. **`## Usage guidance for writer`:** Which context to use for **cover letter** vs **LinkedIn** vs **DM**; if ambiguous, **ask the user once** in this launch session before moving on.

**Do not** treat a lone plugin-generated cover letter as sufficient if Tier A résumés/CVs exist in the same folder—**ingest those files** for this section.

### 3. Connect the Indeed MCP connector (live job search)

Career Navigator’s **`search-jobs`** skill expects the **Indeed** MCP tools **`search_jobs`** and **`get_job_details`**. On **Claude Desktop**, those tools appear only after the user connects **Indeed** under **Customize → Connectors** and finishes **browser-based OAuth** with Indeed (this is **not** a static API key you paste into `.mcp.json`).

**What to expect in Claude Desktop:**

- The **Indeed** connector page describes **“Search for jobs on Indeed”**, developer **Indeed**, and under **Tools** lists **`search_jobs`** and **`get_job_details`**. **Details** may show the connector URL `https://mcp.indeed.com/claude/mcp` (for reference only — connect through the app, not by editing JSON).
- Tapping **Connect** starts the link flow. Claude shows **“Grant access to Indeed”** with a prompt to **complete the sign-in steps in the new browser tab** (and **“Didn’t work? Relaunch the tab”** if needed).
- In the browser, **Indeed** opens an OAuth page on **`secure.indeed.com`** (**“Claude would like to access your account”**). The user signs in (or confirms the right Indeed account), reviews permissions (e.g. search jobs on their behalf, profile access), then clicks **Continue** to authorize.

**Walk the user through:**

1. **Customize** (or **Settings**) → **Connectors** → find **Indeed** in the catalog.
2. Open **Indeed** → confirm **Tools** includes **`search_jobs`** and **`get_job_details`**.
3. Click **Connect**. When **Grant access to Indeed** appears, tell them to switch to the **new browser tab**, finish **Indeed** sign-in / consent, and click **Continue** on the OAuth screen.
4. After success, Claude should show the connector as connected (e.g. **Disconnect** visible instead of **Connect**). If tools still don’t appear, start a **new chat**.

**Validation:** In this session (or after a fresh chat), confirm **`search_jobs`** / **`get_job_details`** are available. If yes:

> "Indeed is connected. Run `/career-navigator:search-jobs` any time, or ask me to find jobs for your target role and location."

If tools are missing after OAuth, have them verify: Indeed account authorized, connector still enabled, **new chat** after connecting.

**Claude Cowork / other hosts:** Use the host’s documented way to enable **Indeed** job search MCP (same tool names when available). Do not invent credentials or scrape Indeed without the official connector.

### 4. Configure Apify for salary benchmarking (optional)

The `salary-research` skill uses the **Apify** MCP tools to pull live compensation data. This step is optional — skip it if the user doesn't need salary benchmarking.

**Do not** ask the user to paste their Apify token into chat, edit `claude_desktop_config.json`, or rely on `.env` / `APIFY_TOKEN` for MCP startup — Claude Desktop does not expand `${APIFY_TOKEN}` inside MCP `args` the way a shell would.

First check if the Apify MCP is already connected. It may be in a deferred state, so double check and make sure to activate them if you need to. If they are active, suggest they run `/career-navigator:salary-research` for a role and location from their profile. If not, Ask the user:
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

4. Validation: Confirm Apify tools are available (e.g. **Call Actor**, **Get Actor run**, **Get dataset items**). If tools need to be activated from a deferred state, then do that. If the tools are missing, summarize what they should double-check (token, enabled tools string, connector enabled, new session).

**Cowork / other hosts:** If the user is not on Claude Desktop, tell them to add Apify MCP the way their host documents (same **Enabled tools** string and a secure token field if the UI offers one). Do not invent a JSON config that embeds the token.

**If no or skipped:**

> "No problem — salary benchmarking is off for now. You can set it up any time by running `/career-navigator:launch` again."
