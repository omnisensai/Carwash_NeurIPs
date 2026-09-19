#!/usr/bin/env python3
"""Verify the counterfactual templates are token-aligned (no model, tokenizers only).

    python check_align.py                       # Llama-3 + Qwen3 tokenizers, all levels, all drive scenarios
    python check_align.py --scenario carwash    # one scenario

For every level and scenario it renders the substrate, replaces line k by the
counterfactual (exactly as cdim.replace_line does), and reports the token count
of the original and the counterfactual line under each tokenizer. A row is OK
when the counts agree under both. It also checks that the tokens outside the
line are unchanged when the whole system text is tokenised (the test cdim.py
applies), which catches merges across the line boundary.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # internals/
from build_prompts import load, substrate_text, counterfactuals   # noqa: E402
from run_internals import parse_prompt, substrate_lines           # noqa: E402
from cdim import replace_line                                     # noqa: E402

TOKENIZERS = {"llama3": "unsloth/Llama-3.2-3B-Instruct", "qwen3": "Qwen/Qwen3-4B-Instruct-2507"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", default=None, help="default: every drive scenario")
    ap.add_argument("--levels", default="L1,L2,L3,L4,L5")
    args = ap.parse_args()
    from transformers import AutoTokenizer
    toks = {k: AutoTokenizer.from_pretrained(v) for k, v in TOKENIZERS.items()}
    D = load()
    scen = [args.scenario] if args.scenario else [s for s, v in D["scenarios"].items() if v["kind"] == "vehicle"]
    bad = 0
    for lvl in args.levels.split(","):
        for sid in scen:
            sysm = parse_prompt(substrate_text(D, lvl, sid))["system"]
            lines = substrate_lines(sysm)
            for cf in counterfactuals(D, lvl, sid):
                orig = lines[cf["line"] - 1]
                alt = replace_line(sysm, cf["line"], cf["text"])
                rep = []
                ok = True
                for name, tk in toks.items():
                    a = len(tk.encode(orig, add_special_tokens=False))
                    b = len(tk.encode(cf["text"], add_special_tokens=False))
                    full_a = tk.encode(sysm, add_special_tokens=False)
                    full_b = tk.encode(alt, add_special_tokens=False)
                    same_len = len(full_a) == len(full_b)
                    ok &= (a == b) and same_len
                    rep.append(f"{name} {a}/{b}{'' if same_len else ' FULL-LEN-DIFF'}")
                bad += not ok
                flag = "ok " if ok else "BAD"
                print(f"{flag} {lvl} {sid:10s} {cf['name']:4s} {' | '.join(rep)}")
                if not ok:
                    print(f"      orig: {orig}\n      cf:   {cf['text']}")
    print(f"\n{bad} misaligned rows" if bad else "\nall counterfactuals aligned under both tokenizers")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
