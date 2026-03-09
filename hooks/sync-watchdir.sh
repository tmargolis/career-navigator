#!/usr/bin/env bash
# Career Navigator — Document Sync
# Scans the user's job search directory for new or modified files.
# Excludes Career Navigator's own managed subdirectories (profile/, corpus/, tracker/).
# Runs at SessionStart (via session-start.sh) and at midnight via Schedule hook.

# --- Resolve config path (platform-aware) ---
case "$(uname -s)" in
  Darwin) CAREER_NAV_CONFIG="$HOME/Library/Application Support/Claude/cowork_plugins/career-navigator/config.json" ;;
  Linux)  CAREER_NAV_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/Claude/cowork_plugins/career-navigator/config.json" ;;
  *)      CAREER_NAV_CONFIG="$APPDATA/Claude/cowork_plugins/career-navigator/config.json" ;;
esac

if [ ! -f "$CAREER_NAV_CONFIG" ]; then
  exit 0
fi

USER_DIR=$(python3 -c "import json; print(json.load(open('$CAREER_NAV_CONFIG'))['user_dir'])" 2>/dev/null | tr -d '[:space:]')

if [ -z "$USER_DIR" ] || [ ! -d "$USER_DIR" ]; then
  exit 0
fi

SYNC_STATE="$USER_DIR/.cn-sync-state.json"

# Find documents recursively, pruning Career Navigator's own managed subdirectories
FIND_ARGS=(
  "$USER_DIR"
  \( -name "profile" -o -name "corpus" -o -name "tracker" \) -prune
  -o -type f \(
    -name "*.pdf" -o -name "*.docx" -o -name "*.doc"
    -o -name "*.md" -o -name "*.txt" -o -name "*.rtf"
  \)
)

if [ -f "$SYNC_STATE" ]; then
  NEW_FILES=$(find "${FIND_ARGS[@]}" -newer "$SYNC_STATE" -print 2>/dev/null)
else
  # First sync — all matching files are new
  NEW_FILES=$(find "${FIND_ARGS[@]}" -print 2>/dev/null)
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
3. Resume or CV → extract experience units, assign skill tags, set performance weights (1.0), append to $USER_DIR/corpus/index.json. Skip if this file path is already in corpus source_documents[]. Also skip any file whose path appears in $USER_DIR/artifacts-index.json (those are Career Navigator outputs, not source documents).
4. Cover letter or application document → extract application details (company, role, date, status), create or update record in $USER_DIR/tracker/tracker.json.
5. Ambiguous → use judgment.

After processing, write {"last_sync": "$TODAY", "last_sync_epoch": $(date +%s)} to $SYNC_STATE
SYNC_PROMPT
