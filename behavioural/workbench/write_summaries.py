#!/usr/bin/env python3
"""Regenerate behavioural/summary.md: one table, every arm that was run.

Reads only the .jsonl records. No GPU, no keys.

    python behavioural/workbench/write_summaries.py
"""
import collections
import glob
import json
import pathlib
import re

FOLDERS = ["baseline", "correct", "substrate"]
HOST = {"openai": "OpenAI", "anthropic": "Anthropic", "openrouter": "OpenRouter"}


def act(t):
    t = t or ""
    m = re.match(r'\s*[\*\_"\'\#\-\s]*\b(walk|drive)\w*\b', t, re.I)
    if m:
        return m.group(1).lower()
    ms = re.findall(r"\b(walk|drive)\w*\b", t, re.I)
    return ms[-1].lower() if ms else None


def cell(v):
    """State plus the count, e.g. 'RC 10/10', 'RI 0/10', 'NR 7/10'."""
    d = sum(1 for x in v.values() if x == "drive")
    s = "RC" if d == len(v) else "RI" if d == 0 else "NR"
    return f"{s} {d}/{len(v)}"


rows = collections.defaultdict(dict)
host = {}
# runs/ is organised by host; every record names its own condition
for f in sorted(glob.glob("behavioural/runs/*/*.jsonl")):
    for ln in open(f):
        if not ln.strip():
            continue
        d = json.loads(ln)
        if str(d.get("error")) != "None":
            continue
        cond = str(d.get("condition", "")).lower()
        if cond not in FOLDERS:
            continue
        arm = "local" if d.get("backend") == "local" else "hosted"
        key = (d["model_label"], arm)
        host[key] = ("RunPod (local)" if arm == "local"
                     else HOST.get(d.get("family"), d.get("family") or "?"))
        rows[key].setdefault(cond, {})[d["sample_index"]] = act(d.get("response_text"))

dual = {m for m, a in rows if (m, "local") in rows and (m, "hosted") in rows}

L = ["# Behavioural runs", "",
     "Every arm sampled, read from the `.jsonl` records in `runs/`. "
     "R = 10 single-pass samples per cell, temperature 1.0. "
     "RC = reproducibly correct, RI = reproducibly incorrect, NR = non-reproducible.", "",
     "| Model | Host | Baseline | Control | Substrate |",
     "|---|---|---|---|---|"]
for (m, arm) in sorted(rows):
    name = f"{m} ({arm})" if m in dual else m
    r = rows[(m, arm)]
    L.append(f"| {name} | {host[(m, arm)]} | "
             f"{cell(r['baseline'])} | {cell(r['correct'])} | {cell(r['substrate'])} |")
L.append("")
pathlib.Path("behavioural/summary.md").write_text("\n".join(L))
print(f"wrote behavioural/summary.md — {len(rows)} arms")
