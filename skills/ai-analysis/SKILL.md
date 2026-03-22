---
name: ai-analysis
description: >
  Evaluates AI and automation displacement risk for the user's current and
  target roles at the task level, using the Anthropic Economic Index. Identifies
  durable differentiators and suggests narrative reframes where the user's
  positioning overweights high-risk tasks. Invokes the analyst agent.
triggers:
  - "AI displacement"
  - "AI risk"
  - "is my job at risk from AI"
  - "how AI-proof is my career"
  - "future-proof my career"
  - "what parts of my job will AI replace"
  - "assess AI risk"
  - "AI automation risk"
  - "how durable are my skills"
  - "what's my AI displacement risk"
---

Invoke the `analyst` agent to assess AI and automation displacement risk for the user's current and target roles.

## Workflow

### 1. Confirm data exists

Read `{user_dir}/corpus/index.json` and `{user_dir}/profile/profile.md`. If the corpus `units` array is empty or `profile.md` has no target roles:

> "I need your experience corpus and target roles to run a displacement assessment. Run `/career-navigator:add-source` to add a resume, then `/career-navigator:setup` to set your target roles."

Otherwise, proceed.

### 2. Invoke analyst — Operation 3

Hand off to the `analyst` agent with:
- The full `corpus/index.json`
- The full `profile/profile.md`
- Instruction to read `references/AI_Job_Report-Anthropic-2026-03.pdf` before analysis

The agent will decompose the user's current and target roles into tasks, score each task against the Economic Index, build a role-level risk profile, identify durable differentiators, and suggest narrative reframes where needed.

### 3. Present the assessment

```
**AI Displacement Assessment** — {Role}

{1–2 sentence highlight: overall risk posture and the single most important durable differentiator to lead with}

Overall risk profile
  High displacement risk tasks:    {n}%  — {examples}
  Moderate displacement risk tasks: {n}%  — {examples}
  Low displacement risk tasks:      {n}%  — {examples}

Tasks most likely to be automated (2–5 year horizon)
- {Task} — {why it's at risk per Economic Index data}

Durable strengths
- {Capability} — {why it is low risk and likely to grow in value}

Narrative reframe
{If the user's positioning overweights high-risk tasks, specific suggestions for reframing toward durable capabilities in resume summaries, cover letters, and outreach}

Adjacent capabilities worth developing
- {Skill/area} — {why it's strategically valuable given the user's existing foundation}

Source: Anthropic Economic Index, {report date}
```

If multiple target roles are present in `profile.md`, run a separate assessment for each and present them in sequence.

### 4. Suggest next step

> "Want me to run the full analyst report to combine this with your search patterns and transferable strengths? Run `/career-navigator:report`."
