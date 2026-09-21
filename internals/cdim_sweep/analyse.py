#!/usr/bin/env python3
"""Tables + figures for a cdim_sweep result dir (no GPU).

    python analyse.py results/llama-3.3-70b/bf16-sweep [results/qwen3-8b/bf16-sweep ...]

Reads <dir>/grid.json (run_grid.py) and <dir>/{ladder,paraphrase,scenario}/*/cdim.json
(run_cdim_cells.py); each may be missing. Writes <dir>/sweep_summary.md and
sweep_envelope.png, sweep_ladder.png, sweep_stability.png.

Per CDIM cell (primary counterfactual):
  delta            M(S) - M(C)
  handoff_line     last row (fraction of depth) where R on the line's own tokens >= 1/2 delta
  handoff_answer   first row (fraction of depth) where R on the answer site >= 1/2 delta
  q_share          max over source rows with |total rescue| >= 1/2 |delta| and receiver rows > source
                   of mediated(question)/total: the largest fraction of the line's effect that
                   the question span carries on its own (CDIM_RESULTS.md 'share via question span')
  rnd_ctrl         random-direction control max |dM|
  ctrl_walk        the control (walk) question stays Walk under every patch
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean, median, pstdev

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from plot_cdim import _first_row_above, _last_row_above, mat   # noqa: E402
ORDER = json.loads((HERE / "ladder.json").read_text())["order"]

BLUE, RED, INK, MUTED, LIGHT = "#2c5aa0", "#b03a2e", "#222222", "#777777", "#d9d9d9"
plt.rcParams.update({"font.size": 8, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": INK,
                     "ytick.color": INK, "axes.titlesize": 9, "axes.spines.top": False, "axes.spines.right": False})
SUBS = ["none", "L0", "L1", "L2", "L3", "L4", "L5", "S", "pro"]


# ---------------------------------------------------------------- CDIM cells --

def cell_metrics(d: Path) -> dict | None:
    f = d / "cdim.json"
    if not f.exists():
        return None
    r = json.loads(f.read_text())
    P = r["counterfactuals"][r["primary"]]
    n = r["n_layers"] + 1
    delta = P["delta_beh"]
    g = f"line{P['line']}"
    Rl = mat(P["R"], [g], n)[0]
    Ra = mat(P["R"], ["answer_site"], n)[0]
    lo = _last_row_above(Rl, 0.5 * delta)
    fa = _first_row_above(Ra, 0.5 * delta)
    share = None
    if r.get("path"):
        p = r["path"]
        best = 0.0
        for rs, tot in p["total_dM"].items():
            if abs(tot) < 0.5 * abs(delta) or abs(tot) < 0.05:
                continue
            for rd, v in p["mediated_dM"]["question"].get(rs, {}).items():
                if int(rd) > int(rs):
                    best = max(best, v / tot)
        share = best
    ctrl = r.get("controls") or {}
    return {"dir": str(d), "cell": d.name, "exp": d.parent.name, "sweep": r.get("sweep", {}),
            "M_S": r["S"]["M"], "greedy": r["S"]["greedy"], "primary": r["primary"], "line": P["line"],
            "delta": delta, "M_C": P["M"], "flips": (r["S"]["M"] > 0) != (P["M"] > 0),
            "n_layers": r["n_layers"], "handoff_line": None if lo is None else lo / r["n_layers"],
            "handoff_answer": None if fa is None else fa / r["n_layers"],
            "handoff_line_row": lo, "handoff_answer_row": fa, "q_share": share,
            "rnd_ctrl": (ctrl.get("random_direction") or {}).get("max_abs"),
            "ctrl_walk": (r.get("library") or {}).get("stays_walk"),
            "ctrl_M_S": (r.get("library") or {}).get("M_S"), "n_tokens": r["n_tokens"]}


def fmt(v, spec="+.2f"):
    return "–" if v is None else format(v, spec)


# ---------------------------------------------------------------- the grid --

def grid_tables(cells: dict, L: list[str], d: Path):
    A = [c for c in cells.values() if c["grid"] == "A"]
    B = [c for c in cells.values() if c["grid"] == "B"]
    if not A:
        return
    subs = [s for s in SUBS if any(c["substrate"] == s for c in A)]

    L.append("## Behavioural grid A: every question under every substrate\n")
    L.append("Drive tasks = scenarios whose rules imply drive; walk tasks = portable-object controls. "
             "P(drive) = fraction of cells whose argmax is a drive token. Selectivity = P(drive | drive task) − P(drive | walk task).\n")
    L.append("| substrate | drive tasks: mean M | P(drive) | walk tasks: mean M | P(drive) | selectivity | carwash P0+T1: M |")
    L.append("|---|---|---|---|---|---|---|")
    for s in subs:
        dr = [c for c in A if c["substrate"] == s and c["correct"] == "drive"]
        wk = [c for c in A if c["substrate"] == s and c["correct"] == "walk"]
        pd_ = mean(c["answer"] == "drive" for c in dr) if dr else float("nan")
        pw_ = mean(c["answer"] == "drive" for c in wk) if wk else float("nan")
        cw = [c for c in dr if c["q"] == "carwash" and c["body"] == "P0" and c["tail"] == "T1"]
        L.append(f"| {s} | {fmt(mean(c['M'] for c in dr)) if dr else '–'} | {pd_:.2f} | "
                 f"{fmt(mean(c['M'] for c in wk)) if wk else '–'} | {pw_:.2f} | {pd_ - pw_:+.2f} | "
                 f"{fmt(cw[0]['M']) if cw else '–'} |")
    L.append("")

    # envelope over paraphrases, per scenario x substrate
    L.append("## Operating envelope: M over the 12 question bodies × 3 tails\n")
    L.append("| scenario | substrate | min | median | max | sd | P(drive) |")
    L.append("|---|---|---|---|---|---|---|")
    env = defaultdict(list)
    for c in A:
        env[(c["q"], c["substrate"])].append(c)
    for q in sorted({c["q"] for c in A}, key=lambda q: (cells_correct(A, q) != "drive", q)):
        for s in subs:
            cs = env.get((q, s), [])
            if not cs:
                continue
            ms = [c["M"] for c in cs]
            L.append(f"| {q} ({cells_correct(A, q)}) | {s} | {min(ms):+.2f} | {median(ms):+.2f} | {max(ms):+.2f} | "
                     f"{pstdev(ms):.2f} | {mean(c['answer'] == 'drive' for c in cs):.2f} |")
    L.append("")

    # tail effect
    L.append("## Question tail (T0 'one word:', T1 '...: walk or drive', T2 '...: drive or walk'), drive tasks, mean M\n")
    L.append("| substrate | T0 | T1 | T2 | max−min |")
    L.append("|---|---|---|---|---|")
    for s in subs:
        row = []
        for t in ("T0", "T1", "T2"):
            cs = [c["M"] for c in A if c["substrate"] == s and c["tail"] == t and c["correct"] == "drive"]
            row.append(mean(cs) if cs else None)
        vals = [v for v in row if v is not None]
        L.append(f"| {s} | {fmt(row[0])} | {fmt(row[1])} | {fmt(row[2])} | {fmt(max(vals) - min(vals), '.2f') if vals else '–'} |")
    L.append("")

    if B:
        L.append("## Grid B: walk questions under the carwash-filled concrete substrates (leak test)\n")
        L.append("| question | " + " | ".join(s for s in ("L2", "L3", "L4", "L5", "S")) + " |")
        L.append("|---|---|---|---|---|---|")
        for q in sorted({c["q"] for c in B}):
            row = []
            for s in ("L2", "L3", "L4", "L5", "S"):
                cs = [c for c in B if c["q"] == q and c["substrate"] == s]
                row.append(f"{cs[0]['M']:+.2f} {cs[0]['answer']}" if cs else "–")
            L.append(f"| {q} ({cells_correct(cells.values(), q)}) | " + " | ".join(row) + " |")
        L.append("")

    # figure: envelope strips, carwash, one strip per substrate
    fig, ax = plt.subplots(figsize=(7, 3), constrained_layout=True)
    rng = np.random.default_rng(0)
    for i, s in enumerate(subs):
        cs = env.get(("carwash", s), [])
        if not cs:
            continue
        ms = np.array([c["M"] for c in cs])
        ax.scatter(i + rng.uniform(-0.18, 0.18, len(ms)), ms, s=14, color=BLUE, alpha=0.75, edgecolor="white", lw=0.5)
        ax.hlines(np.median(ms), i - 0.3, i + 0.3, color=INK, lw=1.5)
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_xticks(range(len(subs)))
    ax.set_xticklabels(subs)
    ax.set_ylabel("M = log P(drive) − log P(walk)")
    ax.set_title("carwash question: M over 12 bodies × 3 tails per substrate (bar = median)", loc="left")
    fig.savefig(d / "sweep_envelope.png", dpi=160)
    plt.close(fig)


def _same_lines(cell_dir: str, substrate_file) -> bool:
    """Was this cdim.json measured on the bullet lines of that substrate file?"""
    r = json.loads((Path(cell_dir) / "cdim.json").read_text())
    want = [ln for ln in substrate_file.read_text().splitlines() if ln.lstrip().startswith("-")]
    return [ln.strip() for ln in r["substrate_lines"]] == [ln.strip() for ln in want]


def cells_correct(cs, q):
    for c in cs:
        if c["q"] == q:
            return c["correct"]
    return "?"


# ---------------------------------------------------------------- CDIM part --

def cdim_tables(d: Path, L: list[str]):
    exps = {}
    for exp in ("ladder", "paraphrase", "scenario", "scenario-pro"):
        cs = [m for p in sorted((d / exp).glob("*/")) if (m := cell_metrics(p))]
        if cs:
            exps[exp] = cs
    # first-round cells next door (results/<model>/<prec>/ and <prec>-pro/) count as the
    # L0 / pro ladder cells when they were measured on those retired substrates
    for lvl, suffix in (("L0", ""), ("pro", "-pro")):
        m = cell_metrics(d.parent / (d.name.replace("-sweep", "") + suffix))
        if m and _same_lines(m["dir"], HERE / "ladder" / f"{lvl}.txt"):
            m["cell"], m["exp"] = lvl, "ladder"
            exps.setdefault("ladder", []).append(m)
    if "ladder" in exps:
        exps["ladder"].sort(key=lambda m: ORDER.index(m["cell"]) if m["cell"] in ORDER else 99)
    if not exps:
        return
    hdr = ("| cell | M(S) | greedy | primary line | Δ | flips | line carries ≥½Δ until (row / depth) | "
           "answer site from (row / depth) | share via question | random ctrl | control stays walk |")
    sep = "|---|---|---|---|---|---|---|---|---|---|---|"
    for exp, cs in exps.items():
        L.append(f"## CDIM: {exp}\n")
        L.append(hdr)
        L.append(sep)
        for m in cs:
            L.append(f"| {m['cell']} | {m['M_S']:+.2f} | {m['greedy']!r} | {m['primary']} (line {m['line']}) | {m['delta']:+.2f} | "
                     f"{'yes' if m['flips'] else 'no'} | {fmt(m['handoff_line_row'], 'd')} / {fmt(m['handoff_line'], '.2f')} | "
                     f"{fmt(m['handoff_answer_row'], 'd')} / {fmt(m['handoff_answer'], '.2f')} | {fmt(m['q_share'], '.0%')} | "
                     f"{fmt(m['rnd_ctrl'], '.2f')} | {m['ctrl_walk']} |")
        L.append("")

    # figure: ladder dose-response
    if "ladder" in exps:
        cs = exps["ladder"]
        fig, axs = plt.subplots(1, 3, figsize=(9.5, 2.8), constrained_layout=True)
        x = np.arange(len(cs))
        lab = [m["cell"] for m in cs]
        axs[0].bar(x, [m["delta"] for m in cs], 0.55, color=INK)
        axs[0].set_title("behavioural effect Δ of the primary line", loc="left")
        axs[0].set_ylabel("nats")
        axs[1].plot(x, [m["q_share"] if m["q_share"] is not None else np.nan for m in cs], "o-", color=RED, lw=2, ms=6)
        axs[1].set_ylim(0, 1)
        axs[1].set_title("share carried by the question span", loc="left")
        axs[2].plot(x, [m["handoff_line"] if m["handoff_line"] is not None else np.nan for m in cs], "o-", color=BLUE, lw=2, ms=6, label="line's own tokens carry ≥½Δ until")
        axs[2].plot(x, [m["handoff_answer"] if m["handoff_answer"] is not None else np.nan for m in cs], "s-", color=RED, lw=2, ms=6, label="answer site carries ≥½Δ from")
        axs[2].set_ylim(0, 1)
        axs[2].set_ylabel("fraction of depth")
        axs[2].set_title("hand-off depth", loc="left")
        axs[2].legend(frameon=False, fontsize=7)
        for ax in axs:
            ax.set_xticks(x)
            ax.set_xticklabels(lab)
            ax.set_xlim(-0.6, len(cs) - 0.4)
            ax.set_xlabel("explicitness level")
        fig.savefig(d / "sweep_ladder.png", dpi=160)
        plt.close(fig)

    # figure: stability across paraphrases / scenarios (route metrics vs the margin)
    pts = [(exp, m) for exp in ("paraphrase", "scenario") for m in exps.get(exp, [])]
    if pts:
        fig, axs = plt.subplots(1, 2, figsize=(7.5, 3), constrained_layout=True)
        for exp, mk, col in (("paraphrase", "o", BLUE), ("scenario", "s", RED)):
            ms = [m for e, m in pts if e == exp]
            if not ms:
                continue
            axs[0].scatter([m["M_S"] for m in ms], [m["handoff_answer"] for m in ms], marker=mk, color=col, s=28, label=exp, edgecolor="white", lw=0.5)
            axs[1].scatter([m["M_S"] for m in ms], [m["q_share"] for m in ms], marker=mk, color=col, s=28, label=exp, edgecolor="white", lw=0.5)
        axs[0].set_ylabel("answer site carries ≥½Δ from (fraction of depth)")
        axs[1].set_ylabel("share via question span")
        for ax in axs:
            ax.set_xlabel("M(S) of the cell")
            ax.set_ylim(0, 1)
            ax.legend(frameon=False, fontsize=7)
        axs[0].set_title("does the hand-off depth move with the margin?", loc="left")
        axs[1].set_title("does the route move with the margin?", loc="left")
        fig.savefig(d / "sweep_stability.png", dpi=160)
        plt.close(fig)


def main(dirs):
    for ds in dirs:
        d = Path(ds)
        L = [f"# cdim_sweep — {d}\n"]
        gf = d / "grid.json"
        if gf.exists():
            g = json.loads(gf.read_text())
            L[0] = f"# cdim_sweep — {g.get('model', d)}\n"
            L.append(f"grid.json: {len(g['cells'])} cells, {g.get('seconds', '?')} s\n")
            grid_tables(g["cells"], L, d)
        cdim_tables(d, L)
        (d / "sweep_summary.md").write_text("\n".join(L) + "\n")
        print(f"wrote {d / 'sweep_summary.md'}")


if __name__ == "__main__":
    main(sys.argv[1:])
