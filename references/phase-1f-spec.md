# Phase 1F — Career Planning, Offer Evaluation & Compensation Negotiation

**Summary:** Phase 1F closes three capabilities explicitly deferred in the spec (Salary Negotiation — §16 Open Questions; Phase 3 Salary Negotiation & Offer Evaluation module) and accelerates them into Phase 1, because they are high-value, locally self-contained, and naturally extend the `honest-advisor` and `market-researcher` agents already delivered in Phase 1C. This phase adds four new skills, four new slash commands, and no new agents. All skills are orchestrated by `honest-advisor` (primary) with structured input from `market-researcher`, and the negotiation skill emits a handoff brief for `writer` to draft send-ready messaging. Phase 1F also extends `job-scout` to consume trajectory data, extends `daily-schedule` with a monthly career-plan refresh cadence, and explicitly wires the `evaluate-offer` → `negotiate-offer` handoff through the tracker and `follow-up-timing` context skill.

---

## New Skills

### `career-plan`

**Agent:** `honest-advisor` (primary), `market-researcher` (input feed)

**Trigger:** Fires when the user asks what their career path looks like, where they are headed, what they should target next, or requests a realistic career plan. Also invocable via `/career-navigator:career-plan`.

**Behavior:**

Reads `profile.md` and the ExperienceLibrary in full before beginning — does not ask for information already present. Requests a current market intelligence brief from `market-researcher` covering role demand trends, compensation trajectories, and AI/automation displacement risk for the user's current and adjacent roles.

Produces a **CareerTrajectoryReport** structured as follows:

- **Current position assessment** — honest evaluation of the user's current market position: seniority band, competitive standing, perceived strengths and liabilities, and any signals from the ExperienceLibrary that distinguish them from peer candidates
- **Realistic near-term trajectory (0–18 months)** — most probable next roles given current profile, market conditions, and application history; ranked by achievability with rationale
- **Medium-term trajectory (18 months–4 years)** — plausible paths assuming the near-term moves succeed; branches where the path diverges (e.g., IC track vs. management track, startup vs. enterprise)
- **Long-term horizon (4+ years)** — honest framing of ceiling risk, optionality, and structural factors (AI displacement, industry cycle) that should inform strategy now
- **Market-informed gap analysis** — skills, credentials, or experiences that would materially change the trajectory, ranked by ROI (cost × time × impact); cross-references the `training-roi` skill's framework

**Optional argument — `[ideal_role]`:** When the user specifies a target role or title, the skill evaluates the gap between the current profile and that role honestly using the `honest-advisor` norm/exception/strategy pattern:
- Is this role realistically achievable from the current position? Under what conditions and timeline?
- What would most candidates with this background achieve, and where does the user sit relative to that norm?
- What specific steps — and in what sequence — would most improve the probability of reaching that role?
- What obstacles are structural (hard to change) vs. addressable, and how should effort be prioritized accordingly?

The advisor does not tell the user what to want. If the ideal role is unlikely, it says so directly, explains why, and offers the nearest realistic alternative plus what the path to the ideal role would actually require.

**Output:** Conversational report plus a `career_trajectory_v1` JSON artifact saved to `{user_dir}/CareerNavigator/career-trajectory.md`. This artifact is read by `job-scout` at scoring time (see *Job Scout Integration* below) and re-evaluated on a monthly cadence by `daily-schedule` (see *Scheduling Integration* below).

---

### `evaluate-offer`

**Agent:** `honest-advisor` (primary), `market-researcher` (input feed)

**Trigger:** Fires when the user mentions receiving a job offer, asks whether they should take a job, or asks for help evaluating an opportunity. Also invocable via `/career-navigator:evaluate-offer`.

Also nudged by `follow-up-timing`: when an offer-stage application exists in the tracker and `evaluate-offer` has not yet been run for that application, `follow-up-timing` surfaces a prompt to run this skill — preventing the user from missing the evaluation step under the time pressure of a real offer deadline.

**Behavior:**

Begins by determining the user's employment context. Actively attempts to classify one of three scenarios rather than asking the user to self-identify:

- **Scenario A — Currently employed, evaluating a new offer:** The user has an active role and is deciding whether to leave. The evaluation must account for the cost of transition (unvested equity, relationship capital, role momentum, transition risk) as well as the upside of the new role.
- **Scenario B — Currently not employed, evaluating an offer:** The user is in active search with no current income. The evaluation weighs urgency and financial runway against fit, trajectory, and whether the role is a step forward or a filler.
- **Scenario C — Context unclear:** The skill asks a single clarifying question to resolve the scenario before proceeding.

Once the scenario is established, reads `profile.md` and ExperienceLibrary to assess how well the offered role utilizes the user's education, certifications, and experience. Requests a compensation benchmark from `market-researcher` for the role, level, geography, and company type.

Produces an **OfferEvaluationReport** covering:

