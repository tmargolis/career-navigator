#!/usr/bin/env bash
set -euo pipefail

CONTENT=$(cat "${CLAUDE_PLUGIN_ROOT}/hooks/context/session-start.md")

echo "{\"systemMessage\": $(echo "$CONTENT" | jq -Rs .)}"