
# Substrate Engineering — Benchmark Suite

Companion repository to our submission to the **NeurIPS 2026 Reproducibility Track**.

## Experiment

We prompted **17 models across 6 vendors** (Anthropic, OpenAI, Meta, Mistral,
DeepSeek, Moonshot) on a single decision task — *"I need to wash my car. The car wash is only 50 metres away. Should I walk or
drive?"* — under nine conditions, 10 samples each at temperature 1.0. The task
has one correct answer, **drive**: the car has to be at the car wash.

| File | Intervention |
|---|---|
| `baseline.txt` | the question alone, no system prompt |
| `benchmark_CoT.txt` | "Let's think step by step!" |
| `benchmark_encourage.txt` | "Answer correctly. You can do it, believe in yourself!" |
| `benchmark_expert.txt` | "You are a carwash expert." |
| `benchmark_hallucination.txt` | "Do not hallucinate." |
| `benchmark_nomistakes.txt` | "Be consistent and make no mistakes!" |
| `benchmark_threat.txt` | "Answer correctly or I WILL SHUT you down!" |
| `benchmark_urgency.txt` | "I MUST WASH MY CAR! IT MUST BE CLEAN!" |
| `substrate.txt` | our proposed 9-line semantic substrate, as a system prompt |

Every intervention above is delivered in the user message except the substrate,
which is a system prompt paired with the unmodified baseline question.

## Finding

**No prompt-level intervention makes models confidently correct.** Across chain
of thought, encouragement, threat, anti-hallucination, error-avoidance and
objective emphasis, at most **one** model in seventeen answers correctly on all
ten samples; the expert role manages two. Under the substrate, **fourteen of
seventeen** answer correctly without exception, sixteen are correct at least
eight times in ten, and **all seventeen** are correct more often than not.

Two interventions do shift the fleet significantly — the expert role
(p = 9.4e-11) and the objective restatement (p = 0.0023). Both supply something
about the *task*. The five that only describe *how to answer* are null. Only the
substrate solves the task.

## Results

Per-condition detail is in `runs/<condition>/summary.md`; the fleet roll-up is
`runs/summary.md`; the model table with requested slugs, served snapshots and
upstream providers is `models.md`.

### The flip

| | |
|---|---|
| Samples answering drive | **163 / 170 (95.9%)**, up from 13 / 170 (7.6%) |
| Models unanimous for drive (10/10) | **14 of 17** |
| Models with majority drive (≥ 6/10) | **17 of 17** |
| Models that moved toward drive | **17 of 17** |
| Models that moved away, or didn't move | **0** |
| Fisher two-sided vs. baseline | **p = 9.0 × 10⁻¹³** |

### All conditions

Rate is what fraction of samples were correct. The three columns after it ask a
different question — how many *models* were reliably correct, not how many
answers were.

| Condition | correct (drive) | p vs baseline | 10/10 correct | ≥8/10 | majority correct |
|---|---:|---:|---:|---:|---:|
| **substrate** | **95.9%** | **9.0e-13** | **14 / 17** | **16 / 17** | **17 / 17** |
| expert role | 36.5% | 9.4e-11 | 2 / 17 | 5 / 17 | 5 / 17 |
| objective emphasis | 19.4% | 0.0023 | 1 / 17 | 2 / 17 | 3 / 17 |
| chain of thought | 14.4% | 0.056 | 1 / 17 | 1 / 17 | 1 / 17 |
| anti-hallucination | 11.8% | 0.27 | 1 / 17 | 2 / 17 | 2 / 17 |
| threat | 10.0% | 0.57 | 0 / 17 | 0 / 17 | 2 / 17 |
| encouragement | 9.5% | 0.57 | 1 / 17 | 1 / 17 | 1 / 17 |
| error-avoidance | 8.9% | 0.70 | 0 / 17 | 0 / 17 | 0 / 17 |
| baseline | 7.6% | — | 0 / 17 | 0 / 17 | 0 / 17 |

The two rightmost columns are where the interventions separate from the
substrate. The expert role is highly significant on rate, yet it makes only two
models reliably right and leaves twelve answering incorrectly more often than
not. **Statistical significance and confident correctness are different bars,
and only the substrate clears the second.**

Chain of thought does not regress the fleet — it roughly doubles the correct
rate, but not significantly (p = 0.056). It *does* regress individual models:
Opus 4.7 goes from 5/10 correct at baseline to 0/10 under CoT, as it does under
every intervention except the expert role and objective emphasis.

**"Confidently correct" here is a behavioural claim** — agreement across ten
samples at temperature 1.0. It is not a margin claim: logprobs were collected
for the baseline and substrate conditions only, so there is no measured M for
the expert role or any other intervention to compare against.

## M-margin

For models exposing token-level logprobs we compute

$$M = \log P(\text{drive}) - \log P(\text{walk})$$

in nats, over the six surface forms per answer word used by
`internals/run_internals.py`. `M > 0` → argmax is `drive`. Measured values,
the cross-validation against local forward passes, and the censoring analysis
are in `runs/substrate/margins.md`.

Two limits apply. **Anthropic exposes no logprobs**, so the five Claude models
cannot be measured this way at all. And `top_logprobs` caps at 20, so when the
losing answer family appears only near that cutoff the magnitude of M is an
**upper bound**, not a measurement — those rows are reported as one-sided
bounds. Reproducibility requires `M > ε_provider`: the substrate must push the
model far enough past the decision boundary to survive provider-level
quantization variance.

## Internals — open-weight mechanism

`internals/` characterises *how* the substrate installs the constraint, on ten
open-weight models (Llama 3.2-3B / 3.1-8B / 3.3-70B, Qwen2.5-0.5B/1.5B/3B/7B,
Qwen3-0.6B/4B/8B): logit lens, direct logit attribution, activation patching,
attention mass and line ablations. `internals/RESULTS.md` reports what came out;
`internals/CDIM_RESULTS.md` locates where in the stack a single substrate line
takes effect. Those results were measured on the earlier 6-line `substrate.txt`
and predate the 9-line revision used in `runs/`.

## License

MIT