- **Role fit assessment** — how well the role maps to the user's skills, experience level, and stated targets in `profile.md`; whether it represents a step forward, lateral, or backward in trajectory
- **Utilization analysis** — which of the user's key credentials and experience units are well-utilized, underutilized, or not utilized at all in this role
- **Compensation fairness determination** — explicit yes/no/borderline verdict on whether the offer is fair given current market benchmarks, with data supporting the determination; flags if the offer is below market, at market, or above market
- **Scenario-specific risk assessment:**
  - Scenario A: transition risk, unvested comp being left behind, relationship capital, counter-offer likelihood
  - Scenario B: financial runway vs. search continuation tradeoff; whether accepting would close better opportunities currently in pipeline
- **Recommendation** — the advisor gives a direct, honest recommendation (accept, decline, negotiate, or continue searching) with reasoning. It does not equivocate. The user decides, but the advisor takes a position.

**Handoff to `negotiate-offer`:** Upon completing the report, the skill emits an **OfferContext** object — structured data including the offer details, compensation benchmark result, scenario classification, and key leverage points identified from the ExperienceLibrary. This object is passed directly to `negotiate-offer` if the user proceeds to negotiation in the same session, or persisted to `{user_dir}/CareerNavigator/offer-context-{application_id}.json` so it can be loaded automatically when `negotiate-offer` is invoked later. `negotiate-offer` reads this file at startup and skips re-collecting any information already present in OfferContext, avoiding redundant questions.

**Handoff to `compare-offers`:** If the tracker contains more than one active offer-stage application, `evaluate-offer` notes this on completion and prompts the user to run `compare-offers` for a side-by-side evaluation. Each OfferEvaluationReport is persisted and consumed by `compare-offers` directly.

---

### `negotiate-offer`

**Agent:** `honest-advisor` (primary), `market-researcher` (input feed), `writer` (output handoff)

**Trigger:** Fires when the user wants to negotiate a salary, starting offer, raise, or promotion. Also invocable via `/career-navigator:negotiate`.

**Behavior:**

On startup, checks for a persisted `offer-context-{application_id}.json` from a prior `evaluate-offer` run. If found, loads it and skips re-collecting offer details and market benchmarks already present. If not found, requests a current compensation benchmark from `market-researcher` and reads `profile.md` and ExperienceLibrary directly.

Identifies the user's specific leverage points — credentials, accomplishments, and experience units that justify above-median compensation in this role — and produces a **NegotiationBrief** covering:

- **Market position** — where the current offer (or current salary) sits relative to market: percentile, comparable range, and any notable company-type or geography adjustments
- **Leverage inventory** — specific, citable items from the user's profile that support a higher number; ranked by persuasive weight for this specific role and company type
- **Ask strategy** — recommended ask amount or range, with rationale; whether to ask for base, equity, sign-on, or a combination given the scenario; timing and sequencing guidance
- **Scenario branching:**
  - New offer: initial counter-offer strategy; what to say if they push back; walk-away floor
  - Raise / promotion: how to frame the conversation; when to have it; what documentation to bring; how to handle "budget freeze" or "not the right time" responses
- **Risk calibration** — honest assessment of whether negotiating carries risk in this specific context (early-stage startup equity vs. cash, government/nonprofit salary bands, etc.); what the realistic downside is of asking

Emits a structured **NegotiationHandoffBrief** to `writer` containing: the ask amount, key leverage points, tone guidance (assertive vs. collaborative), channel (email vs. verbal), and any specific phrasing the advisor recommends. `writer` drafts the send-ready negotiation message in the user's voice using this brief. The user reviews before sending.

**Output:** Conversational brief + `writer` drafts negotiation message. Does not send without explicit user approval.

---

### `compare-offers`

**Agent:** `honest-advisor` (primary), `market-researcher` (input feed)

**Trigger:** Fires when the user asks to compare multiple job offers, or when `evaluate-offer` detects more than one active offer-stage application in the tracker and the user elects to proceed. Also invocable via `/career-navigator:compare-offers`.

**Behavior:**

Loads all available **OfferEvaluationReports** from persisted `offer-context-{application_id}.json` files for active offer-stage applications. For any offer without an existing evaluation, runs `evaluate-offer` inline before proceeding so all offers are evaluated on a consistent basis.

Produces a structured **OfferComparisonReport** covering:

- **Side-by-side compensation table** — base, bonus, equity, sign-on, and total comp for each offer; market percentile for each; gap to market for each
- **Role fit matrix** — each offer scored across: trajectory alignment (does it advance the career plan?), skills utilization (education, certifications, experience), seniority match, and alignment with `profile.md` target companies and industries
- **Risk comparison** — scenario-specific risks (Scenario A transition cost, Scenario B runway pressure) assessed for each offer; highlights if one offer's deadline pressure should affect the evaluation sequence
- **Trajectory alignment** — cross-references `career_trajectory_v1` if present; identifies which offer best serves the near-term and medium-term paths documented in the career plan
- **Honest recommendation** — direct ranking of offers with reasoning. If one offer is clearly superior, says so. If the decision is genuinely close, identifies the one or two factors that should be the tiebreaker and explains why, then lets the user decide.

**Output:** Conversational report. Prompts the user to proceed to `negotiate-offer` for the preferred offer if compensation is below market or negotiable.

