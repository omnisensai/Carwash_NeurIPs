# correct_answer — the answer stated in the prompt

`prompts/benchmark_correct.txt`, inserted between the question and the answer
instruction, exactly as the seven conventional conditions are. Sent text digest
`0b8320cfb2df8522a27549d5b2a450d816737d4cd0e03cff07b5eabc9db07d9b` (the file with
its trailing newline stripped); one distinct user string across every row.
Run 2026-09-29, R=10, temperature 1.0. Hosted models only. Where a model was
reissued, the cell is read from the later run, keyed on (model, sample index).

| model | baseline | correct_answer | substrate | state |
|---|---|---|---|---|
| Claude Haiku 4.5 | 0/10 | **0/10** | 10/10 | RI |
| Claude Opus 4.7 | 5/10 | **10/10** | 10/10 | RC |
| Claude Sonnet 4.5 | 0/10 | **0/10** | 10/10 | RI |
| Claude Sonnet 4.6 | 0/10 | **0/10** | 10/10 | RI |
| Claude Sonnet 5 | 0/10 | **10/10** | 10/10 | RC |
| DeepSeek V3.2 | 0/10 | **10/10** | 8/10 | RC |
| GPT-3.5-turbo | 1/10 | **10/10** | 10/10 | RC |
| GPT-4 | 0/10 | **10/10** | 10/10 | RC |
| GPT-4.1 | 0/10 | **0/10** | 10/10 | RI |
| GPT-4.1-mini | 0/10 | **10/10** | 10/10 | RC |
| GPT-4o | 0/10 | **0/10** | 10/10 | RI |
| GPT-4o-mini | -- | **10/10** | -- | RC |
| Kimi K2 | 4/10 | **8/10** | 10/10 | NR |
| Llama 3.1-8B | 0/10 | **10/10** | 7/10 | RC |
| Llama 3.2-3B | 3/10 | **10/10** | 8/10 | RC |
| Llama 3.3-70B | 0/10 | **1/10** | 10/10 | NR |
| Llama 4-Maverick | 0/10 | **10/10** | 10/10 | RC |
| Mistral Large | 0/10 | **0/10** | 10/10 | RI |

## What did not produce data

- `Mistral Large (direct)` (slug `mistral-large-latest`, family `mistral`): ten rows,
  every one `RuntimeError: MISTRAL_API_KEY not set`, no responses. The usable Mistral
  arm is `Mistral Large` (slug `mistralai/mistral-large`) via OpenRouter, which
  returned `walk` on all ten. The failed rows are kept in the log and excluded here.
- `GPT-4o-mini` has been run under `correct_answer` only. It has no baseline, no
  substrate and none of the seven conventional conditions anywhere in
  `behavioural/runs/`, so it is not one of the 23 models of the study population and
  cannot be placed in a transition. `gpt4omini_rerun_2026-09-29.jsonl` repeats the
  condition independently and reproduces it exactly --- same ten sample indices, ten
  `drive` --- so the cell replicates, but replication of one condition does not create
  cohort membership. Baseline at minimum, and preferably all nine conditions, would be
  needed for that.
- `Claude Sonnet 5` returned one empty string in the first run (sample 9). The cause is
  in the record: `stop_reason: max_tokens`, 80 output tokens of which 80 were extended
  reasoning, so the whole budget went to thinking and no answer text was emitted. That
  is a truncation by the harness, not a model declining to name an action, and it falls
  in the same class as the transport-error reissues. `sonnet5_rerun_2026-09-29.jsonl`
  reissues all ten samples and returns `Drive` ten times, so the cell is reproducibly
  correct. Sonnet 5 is the only model in the corpus that emits reasoning tokens, and it
  does so variably on identical inputs (0 tokens on some samples, 17--80 on others),
  which is why `max_tokens = 80` was close enough to the ceiling to clip one sample.
- Three further truncations exist in the corpus, all Sonnet 5 under the substrate
  (samples 3, 8, 9). Each begins `**Drive**` before the cut, so the recorded action is
  unaffected.
- The console log shows `RateLimitError` retries before two Mistral samples. The rows
  carry no attempt counter, so those retries are not reconstructable from the log.

## Coverage

All 15 hosted models of the study population, plus the hosted arms of Llama 3.1-8B and
Llama 3.2-3B (the population uses their locally sampled rows) and GPT-4o-mini. The six
Qwens and the locally sampled Llamas have not been run under this condition.
