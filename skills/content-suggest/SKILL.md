---
name: content-suggest
description: "Recommends LinkedIn and professional post topics, angles, and cadence aligned to profile and ExperienceLibrary. Invokes writer."
triggers:
  - "linkedin post ideas"
  - "what should i post"
  - "content suggestions"
  - "topics for linkedin"
  - "/career-navigator:content-suggest"
---

Invoke **`writer`** in **`content-suggest`** mode.

## Invocation

- Use the exact agent name **`writer`**. Retry once if invocation fails.

## Workflow

1. Read `{user_dir}/CareerNavigator/profile.md`, `{user_dir}/CareerNavigator/ExperienceLibrary.json`, and **`voice-profile.md`** if present.
2. Ask **`writer`** for **5–8 topic ideas** with: why it fits, risk level (low drama vs spicy), and suggested format (short post vs thread vs link + comment).
3. If the user wants a **full draft** of one topic: ensure **`writer`** voice preflight is satisfied (`voice-profile.md` has **`## User writing samples`** or **`## User writing samples (launch)`**, or ask once for posts / **skip**—same pattern as **`draft-outreach`**). Then invoke **`writer`** to draft one post. **`writer`** must **save** the draft as **`.md`** under **`{user_dir}/LinkedIn Posts/`** (create the folder if needed), **append `artifacts-index.json`** with `"type": "linkedin_post"`, and tell the user the file path to open and edit. Offer **`evaluate-post`** before they publish.
