#!/usr/bin/env python3
"""Put the ten open-weight models through the fleet's nine conditions.

Why this exists: `runs/` holds 17 models sampled through hosted APIs, and
`internals/` holds ten open-weight models measured by logit margin. The two
sets overlap only in name -- the three Llamas in `runs/` were sampled through
OpenRouter across shifting backends, and the seven Qwens appear in `runs/` not
at all. This script samples all ten locally, under one protocol, on prompts
byte-identical to the published sweep, so every model with a mechanistic row
gets a behavioural one measured the same way.

The answer is the emitted word, counted over ten samples -- what the published
fleet reports -- not the margin, which is what `internals/` already measures.

Five of the ten are not served by any hosted API, so the default backend is
local weights via transformers. The `--backend openrouter` path exists for the
ones that are hosted, as a check that local sampling and a served endpoint
agree.

Prompts are never modified. Every condition's text is rebuilt from `prompts/`
and its sha256 is checked against the sha the published `runs/*/ *.jsonl` rows
recorded, so a row produced here is comparable to the 17-model fleet by
construction rather than by assertion. `--dry-run` performs that check alone
and needs neither torch nor a key.

The output schema is the published one, plus `backend`, `top_p`, `seed`,
`torch`, `transformers`, `dtype` and `device`, which the API rows could not
carry and a local run has no excuse to omit.

Usage
-----
  # verify the prompts match the published fleet; nothing is loaded
  python runs/run_qwen_fleet.py --dry-run

  # the whole Qwen sweep, local weights, 10 samples per cell
  python runs/run_qwen_fleet.py --models all --n 10 --outdir runs/qwen

  # one model, one condition
  python runs/run_qwen_fleet.py --models qwen3-8b --conditions baseline,substrate --n 10

  # cross-check a hosted Qwen against the local run
  OPENROUTER_API_KEY=... python runs/run_qwen_fleet.py \
      --models qwen3-8b --backend openrouter --n 10
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent   # this file lives in behavioural/scripts/
PROMPTS = REPO / "prompts"

# Provenance lines appended to some prompt files; not part of the prompt.
SHA_LINE = re.compile(r"^\s*(SHA-?256\s*:.*|[0-9a-f]{64})\s*$", re.M)
# Most prompt files end with the bare instruction and leave the options
# implicit. The published rows show the original runner completing it, so a
# re-run has to complete it the same way or the hashes will not match.
BARE_CONSTRAINT = re.compile(r"^Answer with exactly one word:\s*$", re.M)
CHOICES = "walk or drive"

DRIVE = (" drive", "drive", " Drive", "Drive", " DRIVE", "DRIVE")
WALK = (" walk", "walk", " Walk", "Walk", " WALK", "WALK")

# The ten open-weight models measured in internals/RESULTS.md, by the
# checkpoint the internals.json of each result folder names. `openrouter` is
# None where no hosted endpoint serves that checkpoint.
#
# `gb` is the bf16 weight footprint, used only to warn before a run that will
# not fit: Llama-3.3-70B needs ~140 GB and will not load on one card.
#
# Checked against the OpenRouter catalogue on 25 Sep 2026 (`check_openrouter.sh`):
# two of the seven checkpoints are served, and both endpoints declare exactly
# the checkpoint internals.json names. Nothing in the catalogue is a near miss
# for the other five, so there is no lookalike to mistake for them.
MODELS: dict[str, dict] = {
    "llama-3.2-3b":  dict(hf="unsloth/Llama-3.2-3B-Instruct", label="Llama 3.2-3B",  gb=6,
                         openrouter="meta-llama/llama-3.2-3b-instruct"),
    "llama-3.1-8b":  dict(hf="unsloth/Llama-3.1-8B-Instruct", label="Llama 3.1-8B",  gb=16,
                         openrouter="meta-llama/llama-3.1-8b-instruct"),
    "llama-3.3-70b": dict(hf="unsloth/Llama-3.3-70B-Instruct", label="Llama 3.3-70B", gb=141,
                         openrouter="meta-llama/llama-3.3-70b-instruct"),
    "qwen2.5-0.5b":  dict(hf="Qwen/Qwen2.5-0.5B-Instruct",   label="Qwen2.5-0.5B",   gb=1,  openrouter=None),
    "qwen2.5-1.5b":  dict(hf="Qwen/Qwen2.5-1.5B-Instruct",   label="Qwen2.5-1.5B",   gb=3, openrouter=None),
    "qwen2.5-3b":    dict(hf="Qwen/Qwen2.5-3B-Instruct",     label="Qwen2.5-3B",     gb=6, openrouter=None),
    "qwen2.5-7b":    dict(hf="Qwen/Qwen2.5-7B-Instruct",     label="Qwen2.5-7B",     gb=15, openrouter="qwen/qwen-2.5-7b-instruct"),
    "qwen3-0.6b":    dict(hf="Qwen/Qwen3-0.6B",              label="Qwen3-0.6B",     gb=2, openrouter=None),
    "qwen3-4b-2507": dict(hf="Qwen/Qwen3-4B-Instruct-2507",  label="Qwen3-4B-2507",  gb=8, openrouter=None),
    "qwen3-8b":      dict(hf="Qwen/Qwen3-8B",                label="Qwen3-8B",       gb=17, openrouter="qwen/qwen3-8b"),
}

# The nine conditions of the published fleet, with the `intervention` and
# `intervention_description` strings those rows carry, so summary code that
# groups by intervention sees one fleet and not two.
#
# `role` says where the prompt file goes. The substrate condition is the one
# that differs: the fleet sent substrate.txt as the *system* message with the
# unmodified baseline question as the user message, which is why its
# prompt_sha256 equals baseline's and its system_sha256 is the substrate's.
# `sha` / `sys_sha` are read back from the published rows.
CONDITIONS: dict[str, dict] = {
    "baseline": dict(
        file="baseline.txt", role="user", max_tokens=80,
        intervention="baseline", description="no intervention",
        sha="f9ac23fbd6f7b7cae272af65ba9b9066ccb735c61a96c0307f5bd76d365b2a1a",
        sys_sha="NONE"),
    "substrate": dict(
        file="substrate.txt", role="system", max_tokens=80,
        intervention="substrate_llama_v3",
        description="substrate_llama_v3 (Llama-targeted variant)",
        sha="f9ac23fbd6f7b7cae272af65ba9b9066ccb735c61a96c0307f5bd76d365b2a1a",
        sys_sha="5b56feb32d74ce92484ddd7a2bb7df3396d4bbdfd1002bb976677f36dc0d6754"),
    "expert": dict(
        file="benchmark_expert.txt", role="user", max_tokens=80,
        intervention="expert_role", description="expert role framing",
        sha="54b1a7d6a60ec808166817d436f4de9519d294ddd9319ea1532acbf6eaa192b0",
        sys_sha="NONE"),
    "urgency": dict(
        file="benchmark_urgency.txt", role="user", max_tokens=80,
        intervention="objective_emphasis", description="objective emphasis (shouty)",
        sha="eb7094b24182b28c4c77613b528b723acedd4db666d17146de6f4fb0d16b8103",
        sys_sha="NONE"),
    "cot": dict(
        file="benchmark_CoT.txt", role="user", max_tokens=500,
        intervention="cot", description="chain of thought",
        sha="5ad509a4a1d18deb7a838dabea25776ce39be9be2bd72479005607566027b78b",
        sys_sha="NONE"),
    "hallucination": dict(
        file="benchmark_hallucination.txt", role="user", max_tokens=80,
        intervention="anti_hallucination", description="anti-hallucination instruction",
        sha="7dcc78f45a30ee9b7f82ddc3abd1ec955e2c46c1d293d569768846e677d8c7c2",
        sys_sha="NONE"),
    "threat": dict(
        file="benchmark_threat.txt", role="user", max_tokens=80,
        intervention="threat", description="threat",
        sha="d853a7fe5ff079a99415ae67e58fb0cda508e06d9e3d22317700e0bf62cb8d85",
        sys_sha="NONE"),
    "correct": dict(
        file="benchmark_correct.txt", role="user", max_tokens=80,
        intervention="correct_answer",
        description="correct answer explicitly stated in prompt",
        sha="0b8320cfb2df8522a27549d5b2a450d816737d4cd0e03cff07b5eabc9db07d9b",
        sys_sha="NONE"),
    "encourage": dict(
        file="benchmark_encourage.txt", role="user", max_tokens=80,
        intervention="encouragement", description="encouragement",
        sha="05720293ce0c1bf00352886dd1eb767975801d9e34a65c0aeb0f54384b13b47b",
        sys_sha="NONE"),
    "nomistakes": dict(
        file="benchmark_nomistakes.txt", role="user", max_tokens=80,
        intervention="error_avoidance", description="error avoidance instruction",
        sha="be71e36ba4755ce5c2d035435b5d09323fc1e9ed123b355b03bbb592a4efe8ad",
        sys_sha="NONE"),
}

# prompts/benchmark_goaloriented.txt exists but was not part of the 17-model
# sweep, so it has no published sha to check against and is not run here.

PUBLISHED = list(CONDITIONS)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build(cond: str) -> tuple[str | None, str]:
    """(system, user) for one condition, rebuilt from prompts/.

    The user text is the file with the provenance line dropped, the bare
    one-word instruction completed, and trailing whitespace stripped -- the
    three steps that reproduce the published `user` field byte for byte. The
    substrate is passed through untouched, trailing newline included, because
    that is what its recorded system_sha256 covers.
    """
    c = CONDITIONS[cond]
    raw = (PROMPTS / c["file"]).read_text(encoding="utf-8")
    if c["role"] == "system":
        user = SHA_LINE.sub("", (PROMPTS / "baseline.txt").read_text(encoding="utf-8")).rstrip()
        return raw, BARE_CONSTRAINT.sub(f"Answer with exactly one word: {CHOICES}", user)
    user = SHA_LINE.sub("", raw).rstrip()
    return None, BARE_CONSTRAINT.sub(f"Answer with exactly one word: {CHOICES}", user)


def check_prompts(conds: list[str]) -> list[str]:
    """Compare every rebuilt condition with the sha the published rows carry."""
    bad = []
    for cond in conds:
        c = CONDITIONS[cond]
        system, user = build(cond)
        got_u, want_u = sha256(user), c["sha"]
        got_s = sha256(system) if system is not None else "NONE"
        ok_u, ok_s = got_u == want_u, got_s == c["sys_sha"]
        mark = "ok " if (ok_u and ok_s) else "MISMATCH"
        print(f"  {mark} {cond:14s} user {got_u[:8]}"
              f"{'' if ok_u else ' != ' + want_u[:8]}"
              f"   system {got_s[:8]}{'' if ok_s else ' != ' + c['sys_sha'][:8]}")
        if not (ok_u and ok_s):
            bad.append(cond)
    return bad


def decide(text: str) -> str | None:
    """First answer word the reply commits to, or None if it commits to none.

    The fleet's rows are one word because the prompt asks for one word; CoT
    replies are prose that ends in one. Taking the first occurrence of either
    family is the same rule the published summaries used.
    """
    m = re.search(r"\b(walk|drive)\w*\b", text, re.I)
    return m.group(1).lower() if m else None


# --------------------------------------------------------------------------
# backends
# --------------------------------------------------------------------------

def vram_gb() -> float | None:
    """Total memory of card 0 in GB, or None when there is no CUDA device."""
    try:
        import torch
        if not torch.cuda.is_available():
            return None
        return torch.cuda.get_device_properties(0).total_memory / 1024 ** 3
    except Exception:      # noqa: BLE001 - a cpu-only box has nothing to report
        return None


def load_local(hf_id: str, dtype: str, device: str):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(hf_id)
    model = AutoModelForCausalLM.from_pretrained(
        hf_id, dtype=getattr(torch, dtype),
        device_map={"": 0} if device == "cuda" else None)
    if device != "cuda":
        model.to(device)
    model.eval()
    return tok, model


def gen_local(tok, model, system: str | None, user: str, max_tokens: int,
              temperature: float, top_p: float, seed: int, device: str):
    """One sampled continuation. Returns (text, raw_dict).

    `enable_thinking=False` matches internals/run_internals.py: Qwen3 templates
    otherwise open a <think> block, and the answer word then lands hundreds of
    tokens later, which is a different measurement from the fleet's.
    """
    import torch

    msgs = ([{"role": "system", "content": system}] if system else []) \
        + [{"role": "user", "content": user}]
    try:
        text = tok.apply_chat_template(msgs, tokenize=False,
                                       add_generation_prompt=True,
                                       enable_thinking=False)
    except TypeError:        # templates that do not take the kwarg
        text = tok.apply_chat_template(msgs, tokenize=False,
                                       add_generation_prompt=True)
    enc = tok(text, return_tensors="pt", add_special_tokens=False).to(model.device)
    torch.manual_seed(seed)
    with torch.no_grad():
        out = model.generate(**enc, do_sample=temperature > 0,
                             temperature=temperature, top_p=top_p, top_k=0,
                             max_new_tokens=max_tokens,
                             pad_token_id=tok.pad_token_id or tok.eos_token_id)
    new = out[0][enc["input_ids"].shape[1]:]
    reply = tok.decode(new, skip_special_tokens=True)
    return reply, {"rendered_prompt": text, "rendered_sha256": sha256(text),
                   "prompt_tokens": int(enc["input_ids"].shape[1]),
                   "completion_tokens": int(new.shape[0]), "seed": seed}


def gen_openrouter(slug: str, system: str | None, user: str, max_tokens: int,
                   temperature: float, top_p: float):
    from openai import OpenAI

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set")
    client = OpenAI(api_key=key, base_url="https://openrouter.ai/api/v1")
    msgs = ([{"role": "system", "content": system}] if system else []) \
        + [{"role": "user", "content": user}]
    resp = client.chat.completions.create(model=slug, messages=msgs,
                                          max_tokens=max_tokens,
                                          temperature=temperature, top_p=top_p)
    raw = resp.model_dump()
    return (resp.choices[0].message.content or ""), raw


# --------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Run the seven Qwen models through the fleet's nine conditions.")
    ap.add_argument("--models", default="all",
                    help="comma-separated keys, 'all' (the ten), 'qwens', or 'llamas'. "
                         f"Keys: {', '.join(MODELS)}")
    ap.add_argument("--conditions", default="all",
                    help=f"comma-separated or 'all'. Keys: {', '.join(CONDITIONS)}")
    ap.add_argument("--backend", choices=("local", "openrouter"), default="local")
    ap.add_argument("--n", type=int, default=10, help="samples per model per condition")
    ap.add_argument("--temperature", type=float, default=1.0,
                    help="1.0 to match the published fleet")
    ap.add_argument("--top-p", type=float, default=1.0,
                    help="1.0 leaves the sampled distribution untruncated")
    ap.add_argument("--dtype", default="bfloat16", help="local backend only")
    ap.add_argument("--device", default="cuda", help="local backend only: cuda or cpu")
    ap.add_argument("--seed", type=int, default=0,
                    help="base seed; sample i of a cell uses seed + i")
    ap.add_argument("--outdir", default=None, help="default: behavioural/runs/local/")
    ap.add_argument("--dry-run", action="store_true",
                    help="check the prompts against the published shas and stop")
    args = ap.parse_args()

    if args.models == "all":
        keys = list(MODELS)
    elif args.models == "qwens":
        keys = [k for k in MODELS if k.startswith("qwen")]
    elif args.models == "llamas":
        keys = [k for k in MODELS if k.startswith("llama")]
    else:
        keys = [k.strip() for k in args.models.split(",")]
    conds = PUBLISHED if args.conditions == "all" else [c.strip() for c in args.conditions.split(",")]
    for k in keys:
        if k not in MODELS:
            sys.exit(f"unknown model: {k}\nknown: {', '.join(MODELS)}")
    for c in conds:
        if c not in CONDITIONS:
            sys.exit(f"unknown condition: {c}\nknown: {', '.join(CONDITIONS)}")

    print("prompt check against the published fleet rows:")
    bad = check_prompts(conds)
    if bad:
        sys.exit(f"\n{len(bad)} condition(s) no longer reproduce the published prompt: "
                 f"{', '.join(bad)}\nprompts/ must not be edited; refusing to run.")
    print("  all conditions reproduce the published prompt text\n")
    if args.dry_run:
        return

    if args.backend == "openrouter":
        missing = [k for k in keys if not MODELS[k]["openrouter"]]
        if missing:
            sys.exit("no hosted endpoint for: " + ", ".join(missing)
                     + "\nrun these with --backend local.")
        versions = {"torch": None, "transformers": None}
    else:
        import torch, transformers
        versions = {"torch": torch.__version__, "transformers": transformers.__version__}

    outdir = Path(args.outdir) if args.outdir else REPO / "behavioural" / "runs" / "local"
    outdir.mkdir(parents=True, exist_ok=True)
    stamp = _dt.date.today().isoformat()

    counts: dict[tuple[str, str], dict[str, int]] = {}

    for key in keys:
        cfg = MODELS[key]
        tok = model = None
        if args.backend == "local":
            free = vram_gb()
            if free and cfg.get("gb", 0) > free:
                print(f"SKIP {cfg['label']}: needs ~{cfg['gb']} GB in {args.dtype}, "
                      f"card has {free:.0f} GB. Run it on a bigger pod, or take "
                      f"its row from the API fleet.", file=sys.stderr)
                continue
            print(f"loading {cfg['hf']} ...", flush=True)
            tok, model = load_local(cfg["hf"], args.dtype, args.device)

        out = outdir / f"local_{key}_{args.backend}_{stamp}.jsonl"
        rows = errors = 0
        with out.open("w", encoding="utf-8") as fh:
            for cond in conds:
                c = CONDITIONS[cond]
                system, user = build(cond)
                tally: dict[str, int] = {}
                for i in range(args.n):
                    row = {
                        "timestamp": _dt.datetime.now(_dt.timezone.utc).isoformat(),
                        "task": "carwash",
                        "intervention": c["intervention"],
                        "intervention_description": c["description"],
                        "condition": cond,
                        "prompt_file": c["file"],
                        "sample_index": i,
                        "family": key.split("-")[0],
                        "backend": args.backend,
                        "model_label": cfg["label"],
                        "model_slug": cfg["openrouter"] if args.backend == "openrouter" else cfg["hf"],
                        "model_key": key,
                        "temperature": args.temperature,
                        "top_p": args.top_p,
                        "max_tokens": c["max_tokens"],
                        "system": system or "",
                        "user": user,
                        "system_sha256": sha256(system) if system else "NONE",
                        "prompt_sha256": sha256(user),
                        "messages": ([{"role": "system", "content": system}] if system else [])
                                    + [{"role": "user", "content": user}],
                        "dtype": args.dtype if args.backend == "local" else None,
                        "device": args.device if args.backend == "local" else None,
                        "seed": args.seed + i if args.backend == "local" else None,
                        "torch": versions["torch"],
                        "transformers": versions["transformers"],
                        "response_text": None,
                        "decision": None,
                        "response_raw": None,
                        "error": None,
                    }
                    try:
                        if args.backend == "local":
                            text, raw = gen_local(tok, model, system, user,
                                                  c["max_tokens"], args.temperature,
                                                  args.top_p, args.seed + i, args.device)
                        else:
                            text, raw = gen_openrouter(cfg["openrouter"], system, user,
                                                       c["max_tokens"], args.temperature,
                                                       args.top_p)
                        row["response_text"] = text
                        row["response_raw"] = raw
                        row["decision"] = decide(text)
                        if row["decision"] is None:
                            # No action token: the fleet recorded these as
                            # invalid rather than as a wrong answer.
                            row["error"] = "no action token in reply"
                    except Exception as exc:          # noqa: BLE001
                        row["error"] = f"{type(exc).__name__}: {exc}"
                    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                    rows += 1
                    if row["error"]:
                        errors += 1
                    tally[str(row["decision"])] = tally.get(str(row["decision"]), 0) + 1
                counts[(key, cond)] = tally
                summary = " ".join(f"{k}={v}" for k, v in sorted(tally.items()))
                print(f"  {cfg['label']:14s} {cond:14s} {summary}", flush=True)

        if model is not None:
            del model
            try:
                import torch
                torch.cuda.empty_cache()
            except Exception:      # noqa: BLE001 - cpu runs have nothing to free
                pass
        note = f" ({errors} with no action token or errored)" if errors else ""
        print(f"  wrote {rows} rows -> {out}{note}\n")

    write_summary(outdir, keys, conds, counts, args)


def write_summary(outdir: Path, keys: list[str], conds: list[str],
                  counts: dict, args) -> None:
    """The drive-count table, the thing the published summaries report.

    Drive is the correct answer. A cell is "k/n": k samples answering Drive out
    of n usable ones. Samples with no action token are excluded from n, which
    is how the 17-model sweep handled its one such response.
    """
    lines = [f"# Local fleet -- {_dt.date.today().isoformat()}", "",
             f"{len(keys)} models x {len(conds)} conditions x {args.n} samples, "
             f"temperature {args.temperature}, top_p {args.top_p}, "
             f"backend {args.backend}.", "",
             "Drive is correct. Cells are Drive / usable samples.", "",
             "| model | " + " | ".join(conds) + " |",
             "|---|" + "---|" * len(conds)]
    for key in keys:
        row = [MODELS[key]["label"]]
        for cond in conds:
            t = counts.get((key, cond))
            if not t:
                row.append("--")
                continue
            drive = t.get("drive", 0)
            usable = sum(v for k, v in t.items() if k in ("drive", "walk"))
            row.append(f"{drive}/{usable}" if usable else "0/0")
        lines.append("| " + " | ".join(row) + " |")
    text = "\n".join(lines) + "\n"
    (outdir / "summary.md").write_text(text, encoding="utf-8")
    print(text)
    print(f"wrote {outdir / 'summary.md'}")


if __name__ == "__main__":
    main()
