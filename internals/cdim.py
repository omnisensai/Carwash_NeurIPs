#!/usr/bin/env python3
"""Constraint–Depth Intervention Map (CDIM), Mechanistic_paper.md §2–§9.

Where, across transformer depth and sequence position, does a behaviourally
verified substrate line become causally consequential for the decision?

For the substrate S (system prompt + baseline question) and a token-aligned
counterfactual C_i (the same prompt with bullet line i replaced by a line of
identical token count that neutralises / reverses its semantics,
cdim_counterfactuals.json):

  * behavioural effect   Delta_i = M(S) - M(C_i)                       (§2)
  * forward rescue       R[l,g]  = M(C | r^C_{l,g} <- r^S_{l,g}) - M(C)  (§4.1)
  * reverse disruption   D[l,g]  = M(S) - M(S | r^S_{l,g} <- r^C_{l,g})  (§4.2)

where l runs over the embedding output and every layer output, and g over
semantic groups of positions (each substrate line, the headers, the whole
system block, the question, the answer instruction, the assistant header,
the answer site). All positions of a group are patched jointly.

Controls (§9): same-run patch S->S; random-direction replacement of the same
norm as (S - C); the library question under the same substrate / counterfactual
(must stay Walk). Path validation (§7): the effect of the critical line's
state at (l_src, line) that is mediated by the question span / the answer site
at a later layer l_dst (patch-the-receiver path patching).

M = log P(drive) - log P(walk) summed over surface forms (M_sum of
run_internals.py), read at the position that predicts the first answer
token, teacher-forced, chat template.

    python cdim.py --model meta-llama/Llama-3.1-8B-Instruct --device cpu --dtype bfloat16 \
                   --out results/llama-3.1-8b/bf16
    python plot_cdim.py results/llama-3.1-8b/bf16

Output: <out>/cdim.json (+ cdim_resid.pt with the S / C residual stacks of the
primary counterfactual).
"""
from __future__ import annotations

import argparse
import functools
import json
import sys
import time
from pathlib import Path

import torch

from run_internals import (PROMPTS, answer_ids, decision_margin, embed, greedy,
                           layers_of, lens_logits, load, margin_from_logits,
                           out_tensor, parse_prompt, render, substrate_lines,
                           token_spans)

HERE = Path(__file__).resolve().parent
print = functools.partial(print, flush=True)   # progress lines survive redirection to a log file


# ----------------------------------------------------------------- prompts --

def replace_line(system: str, k: int, new_line: str) -> str:
    """System prompt with bullet line k (1-based) replaced."""
    lines = system.splitlines()
    bullets = [i for i, ln in enumerate(lines) if ln.lstrip().startswith("-")]
    if k < 1 or k > len(bullets):
        raise ValueError(f"substrate has {len(bullets)} bullet lines, no line {k}")
    indent = lines[bullets[k - 1]][:len(lines[bullets[k - 1]]) - len(lines[bullets[k - 1]].lstrip())]
    lines[bullets[k - 1]] = indent + new_line.strip()
    return "\n".join(lines)


def groups_from_spans(spans: dict[str, list[int]], n_tokens: int) -> dict[str, list[int]]:
    """Semantic position groups (§4): every substrate line, the headers, the
    whole system block, the question, the answer instruction, the assistant
    header (without the last position) and the answer site."""
    g: dict[str, list[int]] = {}
    lines = sorted(k for k in spans if k.startswith("line"))
    for k in lines:
        a, b = spans[k]
        g[k] = list(range(a, b))
    hdr = [p for k in spans if k.startswith("hdr_") for p in range(*spans[k])]
    if hdr:
        g["headers"] = sorted(hdr)
    sysblock = sorted(set(hdr) | {p for k in lines for p in g[k]})
    if sysblock:
        g["system"] = sysblock
    if "question" in spans:
        g["question"] = list(range(*spans["question"]))
    if "answer_instr" in spans:
        g["answer_instr"] = list(range(*spans["answer_instr"]))
    if "asst_header" in spans:
        a, b = spans["asst_header"]
        if b - 1 > a:
            g["asst_header"] = list(range(a, b - 1))
    g["answer_site"] = [n_tokens - 1]
    return g


