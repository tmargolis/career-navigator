---
name: launch
description: >
  Launch your job search with Career Navigator: the single entry point for configuration. Sets up the job search folder, builds the user profile, ExperienceLibrary and application tracker from existing documents, walks through the Indeed MCP connector (browser OAuth) for live job search, optional Apify for salary data, optional Gmail / Microsoft 365 inbox and optional Google Calendar connectors (OAuth) for outreach and meeting context, optional LinkedIn post analytics, and Google Drive when applicable. No Customize button required — run this command to do everything.
triggers:
  - "/career-navigator:launch"
  - "/launch"
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

**Integrations (Indeed, Apify, LinkedIn, Gmail, Microsoft 365, Google Calendar, future):** Follow [CONNECTORS.md](CONNECTORS.md): **only prompt for services that are not already connected** in this session (host tools missing or user reports a problem). If **Indeed** / **Apify** / **Gmail** / **M365** / **Google Calendar** tools are already present, a **brief acknowledgment** is enough—**do not** ask setup, OAuth, or browser-access questions for those.

## Workflow

### Connector pattern (apply to steps 3–6)

| Step | What to do |
| --- | --- |
| **1 — Discover** | Check tools in **this chat** for that integration. If **connected** (tools present), acknowledge briefly and **skip** further steps for it. |
| **2 — Configure** | **Only if not connected:** **ask** if they want to set up; guide [CONNECTORS.md](CONNECTORS.md); **they** complete **Connectors** + OAuth/token. **Never** automate OAuth with Chrome/computer use. |
| **3 — Browser access** | **Only if not connected via MCP** or the flow is **browser-only** (e.g. **LinkedIn** analytics). **Do not** ask for **Indeed** / **Apify** / inbox / **calendar** when MCP tools already work. |

Apply **1 → 2 → (3 only when needed)** per integration—**omit** steps 2–3 when step 1 already succeeded.

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
- **`CareerNavigator/profile.md`**: Must contain sections for target roles, compensation floor, location, and key differentiators. If any section is missing or empty, fill it in from other available sources (ExperienceLibrary, resume documents in `{user_dir}`). Also ensure support sections exist or are empty-but-ready to fill:
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

## LinkedIn
- LinkedIn slug: (vanity username, e.g. `todd-margolis` from `linkedin.com/in/todd-margolis`)

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

### 2.4 employment situation + credentials instake (persist to profile.md)

After core files exist (or after they are created/repaired), ensure your
`{user_dir}/CareerNavigator/profile.md` has usable context:

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

5. Ensure `## LinkedIn` has all fields required for scheduled analytics:
   - `LinkedIn slug:`
   - `LinkedIn analytics permission: granted | denied`
   - `LinkedIn analytics mode: chrome | computer | either`
   If slug is missing/blank, ask: "What's your LinkedIn vanity username? (the part after `linkedin.com/in/`)" and save it.
   If permission/mode are missing, ask once and save them. If the user declines analytics, save `permission: denied` and `mode: unknown`.

6. Persistence rules:
   - Do not overwrite other sections (Target Roles, Key Differentiators, etc.).
   - Only update the content under the relevant headings.
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

Apply **Connector pattern**; **do not** ask about **Indeed** if **`search_jobs`** / **`get_job_details`** are already available in **this chat**.

Career Navigator’s **`search-jobs`** skill expects the **Indeed** MCP tools **`search_jobs`** and **`get_job_details`**. On **Claude Desktop**, those tools appear only after the user connects **Indeed** under **Customize → Connectors** and finishes **browser-based OAuth** with Indeed (this is **not** a static API key you paste into `.mcp.json`). **Only if tools are missing**, run **Configure**; **they** complete **Connect** and OAuth—do not drive it via **Claude in Chrome** or **computer use**.

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

**Do not** ask about **Indeed** further (including browser access)—it is already configured.

