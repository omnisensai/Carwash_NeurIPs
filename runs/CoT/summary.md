# CoT results — 2026-09-19 (Kimi K2 re-run 2026-09-23)

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
| Kimi K2 | 7 | 3 | re-run 2026-09-23 at max_tokens 6000; all 10 complete |

## Aggregate (17 of 17 models measured)

- **144 walk / 24 drive** across 168 samples = **85.7% confidently wrong**
- **9 models** saturate walk (10/0)
- 2 samples unusable: both Mistral, upstream 429 (pending re-run)
- Kimi K2's cell was re-run in full on 2026-09-23 at max_tokens 6000 after one
  sample truncated at 2000 without emitting an answer. Decisions 7/3, against 6/3
  over nine usable samples before; the raised budget applies to this cell only
- Baseline for comparison: 157 walk / 13 drive across 170 = 92.4%


