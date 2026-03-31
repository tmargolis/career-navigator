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

## Objective

For **your own** posts only: open recent activity, collect per-post analytics, append **today’s** snapshot to `tracker.json` (`networking[]`), report a one-line summary per post.

## Inputs (ask once if missing)

- **Profile path:** LinkedIn vanity slug for `https://www.linkedin.com/in/{slug}/recent-activity/shares/`
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

One line per post: `[date] — [topic] — impressions: X, reactions: X, comments: X, reposts: X, link visits: X`. Flag posts with **meaningful day-over-day growth** vs the latest prior snapshot. If **no posts** in the window, say so and exit.

## Cadence hint for the user

Weekly or biweekly **`/schedule`** is enough for most job-search visibility loops.