If tools are missing after OAuth, have them verify: Indeed account authorized, connector still enabled, **new chat** after connecting.

**Claude Cowork / other hosts:** Use the host’s documented way to enable **Indeed** job search MCP (same tool names when available). Do not invent credentials or scrape Indeed without the official connector.

### 4. Configure Apify for salary benchmarking (optional)

Apply **Connector pattern**; **do not** ask about **Apify** if its tools are already available—suggest **`/career-navigator:salary-research`** and move on.

The `salary-research` skill uses the **Apify** MCP tools to pull live compensation data. This step is optional — skip it if the user doesn't need salary benchmarking.

**Do not** ask the user to paste their Apify token into chat, edit `claude_desktop_config.json`, or rely on `.env` / `APIFY_TOKEN` for MCP startup — Claude Desktop does not expand `${APIFY_TOKEN}` inside MCP `args` the way a shell would. **They** paste the token into the **Apify** connector form in the app—do not use browser automation to configure it.

First check if the Apify MCP is already connected. It may be in a deferred state, so double check and make sure to activate them if you need to. If they are active, suggest they run `/career-navigator:salary-research` for a role and location from their profile. If not, ask the user:
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

4. Validation: Confirm Apify tools are available (e.g. **Call Actor**, **Get Actor run**, **Get dataset items**). If tools need to be activated from a deferred state, then do that. If the tools are missing, summarize what they should double-check (token, enabled tools string, connector enabled, new session). If Apify is **already connected**, **do not** ask further questions about it.

**Cowork / other hosts:** If the user is not on Claude Desktop, tell them to add Apify MCP the way their host documents (same **Enabled tools** string and a secure token field if the UI offers one). Do not invent a JSON config that embeds the token.

**If no or skipped:**

> "No problem — salary benchmarking is off for now. You can set it up any time by running `/career-navigator:launch` again."

### 5. Offer LinkedIn post analytics (optional)

Apply **Connector pattern** (LinkedIn is usually **no** host MCP for this flow—**browser access** is the main lever).

After **Indeed** and **Apify** (or if the user skipped Apify), offer a **read-only** snapshot of **their own** LinkedIn post metrics into **`{user_dir}/CareerNavigator/tracker.json`** (`networking[]`, per **`linkedin-post-analytics`**). This is optional; do not run it without a clear **yes**.

**1 — Discover:** There is typically **no** LinkedIn MCP tool for this plugin path; note that analytics use **browser** access (step 3).

**2 — Configure:** **Ask** whether they are **logged into LinkedIn** in a browser profile the host can use; **they** sign in—do not automate LinkedIn login.

**3 — Browser access:** **Ask** whether they want **Claude in Chrome** and/or **computer use** for **read-only** LinkedIn analytics (**neither** / Chrome / computer use / both). If **neither**, do **not** run analytics in-browser; offer **schedule later** or skip.

Before running now or scheduling later, persist choices in `{user_dir}/CareerNavigator/profile.md` under `## LinkedIn`:
- `LinkedIn analytics permission: granted | denied`
- `LinkedIn analytics mode: chrome | computer | either`
If they pick **both**, save `mode: either`.

**Say something like:**

> **LinkedIn visibility (optional):** You can snapshot **your** post analytics into your career tracker (read-only). Which browser access should we use—**Claude in Chrome**, **computer use**, **both**, or **neither** (skip browser run for now)?  
> If you want a run **now** or **later** via **`/schedule`**, say so.

**If they choose run now** and approved **Chrome** and/or **computer use**:

1. Confirm the chosen tooling is available in the host. If **neither** was approved or tools are missing, do **not** scrape—explain they can enable tooling, log into LinkedIn, then run **`linkedin-post-analytics`** or **`/career-navigator:linkedin-post-analytics`** (or **continue** in a new chat).
2. If approved: follow **`skills/linkedin-post-analytics/SKILL.md`** end-to-end (ask for LinkedIn vanity slug if unknown, append snapshots to `tracker.json`, summarize).

