#!/usr/bin/env python3
"""Pre-flight for run_internals.py: check the prompts and the margin, no GPU.

Loads a tokenizer (not the model), so it runs in seconds. Three checks:

  1. every prompts/*.txt renders to the text the behavioural runs recorded,
     compared by sha256 against behavioural/runs/*/*.jsonl
  2. the drive/walk token sets are non-empty, disjoint, and decode to what
     they claim
  3. M on a synthetic logit vector equals log(sum P(drive)) - log(sum P(walk))
     computed independently

    python scripts/preflight.py --model Qwen/Qwen3-0.6B
"""
import argparse, glob, hashlib, json, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from run_internals import (PROMPTS, DRIVE_VARIANTS, WALK_VARIANTS, answer_ids,
                           margin_from_logits, parse_prompt, render)

ap = argparse.ArgumentParser()
ap.add_argument("--model", default="Qwen/Qwen3-0.6B")
args = ap.parse_args()

fail = 0

# --- 1. prompts against the behavioural record ------------------------------
recorded = {}
for f in glob.glob(str(HERE.parent.parent / "behavioural/runs/*/*.jsonl")):
    for ln in open(f):
        if not ln.strip():
            continue
        d = json.loads(ln)
        if d.get("prompt_sha256") and d.get("user"):
            recorded.setdefault(d["prompt_sha256"], d["user"])
        if d.get("system_sha256") not in (None, "NONE") and d.get("system"):
            recorded.setdefault(d["system_sha256"], d["system"])

print("1. prompt texts against the behavioural runs")
for p in sorted(PROMPTS.glob("*.txt")):
    pp = parse_prompt(p.read_text(encoding="utf-8"))
    for part in ("system", "user"):
        txt = pp.get(part)
        if not txt:
            continue
        h = hashlib.sha256(txt.encode()).hexdigest()
        if h in recorded:
            print(f"   ok   {p.name:30} {part:6} {h[:8]}")
            continue
        # run_internals strips trailing whitespace before hashing; the
        # behavioural runs sent some files with their trailing newline. Same
        # text, two digests -- match on the stripped form and say so.
        hit = next((rh for rh, rtxt in recorded.items()
                    if rtxt.rstrip() == txt.rstrip()), None)
        if hit:
            print(f"   ok   {p.name:30} {part:6} {h[:8]}  "
                  f"(behavioural recorded {hit[:8]}: same text, trailing newline)")
        else:
            print(f"   NOT IN BEHAVIOURAL RUNS {p.name:30} {part:6} {h[:8]}")
            fail += 1

# --- 2. token sets ----------------------------------------------------------
print(f"\n2. answer token sets for {args.model}")
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained(args.model)
ids = answer_ids(tok)
for k, variants in (("drive", DRIVE_VARIANTS), ("walk", WALK_VARIANTS)):
    kept = [(i, repr(tok.decode([i]))) for i in ids[k]]
    dropped = [v for v in variants
               if len(tok.encode(v, add_special_tokens=False)) != 1]
    print(f"   {k:5} {len(kept)} single-token forms: {kept}")
    if dropped:
        print(f"         dropped (multi-token): {dropped}")
    if not kept:
        print(f"         EMPTY SET -- M would be undefined"); fail += 1
overlap = set(ids["drive"]) & set(ids["walk"])
print(f"   overlap between the two sets: {overlap or 'none'}")
if overlap:
    fail += 1

# --- 3. the margin on a known vector ----------------------------------------
print("\n3. margin arithmetic on a synthetic logit vector")
import torch
V = max(max(ids["drive"]), max(ids["walk"])) + 10
lg = torch.full((V,), -20.0)
for i, t in enumerate(ids["drive"]):
    lg[t] = 2.0 - i          # a few distinct values
for i, t in enumerate(ids["walk"]):
    lg[t] = 1.0 - i
got = margin_from_logits(lg, ids)
lp = torch.log_softmax(lg, -1)
want = math.log(sum(lp[t].exp().item() for t in ids["drive"])) \
     - math.log(sum(lp[t].exp().item() for t in ids["walk"]))
print(f"   margin_from_logits M_sum = {got['M_sum']:+.10f}")
print(f"   independent recompute    = {want:+.10f}")
d = abs(got["M_sum"] - want)
print(f"   |difference| = {d:.2e}  {'ok' if d < 1e-5 else 'MISMATCH'}")
if d >= 1e-5:
    fail += 1

print("\nFAIL" if fail else "\nall checks passed")
sys.exit(1 if fail else 0)
