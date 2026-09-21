#!/usr/bin/env python3
"""Behavioural grid: M for every (question x substrate) cell of cdim_sweep (GPU).

    python run_grid.py --model unsloth/Llama-3.3-70B-Instruct --out results/llama-3.3-70b/bf16-sweep
    python run_grid.py --model Qwen/Qwen3-8B --out results/qwen3-8b/bf16-sweep --cells A

Cells come from build_prompts.cells(): every scenario x paraphrase body x tail
under none / L0..L5 / S / pro filled for the question's own scenario (grid A), and
every question under the carwash-filled L2..L5 and S at P0 x T1 (grid B, leak test).
One forward pass per cell (chat template, logits at the answer position only);
M = log P(drive) - log P(walk) summed over surface forms, as everywhere else.
Resumable: existing cells in <out>/grid.json are skipped. No model is ever run
on CPU by this script unless --device cpu is passed explicitly.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from build_prompts import GEN, cells, load as load_prompts, write_generated   # noqa: E402
from run_internals import answer_ids, load, margin_from_logits, parse_prompt, render   # noqa: E402


def system_text(D, substrate: str, fill: str) -> str | None:
    if substrate == "none":
        return None
    return parse_prompt((GEN / "substrates" / fill / f"{substrate}.txt").read_text())["system"]


def key(c: dict) -> str:
    return "|".join(str(c[k]) for k in ("grid", "q", "body", "tail", "substrate", "fill"))


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True, help="result dir; grid.json is written into it")
    ap.add_argument("--quantize", choices=["4bit", "8bit"], default=None)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--dtype", default=None, choices=["bfloat16", "float16", "float32"])
    ap.add_argument("--label", default=None)
    ap.add_argument("--cells", default="all", help="'all', 'A', 'B', or a comma list of substrates (none,L0..L5,S,pro)")
    ap.add_argument("--flush-every", type=int, default=100)
    args = ap.parse_args()

    D = load_prompts()
    write_generated(D)
    C = cells(D)
    if args.cells in ("A", "B"):
        C = [c for c in C if c["grid"] == args.cells]
    elif args.cells != "all":
        keep = set(args.cells.split(","))
        C = [c for c in C if c["substrate"] in keep]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    f = out / "grid.json"
    res = json.loads(f.read_text()) if f.exists() else {"model": args.label or args.model, "cells": {}}
    done = res["cells"]
    todo = [c for c in C if key(c) not in done]
    print(f"{len(C)} cells, {len(done)} done, {len(todo)} to run", flush=True)
    if not todo:
        return

    print(f"loading {args.model} ({args.quantize or args.dtype or 'default dtype'}, {args.device}) ...", flush=True)
    tok, model = load(args.model, args.quantize, args.device, args.dtype)
    aid = answer_ids(tok)
    dev = model.get_input_embeddings().weight.device
    drive, walk = set(aid["drive"]), set(aid["walk"])
    res.update({"quantize": args.quantize, "dtype": args.dtype, "torch": torch.__version__})
    t0 = time.time()
    for i, c in enumerate(todo, 1):
        s = D["scenarios"][c["q"]]
        user = D["bodies"][c["body"]].format(task=s["task"], place=s["place"]) + "\n\n" + D["tails"][c["tail"]]
        p = {"system": system_text(D, c["substrate"], c["fill"]), "user": user}
        text = render(tok, p, raw=False)
        ids = tok(text, add_special_tokens=False, return_tensors="pt")["input_ids"].to(dev)
        lg = model(input_ids=ids, use_cache=False, logits_to_keep=1).logits[0, -1].float().cpu()
        m = margin_from_logits(lg, aid)
        am = m["argmax"]
        ans = "drive" if am in drive else "walk" if am in walk else "other"
        done[key(c)] = {**c, "correct": s["correct"], "M": m["M_sum"], "M_first": m["M_first"],
                        "p_drive": m["p_drive"], "p_walk": m["p_walk"], "argmax": tok.decode(am),
                        "answer": ans, "n_tokens": int(ids.shape[1])}
        if i % 20 == 0 or i == len(todo):
            print(f"  {i}/{len(todo)}  {key(c)}  M={m['M_sum']:+.2f} {ans}  ({time.time() - t0:.0f} s)", flush=True)
        if i % args.flush_every == 0 or i == len(todo):
            res["seconds"] = round(time.time() - t0, 1)
            f.write_text(json.dumps(res, indent=0, ensure_ascii=False))
    print(f"wrote {f} ({len(done)} cells) in {res['seconds']} s", flush=True)


if __name__ == "__main__":
    main()
