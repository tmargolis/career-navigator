---
name: event-intelligence
description: "Evaluates specific conferences and meetups for networking ROI, audience fit, cost-time tradeoffs, and presentation or speaking opportunities. Invokes networking-strategist."
triggers:
  - "event intelligence"
  - "should I go to this conference"
  - "conference ROI"
  - "speaking opportunity"
  - "CFP worth submitting"
  - "which event should I attend"
  - "/career-navigator:event-intelligence"
---

Invoke **`networking-strategist`** in **`event-intelligence`** mode.

## Invocation

- Use the exact agent name **`networking-strategist`**. Retry once if invocation fails.

## Workflow

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

1. Read `{user_dir}/CareerNavigator/profile.md` and skim `tracker.json` — summary rows alone give target companies, roles, `status`, and `latest_stage`, which is all this skill normally needs. Do not open `detail_file` unless a specific application's notes or stage history bear on the event decision.
   - **If you need to know who the user already knows at a company** (e.g. to judge whether an event adds reach), take `contacts_file` from that company's summary row, load `{user_dir}/CareerNavigator/` + that path (`contacts/<company-slug>.json`), and filter `contacts[]` to entries whose `application` equals the row's `application` label. One company file serves every application at that company — **dedupe by `name`** when listing who is already in the user's network.
2. From conversation, extract **event name(s)** or **category** (e.g. “ML product conferences Q3”) and **user constraints** (budget, travel, PTO).
3. Use available web/search or event tools to verify dates, location, and official URL—do not invent dates or prices.
4. Ask the agent for: **ROI tier**, **audience assessment**, **presentation opportunity flag** (`yes` / `maybe` / `no`) with rationale, **risks** (pay-to-play, low signal), and **go/no-go** recommendation.
5. Optionally append an **`event_radar_v1`** JSON subset (single event or small list) to `{user_dir}/CareerNavigator/event-radar.md` or `network-map.md` per agent guidelines.

## Scheduling (Claude Cowork)

Optional **quarterly** `/schedule` pass before peak conference season if the user targets role-types with strong event hiring channels.
