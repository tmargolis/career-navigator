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
- `{user_dir}/CareerNavigator/tracker.json` (summary rows)
- `{user_dir}/CareerNavigator/applications/<application_id>.json` (the one offer being negotiated)
- `{user_dir}/CareerNavigator/contacts/<company-slug>.json` (the recipient of the negotiation message)
- `{user_dir}/CareerNavigator/offer-context-{application_id}.json` (if present)

Do not share the whole workspace or unrelated folders.

### 1. Confirm required data exists

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

Read:
- `{user_dir}/CareerNavigator/profile.md`
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`
- `{user_dir}/CareerNavigator/tracker.json`

If required files are missing, output:
> Negotiation skipped: run `/career-navigator:launch` to initialize `CareerNavigator/`.

### 2. Identify which offer to negotiate
Preferred path:
- If a user message includes `company` and `role` (or job link / deadline),
  match them to a `tracker.json` summary row where `status` is `"offer"`.

If there is exactly one `"offer"` row in the tracker: use it.

If multiple offer applications exist and matching is ambiguous:
- ask for ONE clarification question: "Which company/role offer are we negotiating?"

Set `application_id` from the row's `id`, and keep its `application` label, `detail_file`,
`contacts_file`, `contact_count`, `latest_stage`, and `latest_stage_date`.

Then load, for **this application only**:
- `{user_dir}/CareerNavigator/` + `detail_file` — `stage_history[]` and `notes[]` carry what
  has already been said about comp, what stage the offer came at, and any prior counter.
  Neither array is in `tracker.json`; drafting without them repeats ground already covered.
- `{user_dir}/CareerNavigator/` + `contacts_file`, when there is a named recipient. Keep
  only entries whose **`application`** equals the row's **`application`** label, **dedupe by
  `name`**, and use their `title`, `relationship`, and prior `interactions[]` to pick the
  recipient and channel. A row with no `contacts_file` has no contacts on file — do not
  invent a slug or a name.

### 3. Load persisted OfferContext (skip re-collect if present)
Check for:
`{user_dir}/CareerNavigator/offer-context-{application_id}.json`
(if absent, check the row's `previous_ids` for a context file saved under an earlier id)

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

### 7. Log the send when the user confirms
Only after the user says they sent it, write the **multi-file transaction** from
[references/tracker-schema.md](../../references/tracker-schema.md) — never update one file
and skip the others:

- In `{user_dir}/CareerNavigator/` + `detail_file`, append to `notes[]`:
  `{ "date": "YYYY-MM-DD", "text": "[negotiation] {ask} sent via {channel}" }`, then set the
  summary row's `notes_count` to the new array length.
- If a contact received it, append to that contact's `interactions[]` in `contacts_file` —
  the entry whose `name` matches **and** whose `application` equals the row's `application`
  label: `{ "date": "YYYY-MM-DD", "type": "email | call", "notes": "Negotiation ask sent" }`.
  If no contact was named, skip this step rather than inventing one.
- On the summary row, set `next_step` to "Await negotiation response" and move
  `follow_up_date` to the agreed check-in date.

Load and re-dump each file programmatically (`json.load` / `json.dump` with `indent=2`,
`ensure_ascii=False`) and reload to verify the counters still match their arrays.

*** End note (host tool safety) ***
- Never use error text as filenames or paths.
- If any host write fails, do not fake persistence; say which file did not write and
  continue in chat. A partially applied §7 transaction is worse than none — if the detail
  file wrote but the summary row did not, report the mismatch so it can be repaired.

