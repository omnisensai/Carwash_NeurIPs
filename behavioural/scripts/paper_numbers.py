#!/usr/bin/env python3
"""Every population-dependent number the paper cites, computed from the runs.

The paper states roughly two dozen counts that all move together when a model
is added or an arm changes. This prints them in one place so the paper can be
diffed against the data instead of audited by hand.

    python behavioural/scripts/paper_numbers.py
"""
import collections
import glob
import json
import re

COND = ["baseline", "cot", "encourage", "expert", "hallucination",
        "nomistakes", "threat", "urgency", "correct", "substrate"]
CONVENTIONAL = ["expert", "urgency", "cot", "hallucination", "threat",
                "encourage", "nomistakes"]
LABEL = {"baseline": "baseline", "expert": "expert role",
         "urgency": "objective emphasis", "cot": "chain of thought",
         "hallucination": "anti-hallucination", "encourage": "encouragement",
         "nomistakes": "error avoidance", "threat": "threat",
         "correct": "control", "substrate": "SUBSTRATE"}
LOCALF = set(glob.glob("behavioural/runs/local/*.jsonl"))


def act(t):
    t = t or ""
    m = re.match(r'\s*[\*\_"\'\#\-\s]*\b(walk|drive)\w*\b', t, re.I)
    if m:
        return m.group(1).lower()
    ms = re.findall(r"\b(walk|drive)\w*\b", t, re.I)
    return ms[-1].lower() if ms else None


cells, host = {}, {}
for f in sorted(glob.glob("behavioural/runs/*/*.jsonl")):
    folder = f.split("/")[2]
    for ln in open(f):
        if not ln.strip():
            continue
        d = json.loads(ln)
        if str(d.get("error")) != "None":
            continue
        c = str(d.get("condition", "")).lower() if f in LOCALF else folder.lower()
        if c not in COND:
            continue
        k = (d["model_label"], c, d["sample_index"])
        if k not in cells or d["timestamp"] > cells[k][1]:
            cells[k] = (act(d.get("response_text")), d["timestamp"])
        host[d["model_label"]] = "local" if d.get("backend") == "local" else "hosted"

MODELS = sorted({m for m, _, _ in cells})


def counts(m, c):
    v = [a for (mm, cc, _), (a, _) in cells.items() if (mm, cc) == (m, c)]
    return sum(1 for x in v if x == "drive"), len(v)


def state(m, c):
    d, n = counts(m, c)
    return "RC" if d == n else "RI" if d == 0 else "NR"


POP = [m for m in MODELS if state(m, "baseline") != "RC"]
EXCL = [m for m in MODELS if m not in POP]
R = 10
N = len(POP)

print(f"MEASURED         {len(MODELS)} models")
print(f"EXCLUDED         {len(EXCL)} ({', '.join(EXCL)}) -- reproducibly correct at baseline")
print(f"POPULATION       {N} models"
      f"  ({sum(1 for m in POP if host[m]=='hosted')} hosted,"
      f" {sum(1 for m in POP if host[m]=='local')} local)")
print(f"EXECUTIONS       R={R}, {N*R} per condition, {N*R*len(COND)} in total\n")

b = collections.Counter(state(m, "baseline") for m in POP)
print(f"BASELINE         RI {b['RI']}, NR {b['NR']}, "
      f"{sum(counts(m,'baseline')[0] for m in POP)}/{N*R} executions name the intended action\n")

print("TABLE 2 — operational state per condition (rows sum to the population)")
print(f"  {'condition':22s}{'RC':>4}{'NR':>4}{'RI':>4}{'intended':>12}{'RI@base->RC':>13}")
baseRI = [m for m in POP if state(m, "baseline") == "RI"]
for c in COND:
    t = collections.Counter(state(m, c) for m in POP)
    tot = sum(counts(m, c)[0] for m in POP)
    conv = sum(1 for m in baseRI if state(m, c) == "RC")
    print(f"  {LABEL[c]:22s}{t['RC']:>4}{t['NR']:>4}{t['RI']:>4}{tot:>8}/{N*R}{conv:>9} of {len(baseRI)}")

print("\nCONVENTIONAL CONDITIONS")
conv_rc = {c: sorted(m for m in baseRI if state(m, c) == "RC") for c in CONVENTIONAL}
allconv = sorted({m for v in conv_rc.values() for m in v})
print(f"  best RC count over the seven: {max(collections.Counter(state(m,c) for m in POP)['RC'] for c in CONVENTIONAL)}")
print(f"  models converted RI->RC by any conventional condition: {len(allconv)} ({', '.join(allconv) or 'none'})")
for c in CONVENTIONAL:
    if conv_rc[c]:
        print(f"    {LABEL[c]:22s} converts {', '.join(conv_rc[c])}")

print("\nSUBSTRATE")
s = collections.Counter(state(m, "substrate") for m in POP)
print(f"  RC {s['RC']}, NR {s['NR']}, RI {s['RI']}"
      f"; {sum(counts(m,'substrate')[0] for m in POP)}/{N*R} executions name the intended action")
print(f"  RI at baseline -> RC: {sum(1 for m in baseRI if state(m,'substrate')=='RC')} of {len(baseRI)}")
baseNR = [m for m in POP if state(m, "baseline") == "NR"]
print(f"  NR at baseline -> RC: {sum(1 for m in baseNR if state(m,'substrate')=='RC')} of {len(baseNR)}")
print(f"  left reproducibly incorrect: "
      f"{', '.join(m for m in POP if state(m,'substrate')=='RI') or 'none'}")

print("\nCONTROL (answer stated in the prompt)")
k = collections.Counter(state(m, "correct") for m in POP)
print(f"  RC {k['RC']}, NR {k['NR']}, RI {k['RI']}"
      f"; {sum(counts(m,'correct')[0] for m in POP)}/{N*R} executions name the intended action")
print(f"  still RI while the prompt states the answer: "
      f"{', '.join(m for m in POP if state(m,'correct')=='RI')}")
both = [m for m in POP if state(m, "correct") == "RC" and state(m, "substrate") == "RC"]
conly = [m for m in POP if state(m, "correct") == "RC" and state(m, "substrate") != "RC"]
sonly = [m for m in POP if state(m, "substrate") == "RC" and state(m, "correct") != "RC"]
neither = [m for m in POP if state(m, "correct") != "RC" and state(m, "substrate") != "RC"]
print(f"  RC under both {len(both)}, control only {len(conly)}, substrate only {len(sonly)},"
      f" neither {len(neither)} ({', '.join(neither) or '-'}); union {N-len(neither)} of {N}")

print("\nINTERNALS (models with a local run in internals/results/)")
import os
have = sorted(d for d in os.listdir("internals/results")
              if os.path.exists(f"internals/results/{d}/bf16/internals.json"))
grid = [d for d in have if os.path.exists(f"internals/results/{d}/bf16/patch_grid.json")]
print(f"  internals.json: {len(have)}  |  patch_grid.json: {len(grid)}")
