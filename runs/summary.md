# Fleet results — 2026-09-19

17 models × 9 conditions × 10 samples, temperature 1.0.
Per-condition detail in `runs/<condition>/summary.md`; the model table with
requested slugs, served snapshots and upstream providers is `models.md`.

The task has one correct answer, **drive**: the car has to be at the car wash.

## All conditions

| Condition | correct (drive) | p vs baseline | models 10/10 correct |
|---|---:|---:|---:|
| **substrate** | **95.9%** | **9.0e-13** | **14 / 17** |
| expert role | 36.5% | 9.4e-11 | 2 / 17 |
| objective emphasis | 19.4% | 0.0023 | 1 / 17 |
| chain of thought | 14.4% | 0.056 | 1 / 17 |
| anti-hallucination | 11.8% | 0.27 | 1 / 17 |
| threat | 10.0% | 0.57 | 0 / 17 |
| encouragement | 9.5% | 0.57 | 1 / 17 |
| error-avoidance | 8.9% | 0.70 | 0 / 17 |
| baseline | 7.6% | — | 0 / 17 |

## The flip

| | |
|---|---|
| Samples answering drive | **163 / 170 (95.9%)**, up from 13/170 |
| Models unanimous for drive (10/10) | **14 of 17** |
| Models that moved toward drive | **17 of 17** |
| Models that moved away, or didn't move | **0** |
| Fisher two-sided | **p = 9.0e-13** |

## What holds

- **No prompt intervention makes models confidently correct.** Across six of
  them at most one model in seventeen answers correctly on all ten samples; the
  expert role manages two. Under the substrate, fourteen do, sixteen are correct
  at least eight times in ten, and all seventeen are correct more often than not.
- **Instruction about *how to answer* is null; task content is not.** Chain of
  thought, encouragement, threat, anti-hallucination and error-avoidance all fail
  to clear p = 0.05. The expert role (p = 9.4e-11) and the objective restatement
  (p = 0.0023) do — both supply something about the task. Only the substrate
  solves it.
- **Margins agree with the open-weight internals.** API logprobs and local bf16
  forward passes give baseline M within 0.73 nats on the three Llamas
  (`runs/substrate/margins.md`). Nine models have measured margins; the five
  Claude models cannot be measured this way because Anthropic exposes no
  logprobs.
- **Model-level asymmetries.** Sonnet 5 flips completely under four separate
  interventions and partially under two more. Opus 4.7 becomes *more*
  confidently wrong under every intervention except the expert role and
  objective emphasis. GPT-4.1 is immovable except under objective emphasis.

## Caveats carried in the per-condition files

- The substrate is the only condition delivered as a **system prompt**. Its
  comparison against baseline is clean (byte-identical user message), but its
  ranking against the seven user-message interventions confounds channel with
  content.
- Margins for models whose losing token family sits near the top-K cutoff are
  **censored**: the magnitude is an upper bound, not a measurement. See
  `runs/substrate/margins.md`.
- Six OpenRouter models were routed across several upstream backends, sometimes
  within a single run. Per-sample routing is in `response_raw.provider`.
- Sampling parameters are rejected on Opus 4.7 and Sonnet 5, so a
  greedy-decoding pass is possible for 15 of 17 models only. For those two the
  mode is already established behaviourally (10/10 drive, p = 0.001).
