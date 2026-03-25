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
Read:
- `{user_dir}/CareerNavigator/tracker.json`

If missing:
> Follow-up-timing skipped: run `/career-navigator:launch`.

### 2. Offer evaluation check (Phase 1F requirement)
For each application in tracker where:
- `status` is `"offer"`
- `offer.deadline` may be set (if present)
- and `{user_dir}/CareerNavigator/offer-context-{application_id}.json` is
  not present

Output a short prompt:
> Offer evaluation due for {company} — {role}. Run `/career-navigator:evaluate-offer`.

### 3. Output format
If there are no offer-evaluation due items:
> No offer evaluations pending.

