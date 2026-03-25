---
name: evaluate-offer
description: >
  Provides honest, scenario-aware evaluation of a job offer (employed vs
  unemployed context), including role fit, utilization analysis, compensation
  fairness using market benchmarks, and negotiation-readiness leverage points.
  Persists OfferContext for downstream negotiation/comparison.
triggers:
  - "evaluate my job offer"
  - "should i take this offer"
  - "offer evaluation"
  - "help me evaluate an offer"
  - "job offer assessment"
  - "/career-navigator:evaluate-offer"
---

Run `evaluate-offer` to produce an honest OfferEvaluationReport and persist an
`OfferContext` JSON file to:
`{user_dir}/CareerNavigator/offer-context-{application_id}.json`

so `negotiate-offer` and `compare-offers` can consume it later.

## Workflow

### Directory sharing (host integration)
If the host UI asks you for a **directory to share with an agent** during this
skill's run, share only your `{user_dir}` job-search folder (the one
containing `CareerNavigator/`).

This skill reads/writes:
- `{user_dir}/CareerNavigator/profile.md`
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`
- `{user_dir}/CareerNavigator/tracker.json`
- `{user_dir}/CareerNavigator/offer-context-{application_id}.json`

Do not share the whole workspace or unrelated folders.

### 1. Confirm required data exists
Read:
- `{user_dir}/CareerNavigator/profile.md`
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`
- `{user_dir}/CareerNavigator/tracker.json`

If missing required files, output:
> Offer evaluation skipped: run `/career-navigator:launch` to initialize `CareerNavigator/`.

### 2. Identify the offer-stage application
From `{user_dir}/CareerNavigator/tracker.json`, find applications where:
- `status` is `"offer"`

Cases:
- If exactly one such application exists: use it as `application_id`.
- If multiple exist: ask for the company and role (or the job link / deadline) and
  pick the matching application.
- If none exist: ask the user to log the offer first via `/career-navigator:track-application`.

### 3. Determine scenario A/B/C (do not ask user to self-identify)
Actively classify one of these scenarios:
- Scenario A: currently employed, evaluating a new offer (deciding whether to leave)
- Scenario B: currently not employed, evaluating an offer (urgency + runway)
- Scenario C: context unclear

Heuristics:
- If the profile has an `## Employment Context` section:
  - If it says employed (or lists a current comp package): use Scenario A.
  - If it says unemployed (or lists unemployment/severance/income sources + runway): use Scenario B.
  - If it says unknown: use Scenario C.
- Otherwise, if tracker/profile indicates current employment context is present in
  notes or recent stage history: use it.
- Otherwise, if the user explicitly states "I have a job" or "I'm between roles"
  in their message: use that.
- If still unclear: ask ONE clarifying question to resolve A vs B.

### 4. Extract/confirm offer details
Collect offer fields from either:
- the existing `tracker.json` offer fields for this `application_id` (if present)
- the user's message (for missing parts)

Fields to extract when available:
- base, bonus, equity, benefits notes
- deadline (`offer.deadline`) and any decision timing

If you cannot determine critical details (e.g., deadline or comp at all), ask
for just those missing items.

### 5. Market benchmark pass (comp fairness)
Hand off to **`market-researcher`** with a request for a compensation benchmark for:
- role + level (infer from profile and role title)
- geography scope (use profile location)
- company type (infer from the offer/company)

Instruction for the agent: if live compensation tooling is not available in this host,
produce a conservative, locally-grounded benchmark and label confidence.

Additionally, if the benchmark comes back with any `unknown`/missing range values
or confidence is not High, you must explicitly offer the user next step to
fetch it via `/career-navigator:salary-research` (and mention that it may
require the Apify connector in Claude Desktop) using the extracted role and
location.

### 6. Honest evaluation synthesis + leverage points
Hand off to **`honest-advisor`** to produce an **OfferEvaluationReport** covering:
- Role fit assessment (step forward/lateral/backward in trajectory)
- Utilization analysis of education/certifications/ExperienceLibrary units
- Compensation fairness determination (below/at/above market)
- Scenario-specific risk assessment (transition risk vs runway pressure)
- Direct recommendation: accept / decline / negotiate / continue searching

The report must include explicit leverage points (credentials, accomplishments,
ExperienceLibrary units) that justify above-median asks.

Instruct `honest-advisor` to:
- Follow the Phase 1F **OfferEvaluationReport** output structure.
- In “What would make this more reliable”, if any benchmark/market data is
  missing, either provide best-available benchmark values with a confidence
  caveat or explicitly offer the next steps to fetch them via:
  - `/career-navigator:salary-research` (role + location)
  - optionally `/career-navigator:market-brief` (for demand/AI outlook)

### 7. Persist `OfferContext` JSON
Write to:
`{user_dir}/CareerNavigator/offer-context-{application_id}.json`

Schema requirement (minimum fields; include more if helpful):
```json
{
  "schema": "offer_context_v1",
  "as_of": "{YYYY-MM-DD}",
  "application_id": "{application_id}",
  "company": "{company}",
  "role": "{role}",
  "scenario": "A|B|C",
  "offer_details": {
    "base": "...",
    "bonus": "...",
    "equity": "...",
    "benefits_notes": "...",
    "deadline": "YYYY-MM-DD|null"
  },
  "compensation_benchmark": {
    "currency": "USD|...",
    "percentile_or_range": "...",
    "market_range": { "low": "...", "median": "...", "high": "..." },
    "confidence": "Preliminary|Directional|Moderate|High",
    "notes": "..."
  },
  "leverage_points": [
    { "rank": 1, "claim": "...", "evidence": "ExperienceLibrary/profile references" }
  ],
  "evaluation_summary": "short 3–6 lines",
  "fairness_verdict": "below_market|at_market|above_market|borderline",
  "recommendation": "accept|decline|negotiate|continue_searching"
}
```

If write-to-disk fails:
- Do not fake a saved file.
- Show the OfferEvaluationReport plus the OfferContext JSON in a fenced code block
  and tell the user to save it manually to the path above.

### 8. Handoff to next step
If the report indicates negotiation is appropriate, prompt the user:
> Run `/career-navigator:negotiate` to draft a send-ready negotiation message.

If the compensation benchmark was missing/incomplete, also prompt:
> If you want tighter numbers, run `/career-navigator:salary-research` for this role + location and I can re-run the evaluation with the fetched benchmarks.

If multiple active offer-stage applications exist, also prompt:
> Run `/career-navigator:compare-offers` for side-by-side evaluation.

### 9. Present result
Present the conversational OfferEvaluationReport and confirm:
> Saved OfferContext to `{user_dir}/CareerNavigator/offer-context-{application_id}.json`.

