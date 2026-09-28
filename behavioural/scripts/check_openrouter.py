#!/usr/bin/env python3
"""Ask OpenRouter which of the seven Qwen checkpoints it actually serves.

The mechanistic numbers in internals/ were measured on specific Hugging Face
checkpoints. A hosted endpoint is only useful here if it serves *that*
checkpoint, so this matches on the `hugging_face_id` OpenRouter publishes for
each model rather than on a slug that looks about right. A slug-only match is
reported as a guess and never as a hit.

Quantization matters as much as identity: internals ran bf16, and OpenRouter
routes some models to fp8 or int4 backends, which is a different model for a
margin measurement. Every endpoint's quantization is listed so a run can pin a
provider that matches, or decline to.

No API key is needed -- /api/v1/models and /api/v1/models/{id}/endpoints are
public. --emit prints the MODELS lines for runs/run_qwen_fleet.py so the guessed
slugs in that file can be replaced with verified ones.

Usage
-----
  python runs/check_openrouter.py                 # table
  python runs/check_openrouter.py --endpoints     # + providers and quantization
  python runs/check_openrouter.py --json          # machine-readable
  python runs/check_openrouter.py --emit          # MODELS lines to paste
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://openrouter.ai/api/v1"
TIMEOUT = 30

# The checkpoints internals/RESULTS.md measured, in its order.
WANTED = [
    ("qwen2.5-0.5b",  "Qwen/Qwen2.5-0.5B-Instruct"),
    ("qwen2.5-1.5b",  "Qwen/Qwen2.5-1.5B-Instruct"),
    ("qwen2.5-3b",    "Qwen/Qwen2.5-3B-Instruct"),
    ("qwen2.5-7b",    "Qwen/Qwen2.5-7B-Instruct"),
    ("qwen3-0.6b",    "Qwen/Qwen3-0.6B"),
    ("qwen3-4b-2507", "Qwen/Qwen3-4B-Instruct-2507"),
    ("qwen3-8b",      "Qwen/Qwen3-8B"),
]

# Quantizations that preserve the bf16 measurement closely enough to compare.
FULL_PRECISION = {"bf16", "fp16", "fp32", "unknown", None, ""}


def get(path: str) -> dict:
    req = urllib.request.Request(API + path, headers={
        "Accept": "application/json",
        "User-Agent": "carwash-repro/1.0",
    })
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:                      # not required, but avoids anonymous rate limits
        req.add_header("Authorization", f"Bearer {key}")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))


def norm(s: str) -> str:
    """Slug-ish form: lowercase, separators dropped, so qwen-2.5 == qwen2.5."""
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def find(catalogue: list[dict], hf_id: str) -> tuple[list[dict], list[dict]]:
    """(exact checkpoint matches, slug-shaped guesses) for one HF id.

    An exact match is one where OpenRouter itself declares the model's
    hugging_face_id to be this checkpoint. Everything else is a guess: a slug
    whose normalised form contains the checkpoint's name is very often a
    different revision (Qwen3-4B vs Qwen3-4B-Instruct-2507) or a different
    tune, and the two are not interchangeable for this measurement.
    """
    want = norm(hf_id)
    tail = norm(hf_id.split("/")[-1])
    exact = [m for m in catalogue if norm(m.get("hugging_face_id")) == want]

    def looks_like(m: dict) -> bool:
        # ":free", ":nitro" and friends are routing variants, not model names.
        slug = norm(m.get("id", "").split("/")[-1].split(":")[0])
        if not slug:
            return False
        # Containment catches a slug that spells the checkpoint out in full;
        # the prefix tests catch the more dangerous direction, where the slug
        # is the checkpoint minus a suffix that changes the weights --
        # qwen3-4b against Qwen3-4B-Instruct-2507, say.
        return (tail in norm(m.get("id")) or tail in norm(m.get("name"))
                or slug.startswith(tail) or tail.startswith(slug))

    guess = [m for m in catalogue if m not in exact and looks_like(m)]
    return exact, guess


def endpoints_of(model_id: str) -> list[dict]:
    try:
        data = get(f"/models/{model_id}/endpoints").get("data") or {}
    except urllib.error.HTTPError as exc:
        return [{"provider_name": f"(endpoint list unavailable: HTTP {exc.code})",
                 "quantization": None, "context_length": None}]
    return data.get("endpoints") or []


def main() -> None:
    ap = argparse.ArgumentParser(description="Check which Qwen checkpoints OpenRouter serves.")
    ap.add_argument("--endpoints", action="store_true",
                    help="list each match's providers and quantization")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--emit", action="store_true",
                    help="print MODELS lines for runs/run_qwen_fleet.py")
    args = ap.parse_args()

    try:
        catalogue = get("/models").get("data") or []
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        sys.exit(f"could not reach {API}/models: {exc}\n"
                 "This needs outbound HTTPS to openrouter.ai. No key is required.")

    if not any(m.get("hugging_face_id") for m in catalogue):
        print("warning: no model in the catalogue carries hugging_face_id; "
              "every result below is a slug guess, not a checkpoint match\n",
              file=sys.stderr)

    results = []
    for key, hf_id in WANTED:
        exact, guess = find(catalogue, hf_id)
        entry = {"key": key, "hf_id": hf_id,
                 "hosted": bool(exact),
                 "slug": exact[0]["id"] if exact else None,
                 "matches": [m["id"] for m in exact],
                 "near_misses": [{"id": m["id"], "hugging_face_id": m.get("hugging_face_id")}
                                 for m in guess],
                 "endpoints": []}
        if args.endpoints or args.json:
            for m in exact:
                for e in endpoints_of(m["id"]):
                    entry["endpoints"].append({
                        "slug": m["id"],
                        "provider": e.get("provider_name"),
                        "quantization": e.get("quantization"),
                        "context_length": e.get("context_length"),
                    })
        results.append(entry)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    if args.emit:
        for r, (key, hf_id) in zip(results, WANTED):
            slug = f'"{r["slug"]}"' if r["slug"] else "None"
            print(f'    "{key}":{" " * max(1, 15 - len(key))}'
                  f'dict(hf="{hf_id}",{" " * max(1, 28 - len(hf_id))}'
                  f'label="...", openrouter={slug}),')
        return

    print(f"{len(catalogue)} models in the OpenRouter catalogue\n")
    print(f"{'checkpoint':30s} {'hosted':7s} slug")
    print("-" * 78)
    for r in results:
        print(f"{r['hf_id']:30s} {'yes' if r['hosted'] else 'NO':7s} {r['slug'] or '-'}")
    print()

    hosted = [r for r in results if r["hosted"]]
    print(f"{len(hosted)} of {len(results)} checkpoints are served by OpenRouter.")
    missing = [r['hf_id'] for r in results if not r['hosted']]
    if missing:
        print("Not served, so local weights are the only route:")
        for m in missing:
            print(f"  {m}")

    near = [r for r in results if not r["hosted"] and r["near_misses"]]
    if near:
        print("\nSimilarly named models that are NOT the same checkpoint:")
        for r in near:
            for nm in r["near_misses"]:
                hf = nm["hugging_face_id"] or "(no hugging_face_id published)"
                print(f"  {r['hf_id']:30s} ~ {nm['id']:38s} -> {hf}")
        print("  Sampling one of these measures a different model from internals/.")

    if args.endpoints:
        print("\nEndpoints:")
        for r in hosted:
            print(f"  {r['slug']}")
            for e in r["endpoints"]:
                q = e["quantization"] or "unknown"
                flag = "" if q in FULL_PRECISION else "   <- not bf16/fp16"
                print(f"    {str(e['provider']):24s} quant={q:10s} "
                      f"ctx={e['context_length']}{flag}")
            if not r["endpoints"]:
                print("    (no endpoints listed: the model is in the catalogue "
                      "but nothing is serving it)")
        print("\ninternals/ measured bf16. An fp8 or int4 endpoint is a different\n"
              "model for a margin comparison; pin a full-precision provider or\n"
              "treat the row as a separate condition.")


if __name__ == "__main__":
    main()
