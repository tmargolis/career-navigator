---
name: compare-offers
description: >
  Compares multiple active offer-stage applications with side-by-side
  compensation, role fit, scenario-specific risk, and trajectory alignment.
  Produces an honest ranking and prompts negotiation handoff.
triggers:
  - "compare offers"
  - "compare job offers"
  - "which offer should i take"
  - "side by side offer comparison"
  - "/career-navigator:compare-offers"
---

Run `compare-offers` to produce an **OfferComparisonReport** across all active
offer-stage applications in the tracker, using persisted OfferContext files when
available (from `evaluate-offer`).

## Workflow

### Directory sharing (host integration)
If the host UI asks you for a **directory to share with an agent** during this
skill's run, share only your `{user_dir}` job-search folder (the one
containing `CareerNavigator/`).

This skill reads:
- `{user_dir}/CareerNavigator/profile.md`
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`
- `{user_dir}/CareerNavigator/tracker.json`
- `{user_dir}/CareerNavigator/offer-context-{application_id}.json` (if present)

Do not share the whole workspace or unrelated folders.

### 1. Confirm required data exists
Read:
- `{user_dir}/CareerNavigator/profile.md`
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`
- `{user_dir}/CareerNavigator/tracker.json`

If missing, output:
> Compare-offers skipped: run `/career-navigator:launch` to initialize `CareerNavigator/`.

### 2. Load all offer-stage applications
From `{user_dir}/CareerNavigator/tracker.json`, select applications where:
- `status` is `"offer"`

If none exist, output:
> No active offers found in your tracker. Log an offer first via `/career-navigator:track-application`.

### 3. Load OfferContext per application; evaluate inline if missing
For each offer application:
- set `offer_context_path = {user_dir}/CareerNavigator/offer-context-{application_id}.json`
- if it exists: load it
- if it does not exist: run the evaluation logic inline:
  - use `honest-advisor` + `market-researcher` to produce OfferEvaluationReport
  - then persist the OfferContext JSON to the expected path

If inline evaluation cannot be performed due to missing details, ask the user
for the minimum missing offer basics and proceed with partial comparisons.

### 4. Trajectory alignment integration
If `{user_dir}/CareerNavigator/career-trajectory.md` exists:
- read and extract the `career_trajectory_v1` JSON block
- use near-term trajectory roles (0–18 months) to label each offer's
  trajectory alignment as: `high|medium|low`

If missing:
- trajectory alignment becomes `unknown` and is explicitly labeled as such.

### 5. Produce OfferComparisonReport
Using all loaded OfferContext objects, synthesize:
- Side-by-side compensation table (base/bonus/equity/sign-on/total, plus benchmark gap)
- Role fit matrix (trajectory alignment, utilization analysis, seniority match, profile targeting)
- Risk comparison (scenario-specific risks; deadline pressure affects evaluation order)
- Trajectory alignment section (tie back to `career_trajectory_v1` if present)
- Honest recommendation ranking:
  - If one is clearly superior: rank it #1 and explain why
  - If genuinely close: identify the top 1–2 tiebreakers and let the user decide

### 6. Prompt negotiation handoff
If the preferred offer is below market or negotiable:
> Run `/career-navigator:negotiate` to draft a send-ready counter/ask.

If negotiation is likely unnecessary:
> Run `/career-navigator:negotiate` only if you want polish on wording or timing.

### 7. Present result
Present the report in chat.

