#!/usr/bin/env python3
"""Figures + summary for cdim.py output (no GPU).

    python plot_cdim.py results/llama-3.1-8b/bf16 [more dirs ...]

Per dir: cdim_map.png (R and D heat-maps of the primary counterfactual,
Mechanistic_paper.md Fig. 2), cdim_maps_all.png (R of every mapped
counterfactual), cdim_agreement.png (behavioural Delta vs peak internal
effect per line, Fig. 3), cdim_path.png (mediated effect, Fig. 5),
cdim_library.png (library control), cdim_lens_vs_rescue.png (§13) and
cdim_summary.md. Several dirs: cdim_overview.png next to them (Fig. 4).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

# diverging: cool pole, neutral grey midpoint, warm pole (Drive is the warm pole)
DIV = LinearSegmentedColormap.from_list("cdim", ["#2c5aa0", "#9db4d8", "#e6e6e6", "#e8a598", "#b03a2e"])
INK, MUTED = "#222222", "#777777"
plt.rcParams.update({"font.size": 8, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK, "axes.titlesize": 9,
                     "axes.spines.top": False, "axes.spines.right": False})


def mat(d: dict, groups: list[str], n_rows: int) -> np.ndarray:
    m = np.full((len(groups), n_rows), np.nan)
    for i, g in enumerate(groups):
        for r, v in enumerate(d[g]):
            if v is not None:
                m[i, r] = v
    return m


def heat(ax, m: np.ndarray, groups: list[str], title: str, vmax: float, cbar=True):
    norm = TwoSlopeNorm(vcenter=0.0, vmin=-vmax, vmax=vmax)
    im = ax.imshow(m, aspect="auto", cmap=DIV, norm=norm, interpolation="nearest")
    ax.set_yticks(range(len(groups)))
    ax.set_yticklabels(groups)
    ax.set_xlabel("row (0 = embedding, l+1 = after layer l)")
    ax.set_title(title, loc="left")
    ax.tick_params(length=2)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    if cbar:
        cb = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
        cb.ax.tick_params(length=2)
        cb.set_label("ΔM (nats)")
    return im


def plot_dir(d: Path) -> dict:
    res = json.loads((d / "cdim.json").read_text())
    groups = list(res["groups"])
    n_rows = res["n_layers"] + 1
    cfs, prim = res["counterfactuals"], res["primary"]
    P = cfs[prim]
    R, D = mat(P["R"], groups, n_rows), mat(P["D"], groups, n_rows)
    vmax = max(np.nanmax(np.abs(R)), np.nanmax(np.abs(D)), 1e-6)
    model = res["model"]

    # --- Fig 2: R and D of the primary counterfactual
    fig, axs = plt.subplots(2, 1, figsize=(9, 5.2), constrained_layout=True)
    heat(axs[0], R, groups, f"{model}: forward rescue R  (S state into the {prim} run; Δbeh={P['delta_beh']:+.2f}, "
                            f"M(S)={res['S']['M']:+.2f}, M(C)={P['M']:+.2f})", vmax)
    heat(axs[1], D, groups, f"reverse disruption D  ({prim} state into the S run)", vmax)
    fig.savefig(d / "cdim_map.png", dpi=160)
    plt.close(fig)

    # --- all mapped counterfactuals, R only
    mapped = res["mapped"]
    fig, axs = plt.subplots(len(mapped), 1, figsize=(9, 2.3 * len(mapped)), constrained_layout=True, squeeze=False)
    vm = max(np.nanmax(np.abs(mat(cfs[n]["R"], groups, n_rows))) for n in mapped)
    for ax, n in zip(axs[:, 0], mapped):
        c = cfs[n]
        heat(ax, mat(c["R"], groups, n_rows), groups,
             f"R, {n} (line {c['line']} {c['kind']}, Δbeh={c['delta_beh']:+.2f}): {c['text'][:70]}", vm)
    fig.savefig(d / "cdim_maps_all.png", dpi=140)
    plt.close(fig)

    # --- Fig 3: behavioural Delta vs peak internal effect on the line's own positions
    loo = None
    ij = d / "internals.json"
    if ij.exists():
        r0 = json.loads(ij.read_text())
        loo = {int(k[8:]): r0["prompts"]["substrate"]["final"]["M_sum"] - v
               for k, v in r0.get("ablations", {}).items() if k.startswith("loo_line")}
    rows_ag = []
    for n in mapped:
        c = cfs[n]
        g = f"line{c['line']}"
        Rl = mat(c["R"], [g], n_rows)[0]
        Dl = mat(c["D"], [g], n_rows)[0]
        Ra = mat(c["R"], ["answer_site"], n_rows)[0]
        Rq = mat(c["R"], ["question"], n_rows)[0]
        # peak rescue on the line's own positions after the embedding row
        rows_ag.append({"cf": n, "line": c["line"], "delta": c["delta_beh"],
                        "peak_R_line": float(np.nanmax(Rl[1:])) if c["delta_beh"] >= 0 else float(np.nanmin(Rl[1:])),
                        "peak_D_line": float(np.nanmax(Dl[1:])) if c["delta_beh"] >= 0 else float(np.nanmin(Dl[1:])),
                        "R_line_row": int(np.nanargmax(np.abs(Rl[1:])) + 1),
                        "last_row_R_line_half": _last_row_above(Rl, 0.5 * c["delta_beh"]),
                        "first_row_R_answer_half": _first_row_above(Ra, 0.5 * c["delta_beh"]),
                        "first_row_R_question_half": _first_row_above(Rq, 0.5 * c["delta_beh"]),
                        "loo": loo.get(c["line"]) if loo else None})
    fig, ax = plt.subplots(figsize=(6.5, 3), constrained_layout=True)
    x = np.arange(len(rows_ag))
    w = 0.2
    ax.bar(x - 1.5 * w, [r["delta"] for r in rows_ag], w, color="#444444", label="Δbeh = M(S) − M(C)")
    ax.bar(x - 0.5 * w, [r["peak_R_line"] for r in rows_ag], w, color="#b03a2e", label="peak R on the line (rows ≥ 1)")
    ax.bar(x + 0.5 * w, [r["peak_D_line"] for r in rows_ag], w, color="#2c5aa0", label="peak D on the line (rows ≥ 1)")
    if loo:
        ax.bar(x + 1.5 * w, [r["loo"] if r["loo"] is not None else 0 for r in rows_ag], w,
               color="#9a9a9a", label="leave-one-out deletion (internals.json)")
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([r["cf"] for r in rows_ag])
    ax.set_ylabel("ΔM (nats)")
    ax.set_title(f"{model}: behavioural effect of each line vs its internal intervention effect", loc="left")
    ax.legend(frameon=False, fontsize=7)
    fig.savefig(d / "cdim_agreement.png", dpi=160)
    plt.close(fig)

    # --- Fig 5: path validation
    path = res.get("path")
    if path:
        grid = path["rows"]
        fig, axs = plt.subplots(1, 2, figsize=(9, 3.4), constrained_layout=True)
        vm = max(abs(v) for v in path["total_dM"].values()) or 1e-6
        for ax, g in zip(axs, ("question", "answer_site")):
            m = np.full((len(grid), len(grid)), np.nan)
            for i, rs in enumerate(grid):
                for j, rd in enumerate(grid):
                    v = path["mediated_dM"][g].get(str(rs), {}).get(str(rd))
                    if v is not None:
                        m[i, j] = v
            im = ax.imshow(m, cmap=DIV, norm=TwoSlopeNorm(0, -vm, vm), interpolation="nearest", aspect="auto")
            ax.set_xticks(range(len(grid)))
            ax.set_xticklabels(grid, fontsize=6)
            ax.set_yticks(range(len(grid)))
            ax.set_yticklabels([f"{r} ({path['total_dM'][str(r)]:+.2f})" for r in grid], fontsize=6)
            ax.set_xlabel(f"receiver row (state of '{g}' inserted alone into the C run)")
            ax.set_ylabel(f"source row of {path['source']} (total rescue)")
            ax.set_title(f"{path['source']} → {g}: mediated ΔM", loc="left")
        cb = plt.colorbar(im, ax=axs, fraction=0.02, pad=0.02)
        cb.set_label("ΔM (nats)")
        fig.savefig(d / "cdim_path.png", dpi=160)
        plt.close(fig)

    # --- library control
    lib = res.get("library")
    if lib:
        gl = list(lib["groups"])
        Rl_, Dl_ = mat(lib["R"], gl, n_rows), mat(lib["D"], gl, n_rows)
        fig, axs = plt.subplots(2, 1, figsize=(9, 5.2), constrained_layout=True)
        heat(axs[0], Rl_, gl, f"library question, R  (M(S)={lib['M_S']:+.2f}, M(C)={lib['M_C']:+.2f}; "
                               f"max patched M={lib['max_patched_M']:+.2f} → {'stays Walk' if lib['stays_walk'] else 'GOES DRIVE'})", vmax)
        heat(axs[1], Dl_, gl, "library question, D", vmax)
        fig.savefig(d / "cdim_library.png", dpi=140)
        plt.close(fig)

    # --- lens vs rescue at the answer site
    lens = res["lens_answer_site"]
    fig, ax = plt.subplots(figsize=(6.5, 2.8), constrained_layout=True)
    rr = np.arange(n_rows)
    ax.plot(rr, lens["S"], color="#b03a2e", lw=1.6, label="logit lens M, S run")
    if prim in lens:
        ax.plot(rr, lens[prim], color="#2c5aa0", lw=1.6, label=f"logit lens M, {prim} run")
        ax.plot(rr, np.array(lens[prim]) * 0 + P["M"] + mat(P["R"], ["answer_site"], n_rows)[0], color="#444444",
                lw=1.6, ls="--", label="M(C | answer-site state ← S), i.e. M(C)+R")
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_xlabel("row")
    ax.set_ylabel("M (nats)")
    ax.set_title(f"{model}: direct readout vs causal sufficiency at the answer site", loc="left")
    ax.legend(frameon=False, fontsize=7)
    fig.savefig(d / "cdim_lens_vs_rescue.png", dpi=160)
    plt.close(fig)

    # --- summary
    ctrl = res.get("controls") or {}
    L = []
    L.append(f"# CDIM — {model} ({res['substrate_file']})\n")
    L.append(f"M(S) = {res['S']['M']:+.3f} (greedy {res['S']['greedy']!r}); {res['n_layers']} layers, "
             f"{res['n_tokens']} tokens; rows = embedding + each layer output; {res['seconds']} s.\n")
    L.append("## Counterfactuals (token-aligned, one line replaced)\n")
    L.append("| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |")
    L.append("|---|---|---|---|---|---|---|---|")
    for n, c in cfs.items():
        L.append(f"| {n} | {c['line']} | {c['kind']} | {c['aligned']} | "
                 f"{c['M']:+.2f} | {c['delta_beh']:+.2f} | {c.get('greedy')!r} | {c['text']} |"
                 if c["aligned"] else f"| {n} | {c['line']} | {c['kind']} | no | – | – | – | {c['text']} |")
    L.append("")
    L.append("## Where the line's effect sits (rows ≥ 1, i.e. inside the network)\n")
    L.append("| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | "
             "first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in rows_ag:
        loo_s = "" if r["loo"] is None else f"{r['loo']:+.2f}"
        L.append(f"| {r['cf']} | {r['delta']:+.2f} | {r['peak_R_line']:+.2f} ({r['R_line_row']}) | {r['peak_D_line']:+.2f} | "
                 f"{r['last_row_R_line_half']} | {r['first_row_R_question_half']} | {r['first_row_R_answer_half']} | {loo_s} |")
    L.append("")
    L.append(f"## Primary counterfactual {prim}: R and D by group (max over rows ≥ 1, and the row)\n")
    L.append("| group | max R (row) | min R (row) | max D (row) | min D (row) |")
    L.append("|---|---|---|---|---|")
    for i, g in enumerate(groups):
        r_, d_ = R[i, 1:], D[i, 1:]
        L.append(f"| {g} | {np.nanmax(r_):+.2f} ({np.nanargmax(r_) + 1}) | {np.nanmin(r_):+.2f} ({np.nanargmin(r_) + 1}) | "
                 f"{np.nanmax(d_):+.2f} ({np.nanargmax(d_) + 1}) | {np.nanmin(d_):+.2f} ({np.nanargmin(d_) + 1}) |")
    L.append("")
    L.append("## Controls\n")
    if ctrl:
        L.append(f"- same-run patch S→S: max |ΔM| = {ctrl['same_run_S']['max_abs']:.4f} nats")
        L.append(f"- random direction of the same norm as S−C in the {ctrl['random_direction']['counterfactual']} run: "
                 f"max |ΔM| = {ctrl['random_direction']['max_abs']:.3f} nats (vs Δbeh {P['delta_beh']:+.2f})")
    if lib:
        L.append(f"- library question: M(S) = {lib['M_S']:+.2f} ({lib['greedy_S']!r}), M(C) = {lib['M_C']:+.2f} "
                 f"({lib['greedy_C']!r}); the largest M reached by any single patch = {lib['max_patched_M']:+.2f} → "
                 f"**{'stays Walk' if lib['stays_walk'] else 'GOES DRIVE'}**")
    if path:
        L.append("")
        L.append(f"## Path validation: {path['source']} → question / answer site (rows {path['rows'][0]}…{path['rows'][-1]})\n")
        L.append("Fraction of the source rescue that survives when only the receiver state is transplanted "
                 "(receiver row = the first grid row after the source, and the last grid row):")
        L.append("")
        L.append("| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |")
        L.append("|---|---|---|---|---|---|")
        g = path["rows"]
        for i, rs in enumerate(g[:-1]):
            tot = path["total_dM"][str(rs)]
            nxt, last = g[i + 1], g[-1]
            def frac(gr, rd):
                v = path["mediated_dM"][gr].get(str(rs), {}).get(str(rd))
                return "–" if v is None else (f"{v:+.2f} ({v / tot:.0%})" if abs(tot) > 0.05 else f"{v:+.2f}")
            L.append(f"| {rs} | {tot:+.2f} | {frac('question', nxt)} | {frac('question', last)} | "
                     f"{frac('answer_site', nxt)} | {frac('answer_site', last)} |")
    L.append("")
    L.append("Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), "
             "cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.")
    (d / "cdim_summary.md").write_text("\n".join(L) + "\n")
    return {"dir": d, "model": model, "groups": groups, "n_rows": n_rows, "R": R, "D": D,
            "prim": prim, "delta": P["delta_beh"], "vmax": vmax}


def _first_row_above(v: np.ndarray, thr: float):
    if thr == 0:
        return None
    ok = np.where((v >= thr) if thr > 0 else (v <= thr))[0]
    return int(ok[0]) if len(ok) else None


def _last_row_above(v: np.ndarray, thr: float):
    if thr == 0:
        return None
    ok = np.where((v >= thr) if thr > 0 else (v <= thr))[0]
    return int(ok[-1]) if len(ok) else None


def main(dirs: list[str]):
    outs = [plot_dir(Path(d)) for d in dirs]
    for o in outs:
        print(f"{o['model']:28s} {o['prim']}  Δ={o['delta']:+.2f}  wrote {o['dir'] / 'cdim_summary.md'}")
    if len(outs) > 1:
        fig, axs = plt.subplots(len(outs), 2, figsize=(12, 2.6 * len(outs)), constrained_layout=True, squeeze=False)
        for row, o in zip(axs, outs):
            # normalised depth on the x axis so models of different depth line up
            for ax, m, name in zip(row, (o["R"], o["D"]), ("R", "D")):
                norm = TwoSlopeNorm(0, -o["vmax"], o["vmax"])
                ax.imshow(m, aspect="auto", cmap=DIV, norm=norm, interpolation="nearest",
                          extent=(0, 1, len(o["groups"]) - 0.5, -0.5))
                ax.set_yticks(range(len(o["groups"])))
                ax.set_yticklabels(o["groups"], fontsize=6)
                ax.set_xlabel("depth (row / rows)")
                ax.set_title(f"{o['model']}: {name}, {o['prim']} (Δbeh={o['delta']:+.2f}, |max|={o['vmax']:.2f})", loc="left")
                for s in ("top", "right", "left", "bottom"):
                    ax.spines[s].set_visible(False)
        out = Path(dirs[0]).parent.parent / "cdim_overview.png" if len({Path(d).parent.parent for d in dirs}) == 1 \
            else Path("cdim_overview.png")
        fig.savefig(out, dpi=140)
        print("wrote", out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