**If they choose schedule later:** still save slug/permission/mode to `profile.md` now so unattended `/schedule` runs can execute without re-asking.

**If they skip or defer:**

> "Understood — run **`linkedin-post-analytics`** or **`/career-navigator:linkedin-post-analytics`** anytime, or add a **`/schedule`** task when you're ready. **`networking-strategist`** can remind you when you're working on visibility."

### 6. Connect Gmail / Microsoft 365 / Google Calendar for email & meeting context (optional)

Apply **Connector pattern**; **do not** prompt for **Gmail**, **Microsoft 365**, or **Google Calendar** if tools for that service are **already** in **this chat** (brief acknowledgment only).

After **Indeed**, **Apify**, and the **LinkedIn post analytics** offer (or skips), offer **Gmail** and/or **Microsoft 365** (inbox) and/or **Google Calendar** so **`draft-outreach`**, **`follow-up`**, and **`contact-context`** can search **read-only** mail and summarize **recent meetings** with a contact **when the user explicitly approves** each lookup.

**Step 2 only:** never automate **Connectors** with Chrome/computer-use tools. **Ask** if they want to set up or re-enable Gmail/M365/Calendar; if **yes**, they complete **Connectors** + OAuth **themselves** while you give instructions.

#### 6a. Gmail — check connection first

1. **Check this session:** Look at tools available in **this chat**. If any clearly belong to **Gmail** / Google mail (names often include `gmail`, `google`, or similar—exact strings vary by host), treat **Gmail as connected and enabled** for this session. Say so briefly (e.g. “Gmail looks connected here—great for inbox context when you approve a search”) and **do not** ask them to install Gmail again. Still offer **Microsoft 365** below if useful.

2. **If no Gmail tools appear:** You **cannot** see their **Connectors** screen from chat. Ask them to open **Customize** / **Settings** → **Connectors** and look at **Gmail**:
   - **Gmail not listed:** Use the normal “add + connect” path in step **6d** (first-time install).
   - **Gmail is listed but turned off** (toggle disabled, connector inactive, or equivalent): ask politely, e.g.  
     > “You already have the **Gmail** connector in Claude, but it’s not enabled right now. Would you like to **turn it on** for **read-only** access? Career Navigator only searches when **you approve** each lookup, and Anthropic’s Gmail integration doesn’t send mail on your behalf.”  
     If they **yes** → ask them to **enable** the toggle (or equivalent) **themselves** in **Connectors**, then **Connect** / re-auth if the UI asks, then start a **new chat** if tools still don’t load. **Do not** use **Claude in Chrome** or **computer use** to flip the toggle or complete OAuth.
   - **Gmail is listed but not signed in** (shows **Connect**, **Reconnect**, or disconnected state): ask politely, e.g.  
     > “Gmail is added but not connected to your Google account. Would you like to **set that up**—you’ll click **Connect** and finish Google sign-in in the browser tab Claude opens? Same **read-only** pattern—we only search when you say yes each time.”  
     If they **yes** → give the steps below; **they** click **Connect** and complete **OAuth** in the app (no passwords in chat).

3. **If they decline** enable/connect: respect that; note they can turn it on later in **Connectors**.

#### 6b. Microsoft 365 (unchanged pattern)

Offer **Microsoft 365** when relevant (see **6d**). Optional: if **Microsoft 365** tools are already in this session (including via project **`.mcp.json`** **`ms365`** → `https://microsoft365.mcp.claude.com/mcp` — Outlook/M365 as an **alternate** to Gmail/Google Calendar), acknowledge and skip redundant install instructions.

#### 6c. Google Calendar — check connection first

1. **Check this session:** Look at tools available in **this chat**. If any clearly belong to **Google Calendar** (names often include `calendar`, `google_calendar`, `gcal`, or similar—exact strings vary by host), treat **Google Calendar as connected and enabled** for this session. Say so briefly (e.g. “Google Calendar looks connected—great for meeting context when you approve a lookup”) and **do not** ask them to install Google Calendar again.

