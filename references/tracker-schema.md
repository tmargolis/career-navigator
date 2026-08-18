# Tracker schema v2 — split layout

**Authoritative reference for every read and write of application data.** All
skills and agents that touch application records follow this file.

## Layout

```
{user_dir}/CareerNavigator/
├── tracker.json                       summary rows only
├── applications/<application_id>.json notes[] + stage_history[] for one application
└── contacts/<company-slug>.json       every contact at one company
```

`tracker.json` no longer contains `notes`, `stage_history`, or `contacts` inside
`applications[]`. Reading only `tracker.json` gives the full pipeline at a glance
without loading detail — that is the point of the split. Load a detail or contacts
file only for the applications actually in play.

## tracker.json

```json
{
  "meta": { "schema": "tracker_v2_split", "last_updated": "YYYY-MM-DD", "layout": { ... } },
  "applications": [ /* summary rows, see below */ ],
  "networking": [ ... ],
  "pipeline_summary": { ... },
  "search_performance": { ... },
  "strategy_signals": { ... }
}
```

### Summary row (`applications[]`)

Carries every scalar field it always had — `id`, `company`, `role`, `location`,
`status`, `job_link`, `req_id`, `salary_range`, `date_applied`, `follow_up_date`,
`next_step`, `priority`, `outcome`, `outcome_notes`, `resume_version`, `artifacts`
— plus these split-layout fields:

| Field | Type | Meaning |
|---|---|---|
| `application` | String | Display label, exactly `"<company> — <role>"` (em dash, spaces around it). This is the join value used in contacts files. |
| `detail_file` | String | Path relative to `CareerNavigator/`, e.g. `applications/app-hex-senior-pm.json`. Always present. |
| `contacts_file` | String | Path relative to `CareerNavigator/`, e.g. `contacts/hex.json`. Present only when the application has contacts. |
| `notes_count` | Int | Number of entries in the detail file's `notes[]`. |
| `stage_count` | Int | Number of entries in the detail file's `stage_history[]`. |
| `contact_count` | Int | Number of contacts at this company linked to this application. |
| `latest_stage` | String | `stage` of the last `stage_history` entry. |
| `latest_stage_date` | String | `date` of the last `stage_history` entry. |
| `previous_ids` | Array | Former ids for this application. Present only when renamed. |

## applications/&lt;application_id&gt;.json

```json
{
  "schema": "application_detail_v1",
  "application_id": "app-hex-senior-pm",
  "application": "Hex — Senior Product Manager",
  "company": "Hex",
  "role": "Senior Product Manager",
  "stage_history": [
    {
      "stage": "recruiter",
      "date": "YYYY-MM-DD",
      "notes": "...",
      "interview_type": "recruiter | hiring_manager | technical | panel | executive | final | null",
      "interviewers": [],
      "post_notes": null
    }
  ],
  "notes": [
    { "date": "YYYY-MM-DD", "text": "..." }
  ]
}
```

## contacts/&lt;company-slug&gt;.json

```json
{
  "company": "Hex",
  "contacts": [
    {
      "name": "Carlos Aguilar",
      "application": "Hex — Senior Product Manager",
      "title": "Head of Product",
      "relationship": "hiring_manager",
      "notes": "...",
      "interactions": [
        { "date": "YYYY-MM-DD", "type": "call | email | linkedin | in_person", "notes": "..." }
      ]
    }
  ],
  "contact_count": 4
}
```

One company file serves every application at that company. Each contact's
`application` field points back to a specific application's `application` label.
The same person appearing across two applications at one company gets one entry
per application — dedupe by `name` when presenting to the user.

**Company slug:** lowercase the company name, strip accents, replace every run of
non-alphanumeric characters with a single hyphen, trim leading/trailing hyphens.
`84.51°` → `84-51`, `StrainBrain / Powr Plant` → `strainbrain-powr-plant`,
`Northwestern University — Office for Research` → `northwestern-university-office-for-research`.
Never invent a slug for an existing company — list `CareerNavigator/contacts/` and
reuse the file that is already there.

## Resolving an application

1. Read `tracker.json` and match on `id`.
2. If no match, check each row's `previous_ids` — historical files under
   `briefs/` reference ids that were renamed and are still valid lookups.
3. Load `detail_file` only when notes or stage history are actually needed.
4. Load `contacts_file` only when contacts are actually needed, then filter its
   `contacts[]` to entries whose `application` equals the row's `application`.

## Application ids

Format: `app-<company-slug>-<role-keywords>`, e.g. `app-hex-senior-pm`,
`app-anthropic-research-pm-labs`, `app-ocrolus-dir-product-platform`.

Never mint a UUID, a bare sequence (`app-001`), or a date-suffixed id. Add a
disambiguating suffix **only** when an id would otherwise collide with an existing
application at the same company with the same role — and prefer a distinguishing
word from the role over a number or date.

## Write rules

Every write that changes application data is a **multi-file transaction**. Never
write one file and skip the others.

**Appending a note**

1. Append `{ "date", "text" }` to the detail file's `notes[]`. Never overwrite
   or reorder existing entries.
2. Set the summary row's `notes_count` to the new array length.

**Appending a stage**

1. Append the stage object to the detail file's `stage_history[]`.
2. Set the summary row's `stage_count`, `latest_stage`, and `latest_stage_date`.
3. Update the summary row's `status` when the stage represents a status change.

**Adding or updating a contact**

1. Resolve `contacts_file` from the summary row. If the row has none, derive the
   slug (rules above), create `contacts/<slug>.json` with `company`, `contacts: []`,
   `contact_count: 0` if it does not exist, and set `contacts_file` on the row.
2. Look for an existing entry with the same `name` **and** the same `application`.
   Append if absent; otherwise update in place and append to `interactions[]`.
3. Recompute the file's `contact_count`, and the summary row's `contact_count`
   for that application.

**Creating a new application**

1. Mint the id per the rules above and build the label
   `"<company> — <role>"`.
2. Write `applications/<id>.json` with `schema`, `application_id`, `application`,
   `company`, `role`, `stage_history` (one entry for the current stage), `notes`.
3. Append the summary row to `tracker.json` → `applications[]` with the scalars,
   `application`, `detail_file`, `notes_count`, `stage_count`, `latest_stage`,
   `latest_stage_date`, and `contacts_file`/`contact_count` if contacts exist.
4. Recalculate `pipeline_summary`.

**Renaming or removing an application**

Rename the detail file alongside the id, append the old id to `previous_ids`, and
update any `application` labels in the company contacts file.

## Editing safety

Edit these files by loading and re-dumping JSON programmatically (Python
`json.load` / `json.dump` with `indent=2`, `ensure_ascii=False`), then re-validate
by reloading. Hand-editing raw JSON has silently corrupted files in this workspace
before.

After any multi-file write, verify: every summary row's `detail_file` resolves,
`notes_count` / `stage_count` match the detail arrays, and `latest_stage` matches
the last `stage_history` entry.

## Escape hatch

`CareerNavigator/_migration/rehydrate.py` rebuilds a single flat v1-shaped tracker
at `tracker-rehydrated.json` for any tool that needs the pre-split shape. It is a
read-only convenience — never treat its output as the source of truth, and never
write back to it.
