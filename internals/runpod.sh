#!/usr/bin/env bash
# Run the baseline-vs-substrate internals sweep on a RunPod (or any fresh
# CUDA box) for the big Llama. Everything is a handful of short forward
# passes, so the run itself takes minutes; the download dominates.
#
#   git clone <this repo> && cd Carwash_NeurIPs/internals
#   bash runpod.sh                         # Llama-3.3-70B, precision picked from GPU memory
#   MODEL=unsloth/Llama-3.1-8B-Instruct bash runpod.sh   # parity check with the aorus runs
#   QUANT=4bit bash runpod.sh              # force nf4 (one 48 GB card is enough)
#   SUBSTRATE=substrate_pro.txt bash runpod.sh           # another substrate file
#
# Precision rule of thumb for 70B: bf16 needs ~140 GB of GPU memory in total
# (2× A100/H100 80 GB, weights are spread automatically), 8bit ~70 GB (one
# 80 GB card, tight), 4bit ~40 GB. Report which one you ran — the 8B numbers
# move by ~0.6 nats between bf16 and nf4, which is exactly the kind of
# environment noise the paper is about.
#
# Results land in results/<name>/internals.json; make the figures anywhere
# (no GPU needed) with:  python plot_internals.py results/<name>
set -euo pipefail
cd "$(dirname "$0")"

MODEL="${MODEL:-unsloth/Llama-3.3-70B-Instruct}"
NAME="${NAME:-$(basename "$MODEL" | tr '[:upper:]' '[:lower:]')}"
QUANT="${QUANT:-auto}"
SUBSTRATE="${SUBSTRATE:-substrate.txt}"          # which prompts/ file is the substrate
[ "$SUBSTRATE" != substrate.txt ] && NAME="$NAME-$(basename "$SUBSTRATE" .txt | sed s/^substrate_//)"

python -c "import torch, transformers, accelerate" 2>/dev/null || \
  pip install -q "torch>=2.4" "transformers>=4.45" accelerate bitsandbytes numpy matplotlib
python -c "import bitsandbytes" 2>/dev/null || pip install -q bitsandbytes

TOTAL_MB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | awk '{s+=$1} END {print s}')
if [ "$QUANT" = auto ]; then
  case "$MODEL" in
    *70B*|*70b*)
      if   [ "$TOTAL_MB" -ge 150000 ]; then QUANT=none
      elif [ "$TOTAL_MB" -ge 78000 ];  then QUANT=8bit
      else                                  QUANT=4bit; fi ;;
    *) QUANT=none ;;
  esac
fi
echo "model=$MODEL  gpu_total=${TOTAL_MB} MiB  quant=$QUANT  -> results/$NAME-$QUANT"

QARG=""; LABEL="$(basename "$MODEL") (bf16)"
if [ "$QUANT" != none ]; then QARG="--quantize $QUANT"; LABEL="$(basename "$MODEL") ($QUANT)"; fi

export HF_HUB_ENABLE_HF_TRANSFER=1 2>/dev/null || true
mkdir -p results
python run_internals.py --model "$MODEL" $QARG --substrate "$SUBSTRATE" --out "results/$NAME-$QUANT" \
    --label "$LABEL, $SUBSTRATE" 2>&1 | tee "results/$NAME-$QUANT.log"

python plot_internals.py "results/$NAME-$QUANT" > /dev/null && echo "figures in results/$NAME-$QUANT/"
echo "done — send back the whole results/$NAME-$QUANT/ folder (json + png + summary.md)"
