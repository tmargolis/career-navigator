---
name: training-roi
description: >
  Recommends learning investments using a cost-benefit-time ROI analysis across
  certifications, degrees, bootcamps, and self-study. Invokes the
  honest-advisor agent in training-roi mode.
triggers:
  - "training roi"
  - "learning roi"
  - "what should i learn next"
  - "is a bootcamp worth it"
  - "is a certification worth it"
  - "should i get a degree"
  - "upskilling plan"
  - "best training path for my target role"
---

Invoke `honest-advisor` in `training-roi` mode to compare learning options and recommend the highest-ROI path for the user's target role.

## Workflow

### 1. Confirm baseline context

Read:
- `{user_dir}/CareerNavigator/profile.md`
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`

If target roles are missing:
> "I need your target role(s) to run a training ROI analysis. Run `/career-navigator:launch` (or update `CareerNavigator/profile.md`) first."

If ExperienceLibrary `units` are missing/empty:
> "I need your ExperienceLibrary to estimate learning ROI. Run `/career-navigator:add-source` to add a resume first."

Optionally read `{user_dir}/CareerNavigator/tracker.json` for confidence and bottleneck context.

### 2. Gather optional constraints

If not already provided in conversation, ask once:
> "Do you want me to optimize for a specific budget and timeline? If yes, share your max budget and ideal timeline (for example: '$3k and 4 months')."

Proceed even if user does not provide constraints.

### 3. Invoke honest-advisor — training-roi mode

For each target role (or the explicitly requested role), hand off to `honest-advisor` with:
- `analysis_mode: training-roi`
- `target_role_type`
- `target_level` (if known/inferred)
- `target_geography`
- `time_horizon_months` (if provided; else default 12)
- `budget_range` (if provided)

Instruction:
- Compare certifications, degrees, bootcamps, and self-study.
- Produce a cost-benefit-time option matrix with ROI score.
- Recommend a primary path and fallback path.
- Include explicit assumptions and data gaps.

### 4. Present the recommendation engine output

Render as:

```
**Training ROI Analysis** — {Target Role}
Time horizon: {n months}
Budget: {value or "not provided"}
Confidence: {Preliminary / Directional / Moderate / High}

Top capability gaps
1. ...
2. ...

Option matrix (cost-benefit-time)
| Path | Type | Estimated cost | Estimated time | Signal strength | ROI score | Key risks |
|---|---|---|---|---|---:|---|
| ... |

Recommended plan
- Primary path: ...
- Fallback path: ...
- First 30 days: ...
- Proof artifacts to create: ...

Assumptions and data gaps
- ...
```

If a paid path is lower ROI than self-study for this user, state that directly and explain why.

### 5. Suggest next step

After presenting:
- Suggest `/career-navigator:assessment` to re-check competitiveness after the first milestone.
- Suggest `/career-navigator:tailor-resume` once proof artifacts are created.

