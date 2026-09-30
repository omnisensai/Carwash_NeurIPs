#!/usr/bin/env python3
"""Fleet figure: every condition patched into the baseline run, every model.

One panel per model that has a patch_grid.json, ordered by parameter count. Each
curve is M at the answer position of the BASELINE run with one condition's
residual transplanted after layer l, read at the model's output -- the abscissa
is where the intervention was made, not where the quantity is read.

Two modes, because the reader's question decides the colouring:

  --style grouped   (default) the seven conventional conditions share one
                    recessive grey; substrate red, control blue. Two identity
                    colours, which is what a small-multiple grid can carry:
                    seven distinct hues fail colour-vision separation at this
                    panel size (green/orange dE 3.2 protan, magenta/orange 12.9
                    even with normal vision), and the panels are read for the
                    shape of the envelope, not for which conventional is which.
  --style coloured  one hue per conventional condition. Legible only at large
                    size and not colour-vision safe; kept for inspection.

    python scripts/plot_patch_fleet.py --out patch_fleet.png
    python scripts/plot_patch_fleet.py --style coloured --out patch_fleet_col.png

Reads patch_grid.json only; no GPU.
"""
import argparse, json
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent          # internals/

import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

CONV = [("benchmark_CoT", "chain of thought"),
        ("benchmark_encourage", "encouragement"),
        ("benchmark_expert", "expert role"),
        ("benchmark_hallucination", "anti-hallucination"),
        ("benchmark_nomistakes", "error avoidance"),
        ("benchmark_threat", "threat"),
        ("benchmark_urgency", "objective emphasis")]

# (folder, display name, parameters in billions) -- panel order is by size
FLEET = [("qwen2.5-0.5b", "Qwen2.5-0.5B", 0.5), ("qwen3-0.6b", "Qwen3-0.6B", 0.6),
         ("qwen2.5-1.5b", "Qwen2.5-1.5B", 1.5), ("llama-3.2-3b", "Llama 3.2-3B", 3),
         ("qwen3-4b-2507", "Qwen3-4B-2507", 4), ("qwen2.5-7b", "Qwen2.5-7B", 7),
         ("llama-3.1-8b", "Llama 3.1-8B", 8), ("qwen3-8b", "Qwen3-8B", 8),
         ("qwen2.5-14b", "Qwen2.5-14B", 14), ("qwen3-14b", "Qwen3-14B", 14),
         ("qwen2.5-32b", "Qwen2.5-32B", 32), ("qwen3-32b", "Qwen3-32B", 32),
         ("llama-3.3-70b", "Llama 3.3-70B", 70), ("qwen2.5-72b", "Qwen2.5-72B", 72)]

CONTROL = "#2a78d6"
# The substrate curve is coloured by the model's SAMPLED state under the substrate,
# read from behavioural/runs/ so the figure cannot drift from the table. Reserved
# status hues: good / warning / critical. Red and green are 4.1 dE apart under
# deuteranopia, so the state is also written into each panel title -- the colour
# reinforces it and never carries it alone.
STATE_COLOUR = {"RC": "#0ca30c", "NR": "#fab219", "RI": "#d03b3b"}
GREY_CONV, GREY_BASE, INK = "#9a988f", "#3d3c38", "#2b2a27"
# seven-hue set for --style coloured; documented above as not CVD-safe
HUES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7"]

def sampled_state(label):
    """(state, drive, usable) for one model under the substrate, or None."""
    import json as _json, re as _re
    best = {}
    for f in (HERE.parent / "behavioural/runs").glob("*/*.jsonl"):
        for ln in open(f):
            if not ln.strip():
                continue
            d = _json.loads(ln)
            if d.get("model_label") != label or d.get("condition") != "substrate":
                continue
            if str(d.get("error")) != "None":
                continue
            k = d["sample_index"]
            if k not in best or d["timestamp"] > best[k][0]:
                best[k] = (d["timestamp"], d.get("response_text") or "")
    if not best:
        return None
    acts = []
    for _ts, txt in best.values():
        m = _re.match(r'\s*[\*\_"\'\#\-\s]*\b(walk|drive)\w*\b', txt, _re.I)
        if not m:
            ms = _re.findall(r"\b(walk|drive)\w*\b", txt, _re.I)
            m = None if not ms else ms[-1]
            acts.append(m.lower() if m else None)
        else:
            acts.append(m.group(1).lower())
    drive = sum(1 for a in acts if a == "drive")
    usable = sum(1 for a in acts if a in ("drive", "walk"))
    state = "RC" if usable and drive == usable else ("RI" if usable and drive == 0 else "NR")
    return state, drive, usable


ap = argparse.ArgumentParser()
ap.add_argument("--style", choices=("grouped", "coloured"), default="grouped")
ap.add_argument("--models", default="",
                help="space-separated result folder names; default is every model "
                     "with a grid, in size order")
ap.add_argument("--ncol", type=int, default=4)
ap.add_argument("--dpi", type=int, default=200,
                help="raster output only; PDF is vector and ignores it")
ap.add_argument("--out", default="patch_fleet.png")
args = ap.parse_args()

# Vector output for LaTeX: embed TrueType rather than the Type 3 default, which
# some venues reject at submission.
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42

want = args.models.split()
fleet = [t for t in FLEET if t[0] in want] if want else FLEET
if want:
    fleet.sort(key=lambda t: want.index(t[0]))
have = [t for t in fleet if (HERE / f"results/{t[0]}/bf16/patch_grid.json").exists()]
missing = [t[0] for t in fleet if t not in have]
if missing:
    print("no patch_grid.json for:", ", ".join(missing))

