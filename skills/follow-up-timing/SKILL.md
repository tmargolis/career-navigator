---
name: follow-up-timing
description: >
  Ambient nudge for offer-evaluation and follow-up timing based on tracker
  state. Prompts the user to run evaluate-offer when an active offer exists
  but OfferContext has not been created yet.
triggers:
  - "offer evaluation due"
  - "i have an offer"
  - "offer deadline"
  - "offer evaluation"
  - "/career-navigator:follow-up-timing"
---

Run `follow-up-timing` to get brief timing nudges based on your tracker:
- Offer evaluation due: when a tracker application has `status: "offer"` but
  `{user_dir}/CareerNavigator/offer-context-{application_id}.json` does not
  exist yet.

## Workflow

### 1. Load tracker and required files

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

Read:
- `{user_dir}/CareerNavigator/tracker.json`

If missing:
> Follow-up-timing skipped: run `/career-navigator:launch`.

This is an ambient nudge and must stay cheap: every field it needs (`id`, `company`,
`role`, `status`, `offer.deadline`, `follow_up_date`, `latest_stage`,
`latest_stage_date`) is on the `tracker.json` summary row. Never open
`applications/<application_id>.json` or `contacts/<company-slug>.json` from this skill.

### 2. Offer evaluation check
For each summary row in `tracker.json` → `applications[]` where:
- `status` is `"offer"`
- `offer.deadline` may be set (if present)
- and `{user_dir}/CareerNavigator/offer-context-{id}.json` is
  not present (use the row's `id`; if a stored context file uses an older id, check
  the row's `previous_ids` before declaring the evaluation missing)

Output a short prompt, using the row's `application` label verbatim:
> Offer evaluation due for {application}. Run `/career-navigator:evaluate-offer`.

### 3. Output format
If there are no offer-evaluation due items:
> No offer evaluations pending.

