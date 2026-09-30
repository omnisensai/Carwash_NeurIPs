#!/usr/bin/env bash
# Sample the nine locally run models under the correct_answer condition.
#
# Why: correct_answer was run on 2026-09-29 through hosted APIs only, which
# covers the 15 hosted models of the study population. The other eight --- the
# six Qwens and the local arms of Llama 3.1-8B and 3.2-3B --- have no row.
# Qwen2.5-3B is sampled too, so the local fleet stays complete; it is outside
# the population (10/10 correct at baseline) and is dropped at analysis time.
# Llama 3.3-70B is not here: its population row is the hosted one, already run.
#
#   cd /workspace/Carwash_NeurIPs
#   bash behavioural/workbench/runpod_correct.sh qwen3-0.6b     # one model, ~2 min
#   nohup bash behavioural/workbench/runpod_correct.sh > correct.log 2>&1 &
#
# Pod: one 24 GB card is enough (Qwen3-8B at ~17 GB is the largest).
# Volume: ~74 GB of weights across the nine, so >= 150 GB at /workspace.
# Ten short samples per model: the downloads dominate, the compute is seconds.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"      # behavioural/workbench
REPO="$(cd "$HERE/../.." && pwd)"
cd "$REPO"
export HF_HOME=${HF_HOME:-/workspace/hf} HF_HUB_ENABLE_HF_TRANSFER=1 TOKENIZERS_PARALLELISM=false

OUT=${OUT:-behavioural/runs/correct}
MODELS=${*:-llama-3.2-3b llama-3.1-8b qwen2.5-0.5b qwen2.5-1.5b qwen2.5-3b qwen2.5-7b qwen3-0.6b qwen3-4b-2507 qwen3-8b}
log() { echo "[$(date -u +%H:%M:%S)] $*"; }

python -c "import torch, transformers" 2>/dev/null || \
  pip install -q --break-system-packages "transformers>=4.45" accelerate hf_transfer

# The prompt must hash to what the hosted rows recorded, or the local rows are
# not comparable to them. Refuse to sample anything if it does not.
log "checking the prompt against the published rows"
python behavioural/workbench/run_local_fleet.py --dry-run --conditions correct || {
  log "FATAL: benchmark_correct.txt does not reproduce 0b8320cf -- not sampling"; exit 1; }

for m in $MODELS; do
  done_file=$(ls "$OUT"/local_${m}_local_*.jsonl 2>/dev/null | head -1)
  if [ -n "$done_file" ]; then log "skip $m -- already in $done_file"; continue; fi
  log "=== $m ==="
  python behavioural/workbench/run_local_fleet.py \
      --models "$m" --conditions correct --n 10 --outdir "$OUT" || log "FAILED: $m"
done

log "verifying every row carries the expected prompt digest"
python - "$OUT" <<'PY'
import json, sys, glob, collections, pathlib
out = pathlib.Path(sys.argv[1]); bad = 0
seen = collections.defaultdict(int)
for f in glob.glob(str(out / "local_*.jsonl")):
    for ln in open(f):
        if not ln.strip():
            continue
        r = json.loads(ln)
        seen[r["model_label"]] += 1
        if r.get("prompt_sha256") != "0b8320cfb2df8522a27549d5b2a450d816737d4cd0e03cff07b5eabc9db07d9b":
            print("  WRONG PROMPT:", f, r.get("sample_index")); bad += 1
        if r.get("intervention") != "correct_answer":
            print("  WRONG CONDITION:", f, r.get("intervention")); bad += 1
for m in sorted(seen):
    print(f"  {m:16} {seen[m]} rows")
print("  FAIL" if bad else "  all rows carry prompt 0b8320cf under correct_answer")
sys.exit(1 if bad else 0)
PY
log "regenerating the per-condition summaries"
python behavioural/workbench/write_summaries.py

log "done -- commit $OUT/local_*.jsonl and the refreshed summary.md files"
