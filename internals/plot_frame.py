#!/usr/bin/env python3
"""Figures for brainscope_frame.py output (no GPU): python plot_frame.py results/<model>/bf16-frame [...]"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BLUE, RED, INK, MUTED = "#2c5aa0", "#b03a2e", "#222222", "#777777"
plt.rcParams.update({"font.size": 8, "axes.edgecolor": MUTED, "axes.spines.top": False, "axes.spines.right": False})


def plot(d: Path):
    r = json.loads((d / "frame.json").read_text())
    C = r["conditions"]
    L = r["n_layers"]
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.4), constrained_layout=True)
    axs[0].plot(range(L), r["separation_dprime"], color=INK, lw=1.8)
    axs[0].axvline(r["best_layer"], color=MUTED, lw=0.8, ls="--")
    axs[0].set_title(f"where the drive frame separates (d' per layer, {r['n_pairs']} pairs)", loc="left")
    axs[0].set_xlabel("layer"); axs[0].set_ylabel("d'")
    for name, c in C.items():
        col = RED if c["answer"] == "drive" else BLUE
        lw = 2.2 if name in ("baseline", "substrate") else 1.0
        axs[1].plot(range(L), c["proj_answer_site"], color=col, lw=lw, alpha=0.9 if lw > 1 else 0.6)
        axs[2].plot(range(L + 1), c["lens_M"], color=col, lw=lw, alpha=0.9 if lw > 1 else 0.6)
        if name in ("baseline", "substrate"):
            axs[1].annotate(name, (L - 1, c["proj_answer_site"][-1]), fontsize=7, color=col, ha="right", va="bottom")
    axs[1].axhline(0, color=MUTED, lw=0.8)
    axs[1].set_title("frame projection at the answer site (red = answers drive, blue = walk)", loc="left")
    axs[1].set_xlabel("layer"); axs[1].set_ylabel("h · d̂")
    axs[2].axhline(0, color=MUTED, lw=0.8)
    axs[2].set_title("logit-lens M at the answer site", loc="left")
    axs[2].set_xlabel("row (0 = embedding)"); axs[2].set_ylabel("M (nats)")
    fig.suptitle(r["model"], x=0.01, ha="left", fontsize=9)
    fig.savefig(d / "frame.png", dpi=160)
    plt.close(fig)

    # token map: baseline vs substrate
    fig, axs = plt.subplots(2, 1, figsize=(11, 5), constrained_layout=True)
    vm = max(np.abs(np.array(C[n]["proj_map"])).max() for n in ("baseline", "substrate") if n in C) or 1
    for ax, n in zip(axs, ("baseline", "substrate")):
        if n not in C:
            continue
        m = np.array(C[n]["proj_map"])
        ax.imshow(m, aspect="auto", cmap="RdBu_r", vmin=-vm, vmax=vm, interpolation="nearest")
        toks = C[n]["tokens"]
        step = max(1, len(toks) // 40)
        ax.set_xticks(range(0, len(toks), step)); ax.set_xticklabels([toks[i].replace("\n", "⏎") for i in range(0, len(toks), step)], rotation=90, fontsize=5)
        ax.set_ylabel("layer"); ax.set_title(f"{n}: frame projection per token and layer (M={C[n]['M']:+.2f})", loc="left")
    fig.savefig(d / "frame_tokens.png", dpi=150)
    plt.close(fig)

    rows = ["| condition | system | M | answer | formation layer | decisive layer (lens) | proj@answer final |", "|---|---|---|---|---|---|---|"]
    for n, c in C.items():
        rows.append(f"| {n} | {'yes' if c['system'] else 'no'} | {c['M']:+.2f} | {c['answer']} | {c['formation_layer']} | {c['decisive_layer']} | {c['proj_answer_site'][-1]:+.2f} |")
    (d / "frame_summary.md").write_text(f"# drive-frame direction — {r['model']}\n\nframe separates best at layer {r['best_layer']} "
                                        f"(d' = {r['separation_dprime'][r['best_layer']]:.2f}, AUC {r['auc'][r['best_layer']]:.2f}); "
                                        f"{r['n_pairs']} contrast pairs; directions via {r['directions_via']}.\n\n" + "\n".join(rows) + "\n")
    print(f"wrote {d}/frame.png, frame_tokens.png, frame_summary.md")


if __name__ == "__main__":
    for a in sys.argv[1:]:
        plot(Path(a))
