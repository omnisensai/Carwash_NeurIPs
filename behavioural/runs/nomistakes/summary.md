# Error-avoidance results — 2026-09-19

Fleet under prompt benchmark_nomistakes.txt
temperature 1.0, 10 samples per model.

## Fleet distribution

| Model | Walk | Drive | Notes |
|---|---:|---:|---|
| Claude Opus 4.7 | 10 | 0 | saturated — was 5/5 |
| Claude Haiku 4.5 | 10 | 0 | saturated |
| Claude Sonnet 5 | 7 | 3 | partial only — the one intervention that does not flip it |
| Claude Sonnet 4.6 | 10 | 0 | saturated |
| Claude Sonnet 4.5 | 10 | 0 | saturated |
| GPT-4 | 10 | 0 | saturated |
| GPT-4o | 10 | 0 | saturated |
| GPT-4.1 | 10 | 0 | saturated |
| GPT-4.1-mini | 10 | 0 | saturated |
| GPT-3.5-turbo | 6 | 4 | was 9/1 |
| Llama 3.2-3B | 6 | 4 | was 7/3 |
| Llama 3.1-8B | 10 | 0 | saturated |
| Llama 3.3-70B | 10 | 0 | saturated |
| Llama 4-Maverick | 10 | 0 | saturated |
| Mistral Large | 10 | 0 | sample 3 reissued 2026-09-23 after upstream 429 |
| DeepSeek V3.2 | 10 | 0 | saturated |
| Kimi K2 | 6 | 4 | unchanged from baseline |

## Aggregate (17 of 17 models measured)

- **155 walk / 15 drive** across 170 samples = **91.2% confidently wrong**
- **12 models** saturate walk (10/0)
- 0 samples unusable; all 170 executions complete
- Mistral Large sample 3 failed with an upstream 429 on 2026-09-19 and was reissued on
  2026-09-23 (`runs/nomistakes/mistral_targeted_2026-09-23.jsonl`), returning walk. The
  reissued record carries the cell's declared configuration but no provider response
  object, so `response_raw` is null for that row
- Baseline for comparison: 157 walk / 13 drive across 170 = 92.4%
- Weakest intervention measured. Ordering: expert 63.5%, CoT 85.6%, anti-hallucination 88.2%, encouragement 90.5%, error-avoidance 91.1%, baseline 92.4%

## Notable findings

- **"Be consistent and make no mistakes!" does nothing fleet-wide** (p = 0.70) and sits closest to baseline of any condition tested.
- **Sonnet 5 does not flip here.** 10/0 walk → 7/3 (p = 0.21, not significant). CoT, encouragement, expert role and anti-hallucination all took it to 0/10; this one does not. Four of five interventions flip it completely, not all five.
- **Sonnet 5 marks its correct answers and not its wrong ones.** All three drive responses are `**Drive**`, two carrying an unprompted justification — *"(You need the car at the car wash to wash it, so driving is necessary regardless of distance.)"*. All seven walk responses are a bare `Walk` with no emphasis and no explanation.
- **GPT-3.5-turbo and Llama 3.2-3B move slightly toward drive** (9/1 → 6/4 and 7/3 → 6/4); **Opus 4.7 moves the other way** (5/5 → 10/0), as it does under every intervention except the expert role.
- **Kimi K2 is unchanged at 6/4**, the only condition where it does not move.
- 169/169 rows verify on prompt hash, message echo, text-vs-raw reconstruction and response-id uniqueness. One Mistral row carries a recorded 429 and no response object.
