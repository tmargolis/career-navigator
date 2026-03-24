---
name: artifact-saved
description: >
  Runs after artifact writes. Reconciles artifacts-index with files present in
  {user_dir} and prepares an analytics-ready artifact event payload.
triggers: []
---

Run **after** new resumes or cover letters are saved to disk (e.g. from `tailor-resume` / `cover-letter`), and/or at the start of `daily-schedule` when PDF/DOCX artifacts exist in `{user_dir}`. There is no separate plugin hook file in this repository.

## Workflow

### 1. Resolve `{user_dir}` and validate index file

Check `{user_dir}/CareerNavigator/artifacts-index.json`.

If missing, output:
> Artifact sync skipped: run `/career-navigator:setup` to initialize artifacts-index.

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
```

If `Added` or `Removed` > 0, append one short line:
> Artifacts index updated to match files currently present in `{user_dir}`.

## Guardrails

- Do not fabricate file paths or metadata not supported by file/index evidence
- Do not delete real files from disk; only reconcile index records
- Keep output concise and operational