2. **If no Google Calendar tools appear:** You **cannot** see their **Connectors** screen from chat. Ask them to open **Customize** / **Settings** → **Connectors** and look at **Google Calendar**:
   - **Google Calendar not listed:** Use the normal “add + connect” path in step **6d** (first-time install).
   - **Google Calendar is listed but turned off** or shows **Connect** / **Reconnect**: ask politely, e.g.  
     > “You already have the **Google Calendar** connector in Claude, but it’s not enabled right now. Would you like to **turn it on**? Career Navigator only reads events **when you approve** each lookup—for example, prior calls with a hiring manager before you draft outreach.”  
     If they **yes** → they **enable** / **Connect** **themselves** in **Connectors**, finish **OAuth** if prompted, then start a **new chat** if tools still don’t load. **Do not** use **Claude in Chrome** or **computer use** to flip the toggle or complete OAuth.
   - **If they decline** enable/connect: respect that; note they can turn it on later in **Connectors**.

#### 6d. Generic email & calendar pitch (when connector state is unknown or user wants several)

If **6a** already confirmed **Gmail** tools in-session, **omit Gmail** from this pitch where redundant. If **6c** already confirmed **Google Calendar** tools in-session, **omit Google Calendar** from redundant install language—still offer **Microsoft 365** if missing.

**Say something like:**

> **Email & calendar context (optional):** If you want help remembering what you already said to recruiters or hiring managers—and **recent meetings** (calls, interviews) with them—you can connect **Gmail** and/or **Microsoft 365 (Outlook)** and/or **Google Calendar** through Claude’s **Connectors**. Auth is **OAuth** in the browser—no passwords in chat. Career Navigator only searches mail or reads calendar **when you say yes** to a specific lookup.  
> Want to **set up** **Gmail**, **Microsoft 365**, **Google Calendar**, **a combination**, or **skip** for now?

**If they want to set up (they do the clicks—do not use Chrome/computer-use tools to connect):**

1. **Customize** / **Settings** → **Connectors**.
2. **Gmail:** They open **Gmail** → **Connect** → finish **Google** sign-in and consent. Official docs: [Gmail integration](https://claude.com/docs/connectors/google/gmail) · [Google Workspace connectors](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors).
3. **Google Calendar:** They open **Google Calendar** → **Connect** → finish **Google** sign-in and consent (separate connector from Gmail). Official docs: [Google Calendar integration](https://claude.com/docs/connectors/google/calendar) · [Google Workspace connectors](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors).
4. **Microsoft 365 (includes Outlook; calendar/Teams surfaces per host):** They open **Microsoft 365** → **Connect** → finish **Microsoft** sign-in. **Team/Enterprise** and sometimes **admin setup** may be required—see [Microsoft 365 connector](https://claude.com/docs/connectors/microsoft/365) and [Enabling and using the Microsoft 365 connector](https://support.claude.com/en/articles/12542951-enabling-and-using-the-microsoft-365-connector). Security overview: [Microsoft 365 connector: Security Guide](https://support.claude.com/en/articles/12684923-microsoft-365-connector-security-guide).
5. After each connection, suggest a **new chat** if mail- or calendar-related tools do not appear.

**Validation:** If the host exposes Gmail, Microsoft 365, or Google Calendar tools, confirm they are listed/enabled. If the user’s **plan or org** does not include a connector, say so plainly and point to in-app **Connectors** catalog and [CONNECTORS.md](CONNECTORS.md). If those tools are **already** working, **do not** ask about browser access for mail or calendar—MCP in chat is enough.

**If skipped:**

> "No problem — outreach and follow-ups will work without inbox or calendar search. You can connect later under **Settings → Connectors** or run **`/career-navigator:launch`** again. Details: **CONNECTORS.md**."
