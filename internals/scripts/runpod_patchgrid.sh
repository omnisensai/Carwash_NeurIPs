#!/usr/bin/env bash
# Layerwise patching of EVERY condition into the baseline, for the nine models
# that fit on one card.
#
# Why: run_internals.py patches one source into the baseline, the substrate, so
# the paper can say where the substrate installs its effect but not whether the
# conventional conditions install one anywhere. This pass patches each
# prompts/*.txt in turn, which turns "the conventional conditions do not flip
# the answer" into "we injected their residual stream at every layer and no
# layer flips it".
#
#   cd /workspace/Carwash_NeurIPs/internals
#   bash scripts/runpod_patchgrid.sh qwen3-0.6b       # one model, ~1 min
#   nohup bash scripts/runpod_patchgrid.sh > patchgrid.log 2>&1 &
#
# Run it AFTER runpod_margins.sh on the same pod: patch_grid.py cross-checks its
# substrate row against the patching array in internals.json, which only means
# anything if that file is the current run.
#
# Llama-3.3-70B is NOT here, for the same reason as in runpod_margins.sh: 141 GB
# in bf16 needs a multi-GPU pod. It therefore has no grid; say so where the
# figure is reported.
#
# Each run writes results/<model>/bf16/patch_grid.json. Nothing existing is
# overwritten. Cost is ten conditions x (n_layers + 1) forward passes with no
# generation, a few minutes per model once the weights are resident.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE/.."
export HF_HOME=${HF_HOME:-/workspace/hf} HF_HUB_ENABLE_HF_TRANSFER=1 TOKENIZERS_PARALLELISM=false
log() { echo "[$(date -u +%H:%M:%S)] $*"; }

declare -A HF=(
  [llama-3.2-3b]=unsloth/Llama-3.2-3B-Instruct
  [llama-3.1-8b]=unsloth/Llama-3.1-8B-Instruct
  [qwen2.5-0.5b]=Qwen/Qwen2.5-0.5B-Instruct
  [qwen2.5-1.5b]=Qwen/Qwen2.5-1.5B-Instruct
  [qwen2.5-3b]=Qwen/Qwen2.5-3B-Instruct
  [qwen2.5-7b]=Qwen/Qwen2.5-7B-Instruct
  [qwen3-0.6b]=Qwen/Qwen3-0.6B
  [qwen3-4b-2507]=Qwen/Qwen3-4B-Instruct-2507
  [qwen3-8b]=Qwen/Qwen3-8B
  # NOT in the default sweep: 141 GB in bf16 needs >1 card. On a multi-GPU
  # pod run_internals.py's load() sets device_map=auto by itself, so
  #   bash scripts/runpod_patchgrid.sh llama-3.3-70b
  # is all it takes there. On one card it will OOM; that is the intended
  # failure, not something to work around by quantizing.
  [llama-3.3-70b]=unsloth/Llama-3.3-70B-Instruct
  # Not in the default sweep. Dense, bf16, single 80 GB card; they extend the
  # Qwen2.5 and Qwen3 ladders past the 4B threshold the paper reports. They have
  # no behavioural counterpart, so their margins cannot be checked against an
  # RC/NR/RI state -- report them as a scale supplement, not as fleet members.
  # Qwen3-30B-A3B is deliberately absent: patching a residual into a
  # mixture-of-experts run does not transplant the routing, so it is a different
  # experiment from the one these scripts implement.
  [qwen2.5-14b]=Qwen/Qwen2.5-14B-Instruct
  [qwen2.5-32b]=Qwen/Qwen2.5-32B-Instruct
  [qwen3-14b]=Qwen/Qwen3-14B
  [qwen3-32b]=Qwen/Qwen3-32B
  # 145 GB in bf16: needs more than one card, like llama-3.3-70b.
  [qwen2.5-72b]=Qwen/Qwen2.5-72B-Instruct
)
MODELS=${*:-llama-3.2-3b llama-3.1-8b qwen2.5-0.5b qwen2.5-1.5b qwen2.5-3b qwen2.5-7b qwen3-0.6b qwen3-4b-2507 qwen3-8b}

python -c "import torch, transformers" 2>/dev/null || \
  pip install -q --break-system-packages "transformers>=4.45" accelerate numpy matplotlib hf_transfer

for m in $MODELS; do
  id="${HF[$m]:-}"
  [ -z "$id" ] && { log "unknown model $m"; continue; }
  log "=== $m ($id) ==="
  python "$HERE/patch_grid.py" --model "$id" --out "results/$m/bf16" || { log "FAILED: $m"; continue; }
done

log "verifying every grid written in this pass"
MODELS="$MODELS" python - <<'PY'
import json, os, sys
want = {"baseline","substrate","benchmark_correct","benchmark_CoT","benchmark_encourage",
        "benchmark_expert","benchmark_hallucination","benchmark_nomistakes",
        "benchmark_threat","benchmark_urgency"}
bad = 0
for name in os.environ.get("MODELS", "").split():
    f = f"results/{name}/bf16/patch_grid.json"
    if not os.path.exists(f):
        print(f"  {name:16} NO GRID WRITTEN"); bad += 1; continue
    d = json.load(open(f))
    got = set(d.get("grid", {}))
    sha = str(d.get("substrate_sha256"))[:8]
    sp  = d.get("self_patch_max_abs_dM")
    dev = d.get("substrate_row_vs_internals_max_abs")
    why = []
    if got != want: why.append(f"conditions missing={sorted(want-got)} extra={sorted(got-want)}")
    if sha != "340228f9": why.append(f"substrate sha {sha}")
    if sp is None or sp > 1e-3: why.append(f"self-patch not flat ({sp})")
    if dev is None: why.append("no cross-check against internals.json")
    elif dev > 0.05: why.append(f"substrate row disagrees with internals.json by {dev:.3f}")
    if why:
        print(f"  {name:16} MISMATCH  " + "; ".join(why)); bad += 1
    else:
        print(f"  {name:16} 10 conditions x {d['n_layers']} layers, substrate {sha}, "
              f"self-patch {sp:.4f}, vs internals.json {dev:.4f}")
print("  FAIL" if bad else "  every grid in this pass is on the behavioural prompts and self-consistent")
print("  note: llama-3.3-70b has no grid (141 GB, needs multi-GPU).")
sys.exit(1 if bad else 0)
PY
log "done -- commit internals/results/*/bf16/patch_grid.json"
