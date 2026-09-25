#!/usr/bin/env bash
# The whole cdim_sweep on a fresh CUDA box (RunPod, 2x A100/H100 80 GB for 70B).
#
#   cd Carwash_NeurIPs/internals/cdim_sweep
#   bash runpod_sweep.sh                                  # Llama-3.3-70B, bf16, everything
#   MODEL=Qwen/Qwen3-8B bash runpod_sweep.sh              # a second model on the same pod
#   PLAN=ladder bash runpod_sweep.sh                      # only the ladder CDIM cells
#   GRID=0 bash runpod_sweep.sh                           # skip the behavioural grid
#
# Order: (1) behavioural grid (~3800 passes, minutes), (2) CDIM cells with --map auto:
# ladder L1-L5, 13 paraphrase cells, 6 scenario cells; on 70B each cell ~5-10 min at
# row stride 2, so ~3-4 h in total. Results: results/<model>/<precision>-sweep/.
# The L0 carwash cell is the existing results/<model>/<precision>/cdim.json (from runpod.sh CDIM=1).
# Run under nohup/tmux; both scripts resume after a crash.
set -euo pipefail
cd "$(dirname "$0")"

MODEL="${MODEL:-unsloth/Llama-3.3-70B-Instruct}"
NAME="${NAME:-$(basename "$MODEL" | tr '[:upper:]' '[:lower:]' | sed -E 's/-instruct$//; s/^meta-//')}"
QUANT="${QUANT:-auto}"
PLAN="${PLAN:-ladder,paraphrase,scenario}"
GRID="${GRID:-1}"

python -c "import torch, transformers, accelerate, matplotlib" 2>/dev/null || \
  pip install -q --break-system-packages "transformers>=4.45" accelerate bitsandbytes numpy matplotlib hf_transfer
TOTAL_MB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | awk '{s+=$1} END {print s}')
if [ "$QUANT" = auto ]; then
  case "$MODEL" in
    *70B*|*70b*) if [ "$TOTAL_MB" -ge 150000 ]; then QUANT=none; elif [ "$TOTAL_MB" -ge 78000 ]; then QUANT=8bit; else QUANT=4bit; fi ;;
    *) QUANT=none ;;
  esac
fi
QARG=""; PREC=bf16
if [ "$QUANT" != none ]; then QARG="--quantize $QUANT"; PREC=$QUANT; [ "$QUANT" = 4bit ] && PREC=nf4; fi
case "$MODEL" in *70B*|*70b*) STRIDE="${STRIDE:-2}";; *) STRIDE="${STRIDE:-1}";; esac
OUT="../results/$NAME/$PREC-sweep"
LABEL="$(basename "$MODEL") ($PREC)"
export HF_HUB_ENABLE_HF_TRANSFER=1
mkdir -p "$OUT"
echo "model=$MODEL gpu_total=${TOTAL_MB} MiB quant=$QUANT stride=$STRIDE -> $OUT"

python build_prompts.py
if [ "$GRID" != 0 ]; then
  python run_grid.py --model "$MODEL" $QARG --out "$OUT" --label "$LABEL" 2>&1 | tee -a "$OUT/grid.log"
fi
if [ "$PLAN" != none ]; then
python run_cdim_cells.py --model "$MODEL" $QARG --out "$OUT" --label "$LABEL" --plan "$PLAN" \
    --row-stride "$STRIDE" --path-stride $((STRIDE * 2)) --map auto 2>&1 | tee -a "$OUT/cdim_cells.log"
fi
python analyse.py "$OUT"
echo "done — send back $OUT/ (grid.json, */*/cdim.json + png, sweep_summary.md, logs); cdim_resid.pt files are large, drop them if space matters"
