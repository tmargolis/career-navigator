#!/usr/bin/env bash
# Career Navigator — SessionStart hook
# 1. Resolves the user's job search directory from ~/.career-navigator
# 2. Syncs new/modified documents from that directory
# 3. Outputs a structured digest prompt for Claude to deliver as a morning brief

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CAREER_NAV_CONFIG="$HOME/.career-navigator"

# --- Resolve user directory ---
if [ ! -f "$CAREER_NAV_CONFIG" ]; then
  cat <<'SETUP_NEEDED'
[CAREER NAVIGATOR — SETUP REQUIRED]

No job search directory configured. To get started:

  1. Run: python3 scripts/init.py /path/to/your/job-search-folder
  2. Restart Claude Desktop
  3. Run /career-navigator:setup to finish configuration
SETUP_NEEDED
  exit 0
fi

USER_DIR=$(cat "$CAREER_NAV_CONFIG" | tr -d '[:space:]')

if [ ! -d "$USER_DIR" ]; then
  echo "[CAREER NAVIGATOR] Job search directory not found: $USER_DIR"
  echo "Run: python3 scripts/init.py /new/path to update the configuration."
  exit 0
fi

PROFILE="$USER_DIR/profile/profile.md"
TRACKER="$USER_DIR/tracker/tracker.json"
ARTIFACTS_INDEX="$USER_DIR/artifacts/index.json"
CORPUS_INDEX="$USER_DIR/corpus/index.json"

# --- First-run detection ---
if [ ! -f "$TRACKER" ] && [ ! -f "$PROFILE" ]; then
  cat <<ONBOARDING
[CAREER NAVIGATOR — FIRST RUN]
Job search directory: $USER_DIR

Welcome to Career Navigator. Run /career-navigator:setup to build your profile
and import your existing resumes and applications. Takes about 2 minutes.
ONBOARDING
  exit 0
fi

# --- Sync new/modified documents ---
"$PLUGIN_ROOT/hooks/sync-watchdir.sh"

# --- Morning digest ---
TODAY=$(date +%Y-%m-%d)

cat <<DIGEST_HEADER
[CAREER NAVIGATOR — SESSION START: $TODAY]
Job search directory: $USER_DIR

Please surface the following as a concise, natural morning brief — no headers, just conversational:

DIGEST_HEADER

if [ -f "$PROFILE" ]; then
  echo "=== USER PROFILE ==="
  head -40 "$PROFILE"
  echo ""
fi

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
  UNIT_COUNT=$(python3 -c "import json; d=json.load(open('$CORPUS_INDEX')); print(len(d.get('experience_units',[])))" 2>/dev/null || echo "unknown")
  TAG_COUNT=$(python3 -c "import json; d=json.load(open('$CORPUS_INDEX')); print(len(d.get('skill_tags',[])))" 2>/dev/null || echo "unknown")
  echo "Experience units in corpus: $UNIT_COUNT"
  echo "Skill tags indexed: $TAG_COUNT"
  echo ""
fi

cat <<DIGEST_INSTRUCTIONS

=== INSTRUCTIONS FOR CLAUDE ===
Based on the data above, deliver a brief morning digest covering:

1. PIPELINE STATUS — count of applications by stage (Applied, Phone Screen, HM Interview, Panel, Final, Offer, Rejected, Ghosted). Skip stages with zero.

2. FOLLOW-UP NEEDED — any applications where status has not changed in more than 7 days and stage is not terminal (Rejected/Withdrawn/Ghosted/Hired). List company + role + days since last update.

3. INTERVIEWS TODAY — scan notes for any interview scheduled today ($TODAY). If found, note that /career-navigator:prep-interview is available.

4. ARTIFACT SUMMARY — brief count of resumes and cover letters. If none, skip.

Keep tone warm but direct. Lead with what needs action today.
DIGEST_INSTRUCTIONS
