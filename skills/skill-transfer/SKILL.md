---
name: skill-transfer
description: >
  Identifies the user's core transferable capabilities from their experience
  corpus and maps them to role types and industries beyond their current track.
  Surfaces non-obvious destinations and flags domain-dependent vs. portable
  strengths. Invokes the analyst agent.
triggers:
  - "what are my transferable skills"
  - "where else could I work"
  - "what roles could I transition to"
  - "what industries could I move into"
  - "analyze my transferable strengths"
  - "what are my core strengths"
  - "where do my skills apply"
  - "career pivot analysis"
  - "what could I do besides"
---

Invoke the `analyst` agent to identify the user's transferable strengths and map them to new destinations.

## Workflow

### 1. Confirm data exists

Read `{user_dir}/corpus/index.json` and `{user_dir}/profile/profile.md`. If the corpus `units` array is empty:

> "Your experience corpus is empty. Run `/career-navigator:add-source` to add a resume first."

Otherwise, proceed.

### 2. Invoke analyst — Operation 2

Hand off to the `analyst` agent with:
- The full `corpus/index.json`
- The full `profile/profile.md`

The agent will identify core capabilities, their transferable form, and the role types and industries where they have high value — including destinations the user may not have considered.

### 3. Present the analysis

```
**Transferable Strengths Analysis**

{1–2 sentence highlight: the single most compelling or surprising strength finding — lead with the capability, not a preamble}

Core capabilities identified
1. {Capability name} — {1-sentence description of what the evidence shows}
   Evidence: {specific roles/achievements that demonstrate this}
   High-value destinations: {role types and industries where this is prized}

2. ...

Portable across industries
{Strengths that transfer broadly with minimal repositioning}

Domain-dependent
{Strengths that are valuable but require specific context or credentials to translate}

Non-obvious opportunities
{Role types or industries the user likely hasn't considered, with specific rationale}
```

### 4. Suggest next step

> "Want me to run an AI displacement assessment to see which of these strengths are most durable? Run `/career-navigator:ai-analysis`."
