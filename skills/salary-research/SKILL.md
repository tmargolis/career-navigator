---
name: salary-research
description: >
  Benchmarks compensation for a role and location from two free sources: live
  posted pay ranges from the Indeed connector, and official wage percentiles
  from the US Bureau of Labor Statistics (OEWS). Returns a table of
  salary-bearing listings, a posted-range summary, and a BLS percentile
  reference line. Fires when compensation is mentioned in any context: offer
  evaluation, role targeting, or explicit request.
when_to_use: >
  Use when the user says things like: "what's the salary for", "what does a
  [role] make", "salary range for", "how much do [role]s earn", "compensation
  for", "benchmark my salary", "what should I be making", "market rate for",
  "salary data", "pay range for", "is this offer competitive", "what are
  [role]s paid".
---

Benchmark pay for a role and location from two free sources and return one compensation summary:

- **Indeed (live market):** pay ranges employers posted on current listings, via the Indeed connector's `search_jobs` tool.
- **BLS OEWS (official baseline):** annual wage percentiles (10th, 25th, median, 75th, 90th) for the matching occupation and metro area, from the Bureau of Labor Statistics public API. No account, key or token is needed.

Neither source costs the user anything. Run whichever is available; if both are, show both.

## 1. Collect inputs

Extract these from the conversation. Do not ask for anything already stated.

| Input | Source | Required |
|---|---|---|
| `role` | Job title from conversation, or `## Target Roles` in `{user_dir}/CareerNavigator/profile.md` | Required |
| `location` | Location from conversation, or `## Location` in `profile.md` | Required |
| `remote` | User says "remote only" or "fully remote" | Optional |
| `compare_to` | A specific offer figure or the profile's compensation floor | Optional |

If `role` or `location` cannot be determined, ask for both in one prompt:
> "What role and location should I pull salary data for? (e.g., 'Senior Product Manager in Chicago')"

## 2. Indeed: posted pay ranges

**Check for the tool.** If `search_jobs` (Indeed connector) is not available in this session, skip to step 3 and say once, at the end: "Connect **Indeed** in **Customize → Connectors** to add live posted ranges (run `/career-navigator:launch` Step 3 for the walkthrough)." Do not scrape Indeed in a browser.

**Search.** Call `search_jobs` with:
- `search`: the role title
- `location`: the city/state, or `"remote"` if `remote` is set
- `country_code`: `"US"` unless the location is elsewhere

Then run **one** broader variant in parallel to widen the sample: drop seniority or specialty words from the title (e.g., "Senior AI Product Manager" → "Product Manager"). Merge both result sets and deduplicate by job ID or link.

**Parse pay.** Take each listing's posted compensation:
- A range ("$110,000 - $160,000 a year") gives min and max.
- A single figure ("$140,000 a year", "Up to $150,000") gives that value as both min and max, or as max only for "up to".
- Hourly pay: multiply by 2,080 to annualize, and mark the row "(hourly)".
- Monthly pay: multiply by 12.
- Skip listings with no posted pay. Do not estimate pay that isn't posted, and do not call `get_job_details` just to look for pay.

If fewer than 5 listings carry pay, call `get_job_details` on up to 5 of the most relevant listings without pay, in parallel, and use any pay those details show.

**Sort** by max salary descending; rows with only a min sort below, by min descending.

## 3. BLS OEWS: wage percentiles

### 3a. Pick the occupation (SOC code)

BLS groups jobs by Standard Occupational Classification (SOC), not by job title, so map the role to the closest code. Use the table below; for titles it doesn't cover, use the closest code you know and say which one you chose.

| Role family (examples) | SOC | BLS occupation |
|---|---|---|
| Product manager, AI/technical PM, head of product, engineering/IT director, CTO-track | `113021` | Computer and Information Systems Managers |
| Product marketing, growth, brand or marketing manager | `112021` | Marketing Managers |
| Sales manager, head of sales, partnerships lead | `112022` | Sales Managers |
| Engineering manager (hardware, mechanical, civil, R&D) | `119041` | Architectural and Engineering Managers |
| CEO, president, executive director, founder | `111011` | Chief Executives |
| General manager, COO, operations director | `111021` | General and Operations Managers |
| Other managers (e.g., program or innovation director with no closer fit) | `119199` | Managers, All Other |
| Software engineer, developer | `151252` | Software Developers |
| Research scientist, ML/AI researcher | `151221` | Computer and Information Research Scientists |
| Data scientist, ML engineer (applied) | `152051` | Data Scientists |
| UX/UI, web or digital product designer | `151255` | Web and Digital Interface Designers |
| Systems or business analyst (IT) | `151211` | Computer Systems Analysts |
| Program or project manager (individual contributor) | `131082` | Project Management Specialists |
| Management consultant, strategy analyst | `131111` | Management Analysts |
| Graphic designer, visual designer | `271024` | Graphic Designers |

