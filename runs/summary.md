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

