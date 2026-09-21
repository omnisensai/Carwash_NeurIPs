#!/usr/bin/env python3
"""CDIM maps for the sweep cells, one model load (GPU).

    python run_cdim_cells.py --model unsloth/Llama-3.3-70B-Instruct --out results/llama-3.3-70b/bf16-sweep \
        --row-stride 2 --path-stride 4
    python run_cdim_cells.py --model Qwen/Qwen3-8B --out results/qwen3-8b/bf16-sweep --plan ladder

Plans (all use the carwash question P0 + T1 unless stated; control question =
the paired walk scenario under the same substrate, as cdim.py does with the library):
  ladder      --levels (default L1..L5 and S) filled for carwash; L0 / pro are the first-round
              results/<model>/<prec>/ and <prec>-pro/ cdim.json when those were measured on them
              -> <out>/ladder/<level>/
  paraphrase  --level (default S, the official substrate) with bodies P1..P11 (tail T1) plus P0+T0 and P0+T2
              -> <out>/paraphrase/<body>_<tail>/
  scenario    --level with every drive scenario except carwash (P0 + T1)
              -> <out>/scenario/<scenario>/      (--with-pro: the same under pro -> <out>/scenario-pro/<scenario>/)
Every cell dir gets cdim.json + cdim_resid.pt (+ the plot_cdim figures at the end).
Resumable: cells with a cdim.json are skipped. --map auto maps only lines with
|Delta| >= --min-delta (at least the largest), which is what the analysis needs.
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
from build_prompts import GEN, load as load_prompts, question_text, write_generated   # noqa: E402
from cdim import run_cdim                                                                     # noqa: E402
from run_internals import answer_ids, load, parse_prompt                                       # noqa: E402


def sub_of(fill: str, level: str):
    """(substrate file, counterfactuals) of a ladder level filled for a scenario, from generated/."""
    cfj = json.loads((GEN / "substrates" / fill / "counterfactuals.json").read_text())
    return str(GEN / "substrates" / fill / f"{level}.txt"), cfj[f"{level}.txt"]


def plan_cells(D, args) -> list[dict]:
    out = []
    plans = args.plan.split(",")
    if "ladder" in plans:
        for lvl in args.levels.split(","):
            f, cfs = sub_of("carwash", lvl)
            out.append({"exp": "ladder", "cell": lvl, "substrate": f, "cfs": cfs, "q": "carwash", "body": "P0",
                        "tail": "T1", "control": "library", "level": lvl})
    if "paraphrase" in plans:
        combos = [(b, "T1") for b in args.bodies.split(",")] + [("P0", "T0"), ("P0", "T2")]
        f, cfs = sub_of("carwash", args.level)
        for b, t in combos:
            out.append({"exp": "paraphrase", "cell": f"{b}_{t}", "substrate": f, "cfs": cfs, "q": "carwash",
                        "body": b, "tail": t, "control": "library", "level": args.level})
    if "scenario" in plans:
        scen = args.scenarios.split(",") if args.scenarios else \
            [s for s, v in D["scenarios"].items() if v["kind"] == "vehicle" and s != "carwash"]
        for s in scen:
            ctrl = D["scenarios"][s]["control"] or "library"
            f, cfs = sub_of(s, args.level)
            out.append({"exp": "scenario", "cell": s, "substrate": f, "cfs": cfs, "q": s, "body": "P0", "tail": "T1",
                        "control": ctrl, "level": args.level})
            if args.with_pro:
                f, cfs = sub_of(s, "pro")
                out.append({"exp": "scenario-pro", "cell": s, "substrate": f, "cfs": cfs, "q": s, "body": "P0",
                            "tail": "T1", "control": ctrl, "level": "pro"})
    return out


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True, help="sweep result dir, e.g. results/llama-3.3-70b/bf16-sweep")
    ap.add_argument("--quantize", choices=["4bit", "8bit"], default=None)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--dtype", default=None, choices=["bfloat16", "float16", "float32"])
    ap.add_argument("--label", default=None)
    ap.add_argument("--plan", default="ladder,paraphrase,scenario")
    ap.add_argument("--levels", default="L1,L2,L3,L4,L5,S", help="ladder cells")
    ap.add_argument("--level", default="S", help="substrate level of the paraphrase / scenario cells")
    ap.add_argument("--bodies", default="P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11")
    ap.add_argument("--scenarios", default=None, help="comma list; default: every drive scenario but carwash")
    ap.add_argument("--with-pro", action="store_true")
    ap.add_argument("--map", default="auto")
    ap.add_argument("--min-delta", type=float, default=1.0)
    ap.add_argument("--row-stride", type=int, default=1)
    ap.add_argument("--path-stride", type=int, default=2)
    ap.add_argument("--no-controls", action="store_true")
    ap.add_argument("--no-path", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    D = load_prompts()
    write_generated(D)
    cells = plan_cells(D, args)
    out = Path(args.out)
    todo = [c for c in cells if not (out / c["exp"] / c["cell"] / "cdim.json").exists()]
    print(f"{len(cells)} cells, {len(todo)} to run", flush=True)
    if not todo:
        return
    print(f"loading {args.model} ({args.quantize or args.dtype or 'default dtype'}, {args.device}) ...", flush=True)
    tok, model = load(args.model, args.quantize, args.device, args.dtype)
    aid = answer_ids(tok)
    label = args.label or args.model
    t0 = time.time()
    dirs = []
    for i, c in enumerate(todo, 1):
        d = out / c["exp"] / c["cell"]
        print(f"\n=== [{i}/{len(todo)}] {c['exp']}/{c['cell']}: {c['q']} {c['body']} {c['tail']} under {Path(c['substrate']).name}"
              f" (control {c['control']}) -> {d}", flush=True)
        sub_p = parse_prompt(Path(c["substrate"]).read_text())
        qf = GEN / "questions" / f"{c['q']}_{c['body']}_{c['tail']}.txt"
        base_p = parse_prompt(qf.read_text())
        assert base_p["user"] == question_text(D, c["q"], c["body"], c["tail"]).strip("\n")
        lf = GEN / "questions" / f"{c['control']}_{c['body']}_{c['tail']}.txt"
        lib_p = parse_prompt(lf.read_text())
        meta = {"quantize": args.quantize, "device": args.device, "dtype": args.dtype,
                "substrate_file": str(Path(c["substrate"]).relative_to(HERE.parent.parent)),
                "baseline_file": str(qf.relative_to(HERE.parent.parent)), "library_file": str(lf.relative_to(HERE.parent.parent)),
                "sweep": {k: c[k] for k in ("exp", "cell", "q", "body", "tail", "control", "level")}}
        run_cdim(tok, model, aid, sub_p, base_p, lib_p, c["cfs"], d,
                 label=f"{label}, {c['exp']}/{c['cell']}", map_sel=args.map, min_delta=args.min_delta,
                 row_stride=args.row_stride, path_stride=args.path_stride, controls=not args.no_controls,
                 library=True, path=not args.no_path, seed=args.seed, meta=meta)
        dirs.append(d)
        print(f"    elapsed {time.time() - t0:.0f} s", flush=True)
    try:
        from plot_cdim import plot_dir
        for d in dirs:
            plot_dir(d)
        print("figures written", flush=True)
    except Exception as e:                       # figures are re-creatable offline
        print(f"plot_cdim failed ({e}); run plot_cdim.py on the cell dirs later", flush=True)


if __name__ == "__main__":
    main()
