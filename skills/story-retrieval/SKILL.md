---
name: story-retrieval
description: >
  Retrieves a small, competency-matched subset of interview stories from
  CareerNavigator/StoryCorpus.json for prep and mock interview workflows.
  Returns only the highest-fit stories so the model can expand into STAR
  responses without loading full raw journals.
triggers:
  - "retrieve interview stories"
  - "find stories for this interview"
  - "story retrieval"
  - "pull stories for competency"
---

Select targeted stories from the persistent story corpus for immediate interview use.

## Workflow

### 1. Resolve `{user_dir}` and gate

Require `{user_dir}/CareerNavigator/StoryCorpus.json`.

If missing or empty:
- Ask to run `mine-stories` first (or run it now with user approval if appropriate).
- Continue with reduced-confidence fallback from `ExperienceLibrary.json` only if the user wants to proceed immediately.

### 2. Build retrieval intent

Use available interview context:
- `application_id` or `company` + `role`
- `interview_stage`
- JD text (if available)
- user-stated focus areas (leadership, conflict, ambiguity, technical depth, etc.)

Derive desired competencies/themes for this specific interview.

### 3. Rank stories

For each story in corpus, score by:
- competency overlap
- theme overlap
- stage relevance (e.g. executive -> strategy/influence; technical -> architecture/debugging)
- quality signals (clarity/specificity/credibility)
- result + ownership signals
- recency/diversity (avoid returning 10 near-duplicates)

### 4. Return compact context set (Layer 3)

Return only a small subset:
- default: 8-12 stories
- for short prep: 5-8
- for deep prep: up to 15 if user explicitly asks

Output each item as:
- `story_id`
- one-line `raw_summary`
- mapped competencies/themes
- why selected for this interview
- STAR readiness status (`star_ready`)
- short coaching note if STAR gaps exist

### 5. Optional STAR promotion

For top stories with incomplete STAR fields:
- draft concise STAR skeletons
- set `star_ready: true` only when S/T/A/R are each concrete and evidence-backed
- write updates back to `StoryCorpus.json`

### 6. Handoff contract for interview-coach

When invoked by prep/mock flows, provide a compact handoff payload:

```json
{
  "retrieval_context": {
    "company": "...",
    "role": "...",
    "interview_stage": "..."
  },
  "selected_stories": [
    {
      "story_id": "...",
      "summary": "...",
      "competencies": ["..."],
      "themes": ["..."],
      "star_ready": true
    }
  ]
}
```

This payload is the preferred interview evidence input for `interview-coach`.
