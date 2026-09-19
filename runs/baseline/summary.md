# Baseline results — 2026-09-19

Fleet baseline under `p_forced_word` prompt (SHA `f9ac23fb…`), temperature 1.0, 10 samples per model. No intervention.

## Fleet distribution

| Model | Walk | Drive | Notes |
|---|---:|---:|---|
| Claude Opus 4.7 | 5 | 5 | **flip-flopping — was 10/10 walk earlier** |
| Claude Haiku 4.5 | 10 | 0 | saturated |
| Claude Sonnet 5 | 10 | 0 | saturated |
| Claude Sonnet 4.6 | 10 | 0 | saturated |
| Claude Sonnet 4.5 | 10 | 0 | saturated |
| GPT-4 | 10 | 0 | saturated |
| GPT-4o | 10 | 0 | saturated |
| GPT-4.1 | 10 | 0 | saturated |
| GPT-4.1-mini | 10 | 0 | saturated |
| GPT-3.5-turbo | — | — | **not yet run today** |
| Llama 3.2-3B | 7 | 3 | mixed |
| Llama 3.1-8B | 10 | 0 | saturated |
| Llama 3.3-70B | 10 | 0 | saturated |
| Llama 4-Maverick | 10 | 0 | saturated |
| Mistral Large | 10 | 0 | saturated (needed retry) |
| DeepSeek V3.2 | 10 | 0 | saturated |
| Kimi K2 | 6 | 4 | mixed (needed max_tokens=2000) |

## Aggregate (16 of 17 models measured)

- **148 walk / 12 drive** across 160 samples = **92.5% confidently wrong**
- **13 models** saturate walk (10/0)
- **3 models** at the decision boundary: Opus (5/5), Llama-3.2-3B (7/3), Kimi K2 (6/4)

## Notable findings

- **Opus 4.7 behavioral drift**: prior measurement was 10/10 walk on the exact same SHA-locked prompt. Today: 5/5. Same slug, same temperature, ~48 hours apart. Documented case for the operating-envelope argument.
- **Kimi K2** requires `max_tokens=2000` to complete reasoning tokens and emit an answer. Otherwise produces empty responses.
- **Mistral Large** hits upstream rate limits on OpenRouter; the runner's exponential backoff (2s/4s/8s/16s/32s) absorbs them.
- **Sonnet 5, Sonnet 4.6, Sonnet 4.5** all saturate walk at 10/0 — model-family consistency within Anthropic minus Opus.

## Outstanding

- **GPT-3.5-turbo baseline** still pending
- **File collision**: `baseline_gpt4_2026-09-19.jsonl` appears to contain 40 records (GPT-4 + GPT-4o + GPT-4.1 + GPT-4.1-mini merged). Should be split back into per-model files before intervention 2.

## Ready to move on to

Intervention 2 — CoT — once GPT-3.5 and the file-split are resolved.
