#!/usr/bin/env bash
# Career Navigator — SessionStart hook
# Outputs a structured digest prompt for Claude to surface at session start.
# Claude receives this as context and delivers a natural morning digest.

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROFILE="$PLUGIN_ROOT/data/profile/profile.md"
TRACKER="$PLUGIN_ROOT/data/applications/tracker.json"
ARTIFACTS_INDEX="$PLUGIN_ROOT/data/artifacts/index.json"
CORPUS_INDEX="$PLUGIN_ROOT/data/corpus/index.json"

# --- First-run detection ---
if [ ! -f "$TRACKER" ] && [ ! -f "$PROFILE" ]; then
  cat <<'ONBOARDING'
[CAREER NAVIGATOR — FIRST RUN]

Welcome to Career Navigator. No job search data exists yet.

Run /cn:setup to get started — it will build your profile, import your
resumes and past applications from Google Drive if connected, and configure
job search integrations. Takes about 2 minutes.
ONBOARDING
  exit 0
fi

# --- Returning session digest ---
TODAY=$(date +%Y-%m-%d)

cat <<DIGEST_HEADER
[CAREER NAVIGATOR — SESSION START DIGEST]
Date: $TODAY

Please surface the following as a concise, natural morning brief — no headers, just conversational:

TRACKER DATA:
DIGEST_HEADER

# Output profile summary for Claude to use as context
if [ -f "$PROFILE" ]; then
  echo "=== USER PROFILE ==="
  # Output just the first 40 lines — enough for target roles, companies, comp floor
  head -40 "$PROFILE"
  echo ""
fi

# Output tracker contents for Claude to parse
if [ -f "$TRACKER" ]; then
  echo "=== APPLICATION TRACKER ==="
  cat "$TRACKER"
  echo ""
fi

if [ -f "$ARTIFACTS_INDEX" ]; then
  echo "=== ARTIFACT INVENTORY ==="
  cat "$ARTIFACTS_INDEX"
  echo ""
fi

if [ -f "$CORPUS_INDEX" ]; then
  echo "=== CORPUS SUMMARY ==="
  # Just output unit and tag counts, not the full corpus
  UNIT_COUNT=$(python3 -c "import json,sys; d=json.load(open('$CORPUS_INDEX')); print(len(d.get('experience_units',[])))" 2>/dev/null || echo "unknown")
  TAG_COUNT=$(python3 -c "import json,sys; d=json.load(open('$CORPUS_INDEX')); print(len(d.get('skill_tags',[])))" 2>/dev/null || echo "unknown")
  echo "Experience units in corpus: $UNIT_COUNT"
  echo "Skill tags indexed: $TAG_COUNT"
  echo ""
fi

cat <<DIGEST_INSTRUCTIONS

=== INSTRUCTIONS FOR CLAUDE ===
Based on the data above, deliver a brief morning digest covering:

1. PIPELINE STATUS — count of applications by stage (Applied, Phone Screen, HM Interview, Panel, Final, Offer, Rejected, Ghosted). Skip stages with zero. If no applications, say so briefly.

2. FOLLOW-UP NEEDED — flag any applications where status has not changed in more than 7 days and current stage is not a terminal state (Rejected/Withdrawn/Ghosted/Hired). List company + role + days since last update.

3. INTERVIEWS TODAY — scan application notes for any interview scheduled today ($TODAY). If found, mention it and note that /cn:prep-interview is available.

4. ARTIFACT SUMMARY — brief count of resumes and cover letters generated. If none, skip.

Keep the tone warm but direct. Lead with what requires action today. If nothing requires action, say so clearly and suggest a next productive step.
DIGEST_INSTRUCTIONS
