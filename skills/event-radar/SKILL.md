---
name: event-radar
description: "Discovers networking events across local, regional, national, and international scopes with ROI tiers and presentation flags. Invokes networking-strategist."
triggers:
  - "event radar"
  - "upcoming conferences"
  - "networking events near me"
  - "meetups for my role"
  - "events this quarter"
  - "/career-navigator:event-radar"
---

Invoke **`networking-strategist`** in **`event-radar`** mode.

## Invocation

- Use the exact agent name **`networking-strategist`**. Retry once if invocation fails.

## Workflow

1. Read `{user_dir}/CareerNavigator/profile.md` for location, remote openness, target roles, and industries.
2. Instruct the agent to scan **local → regional → national → international** as appropriate (skip international if profile is strictly local-only).
3. Prefer **official sites** and **verifiable listings**; when tools are missing, output **search queries** and **what to verify** instead of fabricating events.
4. Deliver grouped results (by scope) with **ROI tier A/B/C**, **presentation opportunity** flag, and links.
5. Offer to write `{user_dir}/CareerNavigator/event-radar.md` including an **`event_radar_v1`** JSON block for downstream use.

## Scheduling (Claude Cowork)

**Monthly** `/schedule` is reasonable for active searchers attending events; reduce cadence if passive.
