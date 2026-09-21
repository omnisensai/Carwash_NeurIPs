#!/usr/bin/env python3
"""Render the cdim_sweep prompt grid (no model needed).

Inputs (this folder): scenarios.json, paraphrases.json, ladder.json + ladder/L*.txt,
ladder_counterfactuals.json. Nothing under prompts/ is touched; L0 is read from
there and used as is.

    python build_prompts.py            # writes generated/ (see below) and prints the grid size
    python build_prompts.py --list     # print every cell id

generated/
  substrates/<scenario>/<level>.txt        the substrate system prompt, level filled for that scenario (L0, L1, S, pro identical for all)
  substrates/<scenario>/counterfactuals.json   {"<level>.txt": [...]} for cdim.py --counterfactuals
  questions/<scenario>_<P>_<T>.txt          user message (body + blank line + tail), format of prompts/baseline.txt

Also importable: load(), substrate_text(level, scenario), question_text(scenario, body, tail),
counterfactuals(level, scenario).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMPTS = HERE.parent.parent / "prompts"
GEN = HERE / "generated"


def _strip_sha(text: str) -> str:
    return "\n".join(ln for ln in text.splitlines() if not ln.lstrip().lower().startswith("sha-256")).rstrip("\n") + "\n"


def load() -> dict:
    sc = json.loads((HERE / "scenarios.json").read_text())["scenarios"]
    par = json.loads((HERE / "paraphrases.json").read_text())
    lad = json.loads((HERE / "ladder.json").read_text())
    cfs = json.loads((HERE / "ladder_counterfactuals.json").read_text())
    plain = json.loads((HERE.parent / "cdim_counterfactuals.json").read_text())   # non-templated, keyed by file basename
    return {"scenarios": {s["id"]: s for s in sc}, "bodies": par["bodies"], "tails": par["tails"],
            "levels": lad["levels"], "order": lad["order"], "class_phrases": lad["class_phrases"],
            "cfs": cfs, "plain_cfs": plain}


def fields(D: dict, scenario: str) -> dict:
    s = dict(D["scenarios"][scenario])
    cls = D["class_phrases"][s["kind"]]
    f = dict(s)
    f["Task3"] = s["task3"][0].upper() + s["task3"][1:]
    # class phrases are themselves templates over the scenario fields
    for k, v in cls.items():
        f[k] = v.format_map(f) if isinstance(v, str) else v
    return f


def substrate_text(D: dict, level: str, scenario: str) -> str:
    """Full 'System:' file text for a level filled for a scenario (as cdim.py reads it)."""
    path = (HERE / D["levels"][level]["file"]).resolve()
    text = _strip_sha(path.read_text())
    if not D["levels"][level].get("templated"):
        return text          # verbatim (L0 embeds the old carwash question; the runners replace it by the cell's question)
    return text.format_map(fields(D, scenario))


def question_text(D: dict, scenario: str, body: str, tail: str) -> str:
    s = D["scenarios"][scenario]
    b = D["bodies"][body].format(task=s["task"], place=s["place"])
    return f"{b}\n\n{D['tails'][tail]}\n"


def counterfactuals(D: dict, level: str, scenario: str) -> list[dict]:
    if not D["levels"][level].get("templated"):
        key = Path(D["levels"][level]["file"]).name
        return [dict(c) for c in D["plain_cfs"][key]]
    f = fields(D, scenario)
    return [{**c, "text": c["text"].format_map(f)} for c in D["cfs"][level]]


def cells(D: dict) -> list[dict]:
    """The behavioural grid: every question (scenario x body x tail) under
    none and every ladder level (L0..L5, S, pro) filled for the question's own
    scenario (grid A), plus every question under the carwash-filled concrete
    levels L2..L5 and S, P0 x T1 only (grid B, selectivity / leak test)."""
    out = []
    for q in D["scenarios"]:
        for b in D["bodies"]:
            for t in D["tails"]:
                for sub in ["none"] + list(D["order"]):
                    out.append({"grid": "A", "q": q, "body": b, "tail": t, "substrate": sub, "fill": q})
    for q in D["scenarios"]:
        for lvl in ("L2", "L3", "L4", "L5", "S"):
            if q != "carwash":
                out.append({"grid": "B", "q": q, "body": "P0", "tail": "T1", "substrate": lvl, "fill": "carwash"})
    return out


def write_generated(D: dict) -> None:
    for sid in D["scenarios"]:
        d = GEN / "substrates" / sid
        d.mkdir(parents=True, exist_ok=True)
        cfj = {}
        for lvl in D["levels"]:
            (d / f"{lvl}.txt").write_text(substrate_text(D, lvl, sid))
            cfj[f"{lvl}.txt"] = counterfactuals(D, lvl, sid)
        (d / "counterfactuals.json").write_text(json.dumps(cfj, indent=1, ensure_ascii=False))
        for b in D["bodies"]:
            for t in D["tails"]:
                qd = GEN / "questions"
                qd.mkdir(parents=True, exist_ok=True)
                (qd / f"{sid}_{b}_{t}.txt").write_text(question_text(D, sid, b, t))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    D = load()
    base = _strip_sha((PROMPTS / "baseline.txt").read_text())
    assert question_text(D, "carwash", "P0", "T1") == base, "carwash P0+T1 must equal prompts/baseline.txt"
    write_generated(D)
    C = cells(D)
    print(f"{len(D['scenarios'])} scenarios x {len(D['bodies'])} bodies x {len(D['tails'])} tails; "
          f"{len(C)} grid cells ({sum(c['grid'] == 'A' for c in C)} A + {sum(c['grid'] == 'B' for c in C)} B); wrote {GEN}/")
    if args.list:
        for c in C:
            print(c["grid"], c["q"], c["body"], c["tail"], c["substrate"], c["fill"])


if __name__ == "__main__":
    main()
