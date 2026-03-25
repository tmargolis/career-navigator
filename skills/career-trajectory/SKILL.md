---
name: career-plan
description: >
  Builds a realistic, honest near/medium/long-term career trajectory and gap
  analysis using profile + ExperienceLibrary, with market-informed demand and
  AI/automation displacement outlook. Saves `career-trajectory.md` for
  downstream job-scout scoring.
triggers:
  - "career plan"
  - "career trajectory"
  - "where am i headed"
  - "what should i target next"
  - "/career-navigator:career-plan"
  - "/career-navigator:career-trajectory"
---

Run `career-plan` to produce a realistic career plan and a
`career_trajectory_v1` JSON artifact saved to:
`{user_dir}/CareerNavigator/career-trajectory.md`.

## Workflow

### Directory sharing (host integration)
If the host UI asks you for a **directory to share with an agent** during this
skill's run, share **only** your `{user_dir}` job-search folder (the one
containing `CareerNavigator/`).

All reads/writes for this skill are under:
- `{user_dir}/CareerNavigator/profile.md`
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`
- `{user_dir}/CareerNavigator/career-trajectory.md`

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

### 5. Save `career-trajectory.md` + `career_trajectory_v1`
Write the final markdown report (including a fenced `career_trajectory_v1`
JSON block) to:
`{user_dir}/CareerNavigator/career-trajectory.md`

**Markdown heading requirement:**
Include a line like:
`## Career trajectory analysis ({YYYY-MM-DD})`
so `daily-schedule` can detect staleness.

**`career_trajectory_v1` JSON block requirement (for job-scout parsing):**
Your JSON block must look like:
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

If the write-to-disk tool fails:
- Do not invent a save.
- Show the full markdown report in a fenced code block and tell the user to
  save it manually to the exact path above.

### 6. Present result
Present the conversational CareerTrajectoryReport in chat and confirm:
> Saved to `{user_dir}/CareerNavigator/career-trajectory.md`.

