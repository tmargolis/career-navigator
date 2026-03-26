#!/usr/bin/env bash
set -euo pipefail

CONTENT_PATH="${CLAUDE_PLUGIN_ROOT}/hooks/context/session-start.md"
CONTENT="$(cat "$CONTENT_PATH")"
export CONTENT

# Avoid external deps like jq; JSON-escape via Python (present on macOS/Linux).
python3 - <<'PY'
import json, os, sys
sys.stdout.write(json.dumps({"systemMessage": os.environ.get("CONTENT", "")}))
PY