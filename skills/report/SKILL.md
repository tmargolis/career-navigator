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

### 1.5 Ensure ATS scores exist (resume artifacts)

Read `{user_dir}/artifacts-index.json`.

If any artifact with `type: "resume"` is missing `ats_score` (or has `ats_score: null`):

- Invoke `resume-score` for that resume artifact (reference its `filename` so the skill can look it up and run the ATS check pass).
- If keyword coverage can’t be computed due to missing JD context, still proceed with formatting/narrative ATS checks and write whatever `ats_score` the ATS pass can compute.
- Re-check `{user_dir}/artifacts-index.json` after the ATS pass(es). If scores are still missing, note the remaining ATS gaps in the report highlights.

### 2. Invoke analyst — all four operations

Hand off to the `analyst` agent with:
- The full `tracker/tracker.json`
- The full `corpus/index.json`
- The full `artifacts-index.json`
- The full `profile/profile.md`
- Instruction to read `references/AI_Job_Report-Anthropic-2026-03.pdf` before the displacement assessment
- Instruction to run all four operations: outcome patterns (Op 1), transferable strengths (Op 2), AI displacement (Op 3), market benchmark (Op 4)
- Instruction: return graph-ready data in addition to the narrative, suitable for writing to `{user_dir}/analysis/analyst-graph-data.json`, using this schema:
  - `ai_displacement_outlook`: `{overall_risk, exposure_min_pct, exposure_max_pct, durable_min_pct, durable_max_pct, durable_differentiators[], narrative_reframe}`
  - `transferable_strengths`: array of `{name, rating, score_0_100, evidence, destinations[]}`

### 3. Present the integrated report

In the text report, include only `HIGHLIGHTS`, `PART 1: WHAT'S WORKING IN YOUR SEARCH`, and `RECOMMENDED NEXT ACTIONS`. Do not output `PART 2`/`PART 3`/`PART 4` sections; instead direct the user to the pipeline dashboard for the AI displacement + transferable strengths graphs and for pipeline/benchmark details.

```
**Analyst Report** — {today's date}

HIGHLIGHTS
- Search:      {1-sentence verdict on what's working or not}
- Strengths:   {1-sentence on the most transferable capability}
- AI outlook:  {1-sentence on overall displacement risk posture}
- vs. Market:  {1-sentence on how pipeline metrics compare to norm for this level and market}
- ATS status:  {1-liner on whether `ats_score` exists for your resume artifacts (and remaining gaps)}

---

PART 1: WHAT'S WORKING IN YOUR SEARCH
{1–2 sentence highlight for the single most actionable outcome-pattern finding}
{Short detail (3–6 bullets) capturing: what the data shows, what it doesn't show yet, and the 1–2 biggest pipeline bottlenecks}

Corpus weights updated: {n} changed ({n} up, {n} down)
Data confidence: {Preliminary / Directional / Moderate / High}

Note: The AI displacement + transferable strengths graphs (and pipeline funnel/benchmark + corpus weights) are interactive in your pipeline dashboard, so I’m not duplicating those charts/tables in the text report.

---

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

### 4. Write dashboard graph data (AI displacement + transferable strengths)

Write `{user_dir}/analysis/analyst-graph-data.json` (create `{user_dir}/analysis/` if needed) using the graph-ready data returned by the analyst agent in step 2.

Required JSON keys:
- `ai_displacement_outlook`
- `transferable_strengths`

If any field is missing due to insufficient data, set it to `null` (or `[]`) so the dashboard shows placeholders instead of failing.

Dashboard subkeys (when available):
- `ai_displacement_outlook`: `overall_risk`, `exposure_min_pct`, `exposure_max_pct`, `durable_min_pct`, `durable_max_pct`
- `transferable_strengths[]`: `name`, `rating`, `score_0_100` (plus optional `evidence` and `destinations[]`)

### 5. Generate the pipeline dashboard

After presenting the text report, invoke the `pipeline-dashboard` skill. It will read the same data files, build the visualization, write `{user_dir}/pipeline-dashboard.html`, and open it in the browser automatically.

Do not wait for the user to ask — generate it every time the report runs.

### 6. Suggest next step

Based on the most prominent finding across all four analyses:
- If any ATS scores are weak: > "Run `/career-navigator:ats-optimization` on specific resumes that could be improved."
- If search patterns are weak: > "Run `/career-navigator:tailor-resume` using the updated corpus weights."
- If transferable strengths suggest a pivot: > "Run `/career-navigator:search-jobs` targeting {role type}."
- If AI risk is high in current positioning: > "Run `/career-navigator:cover-letter` to try a reframed narrative."
- If pipeline metrics are below norm: > "Run `/career-navigator:benchmark` for the full breakdown with targeted fixes."
