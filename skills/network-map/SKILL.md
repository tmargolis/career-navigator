---
name: network-map
description: "Maps plausible paths and gaps from the user to target employers—bridges, hypotheses, and dream-job leverage points. Outputs prose plus network_map_v1 JSON for a future visualization layer. Invokes networking-strategist."
triggers:
  - "network map"
  - "map my network"
  - "who can introduce me"
  - "dream job connections"
  - "path to company"
  - "introduction strategy"
  - "/career-navigator:network-map"
---

Invoke **`networking-strategist`** in **`network-map`** mode.

## Invocation

- Use the exact agent name **`networking-strategist`**. Retry once if invocation fails.

## Workflow

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

1. Read `{user_dir}/CareerNavigator/profile.md`, `tracker.json` (summary rows), and `ExperienceLibrary.json`.
   - **Known contacts (the confirmed nodes of the map):** contacts no longer live in `applications[]`. For each target application, take `contacts_file` from its summary row, load `{user_dir}/CareerNavigator/` + that path (`contacts/<company-slug>.json`), and filter `contacts[]` to entries whose `application` equals the row's `application` label. Never derive the slug yourself; a row without `contacts_file` has no contacts on file. One company file serves every application at that company, so the same person can appear more than once — **dedupe by `name`** so a person becomes one node, not several.
   - **Relationship evidence:** each matched contact's `relationship`, `title`, `notes`, and `interactions[]` are the confirmed edges. Open a row's `detail_file` (`applications/<application_id>.json`) for `notes[]` / `stage_history[]` only for the applications actually in play — the row's `latest_stage`, `latest_stage_date`, `notes_count`, `stage_count`, and `contact_count` usually answer the question without opening anything.
2. If the user names specific companies or contacts, include them as **confirmed**; everything else is **hypothesis** with confidence labels.
3. Require the agent to:
   - summarize **targets → paths → gaps** in readable form;
   - emit a **`network_map_v1`** JSON block per `agents/networking-strategist/AGENT.md`;
   - state explicitly that **graph visualization is deferred** to a later product iteration (the JSON is the interchange format).
4. Write or update `{user_dir}/CareerNavigator/network-map.md` with the narrative + fenced JSON when the user agrees to save (default: offer save after output).

## Future visualization

Do not render graphs in this skill. Preserve **`network_map_v1`** so a later visualization layer can render nodes/edges without re-inferring the map.
