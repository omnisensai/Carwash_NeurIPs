#!/usr/bin/env python3
"""Figures + a markdown summary from results/<name>/internals.json.
Needs only numpy + matplotlib (no GPU, no torch).

    python plot_internals.py results/llama-3.2-3b [results/llama-3.1-8b-4bit ...]

Per result dir: lens.png, dla.png, heads.png, attention.png, ablations.png,
benchmarks.png, diff.png, summary.md. With several dirs also a cross-model
overview.png next to them.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C_BASE, C_SUB, C_PATCH = "#6b7280", "#d97706", "#2563eb"


def load(d: Path) -> dict:
    return json.loads((d / "internals.json").read_text())


def layer_axis(n):            # rows: emb, layer0..layer(n-1)
    return np.arange(-1, n)


def fig_lens(r: dict, d: Path):
    n = r["n_layers"]
    x = layer_axis(n)
    b, s = r["prompts"]["baseline"]["lens"], r["prompts"]["substrate"]["lens"]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.axhline(0, color="k", lw=0.6)
    ax.plot(x, b["M_sum"], "-o", ms=3, color=C_BASE, label="baseline (logit lens)")
    ax.plot(x, s["M_sum"], "-o", ms=3, color=C_SUB, label="substrate (logit lens)")
    if "patching" in r:
        ax.plot(np.arange(n), r["patching"]["M_sum"], "--s", ms=3, color=C_PATCH,
                label="baseline + substrate residual patched at layer (final M)")
    ax.set_xlabel("layer (-1 = embedding)")
    ax.set_ylabel("M = log P(drive) − log P(walk)  [nats]")
    ax.set_title(f"{r['model']}: where the decision forms")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(d / "lens.png", dpi=150)
    plt.close(fig)


def fig_dla(r: dict, d: Path):
    n = r["n_layers"]
    x = np.arange(n)
    b, s = r["prompts"]["baseline"]["dla"], r["prompts"]["substrate"]["dla"]
    fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    for ax, kind in zip(axes, ("attn", "mlp")):
        ax.axhline(0, color="k", lw=0.6)
        ax.bar(x - 0.2, b[kind], 0.4, color=C_BASE, label="baseline")
        ax.bar(x + 0.2, s[kind], 0.4, color=C_SUB, label="substrate")
        ax.set_ylabel(f"{kind} → drive−walk logit")
        ax.legend(fontsize=8)
    axes[0].set_title(f"{r['model']}: direct logit attribution per sublayer "
                      f"(sums: base {b['total']:+.2f}, sub {s['total']:+.2f})")
    axes[1].set_xlabel("layer")
    fig.tight_layout()
    fig.savefig(d / "dla.png", dpi=150)
    plt.close(fig)


def fig_heads(r: dict, d: Path):
    b = np.array(r["prompts"]["baseline"]["dla"]["heads"])
    s = np.array(r["prompts"]["substrate"]["dla"]["heads"])
    diff = s - b
    v = float(np.abs(diff).max()) or 1.0
    fig, ax = plt.subplots(figsize=(10, 0.22 * b.shape[0] + 2))
    im = ax.imshow(diff, cmap="RdBu_r", vmin=-v, vmax=v, aspect="auto")
    ax.set_xlabel("head")
    ax.set_ylabel("layer")
    ax.set_title(f"{r['model']}: per-head DLA change, substrate − baseline "
                 f"(red = pushes drive more)")
    fig.colorbar(im, ax=ax, label="Δ drive−walk logit")
    # annotate top movers
    flat = np.argsort(-np.abs(diff).ravel())[:8]
    for f in flat:
        L, H = divmod(int(f), diff.shape[1])
        ax.text(H, L, f"{diff[L, H]:+.1f}", ha="center", va="center", fontsize=6)
    fig.tight_layout()
    fig.savefig(d / "heads.png", dpi=150)
    plt.close(fig)


SPAN_ORDER = ["bos", "hdr_user", "line1", "line2", "hdr_action", "line3", "line4",
              "line5", "line6", "question", "answer_instr", "asst_header", "last"]


def fig_attention(r: dict, d: Path):
    n = r["n_layers"]
    x = np.arange(n)
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5), sharey=True)
    for ax, name in zip(axes, ("baseline", "substrate")):
        am = r["prompts"][name]["attn_mass"]
        keys = [k for k in SPAN_ORDER if k in am]
        bottom = np.zeros(n)
        cmap = plt.get_cmap("tab20")
        for i, k in enumerate(keys):
            vals = np.array(am[k]["mean"])
            ax.bar(x, vals, bottom=bottom, color=cmap(i % 20), label=k, width=0.9)
            bottom += vals
        ax.set_title(f"{name}: attention mass from the answer position (mean over heads)")
        ax.set_xlabel("layer")
    axes[0].set_ylabel("attention mass")
    axes[1].legend(fontsize=7, ncol=2, loc="upper right")
    fig.tight_layout()
    fig.savefig(d / "attention.png", dpi=150)
    plt.close(fig)


def fig_ablations(r: dict, d: Path):
    if "ablations" not in r:
        return
    ab = r["ablations"]
    full = r["prompts"]["substrate"]["final"]["M_sum"]
    base = r["prompts"]["baseline"]["final"]["M_sum"]
    names = ["baseline", "headers_only"] + [f"only_line{i}" for i in range(1, 7)] \
        + [f"loo_line{i}" for i in range(1, 7)] + ["substrate (full)"]
    vals = [base, ab.get("headers_only", np.nan)] + [ab.get(f"only_line{i}", np.nan) for i in range(1, 7)] \
        + [ab.get(f"loo_line{i}", np.nan) for i in range(1, 7)] + [full]
    cols = [C_BASE, C_BASE] + ["#60a5fa"] * 6 + ["#f87171"] * 6 + [C_SUB]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.axhline(0, color="k", lw=0.6)
    ax.bar(range(len(vals)), vals, color=cols)
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("M [nats]")
    ax.set_title(f"{r['model']}: substrate line ablations "
                 f"(blue = that line only, red = all but that line)")
    fig.tight_layout()
    fig.savefig(d / "ablations.png", dpi=150)
    plt.close(fig)


def fig_benchmarks(r: dict, d: Path):
    if "benchmarks" not in r:
        return
    bm = r["benchmarks"]
    names = list(bm)
    vals = [bm[k]["M_sum"] for k in names]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.axhline(0, color="k", lw=0.6)
    ax.bar(range(len(vals)), vals,
           color=[C_SUB if k == "substrate" else C_BASE for k in names])
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("M [nats]")
    ax.set_title(f"{r['model']}: every prompt in prompts/ (M > 0 ⇒ drive)")
    fig.tight_layout()
    fig.savefig(d / "benchmarks.png", dpi=150)
    plt.close(fig)


def fig_diff(r: dict, d: Path):
    n = r["n_layers"]
    x = layer_axis(n)
    df = r["diff"]
    fig, ax1 = plt.subplots(figsize=(9, 4))
    ax1.plot(x, df["cos_resid"], "-o", ms=3, color=C_BASE, label="cos(baseline, substrate) residual")
    ax1.plot(x, df["cos_diff_u"], "-o", ms=3, color=C_SUB, label="cos(substrate − baseline, drive−walk unembed)")
    ax1.axhline(0, color="k", lw=0.6)
    ax1.set_ylabel("cosine")
    ax1.set_xlabel("layer (-1 = embedding)")
    ax2 = ax1.twinx()
    ax2.plot(x, np.array(df["norm_diff"]) / np.array(df["norm_base"]), ":", color=C_PATCH,
             label="|Δ| / |baseline|")
    ax2.set_ylabel("relative norm of the difference")
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, fontsize=8)
    ax1.set_title(f"{r['model']}: residual at the answer position, baseline vs substrate")
    fig.tight_layout()
    fig.savefig(d / "diff.png", dpi=150)
    plt.close(fig)


def summary(r: dict, d: Path) -> str:
    b, s = r["prompts"]["baseline"], r["prompts"]["substrate"]
    n = r["n_layers"]
    lines = [f"# {r['model']}", "",
             f"quant: {r['quantize'] or 'bf16'} · layers {n} · heads {r['n_heads']} · "
             f"drive token {r['drive_token'][1]!r} · walk token {r['walk_token'][1]!r}", "",
             "| prompt | M (nats) | p(drive) | p(walk) | greedy |", "|---|---|---|---|---|"]
    for name, p in (("baseline", b), ("substrate", s)):
        f = p["final"]
        lines.append(f"| {name} | {f['M_sum']:+.2f} | {f['p_drive']:.3f} | {f['p_walk']:.3f} | {f['greedy']!r} |")
    lines += ["", "## logit lens (M per layer, emb first)",
              "baseline:  " + " ".join(f"{v:+.1f}" for v in b["lens"]["M_sum"]),
              "substrate: " + " ".join(f"{v:+.1f}" for v in s["lens"]["M_sum"]),
              f"final lens row == model logits: base {b['lens']['final_row_matches_model']}, "
              f"sub {s['lens']['final_row_matches_model']}", ""]
    if "patching" in r:
        pm = r["patching"]["M_sum"]
        pos = [i for i, v in enumerate(pm) if v > 0]
        lines += ["## patching (substrate residual into baseline at the answer position)",
                  "M per layer: " + " ".join(f"{v:+.1f}" for v in pm),
                  f"layers where the patch alone flips baseline to drive: {pos}", ""]
    bd, sd = b["dla"], s["dla"]
    da = np.array(sd["attn"]) - np.array(bd["attn"])
    dm = np.array(sd["mlp"]) - np.array(bd["mlp"])
    lines += ["## direct logit attribution (drive−walk), substrate − baseline",
              f"DLA sums: base {bd['total']:+.2f} (model {bd['M_first_check']:+.2f}), "
              f"sub {sd['total']:+.2f} (model {sd['M_first_check']:+.2f})",
              "top Δ attention layers: " + ", ".join(f"L{i} {da[i]:+.2f}" for i in np.argsort(-np.abs(da))[:5]),
              "top Δ MLP layers:       " + ", ".join(f"L{i} {dm[i]:+.2f}" for i in np.argsort(-np.abs(dm))[:5])]
    hd = np.array(sd["heads"]) - np.array(bd["heads"])
    top = np.argsort(-np.abs(hd).ravel())[:8]
    lines.append("top Δ heads: " + ", ".join(
        f"L{L}H{H} {hd[L, H]:+.2f}" for L, H in (divmod(int(t), hd.shape[1]) for t in top)))
    lines.append("")
    am = s["attn_mass"]
    lines += ["## attention from the answer position (substrate run, mean over heads and layers)"]
    for k in SPAN_ORDER:
        if k in am:
            v = np.array(am[k]["mean"])
            lines.append(f"- {k}: mean {v.mean():.3f}, max layer L{int(v.argmax())} ({v.max():.3f})")
    # heads that both attend to substrate lines and push drive
    line_keys = [k for k in am if k.startswith("line")]
    if line_keys:
        mass = sum(np.array(am[k]["heads"]) for k in line_keys)   # [L, H]
        score = mass * np.clip(hd, 0, None)
        top = np.argsort(-score.ravel())[:6]
        lines.append("heads attending to substrate lines AND pushing drive (mass × ΔDLA): " + ", ".join(
            f"L{L}H{H} mass {mass[L, H]:.2f} Δ{hd[L, H]:+.2f}"
            for L, H in (divmod(int(t), hd.shape[1]) for t in top)))
    lines.append("")
    if "ablations" in r:
        ab = r["ablations"]
        lines += ["## substrate line ablations (M)", "| variant | M |", "|---|---|"]
        for k, v in ab.items():
            lines.append(f"| {k} | {v:+.2f} |")
        lines.append("")
        for i, ln in enumerate(r.get("substrate_lines", []), 1):
            lines.append(f"line{i}: {ln.strip()}")
        lines.append("")
    if "benchmarks" in r:
        lines += ["## all prompts", "| prompt | M | argmax | greedy |", "|---|---|---|---|"]
        for k, v in r["benchmarks"].items():
            lines.append(f"| {k} | {v['M_sum']:+.2f} | {v['argmax']!r} | {v['greedy']!r} |")
        lines.append("")
    text = "\n".join(lines)
    (d / "summary.md").write_text(text)
    return text


def overview(rs: list[tuple[str, dict]], out: Path):
    fig, axes = plt.subplots(1, len(rs), figsize=(6 * len(rs), 4), sharey=True)
    axes = np.atleast_1d(axes)
    for ax, (name, r) in zip(axes, rs):
        n = r["n_layers"]
        x = layer_axis(n) / max(n - 1, 1)     # relative depth
        ax.axhline(0, color="k", lw=0.6)
        ax.plot(x, r["prompts"]["baseline"]["lens"]["M_sum"], "-", color=C_BASE, label="baseline")
        ax.plot(x, r["prompts"]["substrate"]["lens"]["M_sum"], "-", color=C_SUB, label="substrate")
        if "patching" in r:
            ax.plot(np.arange(n) / max(n - 1, 1), r["patching"]["M_sum"], "--", color=C_PATCH, label="patched")
        ax.set_title(r["model"], fontsize=9)
        ax.set_xlabel("relative depth")
    axes[0].set_ylabel("M [nats]")
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def main():
    dirs = [Path(a) for a in sys.argv[1:]]
    if not dirs:
        sys.exit(__doc__)
    rs = []
    for d in dirs:
        r = load(d)
        for f in (fig_lens, fig_dla, fig_heads, fig_attention, fig_ablations, fig_benchmarks, fig_diff):
            f(r, d)
        print(summary(r, d))
        rs.append((d.name, r))
    if len(rs) > 1:
        overview(rs, dirs[0].parent / "overview.png")
        print("wrote", dirs[0].parent / "overview.png")


if __name__ == "__main__":
    main()
