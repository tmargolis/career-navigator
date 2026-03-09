#!/usr/bin/env bash
# Career Navigator — Document Sync
# Scans the root of the user's job search directory for new or modified files.
# Excludes Career Navigator's own subdirectories (corpus/, tracker/, artifacts/, profile/).
# Runs at SessionStart (via session-start.sh) and at midnight via Schedule hook.

CAREER_NAV_CONFIG="$HOME/.career-navigator"

if [ ! -f "$CAREER_NAV_CONFIG" ]; then
  exit 0
fi

USER_DIR=$(cat "$CAREER_NAV_CONFIG" | tr -d '[:space:]')

if [ ! -d "$USER_DIR" ]; then
  exit 0
fi

SYNC_STATE="$USER_DIR/.sync-state.json"

# Find documents at the root level only (maxdepth 1) — skip managed subdirectories
if [ -f "$SYNC_STATE" ]; then
  NEW_FILES=$(find "$USER_DIR" -maxdepth 1 -type f \( \
    -name "*.pdf" -o -name "*.docx" -o -name "*.doc" \
    -o -name "*.md" -o -name "*.txt" -o -name "*.rtf" \
  \) -newer "$SYNC_STATE" 2>/dev/null)
else
  # First sync — treat all root-level documents as new
  NEW_FILES=$(find "$USER_DIR" -maxdepth 1 -type f \( \
    -name "*.pdf" -o -name "*.docx" -o -name "*.doc" \
    -o -name "*.md" -o -name "*.txt" -o -name "*.rtf" \
  \) 2>/dev/null)
fi

if [ -z "$NEW_FILES" ]; then
  exit 0
fi

FILE_COUNT=$(echo "$NEW_FILES" | grep -c .)
TODAY=$(date +%Y-%m-%d)

cat <<SYNC_PROMPT
[CAREER NAVIGATOR — DOCUMENT SYNC: $TODAY]
$FILE_COUNT new or updated file(s) in: $USER_DIR

Files to process:
$NEW_FILES

For each file:
1. Read the file.
2. Classify: resume/CV, cover letter, application record, or other job search material.
3. Resume or CV → extract experience units, assign skill tags, set performance weights (1.0), append to $USER_DIR/corpus/index.json. Skip if this file path is already in corpus source_documents[].
4. Cover letter or application document → extract application details (company, role, date, status), create or update record in $USER_DIR/tracker/tracker.json.
5. Ambiguous → use judgment.

After processing all files, write {"last_sync": "$TODAY", "last_sync_epoch": $(date +%s)} to $SYNC_STATE
SYNC_PROMPT
