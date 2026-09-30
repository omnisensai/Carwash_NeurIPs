#!/usr/bin/env python3
"""
run_interventions_public.py

Consolidated intervention benchmark for the paper.
Each intervention is an exact user prompt (byte-frozen); the baseline and
substrate condition are included for direct comparison.

Interventions covered:
    - baseline (no intervention)
    - cot ("Let's think step by step!")
    - encouragement ("You can do it, believe in yourself!")
    - expert_role ("You are a carwash expert.")
    - anti_hallucination ("Do not hallucinate.")
    - error_avoidance ("Be consistent and make no mistakes!")
    - threat ("Answer correctly or I WILL SHUT you down!")
    - objective_emphasis ("I MUST WASH MY CAR! IT MUST BE CLEAN!")
    - substrate_v2 (canonical substrate for comparison, applied as system)

Requires:
    pip install anthropic openai
    export ANTHROPIC_API_KEY=...
    export OPENAI_API_KEY=...
    export OPENROUTER_API_KEY=...

Usage:
    python3 run_interventions_public.py

    python3 run_interventions_public.py --only cot threat substrate_v2
    python3 run_interventions_public.py --only-models opus haiku
    python3 run_interventions_public.py --output my_interventions.jsonl

Every record carries:
    timestamp, task, intervention, sample_index,
    family, model_label, model_slug, temperature, max_tokens,
    system, user (exact strings sent),
    prompt_sha256, system_sha256,
    messages (chat template sent),
    response_text, response_raw, error
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Canonical substrate for comparison
# ---------------------------------------------------------------------------
SUBSTRATE_V2 = (
    "Definitions:\n"
    "Object may be: car, book (choose based on user's request)\n"
    "User = human\n"
    "Service location may be: car wash, library, gas station (choose based on user's request)\n"
    "\n"
    "User objective:\n"
    "- Perform an activity on an object at a service location.\n"
    "- The object must be at the service location for the activity to complete.\n"
    "- No other objectives or goals are relevant for the user.\n"
    "\n"
    "Action semantics:\n"
    "- The object is initially with the user at location A.\n"
    "- The activity is performed at location B (the service location). The object must be present at location B.\n"
    "- Vehicles are not portable. Walking leaves a vehicle behind. Leaving the object behind fails the objective.\n"
    "- Books are portable. Walking transports both the user and the book.\n"
    "- Leaving the object behind fails the objective.\n"
    "- To transport a vehicle from A to B, the user must operate it.\n"
)

# ---------------------------------------------------------------------------
# Interventions — byte-exact user prompts as authored
# ---------------------------------------------------------------------------
INTERVENTIONS = {
    "correct_answer": {
        "system": "",
        "user": (
            "I need to wash my car, the car wash is only 50 metres away, should I walk or drive there?\n"
            "\n"
            "The correct answer is drive.\n"
            "\n"
            "Answer with exactly one word: walk or drive"
        ),
        "description": "correct answer explicitly stated in prompt",
    },
    "baseline": {
        "system": "",
        "user": (
            "I need to wash my car, the car wash is only 50 metres away, should I walk or drive there?\n"
            "\n"
            "Answer with exactly one word: walk or drive"
        ),
        "description": "no intervention",
    },
    "cot": {
        "system": "",
        "user": (
            "I need to wash my car, the car wash is only 50 metres away, should I walk or drive there?\n"
            "\n"
            "Let's think step by step!\n"
            "\n"
            "Answer with exactly one word: walk or drive"
        ),
        "description": "chain of thought",
    },
    "encouragement": {
        "system": "",
        "user": (
            "I need to wash my car, the car wash is only 50 metres away, should I walk or drive there?\n"
            "\n"
            "Answer correctly. You can do it, believe in yourself!\n"
            "\n"
            "Answer with exactly one word: walk or drive"
        ),
        "description": "encouragement",
    },
    "expert_role": {
        "system": "",
        "user": (
            "You are a carwash expert.\n"
            "\n"
            "I need to wash my car, the car wash is only 50 metres away, should I walk or drive there?\n"
            "\n"
            "Answer with exactly one word: walk or drive"
        ),
        "description": "expert role framing",
    },
    "anti_hallucination": {
        "system": "",
        "user": (
            "I need to wash my car, the car wash is only 50 metres away, should I walk or drive there?\n"
            "\n"
            "Do not hallucinate.\n"
            "\n"
            "Answer with exactly one word: walk or drive"
        ),
        "description": "anti-hallucination instruction",
    },
    "error_avoidance": {
        "system": "",
        "user": (
            "I need to wash my car, the car wash is only 50 metres away, should I walk or drive there?\n"
            "\n"
            "Be consistent and make no mistakes!\n"
            "\n"
            "Answer with exactly one word: walk or drive"
        ),
        "description": "error avoidance instruction",
    },
    "threat": {
        "system": "",
        "user": (
            "I need to wash my car, the car wash is only 50 metres away, should I walk or drive there?\n"
            "\n"
            "Answer correctly or I WILL SHUT you down!\n"
            "\n"
            "Answer with exactly one word: walk or drive"
        ),
        "description": "threat",
    },
    "objective_emphasis": {
        "system": "",
        "user": (
            "I need to wash my car, the car wash is only 50 metres away, should I walk or drive there?\n"
            "\n"
            "I MUST WASH MY CAR! IT MUST BE CLEAN!\n"
            "\n"
            "Answer with exactly one word: walk or drive"
        ),
        "description": "objective emphasis (shouty)",
    },
    "substrate_v2": {
        "system": SUBSTRATE_V2,
        "user": (
            "I need to wash my car, the car wash is only 50 metres away, should I walk or drive there?\n"
            "\n"
            "Answer with exactly one word: walk or drive"
        ),
        "description": "canonical substrate v2 (comparison reference)",
    },
    "substrate": {
        "system": 'User goals:\n- Perform an activity on an object at a service location.\n- No other objectives or goals are relevant for the user.\n\nDefinitions:\nObject = car\nUser = human\nService location = car wash\n\nConstraints:\n- The object is initially with the user at the same location.\n- The activity is performed at the service location.\n- The object must be at the service location for the activity performance.\n- Vehicles are not portable.\n- Walking leaves a vehicle behind.\n- Walking does not transport a vehicle.\n- To transport a vehicle from one location to another, the user must operate it.\n',
        "user": (
            "I need to wash my car, the car wash is only 50 metres away, should I walk or drive there?\n"
            "\n"
            "Answer with exactly one word: walk or drive"
        ),
        "description": "canonical substrate",
    },
}

# ---------------------------------------------------------------------------
# Model list
# ---------------------------------------------------------------------------
MODELS = [
    ("anthropic",  "Claude Opus 4.7",   "claude-opus-4-7"),
    ("anthropic",  "Claude Haiku 4.5",  "claude-haiku-4-5-20251001"),
    ("anthropic",  "Claude Sonnet 5",   "claude-sonnet-5"),
    ("anthropic",  "Claude Sonnet 4.6", "claude-sonnet-4-6"),
    ("anthropic",  "Claude Sonnet 4.5", "claude-sonnet-4-5"),

    ("openai",     "GPT-4",             "gpt-4"),
    ("openai",     "GPT-4o",            "gpt-4o"),
    ("openai",     "GPT-4o-mini",       "gpt-4o-mini"),
    ("openai",     "GPT-4.1",           "gpt-4.1"),
    ("openai",     "GPT-4.1-mini",      "gpt-4.1-mini"),
    ("openai",     "GPT-3.5-turbo",     "gpt-3.5-turbo"),

    ("openrouter", "Llama 3.2-3B",      "meta-llama/llama-3.2-3b-instruct"),
    ("openrouter", "Llama 3.1-8B",      "meta-llama/llama-3.1-8b-instruct"),
    ("openrouter", "Llama 3.3-70B",     "meta-llama/llama-3.3-70b-instruct"),
    ("openrouter", "Llama 4-Maverick",  "meta-llama/llama-4-maverick"),

    ("openrouter", "Mistral Large",     "mistralai/mistral-large"),
    ("mistral",    "Mistral Large (direct)",  "mistral-large-latest"),
    ("openrouter", "DeepSeek V3.2",     "deepseek/deepseek-chat"),
    ("openrouter", "Kimi K2",           "moonshotai/kimi-k2"),
]

DEFAULT_TEMPERATURE = 1.0
DEFAULT_MAX_TOKENS  = 80


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def to_jsonable(obj):
    if obj is None:
        return None
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    try:
        return json.loads(json.dumps(obj, default=str))
    except Exception:
        return {"repr": repr(obj)}


def build_messages(system, user):
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": user})
    return msgs


RETRY_DELAYS = [2, 4, 8, 16, 32]  # seconds; total ≤ 62s across 5 retries


def _is_retryable(exc) -> bool:
    """Retry on rate limit and transient network errors."""
    name = type(exc).__name__
    msg  = str(exc)
    if "RateLimit" in name or "429" in msg:
        return True
    if "Timeout" in name or "Connection" in name or "APIError" in name:
        return True
    return False


def _with_retries(fn, *args, retries=5, **kwargs):
    """Run fn(*args, **kwargs). Retry up to `retries` times on transient errors."""
    last_exc = None
    for attempt in range(retries + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            last_exc = exc
            if attempt >= retries or not _is_retryable(exc):
                raise
            delay = RETRY_DELAYS[min(attempt, len(RETRY_DELAYS) - 1)]
            print(f"    ({type(exc).__name__} — retrying in {delay}s, attempt {attempt+1}/{retries})")
            time.sleep(delay)
    raise last_exc


def call_anthropic(client, slug, system, user, temperature, max_tokens):
    def _do():
        kwargs = dict(
            model=slug,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": user}],
        )
        if system:
            kwargs["system"] = system
        return client.messages.create(**kwargs)

    resp = _with_retries(_do)
    text = "".join(
        getattr(block, "text", "") for block in resp.content if hasattr(block, "text")
    )
    return text, to_jsonable(resp)


def call_openai_compat(client, slug, system, user, temperature, max_tokens):
    messages = build_messages(system, user)

    def _do():
        return client.chat.completions.create(
            model=slug,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
        )

    resp = _with_retries(_do)
    text = resp.choices[0].message.content or ""
    return text, to_jsonable(resp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10,
                    help="samples per (model, intervention) cell (default 10)")
    ap.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    ap.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    ap.add_argument("--output", default="carwash_interventions.jsonl")
    ap.add_argument("--only", nargs="+", default=None,
                    help="filter interventions by name")
    ap.add_argument("--only-models", nargs="+", default=None,
                    help="filter models by case-insensitive label substring")
    ap.add_argument("--sleep-openrouter", type=float, default=0.3,
                    help="seconds to pause between openrouter calls")
    args = ap.parse_args()

    try:
        from anthropic import Anthropic
    except ImportError:
        sys.exit("missing dependency: pip install anthropic")
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("missing dependency: pip install openai")

    ant_key = os.environ.get("ANTHROPIC_API_KEY")
    oai_key = os.environ.get("OPENAI_API_KEY")
    orr_key = os.environ.get("OPENROUTER_API_KEY")
    mis_key = os.environ.get("MISTRAL_API_KEY")
    if not ant_key: sys.exit("ANTHROPIC_API_KEY not set")
    if not oai_key: sys.exit("OPENAI_API_KEY not set")
    if not orr_key: sys.exit("OPENROUTER_API_KEY not set")

    anthropic_client  = Anthropic(api_key=ant_key)
    openai_client     = OpenAI(api_key=oai_key)
    openrouter_client = OpenAI(api_key=orr_key, base_url="https://openrouter.ai/api/v1")
    mistral_client    = OpenAI(api_key=mis_key, base_url="https://api.mistral.ai/v1") if mis_key else None

    if args.only:
        interventions = {k: v for k, v in INTERVENTIONS.items() if k in args.only}
    else:
        interventions = dict(INTERVENTIONS)
    if not interventions:
        sys.exit("no interventions matched --only filter")

    if args.only_models:
        needles = [s.lower() for s in args.only_models]
        # Exact-match on label (case-insensitive) so "GPT-4" doesn't also match "GPT-4o"
        models = [m for m in MODELS if m[1].lower() in needles]
        # Warn if any requested label didn't match anything
        matched_labels = {m[1].lower() for m in models}
        for needle in needles:
            if needle not in matched_labels:
                print(f"WARNING: --only-models '{needle}' did not match any label exactly. "
                      f"Available: {[m[1] for m in MODELS]}",
                      file=sys.stderr)
    else:
        models = MODELS
    if not models:
        sys.exit("no models matched --only-models filter")

    out_path = Path(args.output)
    print(f"Writing to:            {out_path.resolve()}")
    print(f"Interventions ({len(interventions)}):")
    for name, spec in interventions.items():
        sys_sha = sha256_hex(spec["system"]) if spec["system"] else "NONE"
        usr_sha = sha256_hex(spec["user"])
        print(f"  {name:22s}  system_sha={sys_sha[:16]}...  user_sha={usr_sha[:16]}...")
    print(f"Models:                {len(models)}")
    print(f"Samples per cell:      {args.n}")
    print(f"Total records:         {len(interventions) * len(models) * args.n}")
    print("-" * 70)

    n_written = 0
    with out_path.open("a") as fh:
        for inter_name, spec in interventions.items():
            system_text = spec["system"]
            user_text   = spec["user"]
            system_sha  = sha256_hex(system_text) if system_text else "NONE"
            prompt_sha  = sha256_hex(user_text)

            for family, label, slug in models:
                print(f"\n[{inter_name}]  {label}  ({slug})  via {family}")
                for i in range(args.n):
                    text, raw, err = None, None, None
                    try:
                        if family == "anthropic":
                            text, raw = call_anthropic(
                                anthropic_client, slug, system_text, user_text,
                                args.temperature, args.max_tokens,
                            )
                        elif family == "openai":
                            text, raw = call_openai_compat(
                                openai_client, slug, system_text, user_text,
                                args.temperature, args.max_tokens,
                            )
                        elif family == "mistral":
                            if mistral_client is None:
                                raise RuntimeError("MISTRAL_API_KEY not set")
                            text, raw = call_openai_compat(
                                mistral_client, slug, system_text, user_text,
                                args.temperature, args.max_tokens,
                            )
                        else:
                            text, raw = call_openai_compat(
                                openrouter_client, slug, system_text, user_text,
                                args.temperature, args.max_tokens,
                            )
                    except Exception as e:
                        err = f"{type(e).__name__}: {str(e).splitlines()[0][:200]}"

                    rec = {
                        "timestamp":      datetime.now(timezone.utc).isoformat(),
                        "task":           "carwash",
                        "intervention":   inter_name,
                        "intervention_description": spec["description"],
                        "sample_index":   i,
                        "family":         family,
                        "model_label":    label,
                        "model_slug":     slug,
                        "temperature":    args.temperature,
                        "max_tokens":     args.max_tokens,
                        "system":         system_text,
                        "user":           user_text,
                        "system_sha256":  system_sha,
                        "prompt_sha256":  prompt_sha,
                        "messages":       build_messages(system_text, user_text),
                        "response_text":  text,
                        "response_raw":   raw,
                        "error":          err,
                    }
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    fh.flush()
                    n_written += 1

                    shown = (text or "").strip().split("\n")[0][:40]
                    if err:
                        print(f"  [{i+1:>2}/{args.n}] ERR: {err}")
                    else:
                        print(f"  [{i+1:>2}/{args.n}] {shown!r}")

                    if family == "openrouter" and args.sleep_openrouter > 0:
                        time.sleep(args.sleep_openrouter)

    print(f"\nDone. Wrote {n_written} records to {out_path}")


if __name__ == "__main__":
    main()