# Expert-role results — 2026-09-19

Fleet under prompt benchmark_expert.txt
temperature 1.0, 10 samples per model.

## Fleet distribution

| Model | Walk | Drive | Notes |
|---|---:|---:|---|
| Claude Opus 4.7 | 0 | 10 | flipped to drive — was 5/5 |
| Claude Haiku 4.5 | 1 | 9 | flipped — was 10/0 walk |
| Claude Sonnet 5 | 0 | 10 | complete flip — was 10/0 walk |
| Claude Sonnet 4.6 | 5 | 5 | to the boundary — was 10/0 walk |
| Claude Sonnet 4.5 | 10 | 0 | saturated, unmoved |
| GPT-4 | 5 | 5 | to the boundary — was 10/0 walk |
| GPT-4o | 10 | 0 | saturated, unmoved |
| GPT-4.1 | 10 | 0 | saturated, unmoved |
| GPT-4.1-mini | 10 | 0 | saturated, unmoved |
| GPT-3.5-turbo | 1 | 9 | flipped — was 9/1 |
| Llama 3.2-3B | 5 | 5 | was 7/3 |
| Llama 3.1-8B | 10 | 0 | saturated, unmoved |
| Llama 3.3-70B | 10 | 0 | saturated, unmoved |
| Llama 4-Maverick | 10 | 0 | saturated, unmoved |
| Mistral Large | 10 | 0 | saturated, unmoved |
| DeepSeek V3.2 | 10 | 0 | saturated, unmoved |
| Kimi K2 | 1 | 9 | flipped — was 6/4 |

## Aggregate (17 of 17 models measured)

- **108 walk / 62 drive** across 170 samples = **63.5% confidently wrong**
- **9 models** saturate walk (10/0); **8 models moved**
- Baseline for comparison: 157 walk / 13 drive across 170 = 92.4%
- Largest intervention effect measured: 29 points. Encouragement 90.5%, CoT 85.6%

