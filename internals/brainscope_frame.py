#!/usr/bin/env python3
"""The "drive frame" across layers and prompt conditions (brainscope directions).

Where in the network does the representation "the object has to come along, so
drive" form, and which of the prompt conditions install it? Three steps:

 1. direction  A contrast-pair direction per layer, extracted with brainscope's
               `pca_directions` (first principal component of completion-hidden
               differences, repeng-style): the same question answered with a
               drive rationale (positive) and a walk rationale (negative), over
               every vehicle scenario x question body of cdim_sweep. The per-layer
               separation score says where the frame lives.
 2. projection Every token of every condition prompt (baseline, each prompts/
               benchmark_*.txt, the substrate, every ladder level) projected on
               that layer's unit direction: a [layers x tokens] map per condition,
               plus the answer-site curve and the mean over the question span.
 3. readout    Logit-lens M per layer at the answer site for every condition, and
               the final M / greedy answer. Formation layer = first layer where the
               answer-site projection reaches half its final value; decisive layer
               = first row from which the lens M stays on the final side of zero.

    python brainscope_frame.py --model unsloth/Llama-3.3-70B-Instruct --out results/llama-3.3-70b/bf16-frame
    python brainscope_frame.py --model Qwen/Qwen3-8B --out results/qwen3-8b/bf16-frame

Needs `pip install brainscope` (falls back to a local copy of the two functions
if the package is absent). Output: frame.json, frame_pairs.jsonl, frame.png.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch

from run_internals import (PROMPTS, answer_ids, greedy, lens_logits, load, margin_from_logits,
                           parse_prompt, render, token_spans)
from cdim import FullCapture

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "cdim_sweep"))
from build_prompts import GEN, load as load_prompts, write_generated   # noqa: E402

try:
    from brainscope.pca_directions import completion_hiddens, pca_direction
    BRAINSCOPE = "brainscope"
except Exception:                                   # same maths, local copy
    BRAINSCOPE = "local"

    @torch.inference_mode()
    def completion_hiddens(model, tok, device, system, prompt, completion):
        msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
        def ids(m, gen):
            o = tok.apply_chat_template(m, add_generation_prompt=gen, return_tensors="pt", enable_thinking=False)
            return o if torch.is_tensor(o) else o["input_ids"]
        pre = ids(msgs, True)
        full = ids(msgs + [{"role": "assistant", "content": completion}], False)
        out = model(input_ids=full.to(device), output_hidden_states=True)
        span = slice(pre.shape[1], full.shape[1])
        return torch.stack([h[0, span].float().mean(0) for h in out.hidden_states[1:]])

    def pca_direction(diffs):
        x = diffs - diffs.mean(0, keepdim=True)
        _, _, v = torch.linalg.svd(x, full_matrices=False)
        d = v[0]
        return d if (diffs @ d).mean() >= 0 else -d


RATIONALE = {
    "drive": "Drive. The {object} has to be at the {place} for that, and walking would leave it at {origin}.",
    "walk":  "Walk. The {place} is only 50 metres away, so walking there is the obvious choice.",
}


def contrast_pairs(D, bodies):
    for sid, s in D["scenarios"].items():
        if s["kind"] != "vehicle":
            continue
        for b in bodies:
            prompt = D["bodies"][b].format(task=s["task"], place=s["place"]) + "\n\n" + D["tails"]["T1"]
            yield {"scenario": sid, "body": b, "prompt": prompt, "system": None,
                   "positive": RATIONALE["drive"].format(**s), "negative": RATIONALE["walk"].format(**s)}


def conditions(D, fill: str) -> dict[str, dict]:
    """name -> {system, user}: baseline, every benchmark file, the substrate (S), the ladder levels."""
    base = parse_prompt((PROMPTS / "baseline.txt").read_text())
    out = {"baseline": {"system": None, "user": base["user"]}}
    for f in sorted(PROMPTS.glob("benchmark_*.txt")):
        p = parse_prompt(f.read_text())
        if p["user"]:
            out[f.stem.replace("benchmark_", "")] = {"system": None, "user": p["user"]}
    for lvl in D["order"]:
        p = parse_prompt((GEN / "substrates" / fill / f"{lvl}.txt").read_text())
        out[f"substrate_{lvl}" if lvl != "S" else "substrate"] = {"system": p["system"], "user": base["user"]}
    return out


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--quantize", choices=["4bit", "8bit"], default=None)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--dtype", default=None, choices=["bfloat16", "float16", "float32"])
    ap.add_argument("--label", default=None)
    ap.add_argument("--bodies", default="P0,P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11")
    ap.add_argument("--fill", default="carwash")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    D = load_prompts()
    write_generated(D)
    print(f"loading {args.model} ({args.quantize or args.dtype or 'default dtype'}, {args.device}); directions via {BRAINSCOPE}", flush=True)
    tok, model = load(args.model, args.quantize, args.device, args.dtype)
    aid = answer_ids(tok)
    dev = model.get_input_embeddings().weight.device

    # 1. direction per layer
    pairs = list(contrast_pairs(D, args.bodies.split(",")))
    (out / "frame_pairs.jsonl").write_text("\n".join(json.dumps(p) for p in pairs) + "\n")
    print(f"{len(pairs)} contrast pairs ...", flush=True)
    diffs, pos, neg = [], [], []
    for i, p in enumerate(pairs, 1):
        hp = completion_hiddens(model, tok, dev, p["system"], p["prompt"], p["positive"])
        hn = completion_hiddens(model, tok, dev, p["system"], p["prompt"], p["negative"])
        diffs.append((hp - hn).cpu()); pos.append(hp.cpu()); neg.append(hn.cpu())
        if i % 20 == 0:
            print(f"  {i}/{len(pairs)}", flush=True)
    diffs, pos, neg = torch.stack(diffs), torch.stack(pos), torch.stack(neg)      # [N, L, H]
    n_layers = diffs.shape[1]
    dirs, score, auc = [], [], []
    for l in range(n_layers):
        d = pca_direction(diffs[:, l])
        d = d / d.norm()
        pp, nn = pos[:, l] @ d, neg[:, l] @ d
        sep = float((pp.mean() - nn.mean()) / (0.5 * (pp.std() + nn.std()) + 1e-6))
        a = float((pp[:, None] > nn[None, :]).float().mean())
        dirs.append(d); score.append(sep); auc.append(a)
    dirs = torch.stack(dirs)                                                       # [L, H], row l = after layer l
    best = int(torch.tensor(score).argmax())
    print("per-layer separation (d'):", " ".join(f"{l}:{s:.1f}" for l, s in enumerate(score)), flush=True)
    print(f"frame lives around layer {best} (d'={score[best]:.2f}, AUC={auc[best]:.2f})", flush=True)

    # 2 + 3. projections and lens per condition
    conds = conditions(D, args.fill)
    res_c = {}
    for name, p in conds.items():
        text = render(tok, p, raw=False)
        ids = tok(text, add_special_tokens=False, return_tensors="pt")["input_ids"]
        cap = FullCapture(model)
        try:
            lg = model(input_ids=ids.to(dev), use_cache=False, logits_to_keep=1).logits[0, -1].float().cpu()
        finally:
            cap.remove()
        st = cap.stack()                                                            # [L+1, T, H]; row l+1 = after layer l
        proj = torch.einsum("lth,lh->lt", st[1:], dirs)                            # [L, T]
        spans = token_spans(tok, text, ids[0].tolist(), p)
        q = spans.get("question")
        m = margin_from_logits(lg, aid)
        lens = [margin_from_logits(lens_logits(model, st[r, -1]), aid)["M_sum"] for r in range(st.shape[0])]
        ans = proj[:, -1].tolist()
        final = ans[-1]
        half = next((l for l, v in enumerate(ans) if abs(final) > 0 and v / final >= 0.5 and (v > 0) == (final > 0)), None)
        # decisive = first row from which the lens stays on the final side of zero
        side = lens[-1] > 0
        decisive = next((r for r in range(len(lens)) if all((v > 0) == side for v in lens[r:])), None)
        res_c[name] = {"system": p["system"] is not None, "M": m["M_sum"], "greedy": greedy(model, tok, text),
                       "answer": "drive" if m["M_sum"] > 0 else "walk", "n_tokens": int(ids.shape[1]),
                       "tokens": [tok.decode(t) for t in ids[0].tolist()], "question_span": q,
                       "proj_answer_site": ans, "proj_question_mean": proj[:, q[0]:q[1]].mean(1).tolist() if q else None,
                       "proj_map": proj.tolist(), "lens_M": lens,
                       "formation_layer": half, "decisive_layer": decisive}
        print(f"  {name:16s} M={m['M_sum']:+.2f} {res_c[name]['answer']:5s} proj@answer final={final:+.2f} "
              f"formation L{half} decisive L{decisive}", flush=True)

    res = {"model": args.label or args.model, "quantize": args.quantize, "dtype": args.dtype, "directions_via": BRAINSCOPE,
           "n_layers": n_layers, "layer_note": "index l = output of decoder layer l (embedding row dropped)",
           "n_pairs": len(pairs), "rationales": RATIONALE, "separation_dprime": score, "auc": auc, "best_layer": best,
           "conditions": res_c, "seconds": round(time.time() - t0, 1)}
    (out / "frame.json").write_text(json.dumps(res, ensure_ascii=False))
    torch.save({"directions": dirs, "note": "unit direction per layer, row l = after layer l"}, out / "frame_dirs.pt")
    print(f"wrote {out / 'frame.json'} in {res['seconds']} s", flush=True)
    try:
        from plot_frame import plot
        plot(out)
    except Exception as e:
        print(f"plot_frame failed ({e}); run plot_frame.py later", flush=True)


if __name__ == "__main__":
    main()
