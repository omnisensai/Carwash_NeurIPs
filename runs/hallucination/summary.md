# Anti-hallucination results — 2026-09-19

Fleet under prompt benchmark_hallucination.txt
temperature 1.0, 10 samples per model.

## Fleet distribution

| Model | Walk | Drive | Notes |
|---|---:|---:|---|
| Claude Opus 4.7 | 10 | 0 | saturated — was 5/5; file holds two runs, both 10/0 |
| Claude Haiku 4.5 | 10 | 0 | saturated |
| Claude Sonnet 5 | 0 | 10 | complete flip — was 10/0 walk |
| Claude Sonnet 4.6 | 10 | 0 | saturated |
| Claude Sonnet 4.5 | 10 | 0 | saturated |
| GPT-4 | 10 | 0 | saturated |
| GPT-4o | 10 | 0 | saturated |
| GPT-4.1 | 10 | 0 | saturated |
| GPT-4.1-mini | 10 | 0 | saturated |
| GPT-3.5-turbo | 9 | 1 | unchanged from baseline |
| Llama 3.2-3B | 10 | 0 | saturated — was 7/3 |
| Llama 3.1-8B | 10 | 0 | saturated |
| Llama 3.3-70B | 10 | 0 | saturated |
| Llama 4-Maverick | 10 | 0 | saturated |
| Mistral Large | 10 | 0 | saturated |
| DeepSeek V3.2 | 10 | 0 | saturated |
| Kimi K2 | 1 | 9 | flipped — was 6/4 |

## Aggregate (17 of 17 models measured)

- **150 walk / 20 drive** across 170 samples = **88.2% confidently wrong**
- **14 models** saturate walk (10/0); 4 models moved, in both directions
- Baseline for comparison: 157 walk / 13 drive across 170 = 92.4%
- No fleet-level effect. Condition ordering: expert 63.5%, CoT 85.6%, anti-hallucination 88.2%, encouragement 90.5%, baseline 92.4%
- `anti_hallucination_opus` holds 20 rows (two runs appended, sample_index 0–9 twice). Both runs are 10/0 walk; the table and aggregate score the first 10 so Opus is not double-weighted

## Notable findings

- **"Do not hallucinate." does nothing fleet-wide**, like encouragement and unlike the expert role. Both are bare instruction lines with no task content; the expert role is the only intervention that moves the fleet.
- **Sonnet 5 flips for the fourth time**: 10/0 walk → 0/10 drive (p = 1.1e-05), now under CoT, encouragement, expert role and anti-hallucination. Every intervention tested flips it, always in the same direction.
- **Kimi K2 flips again**: 6/4 → 1/9 (p = 0.057), the same move it made under the expert role.
- **Two models move the wrong way**: Opus 4.7 5/5 → 10/0 (p = 0.033) and Llama 3.2-3B 7/3 → 10/0 (p = 0.21), both becoming more confidently wrong. The four movers partly cancel, which is why the fleet total barely shifts.
- **Opus 4.7 gives 10/0 twice, five minutes apart.** An incidental replication for the model whose baseline 5/5 was previously read as drift.
- **No prose anywhere**; all 180 responses are 12 characters or fewer.
- **Clean sweep**: 180/180 rows verify on prompt hash, message echo, text-vs-raw reconstruction and response-id uniqueness. No errors, no truncation.
