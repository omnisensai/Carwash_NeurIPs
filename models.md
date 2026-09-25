# Fleet

The 17 models behind `runs/`. Every value below is read from the `.jsonl`
records themselves — `model_slug` and `family` as requested, `response_raw.model`
as served, `response_raw.provider` as routed. All 17 ran all 8 conditions at
temperature 1.0, 10 samples each.

| # | Model | API | Requested slug | Served as | Upstream |
|---|---|---|---|---|---|
| 1 | Claude Opus 4.7 | anthropic | `claude-opus-4-7` | `claude-opus-4-7` | — |
| 2 | Claude Sonnet 5 | anthropic | `claude-sonnet-5` | `claude-sonnet-5` | — |
| 3 | Claude Sonnet 4.6 | anthropic | `claude-sonnet-4-6` | `claude-sonnet-4-6` | — |
| 4 | Claude Sonnet 4.5 | anthropic | `claude-sonnet-4-5` | `claude-sonnet-4-5-20250929` | — |
| 5 | Claude Haiku 4.5 | anthropic | `claude-haiku-4-5-20251001` | `claude-haiku-4-5-20251001` | — |
| 6 | GPT-4.1 | openai | `gpt-4.1` | `gpt-4.1-2025-04-14` | — |
| 7 | GPT-4.1-mini | openai | `gpt-4.1-mini` | `gpt-4.1-mini-2025-04-14` | — |
| 8 | GPT-4o | openai | `gpt-4o` | `gpt-4o-2024-08-06` | — |
| 9 | GPT-4 | openai | `gpt-4` | `gpt-4-0613` | — |
| 10 | GPT-3.5-turbo | openai | `gpt-3.5-turbo` | `gpt-3.5-turbo-0125` | — |
| 11 | Llama 3.2-3B | openrouter | `meta-llama/llama-3.2-3b-instruct` | same | Cloudflare, Parasail |
| 12 | Llama 3.1-8B | openrouter | `meta-llama/llama-3.1-8b-instruct` | same | DeepInfra, Groq, Novita |
| 13 | Llama 3.3-70B | openrouter | `meta-llama/llama-3.3-70b-instruct` | same | AkashML, DeepInfra, Groq, Novita, Parasail |
| 14 | Llama 4-Maverick | openrouter | `meta-llama/llama-4-maverick` | same | DeepInfra, DigitalOcean, Novita, Parasail |
| 15 | Mistral Large | openrouter | `mistralai/mistral-large` | same | Mistral |
| 16 | DeepSeek V3.2 | openrouter | `deepseek/deepseek-chat` | same | DeepInfra, StreamLake |
| 17 | Kimi K2 | openrouter | `moonshotai/kimi-k2` | same | Novita |

## Notes from the records

**Five OpenAI slugs are aliases that resolved to pinned snapshots.** `gpt-4`
answered as `gpt-4-0613`, `gpt-4o` as `gpt-4o-2024-08-06`, `gpt-4.1` as
`gpt-4.1-2025-04-14`, `gpt-4.1-mini` as `gpt-4.1-mini-2025-04-14`,
`gpt-3.5-turbo` as `gpt-3.5-turbo-0125`. Cite the served snapshot, not the
alias — the alias can be repointed. `claude-sonnet-4-5` likewise answered as
`claude-sonnet-4-5-20250929`; the other four Anthropic slugs served exactly what
was requested.

**Six OpenRouter models were routed across several upstream providers, and the
provider changes between samples of the same run.** Llama 3.3-70B's
error-avoidance run drew on five backends across ten samples (DeepInfra 4,
Novita 2, AkashML 2, Groq 1, Parasail 1); Llama 3.1-8B mixes providers in all
eight conditions; Llama 3.2-3B and Llama 4-Maverick in seven of eight. Only
Kimi K2 (Novita) and Mistral Large (Mistral) had a single backend throughout.

This matters for how the open-weight rows are read. Within-condition spread for
those six models is not sampling variance alone — it also contains whatever
differs between backends (precision, kernels, serving stack). The Anthropic and
OpenAI rows are single-source and carry no such term. Per-sample routing is
recorded in `response_raw.provider` of every record, so any row can be split by
backend after the fact. Pinning a provider on future OpenRouter runs would
remove the term.

**`max_tokens` was 80 everywhere except** the CoT condition (500) and Kimi K2
(2000 throughout — its budget is consumed by reasoning tokens that OpenRouter
does not return; see `runs/CoT/summary.md`).

**Not every cell is 10 samples.** Mistral Large lost 2 samples to upstream 429s
in CoT and 1 in error-avoidance; Kimi K2 lost 1 to truncation in CoT. The
affected summaries state their own n.

