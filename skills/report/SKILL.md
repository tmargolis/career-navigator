---
name: report
description: >
  Runs all three analyst operations — outcome pattern analysis, transferable
  strengths, and AI displacement assessment — and delivers a unified insight
  report. The integrated view of the user's search health, career capital, and
  future positioning. Invokes the analyst agent.
triggers:
  - "run the analyst"
  - "analyst report"
  - "full analyst report"
  - "run full analysis"
  - "give me an analyst report"
  - "run all three analyses"
  - "full career analysis"
  - "show me the full report"
---

Invoke the `analyst` agent to run all three operations and deliver the integrated insight report.

## Workflow

### 1. Confirm data exists

Read `{user_dir}/tracker/tracker.json`, `{user_dir}/corpus/index.json`, `{user_dir}/profile/profile.md`, and `{user_dir}/artifacts-index.json`. If the corpus is empty:

> "Your experience corpus is empty. Run `/career-navigator:add-source` to add a resume first."

If the tracker has no applications, note this inline — pattern analysis will be limited but the other two operations can still run.

### 2. Invoke analyst — all three operations

Hand off to the `analyst` agent with:
- The full `tracker/tracker.json`
- The full `corpus/index.json`
- The full `artifacts-index.json`
- The full `profile/profile.md`
- Instruction to read `references/AI_Job_Report-Anthropic-2026-03.pdf` before the displacement assessment

The agent will run Operation 1 (outcome patterns + weight updates), Operation 2 (transferable strengths), and Operation 3 (AI displacement), then return results for all three.

### 3. Present the integrated report

```
**Analyst Report** — {today's date}

HIGHLIGHTS
- Search:     {1-sentence verdict on what's working or not}
- Strengths:  {1-sentence on the most transferable capability}
- AI outlook: {1-sentence on overall displacement risk posture}

---

PART 1: WHAT'S WORKING IN YOUR SEARCH
{1–2 sentence section highlight before detail}
{Outcome pattern findings — lead with the most actionable finding}

Corpus weights updated: {n} changed ({n} up, {n} down)
Data confidence: {Preliminary / Directional / Moderate / High}

---

PART 2: YOUR TRANSFERABLE STRENGTHS
{1–2 sentence section highlight before detail}
{Core capabilities and non-obvious destinations}

---

PART 3: AI DISPLACEMENT OUTLOOK
{1–2 sentence section highlight before detail}
{Risk profile for current and target roles, durable differentiators, narrative reframe}

---

RECOMMENDED NEXT ACTIONS
1. {Most impactful thing to change or do, based on all three analyses}
2. ...
```

### 4. Suggest next step

Based on the most prominent finding, suggest one specific follow-on action:
- If search patterns are weak: > "Run `/career-navigator:tailor-resume` using the updated corpus weights."
- If transferable strengths suggest a pivot: > "Run `/career-navigator:search-jobs` targeting {role type}."
- If AI risk is high in current positioning: > "Run `/career-navigator:cover-letter` to try a reframed narrative."
