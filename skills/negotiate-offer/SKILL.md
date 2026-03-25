---
name: negotiate-offer
description: >
  Produces negotiation leverage and a send-ready negotiation draft via
  writer. Loads OfferContext persisted by evaluate-offer and
  avoids re-collecting already-known details.
triggers:
  - "negotiate my salary"
  - "negotiate this offer"
  - "raise negotiation"
  - "promotion negotiation"
  - "salary counter offer"
  - "help me negotiate"
  - "/career-navigator:negotiate"
---

Run `negotiate-offer` to draft send-ready negotiation messaging in the
user's voice using:
- persisted `OfferContext` from `evaluate-offer` when available
- otherwise, minimal collection + fresh market benchmark

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

If required files are missing, output:
> Negotiation skipped: run `/career-navigator:launch` to initialize `CareerNavigator/`.

### 2. Identify which offer to negotiate
Preferred path:
- If a user message includes `company` and `role` (or job link / deadline),
  match them to an application in tracker where `status` is `"offer"`.

If there is exactly one `"offer"` application in the tracker: use it.

If multiple offer applications exist and matching is ambiguous:
- ask for ONE clarification question: "Which company/role offer are we negotiating?"

Set `application_id`.

### 3. Load persisted OfferContext (skip re-collect if present)
Check for:
`{user_dir}/CareerNavigator/offer-context-{application_id}.json`

If found:
- load it
- skip re-collecting offer details and market benchmarks already present in
  the file

If not found:
- request any missing offer basics (comp + deadline + any key terms)
- then proceed with benchmark/leverage using profile + ExperienceLibrary

### 4. Build negotiation leverage + ask strategy
Use `honest-advisor` (primary) + `market-researcher` (input) to produce a
**NegotiationBrief** including:
- Market position (where current offer sits vs benchmark)
- Leverage inventory (ranked credentials/accomplishments/ExperienceLibrary
  units that justify an above-median ask)
- Ask strategy (recommended base/equity/sign-on targets and sequencing)
- Risk calibration (downside in this scenario; walk-away floor if possible)

### 5. Emit `NegotiationHandoffBrief` to `writer`
Create a structured **NegotiationHandoffBrief** object that includes:
- ask amount/range
- key leverage points
- tone guidance (assertive vs collaborative)
- recommended channel (email vs verbal)
- suggested phrasing (short bullet list)

Then invoke **`writer`** with mode:
- `negotiate-offer`

so `writer` drafts the send-ready negotiation message in the user's
voice.

### 6. Present draft + ask for explicit approval
Show the `writer` draft in full and ask:
> "Ready to send? If you want changes, tell me what to adjust (ask size, tone, channel)."

Do not send anything automatically.

*** End note (host tool safety) ***
- Never use error text as filenames or paths.
- If any host write fails (should be rare in this skill because we only read
  files), do not fake persistence; just continue in chat.

