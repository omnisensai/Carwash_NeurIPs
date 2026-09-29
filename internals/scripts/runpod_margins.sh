#!/usr/bin/env bash
# Re-measure the nine models that fit on one card, on the current prompts/.
#
# Why: the runs in results/ were made 21--25 Sep, before benchmark_correct.txt
# existed and while benchmark_goaloriented.txt was still in prompts/. They
# therefore carry a condition the behavioural runs never sampled and lack the
# control. run_internals.py sweeps every prompts/*.txt, so one pass per model
# fixes both: it gains benchmark_correct and drops benchmark_goaloriented,
# leaving the internals measuring exactly the ten behavioural conditions.
#
#   cd /workspace/Carwash_NeurIPs/internals
#   bash scripts/runpod_margins.sh qwen3-0.6b        # one model, ~30 s
#   nohup bash scripts/runpod_margins.sh > margins.log 2>&1 &
#
# Llama-3.3-70B is NOT here: 141 GB in bf16 does not fit on one 80 GB card, so
# it needs a multi-GPU pod. Its existing run stays as it is and therefore has
# no control margin; say so wherever the table is reported.
#
# Each run writes results/<model>/bf16/ IN PLACE, replacing the September run.
# The old ones are in git history. Compute is 18--93 s per model; the weights
# are already in HF_HOME if the behavioural run used this pod.
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
)
MODELS=${*:-llama-3.2-3b llama-3.1-8b qwen2.5-0.5b qwen2.5-1.5b qwen2.5-3b qwen2.5-7b qwen3-0.6b qwen3-4b-2507 qwen3-8b}

python -c "import torch, transformers" 2>/dev/null || \
  pip install -q --break-system-packages "transformers>=4.45" accelerate numpy matplotlib hf_transfer

for m in $MODELS; do
  id="${HF[$m]:-}"
  [ -z "$id" ] && { log "unknown model $m"; continue; }
  log "=== $m ($id) ==="
  python "$HERE/run_internals.py" --model "$id" --out "results/$m/bf16" || { log "FAILED: $m"; continue; }
  python "$HERE/plot_internals.py" "results/$m/bf16" > /dev/null && log "figures written"
done

log "verifying the conditions measured match the behavioural protocol"
python - <<'PY'
import json, glob, sys
want = {"baseline","substrate","benchmark_correct","benchmark_CoT","benchmark_encourage",
        "benchmark_expert","benchmark_hallucination","benchmark_nomistakes",
        "benchmark_threat","benchmark_urgency"}
bad = 0
for f in sorted(glob.glob("results/*/bf16/internals.json")):
    d = json.load(open(f)); got = set(d.get("benchmarks", {}))
    name = f.split("/")[1]
    sha = str(d.get("substrate_sha256"))[:8]
    if got == want and sha == "340228f9":
        print(f"  {name:16} 10 conditions, substrate {sha}")
    else:
        print(f"  {name:16} MISMATCH  missing={sorted(want-got)} extra={sorted(got-want)} sha={sha}")
        bad += 1
print("  FAIL" if bad else "  every run measures the ten behavioural conditions")
sys.exit(1 if bad else 0)
PY
log "done -- commit internals/results/*/bf16/"
