#!/usr/bin/env bash
# Measure the seven Qwens on the prompts/ the repo holds now.
#
# This script produced results/qwen*/bf16/ in this repo (RunPod A40, 25 Sep).
# It re-ran the six Qwens whose earlier runs had used the retired six-line
# substrate and the pre-19-Sep conventional prompts; Qwen3-8B was already
# current from the 21 Sep run and was re-run here as a replication check.
# Those retired runs are in git history before 42b57d0.
#
#   cd /workspace/Carwash_NeurIPs/internals
#   bash scripts/runpod_qwen.sh qwen2.5-0.5b     # one model first: ~2 min, proves the pod
#   nohup bash scripts/runpod_qwen.sh > qwen.log 2>&1 &     # then all seven
#
# Naming one or more models runs only those, and skips the final provenance
# check over all seven, which would otherwise fail on the ones not yet redone.
#
# Pod: one 24 GB card is enough (Qwen3-8B is the largest at ~16 GB in bf16).
# Volume: ~51 GB of weights across the seven, so >= 100 GB at /workspace.
# No HF token needed; all seven are ungated. Minutes of compute per model --
# the downloads dominate.
#
# A result folder that is not on the current prompts is MOVED to
# results/superseded/, not deleted, so nothing is lost if this is re-run by
# mistake. That folder is gitignored and does not belong in a commit.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # internals/scripts
cd "$HERE/.."                                          # results/ is relative to internals/
export HF_HOME=${HF_HOME:-/workspace/hf} HF_HUB_ENABLE_HF_TRANSFER=1 TOKENIZERS_PARALLELISM=false

ARCHIVE=results/superseded
log() { echo "[$(date -u +%H:%M:%S)] $*"; }

# 5b56feb3 is prompts/substrate.txt; 340228f9 is the same text without its
# trailing newline. 6f89be2b is the retired six-line substrate. A current run
# also has benchmark_goaloriented (added 19 Sep) and no benchmark_library
# (deleted 19 Sep), which pins the conventional prompts to the current wording.
is_current() {   # is_current <internals.json>
  [ -e "$1" ] || return 1
  python - "$1" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    sys.exit(1)
bm = d.get("benchmarks") or {}
sys.exit(0 if (d.get("substrate_sha256", "")[:8] in ("5b56feb3", "340228f9")
               and "benchmark_goaloriented" in bm
               and "benchmark_library" not in bm) else 1)
PY
}

run() {   # run <hf-id> <result-folder-name>
  local hf=$1 name=$2
  if is_current "results/$name/bf16/internals.json"; then
    log "skip $name (already measured on the current prompts)"
    return 0
  fi
  # Anything else at that path is the superseded 17 Sep run; keep it.
  if [ -d "results/$name" ]; then
    mkdir -p "$ARCHIVE"
    rm -rf "${ARCHIVE:?}/$name"
    mv "results/$name" "$ARCHIVE/$name"
    log "archived stale results/$name -> $ARCHIVE/$name"
  fi
  log "start $name"
  env MODEL="$hf" NAME="$name" bash runpod.sh
  log "end $name rc=$?"
}

# runpod.sh derives the folder name by lowercasing and stripping a trailing
# "-instruct", which gives the right answer for six of the seven; Qwen3-4B's
# checkpoint ends in "-2507", so NAME is passed explicitly for all of them.
MODELS="qwen2.5-0.5b:Qwen/Qwen2.5-0.5B-Instruct
qwen2.5-1.5b:Qwen/Qwen2.5-1.5B-Instruct
qwen2.5-3b:Qwen/Qwen2.5-3B-Instruct
qwen2.5-7b:Qwen/Qwen2.5-7B-Instruct
qwen3-0.6b:Qwen/Qwen3-0.6B
qwen3-4b-2507:Qwen/Qwen3-4B-Instruct-2507
qwen3-8b:Qwen/Qwen3-8B"

# Smallest first, so a pod that is going to fail fails in two minutes on a
# 1 GB download rather than twenty on a 16 GB one.
want="$*"
for arg in $want; do        # a typo must not look like a run that did nothing
  case "$MODELS" in
    *"$arg:"*) ;;
    *) echo "unknown model: $arg" >&2
       echo "known: $(echo "$MODELS" | cut -d: -f1 | tr '\n' ' ')" >&2
       exit 2 ;;
  esac
done

for entry in $MODELS; do
  name=${entry%%:*} hf=${entry#*:}
  case " $want " in
    "  ") run "$hf" "$name" ;;                    # no arguments: all seven
    *" $name "*) run "$hf" "$name" ;;
    *) continue ;;
  esac
done

if [ -n "$want" ]; then
  log "ran only: $want -- skipping the all-seven provenance check"
  exit 0
fi

log "verifying prompt provenance"
fail=0
for f in results/qwen*/bf16/internals.json; do
  if is_current "$f"; then echo "  ok    $f"; else echo "  STALE $f"; fail=1; fi
done
if [ "$fail" -ne 0 ]; then
  log "at least one run did not use the current prompts/ -- re-pull the repo"
  log "and rerun those models; do not report their numbers."
  exit 1
fi
log "all seven used the current prompts/"

python "$HERE/plot_internals.py" results/qwen*/bf16/ > /dev/null 2>&1 && log "figures written"
log "done -- commit results/qwen*/bf16/ and, if it was created, $ARCHIVE/"
