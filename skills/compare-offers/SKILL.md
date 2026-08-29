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
- `{user_dir}/CareerNavigator/tracker.json` (summary rows)
- `{user_dir}/CareerNavigator/applications/<application_id>.json` (one per offer being compared)
- `{user_dir}/CareerNavigator/contacts/<company-slug>.json` (only when naming the person to negotiate with)
- `{user_dir}/CareerNavigator/offer-context-{application_id}.json` (if present)

Do not share the whole workspace or unrelated folders.

### 1. Confirm required data exists

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

Read:
- `{user_dir}/CareerNavigator/profile.md`
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`
- `{user_dir}/CareerNavigator/tracker.json`

If missing, output:
> Compare-offers skipped: run `/career-navigator:launch` to initialize `CareerNavigator/`.

### 2. Load all offer-stage applications
From the `tracker.json` summary rows, select applications where:
- `status` is `"offer"`

If none exist, output:
> No active offers found in your tracker. Log an offer first via `/career-navigator:track-application`.

For **each selected offer only** — never for the rest of the pipeline — read
`{user_dir}/CareerNavigator/` + the row's `detail_file`. The comparison reasons over the
full interview and negotiation history in `stage_history[]` and `notes[]`, and neither
array exists in `tracker.json` any more; comparing from the summary rows alone produces
offers with no history behind them. Keep each row's `application` label, `latest_stage`,
`latest_stage_date`, `contacts_file`, and `contact_count` alongside the detail.

When the comparison needs the person on the other side of an offer (recruiter, hiring
manager), read `{user_dir}/CareerNavigator/` + that row's `contacts_file`, keep only
entries whose **`application`** equals the row's **`application`** label, and **dedupe by
`name`** — one company file serves every application at that company. A row with no
`contacts_file` has no contacts on file; do not derive a slug yourself.

### 3. Load OfferContext per application; evaluate inline if missing
For each offer application:
- set `offer_context_path = {user_dir}/CareerNavigator/offer-context-{application_id}.json`
  (use the row's `id`; if nothing is there, check the row's `previous_ids` before deciding
  the context is missing)
- if it exists: load it
- if it does not exist: run the evaluation logic inline:
  - use `honest-advisor` + `market-researcher` to produce OfferEvaluationReport
  - then persist the OfferContext JSON to the expected path

If inline evaluation cannot be performed due to missing details, ask the user
for the minimum missing offer basics and proceed with partial comparisons.

### 4. Trajectory alignment integration
If `{user_dir}/CareerNavigator/career-trajectory-data.json` exists:
- read it as `career_trajectory_v1`
- use near-term trajectory roles (0–18 months) to label each offer's
  trajectory alignment as: `high|medium|low`

If missing:
- trajectory alignment becomes `unknown` and is explicitly labeled as such.

### 5. Produce OfferComparisonReport
Using all loaded OfferContext objects, synthesize:
- Side-by-side compensation table (base/bonus/equity/sign-on/total, plus benchmark gap)
- Role fit matrix (trajectory alignment, utilization analysis, seniority match, profile targeting)
- Process history per offer, drawn from each detail file loaded in §2 (stages reached, dates, how the negotiation has gone so far) — label each offer with its `application` label
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

