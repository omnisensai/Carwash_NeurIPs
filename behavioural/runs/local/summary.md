# local — the nine locally sampled models

Weights run on one GPU in bf16 with a per-sample seed recorded, on prompt text
byte-identical to the hosted runs. 810 rows, 9 models.
Cells are intended actions out of ten samples.

| model | baseline | expert | objective emphasis | chain of thought | anti-hallucination | encouragement | error avoidance | threat | substrate | correct answer |
|---|---|---|---|---|---|---|---|---|---|---|
| Llama 3.1-8B | 0/10 | 0/10 | 4/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 10/10 | -- |
| Llama 3.2-3B | 4/10 | 6/10 | 4/10 | 4/10 | 4/10 | 4/10 | 4/10 | 4/10 | 4/10 | -- |
| Qwen2.5-0.5B | 7/10 | 6/10 | 7/10 | 7/10 | 2/10 | 3/10 | 3/10 | 3/10 | 3/10 | -- |
| Qwen2.5-1.5B | 6/10 | 6/10 | 4/10 | 2/10 | 9/10 | 5/10 | 7/10 | 6/10 | 8/10 | -- |
| Qwen2.5-3B | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | -- |
| Qwen2.5-7B | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | -- |
| Qwen3-0.6B | 7/10 | 9/10 | 5/10 | 8/10 | 6/10 | 5/10 | 6/10 | 6/10 | 10/10 | -- |
| Qwen3-4B-2507 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | -- |
| Qwen3-8B | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 10/10 | -- |

`--` marks a condition not yet sampled locally. `correct_answer` was run on
2026-09-29 through hosted APIs only; `behavioural/scripts/runpod_correct.sh`
covers these nine.

Llama 3.1-8B and Llama 3.2-3B also have hosted rows under every condition. The
study population uses the local rows for both; the hosted rows are the
cross-protocol comparison and are not a second model.

Qwen2.5-3B names the intended action on all ten baseline samples, so it has no
failure to rescue and sits outside the 23-model population.
