#!/usr/bin/env python3
"""Re-run the carwash prompts and log each model's verbatim reply.

Why this exists: the prompt files in prompts/ end with an "Answer with exactly
one word" instruction, so every reply in runs/baseline/*.jsonl is 4-6
characters. Those runs are complete and untruncated -- they just measure a
forced choice. To see what a model actually says, the constraint has to come
off the request.

prompts/ is never modified. --verbatim and --two-turn drop the constraint line
from the text in memory and record exactly what was sent (and its sha256) in
every row, so the provenance stays checkable.

Three modes:

  --forced     (default) reproduces the existing runs: prompt as-is, one word.
  --verbatim   drops the constraint, raises max_tokens. Prose reply, no label.
  --two-turn   turn 1 verbatim prose, turn 2 asks for the one-word label.
               Gives both from a single rollout; `decision` holds the label.

The output schema is a superset of runs/baseline/*.jsonl -- every field those
files carry is written with the same name and meaning, so old and new rows can
be read by the same code.

Usage
-----
  export ANTHROPIC_API_KEY=... OPENAI_API_KEY=... OPENROUTER_API_KEY=...

  # what would be sent, no API calls, no keys needed
  python runs/run_prompts.py --models sonnet5 --two-turn --dry-run

  # one model, verbatim prose, 5 samples
  python runs/run_prompts.py --models sonnet5 --verbatim --n 5

  # the full sweep, two-turn, into runs/verbatim/
  python runs/run_prompts.py --models all --two-turn --n 10 --outdir runs/verbatim
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROMPTS = REPO / "prompts"

# Trailing provenance line in some prompt files; not part of the prompt.
SHA_LINE = re.compile(r"^SHA-256:.*$", re.MULTILINE)
# The forced-choice instruction, with or without the ": walk or drive" tail.
ONE_WORD = re.compile(r"^Answer with exactly one word.*$", re.MULTILINE)
# Most prompt files end with the bare form and leave the options implicit; the
# published rows show the original runner completing it. baseline.txt is the one
# file that already spells the options out.
BARE_CONSTRAINT = re.compile(r"^Answer with exactly one word:\s*$", re.MULTILINE)
CHOICES = "walk or drive"

FOLLOWUP = "Answer with exactly one word: walk or drive"

# Model slugs are exactly those in runs/baseline/*.jsonl so a re-run stays
# comparable to the published rows. `thinking`: "adaptive" for Claude 4.6+,
# "budget" for pre-4.6 Claude, None for everything else.
MODELS: dict[str, dict] = {
    # --- Anthropic ---
    "sonnet5":    dict(family="anthropic", slug="claude-sonnet-5",              label="Claude Sonnet 5",   thinking="adaptive"),
    "sonnet46":   dict(family="anthropic", slug="claude-sonnet-4-6",            label="Claude Sonnet 4.6", thinking="adaptive"),
    "sonnet45":   dict(family="anthropic", slug="claude-sonnet-4-5",            label="Claude Sonnet 4.5", thinking="budget"),
    "opus":       dict(family="anthropic", slug="claude-opus-4-7",              label="Claude Opus 4.7",   thinking="adaptive"),
    "haiku":      dict(family="anthropic", slug="claude-haiku-4-5-20251001",    label="Claude Haiku 4.5",  thinking="budget"),
    # Not in the published sweep; available if you want a current-generation row.
    "opus5":      dict(family="anthropic", slug="claude-opus-5",                label="Claude Opus 5",     thinking="adaptive"),
    # --- OpenAI ---
    "gpt41":      dict(family="openai", slug="gpt-4.1",         label="GPT-4.1",        thinking=None),
    "gpt41mini":  dict(family="openai", slug="gpt-4.1-mini",    label="GPT-4.1-mini",   thinking=None),
    "gpt4o":      dict(family="openai", slug="gpt-4o",          label="GPT-4o",         thinking=None),
    "gpt4":       dict(family="openai", slug="gpt-4",           label="GPT-4",          thinking=None),
    "gpt35":      dict(family="openai", slug="gpt-3.5-turbo",   label="GPT-3.5-turbo",  thinking=None),
    # --- OpenRouter (open weights + others) ---
    "llama3b":    dict(family="openrouter", slug="meta-llama/llama-3.2-3b-instruct",  label="Llama 3.2-3B",    thinking=None),
    "llama8b":    dict(family="openrouter", slug="meta-llama/llama-3.1-8b-instruct",  label="Llama 3.1-8B",    thinking=None),
    "llama70b":   dict(family="openrouter", slug="meta-llama/llama-3.3-70b-instruct", label="Llama 3.3-70B",   thinking=None),
    "maverick":   dict(family="openrouter", slug="meta-llama/llama-4-maverick",       label="Llama 4-Maverick", thinking=None),
    "mistral":    dict(family="openrouter", slug="mistralai/mistral-large",           label="Mistral Large",   thinking=None),
    "deepseek":   dict(family="openrouter", slug="deepseek/deepseek-chat",            label="DeepSeek V3.2",   thinking=None),
    "kimi":       dict(family="openrouter", slug="moonshotai/kimi-k2",                label="Kimi K2",         thinking=None),
}

PUBLISHED_SWEEP = [
    "sonnet5", "sonnet46", "sonnet45", "opus", "haiku",
    "gpt41", "gpt41mini", "gpt4o", "gpt4", "gpt35",
    "llama3b", "llama8b", "llama70b", "maverick", "mistral", "deepseek", "kimi",
]


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_prompt(name: str) -> str:
    """Prompt text with the trailing SHA-256 provenance line removed.

    Reproduces the `user` field of the published rows byte for byte, which is
    why sha256(load_prompt('baseline.txt')) equals the hash the file declares.
    """
    path = PROMPTS / name
    if not path.exists():
        sys.exit(f"no such prompt: {path}")
    return SHA_LINE.sub("", path.read_text(encoding="utf-8")).rstrip()


def complete_constraint(text: str) -> str:
    """Fill in the options when a prompt file ends with the bare instruction.

    prompts/benchmark_*.txt and substrate.txt end with "Answer with exactly one
    word:" and leave the options implicit. The published runs sent
    "...one word: walk or drive", so completing it here keeps a re-run
    byte-comparable with runs/baseline/ and runs/CoT/.
    """
    return BARE_CONSTRAINT.sub(f"Answer with exactly one word: {CHOICES}", text)


def drop_constraint(text: str) -> tuple[str, str | None]:
    """Remove the forced-choice line. Returns (text, the line removed or None).

    Operates on the in-memory string only; the file on disk is never touched.
    """
    found = ONE_WORD.search(text)
    if not found:
        return text, None
    return ONE_WORD.sub("", text).rstrip(), found.group(0)



# --------------------------------------------------------------------------
# providers
# --------------------------------------------------------------------------

def call_anthropic(cfg: dict, messages: list[dict], max_tokens: int,
                   temperature: float, want_thinking: bool):
    """One Anthropic request. Returns (text, thinking_text, raw_dict)."""
    import anthropic

    client = anthropic.Anthropic()
    kwargs: dict = dict(model=cfg["slug"], max_tokens=max_tokens, messages=messages)

    if want_thinking and cfg["thinking"] == "adaptive":
        # display defaults to "omitted" (empty thinking text) on current models;
        # "summarized" is the most reasoning the API will return. The raw chain
        # of thought is never exposed -- this is a summary, not a transcript.
        kwargs["thinking"] = {"type": "adaptive", "display": "summarized"}
    elif want_thinking and cfg["thinking"] == "budget":
        # Pre-4.6 models still take a fixed budget, which must be < max_tokens.
        kwargs["thinking"] = {"type": "enabled", "budget_tokens": max(1024, max_tokens // 2)}
    else:
        # temperature and thinking cannot both be set on 4.6+ models.
        kwargs["temperature"] = temperature

    resp = client.messages.create(**kwargs)
    raw = resp.model_dump()
    text = "".join(b.text for b in resp.content if b.type == "text")
    thinking = "".join(getattr(b, "thinking", "") or "" for b in resp.content if b.type == "thinking")
    return text, thinking, raw


def call_openai_compatible(cfg: dict, messages: list[dict], max_tokens: int,
                           temperature: float):
    """One OpenAI or OpenRouter request. Returns (text, thinking_text, raw_dict).

    OpenRouter speaks the OpenAI wire format, so both families share this path.
    Claude is never routed here -- it uses the Anthropic SDK above.
    """
    from openai import OpenAI

    if cfg["family"] == "openrouter":
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            sys.exit("OPENROUTER_API_KEY is not set")
        client = OpenAI(api_key=key, base_url="https://openrouter.ai/api/v1")
    else:
        client = OpenAI()

    resp = client.chat.completions.create(
        model=cfg["slug"], messages=messages,
        max_tokens=max_tokens, temperature=temperature,
    )
    raw = resp.model_dump()
    msg = resp.choices[0].message
    text = msg.content or ""
    # Some OpenRouter reasoning models expose a separate reasoning field.
    thinking = getattr(msg, "reasoning", None) or ""
    return text, thinking, raw


# Retrying these never helps: a missing package, a bad key, or a malformed
# request fails the same way every time.
FATAL = ("ImportError", "ModuleNotFoundError", "AuthenticationError",
         "PermissionDeniedError", "BadRequestError", "NotFoundError")


def call(cfg: dict, messages: list[dict], max_tokens: int, temperature: float,
         want_thinking: bool, retries: int = 4):
    """Dispatch to the right provider, retrying only transient failures."""
    for attempt in range(retries):
        try:
            if cfg["family"] == "anthropic":
                return call_anthropic(cfg, messages, max_tokens, temperature, want_thinking)
            return call_openai_compatible(cfg, messages, max_tokens, temperature)
        except SystemExit:
            raise
        except Exception as exc:  # noqa: BLE001 - provider SDKs raise many types
            if type(exc).__name__ in FATAL or attempt == retries - 1:
                raise
            wait = 2 ** (attempt + 1)
            print(f"    {type(exc).__name__}: {exc} -- retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise AssertionError("unreachable")


# --------------------------------------------------------------------------

def run_one(cfg: dict, key: str, prompt_file: str, mode: str, sample: int,
            max_tokens: int, temperature: float, want_thinking: bool,
            dry_run: bool) -> dict:
    """Build, send, and log a single rollout."""
    original = load_prompt(prompt_file)

    if mode == "forced":
        sent, removed = complete_constraint(original), None
    else:
        sent, removed = drop_constraint(original)

    row: dict = {
        "timestamp": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "task": "carwash",
        "intervention": Path(prompt_file).stem,
        "intervention_description": f"{prompt_file}, mode={mode}",
        "mode": mode,
        "constraint_removed": removed,
        "sample_index": sample,
        "family": cfg["family"],
        "model_label": cfg["label"],
        "model_slug": cfg["slug"],
        "model_key": key,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "system": "",
        "user": sent,
        "system_sha256": sha256(""),
        "prompt_sha256": sha256(sent),
        "prompt_file_sha256": sha256(original),
        "messages": [{"role": "user", "content": sent}],
        "response_text": None,
        "thinking_text": None,
        "decision": None,
        "turns": [],
        "response_raw": None,
        "error": None,
    }

    if dry_run:
        row["error"] = "dry-run: nothing sent"
        return row

    try:
        messages = [{"role": "user", "content": sent}]
        text, thinking, raw = call(cfg, messages, max_tokens, temperature, want_thinking)
        row["response_text"] = text
        row["thinking_text"] = thinking or None
        row["response_raw"] = raw
        row["turns"].append({"turn": 1, "sent": messages, "text": text,
                             "thinking": thinking or None, "raw": raw})

        if mode == "forced":
            row["decision"] = text.strip().strip(".").lower() or None

        elif mode == "two-turn":
            # Turn 2: keep the prose, then ask for the label. The assistant turn
            # is real conversation history, not a prefill.
            messages2 = messages + [
                {"role": "assistant", "content": text},
                {"role": "user", "content": FOLLOWUP},
            ]
            text2, thinking2, raw2 = call(cfg, messages2, 16, temperature, False)
            row["decision"] = text2.strip().strip(".").lower() or None
            row["turns"].append({"turn": 2, "sent": messages2, "text": text2,
                                 "thinking": thinking2 or None, "raw": raw2})
    except Exception as exc:  # noqa: BLE001
        row["error"] = f"{type(exc).__name__}: {exc}"

    return row


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Re-run the carwash prompts, logging verbatim replies.")
    ap.add_argument("--models", default="sonnet5",
                    help="comma-separated keys, or 'all' for the published sweep. "
                         f"Keys: {', '.join(MODELS)}")
    ap.add_argument("--prompt", default="baseline.txt",
                    help="file in prompts/ (repeatable via comma)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--forced", action="store_const", const="forced", dest="mode",
                      help="prompt as written: one-word answer (reproduces existing runs)")
    mode.add_argument("--verbatim", action="store_const", const="verbatim", dest="mode",
                      help="drop the one-word constraint: prose reply")
    mode.add_argument("--two-turn", action="store_const", const="two-turn", dest="mode",
                      help="prose, then a second turn for the one-word label")
    ap.set_defaults(mode="forced")
    ap.add_argument("--n", type=int, default=1, help="samples per model per prompt")
    ap.add_argument("--max-tokens", type=int, default=None,
                    help="default: 16 forced, 4000 otherwise")
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--thinking", action="store_true",
                    help="request summarized reasoning where the model supports it "
                         "(Anthropic only; the raw chain of thought is never returned)")
    ap.add_argument("--outdir", default=None,
                    help="default: runs/<mode>/")
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would be sent; no API calls, no keys needed")
    args = ap.parse_args()

    keys = PUBLISHED_SWEEP if args.models == "all" else [k.strip() for k in args.models.split(",")]
    unknown = [k for k in keys if k not in MODELS]
    if unknown:
        sys.exit(f"unknown model key(s): {', '.join(unknown)}\nknown: {', '.join(MODELS)}")

    prompt_files = [p.strip() for p in args.prompt.split(",")]
    max_tokens = args.max_tokens if args.max_tokens is not None else (16 if args.mode == "forced" else 4000)

    outdir = Path(args.outdir) if args.outdir else REPO / "runs" / args.mode
    outdir.mkdir(parents=True, exist_ok=True)
    stamp = _dt.date.today().isoformat()

    print(f"mode={args.mode}  max_tokens={max_tokens}  n={args.n}  -> {outdir}")
    if args.dry_run:
        print("DRY RUN: no requests will be sent\n")

    for key in keys:
        cfg = MODELS[key]
        out = outdir / f"{args.mode}_{key}_{stamp}.jsonl"
        rows, errors = 0, 0
        with out.open("w", encoding="utf-8") as fh:
            for prompt_file in prompt_files:
                for sample in range(args.n):
                    print(f"  {cfg['label']:22s} {prompt_file:26s} sample {sample + 1}/{args.n}")
                    row = run_one(cfg, key, prompt_file, args.mode, sample,
                                  max_tokens, args.temperature, args.thinking,
                                  args.dry_run)
                    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                    rows += 1
                    if row["error"] and not args.dry_run:
                        errors += 1
                        print(f"      ERROR: {row['error']}", file=sys.stderr)
                    elif not args.dry_run:
                        preview = (row["response_text"] or "")[:90].replace("\n", " ")
                        print(f"      decision={row['decision']!r}  {len(row['response_text'] or '')} chars: {preview}")

        note = f" ({errors} errored)" if errors else ""
        print(f"  wrote {rows} rows -> {out}{note}\n")

    if args.dry_run:
        example = run_one(MODELS[keys[0]], keys[0], prompt_files[0], args.mode,
                          0, max_tokens, args.temperature, args.thinking, True)
        print("--- prompt that would be sent ---")
        print(example["user"])
        print("--- end ---")
        if example["constraint_removed"]:
            print(f"\nconstraint line dropped (in memory only): {example['constraint_removed']!r}")
        print(f"prompt_sha256: {example['prompt_sha256']}")


if __name__ == "__main__":
    main()
