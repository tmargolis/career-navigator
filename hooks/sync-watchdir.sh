#!/usr/bin/env bash
# Career Navigator — Watch Directory Sync
# Scans the user's watch directory for new or modified documents.
# Outputs a structured prompt for Claude to extract content into corpus and tracker.
# Runs at SessionStart (via session-start.sh) and at midnight via Schedule hook.

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROFILE="$PLUGIN_ROOT/data/profile/profile.md"
SYNC_STATE="$PLUGIN_ROOT/data/.sync-state.json"

# --- No profile yet ---
if [ ! -f "$PROFILE" ]; then
  exit 0
fi

# --- Read watch directory from profile ---
WATCH_DIR=$(grep -A2 "^## Watch Directory" "$PROFILE" | grep "^\*\*Path\*\*:" | sed 's/\*\*Path\*\*: *//' | tr -d ' ')

if [ -z "$WATCH_DIR" ] || [ "$WATCH_DIR" = "[/absolute/path/to/your/job-search-documents]" ]; then
  exit 0
fi

if [ ! -d "$WATCH_DIR" ]; then
  echo "[CAREER NAVIGATOR SYNC] Watch directory not found: $WATCH_DIR"
  echo "Update the path in data/profile/profile.md or run /career-navigator:setup."
  exit 0
fi

# --- Find new or modified files ---
# Use sync state file as the timestamp reference if it exists
if [ -f "$SYNC_STATE" ]; then
  NEW_FILES=$(find "$WATCH_DIR" -type f \( \
    -name "*.pdf" -o -name "*.docx" -o -name "*.doc" \
    -o -name "*.md" -o -name "*.txt" -o -name "*.rtf" \
  \) -newer "$SYNC_STATE" 2>/dev/null)
else
  # First sync — treat all files as new
  NEW_FILES=$(find "$WATCH_DIR" -type f \( \
    -name "*.pdf" -o -name "*.docx" -o -name "*.doc" \
    -o -name "*.md" -o -name "*.txt" -o -name "*.rtf" \
  \) 2>/dev/null)
fi

# --- Nothing new — exit silently ---
if [ -z "$NEW_FILES" ]; then
  exit 0
fi

FILE_COUNT=$(echo "$NEW_FILES" | grep -c .)
TODAY=$(date +%Y-%m-%d)

cat <<SYNC_PROMPT
[CAREER NAVIGATOR — WATCH DIRECTORY SYNC: $TODAY]
$FILE_COUNT new or updated file(s) detected in: $WATCH_DIR

Files to process:
$NEW_FILES

For each file listed above:
1. Read the file.
2. Classify it: resume/CV, cover letter, application record, or other job search material.
3. Resume or CV → run the /career-navigator:add-source extraction: parse experience units, assign skill tags, set performance weights (1.0), append to data/corpus/index.json. Skip if this exact file path already appears in corpus source_documents[].
4. Cover letter, application email, or document addressed to a specific company → extract application details (company, role, date, status) and create or update the record in data/tracker/tracker.json.
5. Ambiguous document → use judgment; extract whatever is applicable.

After processing all files, update $SYNC_STATE by writing: {"last_sync": "$TODAY", "last_sync_epoch": $(date +%s)}
SYNC_PROMPT
