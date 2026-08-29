---
name: career-plan
description: >
  Builds a realistic, honest near/medium/long-term career trajectory and gap
  analysis using profile + ExperienceLibrary, with market-informed demand and
  AI/automation displacement outlook. Saves `career-trajectory.md` (report) and
  `career-trajectory-data.json` (`career_trajectory_v1`) for downstream scoring.
triggers:
  - "career plan"
  - "career trajectory"
  - "where am i headed"
  - "what should i target next"
  - "/career-navigator:career-plan"
  - "/career-navigator:career-trajectory"
---

Run `career-plan` to produce a realistic career plan, a human-readable report
at `{user_dir}/CareerNavigator/career-trajectory.md`, and a structured
`career_trajectory_v1` artifact at
`{user_dir}/CareerNavigator/career-trajectory-data.json`.

## Workflow

### Directory sharing (host integration)
If the host UI asks you for a **directory to share with an agent** during this
skill's run, share **only** your `{user_dir}` job-search folder (the one
containing `CareerNavigator/`).

All reads/writes for this skill are under:
- `{user_dir}/CareerNavigator/profile.md`
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`
- `{user_dir}/CareerNavigator/career-trajectory.md`
- `{user_dir}/CareerNavigator/career-trajectory-data.json`
- `{user_dir}/CareerNavigator/career-trajectory-{as_of}-{ideal_role_slug}.md` (versioned report snapshot)
- `{user_dir}/CareerNavigator/career-trajectory-data-{as_of}-{ideal_role_slug}.json` (versioned data snapshot)

Do not share the whole workspace or unrelated folders.

### 1. Confirm required data exists
Read:
- `{user_dir}/CareerNavigator/profile.md`
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`

If missing, output:
> Career plan skipped: run `/career-navigator:launch` to initialize `CareerNavigator/` first.

### 2. Optional ideal role argument
If the user provides an explicit target (e.g. "for an Applied AI PM role" or
"ideal_role: Senior Product Manager"), capture it as `ideal_role` for targeted
gap analysis. Otherwise set `ideal_role = null`.

### 3. Market intelligence pass (demand + AI displacement + compensation direction)
Hand off to the **`market-researcher`** agent with:
- The full `profile.md` and key target roles/locations (as provided).
- The full `ExperienceLibrary.json` (so it can align displacement risk to the
  user's durable strengths).
- Instruction: produce horizon-aware signals for:
  - Near-term (0–18 months)
  - Medium-term (18 months–4 years)
  - Long-term (4+ years)
- Compensation trajectory direction (where compensation tends to rise/flatten
  over the horizons) and geography competitiveness notes.

### 4. Honest trajectory synthesis
Hand off to the **`honest-advisor`** agent with:
- The market intelligence output from step 3.
- The full profile + ExperienceLibrary.
- The optional `ideal_role` (if present).
- Also pass along the `## Employment Context` (if present) so the plan can
  account for transition cost (employed) or urgency/runway (unemployed).

Instruction: apply the norm/exception/strategy pattern and output a
**CareerTrajectoryReport** with:
- Current position assessment (competitive standing + why, grounded in tracker/
  ExperienceLibrary when available)
- Realistic near-term trajectory (0–18 months), ranked by achievability
- Medium-term trajectory (18 months–4 years), with branches (e.g. IC vs
  management; startup vs enterprise)
- Long-term horizon (4+ years), honest framing of ceiling risk/optionality
- Market-informed gap analysis ranked by ROI (cost x time x impact)

If `ideal_role` is set:
- Add an "Ideal role gap analysis" section stating whether the ideal role is
  realistically achievable, under what conditions/timeline, and what steps
  would most change the outcome probability.

### 5. Save report + `career_trajectory_v1` data (with versioned history)
Write two artifacts per run:

1) **Markdown report** (human-readable; no embedded JSON):
- Versioned snapshot: `{user_dir}/CareerNavigator/career-trajectory-{as_of}-{ideal_role_slug}.md`
- Canonical report: `{user_dir}/CareerNavigator/career-trajectory.md`

2) **`career_trajectory_v1` JSON** (machine-readable; used by `job-scout`, `search-jobs`, `compare-offers`, `daily-schedule`):
- Versioned snapshot: `{user_dir}/CareerNavigator/career-trajectory-data-{as_of}-{ideal_role_slug}.json`
- Canonical data: `{user_dir}/CareerNavigator/career-trajectory-data.json`

Where:
- `as_of` = current date `YYYY-MM-DD`
- `ideal_role_slug` = `ideal_role` lowercased, trimmed, spaces collapsed to `-`, and any characters in `\ / : * ? " < > |` removed; if `ideal_role = null`, use `no-ideal-role`.

**Write order (recommended):**
- First write both **versioned snapshots** (`.md` + `.json`).
- Then write both **canonical files** (`.md` + `.json`) so downstream consumers always read the latest pair.

**Markdown heading requirement:**
Include a line like:
`## Career trajectory analysis ({YYYY-MM-DD})`
so readers (and `daily-schedule` fallback) can see the report date at a glance.

**`career_trajectory_v1` JSON requirement:**
The data file must be valid JSON with this shape:
```json
{
  "schema": "career_trajectory_v1",
  "as_of": "{YYYY-MM-DD}",
  "ideal_role": "{string or null}",
  "near_term_roles": [
    { "rank": 1, "role_title": "...", "achievability_label": "high|med|low", "rationale": "..." }
  ],
  "medium_term_roles": [
    { "rank": 1, "role_title": "...", "achievability_label": "high|med|low", "rationale": "..." }
  ],
  "gap_analysis": [
    { "priority_rank": 1, "gap_area": "...", "why_it_matters": "...", "roi_score_0_100": 0, "cost_time_estimate": "...", "execution_risks": "..." }
  ]
}
```

Do **not** embed this JSON in `career-trajectory.md`; downstream skills read
`career-trajectory-data.json` directly.

If the write-to-disk tool fails:
- Do not invent a save.
- Show the full markdown report and the JSON payload in separate fenced code
  blocks and tell the user to save them manually to the versioned + canonical
  paths above.

### 6. Present result
Present the conversational CareerTrajectoryReport in chat and confirm:
> Saved snapshot to `{user_dir}/CareerNavigator/career-trajectory-{as_of}-{ideal_role_slug}.md` and `{user_dir}/CareerNavigator/career-trajectory-data-{as_of}-{ideal_role_slug}.json` (and updated canonical `career-trajectory.md` + `career-trajectory-data.json` for downstream scoring).

