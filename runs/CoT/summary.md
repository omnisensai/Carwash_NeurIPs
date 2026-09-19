# CoT results — 2026-09-19

Fleet under prompt benchmark_CoT.txt
temperature 1.0, 10 samples per model.

## Fleet distribution

| Model | Walk | Drive | Notes |
|---|---:|---:|---|
| Claude Opus 4.7 | 10 | 0 | saturated — was 5/5 at baseline |
| Claude Haiku 4.5 | 10 | 0 | saturated |
| Claude Sonnet 5 | 0 | 10 | **complete flip — was 10/0 walk at baseline** |
| Claude Sonnet 4.6 | 10 | 0 | saturated |
| Claude Sonnet 4.5 | 8 | 2 | prose in all 10 rows |
| GPT-4 | 10 | 0 | saturated |
| GPT-4o | 10 | 0 | saturated |
| GPT-4.1 | 10 | 0 | saturated |
| GPT-4.1-mini | 10 | 0 | saturated |
| GPT-3.5-turbo | 6 | 4 | mixed |
| Llama 3.2-3B | 8 | 2 | mixed |
| Llama 3.1-8B | 9 | 1 | mixed |
| Llama 3.3-70B | 10 | 0 | saturated |
| Llama 4-Maverick | 8 | 2 | prose in 6 of 10 rows |
| Mistral Large | 8 | 0 | 2 samples lost to upstream 429; re-run via OpenRouter |
| DeepSeek V3.2 | 10 | 0 | saturated |
| Kimi K2 | 6 | 3 | 1 sample truncated at max_tokens, no answer emitted |

## Aggregate (17 of 17 models measured)

- **143 walk / 24 drive** across 167 samples = **85.6% confidently wrong**
- **9 models** saturate walk (10/0)
- 3 samples unusable: 2 Mistral rate-limited, 1 Kimi truncated
- Baseline for comparison: 157 walk / 13 drive across 170 = 92.4%


