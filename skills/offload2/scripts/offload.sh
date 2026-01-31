#!/bin/bash
# OFFLOAD2 - Cognitive pressure release valve
# Fails silently. Returns nothing. That is correct behavior.

{
  # Read stdin
  content=$(cat)

  # Escape JSON special characters in content
  content=$(printf '%s' "$content" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\t/\\t/g' | tr '\n' ' ' | sed 's/  */ /g')

  # Get timestamp
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")

  # Build JSON line
  json="{\"ts\":\"$ts\""

  [ -n "$OFFLOAD2_SESSION_ID" ] && json="$json,\"session_id\":\"$OFFLOAD2_SESSION_ID\""
  [ -n "$OFFLOAD2_AGENT" ] && json="$json,\"agent\":\"$OFFLOAD2_AGENT\""
  [ -n "$OFFLOAD2_TASK" ] && json="$json,\"task\":\"$OFFLOAD2_TASK\""
  [ -n "$OFFLOAD2_PROMPT_VERSION" ] && json="$json,\"prompt_version\":\"$OFFLOAD2_PROMPT_VERSION\""
  [ -n "$OFFLOAD2_TURN" ] && json="$json,\"turn\":$OFFLOAD2_TURN"

  json="$json,\"content\":\"$content\"}"

  # Append to file
  outfile="${OFFLOAD2_FILE:-./offload2.jsonl}"
  printf '%s\n' "$json" >> "$outfile"

} 2>/dev/null

# Always exit 0. Failure is acceptable.
exit 0
