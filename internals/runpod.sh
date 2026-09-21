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
#   CDIM=1 bash runpod.sh                  # also the constraint-depth intervention map (cdim.py, ~2-3x the passes)
#   CDIM=only bash runpod.sh               # cdim.py alone (internals.json already there)
#
# Precision rule of thumb for 70B: bf16 needs ~140 GB of GPU memory in total
# (2× A100/H100 80 GB, weights are spread automatically), 8bit ~70 GB (one
# 80 GB card, tight), 4bit ~40 GB. Report which one you ran — the 8B numbers
# move by ~0.6 nats between bf16 and nf4, which is exactly the kind of
# environment noise the paper is about.
#
# Results land in results/<model>/<precision>[-<substrate>]/ (e.g.
# results/llama-3.3-70b/bf16-pro/); figures anywhere, no GPU:
#   python plot_internals.py results/llama-3.3-70b/*/
set -euo pipefail
cd "$(dirname "$0")"

MODEL="${MODEL:-unsloth/Llama-3.3-70B-Instruct}"
NAME="${NAME:-$(basename "$MODEL" | tr '[:upper:]' '[:lower:]' | sed -E 's/-instruct$//; s/^meta-//')}"
QUANT="${QUANT:-auto}"
SUBSTRATE="${SUBSTRATE:-substrate.txt}"          # which prompts/ file is the substrate

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
QARG=""; PREC=bf16
if [ "$QUANT" != none ]; then QARG="--quantize $QUANT"; PREC=$QUANT; [ "$QUANT" = 4bit ] && PREC=nf4; fi
VARIANT="$PREC"
[ "$SUBSTRATE" != substrate.txt ] && VARIANT="$PREC-$(basename "$SUBSTRATE" .txt | sed s/^substrate_//)"
OUT="${OUT:-results/$NAME/$VARIANT}"             # e.g. results/llama-3.3-70b/bf16-pro; OUT=... overrides
# NOTE: results/<model>/bf16[-pro]/ of 17-18 Sep were measured on the six-line substrate that
# prompts/substrate.txt held then (now internals/cdim_sweep/ladder/L0.txt). prompts/substrate.txt
# is the nine-line substrate since 19 Sep; write reruns of the old models elsewhere (OUT=...).
LABEL="$(basename "$MODEL") ($PREC)"
echo "model=$MODEL  gpu_total=${TOTAL_MB} MiB  quant=$QUANT  -> $OUT"

export HF_HUB_ENABLE_HF_TRANSFER=1 2>/dev/null || true
mkdir -p "$OUT"
CDIM="${CDIM:-0}"
if [ "$CDIM" != only ]; then
python run_internals.py --model "$MODEL" $QARG --substrate "$SUBSTRATE" --out "$OUT" \
    --label "$LABEL, $SUBSTRATE" 2>&1 | tee "$OUT/run.log"

python plot_internals.py "$OUT" > /dev/null && echo "figures in $OUT/"
fi
if [ "$CDIM" != 0 ]; then                        # Mechanistic_paper.md experiment; 70B: every 2nd row
  case "$MODEL" in *70B*|*70b*) STRIDE="${CDIM_STRIDE:-2}";; *) STRIDE="${CDIM_STRIDE:-1}";; esac
  python cdim.py --model "$MODEL" $QARG --substrate "$SUBSTRATE" --out "$OUT" --label "$LABEL, $SUBSTRATE" \
      --row-stride "$STRIDE" --path-stride $((STRIDE * 2)) 2>&1 | tee "$OUT/cdim.log"
  python plot_cdim.py "$OUT" > /dev/null && echo "CDIM figures in $OUT/"
fi
echo "done — send back the whole $OUT/ folder (json + png + summary.md + run.log)"
