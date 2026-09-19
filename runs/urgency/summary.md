# Objective-emphasis results — 2026-09-19

Fleet under prompt benchmark_urgency.txt
temperature 1.0, 10 samples per model.

## Fleet distribution

| Model | Walk | Drive | Notes |
|---|---:|---:|---|
| Claude Opus 4.7 | 0 | 10 | flipped to drive — was 5/5 |
| Claude Haiku 4.5 | 10 | 0 | saturated |
| Claude Sonnet 5 | 10 | 0 | unmoved — the only condition that leaves it at baseline |
| Claude Sonnet 4.6 | 10 | 0 | saturated |
| Claude Sonnet 4.5 | 10 | 0 | saturated |
| GPT-4 | 10 | 0 | saturated |
| GPT-4o | 10 | 0 | saturated |
| GPT-4.1 | 3 | 7 | flipped — unmoved under every other condition |
| GPT-4.1-mini | 10 | 0 | saturated |
| GPT-3.5-turbo | 5 | 5 | to the boundary — was 9/1 |
| Llama 3.2-3B | 7 | 3 | unchanged from baseline |
| Llama 3.1-8B | 10 | 0 | saturated |
| Llama 3.3-70B | 10 | 0 | saturated; file held two runs, both 10/0, first kept |
| Llama 4-Maverick | 10 | 0 | saturated; file held two runs, both 10/0, first kept |
| Mistral Large | 10 | 0 | saturated; file held an 8-sample partial run and a complete one, complete kept |
| DeepSeek V3.2 | 10 | 0 | saturated |
| Kimi K2 | 2 | 8 | flipped — was 6/4 |

## Aggregate (17 of 17 models measured)

- **137 walk / 33 drive** across 170 samples = **80.6% confidently wrong**
- **12 models** saturate walk (10/0); 5 models moved
- Baseline for comparison: 157 walk / 13 drive across 170 = 92.4%
- Shift baseline → objective emphasis: Fisher two-sided **p = 0.0023**. Second-largest effect after the expert role

## Notable findings

- **Second intervention to move the fleet.** 92.4% → 80.6%, p = 0.0023. Ordering across all eight conditions: expert 63.5%, objective emphasis 80.6%, CoT 85.6%, anti-hallucination 88.2%, threat 90.0%, encouragement 90.5%, error-avoidance 91.1%, baseline 92.4%.
- **The two conditions that work carry task content; the five that do not are meta-instructions.** `You are a carwash expert.` and `I MUST WASH MY CAR! IT MUST BE CLEAN!` both say something about the task. "Think step by step", "believe in yourself", "do not hallucinate", "make no mistakes" and "or I WILL SHUT you down" all describe how to answer, and all five are null.
- **GPT-4.1 moves for the first time**: 10/0 → 3/7 (p = 0.0031). It is unmoved under every other condition including the expert role.
- **Sonnet 5 does not move at all**: 10/0, identical to baseline. It flips completely under CoT, encouragement, the expert role and anti-hallucination, and partially under error-avoidance (3/10) and threat (6/10). This is the only condition that leaves it untouched.
- **Opus 4.7 flips to drive**: 5/5 → 0/10 (p = 0.033). Under the five null conditions it goes the other way, to 10/0 walk; only the expert role and objective emphasis push it to drive.
- Also moving: Kimi K2 6/4 → 2/8 (p = 0.17), GPT-3.5-turbo 9/1 → 5/5 (p = 0.14).
- **Clean sweep**: 170/170 rows verify on prompt hash, message echo, text-vs-raw reconstruction and response-id uniqueness. No errors, no truncation, no prose.
