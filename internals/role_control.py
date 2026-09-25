#!/usr/bin/env python3
"""Role-placement control: does the substrate work because of what it says,
or because it is delivered as a system message?

The fleet applies the substrate as a system prompt and every conventional
intervention as user-message text, so content and role are confounded. This
measures the same substrate text in both roles, everything else fixed.

  A  system = substrate, user = question          (as the fleet runs it)
  B  system = empty,     user = substrate + question   (as the conventional
                                                        interventions are run)

If M(A) ~ M(B) the confound is empirically dismissed and the fleet comparison
stands as published. If M(A) >> M(B), placement carries part of the effect and
the fleet needs restructuring so every condition uses the same role.

  python role_control.py --model unsloth/Llama-3.1-8B-Instruct
  python role_control.py --model unsloth/Llama-3.3-70B-Instruct --quantize 4bit
"""
from __future__ import annotations

import argparse
import json

from run_internals import (PROMPTS, answer_ids, forward, load, margin_from_logits,
                           parse_prompt, render)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--quantize", default=None)
    ap.add_argument("--device", default="auto")
    ap.add_argument("--dtype", default=None)
    ap.add_argument("--substrate", default="substrate.txt")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    tok, model = load(args.model, args.quantize, args.device, args.dtype)
    aid = answer_ids(tok)

    base = parse_prompt((PROMPTS / "baseline.txt").read_text())
    sub = parse_prompt((PROMPTS / args.substrate).read_text())
    question, spec = base["user"], sub["system"]

    conditions = {
        "untreated":       {"system": None, "user": question},
        "A_system_role":   {"system": spec, "user": question},
        "B_user_role":     {"system": None, "user": f"{spec}\n\n{question}"},
    }

    out = {"model": args.model, "substrate_file": args.substrate,
           "substrate_sha256": sub["sha256"], "baseline_sha256": base["sha256"]}
    for name, p in conditions.items():
        _, lg, _ = forward(model, tok, render(tok, p, False), None, want_attn=False)
        m = margin_from_logits(lg, aid)
        top = tok.decode([m["argmax"]])
        out[name] = {"M_sum": m["M_sum"], "p_drive": m["p_drive"],
                     "p_walk": m["p_walk"], "top_token": top}
        print(f"{name:16s} M_sum={m['M_sum']:+.3f}  "
              f"p_drive={m['p_drive']:.3f} p_walk={m['p_walk']:.3f}  "
              f"top={top!r}", flush=True)

    d = out["A_system_role"]["M_sum"] - out["B_user_role"]["M_sum"]
    out["placement_effect"] = d
    print(f"\nplacement effect  M(system) - M(user) = {d:+.3f} nats")

    if args.out:
        with open(args.out, "w") as f:
            json.dump(out, f, indent=1)
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
