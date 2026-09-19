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

