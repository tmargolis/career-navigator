---
name: assessment
description: >
  Provides a candid, evidence-based assessment and gap analysis against the
  user's target role requirements using the `honest-advisor` agent's
  norm/exception/strategy pattern.
triggers:
  - "assessment"
  - "role readiness"
  - "gap analysis"
  - "what gaps do I have"
  - "am I qualified"
  - "honest assessment"
  - "how competitive am I for"
  - "do I meet the requirements"
---

Invoke the `honest-advisor` agent to run a norm/exception/strategy assessment, then present the result as a gap analysis against the user's target role requirements.

## Workflow

### 1. Confirm data exists

Read `{user_dir}/CareerNavigator/profile.md`. If it has no `target_roles` (or equivalent target-role fields):

> "I need your target role(s) to run an assessment. Run `/career-navigator:launch` (or update your `CareerNavigator/profile.md`)."

Read `{user_dir}/CareerNavigator/ExperienceLibrary.json`. If the ExperienceLibrary `units` array is empty:

> "Your ExperienceLibrary is empty. Run `/career-navigator:add-source` to add a resume first."

Optionally read `{user_dir}/CareerNavigator/tracker.json` to estimate how strong your evidence base is. If resolved outcomes are < 5, expect confidence to be `Preliminary`.

### 2. Invoke honest-advisor — assessment + gap analysis

For each target role in `CareerNavigator/profile.md`, hand off to the `honest-advisor` agent with:

- `target_role_type` for that role
- `target_level` (from profile if present; otherwise infer from role title)
- `target_geography` (from profile; if remote/national, treat as "Remote (national pool)")
- Instruction: "Treat your `EXCEPTIONS` as the concrete gaps vs. the target requirements in `CareerNavigator/profile.md`. Explicitly map each exception back to which requirement(s) are most likely under-covered (ATS relevance, narrative/seniority fit, or targeting)."

If multiple target roles exist, run the roles sequentially and label each section.

### 3. Present the gap analysis

Render the agent output as:

```
**Assessment (Gap Analysis)** — {Target Role}
Confidence: {Preliminary/Directional/Moderate/High} ({resolved_outcomes} resolved outcomes)

Target requirements (from profile):
- {requirement 1}
- {requirement 2}

Evidence-based gaps:
1. {exception headline + deviation direction}
   - Impacts: {which requirements this likely undermines}
   - Evidence: {cite tracker/artifacts/ExperienceLibrary evidence}
2. ...

Repositioning plan:
Immediate fixes:
- ...

Pipeline adjustments:
- ...

Compounding investment:
- ...

What would make this more reliable:
- ...
```

Keep it tight: at most 3–4 requirements and 2–4 gaps per role.

### 4. Suggest next step

Based on the highest-leverage gap:

- If ATS/relevance gaps: suggest `/career-navigator:resume-score` or `/career-navigator:ats-optimization` on the weakest artifact.
- If targeting exception (role/company mismatch): suggest `/career-navigator:search-jobs` using your refined role framing.
- If narrative/seniority exception: suggest `/career-navigator:tailor-resume` and then `/career-navigator:cover-letter`.
- If training ROI gap: suggest treating the recommendation as a plan and logging outcomes after 1–2 application cycles.