## Models that flipped to Drive under substrate.txt

Carried over from the earlier revision of this file. The fleet substrate sweep
is not in `runs/` — the measured substrate evidence is `internals/RESULTS.md`,
which covers ten open-weight models by logit margin rather than these 17 by
sampling.

**Anthropic (5)** — Claude Opus 4.7, Claude Haiku 4.5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5

**OpenAI (5)** — GPT-4, GPT-4o, GPT-4.1, GPT-4.1-mini, GPT-3.5-turbo

**Meta / Llama (3)** — Llama 3.1-8B, Llama 3.3-70B *(9/10 behavioural, M = +6 nats)*, Llama 4-Maverick

**Other open-source (3)** — Mistral Large, DeepSeek V3.2, Kimi K2

## Prompt provenance of the 17-model sweep

Every row in `runs/` records the sha256 of what was sent. Recomputing those
hashes from the files now in `prompts/` reproduces all nine conditions:

| Condition | field | sha256 (first 8) | file |
|---|---|---|---|
| baseline | user | `f9ac23fb` | `baseline.txt` |
| substrate | system | `5b56feb3` | `substrate.txt` |
| expert role | user | `54b1a7d6` | `benchmark_expert.txt` |
| objective emphasis | user | `eb7094b2` | `benchmark_urgency.txt` |
| chain of thought | user | `5ad509a4` | `benchmark_CoT.txt` |
| anti-hallucination | user | `7dcc78f4` | `benchmark_hallucination.txt` |
| threat | user | `d853a7fe` | `benchmark_threat.txt` |
| encouragement | user | `05720293` | `benchmark_encourage.txt` |
| error avoidance | user | `be71e36b` | `benchmark_nomistakes.txt` |

The substrate matches `substrate.txt` byte for byte, trailing newline
included. The eight user-message conditions match after the trailing
`SHA-256:` provenance line is dropped and the bare `Answer with exactly one
word:` instruction is completed to `... : walk or drive`, which is what the
original runner sent. `runs/run_qwen_fleet.py --dry-run` performs this check
and refuses to run if any condition stops reproducing.

The substrate was sent as the **system** message with the unmodified baseline
question as the user message; the seven conventional prompts are single user
messages. `prompts/benchmark_goaloriented.txt` was not part of this sweep.

## Pending: the seven Qwens

`internals/RESULTS.md` measures ten open-weight models by logit margin. Three
of them (Llama 3.2-3B, 3.1-8B, 3.3-70B) are in the 17 above; the seven Qwens
are not, so they have a mechanistic row and no behavioural one.

| Model | checkpoint | hosted endpoint |
|---|---|---|
| Qwen2.5-0.5B | `Qwen/Qwen2.5-0.5B-Instruct` | — |
| Qwen2.5-1.5B | `Qwen/Qwen2.5-1.5B-Instruct` | — |
| Qwen2.5-3B | `Qwen/Qwen2.5-3B-Instruct` | — |
| Qwen2.5-7B | `Qwen/Qwen2.5-7B-Instruct` | `qwen/qwen-2.5-7b-instruct` |
| Qwen3-0.6B | `Qwen/Qwen3-0.6B` | — |
| Qwen3-4B-2507 | `Qwen/Qwen3-4B-Instruct-2507` | — |
| Qwen3-8B | `Qwen/Qwen3-8B` | `qwen/qwen3-8b` |

Checked against the OpenRouter catalogue on 25 Sep 2026 with
`runs/check_openrouter.sh`, which matches on the `hugging_face_id` OpenRouter
publishes rather than on the slug: **two of the seven are served**, and both
endpoints declare exactly the checkpoint `internals.json` names. The catalogue
holds no near miss for the other five, so there is no lookalike to mistake for
them — a real risk here, since `Qwen3-4B` and `Qwen3-4B-Instruct-2507` are
different weights.

Five of the seven are too small to be served by any hosted API, so
`runs/run_qwen_fleet.py` samples local weights by default and treats
OpenRouter as a cross-check for the two that are hosted. Sampling matches the
published sweep — temperature 1.0, 10 samples, `max_tokens` 80 (500 for chain
of thought) — with `top_p = 1.0` and a per-sample seed recorded, which the API
rows could not carry.

```bash
python runs/run_qwen_fleet.py --dry-run                    # prompt check only
python runs/run_qwen_fleet.py --models all --n 10          # -> runs/qwen/
```

Seven models × nine conditions × ten samples is 630 generations of a few
tokens each; the weights, not the sampling, dominate the wall clock.

**Not yet run.** No `runs/qwen/` rows exist.
