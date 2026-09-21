#!/usr/bin/env bash
# Everything for the 21 Sep 2026 pod, in order of value; every phase skips when its
# output exists, so the script can be re-launched after a crash.
#   cd /workspace/Carwash_NeurIPs/internals && nohup bash pod_master.sh > master.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")"
export HF_HOME=${HF_HOME:-/workspace/hf} HF_HUB_ENABLE_HF_TRANSFER=1 TOKENIZERS_PARALLELISM=false
python -c "import brainscope" 2>/dev/null || pip install -q --break-system-packages brainscope
log() { echo "[$(date -u +%H:%M:%S)] $*"; }
phase() {  # phase <name> <done-file> <command...>
  local name=$1 done=$2; shift 2
  if [ -e "$done" ]; then log "skip $name ($done exists)"; return 0; fi
  log "start $name"; "$@"; local rc=$?; log "end $name rc=$rc"; return $rc
}
L70=unsloth/Llama-3.3-70B-Instruct; L8=unsloth/Llama-3.1-8B-Instruct; L3=unsloth/Llama-3.2-3B-Instruct; Q8=Qwen/Qwen3-8B

# 0. sanity on 3B (also its rerun on the new substrate: baseline + all benchmarks + substrate + CDIM)
phase sanity-3b results/llama-3.2-3b/bf16/cdim.json env MODEL=$L3 CDIM=1 bash runpod.sh
# 1. 70B: internals + CDIM on the new substrate
phase 70b-internals results/llama-3.3-70b/bf16/cdim.json env MODEL=$L70 CDIM=1 bash runpod.sh
# 2. 70B: explicitness ladder (L1..L5, S) + grid
phase 70b-ladder results/llama-3.3-70b/bf16-sweep/ladder/S/cdim.json env MODEL=$L70 PLAN=ladder bash cdim_sweep/runpod_sweep.sh
# 3. 8B + Qwen3-8B: internals + CDIM on the new substrate
phase 8b-internals results/llama-3.1-8b/bf16/cdim.json env MODEL=$L8 CDIM=1 bash runpod.sh
phase qwen8b-internals results/qwen3-8b/bf16/cdim.json env MODEL=$Q8 CDIM=1 bash runpod.sh
# 4. brainscope drive-frame direction across all conditions
phase 70b-frame results/llama-3.3-70b/bf16-frame/frame.json python brainscope_frame.py --model $L70 --out results/llama-3.3-70b/bf16-frame
phase qwen8b-frame results/qwen3-8b/bf16-frame/frame.json python brainscope_frame.py --model $Q8 --out results/qwen3-8b/bf16-frame
phase 8b-frame results/llama-3.1-8b/bf16-frame/frame.json python brainscope_frame.py --model $L8 --out results/llama-3.1-8b/bf16-frame
# 5. 70B paraphrase + scenario cells; Qwen3-8B ladder
phase 70b-cells results/llama-3.3-70b/bf16-sweep/scenario/van/cdim.json env MODEL=$L70 PLAN=paraphrase,scenario GRID=0 bash cdim_sweep/runpod_sweep.sh
phase qwen8b-ladder results/qwen3-8b/bf16-sweep/ladder/S/cdim.json env MODEL=$Q8 PLAN=ladder bash cdim_sweep/runpod_sweep.sh
# 6. the 8B family (eleven fine-tunes); frees the 70B cache first (disk)
rm -rf "$HF_HOME"/hub/models--unsloth--Llama-3.3-70B-Instruct
phase family-8b results/llama-3.1-8b-lexi-uncensored-v2/bf16/cdim.json bash cdim_sweep/run_family_8b.sh
# 7. Mistral Large 2411 in 4-bit (123B dense): internals + CDIM; frees the family caches first
rm -rf "$HF_HOME"/hub/models--NousResearch--* "$HF_HOME"/hub/models--allenai--* "$HF_HOME"/hub/models--cognitivecomputations--* \
       "$HF_HOME"/hub/models--mlabonne--* "$HF_HOME"/hub/models--aaditya--* "$HF_HOME"/hub/models--akjindal53244--* "$HF_HOME"/hub/models--Orenguteng--*
phase mistral-large results/mistral-large-2411/nf4/cdim.json env MODEL=mistralai/Mistral-Large-Instruct-2411 NAME=mistral-large-2411 QUANT=4bit CDIM=1 bash runpod.sh
# figures + summaries that need no GPU
python plot_internals.py results/*/bf16/ results/*/nf4/ > /dev/null 2>&1 && log "overview.png"
python plot_cdim.py results/llama-3.3-70b/bf16 results/llama-3.1-8b/bf16 results/qwen3-8b/bf16 results/llama-3.2-3b/bf16 > /dev/null 2>&1 && log "cdim_overview.png"
python cdim_sweep/analyse.py results/*/bf16-sweep > /dev/null 2>&1 && log "sweep summaries"
python plot_frame.py results/*/bf16-frame > /dev/null 2>&1 && log "frame figures"
log "ALL DONE"
