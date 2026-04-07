---
name: linkedin-post-analytics
description: >
  Read-only snapshot of the user's own LinkedIn post analytics into tracker.json networking entries.
  Requires browser control (Claude in Chrome MCP or approved computer/browser use). Scheduled-friendly.
triggers:
  - "linkedin post analytics"
  - "linkedin-post-analytics"
  - "snapshot linkedin analytics"
  - "append linkedin analytics to tracker"
  - "/career-navigator:linkedin-post-analytics"
---

## Gate (run first)

1. **Pattern:** [CONNECTORS.md](CONNECTORS.md) **three-step** for this integration: **Discover** — no standard LinkedIn MCP here; **Configure** — user **logged into LinkedIn** in the host browser (**they** sign in); **Browser access** — **ask** **Claude in Chrome** and/or **computer use** (**neither** / one / both). If **neither** or no tooling, **stop**—do **not** scrape without **read-only** approval for the chosen mode(s).
2. **`{user_dir}`:** Resolve the job-search folder; tracker is `{user_dir}/CareerNavigator/tracker.json`.
3. **Scheduled unattended runs:** If this invocation came from `/schedule` (or user asked for unattended), do **not** ask interactive browser/tooling questions. Continue only when prior consent is already saved in `{user_dir}/CareerNavigator/profile.md` under `## LinkedIn`:
   - `LinkedIn slug: <value>`
   - `LinkedIn analytics permission: granted`
   - `LinkedIn analytics mode: chrome | computer | either`
   If any of these are missing, stop with a concise setup message telling the user to run one interactive setup once.

## Tool-call guidance

**Preferred order:** for **interactive** runs, use the user-approved mode (`chrome`, `computer`, or `either`). If mode is `either`, try **Claude in Chrome** first, then computer.

**Claude in Chrome path (strict, typed params):**
- First try `tabs_context_mcp` with correctly typed values (for example, `createIfEmpty` must be the boolean `true`, not the string `"true"`).
- If context initialization still fails, call `tabs_create_mcp`, then retry `tabs_context_mcp` once.
- Then call `navigate` to the LinkedIn URL.
- If `navigate` fails because `tabId` is typed incorrectly, retry once with a numeric `tabId` (integer, not quoted).
- If still failing, stop with: "Claude in Chrome couldn't initialize a valid tab context. Open Chrome, confirm you're signed into LinkedIn, and rerun `linkedin-post-analytics`."

**No circular fallback loops:**
- At most one retry per failing step.
- Do not bounce between tools repeatedly.
- If chosen mode fails, only try the alternate mode when the saved/approved mode is `either`.

## Objective

For **your own** posts only: open recent activity, collect per-post analytics, append **today’s** snapshot to `tracker.json` (`networking[]`), report a one-line summary per post.

## Inputs (ask once if missing)

- **Profile path:** Read `{user_dir}/CareerNavigator/profile.md` → `## LinkedIn` → `LinkedIn slug:`. If present, use it. If missing or blank, ask once and save it back to `profile.md` under that heading before proceeding.
- **Consent state (persist):** For interactive runs, if missing, ask once and save:
  - `LinkedIn analytics permission: granted | denied`
  - `LinkedIn analytics mode: chrome | computer | either`
  Scheduled runs require `permission: granted` plus a mode.
- **Window:** default posts from the **last ~60 days** (or user’s “several months” if they state it)

## Steps

1. Navigate to the **recent activity / shares** URL above. User should already be logged in; if LinkedIn demands re-auth, **stop** and notify them.
2. **Read-only:** do not post, react, comment, or DM. If a post’s analytics control is missing or the panel errors, **note and skip** that post.
3. For each post in the window: capture **post URL** (`…/feed/update/urn:li:activity:…`), **date posted** (best effort), **topic** (short label). Open **View analytics** (bar chart) and read: impressions, members reached, reactions, comments, reposts, saves, sends on LinkedIn, profile viewers from post, followers gained, link visits, plus top audience (industry / seniority / company size) **if shown**.
4. Read `tracker.json`. For each post:
   - If `networking` has `type: "linkedin_post"` and matching `url`: append to `analytics_history` one object: `{ "date": "YYYY-MM-DD", …metrics… }` (same field names as below).
   - Else create a new entry: `id` = next `net-NNN` (max existing + 1), `type: "linkedin_post"`, `description`, `url`, `date_posted`, `analytics_history: [ { … } ]`, `notes` (e.g. auto-discovered + date), `outcome: "active"`.
5. Write `tracker.json` back. Preserve unrelated keys (`applications`, etc.).

**`analytics_history` object (use 0 or `[]` / `"—"` when unknown):**

`impressions`, `members_reached`, `reactions`, `comments`, `reposts`, `saves`, `sends`, `profile_viewers_from_post`, `followers_gained`, `link_visits`, `links` (array), `top_audience`: `{ "industry", "seniority", "company_size" }` (strings).

## Report

One line per post: `[topic], impressions: X(+Y), reactions: X(+Y), comments: X(+Y), reposts: X(+Y), link visits: X(+Y), [date]`. Flag posts with **meaningful day-over-day growth** (Y) vs the latest prior snapshot. If **no posts** in the window, say so and exit.

## Cadence hint for the user

For users who granted permission and saved mode, morning **`/schedule`** runs are supported. Weekly or biweekly cadence is enough for most job-search visibility loops, but daily is acceptable during active networking pushes.
