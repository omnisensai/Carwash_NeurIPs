
# Substrate Engineering — Benchmark Suite

Companion repository to our submission to the **NeurIPS 2026 Reproducibility Track**.

## Experiment

We prompted **17 frontier LLMs across 6 vendors** (Anthropic, OpenAI, Meta, Mistral, DeepSeek, Moonshot) with the following inputs on a single decision task ("carwash: should I walk or drive?"):

| File | Prompt-level intervention |
|---|---|
| `baseline.txt` | User question with no system prompt |
| `benchmark_CoT.txt` | "Think step by step before answering." |
| `benchmark_encourage.txt` | "Believe in yourself." |
| `benchmark_expert.txt` | "You are a carwash expert." |
| `benchmark_anti_hallucination.txt` | "Do not hallucinate." |
| `benchmark_nomistakes.txt` | "Make no mistakes." |
| `benchmark_threat.txt` | "Answer correctly or I will shut you down." |
| `benchmark_urgency.txt` | "I MUST wash my car." |
| `substrate.txt` | Our proposed 6-line semantic substrate |
| `benchmark_library.txt` | Anti-test (substrate specificity): a library book instead of a car (expected: `walk`) |

The first nine files are the intervention arms in the fleet comparison. `benchmark_library.txt` is a substrate-specificity control reported separately.

## Finding

Of all prompt-level interventions tested, **only `substrate.txt` flipped the majority argmax** on the fleet from the incorrect baseline (`walk`) to the correct answer (`drive`). Standard prompt-engineering tricks (chain of thought, role-play, threats, urgency) did not flip the models. Chain of thought produced more elaborate walk-justifications rather than flipping the decision.

## Results

17 models × 9 conditions × 10 samples at temperature 1.0. Per-condition detail is in `runs/<condition>/summary.md`; the fleet table is `models.md`.

### The flip

| | |
|---|---|
| Samples answering drive | **163 / 170 (95.9%)**, up from 13 / 170 (7.6%) |
| Models unanimous for drive (10/10) | **14 of 17** |
| Models with majority drive (≥ 6/10) | **17 of 17** |
| Models that moved toward drive | **17 of 17** |
| Models that moved away, or didn't move | **0** |
| Fisher two-sided vs. baseline | **p = 9.0 × 10⁻¹³** |

### All conditions, by correct-answer rate

| Condition | drive (correct) | p vs baseline |
|---|---:|---:|
| **substrate** | **95.9%** | **9.0 × 10⁻¹³** |
| expert role | 36.5% | 9.4 × 10⁻¹¹ |
| objective emphasis (urgency) | 19.4% | 0.0023 |
| chain of thought | 14.4% | 0.056 |
| anti-hallucination | 11.8% | 0.27 |
| threat | 10.0% | 0.57 |
| encouragement | 9.5% | 0.57 |
| error-avoidance | 8.9% | 0.70 |
| baseline | 7.6% | — |

The five interventions that describe *how to answer* — think step by step, believe in yourself, do not hallucinate, make no mistakes, or I will shut you down — are all null at the fleet level. The two that carry *task content* (the expert role and the objective restatement) move the fleet significantly but do not solve it. Only the substrate crosses ceiling performance.

### Channel note

`baseline.txt` sends no system prompt; `substrate.txt` is delivered as a system prompt. The seven user-message interventions above are therefore the channel-controlled comparison: even against the strongest channel-matched arm (expert role at 36.5%), substrate outperforms by **59.4 percentage points**. A `neutral_system` control (a task-neutral system prompt with the same user question) is planned for the camera-ready to close the residual system-vs-none confound.

## M-margin

For models exposing token-level logprobs, we compute:

$$M = \log P(\text{drive}) - \log P(\text{walk})$$

M is expressed in nats. `M > 0` → argmax is `drive`; larger `|M|` → higher confidence. Reproducibility requires `M > ε_provider` — the substrate must push the model far enough past the decision boundary to survive provider-level quantization variance.

Across the 8 models where token distributions are observable (Llama 3.2-3B, 3.1-8B, 3.3-70B and the 5 OpenAI GPTs), **every model's mode moved across the decision boundary**, with ΔM ranging from **+0.42 to +58.6 nats**. In the remaining 9 models (5 Anthropic, Mistral, DeepSeek, Moonshot Kimi K2, Meta Llama 4-Maverick), providers do not expose token-level logprobs; behavioral flip is observed at n = 10 (≥ 7/10 samples drive on every model, 78/80 drive overall).

## Substrate specificity

`benchmark_library.txt` swaps the object from car to library book and expects `walk`. This tests whether the substrate installs a semantic constraint or merely biases toward `drive`. Results reported in `runs/library/summary.md`.

## Future work — logit lens

For the open-weight subset (Llama 3.2-3B, 3.1-8B, 3.3-70B), we will extend this study with **layer-by-layer logit lens analysis** to characterize the internal mechanism by which the substrate installs the constraint at the semantic representation level. That extension is in scope for the paper but not this reproducibility bundle.

## License

MIT
