#!/bin/bash
# Which of the seven Qwen checkpoints does OpenRouter actually serve?
#
# Uses only curl, grep and sed -- all in the macOS base system, so no Xcode
# Command Line Tools, no Python, no Homebrew, no API key.
#
#   chmod +x check_openrouter.sh
#   ./check_openrouter.sh
#
# The match is on the hugging_face_id OpenRouter publishes for each model, not
# on a slug that looks about right: Qwen3-4B and Qwen3-4B-Instruct-2507 are
# different weights, and only one of them is what internals/ measured.

set -u

API="${OPENROUTER_MODELS_URL:-https://openrouter.ai/api/v1/models}"

TARGETS="Qwen/Qwen2.5-0.5B-Instruct
Qwen/Qwen2.5-1.5B-Instruct
Qwen/Qwen2.5-3B-Instruct
Qwen/Qwen2.5-7B-Instruct
Qwen/Qwen3-0.6B
Qwen/Qwen3-4B-Instruct-2507
Qwen/Qwen3-8B"

RAW=$(mktemp "${TMPDIR:-/tmp}/orcat.XXXXXX")
trap 'rm -f "$RAW" "$RAW.ids"' EXIT

printf 'fetching the OpenRouter catalogue ...\n'
if ! curl -sS --fail --max-time 60 -H 'Accept: application/json' "$API" > "$RAW"; then
    echo "could not reach $API -- this needs outbound HTTPS to openrouter.ai." >&2
    exit 1
fi

# Every checkpoint the catalogue declares, one per line.
grep -o '"hugging_face_id":"[^"]*"' "$RAW" \
  | sed 's/.*:"//; s/"$//' | grep -v '^$' | sort -u > "$RAW.ids"

total=$(grep -o '"id":"[^"]*"' "$RAW" | wc -l | tr -d ' ')
served=$(wc -l < "$RAW.ids" | tr -d ' ')
printf '%s entries in the catalogue, %s of them declaring a checkpoint\n\n' "$total" "$served"

if [ "$served" -eq 0 ]; then
    echo "warning: no model declares hugging_face_id; this script cannot tell" >&2
    echo "a checkpoint match from a lookalike. Stopping rather than guessing." >&2
    exit 1
fi

printf '%-30s %-8s %s\n' "checkpoint" "hosted" "slug"
printf -- '------------------------------------------------------------------------\n'

missing=""
for hf in $TARGETS; do
    if grep -qxF "$hf" "$RAW.ids"; then
        # The slug of the object declaring this checkpoint. [^{}]* keeps the
        # match inside one model object; if the field order ever changes this
        # comes back empty and the row still reads "yes".
        slug=$(grep -oE "[{]\"id\":\"[^\"]*\"[^{}]*\"hugging_face_id\":\"$hf\"" "$RAW" \
               | head -1 | sed 's/^{"id":"//; s/".*//')
        printf '%-30s %-8s %s\n' "$hf" "yes" "${slug:-(slug not extracted)}"
    else
        printf '%-30s %-8s %s\n' "$hf" "NO" "-"
        missing="$missing $hf"
    fi
done

echo
if [ -n "$missing" ]; then
    echo "Not served, so local weights are the only route:"
    for hf in $missing; do echo "  $hf"; done
    echo
fi

# Lookalikes: same family and size, different suffix -- a different model.
echo "Similarly named checkpoints that OpenRouter does serve:"
found_near=0
for hf in $TARGETS; do
    prefix=$(echo "$hf" | sed -E 's/(-Instruct.*|-Chat.*)$//')
    near=$(grep -i "^$prefix" "$RAW.ids" | grep -vxF "$hf")
    for n in $near; do
        printf '  %-30s ~ %s\n' "$hf" "$n"
        found_near=1
    done
done
[ "$found_near" -eq 0 ] && echo "  (none)"
echo
echo "A lookalike is not a substitute: sampling it measures different weights"
echo "from the ones internals/ measured."