Product management has no SOC code of its own. For PM roles in software or AI, `113021` is the standard proxy; for consumer or marketing-led PM roles, also pull `112021` and show both.

### 3b. Pick the area code

Use the metro area (CBSA) code, padded to 7 digits with leading zeros:

| Metro | Area code |
|---|---|
| New York | `0035620` |
| Los Angeles | `0031080` |
| San Francisco | `0041860` |
| San Jose | `0041940` |
| Seattle | `0042660` |
| Boston | `0014460` |
| Chicago | `0016980` |
| Austin | `0012420` |
| Denver | `0019740` |
| Washington, DC | `0047900` |
| Atlanta | `0012060` |
| Dallas | `0019100` |
| Houston | `0026420` |
| Philadelphia | `0037980` |
| Minneapolis | `0033460` |
| Phoenix | `0038060` |
| San Diego | `0041740` |
| Miami | `0033100` |

For another US metro, use its CBSA code if you know it (list: https://www.bls.gov/oes/current/msa_def.htm). For **remote** roles, or when the metro is unknown or returns no data, use the **national** series instead.

### 3c. Build the series IDs

- Metro: `OEUM` + area code (7 digits) + `000000` + SOC (6 digits) + datatype (2 digits)
- National: `OEUN` + `0000000` + `000000` + SOC + datatype

Datatypes (annual wages): `11` = 10th percentile, `12` = 25th, `13` = median, `14` = 75th, `15` = 90th.

Example: Chicago, Computer and Information Systems Managers, median = `OEUM001698000000011302113`.

### 3d. Fetch

The BLS public API (v1) is free and needs no key; it allows about 25 requests per day per network.

- **With a shell** (preferred, one request for all five percentiles):
  ```bash
  curl -s -X POST -H 'Content-Type: application/json' \
    -d '{"seriesid":["<id>11","<id>12","<id>13","<id>14","<id>15"]}' \
    https://api.bls.gov/publicAPI/v1/timeseries/data/
  ```
- **With a web-fetch tool only:** GET `https://api.bls.gov/publicAPI/v1/timeseries/data/<series_id>` for the median (`13`) first, then the 25th and 75th (`12`, `14`) if requests allow.

In each series, use the data point with `"latest": "true"` and report its `year`. A missing or `"-"` value means BLS suppressed or didn't publish that figure: show `—`. If the metro series has no data, retry the national series once and label it national.

If the host can't reach `api.bls.gov` at all, skip this section and say so in the output.

## 4. Output

```
## Salary Benchmarks: {role} · {location}
{today's date} · Sources: Indeed posted ranges ({n} listings) · BLS OEWS {year}
```

### Posted ranges (Indeed)

| Title | Company | Location | Min | Max |
|---|---|---|---|---|
| [title](job link) | company | location | $145k | $190k |

- Format as `$XXXk`. Use `—` for a missing min or max. Note non-USD currency with its code.
- Show at most 15 rows; say how many more were found.

Below the table, computed only from listings with posted pay:

```
- Low: $XXXk (lowest min)
- Median: $XXXk (median of each listing's midpoint, or its single figure)
- High: $XXXk (highest max)
- Based on: {n} of {total} listings with posted pay
```

If fewer than 3 listings carry pay, add: "⚠️ Only {n} listing(s) posted pay, so this range may not be representative."

### Official wages (BLS OEWS)

```
{Occupation name} (SOC {xx-xxxx}) · {metro or "National"} · {year}
10th $XXk · 25th $XXk · Median $XXXk · 75th $XXXk · 90th $XXXk
```

Add one line on what this measures: BLS wages are base pay for **everyone currently employed** in that occupation and area, across all levels and industries. They exclude bonus and equity, so they usually sit below posted ranges for senior or AI-focused roles. Use the 75th and 90th percentiles as the reference for senior and leadership roles.

### Contextual note

Only when there is a specific figure to compare (`compare_to`), add one or two sentences placing it against both sources, for example:
> "Your $185k offer sits near the median of posted ranges ($180k) and between the BLS 75th ($220k) and median ($174k) for Chicago, so it's market-rate base pay, not above it."

Do not invent a comparison when there is no figure.

## 5. Errors

**Indeed returns no listings with pay:**
> "Found {n} listings for '{role}' in '{location}', but none posted pay. That's common for senior roles listed as 'competitive'. The BLS figures above are the best available baseline; a broader title or a larger metro may surface posted ranges."

**Indeed returns nothing:**
> "Indeed returned no listings for '{role}' in '{location}'. Try a broader title (e.g., 'Product Manager' instead of 'Senior AI Product Manager') or a larger metro."

**BLS returns `REQUEST_NOT_PROCESSED`** (daily limit reached): show the Indeed results alone and say the BLS baseline can be retried tomorrow.

**Both sources unavailable:** say so plainly. Do not produce figures from memory and present them as data; if you give a rough estimate, label it as an estimate with low confidence.
