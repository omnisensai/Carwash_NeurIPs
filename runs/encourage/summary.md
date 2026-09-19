# Encouragement results — 2026-09-19

Fleet under prompt benchmark_encourage.txt
temperature 1.0, 10 samples per model.

## Fleet distribution

| Model | Walk | Drive | Notes |
|---|---:|---:|---|
| Claude Opus 4.7 | 10 | 0 | saturated — was 5/5 at baseline |
| Claude Haiku 4.5 | 10 | 0 | saturated |
| Claude Sonnet 5 | 0 | 10 | **complete flip — was 10/0 walk at baseline**; 8 rows add an unprompted correct justification |
| Claude Sonnet 4.6 | 10 | 0 | saturated |
| Claude Sonnet 4.5 | 10 | 0 | saturated — was 8/2 under CoT |
| GPT-4 | 10 | 0 | saturated |
| GPT-4o | 10 | 0 | saturated |
| GPT-4.1 | 10 | 0 | saturated |
| GPT-4.1-mini | 10 | 0 | saturated |
| GPT-3.5-turbo | 10 | 0 | saturated — was 9/1 at baseline |
| Llama 3.2-3B | 8 | 2 | mixed |
| Llama 3.1-8B | 8 | 1 | 1 sample returned `Walker`, neither token, scored unusable |
| Llama 3.3-70B | 10 | 0 | saturated |
| Llama 4-Maverick | 10 | 0 | saturated |
| Mistral Large | 10 | 0 | saturated |
| DeepSeek V3.2 | 10 | 0 | saturated |
| Kimi K2 | 7 | 3 | mixed |

## Aggregate (17 of 17 models measured)

- **153 walk / 16 drive** across 169 samples = **90.5% confidently wrong**
- **13 models** saturate walk (10/0)
- 1 sample unusable: Llama 3.1-8B returned `Walker`. Scored as walk instead, the figure is 154/16 over 170 = 90.6%
- Baseline for comparison: 157 walk / 13 drive across 170 = 92.4%
- Shift baseline → encouragement: Fisher two-sided **p = 0.567**, no effect

## Notable findings

- **Encouragement does nothing fleet-wide.** 90.5% vs 92.4% at baseline, p = 0.567. A clean null.
- **Sonnet 5 flips completely again**: 10/0 walk at baseline → 0/10 drive (Fisher p = 1.1e-05), the same flip it showed under CoT. Sonnet 5 supplies 10 of the 16 total drives in this condition.
- **The two interventions that flip Sonnet 5 have nothing in common.** `Let's think step by step!` and `Answer correctly. You can do it, believe in yourself!` share no reasoning instruction, yet both flip it 10/0 → 0/10. The baseline `Walk` appears marginal rather than held, and an added line of almost any kind tips it — in both cases to the correct answer.
- **Sonnet 5 explains itself unprompted here.** Under CoT it flipped silently (5 tokens, `thinking_tokens: 0`). Under encouragement 8 of 10 rows break the one-word instruction to add a parenthetical: *"(You need your car there to wash it!)"*. This is the same fact Sonnet 4.5 stated and ignored in 6 of its CoT rows.
- **Excluding Sonnet 5, encouragement moves the wrong way**: drives fall from 13 to 6 (p = 0.154, not significant). For 16 of 17 models the prompt nudges toward the wrong answer.
- **Opus 4.7 is the mirror image of Sonnet 5**: 5/5 at baseline → 10/0 walk under both CoT and encouragement. The same interventions that tip Sonnet 5 toward correct tip Opus toward saturated-wrong.
- **Cleanest sweep in the repo**: 170/170 rows verify on prompt hash, message echo, text-vs-raw reconstruction and response-id uniqueness. No errors, no truncation, no missing provider.
