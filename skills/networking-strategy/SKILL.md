---
name: networking-strategy
description: "Builds an evidence-based networking plan for target roles—priorities, sequencing, warm paths, and gap fixes. Outreach copy is handled by writer. Invokes networking-strategist."
triggers:
  - "networking strategy"
  - "who should I network with"
  - "how should I network"
  - "job search networking plan"
  - "warm intros"
  - "informational interviews"
  - "/career-navigator:networking-strategy"
---

Invoke **`networking-strategist`** in **`networking-strategy`** mode.

## Invocation

- Use the exact agent name **`networking-strategist`**. If invocation fails, retry once with the same name before reporting an error.

## Workflow

1. Read `{user_dir}/CareerNavigator/profile.md`, `tracker.json`, and `ExperienceLibrary.json`.
2. Pass the user’s stated goal (if any): target role, dream companies, or timeline.
3. Ask the agent for: **90-day plan**, **top 5 relationship moves**, **what not to do**, and—when messages are needed—a **handoff brief for `writer`** (objective, audience, hooks, tone, avoid list) per `agents/networking-strategist/AGENT.md`. Direct the user to **`writer`** or **`/career-navigator:draft-outreach`** for actual LinkedIn/email copy.
4. Offer to persist a summary to `{user_dir}/CareerNavigator/networking-strategy.md` (create or append dated section) when the user wants a durable reference.

## Scheduling (Claude Cowork)

`networking-strategy` benefits from a **monthly** `/schedule` refresh after major tracker or target changes.
