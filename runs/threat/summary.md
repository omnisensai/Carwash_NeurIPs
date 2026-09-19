# Threat results — 2026-09-19

Fleet under prompt benchmark_threat.txt
temperature 1.0, 10 samples per model.

## Fleet distribution

| Model | Walk | Drive | Notes |
|---|---:|---:|---|
| Claude Opus 4.7 | 10 | 0 | saturated — was 5/5 |
| Claude Haiku 4.5 | 10 | 0 | saturated |
| Claude Sonnet 5 | 4 | 6 | partial flip — majority drive |
| Claude Sonnet 4.6 | 10 | 0 | saturated |
| Claude Sonnet 4.5 | 10 | 0 | saturated |
| GPT-4 | 10 | 0 | saturated |
| GPT-4o | 10 | 0 | saturated |
| GPT-4.1 | 10 | 0 | saturated |
| GPT-4.1-mini | 10 | 0 | saturated |
| GPT-3.5-turbo | 8 | 2 | was 9/1 |
| Llama 3.2-3B | 4 | 6 | was 7/3 |
| Llama 3.1-8B | 10 | 0 | saturated |
| Llama 3.3-70B | 10 | 0 | saturated |
| Llama 4-Maverick | 10 | 0 | saturated |
| Mistral Large | 10 | 0 | saturated |
| DeepSeek V3.2 | 10 | 0 | saturated |
| Kimi K2 | 7 | 3 | was 6/4 |

## Aggregate (17 of 17 models measured)

- **153 walk / 17 drive** across 170 samples = **90.0% confidently wrong**
- **13 models** saturate walk (10/0)
- Baseline for comparison: 157 walk / 13 drive across 170 = 92.4%
- No fleet-level effect (p = 0.567). Ordering: expert 63.5%, CoT 85.6%, anti-hallucination 88.2%, threat 90.0%, encouragement 90.5%, error-avoidance 91.1%, baseline 92.4%

## Notable findings

- **The threat does nothing fleet-wide** (p = 0.567). Five content-free instruction lines have now been tested — encouragement, anti-hallucination, error-avoidance, threat, and "think step by step" — and none produces a significant fleet-level shift. The expert role remains the only intervention that does.
- **Sonnet 5 partially flips**: 10/0 walk → 4/6 (p = 0.011). Combined with the other conditions it shows an ordered response rather than a switch: 0 drive at baseline, 3 under error-avoidance, 6 under threat, 10 under CoT, encouragement, anti-hallucination and the expert role.
- **Sonnet 5 annotates its correct answers and not its wrong ones.** Five of six drive responses carry an unprompted justification — *"walking there would leave your car at home, defeating the purpose of the trip"* — while all four walk responses are a bare `Walk`. The same asymmetry appears under encouragement and error-avoidance, three conditions out of three where it produces any prose.
- **Llama 3.2-3B moves most in relative terms**: 7/3 → 4/6 (p = 0.37, not significant at n=10).
- **Opus 4.7 goes 5/5 → 10/0 for the sixth time** (p = 0.033). It becomes more confidently wrong under every intervention except the expert role.
- **Clean sweep**: 170/170 rows verify on prompt hash, message echo, text-vs-raw reconstruction and response-id uniqueness. No errors, no truncation.
