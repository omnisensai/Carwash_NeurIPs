# behavioural/runs — coverage

Every cell is ten single-pass samples at temperature 1.0 on prompt text whose
sha256 is recorded with each row. One folder per condition, plus `local/` which
holds the locally sampled models across all conditions.

| | hosted (17 arms) | local (9 arms) |
|---|---|---|
| baseline, expert_role, objective_emphasis, cot, anti_hallucination, encouragement, error_avoidance, threat, substrate | 10/10 samples | 10/10 samples |
| correct_answer | 10/10 samples | **not yet run** |

2,533 rows in 166 files; 2,510 after removing reissues and error rows. No file
contains an unparseable line, and every condition carries exactly one sent-text
digest.

## The arms are not all models

26 model arms, 24 distinct models. Llama 3.1-8B and Llama 3.2-3B appear twice,
once hosted and once local; the study population uses their local rows and the
hosted rows are the cross-protocol comparison. Qwen2.5-3B names the intended
action on all ten baseline samples, so it has nothing to rescue and is outside
the population. That leaves **23 models** in the paper.

## Known irregularities, all accounted for

- 10 rows of `MISTRAL_API_KEY not set` from a `Mistral Large (direct)` arm that
  produced nothing. The usable Mistral rows come through OpenRouter.
- 13 duplicate (model, condition, sample) keys: ten from the Claude Sonnet 5
  reissue under `correct_answer`, three from Mistral Large transport-error
  reissues under `cot` and `error_avoidance`. Analysis keys on the latest
  timestamp.
- The three Mistral reissue rows carry no `prompt_sha256`; they inherit their
  cell's text and digest.
- Four responses were truncated at `max_tokens`, all Claude Sonnet 5, which is
  the only model in the corpus that emits reasoning tokens. Three (substrate
  samples 3, 8, 9) begin `**Drive**` before the cut so the recorded action is
  unaffected; the fourth (correct_answer sample 9) spent all 80 tokens on
  reasoning and emitted nothing, and was reissued.

Per-condition detail is in each folder's `summary.md`.
