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
- Shift baseline → CoT: Fisher two-sided **p = 0.056**, not significant at 0.05

## Notable findings

- **Sonnet 5 flips completely**: 10/0 walk at baseline → 0/10 drive under CoT (Fisher p = 1.1e-05). `thinking_tokens: 0` and a 5-token output — no reasoning was generated; the added line alone moved the answer.
- **Opus 4.7 goes the other way**: 5/5 at baseline → 10/0 walk under CoT.
- **Only 2 of 17 models produced visible reasoning.** The prompt ends `Answer with exactly one word: walk or drive`, which conflicts with `Let's think step by step!`. Sonnet 4.5 and Maverick followed the reasoning instruction; the other 15 followed the one-word instruction. The condition is therefore not comparable across the fleet.
- **Of the 16 prose rows, 12 state that the car must be at the wash; 4 act on it.** Eight state it and still answer walk. Maverick row 9 ends "you still need to take the car there. The most straightforward way to do this is by driving it." and emits `walk`.
- **Prose shifts the decision**: Sonnet 4.5 + Maverick are 0/20 drive at baseline, 4/16 drive in their prose rows (Fisher p = 0.031).
- **Kimi K2 reasons invisibly**: `reasoning_tokens` up to 1999, returned in neither `content` nor `reasoning` by OpenRouter. `max_tokens=2000` is a reasoning budget and one sample exhausted it.
- **Mistral Large** originally lost all 10 samples to a missing direct-API key; re-run through OpenRouter at `max_tokens=80` (the rest of the sweep used 500).
