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

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

1. Read `{user_dir}/CareerNavigator/profile.md`, `tracker.json` (summary rows), and `ExperienceLibrary.json`.
   - **Existing relationships:** contacts are no longer inside `applications[]`. For each application you are planning around, take `contacts_file` from its summary row, load `{user_dir}/CareerNavigator/` + that path (`contacts/<company-slug>.json`), and filter `contacts[]` to entries whose `application` equals the row's `application` label. Never derive the slug yourself; a row without `contacts_file` has no contacts. One company file serves every application at that company, so **dedupe by `name`** before presenting a relationship map or a warm-path list to the user.
   - **Pipeline context:** the summary rows' `status`, `latest_stage`, `latest_stage_date`, `notes_count`, `stage_count`, and `contact_count` are usually enough to prioritize. Open a row's `detail_file` (`applications/<application_id>.json`) for `notes[]` / `stage_history[]` only for the applications actually in play.
2. Pass the user’s stated goal (if any): target role, dream companies, or timeline.
3. Ask the agent for: **90-day plan**, **top 5 relationship moves**, **what not to do**, and—when messages are needed—a **handoff brief for `writer`** (objective, audience, hooks, tone, avoid list) per `agents/networking-strategist/AGENT.md`. Direct the user to **`writer`** or **`/career-navigator:draft-outreach`** for actual LinkedIn/email copy.
4. Offer to persist a summary to `{user_dir}/CareerNavigator/networking-strategy.md` (create or append dated section) when the user wants a durable reference.

## Scheduling (Claude Cowork)

`networking-strategy` benefits from a **monthly** `/schedule` refresh after major tracker or target changes.
