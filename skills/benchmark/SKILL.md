---
name: benchmark
description: >
  Benchmarks the user's pipeline conversion rates, response timelines, ATS
  scores, and compensation positioning against industry norms segmented by
  role, level, company size, and geography. Invokes analyst Operation 4.
triggers:
  - "how does my search compare"
  - "benchmark my search"
  - "benchmark my numbers"
  - "am I above average"
  - "am I below average"
  - "how are my response rates"
  - "how do my numbers look"
  - "how does my pipeline compare"
  - "how am I doing compared to other candidates"
  - "what's a normal response rate"
  - "is my conversion rate good"
  - "how long does it usually take to get an offer"
  - "how competitive is my market"
---

Benchmark the user's pipeline performance against industry norms for their role, level, company size, and geography.

## Workflow

### 1. Check data threshold

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

Read `{user_dir}/CareerNavigator/tracker.json`. Count the total number of applications (any status) from the summary rows — no detail files needed for this check. If fewer than 5:

> "You need at least 5 applications to run a meaningful benchmark — you have {n} so far. Keep logging applications via `/career-navigator:track-application` and run this again once you have more history."

Stop here if below threshold.

If ≥5 but fewer than 10 resolved outcomes, proceed with a note that results are preliminary.

### 2. Load the stage history the conversion math needs

Every PIPELINE CONVERSION and TIMELINES figure below is computed from `stage_history[]`, and **`tracker.json` alone contains no stage history** — it moved to the per-application detail files. Computing app → response, screen → interview, interview → offer, or days-to-response from `tracker.json` by itself silently yields zeros and reports the user as far below norm when they are not.

1. Read `{user_dir}/CareerNavigator/tracker.json` and take `applications[]`.
2. Iterate every row and load its `detail_file` (relative to `CareerNavigator/`) for that application's `stage_history[]`. Skip a row only when its `stage_count` is `0` — that row genuinely has no stages to count.
3. Use the summary fields where they answer the question directly: `latest_stage` and `latest_stage_date` give the current funnel position and last movement date, and `stage_count` / `notes_count` / `contact_count` give volumes without a read.

### 3. Invoke analyst — Operation 4

Hand off to the `analyst` agent with:
- `CareerNavigator/tracker.json` (summary rows) **plus** the loaded `applications/<application_id>.json` detail files — pass both; conversion and timeline math is impossible from summary rows alone
- The full `CareerNavigator/artifacts-index.json`
- The full `CareerNavigator/profile.md`
- Instruction to run Operation 4: Market Benchmark

### 4. Present the benchmark report

Use the output from the analyst to render:

```
**Benchmark Report** — {today's date}
Data confidence: {Preliminary / Directional / Moderate / High} ({n} applications, {n} resolved outcomes)

PIPELINE CONVERSION
  App → Response:       {user%}  (norm: {low}–{high}%  ·  {above/below/at norm})
  Response → Screen:    {user%}  (norm: {low}–{high}%  ·  {above/below/at norm})
  Screen → Interview:   {user%}  (norm: {low}–{high}%  ·  {above/below/at norm})
  Interview → Offer:    {user%}  (norm: {low}–{high}%  ·  {above/below/at norm})

TIMELINES
  Avg days to response: {n} days  (norm: {low}–{high} days for {company size mix})
  Ghosting rate:        {user%}  (norm: {low}–{high}%  ·  {above/below/at norm})

ATS SCORES
  Avg artifact score:   {n}/100  (competitive threshold: 70+  ·  {above/below})
  Lowest artifact:      {score} — {filename}

MARKET CONTEXT
  {1–2 sentences on geographic competitiveness and role-level supply/demand for user's target}

GAPS TO ADDRESS
  {Numbered list of the 1–3 metrics most below norm, with a one-line interpretation each}

STRENGTHS
  {1–2 metrics above norm — acknowledge what's working}
```

If a metric cannot be calculated (e.g., no offers yet, so interview → offer rate is undefined), show `—` and note why.

### 5. Suggest next step

Based on the lowest-performing metric:

- App → Response below norm: > "Your resume may not be clearing ATS or targeting JDs closely enough. Run `/career-navigator:resume-score` against your weakest-performing artifact."
- Response → Screen or Screen → Interview below norm: > "Your materials are getting in — the issue is later in the funnel. Run `/career-navigator:pattern-analysis` to see which ExperienceLibrary units are in stalled applications."
- Timelines slow across the board: > "Long timelines are common for enterprise roles. Check `/career-navigator:track-application` to ensure follow-ups are scheduled."
- ATS scores below 70: > "Run `/career-navigator:ats-optimization` to surface the highest-impact fixes on your active artifacts."
