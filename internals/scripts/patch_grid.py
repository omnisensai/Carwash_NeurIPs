#!/usr/bin/env python3
"""Layerwise activation patching of EVERY condition into the baseline run.

`run_internals.py` patches one source into the baseline: the substrate. This
script runs the same intervention with every `prompts/*.txt` as the source, so
the substrate's trajectory can be read against the trajectory of each
conventional condition and of the control.

For each source condition c and each layer l:

    run the baseline prompt, replace the residual stream at the answer
    position after layer l with c's residual at the same position and
    layer, and read M at the answer position.

Nothing about the measurement differs from `run_internals.py`. The chat
template (`render`), the answer position and the drive/walk token sets
(`answer_ids`), the patch hook (`Patch`), the forward pass (`forward`) and the
margin (`margin_from_logits`) are imported from it rather than reimplemented,
so the `substrate` row of this grid reproduces that file's `patching` array and
the `baseline` row is the self-patch control: flat at the baseline margin.

    python scripts/patch_grid.py --model unsloth/Llama-3.2-3B-Instruct \
        --out results/llama-3.2-3b/bf16

Writes `patch_grid.json` next to `internals.json`. Cost is
n_conditions x (n_layers + 1) forward passes with no generation and no
logit-lens sweep: 370 for a 36-layer model over ten conditions, a few minutes
on one card once the weights are resident.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from run_internals import (  # noqa: E402
    PROMPTS, Capture, Patch, answer_ids, forward, load, margin_from_logits,
    parse_prompt, render,
)


def resid_stack(model, tok, text: str, cap: Capture, aid: dict) -> tuple[torch.Tensor, dict]:
    """Residual stream at the answer position: row 0 = embedding output,
    row l+1 = output of layer l. Same rows run_internals.py patches from.

    want_attn=True is not cosmetic: `output_attentions` forces eager attention,
    and the eager and SDPA kernels do not agree bit for bit. `analyse_prompt`
    captures the substrate stack under eager, so capturing under SDPA here
    would shift every patched margin by a few hundredths of a nat against the
    `patching` array in internals.json. Same kernel, same numbers."""
    _, lg, _ = forward(model, tok, text, cap, want_attn=True)
    n = len(cap.resid)
    return (torch.stack([cap.emb] + [cap.resid[i] for i in range(n)]),
            margin_from_logits(lg, aid))


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="HF id or local snapshot path")
    ap.add_argument("--out", required=True, help="output directory (same one as internals.json)")
    ap.add_argument("--quantize", choices=["4bit", "8bit"], default=None)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--dtype", default=None, choices=["bfloat16", "float16", "float32"])
    ap.add_argument("--raw", action="store_true",
                    help="feed the prompt files verbatim instead of the chat template")
    ap.add_argument("--label", default=None, help="model label stored in the json")
    ap.add_argument("--baseline", default="baseline.txt")
    ap.add_argument("--substrate", default="substrate.txt")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    print(f"loading {args.model} ({args.quantize or args.dtype or 'default dtype'}, "
          f"{args.device}) ...", flush=True)
    tok, model = load(args.model, args.quantize, args.device, args.dtype)
    aid = answer_ids(tok)
    print("answer token ids:", aid, flush=True)
    cap = Capture(model)

    base_p = parse_prompt((PROMPTS / args.baseline).read_text())
    base_text = render(tok, base_p, args.raw)
    _, base_m = resid_stack(model, tok, base_text, cap, aid)
    base_M = base_m["M_sum"]

    res = {
        "model": args.label or args.model, "quantize": args.quantize,
        "device": args.device, "dtype": args.dtype,
        "baseline_file": args.baseline, "substrate_file": args.substrate,
        "baseline_sha256": base_p["sha256"],
        "substrate_sha256": parse_prompt((PROMPTS / args.substrate).read_text())["sha256"],
        "question": base_p["user"], "raw_prompts": args.raw,
        "answer_token_ids": aid, "baseline_M_sum": base_M,
        "note": "grid[c][l] = M at the answer position of the BASELINE run with "
                "condition c's residual patched in at the answer position after "
                "layer l; l runs 0..n_layers-1. grid['baseline'] is the "
                "self-patch control and must be flat at baseline_M_sum.",
        "grid": {}, "source_M_sum": {},
    }

    n_layers = None
    for f in sorted(PROMPTS.glob("*.txt")):
        name = f.stem
        p = parse_prompt(f.read_text())
        # Same rule as run_internals.py's benchmarks loop: a file with no user
        # block (the substrate is one) gets the baseline's question; a
        # benchmark file carries its intervention IN the user block and must be
        # left alone, or the condition is silently reduced to the baseline.
        if p["user"] is None or name.startswith("substrate"):
            p["user"] = base_p["user"]
        st, src_m = resid_stack(model, tok, render(tok, p, args.raw), cap, aid)
        if n_layers is None:
            n_layers = st.shape[0] - 1
            res["n_layers"] = n_layers
            print(f"n_layers={n_layers}  baseline M_sum={base_M:+.3f}", flush=True)
        elif st.shape[0] - 1 != n_layers:
            sys.exit(f"{name}: {st.shape[0] - 1} layers against {n_layers} — refusing to patch")

        res["source_M_sum"][name] = src_m["M_sum"]
        row = []
        for l in range(n_layers):
            ph = Patch(model, l, st[l + 1])
            try:
                _, lg, _ = forward(model, tok, base_text, None, want_attn=False)
            finally:
                ph.remove()
            row.append(margin_from_logits(lg, aid)["M_sum"])
        res["grid"][name] = row
        cross = next((l for l, v in enumerate(row) if v > 0), None)
        print(f"  {name:24s} source M={src_m['M_sum']:+8.3f}  patched "
              f"{row[0]:+8.3f} -> {row[-1]:+8.3f}  max={max(row):+8.3f}  "
              f"cross={'L%d' % cross if cross is not None else '--'}", flush=True)
        del st

    # the self-patch control has to come back flat, or the hook is in the wrong place
    sp = res["grid"].get(Path(args.baseline).stem)
    if sp is not None:
        drift = max(abs(v - base_M) for v in sp)
        res["self_patch_max_abs_dM"] = drift
        print(f"self-patch control: max|dM| = {drift:.4f}"
              f"{'' if drift < 1e-3 else '   *** NOT FLAT — do not cite this run ***'}", flush=True)

    # cross-check against the substrate-only patch already in internals.json:
    # same intervention, same source, so the two must agree to run-to-run noise
    ij = out / "internals.json"
    if ij.exists():
        try:
            prev = json.loads(ij.read_text())
            ref = (prev.get("patching") or {}).get("M_sum")
            mine = res["grid"].get(Path(args.substrate).stem)
            if ref and mine and len(ref) == len(mine):
                dev = max(abs(a - b) for a, b in zip(ref, mine))
                res["substrate_row_vs_internals_max_abs"] = dev
                print(f"substrate row vs internals.json patching: max|diff| = {dev:.4f}"
                      f"{'' if dev < 0.05 else '   *** CHECK THIS BEFORE CITING ***'}", flush=True)
            if ref and mine and len(ref) != len(mine):
                print(f"note: internals.json patching has {len(ref)} layers "
                      f"against {len(mine)} here — not comparing", flush=True)
        except Exception as e:                       # a stale json must not kill the run
            print(f"note: could not cross-check against internals.json ({e})", flush=True)

    res["seconds"] = round(time.time() - t0, 1)
    res["torch"] = torch.__version__
    import transformers
    res["transformers"] = transformers.__version__
    (out / "patch_grid.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    cap.remove()
    print(f"wrote {out / 'patch_grid.json'} in {res['seconds']} s", flush=True)


if __name__ == "__main__":
    main()
