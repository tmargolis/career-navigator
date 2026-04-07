---
name: mine-stories
description: >
  Builds and refreshes CareerNavigator/StoryCorpus.json by extracting interview
  story candidates from raw sources (journals, PKM notes, debriefs, resumes,
  and related documents). Runs as a one-time/offline preprocessing pass and as
  an incremental refresh when new source files are detected in {user_dir}.
triggers:
  - "mine stories"
  - "extract interview stories"
  - "build story corpus"
  - "refresh story corpus"
  - "index my journal for interview stories"
  - "update story corpus"
---

Create and maintain a persistent interview story corpus so downstream interview skills never need to read full raw journals repeatedly.

## Workflow

### 1. Resolve `{user_dir}` and required paths

Use:
- `{user_dir}/CareerNavigator/StoryCorpus.json` (target corpus)
- `{user_dir}` (raw source discovery root)

If `StoryCorpus.json` is missing, create it using the schema in step 5.

### 2. Discover source candidates

Scan `{user_dir}` recursively for likely story-bearing files, prioritizing:
- Journal and weekly logs
- Interview debrief notes
- PKM exports/notes (including Notion and Capacities content when available via connector/MCP or local export)
- Resume/CV/cover-letter prose
- Plain text/markdown notes with dated entries

Exclude:
- `{user_dir}/CareerNavigator/*.json`
- Generated artifacts that are not user-authored source evidence
- Binary/media files that cannot be parsed

### 3. Detect incremental work vs full build

If `StoryCorpus.json` already exists:
- Build a file fingerprint map using source path + modified time.
- Skip files already processed with unchanged modified time.
- Process only new/changed files.

If no prior corpus metadata exists, run full build once.

### 4. Extract story candidates (Layer 1)

For each new/changed source:
1. Chunk by natural entry boundary (date, heading, section, paragraph blocks).
2. Run a cheap extraction pass with this intent:
   > "Extract any anecdote, decision, challenge, outcome, or project detail from this entry. Output structured JSON."
3. Keep extracted candidates, not raw source chunks.

Each candidate should include:
- short narrative summary
- date (explicit or inferred if strongly supported)
- competency/theme tags
- ownership/result signals
- confidence score for extraction quality

### 5. Write / merge `StoryCorpus.json` (Layer 2)

Use this top-level shape:

```json
{
  "meta": {
    "created": "YYYY-MM-DD",
    "updated": "YYYY-MM-DD",
    "version": "1.0",
    "description": "Interview story corpus extracted from user-owned sources for prep and mock interview retrieval."
  },
  "stories": [
    {
      "story_id": "story-uuid",
      "source": "journal | pkm | debrief | resume | other",
      "source_path": "relative/path/to/file",
      "source_entry_ref": "date heading or chunk id",
      "date": "YYYY-MM-DD",
      "raw_summary": "Concise evidence summary from extraction.",
      "themes": ["technical_leadership", "crisis_management"],
      "competencies": ["problem_solving", "ownership", "cross_functional"],
      "result_signal": true,
      "ownership_signal": true,
      "star_ready": false,
      "star": {
        "situation": "",
        "task": "",
        "action": "",
        "result": ""
      },
      "quality": {
        "clarity": "low | medium | high",
        "specificity": "low | medium | high",
        "credibility": "low | medium | high"
      },
      "embedding": [],
      "score_hint": 0.0,
      "last_refreshed": "YYYY-MM-DD"
    }
  ],
  "source_index": [
    {
      "path": "relative/path",
      "mtime": "ISO-8601",
      "status": "processed | skipped",
      "last_processed": "ISO-8601"
    }
  ]
}
```

Merge behavior:
- Preserve existing `story_id` where the same source entry is re-processed.
- Update fields if extraction improved.
- Add new stories for new source entries.
- Remove nothing unless the user explicitly asks for deletion.

### 6. Compression and deduplication

After merge:
- Dedupe near-identical stories (same incident/outcome phrased differently).
- Keep the strongest version (highest clarity/specificity/credibility).
- Mark related story variants if both are useful for different competencies.

### 7. Output + next action

Report:
- files scanned
- files newly processed
- stories added/updated
- stories marked `star_ready`
- key competency coverage gaps

When this runs during launch/setup, suggest running `story-retrieval` inside prep workflows rather than re-mining.