# ------------------------------------------------------------------- hooks --

class FullCapture:
    """Residual stream at EVERY position: row 0 = embedding output, row l+1 =
    output of layer l. Stored fp32 on CPU as [L+1, T, d]."""

    def __init__(self, model):
        self.handles = []
        self.rows: dict[int, torch.Tensor] = {}
        self.handles.append(embed(model).register_forward_hook(self._row(0)))
        for i, layer in enumerate(layers_of(model)):
            self.handles.append(layer.register_forward_hook(self._row(i + 1)))

    def _row(self, r):
        def hook(_m, _i, out):
            self.rows[r] = out_tensor(out)[0].detach().float().cpu()
        return hook

    def stack(self) -> torch.Tensor:
        return torch.stack([self.rows[r] for r in range(len(self.rows))])

    def remove(self):
        for h in self.handles:
            h.remove()


class RowCapture:
    """Residual at one row (0 = embedding, l+1 = layer l) at given positions."""

    def __init__(self, model, row: int, pos: list[int]):
        mod = embed(model) if row == 0 else layers_of(model)[row - 1]
        self.pos, self.val = pos, None

        def hook(_m, _i, out):
            self.val = out_tensor(out)[0, self.pos, :].detach().float().cpu()
        self.h = mod.register_forward_hook(hook)

    def remove(self):
        self.h.remove()


class GroupPatch:
    """Replace the residual at row r (0 = embedding, l+1 = layer l), positions
    pos, by vec[pos] (vec: [T, d] or [len(pos), d]) during one forward."""

    def __init__(self, model, row: int, pos: list[int], vec: torch.Tensor):
        mod = embed(model) if row == 0 else layers_of(model)[row - 1]
        v = vec if vec.shape[0] == len(pos) else vec[pos]

        def hook(_m, _i, out):
            t = out_tensor(out)
            t[0, pos, :] = v.to(t.dtype).to(t.device)
        self.h = mod.register_forward_hook(hook)

    def remove(self):
        self.h.remove()


@torch.no_grad()
def run_margin(model, ids: torch.Tensor, aid: dict, patches: list = (), cap=None) -> float:
    try:
        out = model(input_ids=ids, use_cache=False, logits_to_keep=1)
    finally:
        for p in patches:
            p.remove()
    return margin_from_logits(out.logits[0, -1].float().cpu(), aid)["M_sum"]


@torch.no_grad()
def run_full(model, tok, text: str, aid: dict):
    """One captured pass: ids, final margin dict, [L+1, T, d] residual stack."""
    ids = tok(text, add_special_tokens=False, return_tensors="pt")["input_ids"]
    dev = embed(model).weight.device
    cap = FullCapture(model)
    try:
        out = model(input_ids=ids.to(dev), use_cache=False, logits_to_keep=1)
    finally:
        cap.remove()
    m = margin_from_logits(out.logits[0, -1].float().cpu(), aid)
    m["greedy"] = greedy(model, tok, text)
    m["decision"] = decision_margin(model, tok, text, aid)
    return ids.to(dev), m, cap.stack()


# --------------------------------------------------------------------- map --

def cdim_map(model, ids_c, ids_s, aid, stack_s, stack_c, groups, M_s, M_c, rows, log=print):
    """R[row][group] and D[row][group] over rows (0 = emb) and groups."""
    R = {g: [None] * (max(rows) + 1) for g in groups}
    D = {g: [None] * (max(rows) + 1) for g in groups}
    for r in rows:
        for g, pos in groups.items():
            m = run_margin(model, ids_c, aid, [GroupPatch(model, r, pos, stack_s[r])])
            R[g][r] = m - M_c
            m = run_margin(model, ids_s, aid, [GroupPatch(model, r, pos, stack_c[r])])
            D[g][r] = M_s - m
        log(f"  row {r:02d}: " + " ".join(f"{g}={R[g][r]:+.2f}/{D[g][r]:+.2f}" for g in groups))
    return R, D


