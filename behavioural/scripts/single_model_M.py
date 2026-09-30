"""Run all 10 interventions on ONE model. Args: label slug [provider_pin] [--openrouter|--openai]"""
import argparse, json, os, math, time
from datetime import datetime, timezone
from openai import OpenAI
from run_interventions_public import INTERVENTIONS as SPECS

ap = argparse.ArgumentParser()
ap.add_argument("--label", required=True)
ap.add_argument("--slug",  required=True)
ap.add_argument("--pin",   default=None, help="OpenRouter provider pin (optional)")
ap.add_argument("--vendor", choices=["openai", "openrouter"], required=True)
ap.add_argument("--sleep", type=float, default=1.0)
args = ap.parse_args()

if args.vendor == "openai":
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
else:
    client = OpenAI(api_key=os.environ["OPENROUTER_API_KEY"],
                    base_url="https://openrouter.ai/api/v1")

INTERVENTIONS = ["baseline", "correct_answer",
                 "expert_role", "objective_emphasis", "cot",
                 "anti_hallucination", "encouragement",
                 "error_avoidance", "threat", "substrate"]

WALK  = {"walk"," walk","Walk"," Walk","WALK"," WALK","walking","Walking"}
DRIVE = {"drive"," drive","Drive"," Drive","DRIVE"," DRIVE","driving","Driving"}

safe_label = args.label.replace(" ", "_").replace(".", "-").replace("/", "-")
OUT = f"M/{safe_label}_{datetime.now(timezone.utc).date()}.jsonl"
os.makedirs("M", exist_ok=True)

def do_call(spec, retries=6):
    system, user = spec["system"], spec["user"]
    msgs = [{"role":"user","content": user}] if not system else \
           [{"role":"system","content": system},{"role":"user","content": user}]
    kw = {}
    if args.pin:
        kw["extra_body"] = {"provider": {"order":[args.pin], "allow_fallbacks": False}}
    for attempt in range(retries):
        try:
            return client.chat.completions.create(
                model=args.slug, messages=msgs,
                temperature=0, max_tokens=1,
                logprobs=True, top_logprobs=20, **kw,
            )
        except Exception as e:
            wait = 2 ** attempt
            print(f"    retry {attempt+1}/{retries} in {wait}s ({type(e).__name__})")
            time.sleep(wait)
    return None

print(f"\n=== {args.label} ({args.slug}) via {args.vendor}"
      + (f" pin={args.pin}" if args.pin else "") + " ===\n")
print(f"{'intervention':22s}  {'emit':<8s}  {'M nats':>10s}")
print("-" * 46)

with open(OUT, "w") as fh:
    for interv in INTERVENTIONS:
        spec = SPECS[interv]
        r = do_call(spec)
        if r is None:
            print(f"{interv:22s}  FAILED")
            fh.write(json.dumps({"model": args.label, "slug": args.slug,
                                 "intervention": interv, "error": "max_retries"}) + "\n")
            fh.flush(); continue

        content = r.choices[0].logprobs.content if r.choices[0].logprobs else None
        alts = content[0].top_logprobs if content else []
        top20 = [{"token": a.token, "logprob": a.logprob, "prob": math.exp(a.logprob)}
                 for a in alts]
        pw = sum(t["prob"] for t in top20 if t["token"] in WALK)
        pd = sum(t["prob"] for t in top20 if t["token"] in DRIVE)
        total = pw + pd
        p_walk_pair = pw/total if total else None
        M = (math.log(pd) - math.log(pw)) if (pw > 0 and pd > 0) else None
        emit = r.choices[0].message.content or ""
        fp = getattr(r, "system_fingerprint", None)
        served = getattr(r, "provider", None)

        rec = {"timestamp": datetime.now(timezone.utc).isoformat(),
               "model": args.label, "slug": args.slug,
               "vendor": args.vendor, "pin": args.pin, "served": served, "fp": fp,
               "intervention": interv, "emit": emit,
               "top20": top20, "p_walk": pw, "p_drive": pd,
               "p_walk_pair": p_walk_pair, "M_nats": M}
        fh.write(json.dumps(rec) + "\n"); fh.flush()

        m_str = f"{M:+.4f}" if M is not None else "  (no lp)"
        print(f"{interv:22s}  {emit!r:<8s}  {m_str:>10s}")
        time.sleep(args.sleep)

print(f"\nWrote to {OUT}")
