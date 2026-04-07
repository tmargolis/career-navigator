---
name: artifact-saved
description: "Runs after artifact writes. Reconciles artifacts-index with files on disk in the user job search folder and prepares an analytics-ready artifact event summary."
triggers:
  - "reconcile artifacts index"
  - "sync artifacts index with files"
  - "fix artifacts-index.json"
  - "refresh artifact inventory from disk"
  - "/career-navigator:artifact-saved"
---

Run **after** new resumes or cover letters are saved to disk (e.g. from `tailor-resume` / `cover-letter`), and/or at the start of `daily-schedule` when PDF/DOCX artifacts exist in `{user_dir}`. There is no separate plugin hook file in this repository.

Important behavior:
- This workflow must also auto-trigger `add-source` for newly discovered resume/CV source files that are not yet ingested into `ExperienceLibrary`.
- This workflow should trigger incremental `mine-stories` when newly ingested or changed source files can affect interview story coverage.
- Do not ask the user to manually run `add-source` when auto-ingest can be performed.

## Workflow

### 1. Resolve `{user_dir}` and validate index file

Check `{user_dir}/CareerNavigator/artifacts-index.json`.

If missing, output:
> Artifact sync skipped: run `/career-navigator:launch` to initialize artifacts-index.

### 2. Reconcile artifact inventory

Scan `{user_dir}` for artifact files used by this plugin (PDF and DOCX).

Cross-check file system state against `{user_dir}/CareerNavigator/artifacts-index.json`:
- Add missing records for files found on disk but not in index
- Remove stale index records for files no longer present
- Keep existing metadata when filename/path still matches

For newly added records, set:
- `source` to `existing` when inferred from user files
- `date_created` to today if unknown
- `type` inferred from filename when possible (`resume` or `cover_letter`), otherwise leave neutral notes

Update `meta` with:
- `updated_at`: `{today}`

### 2.5 Auto-ingest source documents

From discovered PDF/DOCX files, identify likely source documents (resume/CV variants).

For each likely source doc not yet represented in `ExperienceLibrary`:
- Run `add-source` automatically with that file path.
- Record whether ingest succeeded or failed.

After auto-ingest attempts, re-read:
- `{user_dir}/CareerNavigator/ExperienceLibrary.json`
- `{user_dir}/CareerNavigator/artifacts-index.json`

Then finalize reconciliation counts.

### 2.6 Incremental story refresh trigger

After source auto-ingest, check whether any newly discovered or changed files are
story-bearing (resume/CV prose, journal-style notes, debrief notes, PKM exports).

When yes:
- Run `mine-stories` in incremental mode automatically.
- Update `{user_dir}/CareerNavigator/StoryCorpus.json` `meta.updated` and `source_index`.
- Record refresh status for output.

When no:
- Skip story refresh silently.

### 3. Prepare analytics event handoff

Create an event summary payload (for current local logging and future connector handoff):
- `event_type`: `artifact_saved`
- `created_count`
- `removed_count`
- `unchanged_count`
- `as_of`

If analytics connector is not configured, explicitly note:
> Analytics connector handoff deferred (no connector configured in this phase).

### 4. Output format

```
ArtifactSaved processed.
Added: {n}
Removed: {n}
Unchanged: {n}
Auto-ingested source docs: {n}
Ingest failed: {n}
Story corpus refreshed: {yes/no} ({n_files} changed source file(s))
```

If `Added` or `Removed` > 0, append one short line:
> Artifacts index updated to match files currently present in `{user_dir}`.

## Guardrails

- Do not fabricate file paths or metadata not supported by file/index evidence
- Do not delete real files from disk; only reconcile index records
- Do not edit `ExperienceLibrary.json` with brittle line-based string replacement; treat JSON as structured data and rewrite safely.
- Keep output concise and operational
