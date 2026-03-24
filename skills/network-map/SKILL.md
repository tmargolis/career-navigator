---
name: network-map
description: "Maps plausible paths and gaps from the user to target employers—bridges, hypotheses, and dream-job leverage points. Outputs prose plus network_map_v1 JSON for a future visualization phase. Invokes networking-strategist."
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

1. Read `{user_dir}/CareerNavigator/profile.md`, `tracker.json`, and `ExperienceLibrary.json`.
2. If the user names specific companies or contacts, include them as **confirmed**; everything else is **hypothesis** with confidence labels.
3. Require the agent to:
   - summarize **targets → paths → gaps** in readable form;
   - emit a **`network_map_v1`** JSON block per `agents/networking-strategist/AGENT.md`;
   - state explicitly that **graph visualization is deferred** to a later product phase (the JSON is the interchange format).
4. Write or update `{user_dir}/CareerNavigator/network-map.md` with the narrative + fenced JSON when the user agrees to save (default: offer save after output).

## Future visualization

Do not render graphs in Phase 1E. Preserve **`network_map_v1`** so a later phase can render nodes/edges without re-inferring the map.
