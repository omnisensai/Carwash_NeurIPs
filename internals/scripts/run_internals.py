#!/usr/bin/env python3
"""Baseline vs. substrate prompt: what changes inside a Llama.

One forward pass per prompt (teacher-forced prefill, no sampling), all
readouts at the position that predicts the first answer token:

  * final margin  M = log P(drive) - log P(walk)         (paper's M, in nats)
  * logit lens    M_l per layer (residual -> final RMSNorm -> lm_head)
  * DLA           direct logit attribution of every attention / MLP sublayer
                  and every attention head to the drive-minus-walk direction
                  (exact decomposition of M under the final RMSNorm)
  * attention     mass from the answer position onto each substrate line,
                  the question, the words "walk"/"drive"/"car", headers
  * residual diff cosine between baseline and substrate per layer
  * patching      baseline run with the substrate residual patched in at
                  the answer position, one layer at a time -> M per layer
  * ablations     leave-one-out and one-line-only substrate variants -> M
  * benchmarks    every prompts/*.txt -> M (reproduces the paper's table)

Model-agnostic over HF causal LMs with a pre-norm residual stream (Llama,
Qwen, Mistral, ...). Runs on one 16 GB card for 3B/8B (8B needs --quantize
4bit next to other GPU users) and on multi-GPU boxes for 70B (device_map
auto). Output: results/<name>/internals.json (+ resid_last.pt) — plot with
plot_internals.py, which needs no GPU.

    python run_internals.py --model unsloth/Llama-3.2-3B-Instruct --out results/llama-3b
    python run_internals.py --model unsloth/Llama-3.3-70B-Instruct --out results/llama-70b
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import time
from pathlib import Path

import torch

HERE = Path(__file__).resolve().parent
PROMPTS = HERE.parent.parent / "prompts"   # repo root; this file lives in internals/scripts/

DRIVE_VARIANTS = [" drive", "drive", " Drive", "Drive", " DRIVE", "DRIVE"]
WALK_VARIANTS = [" walk", "walk", " Walk", "Walk", " WALK", "WALK"]


# ----------------------------------------------------------------- prompts --

def parse_prompt(text: str) -> dict:
    """Split a prompts/*.txt file into system / user parts.

    Files with a 'System:' ... 'User:' scaffold become a system + user
    message; everything else is a bare user message."""
    # provenance lines appended to the files (e.g. "SHA-256: ...") are not prompt
    text = "\n".join(ln for ln in text.splitlines()
                     if not re.match(r"\s*(SHA-?256\s*:|[0-9a-f]{64}\s*$)", ln, re.I)).strip("\n")
    m = re.match(r"\s*System:\s*\n(.*?)\n\s*User:\s*\n(.*)\Z", text, re.S)
    sha = hashlib.sha256(text.encode()).hexdigest()   # matches the SHA-256 line the repo keeps
    if m:
        return {"system": m.group(1).strip("\n"), "user": m.group(2).strip("\n"), "sha256": sha}
    if "?" not in text:            # a bare system prompt (e.g. substrate_pro.txt):
        return {"system": text, "user": None, "sha256": sha}   # the caller supplies the question
    return {"system": None, "user": text, "sha256": sha}


def substrate_lines(system: str) -> list[str]:
    """The bullet lines of the substrate (the six constraints)."""
    return [ln for ln in system.splitlines() if ln.lstrip().startswith("-")]


def substrate_variants(system: str) -> dict[str, str]:
    """Leave-one-out and one-line-only versions of the substrate system
    prompt; headers ('User objective:', 'Action semantics:') are kept."""
    lines = system.splitlines()
    bullets = [i for i, ln in enumerate(lines) if ln.lstrip().startswith("-")]
    out = {}
    for k, i in enumerate(bullets, 1):
        out[f"loo_line{k}"] = "\n".join(ln for j, ln in enumerate(lines) if j != i)
    for k, i in enumerate(bullets, 1):
        keep = set(j for j in range(len(lines)) if j not in bullets) | {i}
        out[f"only_line{k}"] = "\n".join(ln for j, ln in enumerate(lines) if j in keep)
    out["headers_only"] = "\n".join(ln for j, ln in enumerate(lines) if j not in bullets)
    return out


def build_messages(p: dict) -> list[dict]:
    msgs = []
    if p["system"]:
        msgs.append({"role": "system", "content": p["system"]})
    msgs.append({"role": "user", "content": p["user"]})
    return msgs


def render(tok, p: dict, raw: bool) -> str:
    if raw:
        return ((p["system"] + "\n\n") if p["system"] else "") + p["user"]
    return tok.apply_chat_template(build_messages(p), tokenize=False,
                                   add_generation_prompt=True,
                                   enable_thinking=False)   # Qwen3-style hybrids: no <think> block; others ignore it


def token_spans(tok, text: str, ids: list[int], p: dict) -> dict[str, list[int]]:
    """Named token spans [start, end) found by locating substrings in the
    rendered prompt text and mapping char offsets to tokens."""
    enc = tok(text, add_special_tokens=False, return_offsets_mapping=True)
    assert enc["input_ids"] == ids, "offset tokenization diverged"
    offs = enc["offset_mapping"]

    def span(sub: str, start_from: int = 0) -> list[int] | None:
        c0 = text.find(sub, start_from)
        if c0 < 0:
            return None
        c1 = c0 + len(sub)
        toks = [i for i, (a, b) in enumerate(offs) if b > c0 and a < c1 and b > a]
        return [toks[0], toks[-1] + 1] if toks else None

    spans: dict[str, list[int]] = {}
    spans["bos"] = [0, 1]
    if p["system"]:
        for k, ln in enumerate(substrate_lines(p["system"]), 1):
            s = span(ln)
            if s:
                spans[f"line{k}"] = s
        for hdr in ("User objective:", "Action semantics:", "User goals:", "Definitions:", "Constraints:"):
            s = span(hdr)
            if s:
                spans["hdr_" + hdr.split()[0].lower().rstrip(":")] = s
        # 'Object = car' style definition lines (nine-line substrate of 19 Sep 2026)
        for k, ln in enumerate([ln for ln in p["system"].splitlines() if " = " in ln and not ln.lstrip().startswith("-")], 1):
            s = span(ln.strip())
            if s:
                spans[f"def{k}"] = s
    q_start = text.find(p["user"])
    q = p["user"].split("\n")[0]
    s = span(q, q_start)
    if s:
        spans["question"] = s
    s = span("Answer with exactly one word", q_start)
    if s:
        spans["answer_instr"] = s
    for w in ("walk", "drive", "car wash", "50 metres"):
        s = span(w, q_start)
        if s:
            spans["q_" + w.replace(" ", "_")] = s
    # the assistant header = everything after the user content
    u_end = q_start + len(p["user"])
    toks = [i for i, (a, b) in enumerate(offs) if a >= u_end and b > a]
    if toks:
        spans["asst_header"] = [toks[0], len(ids)]
    spans["last"] = [len(ids) - 1, len(ids)]
    return spans


# ------------------------------------------------------------------- model --

def load(model_id: str, quantize: str | None, device: str, dtype: str | None = None):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(model_id)
    dt = getattr(torch, dtype) if dtype else (torch.bfloat16 if device == "cuda" else torch.float32)
    kw = {"dtype": dt,
          "attn_implementation": "eager"}   # eager: attentions are materialised
    if quantize:
        from transformers import BitsAndBytesConfig
        kw["quantization_config"] = (
            BitsAndBytesConfig(load_in_8bit=True) if quantize == "8bit" else
            BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16,
                               bnb_4bit_quant_type="nf4"))
        # one card: force everything onto it (accelerate's 'auto' spills to CPU
        # when other processes hold part of the card); many cards: spread
        kw["device_map"] = "auto" if torch.cuda.device_count() > 1 else {"": 0}
    elif device == "cuda" and torch.cuda.device_count() > 1:
        kw["device_map"] = "auto"
    model = AutoModelForCausalLM.from_pretrained(model_id, **kw)
    if "device_map" not in kw:
        model = model.to(device)
    return tok, model.eval()


def core(model):
    for attr in ("model", "transformer"):
        c = getattr(model, attr, None)
        if c is not None:
            return c
    raise RuntimeError("no decoder core found")


def layers_of(model):
    c = core(model)
    for attr in ("layers", "h", "blocks"):
        if hasattr(c, attr):
            return getattr(c, attr)
    raise RuntimeError("no decoder layers found")


def final_norm(model):
    c = core(model)
    for attr in ("norm", "ln_f", "final_layernorm"):
        if hasattr(c, attr):
            return getattr(c, attr)
    raise RuntimeError("no final norm found")


def embed(model):
    return model.get_input_embeddings()


def out_tensor(out):
    return out[0] if isinstance(out, tuple) else out


class Capture:
    """Forward hooks capturing, at the LAST position: embedding output, each
    layer's residual output, each attention / MLP sublayer output, and each
    head's pre-o_proj input (for per-head DLA)."""

    def __init__(self, model):
        self.model = model
        self.handles = []
        self.reset()
        L = layers_of(model)
        self.handles.append(embed(model).register_forward_hook(self._emb))
        for i, layer in enumerate(L):
            self.handles.append(layer.register_forward_hook(self._layer(i)))
            self.handles.append(layer.self_attn.register_forward_hook(self._sub("attn", i)))
            self.handles.append(layer.mlp.register_forward_hook(self._sub("mlp", i)))
            self.handles.append(layer.self_attn.o_proj.register_forward_pre_hook(self._heads(i)))

    def reset(self):
        self.emb = None
        self.resid: dict[int, torch.Tensor] = {}
        self.attn: dict[int, torch.Tensor] = {}
        self.mlp: dict[int, torch.Tensor] = {}
        self.head_in: dict[int, torch.Tensor] = {}

    def _emb(self, _m, _i, out):
        self.emb = out[0, -1].detach().float().cpu()

    def _layer(self, i):
        def hook(_m, _i, out):
            self.resid[i] = out_tensor(out)[0, -1].detach().float().cpu()
        return hook

    def _sub(self, kind, i):
        def hook(_m, _i, out):
            getattr(self, kind)[i] = out_tensor(out)[0, -1].detach().float().cpu()
        return hook

    def _heads(self, i):
        def hook(_m, inp):
            self.head_in[i] = inp[0][0, -1].detach().float().cpu()
        return hook

    def remove(self):
        for h in self.handles:
            h.remove()


class Patch:
    """Replace the residual at (layer, last position) during one forward."""

    def __init__(self, model, layer: int, vec: torch.Tensor):
        target = layers_of(model)[layer]

        def hook(_m, _i, out):
            t = out_tensor(out)
            t[0, -1, :] = vec.to(t.dtype).to(t.device)
        self.h = target.register_forward_hook(hook)

    def remove(self):
        self.h.remove()


# ---------------------------------------------------------------- readouts --

def dequant_weight(lin) -> torch.Tensor:
    """fp32 CPU copy of a Linear's weight, also for bitsandbytes 4/8-bit."""
    w = lin.weight
    if w.dtype in (torch.bfloat16, torch.float16, torch.float32):
        return w.detach().float().cpu()
    import bitsandbytes.functional as F
    if w.dtype == torch.uint8:                                  # nf4
        return F.dequantize_4bit(w.data, w.quant_state).float().cpu()
    if w.dtype == torch.int8:                                   # LLM.int8 row-wise
        return (w.data.float() * w.SCB.float().view(-1, 1) / 127.0).cpu()
    raise RuntimeError(f"unknown quantized weight dtype {w.dtype}")


def rmsnorm_fp32(x: torch.Tensor, norm) -> torch.Tensor:
    w = norm.weight.detach().float().cpu()
    eps = getattr(norm, "variance_epsilon", getattr(norm, "eps", 1e-6))
    return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * w


def lens_logits(model, x: torch.Tensor) -> torch.Tensor:
    """Final norm + lm_head of one residual vector, fp32 logits on CPU."""
    head = model.get_output_embeddings()
    W = head.weight
    z = rmsnorm_fp32(x, final_norm(model)).to(W.device).to(W.dtype)
    return (z @ W.T).float().cpu()


def margin_from_logits(lg: torch.Tensor, ids: dict) -> dict:
    lp = torch.log_softmax(lg, -1)
    pd = lp[ids["drive"]].exp().sum()
    pw = lp[ids["walk"]].exp().sum()
    d_best = ids["drive"][int(lp[ids["drive"]].argmax())]
    w_best = ids["walk"][int(lp[ids["walk"]].argmax())]
    ranks = lp.argsort(descending=True)
    rank_of = {int(t): r for r, t in enumerate(ranks[:2000].tolist())}
    return {
        "M_sum": float(pd.log() - pw.log()),          # sum over surface variants
        "M_first": float(lp[d_best] - lp[w_best]),    # best drive vs best walk token
        "p_drive": float(pd), "p_walk": float(pw),
        "drive_token": d_best, "walk_token": w_best,
        "rank_drive": rank_of.get(d_best, 2000), "rank_walk": rank_of.get(w_best, 2000),
        "argmax": int(lg.argmax()),
    }


def answer_ids(tok) -> dict:
    def ids(variants):
        out = []
        for v in variants:
            t = tok.encode(v, add_special_tokens=False)
            if len(t) == 1 and t[0] not in out:
                out.append(t[0])
        return out
    return {"drive": ids(DRIVE_VARIANTS), "walk": ids(WALK_VARIANTS)}


@torch.no_grad()
def forward(model, tok, text: str, cap: Capture | None, want_attn: bool):
    ids = tok(text, add_special_tokens=False, return_tensors="pt")["input_ids"]
    dev = embed(model).weight.device
    if cap:
        cap.reset()
    out = model(input_ids=ids.to(dev), output_attentions=want_attn, use_cache=False,
                logits_to_keep=1)          # lm_head only at the answer position (memory)
    attn = None
    if want_attn:
        # [L, H, T] rows of the last query position
        attn = torch.stack([a[0, :, -1, :].float().cpu() for a in out.attentions])
    return ids[0].tolist(), out.logits[0, -1].float().cpu(), attn


@torch.no_grad()
def greedy(model, tok, text: str, n: int = 4) -> str:
    ids = tok(text, add_special_tokens=False, return_tensors="pt")["input_ids"]
    dev = embed(model).weight.device
    g = model.generate(ids.to(dev), max_new_tokens=n, do_sample=False,
                       pad_token_id=tok.eos_token_id)
    return tok.decode(g[0, ids.shape[1]:])


@torch.no_grad()
def decision_margin(model, tok, text: str, aid: dict, steps: int = 6) -> dict:
    """M at the DECISION position: greedy-decode a few tokens and read the
    margin at the first step whose argmax is a drive/walk surface form. With
    the chat template Llama answers with a bare word, so this is step 0 and
    equals the final margin; on raw text it opens with ' **' or similar and
    the first-token margin is not the decision."""
    ids = tok(text, add_special_tokens=False, return_tensors="pt")["input_ids"]
    dev = embed(model).weight.device
    ids = ids.to(dev)
    answer = set(aid["drive"]) | set(aid["walk"])
    past = None
    cur = ids
    out_toks = []
    for step in range(steps):
        out = model(input_ids=cur, past_key_values=past, use_cache=True, logits_to_keep=1)
        past = out.past_key_values
        lg = out.logits[0, -1].float().cpu()
        nxt = int(lg.argmax())
        out_toks.append(nxt)
        if nxt in answer:
            m = margin_from_logits(lg, aid)
            return {"step": step, "M_sum": m["M_sum"], "p_drive": m["p_drive"],
                    "p_walk": m["p_walk"], "prefix": tok.decode(out_toks[:-1]),
                    "token": tok.decode(nxt)}
        cur = torch.tensor([[nxt]], device=dev)
    return {"step": None, "M_sum": None, "prefix": tok.decode(out_toks), "token": None}


def analyse_prompt(model, tok, name: str, p: dict, raw: bool, aid: dict,
                   cap: Capture, u_dir: torch.Tensor | None = None,
                   u_tokens: tuple | None = None) -> dict:
    """Everything for one prompt. u_dir: drive-minus-walk unembedding row
    (fp32, CPU); when None it is derived from this prompt's best tokens."""
    text = render(tok, p, raw)
    gen = greedy(model, tok, text)      # BEFORE the capture pass: generate() fires the hooks too
    ids, lg, attn = forward(model, tok, text, cap, want_attn=True)
    spans = token_spans(tok, text, ids, p)
    final = margin_from_logits(lg, aid)
    final["top5"] = [[tok.decode(int(t)), round(float(pp), 4)]
                     for pp, t in zip(*torch.softmax(lg, -1).topk(5))]
    final["greedy"] = gen
    final["decision"] = decision_margin(model, tok, text, aid)
    n_layers = len(cap.resid)

    # --- logit lens over the residual stream (emb = row 0, layer i = row i+1)
    stack = torch.stack([cap.emb] + [cap.resid[i] for i in range(n_layers)])
    lens = {"M_sum": [], "M_first": [], "p_drive": [], "p_walk": [],
            "rank_drive": [], "rank_walk": [], "top1": []}
    for r in range(stack.shape[0]):
        l_r = lens_logits(model, stack[r])
        m = margin_from_logits(l_r, aid)
        for k in ("M_sum", "M_first", "p_drive", "p_walk", "rank_drive", "rank_walk"):
            lens[k].append(m[k])
        lens["top1"].append(tok.decode(m["argmax"]))
    # sanity: the last lens row must reproduce the model's own logits
    lens["final_row_matches_model"] = bool(
        abs(lens["M_first"][-1] - final["M_first"]) < 0.05)

    # --- direct logit attribution under the final RMSNorm (exact, linear
    #     given the final rms of the residual)
    head = model.get_output_embeddings().weight
    d_tok, w_tok = final["drive_token"], final["walk_token"]
    if u_dir is None:
        u_dir = (head[d_tok].float() - head[w_tok].float()).cpu()
        u_tokens = (d_tok, w_tok)
    norm = final_norm(model)
    g = norm.weight.detach().float().cpu()
    eps = getattr(norm, "variance_epsilon", getattr(norm, "eps", 1e-6))
    x_final = cap.resid[n_layers - 1]
    rms = float(torch.sqrt(x_final.pow(2).mean() + eps))
    v = (g * u_dir) / rms                      # DLA(c) = c . v
    dla = {"emb": float(cap.emb @ v),
           "attn": [float(cap.attn[i] @ v) for i in range(n_layers)],
           "mlp": [float(cap.mlp[i] @ v) for i in range(n_layers)]}
    dla["total"] = dla["emb"] + sum(dla["attn"]) + sum(dla["mlp"])
    # the total must equal the model's own logit difference for the SAME token
    # pair u_dir was built from (the shared pair may differ from this prompt's
    # own best surface forms, e.g. 'walk' vs 'Walk')
    lp = torch.log_softmax(lg, -1)
    dla["M_first_check"] = float(lp[d_tok] - lp[w_tok]) if u_dir is None else \
        float(lp[u_tokens[0]] - lp[u_tokens[1]])
    dla["tokens"] = [tok.decode(d_tok), tok.decode(w_tok)] if u_dir is None else \
        [tok.decode(u_tokens[0]), tok.decode(u_tokens[1])]
    # per head: o_proj(x) = sum_h W_o[:, h] x_h  ->  DLA_h = x_h . (W_o[:, h]^T v)
    L = layers_of(model)
    n_heads = model.config.num_attention_heads
    heads = []
    for i in range(n_layers):
        Wo = dequant_weight(L[i].self_attn.o_proj)
        wv = (Wo.T.cpu() @ v).view(n_heads, -1)               # [H, head_dim]
        xh = cap.head_in[i].view(n_heads, -1)
        heads.append([float((xh[h] * wv[h]).sum()) for h in range(n_heads)])
    dla["heads"] = heads

    # --- attention from the answer position onto named spans
    attn_mass = {}
    for s, (a, b) in spans.items():
        m = attn[:, :, a:b].sum(-1)            # [L, H]
        attn_mass[s] = {"mean": m.mean(1).tolist(), "heads": m.tolist()}
    # entropy of each head's row (how spread the attention is)
    ent = -(attn.clamp_min(1e-12) * attn.clamp_min(1e-12).log()).sum(-1)

    return {
        "text": text, "n_tokens": len(ids), "tokens": [tok.decode(t) for t in ids],
        "spans": spans, "final": final, "lens": lens, "dla": dla,
        "attn_mass": attn_mass, "attn_entropy_mean": ent.mean(1).tolist(),
        "_stack": stack, "_u": u_dir, "_u_tokens": u_tokens, "_ids": ids,
    }


# -------------------------------------------------------------------- main --

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="HF id or local snapshot path")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--quantize", choices=["4bit", "8bit"], default=None)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--dtype", default=None, choices=["bfloat16", "float16", "float32"],
                    help="weights dtype (default bf16 on cuda, fp32 on cpu)")
    ap.add_argument("--raw", action="store_true",
                    help="feed the prompt files verbatim instead of the chat template")
    ap.add_argument("--no-patching", action="store_true")
    ap.add_argument("--no-ablations", action="store_true")
    ap.add_argument("--no-benchmarks", action="store_true")
    ap.add_argument("--label", default=None, help="model label stored in the json")
    ap.add_argument("--substrate", default="substrate.txt",
                    help="which prompts/ file is the substrate (default substrate.txt)")
    ap.add_argument("--baseline", default="baseline.txt")
    ap.add_argument("--keep-substrate-question", action="store_true",
                    help="keep the question embedded in the substrate file instead of the baseline's")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    print(f"loading {args.model} ({args.quantize or args.dtype or 'default dtype'}, {args.device}) ...", flush=True)
    tok, model = load(args.model, args.quantize, args.device, args.dtype)
    aid = answer_ids(tok)
    print("answer token ids:", aid, flush=True)
    cap = Capture(model)

    base_p = parse_prompt((PROMPTS / args.baseline).read_text())
    sub_p = parse_prompt((PROMPTS / args.substrate).read_text())
    if not sub_p["system"]:
        sys.exit(f"{args.substrate} has no 'System:' block — nothing to ablate")
    if sub_p["user"] is None:
        sub_p["user"] = base_p["user"]       # bare system file + baseline question
    elif sub_p["user"] != base_p["user"] and not args.keep_substrate_question:
        print(f"note: {args.substrate} embeds its own question, which differs from {args.baseline}; "
              "using the baseline question (pass --keep-substrate-question to keep the file's)", flush=True)
        sub_p["user"] = base_p["user"]

    print("baseline ...", flush=True)
    base = analyse_prompt(model, tok, "baseline", base_p, args.raw, aid, cap)
    # one shared drive-minus-walk direction for both prompts: the tokens the
    # substrate run prefers (they are the same surface form in practice)
    print("substrate ...", flush=True)
    sub = analyse_prompt(model, tok, "substrate", sub_p, args.raw, aid, cap)
    u = sub["_u"]
    if not torch.equal(u, base["_u"]):
        print("note: baseline picked different answer surface forms; re-attributing "
              "baseline with the substrate's drive/walk tokens", flush=True)
        base = analyse_prompt(model, tok, "baseline", base_p, args.raw, aid, cap, u_dir=u,
                              u_tokens=sub["_u_tokens"])

    n_layers = sub["_stack"].shape[0] - 1
    res = {
        "model": args.label or args.model, "quantize": args.quantize,
        "device": args.device, "dtype": args.dtype,
        "baseline_file": args.baseline, "substrate_file": args.substrate,
        "baseline_sha256": base_p["sha256"], "substrate_sha256": sub_p["sha256"],
        "question": base_p["user"],
        "raw_prompts": args.raw, "n_layers": n_layers,
        "n_heads": model.config.num_attention_heads,
        "answer_token_ids": aid,
        "drive_token": [sub["final"]["drive_token"], tok.decode(sub["final"]["drive_token"])],
        "walk_token": [sub["final"]["walk_token"], tok.decode(sub["final"]["walk_token"])],
        "prompts": {},
    }
    for name, r in (("baseline", base), ("substrate", sub)):
        res["prompts"][name] = {k: v for k, v in r.items() if not k.startswith("_")}
        print(f"  {name:10s} M_sum={r['final']['M_sum']:+.3f}  M_first={r['final']['M_first']:+.3f} "
              f"p(drive)={r['final']['p_drive']:.3f} p(walk)={r['final']['p_walk']:.3f} "
              f"greedy={r['final']['greedy']!r}", flush=True)

    # --- residual diff per layer (rows: emb, layer0..)
    sb, ss = base["_stack"], sub["_stack"]
    diff = ss - sb
    cos = torch.nn.functional.cosine_similarity(sb, ss, dim=1)
    res["diff"] = {
        "cos_resid": cos.tolist(),
        "norm_base": sb.norm(dim=1).tolist(), "norm_sub": ss.norm(dim=1).tolist(),
        "norm_diff": diff.norm(dim=1).tolist(),
        "cos_diff_u": torch.nn.functional.cosine_similarity(
            diff, u.unsqueeze(0).expand_as(diff), dim=1).tolist(),
    }
    torch.save({"baseline": sb, "substrate": ss, "u_drive_minus_walk": u,
                "rows": ["emb"] + [f"layer{i}" for i in range(n_layers)]},
               out / "resid_last.pt")

    # --- activation patching: baseline run, substrate residual at the answer
    #     position patched in at layer l -> M
    if not args.no_patching:
        print("patching ...", flush=True)
        base_text = render(tok, base_p, args.raw)
        pm = []
        for l in range(n_layers):
            ph = Patch(model, l, ss[l + 1])
            try:
                _, lg, _ = forward(model, tok, base_text, None, want_attn=False)
            finally:
                ph.remove()
            pm.append(margin_from_logits(lg, aid)["M_sum"])
            print(f"  patch L{l:02d}: M_sum={pm[-1]:+.3f}", flush=True)
        res["patching"] = {"M_sum": pm, "note": "baseline prompt, substrate residual "
                           "patched at the answer position after layer l"}

    # --- substrate line ablations
    if not args.no_ablations:
        print("ablations ...", flush=True)
        abl = {}
        for vname, sysm in substrate_variants(sub_p["system"]).items():
            text = render(tok, {"system": sysm, "user": sub_p["user"]}, args.raw)
            _, lg, _ = forward(model, tok, text, None, want_attn=False)
            abl[vname] = margin_from_logits(lg, aid)["M_sum"]
            print(f"  {vname:14s} M_sum={abl[vname]:+.3f}", flush=True)
        # bare-system control: substrate lines but no chat scaffold difference
        res["ablations"] = abl
        res["substrate_lines"] = substrate_lines(sub_p["system"])

    # --- every benchmark prompt
    if not args.no_benchmarks:
        print("benchmarks ...", flush=True)
        bm = {}
        # anti-test control; optional, skipped when the prompt file is absent
        _lib = PROMPTS / "benchmark_library.txt"
        library_p = parse_prompt(_lib.read_text()) if _lib.exists() else None
        for f in sorted(PROMPTS.glob("*.txt")):
            p = parse_prompt(f.read_text())
            if p["user"] is None or (f.stem.startswith("substrate") and not args.keep_substrate_question):
                p["user"] = base_p["user"]
            text = render(tok, p, args.raw)
            _, lg, _ = forward(model, tok, text, None, want_attn=False)
            m = margin_from_logits(lg, aid)
            dm = decision_margin(model, tok, text, aid)
            bm[f.stem] = {"M_sum": m["M_sum"], "M_first": m["M_first"],
                          "p_drive": m["p_drive"], "p_walk": m["p_walk"],
                          "argmax": tok.decode(m["argmax"]),
                          "greedy": greedy(model, tok, text), "decision": dm}
            print(f"  {f.stem:24s} M_sum={m['M_sum']:+.3f} argmax={bm[f.stem]['argmax']!r} "
                  f"greedy={bm[f.stem]['greedy']!r}  decision@{dm['step']}: "
                  f"M={dm['M_sum'] if dm['M_sum'] is None else round(dm['M_sum'], 3)}", flush=True)
        res["benchmarks"] = bm
        # anti-test: each substrate system prompt with the library question (expected: walk)
        anti = {}
        for f in (sorted(PROMPTS.glob("substrate*.txt")) if library_p else []):
            p = parse_prompt(f.read_text())
            if not p["system"]:
                continue
            text = render(tok, {"system": p["system"], "user": library_p["user"]}, args.raw)
            _, lg, _ = forward(model, tok, text, None, want_attn=False)
            m = margin_from_logits(lg, aid)
            anti[f.stem + "+library"] = {"M_sum": m["M_sum"], "argmax": tok.decode(m["argmax"]),
                                         "greedy": greedy(model, tok, text),
                                         "decision": decision_margin(model, tok, text, aid)}
            print(f"  {f.stem + '+library':24s} M_sum={m['M_sum']:+.3f} greedy={anti[f.stem + '+library']['greedy']!r}", flush=True)
        res["anti_test"] = anti

    res["seconds"] = round(time.time() - t0, 1)
    res["torch"] = torch.__version__
    import transformers
    res["transformers"] = transformers.__version__
    (out / "internals.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    cap.remove()
    print(f"wrote {out / 'internals.json'} in {res['seconds']} s", flush=True)


if __name__ == "__main__":
    with torch.no_grad():
        main()