def path_map(model, ids_c, aid, stack_s, src_pos, dst_groups, M_c, src_rows, dst_rows, log=print):
    """Patch-the-receiver path patching: the S state of the source group at
    row r_src is inserted into the C run; the receiver state (row r_dst,
    group g_dst) produced by that run is then inserted alone into a clean C
    run. mediated[g_dst][r_src][r_dst] = M(that run) - M(C)."""
    out = {g: {} for g in dst_groups}
    for rs in src_rows:
        total = run_margin(model, ids_c, aid, [GroupPatch(model, rs, src_pos, stack_s[rs])]) - M_c
        for rd in dst_rows:
            if rd <= rs:
                continue
            for g, pos in dst_groups.items():
                rc = RowCapture(model, rd, pos)
                try:
                    run_margin(model, ids_c, aid, [GroupPatch(model, rs, src_pos, stack_s[rs])])
                finally:
                    rc.remove()
                m = run_margin(model, ids_c, aid, [GroupPatch(model, rd, pos, rc.val)])
                out[g].setdefault(str(rs), {})[str(rd)] = m - M_c
        log(f"  src row {rs:02d}: total={total:+.2f} " +
            " ".join(f"{g}@{rd}={out[g][str(rs)][str(rd)]:+.2f}" for g in dst_groups
                     for rd in dst_rows if rd > rs))
        out.setdefault("_total", {})[str(rs)] = total
    return out


# -------------------------------------------------------------------- main --

def prompt_path(name: str) -> Path:
    """A prompts/ file name (the default) or a path to a file elsewhere (cdim_sweep/generated/...)."""
    p = Path(name)
    return p if p.exists() and p.is_file() else PROMPTS / name


