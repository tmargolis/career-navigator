---
name: evaluate-post
description: "Evaluates a professional post or outreach draft for audience fit and cultural/political/reputational risk vs target company profiles. Invokes content-advisor."
triggers:
  - "evaluate this post"
  - "cultural risk"
  - "is this safe to post"
  - "review my linkedin draft"
  - "employer risk"
  - "/career-navigator:evaluate-post"
---

Invoke **`content-advisor`** in **`evaluate-post`** mode.

## Invocation

- Use the exact agent name **`content-advisor`**. Retry once if invocation fails.

## Workflow

1. Read `{user_dir}/CareerNavigator/profile.md` (**Target Companies**, **Target Roles**, industries). If targets are empty, ask once whether to evaluate against **role-level** norms only.
2. Collect the **draft text** from the user (or from the current turn).
3. Instruct **`content-advisor`** to run the **evaluate-post** operation: **risk tier**, rationale vs each named target employer type, and optional **safer paraphrases**—user decides whether to edit.
4. If risk is **high**, suggest pausing publish until they adjust or run **`content-suggest`** for alternative angles.

## Relation to cultural-risk-flag

When drafting in other flows triggers a risk check, prefer this skill’s rules so **`content-advisor`** remains the single evaluator for public copy.
