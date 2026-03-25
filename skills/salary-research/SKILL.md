---
name: salary-research
description: >
  Pulls live compensation data for a role and location using the Apify
  best-job-search actor. Returns a markdown table of salary-bearing listings
  sorted by maximum salary, plus a compensation range summary (min, max,
  median). Fires when compensation is mentioned in any context — offer
  evaluation, role targeting, or explicit request.
triggers:
  - "what's the salary for"
  - "what does a [role] make"
  - "salary range for"
  - "how much do [role]s earn"
  - "compensation for"
  - "benchmark my salary"
  - "what should I be making"
  - "market rate for"
  - "salary data"
  - "pay range for"
  - "is this offer competitive"
  - "what are [role]s paid"
---

Pull live salary data for a role and location via the Apify MCP server and return a structured compensation summary.

## Preflight check

Before doing anything else, confirm Apify MCP tools are available in this session (e.g. **Call Actor**, **Get Actor run**, **Get dataset items**). They appear when the user adds the **Apify** **Desktop** connector in Claude **Customize → Connectors**, pastes their token in the connector UI (not in chat), and sets **Enabled tools** to:

`call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search`

If those tools are **not** available:
> "Salary benchmarking needs the Apify Desktop connector. In Claude Desktop: **Customize → Connectors → Desktop → Apify → Configure** — add your Apify token, set **Enabled tools** to `call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search`, save, enable the connector, then open a **new chat** and try again. Or run `/career-navigator:launch` Step 4 for the full walkthrough."

Stop here — do not proceed without the MCP connection.

## Workflow

### 1. Collect inputs

Extract the following from the conversation. Do not ask for anything already stated:

| Input | Source | Required |
|---|---|---|
| `keyword` | Job title from conversation or `## Target Roles` in `profile.md` | Required |
| `location` | Location from conversation or `## Location` in `profile.md` | Required |
| `remoteOnly` | Mentioned by user ("remote only", "fully remote") | Optional |
| `minSalary` | Mentioned by user ("above $120k", "minimum $150k") | Optional |

If `keyword` or `location` cannot be determined from context or profile, ask for them together in a single prompt:
> "What role and location should I pull salary data for? (e.g., 'Senior Product Manager in Chicago')"

### 2. Call the Apify actor

Use the Apify MCP `call-actor` tool with the following parameters:

- **Actor ID:** `cheapget/best-job-search`
- **Input:**
```json
{
  "keyword": "<role title>",
  "location": "<city, state or country>",
  "maxResults": 25,
  "remoteOnly": <true if specified, omit otherwise>,
  "minSalary": <integer if specified, omit otherwise>
}
```

### 3. Parse the response

From each result record, extract these fields:

| Field | Source key |
|---|---|
| Title | `title` |
| Company | `company_name` |
| Location | `location` |
| Remote | `is_remote` |
| Salary min | `salary_minimum` |
| Salary max | `salary_maximum` |
| Currency | `salary_currency` |
| Platform | `platform` |
| URL | `platform_url` |
| Posted | `posted_date` |

### 4. Deduplicate

Where the same `title` + `company_name` combination appears across multiple location variants, keep only the record with the highest `salary_maximum`. If `salary_maximum` is null on all variants, keep the record with the highest `salary_minimum`. If all salary fields are null across all variants, keep the first occurrence.

### 5. Filter

Remove records where **both** `salary_minimum` and `salary_maximum` are null — unless doing so would leave fewer than 5 results. If fewer than 5 salary-bearing records remain after filtering, include all deduplicated records (with and without salary) so the table is still useful.

### 6. Sort

Sort the remaining records by `salary_maximum` descending. Records with no `salary_maximum` sort to the bottom, ordered by `salary_minimum` descending.

### 7. Output

#### Salary listings table

```
## Salary Benchmarks — {keyword} · {location}
Data via Apify · {today's date} · {n} listings

| Title | Company | Location | Remote | Min | Max | Platform |
|---|---|---|---|---|---|---|
| [title](platform_url) | company_name | location | ✓ / — | $salary_minimum | $salary_maximum | platform |
```

- Format salary values as `$XXXk` (e.g., `$145k`) or `$XXX,XXX` for precision if the source provides it. Use the `salary_currency` field — if not USD, show the currency code (e.g., `£85k`).
- If `salary_minimum` or `salary_maximum` is null for a record, show `—`.
- If `is_remote` is true, show ✓; otherwise show —.
- Embed `platform_url` in the title as a hyperlink.
- Show `posted_date` if available as a relative label (e.g., "3d ago") — omit the column if no records have it.

#### Compensation range summary

Below the table, add a summary block calculated across **only the records that have at least one salary field populated**:

```
### Compensation Range
- **Low:** $XXXk  (lowest salary_minimum across results)
- **Median:** $XXXk  (median of salary_maximum values, or salary_minimum where max is null)
- **High:** $XXXk  (highest salary_maximum across results)
- **Currency:** USD (or note if mixed)
- **Based on:** {n} of {total} listings with salary data
```

If fewer than 3 salary-bearing records exist, add a caveat:
> "⚠️ Only {n} listing(s) included salary data — this range may not be representative."

#### Contextual note

If the user asked about a specific offer or their own comp floor, add one sentence comparing it to the range:
> "Your offer of $135k base falls at the 60th percentile of listed ranges for this role and market."

Or if comparing to their profile's compensation floor:
> "Your comp floor of $120k is below the median listed range — you have room to negotiate."

Only include this if there is a specific figure to compare against. Do not fabricate a comparison.

### 8. Error handling

**Actor returns no results:**
> "Apify returned no salary data for '{keyword}' in '{location}'. Try a broader title (e.g., 'Product Manager' instead of 'Senior AI Product Manager') or a larger metro area."

**All results filtered out (no salary data in any record):**
> "Found {n} listings for '{keyword}' in '{location}', but none included salary information. This is common for roles where compensation is listed as 'competitive' or 'DOE'. Try adding a `minSalary` filter to surface listings that disclose pay."

**MCP call fails or times out:**
> "The Apify request didn't complete. In Claude Desktop, open **Customize → Connectors → Apify**, confirm your token and **Enabled tools** (`call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search`), save, enable the connector, and try again in a **new chat**. See `/career-navigator:launch` Step 4 if you need the full walkthrough."