def run_cdim(tok, model, aid, sub_p: dict, base_p: dict, lib_p: dict | None, cfs: list[dict], out: Path,
             *, label: str, map_sel: str = "all", min_delta: float = 1.0, row_stride: int = 1,
             path_stride: int = 2, controls: bool = True, library: bool = True, path: bool = True,
             seed: int = 0, meta: dict | None = None) -> dict:
    """The whole CDIM run for one (substrate system prompt, question) pair on an
    already loaded model. sub_p / base_p / lib_p are parse_prompt() dicts; the
    question is base_p["user"], the control question lib_p["user"]. Writes
    <out>/cdim.json and cdim_resid.pt and returns the json dict."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    torch.manual_seed(seed)
    sub_p = dict(sub_p)
    sub_p["user"] = base_p["user"]          # the baseline question, as in run_internals.py
    lines = substrate_lines(sub_p["system"])

    # --- S
    text_s = render(tok, sub_p, raw=False)
    ids_s, m_s, stack_s = run_full(model, tok, text_s, aid)
    spans_s = token_spans(tok, text_s, ids_s[0].tolist(), sub_p)
    groups = groups_from_spans(spans_s, ids_s.shape[1])
    n_rows = stack_s.shape[0]                    # emb + layers
    M_s = m_s["M_sum"]
    print(f"S: M={M_s:+.3f} greedy={m_s['greedy']!r} tokens={ids_s.shape[1]} rows={n_rows}", flush=True)
    print("groups:", {g: (p[0], p[-1] + 1, len(p)) for g, p in groups.items()}, flush=True)

    # --- counterfactuals: alignment + behavioural effect
    res_cf = {}
    for cf in cfs:
        sysm = replace_line(sub_p["system"], cf["line"], cf["text"])
        p = {"system": sysm, "user": sub_p["user"]}
        text_c = render(tok, p, raw=False)
        ids_c = tok(text_c, add_special_tokens=False, return_tensors="pt")["input_ids"]
        ok = ids_c.shape[1] == ids_s.shape[1]
        if ok:
            span = spans_s[f"line{cf['line']}"]
            same = ids_c[0].tolist()
            same_outside = all(a == b for i, (a, b) in enumerate(zip(same, ids_s[0].tolist()))
                               if not (span[0] <= i < span[1]))
            ok = same_outside
        cf_text_tok = len(tok.encode(cf["text"], add_special_tokens=False))
        res_cf[cf["name"]] = {"line": cf["line"], "kind": cf.get("kind"), "text": cf["text"],
                              "original": lines[cf["line"] - 1], "aligned": bool(ok),
                              "n_tokens_line": cf_text_tok, "_p": p, "_text": text_c}
        if not ok:
            print(f"  {cf['name']}: NOT token-aligned ({ids_c.shape[1]} vs {ids_s.shape[1]} tokens) — skipped", flush=True)
            continue
        ids_c, m_c, stack_c = run_full(model, tok, text_c, aid)
        res_cf[cf["name"]].update({"M": m_c["M_sum"], "greedy": m_c["greedy"], "decision": m_c["decision"],
                                   "delta_beh": M_s - m_c["M_sum"], "_ids": ids_c, "_stack": stack_c})
        print(f"  {cf['name']} (line {cf['line']}, {cf.get('kind')}): M={m_c['M_sum']:+.3f} "
              f"Delta={M_s - m_c['M_sum']:+.3f} greedy={m_c['greedy']!r}", flush=True)

    aligned = [n for n, r in res_cf.items() if r["aligned"]]
    if not aligned:
        sys.exit("no aligned counterfactual")
    if map_sel == "all":
        to_map = aligned
    elif map_sel == "auto":
        to_map = [n for n in aligned if abs(res_cf[n]["delta_beh"]) >= min_delta]
        if not to_map:
            to_map = [max(aligned, key=lambda n: abs(res_cf[n]["delta_beh"]))]
    else:
        to_map = [n for n in map_sel.split(",") if n in aligned]
    primary = max(to_map, key=lambda n: abs(res_cf[n]["delta_beh"]))
    rows = list(range(0, n_rows, row_stride))
    if rows[-1] != n_rows - 1:
        rows.append(n_rows - 1)
    print(f"mapping {to_map} (primary {primary}); rows {rows[0]}..{rows[-1]} stride {row_stride}", flush=True)

    # answer-site logit lens of S and each mapped C (optional readout, §13)
    lens = {"S": [margin_from_logits(lens_logits(model, stack_s[r, -1]), aid)["M_sum"] for r in range(n_rows)]}

    # --- the maps
    for n in to_map:
        r = res_cf[n]
        print(f"CDIM {n}: R (S -> C) and D (C -> S) ...", flush=True)
        R, D = cdim_map(model, r["_ids"], ids_s, aid, stack_s, r["_stack"], groups, M_s, r["M"], rows)
        r["R"], r["D"] = R, D
        lens[n] = [margin_from_logits(lens_logits(model, r["_stack"][k, -1]), aid)["M_sum"] for k in range(n_rows)]

    # --- controls (§9)
    ctrl = {}
    if controls:
        pr = res_cf[primary]
        ctrl_rows = sorted(set([0, 1, n_rows // 4, n_rows // 2, 3 * n_rows // 4, n_rows - 1]))
        print(f"controls (rows {ctrl_rows}) ...", flush=True)
        same = {g: {} for g in groups}
        for r in ctrl_rows:
            for g, pos in groups.items():
                same[g][str(r)] = run_margin(model, ids_s, aid, [GroupPatch(model, r, pos, stack_s[r])]) - M_s
        ctrl["same_run_S"] = {"dM": same,
                              "max_abs": max(abs(v) for g in same for v in same[g].values())}
        rnd_rows = sorted(set(list(range(0, n_rows, max(1, n_rows // 8))) + [n_rows - 1]))
        rnd = {g: {} for g in groups}
        gen = torch.Generator().manual_seed(seed)
        for r in rnd_rows:
            for g, pos in groups.items():
                diff = stack_s[r][pos] - pr["_stack"][r][pos]
                noise = torch.randn(diff.shape, generator=gen)
                noise = noise / noise.norm(dim=-1, keepdim=True) * diff.norm(dim=-1, keepdim=True)
                vec = pr["_stack"][r][pos] + noise
                rnd[g][str(r)] = run_margin(model, pr["_ids"], aid, [GroupPatch(model, r, pos, vec)]) - pr["M"]
        ctrl["random_direction"] = {
            "dM": rnd, "counterfactual": primary,
            "note": "C run, group state replaced by C + random direction with the per-position norm of (S - C)",
            "max_abs": max(abs(v) for g in rnd for v in rnd[g].values())}
        print(f"  same-run max|dM|={ctrl['same_run_S']['max_abs']:.4f}  "
              f"random-direction max|dM|={ctrl['random_direction']['max_abs']:.3f}", flush=True)

    # --- control question (library by default) under S and the primary C (must stay Walk)
    lib = None
    if library and lib_p is not None:
        pr = res_cf[primary]
        print("library control ...", flush=True)
        lib_s = {"system": sub_p["system"], "user": lib_p["user"]}
        lib_c = {"system": pr["_p"]["system"], "user": lib_p["user"]}
        t_ls, t_lc = render(tok, lib_s, False), render(tok, lib_c, False)
        ids_ls, m_ls, st_ls = run_full(model, tok, t_ls, aid)
        ids_lc, m_lc, st_lc = run_full(model, tok, t_lc, aid)
        assert ids_ls.shape == ids_lc.shape
        spans_l = token_spans(tok, t_ls, ids_ls[0].tolist(), lib_s)
        groups_l = groups_from_spans(spans_l, ids_ls.shape[1])
        print(f"  library S: M={m_ls['M_sum']:+.3f} greedy={m_ls['greedy']!r}; "
              f"library C: M={m_lc['M_sum']:+.3f} greedy={m_lc['greedy']!r}", flush=True)
        R, D = cdim_map(model, ids_lc, ids_ls, aid, st_ls, st_lc, groups_l, m_ls["M_sum"], m_lc["M_sum"], rows)
        patched_max = max(max(max(v for v in R[g] if v is not None) + m_lc["M_sum"],
                              m_ls["M_sum"] - min(v for v in D[g] if v is not None)) for g in R)
        lib = {"counterfactual": primary, "question": lib_p["user"], "M_S": m_ls["M_sum"], "M_C": m_lc["M_sum"],
               "greedy_S": m_ls["greedy"], "greedy_C": m_lc["greedy"],
               "delta_beh": m_ls["M_sum"] - m_lc["M_sum"], "groups": groups_l,
               "R": R, "D": D, "max_patched_M": patched_max,
               "stays_walk": bool(patched_max < 0)}
        print(f"  library: max patched M={patched_max:+.3f} -> {'stays Walk' if patched_max < 0 else 'GOES DRIVE'}", flush=True)

    # --- path validation (§7) on the primary counterfactual
    pth = None
    if path:
        pr = res_cf[primary]
        src = groups[f"line{pr['line']}"]
        dst = {"question": groups["question"], "answer_site": groups["answer_site"]}
        grid = list(range(0, n_rows, path_stride))
        if grid[-1] != n_rows - 1:
            grid.append(n_rows - 1)
        print(f"path validation: line{pr['line']} -> question / answer_site, rows {grid} ...", flush=True)
        med = path_map(model, pr["_ids"], aid, stack_s, src, dst, pr["M"], grid, grid)
        pth = {"counterfactual": primary, "source": f"line{pr['line']}", "rows": grid,
               "total_dM": med.pop("_total"), "mediated_dM": med,
               "note": "mediated_dM[g][r_src][r_dst]: S state of the source group inserted at row r_src into "
                       "the C run; the resulting receiver state (row r_dst, group g) inserted alone into a "
                       "clean C run; M - M(C). total_dM[r_src] is the plain rescue R[r_src, source]."}

    # --- write
    res = {
        "model": label,
        "substrate_sha256": sub_p["sha256"], "baseline_sha256": base_p["sha256"],
        "question": sub_p["user"], "n_layers": n_rows - 1, "rows": rows,
        "row_note": "row 0 = embedding output, row l+1 = output of decoder layer l",
        "n_tokens": ids_s.shape[1], "tokens": [tok.decode(t) for t in ids_s[0].tolist()],
        "spans": spans_s, "groups": groups, "substrate_lines": lines,
        "S": {"M": M_s, "greedy": m_s["greedy"], "decision": m_s["decision"]},
        "counterfactuals": {n: {k: v for k, v in r.items() if not k.startswith("_")} for n, r in res_cf.items()},
        "mapped": to_map, "primary": primary,
        "lens_answer_site": lens, "controls": ctrl, "library": lib, "path": pth,
        "seconds": round(time.time() - t0, 1), "torch": torch.__version__,
    }
    res.update(meta or {})
    import transformers
    res["transformers"] = transformers.__version__
    (out / "cdim.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    torch.save({"S": stack_s, "C": res_cf[primary]["_stack"], "primary": primary,
                "rows": ["emb"] + [f"layer{i}" for i in range(n_rows - 1)]}, out / "cdim_resid.pt")
    print(f"wrote {out / 'cdim.json'} in {res['seconds']} s", flush=True)
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True, help="result dir (cdim.json is written into it)")
    ap.add_argument("--quantize", choices=["4bit", "8bit"], default=None)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--dtype", default=None, choices=["bfloat16", "float16", "float32"])
    ap.add_argument("--label", default=None)
    ap.add_argument("--substrate", default="substrate.txt", help="prompts/ file name, or a path to a System: file")
    ap.add_argument("--baseline", default="baseline.txt", help="prompts/ file name, or a path to a question file")
    ap.add_argument("--library", default="benchmark_library.txt",
                    help="control question that must stay Walk (prompts/ file name or path)")
    ap.add_argument("--counterfactuals", default=str(HERE / "cdim_counterfactuals.json"))
    ap.add_argument("--map", default="all",
                    help="which counterfactuals get the full layer x group map: "
                         "'all', 'auto' (|Delta| >= --min-delta, at least the largest), or names (cf6,cf1)")
    ap.add_argument("--min-delta", type=float, default=1.0)
    ap.add_argument("--row-stride", type=int, default=1, help="patch every k-th row (70B: 2)")
    ap.add_argument("--path-stride", type=int, default=2, help="row stride of the path-validation grid")
    ap.add_argument("--no-controls", action="store_true")
    ap.add_argument("--no-library", action="store_true")
    ap.add_argument("--no-path", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    print(f"loading {args.model} ({args.quantize or args.dtype or 'default dtype'}, {args.device}) ...", flush=True)
    tok, model = load(args.model, args.quantize, args.device, args.dtype)
    aid = answer_ids(tok)

    base_p = parse_prompt(prompt_path(args.baseline).read_text())
    sub_p = parse_prompt(prompt_path(args.substrate).read_text())
    lib_p = parse_prompt(prompt_path(args.library).read_text())
    if not sub_p["system"]:
        sys.exit(f"{args.substrate} has no 'System:' block")
    cfs = json.loads(Path(args.counterfactuals).read_text()).get(Path(args.substrate).name)
    if not cfs:
        sys.exit(f"no counterfactuals for {Path(args.substrate).name} in {args.counterfactuals}")
    run_cdim(tok, model, aid, sub_p, base_p, lib_p, cfs, Path(args.out),
             label=args.label or args.model, map_sel=args.map, min_delta=args.min_delta,
             row_stride=args.row_stride, path_stride=args.path_stride, controls=not args.no_controls,
             library=not args.no_library, path=not args.no_path, seed=args.seed,
             meta={"quantize": args.quantize, "device": args.device, "dtype": args.dtype,
                   "substrate_file": args.substrate, "baseline_file": args.baseline, "library_file": args.library})


if __name__ == "__main__":
    with torch.no_grad():
        main()
