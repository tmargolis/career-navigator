---
name: market-brief
description: >
  Generates a market intelligence brief for the user's target roles, including
  role demand trends, AI/automation displacement signals, and geographic
  competitiveness context. Invokes the market-researcher agent.
triggers:
  - "market brief"
  - "job market trends"
  - "what does the market look like"
  - "market demand for my role"
  - "is this role in demand"
  - "ai displacement outlook"
  - "how competitive is my market right now"
  - "/career-navigator:market-brief"
---

Invoke the `market-researcher` agent to generate a current market intelligence brief grounded in the user's role targets and location preferences.

## Workflow

### 1. Confirm required context

Read `{user_dir}/profile/profile.md`.

If target roles are missing:
> "I need your target role(s) to generate a market brief. Run `/career-navigator:setup` (or update `profile/profile.md`) with your target roles first."

If location preferences are missing, continue but mark geographic confidence as limited.

Optionally read:
- `{user_dir}/tracker/tracker.json` for user-specific conversion/timeline signals
- `{user_dir}/corpus/index.json` for capability-fit context

### 2. Invoke market-researcher

Hand off to `market-researcher` with:
- The full `profile/profile.md`
- The full `tracker/tracker.json` (if present)
- The full `corpus/index.json` (if present)
- Instruction to include all three required sections:
  1. Role demand trends
  2. AI/automation displacement outlook
  3. Geographic competitiveness signals

If the user asks about a specific role/geography, prioritize that in the brief and treat other profile targets as secondary.

### 3. Present the brief

Render the returned output in this structure:

```
**Market Brief** — {today's date}
Target role(s): {list}
Geography: {scope}
Confidence: {Preliminary / Directional / Moderate / High}

HIGHLIGHTS
- Demand: {1 line}
- AI outlook: {1 line}
- Geography: {1 line}

ROLE DEMAND TRENDS
{role-by-role demand posture and implications}

AI/AUTOMATION DISPLACEMENT OUTLOOK
{high-risk vs durable task clusters + positioning shift}

GEOGRAPHIC SIGNALS
{market-by-market competitiveness and timeline implications}

PRIORITIZED NEXT MOVES (30-60 days)
1. ...
2. ...
3. ...
```

Keep the brief practical: concise, evidence-based, and directly tied to search decisions.

### 4. Suggest next step

Based on the top recommendation:
- If targeting shift is needed: suggest `/career-navigator:search-jobs` with refined role/location filters.
- If narrative shift is needed: suggest `/career-navigator:assessment` and then `/career-navigator:tailor-resume`.
- If execution cadence is the issue: suggest `/career-navigator:follow-up` and `/career-navigator:track-application`.