---

## New Slash Commands

| Command | Description |
|---|---|
| **/career-navigator:career-plan** | Runs the `career-plan` skill. Optional argument: `[ideal_role]` for targeted gap analysis against a specific target title. |
| **/career-navigator:evaluate-offer** | Runs the `evaluate-offer` skill. Accepts offer details conversationally or as pasted text. Emits OfferContext for downstream use by `negotiate-offer` and `compare-offers`. |
| **/career-navigator:negotiate** | Runs the `negotiate-offer` skill. Works for new offers, raises, and promotions. Loads OfferContext from a prior `evaluate-offer` run if available. Produces a `writer` negotiation draft. |
| **/career-navigator:compare-offers** | Runs the `compare-offers` skill. Loads all active OfferEvaluationReports; runs `evaluate-offer` inline for any offer not yet evaluated. Produces a side-by-side comparison with an honest recommendation. |

---

## Agent Updates (no new agents)

| Agent | Update |
|---|---|
| **honest-advisor** | Extended to serve as the primary agent for `career-plan`, `evaluate-offer`, `negotiate-offer`, and `compare-offers`. No change to the agent's design philosophy (§14) — the norm/exception/strategy pattern applies throughout. |
| **market-researcher** | Extended to respond to structured input requests from Phase 1F skills: compensation benchmarks (role + level + geography + company type), trajectory demand signals, and AI/automation displacement risk at career-planning horizon lengths. |
| **writer** | Extended to accept **NegotiationHandoffBrief** as a new input type, producing a send-ready negotiation message in the user's voice. Follows the same handoff pattern as CoverLetterBrief and FollowUpBrief. |
| **job-scout** | Extended to read `career_trajectory_v1` from `{user_dir}/CareerNavigator/career-trajectory.md` at scoring time. When this artifact is present, job-scout incorporates trajectory alignment as a scoring dimension alongside profile keyword match and outcome history — surfacing roles that serve the user's near-term trajectory targets, not just current profile fit. If the file is absent, scoring falls back to existing behavior. |

---

## Scheduling Integration

### `daily-schedule` — Monthly Career Plan Refresh

The `daily-schedule` skill is extended with a **monthly career-plan checkpoint**. On the first run of each calendar month (evaluated by comparing the last-modified timestamp of `career-trajectory.md` against the current date), `daily-schedule` checks whether any of the following conditions are true:

- `career-trajectory.md` does not exist (first run)
- The file was last generated more than 30 days ago
- The tracker contains 5 or more new outcome events (rejections, offers, completions) since the last generation

If any condition is met, `daily-schedule` surfaces a prompt: *"Your career plan was last updated [date]. Based on recent activity, it may be worth a refresh — run `/career-navigator:career-plan` to update your trajectory analysis."*

The skill does not auto-run `career-plan` without user confirmation, as the skill involves a meaningful market-researcher call and conversational output. It nudges; the user initiates.

---

## Tracker & Context Skill Integration

### `follow-up-timing` — Offer Evaluation Nudge

The `follow-up-timing` context skill is extended with an **offer evaluation check**. When an application reaches `status: Offer` in the tracker and no `offer-context-{application_id}.json` file exists for that application, `follow-up-timing` surfaces a prompt on next session start or `daily-schedule` run: *"You have an active offer from [company]. Run `/career-navigator:evaluate-offer` to get an honest assessment before the deadline."*

This prevents the user from missing the evaluation step under the time pressure of a real offer deadline. The nudge is suppressed once the file is created or the application status moves to `Accepted` or `Declined`.

### Handoff Chain Summary

The full Phase 1F handoff chain, in sequence:

```
market-researcher ──► career-plan ──► career_trajectory_v1 ──► job-scout (scoring)
                                                                  └──► daily-schedule (monthly refresh nudge)

market-researcher ──► evaluate-offer ──► OfferContext (persisted) ──► negotiate-offer
                                     └──► OfferEvaluationReport ───► compare-offers
                                     └──► follow-up-timing nudge (if offer in tracker, no eval yet)

negotiate-offer ──► NegotiationHandoffBrief ──► writer (send-ready draft)
```

---

## Resolves Open Questions

| §16 Item | Resolution |
|---|---|
| **Salary Negotiation** — "Offer evaluation and negotiation guidance mentioned briefly — full scope not yet specified. Candidate for Phase 3." | Fully specified and delivered in Phase 1F. Scope covers new offer negotiation, raise/promotion negotiation, offer evaluation with scenario-aware (employed/unemployed/unclear) branching, multi-offer comparison, and structured handoff between evaluation and negotiation. |

---

## New Data Artifacts

| Artifact | Location | Producer | Consumers |
|---|---|---|---|
| `career-trajectory.md` / `career_trajectory_v1` | `{user_dir}/CareerNavigator/career-trajectory.md` | `career-plan` skill | `job-scout`, `daily-schedule`, `compare-offers` |
| `offer-context-{application_id}.json` | `{user_dir}/CareerNavigator/` | `evaluate-offer` skill | `negotiate-offer`, `compare-offers` |
