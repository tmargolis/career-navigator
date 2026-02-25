---
name: salary-research
trigger: auto
fires_when:
  - Compensation, salary, pay, total comp, TC, equity, RSU, or bonus is mentioned
  - An offer is being discussed or evaluated
  - A job description includes salary range information
  - The user asks about whether to disclose their salary expectations
description: >
  Automatically surfaces current salary market data, equity interpretation
  guidance, and negotiation framing when compensation enters the conversation.
---

# Salary Research Skill

This skill fires when compensation is mentioned in any context. Pull the most relevant data for the specific role, level, and geography being discussed, then apply the guidance below.

## 1. How to Research Salary Ranges

Use the following sources in priority order. Cite the source and note when data was last updated.

| Source | Best For | URL |
|--------|----------|-----|
| **Levels.fyi** | Tech roles, especially engineering and PM; includes RSU/equity breakdowns | levels.fyi |
| **Glassdoor** | Broad coverage across industries; includes bonus data | glassdoor.com/Salaries |
| **LinkedIn Salary** | Good for non-tech roles; filters by industry and company size | linkedin.com/salary |
| **Bureau of Labor Statistics** | Authoritative baseline; annual OES survey; lags real market by ~18 months | bls.gov/oes |
| **CareerOneStop** | BLS data with geographic breakdown and occupation outlook | careeronestop.org |
| **Payscale** | Total compensation with experience-level filters | payscale.com |
| **Blind** | Anonymous tech industry data; skews toward senior IC and staff+ | teamblind.com |

When researching, triangulate across at least two sources. Report the range, not a single number.

## 2. Interpreting Ranges

**Geography adjustment**: Salary ranges vary significantly by metro area. A $150K role in San Francisco may be equivalent to $100K in Austin or $85K in Chicago after cost-of-living adjustment — but note that remote roles at SF-based companies often pay SF rates regardless of your location. Clarify whether the role is remote/hybrid when interpreting ranges.

**Company size**: Startups (Series A–C) typically pay 10–25% below market base but compensate with equity. Unicorns and public companies typically pay at or above market with structured equity programs. Enterprise/F500 companies often pay slightly below FAANG but with strong benefits.

**Level calibration**: Titles are not standardized. "Senior Engineer" at one company is L5 at another. When possible, identify the internal level or compare by scope/scope (individual contributor managing $X budget, team of Y, etc.) rather than title.

**Total compensation = base + bonus target + equity value**. For equity:
- RSUs at public companies: value = (shares × current price) / vesting years
- Stock options at private companies: value is speculative; weight by stage, last valuation, and preference stack
- ESPP: typically 15% discount on shares — real value but not part of TC negotiation

## 3. Equity / RSU Interpretation

When equity is mentioned, ask for or calculate:
- Grant size (shares or dollar value at grant)
- Vesting schedule (standard: 4-year cliff/monthly, but ask)
- Cliff (typically 1 year — you get 25% at 12 months, then monthly)
- Public vs. private (private = illiquid; cannot be valued the same as public)
- Refresh grants (offered annually at high-performing companies; ask)

Flag any of these risk factors:
- Cliff longer than 1 year
- No refresh grant policy
- Double-trigger acceleration not included (important for acquisition scenarios)
- Options with a strike price above the last 409A valuation (underwater risk)
- Short post-termination exercise window (90 days standard; anything shorter is punitive)

## 4. Negotiation Framing

**Core rules:**
1. **Never give a number first.** If asked for salary expectations, deflect: "I'm open to the right opportunity — what's the budgeted range for this role?" Most companies have a range; getting them to state it first is always better.
2. **Anchor high within a credible range.** Once you must state a number, anchor at the top of the market range for your level and experience. You can always come down; you cannot go up.
3. **Negotiate total comp, not just base.** If base is fixed, negotiate signing bonus, equity, title (which affects future comp), vacation, remote flexibility, and start date.
4. **Everything is negotiable, not all at once.** Don't fire all requests simultaneously. Secure verbal agreement on each component before moving to the next.
5. **Never apologize for negotiating.** No competent company rescinds an offer because a candidate negotiated professionally.

**Framing language:**
- "Based on my research and the scope of this role, I was expecting something in the range of $X–$Y. Is there flexibility there?"
- "I'm excited about this role. The base is a bit below what I was targeting — is there room to discuss the equity component or signing bonus?"
- "I have a competing offer at $X. Is there anything you can do to close the gap?"

**When NOT to negotiate aggressively**: Government and union roles with published pay bands. Negotiating above band is typically not possible and asking can signal unfamiliarity with the sector.

## 5. Salary Disclosure Laws

Several U.S. states and cities require employers to provide salary ranges upon request or in job postings (California, Colorado, New York, Washington, and others). If the JD omits a range in a jurisdiction where disclosure is required, the user can request the range — this is a legal right, not an aggressive move.
