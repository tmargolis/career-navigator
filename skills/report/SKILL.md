---
name: report
description: >
  Runs all four analyst operations — outcome pattern analysis, transferable
  strengths, AI displacement assessment, and market benchmark — and delivers
  a unified insight report followed by an interactive D3 pipeline dashboard
  opened in the browser. The integrated view of the user's search health,
  career capital, future positioning, and how their metrics compare to
  industry norms. Invokes the analyst agent and pipeline-dashboard skill.
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

### 2. Invoke analyst — all four operations

Hand off to the `analyst` agent with:
- The full `tracker/tracker.json`
- The full `corpus/index.json`
- The full `artifacts-index.json`
- The full `profile/profile.md`
- Instruction to read `references/AI_Job_Report-Anthropic-2026-03.pdf` before the displacement assessment
- Instruction to run all four operations: outcome patterns (Op 1), transferable strengths (Op 2), AI displacement (Op 3), market benchmark (Op 4)

### 3. Present the integrated report

```
**Analyst Report** — {today's date}

HIGHLIGHTS
- Search:      {1-sentence verdict on what's working or not}
- Strengths:   {1-sentence on the most transferable capability}
- AI outlook:  {1-sentence on overall displacement risk posture}
- vs. Market:  {1-sentence on how pipeline metrics compare to norm for this level and market}

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

PART 4: BENCHMARK vs. INDUSTRY NORMS
{1–2 sentence section highlight — are metrics above or below norm for this level and market?}

  Pipeline ({level} · {primary company size} · {geography})
    App → Response:     {user%}  norm {low–high%}  {▲ above / ▼ below / — at norm}
    Response → Screen:  {user%}  norm {low–high%}  {▲/▼/—}
    Screen → Interview: {user%}  norm {low–high%}  {▲/▼/—}
    Interview → Offer:  {user%}  norm {low–high%}  {▲/▼/—}
    Avg days to response: {n}d   norm {low–high}d  {▲/▼/—}
    Ghosting rate:      {user%}  norm {low–high%}  {▲/▼/—}

  ATS Scores
    Avg: {n}/100  ·  threshold: 70+  ·  {above/below}
    Lowest: {score} — {filename}

  {1–2 sentences on compensation positioning vs. level and company size norms, or note to run salary-research if no data}

---

RECOMMENDED NEXT ACTIONS
1. {Most impactful action, drawing on all four analyses}
2. ...
```

### 4. Generate the pipeline dashboard

After presenting the text report, invoke the `pipeline-dashboard` skill. It will read the same data files, build the visualization, write `{user_dir}/pipeline-dashboard.html`, and open it in the browser automatically.

Do not wait for the user to ask — generate it every time the report runs.

### 5. Suggest next step

Based on the most prominent finding across all four analyses:
- If search patterns are weak: > "Run `/career-navigator:tailor-resume` using the updated corpus weights."
- If transferable strengths suggest a pivot: > "Run `/career-navigator:search-jobs` targeting {role type}."
- If AI risk is high in current positioning: > "Run `/career-navigator:cover-letter` to try a reframed narrative."
- If pipeline metrics are below norm: > "Run `/career-navigator:benchmark` for the full breakdown with targeted fixes."
