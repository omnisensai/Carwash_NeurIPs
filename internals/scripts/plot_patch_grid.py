#!/usr/bin/env python3
"""Figure: layerwise patching trajectories, every condition into the baseline.

One panel per model. Each curve is M at the answer position of the baseline run
with one condition's residual patched in after layer l. The substrate is drawn
heavy, the control dashed, the seven conventional conditions thin and grey, and
the self-patch (baseline into baseline) is the flat reference line.

    python scripts/plot_patch_grid.py results/*/bf16/
    python scripts/plot_patch_grid.py results/*/bf16/ --out ../paper/fig_patch_grid.pdf

Reads patch_grid.json only; it does not need a GPU.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CONVENTIONAL = ["benchmark_CoT", "benchmark_encourage", "benchmark_expert",
                "benchmark_hallucination", "benchmark_nomistakes",
                "benchmark_threat", "benchmark_urgency"]
LABEL = {"benchmark_CoT": "chain of thought", "benchmark_encourage": "encouragement",
         "benchmark_expert": "expert role", "benchmark_hallucination": "anti-hallucination",
         "benchmark_nomistakes": "error avoidance", "benchmark_threat": "threat",
         "benchmark_urgency": "objective emphasis", "benchmark_correct": "control",
         "substrate": "substrate", "baseline": "baseline (self-patch)"}


def panel(ax, d, title):
    n = d["n_layers"]
    x = [l / n for l in range(n)]
    g = d["grid"]
    ax.axhline(0, color="0.55", lw=0.8, zorder=1)
    if "baseline" in g:
        ax.plot(x, g["baseline"], color="0.35", lw=1.0, ls=(0, (1, 2)), zorder=2)
    for c in CONVENTIONAL:
        if c in g:
            ax.plot(x, g[c], color="0.62", lw=0.9, zorder=3)
    if "benchmark_correct" in g:
        ax.plot(x, g["benchmark_correct"], color="#1f77b4", lw=1.6, ls="--", zorder=4)
    if "substrate" in g:
        ax.plot(x, g["substrate"], color="#d62728", lw=2.2, zorder=5)
        cross = next((l for l, v in enumerate(g["substrate"]) if v > 0), None)
        if cross is not None:
            ax.plot([cross / n], [g["substrate"][cross]], "o", ms=5,
                    color="#d62728", zorder=6)
            ax.annotate(f"L{cross}", (cross / n, g["substrate"][cross]),
                        textcoords="offset points", xytext=(4, -10), fontsize=7,
                        color="#d62728")
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("fraction of depth", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.margins(x=0.02)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dirs", nargs="+", help="results/<model>/bf16/ folders")
    ap.add_argument("--out", default=None, help="output file (default: patch_grid.png per folder)")
    ap.add_argument("--cols", type=int, default=3)
    args = ap.parse_args()

    runs = []
    for p in args.dirs:
        f = Path(p) / "patch_grid.json"
        if not f.exists():
            print(f"skip {p}: no patch_grid.json")
            continue
        d = json.loads(f.read_text())
        runs.append((Path(p).parts[-2] if len(Path(p).parts) > 1 else str(p), d, Path(p)))
    if not runs:
        raise SystemExit("no patch_grid.json found")

    if args.out is None:
        for name, d, p in runs:
            fig, ax = plt.subplots(figsize=(4.2, 3.0), constrained_layout=True)
            panel(ax, d, name)
            ax.set_ylabel("M (nats)", fontsize=8)
            fig.savefig(p / "patch_grid.png", dpi=180)
            plt.close(fig)
            print("wrote", p / "patch_grid.png")
        return

    cols = min(args.cols, len(runs))
    rows = -(-len(runs) // cols)
    fig, axes = plt.subplots(rows, cols, figsize=(3.4 * cols, 2.5 * rows),
                             constrained_layout=True, squeeze=False)
    for ax in axes.flat[len(runs):]:
        ax.axis("off")
    for ax, (name, d, _) in zip(axes.flat, runs):
        panel(ax, d, name)
    for r in range(rows):
        axes[r][0].set_ylabel("M (nats)", fontsize=8)
    handles = [
        plt.Line2D([], [], color="#d62728", lw=2.2, label="substrate"),
        plt.Line2D([], [], color="#1f77b4", lw=1.6, ls="--", label="control (answer stated)"),
        plt.Line2D([], [], color="0.62", lw=0.9, label="seven conventional conditions"),
        plt.Line2D([], [], color="0.35", lw=1.0, ls=(0, (1, 2)), label="baseline (self-patch)"),
    ]
    fig.legend(handles=handles, loc="outside lower center", ncol=4, fontsize=8, frameon=False)
    fig.savefig(args.out, dpi=200, bbox_inches="tight")
    print("wrote", args.out)


if __name__ == "__main__":
    main()
