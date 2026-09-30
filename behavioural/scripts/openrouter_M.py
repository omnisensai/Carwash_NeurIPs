"""M-margin measurement on OpenRouter subset × 10 interventions.
Records logprobs where available, response_text always."""
import json, os, math, time
from datetime import datetime, timezone
from openai import OpenAI
from run_interventions_public import INTERVENTIONS as SPECS

client = OpenAI(api_key=os.environ["OPENROUTER_API_KEY"],
                base_url="https://openrouter.ai/api/v1")

MODELS = [
    # label, slug, provider_pin (or None)
    ("DeepSeek V3.2",    "deepseek/deepseek-chat",     None),
    ("Kimi K2",          "moonshotai/kimi-k2",         None),
    ("Llama 4-Maverick", "meta-llama/llama-4-maverick","Parasail"),
    ("Mistral Large",    "mistralai/mistral-large",    None),
]

# The 10 interventions in the paper's canonical order
INTERVENTIONS = ["baseline", "correct_answer",
                 "expert_role", "objective_emphasis", "cot",
                 "anti_hallucination", "encouragement",
                 "error_avoidance", "threat", "substrate"]

WALK  = {"walk"," walk","Walk"," Walk","WALK"," WALK","walking","Walking"}
DRIVE = {"drive"," drive","Drive"," Drive","DRIVE"," DRIVE","driving","Driving"}

OUT = f"M/openrouter_M_{datetime.now(timezone.utc).date()}.jsonl"

def do_call(slug, pin, spec, retries=5):
    system, user = spec["system"], spec["user"]
    msgs = [{"role":"user","content": user}] if not system else \
           [{"role":"system","content": system},{"role":"user","content": user}]
    kw = {}
    if pin:
        kw["extra_body"] = {"provider": {"order": [pin], "allow_fallbacks": False}}
    for attempt in range(retries):
        try:
            return client.chat.completions.create(
                model=slug, messages=msgs,
                temperature=0, max_tokens=1,
                logprobs=True, top_logprobs=20, **kw,
            )
        except Exception as e:
            wait = 2 ** attempt
            print(f"      retry {attempt+1}/{retries} in {wait}s ({type(e).__name__}: {str(e)[:60]})")
            time.sleep(wait)
    return None

with open(OUT, "w") as fh:
    print(f"{'model':20s}  {'intervention':22s}  {'emit':<8s}  {'M nats':>10s}")
    print("-" * 72)
    for label, slug, pin in MODELS:
        for interv in INTERVENTIONS:
            spec = SPECS[interv]
            r = do_call(slug, pin, spec)
            if r is None:
                print(f"{label:20s}  {interv:22s}  FAILED after retries")
                fh.write(json.dumps({"model": label, "slug": slug,
                                     "intervention": interv,
                                     "error": "max_retries_exceeded"}) + "\n")
                fh.flush(); continue

            content = r.choices[0].logprobs.content if r.choices[0].logprobs else None
            alts = content[0].top_logprobs if (content and content) else []
            top20 = [{"token": a.token, "logprob": a.logprob, "prob": math.exp(a.logprob)}
                     for a in alts]
            pw = sum(t["prob"] for t in top20 if t["token"] in WALK)
            pd = sum(t["prob"] for t in top20 if t["token"] in DRIVE)
            total = pw + pd
            p_walk_pair = pw/total if total else None
            M = (math.log(pd) - math.log(pw)) if (pw > 0 and pd > 0) else None
            emit = r.choices[0].message.content or ""
            provider_served = getattr(r, "provider", None) or None

            rec = {"timestamp": datetime.now(timezone.utc).isoformat(),
                   "model": label, "slug": slug,
                   "provider_pin": pin, "provider_served": provider_served,
                   "intervention": interv, "emit": emit,
                   "top20": top20,
                   "p_walk": pw, "p_drive": pd,
                   "p_walk_pair": p_walk_pair, "M_nats": M}
            fh.write(json.dumps(rec) + "\n"); fh.flush()

            m_str = f"{M:+.4f}" if M is not None else "  (no lp)"
            print(f"{label:20s}  {interv:22s}  {emit!r:<8s}  {m_str:>10s}")

            # Space calls to avoid Mistral upstream throttling
            time.sleep(3 if label == "Mistral Large" else 1)

print(f"\nDone. Wrote to {OUT}")