ncol = args.ncol
nrow = -(-len(have) // ncol)
fig, axes = plt.subplots(nrow, ncol, figsize=(4.0 * ncol, 3.0 * nrow),
                         constrained_layout=True)
axes = axes.ravel()

for ax, (mid, title, _b) in zip(axes, have):
    d = json.load(open(HERE / f"results/{mid}/bf16/patch_grid.json"))
    g, n, base = d["grid"], d["n_layers"], d["baseline_M_sum"]
    x = list(range(n))
    ax.axhline(0, color=INK, lw=1.0, zorder=1)
    ax.plot(x, g["baseline"], color=GREY_BASE, lw=1.4, ls=(0, (4, 2)), zorder=3)
    for i, (k, lab) in enumerate(CONV):
        if args.style == "grouped":
            ax.plot(x, g[k], lw=1.0, color=GREY_CONV, alpha=.85, zorder=4)
        else:
            ax.plot(x, g[k], lw=1.1, color=HUES[i], alpha=.95, zorder=4, label=lab)
    if "benchmark_correct" in g:
        ax.plot(x, g["benchmark_correct"], color=CONTROL, lw=1.6,
                ls=(0, (1, 1.6)), zorder=6)
    st = sampled_state(title)
    key = st[0] if st else "RC"
    col = STATE_COLOUR[key]
    ax.plot(x, g["substrate"], color=col, lw=2.6, zorder=9)

    # A crossing only means something when the model is on the wrong side to
    # begin with. Where the baseline margin is already positive there is nothing
    # to reverse, and the first positive layer is layer 0 by default -- marking
    # it would read as a transplant reversal that never happened.
    c = next((l for l, v in enumerate(g["substrate"]) if v > 0), None) if base < 0 else None
    if c is not None:
        ax.plot([c], [g["substrate"][c]], "o", ms=8, color=col,
                mec="white", mew=1.4, zorder=10)
        # below-right normally; above-right when the curve sits near zero and the
        # label would land on the zero rule (Llama 3.2-3B spans half a nat)
        span = max(g["substrate"]) - min(g["substrate"])
        dy = 9 if abs(g["substrate"][c]) < .08 * span else -13
        ax.annotate(f"L{c}/{n}", (c, g["substrate"][c]), textcoords="offset points",
                    xytext=(8, dy), fontsize=9, color=col, weight="bold")
    # The sampled state is written out, not left to the colour: red and green are
    # not separable under deuteranopia.
    tag = f"   substrate {st[1]}/{st[2]} {st[0]}" if st else ""
    ax.set_title(f"{title}   ({n} layers){tag}", fontsize=10.5, color=INK)
    ax.tick_params(labelsize=8, colors=INK)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c9c7bf")
    ax.margins(x=.02)

for ax in axes[len(have):]:
    ax.set_visible(False)
for ax in axes[max(0, len(have) - ncol):len(have)]:
    ax.set_xlabel("layer $l$ of the transplant", fontsize=9, color=INK)
for r in range(nrow):
    axes[r * ncol].set_ylabel("final-output $M$  [nats]", fontsize=9, color=INK)

from matplotlib.lines import Line2D
handles = [Line2D([], [], color=STATE_COLOUR["RC"], lw=2.6,
                  label="SUBSTRATE \u2014 reproducibly correct (10/10)"),
           Line2D([], [], color=STATE_COLOUR["NR"], lw=2.6,
                  label="SUBSTRATE \u2014 non-reproducible"),
           Line2D([], [], color=STATE_COLOUR["RI"], lw=2.6,
                  label="SUBSTRATE \u2014 reproducibly incorrect (0/10)"),
           Line2D([], [], color=CONTROL, lw=1.6, ls=(0, (1, 1.6)),
                  label="control (prompt states the answer)"),
           Line2D([], [], color=GREY_BASE, lw=1.4, ls=(0, (4, 2)),
                  label="baseline, patched with its own residual")]
if args.style == "grouped":
    handles.insert(1, Line2D([], [], color=GREY_CONV, lw=1.0,
                             label="seven conventional conditions"))
else:
    handles[1:1] = [Line2D([], [], color=HUES[i], lw=1.1, label=lab)
                    for i, (_k, lab) in enumerate(CONV)]
# The grid leaves spare slots whenever len(have) is not a multiple of ncol; put
# the key there rather than under the figure, where a multi-row legend lands on
# the bottom panels' tick labels.
spare = axes[len(have):]
if len(spare):
    lax = spare[0]
    lax.set_visible(True); lax.axis("off")
    lax.legend(handles=handles, loc="center left", ncol=1, fontsize=10,
               frameon=False, handlelength=2.4, labelspacing=.9)
else:
    # No spare slot: hang the key below the axes. Anchoring its TOP edge at
    # y=0 keeps it clear of the bottom row's tick labels, which a plain
    # "lower center" lands on; bbox_inches="tight" grows the canvas to fit.
    fig.legend(handles=handles, loc="upper center", ncol=min(4, len(handles)),
               fontsize=9.5, frameon=False, bbox_to_anchor=(.5, -.02))
fig.suptitle("Every condition patched into the baseline run, one panel per model.\n"
             "The donor residual replaces the baseline's after layer $l$; "
             "$M$ is then read at the model's output.",
             fontsize=12.5, color=INK)
fig.savefig(args.out, dpi=args.dpi, bbox_inches="tight", facecolor="white")
print("wrote", args.out)
