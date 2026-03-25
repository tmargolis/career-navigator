---
name: suggest-roles
description: >
  Suggests non-obvious role opportunities based on transferable strengths and
  market conditions. Invokes honest-advisor and market-researcher, then writes
  outcome-driven role signals for job-scout scoring improvements.
triggers:
  - "suggest roles"
  - "what roles should i target"
  - "non-obvious roles for me"
  - "what else could i apply to"
  - "role pivot suggestions"
  - "/career-navigator:suggest-roles"
---

Invoke both `honest-advisor` and `market-researcher` to generate role suggestions and write actionable signals that improve `job-scout` ranking.

Important invocation rule:
- Use the exact agent names `honest-advisor` and `market-researcher`.
- Do not invent or alias agent types (for example, do not call "career-assessment" or "market-analysis" agent types).
- If either agent invocation fails, retry once using the exact names above before returning an error.

## Workflow

### 1. Confirm data exists

Read:
- `{user_dir}/CareerNavigator/profile.md`
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`

If profile has no target roles:
> "I need your current target role(s) first. Run `/career-navigator:launch` or update `CareerNavigator/profile.md` before running role suggestions."

If ExperienceLibrary `units` is empty:
> "Your ExperienceLibrary is empty. Run `/career-navigator:add-source` to add a resume before role suggestions."

Optionally read `{user_dir}/CareerNavigator/tracker.json` for confidence and outcome context.

### 2. Run advisor pass (competitiveness + transferable fit)

Invoke `honest-advisor` in `assessment` mode for the user's primary target role. Ask it to:
- identify under-covered requirements
- identify nearby role variants where the user's strongest signals are more competitive
- return 3-6 candidate roles with rationale

### 3. Run market pass (demand + displacement + geography)

Invoke `market-researcher` for the same role set and geography. Ask it to:
- classify demand posture for each candidate role (rising/stable/softening)
- flag displacement risk posture
- identify geography-specific competitiveness constraints/opportunities

### 4. Synthesize suggestions

Combine both outputs into a ranked role list:
- prioritize roles where transferable fit is strong **and** demand posture is favorable
- down-rank roles with weak fit, softening demand, or severe geography mismatch
- include at least one "stretch but plausible" option if evidence supports it

### 5. Write job-scout scoring signals

Update `{user_dir}/CareerNavigator/tracker.json` with a `strategy_signals` object (create if missing):

```json
{
  "strategy_signals": {
    "as_of": "YYYY-MM-DD",
    "recommended_role_types": ["..."],
    "adjacent_role_types": ["..."],
    "deprioritize_role_types": ["..."],
    "market_tailwinds": ["..."],
    "market_headwinds": ["..."],
    "preferred_geographies": ["..."],
    "avoid_geographies": ["..."],
    "signal_confidence": "Preliminary | Directional | Moderate | High",
    "source": ["honest-advisor", "market-researcher"]
  }
}
```

These signals are consumed by `job-scout` to improve ranking.

### 6. Present result

Format:

```
**Suggested Roles** — {today's date}
Confidence: {tier}

Top role opportunities
1. {Role}
   - Why this fits: {transferable-fit rationale}
   - Market signal: {demand/geography/displacement summary}
2. ...

Deprioritize for now
- {Role}: {why}

Job-scout update
- Recommended role types written: {list}
- Deprioritized role types written: {list}
- Geography signals written: {list}
```

### 7. Suggest next step

After presenting:
- Suggest `/career-navigator:search-jobs` to run ranking with the updated role/geography strategy signals.
- Suggest `/career-navigator:tailor-resume` for the top suggested role.

Failure fallback:
- If one agent still fails after retry, continue with the successful agent output, clearly label partial-completion status, and tell the user which exact agent failed.

