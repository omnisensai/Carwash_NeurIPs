#!/usr/bin/env bash
# The "controlled trial": one architecture (Llama-3/3.1 8B, 32 layers, d=4096),
# many subjects (fine-tunes of it), the same before/after measurement on each.
#
#   cd Carwash_NeurIPs/internals/cdim_sweep
#   bash run_family_8b.sh                              # every model in ROSTER, substrate.txt
#   SUBSTRATE=substrate_pro.txt bash run_family_8b.sh  # another prompts/ substrate (e.g. the new ones)
#   PLAN=ladder bash run_family_8b.sh                  # also the ladder cells per model (default: grid + scenario)
#   ROSTER="unsloth/Llama-3.1-8B-Instruct NousResearch/Hermes-3-Llama-3.1-8B" bash run_family_8b.sh
#
# Per model: (1) runpod.sh — baseline vs substrate internals (lens, answer-site
# patching, DLA, line ablations, benchmarks), the "before / after"; (2) a gate:
# the substrate must move M by >= MIN_DELTA nats (default 3) and land on Drive,
# otherwise the subject gets the behavioural grid only; (3) for subjects that
# pass, the CDIM map and runpod_sweep.sh (grid + chosen CDIM cells). Everything bf16 on one 80 GB card; an 8B pass is
# ~30 ms, so one model is ~15-30 min. Results: results/<model>/bf16/ and bf16-sweep/.
#
# Same layer count in every subject, so hand-off rows, patch-flip layers and
# DLA layers compare directly; the analysis is then a distribution over subjects.
# Excluded on purpose: meta-llama/* (gated; unsloth mirrors are identical
# tensors), meta-llama/Llama-3.1-8B base (no chat template: opens with markdown,
# see CLAUDE.md), DeepSeek-R1-Distill-Llama-8B and Nemotron-Nano-8B (reasoning
# models: they emit a <think> block first, so the first-token margin is not the
# decision). Add them to ROSTER only with a decision-position readout.
set -euo pipefail
cd "$(dirname "$0")"

ROSTER="${ROSTER:-
unsloth/llama-3-8b-Instruct
unsloth/Llama-3.1-8B-Instruct
NousResearch/Hermes-2-Pro-Llama-3-8B
NousResearch/Hermes-3-Llama-3.1-8B
allenai/Llama-3.1-Tulu-3-8B
allenai/Llama-3.1-Tulu-3.1-8B
cognitivecomputations/dolphin-2.9.4-llama3.1-8b
mlabonne/Meta-Llama-3.1-8B-Instruct-abliterated
aaditya/Llama3-OpenBioLLM-8B
akjindal53244/Llama-3.1-Storm-8B
Orenguteng/Llama-3.1-8B-Lexi-Uncensored-V2
}"
SUBSTRATE="${SUBSTRATE:-substrate.txt}"
PLAN="${PLAN:-scenario}"
export HF_HUB_ENABLE_HF_TRANSFER=1

MIN_DELTA="${MIN_DELTA:-3}"     # nats: the substrate must move M by at least this much, and the answer must be Drive
for m in $ROSTER; do
  name="$(basename "$m" | tr '[:upper:]' '[:lower:]' | sed -E 's/-instruct$//; s/^meta-//')"
  echo "=============== $m  ($name)"
  # 1. cheap before/after first (baseline + every prompts/*.txt + substrate, lens, patching, DLA, ablations)
  MODEL="$m" NAME="$name" QUANT=none SUBSTRATE="$SUBSTRATE" CDIM=0 bash ../runpod.sh 2>&1 | tail -3
  # 2. gate: does the substrate actually work on this subject?
  verdict=$(python - "$name" "$MIN_DELTA" <<'PY'
import json, sys
name, mind = sys.argv[1], float(sys.argv[2])
r = json.load(open(f"../results/{name}/bf16/internals.json"))
b, s = r["prompts"]["baseline"]["final"]["M_sum"], r["prompts"]["substrate"]["final"]["M_sum"]
ok = (s - b) >= mind and s > 0
print(f"{'PASS' if ok else 'FAIL'} baseline M={b:+.2f} substrate M={s:+.2f} delta={s-b:+.2f} greedy={r['prompts']['substrate']['final']['greedy']!r}")
PY
)
  echo "gate: $verdict" | tee -a ../results/family_gate.log
  case "$verdict" in
    PASS*) MODEL="$m" NAME="$name" QUANT=none SUBSTRATE="$SUBSTRATE" CDIM=only bash ../runpod.sh 2>&1 | tail -3
           MODEL="$m" NAME="$name" QUANT=none PLAN="$PLAN" bash runpod_sweep.sh 2>&1 | tail -3 ;;
    *)     echo "  substrate does not flip $name (or moves it < $MIN_DELTA nats): no maps, grid only"
           MODEL="$m" NAME="$name" QUANT=none PLAN=none GRID=1 bash runpod_sweep.sh 2>&1 | tail -3 ;;
  esac
done
echo "gate summary:"; cat ../results/family_gate.log
python ../plot_internals.py ../results/*/bf16/ > /dev/null && echo "overview.png updated"
python ../plot_cdim.py $(for m in $ROSTER; do n="$(basename "$m" | tr '[:upper:]' '[:lower:]' | sed -E 's/-instruct$//; s/^meta-//')"; [ -f "../results/$n/bf16/cdim.json" ] && echo "../results/$n/bf16"; done) > /dev/null && echo "cdim_overview.png updated"
echo "done — the family table: python analyse.py ../results/*/bf16-sweep; per-model summary.md and cdim_summary.md in results/<model>/bf16/"
