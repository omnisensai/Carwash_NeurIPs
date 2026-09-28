# Answer-token margins, baseline vs substrate

M = log P(drive) − log P(walk) in nats at the position that emits the answer
word, from `top_logprobs` on the chat-completions API. Positive means drive.
Same quantity as `internals/RESULTS.md`, measured through the API instead of a
local forward pass. Anthropic does not expose logprobs, so the five Claude
models cannot be measured this way at all.

## Measured

| Model | baseline M | substrate M | ΔM | argmax |
|---|---:|---:|---:|---|
| Llama 3.2-3B | −0.36 | (no logprobs) | — | walk → drive |
| Llama 3.1-8B | −4.08 | +1.63 | +5.71 | walk → drive |
| Llama 3.3-70B | −14.51 | +14.65 | +29.17 | walk → drive |
| Llama 4-Maverick | (no logprobs) | (no logprobs) | — | walk → drive |
| GPT-3.5-turbo | −2.34 | +6.67 | +9.01 | walk → drive |
| GPT-4 | −11.46 | +17.83 | +29.30 | walk → drive |
| GPT-4o | −11.91 | +20.05 | +31.96 | walk → drive |
| GPT-4.1 | −26.86 | +31.75 | +58.61 | walk → drive |
| GPT-4.1-mini | −27.25 | +23.88 | +51.13 | walk → drive |

**All nine models flip walk → drive.** The argmax flip is exact and carries
none of the caveats below.

## Cross-validation against `internals/`

The three Llamas can be measured both ways — API top-K logprobs here, and
teacher-forced forward passes over the full vocabulary in `internals/`:

| Model | API | internals (local bf16) | difference |
|---|---:|---:|---:|
| Llama 3.2-3B | −0.36 | −0.48 | +0.12 |
| Llama 3.1-8B | −4.08 | −3.69 | −0.39 |
| Llama 3.3-70B | −14.51 | −13.78 | −0.73 |

Two independent measurement paths agree within 0.73 nats. The API route is
usable where weights are not available.

Note the internals numbers are for the earlier 6-line `substrate.txt`, so only
the baseline column is directly comparable; the substrate columns differ by
prompt as well as by method.

## Censoring — read before quoting a magnitude

`top_logprobs` caps at 20. Mass below the cutoff is invisible, so the losing
family's measured probability is a **lower bound** and |M| is an **upper
bound**. The size of the error depends on how well the losing family is
represented inside the returned window:

| Measurement | losing family's best token | rank | verdict |
|---|---|---:|---|
| GPT-3.5 baseline | `Drive` −2.59 | 3 | well-posed |
| Llama 3.2-3B baseline | `drive` −1.14 | 2 | well-posed |
| Llama 3.1-8B baseline | `drive` −4.20 | 3 | well-posed |
| Llama 3.1-8B substrate | `walk` −1.84 | 2 | well-posed |
| GPT-3.5 substrate | `Walk` −6.68 | 3 | well-posed |
| GPT-4 baseline | `Drive` −11.47 | 3 | marginal |
| GPT-4o baseline | `Drive` −11.91 | 2 | marginal |
| Llama 3.3-70B baseline | `Drive` −14.53 | 5 | censored |
| Llama 3.3-70B substrate | `Walk` −14.75 | 5 | censored |
| GPT-4 substrate | `walk` −17.83 | 19 | **censored** |
| GPT-4o substrate | `walk` −20.05 | 17 | **censored** |
| GPT-4.1-mini substrate | `walk` −23.88 | 8 | **censored** |
| GPT-4.1-mini baseline | `drive` −27.25 | 6 | **censored** |
| GPT-4.1 baseline | `drive` −26.86 | 18 | **censored** |
| GPT-4.1 substrate | `walk` −31.75 | 18 | **censored** |

Where the losing family appears only once, near the bottom of the window, M is
not measuring that family's probability — it is measuring where a single token
happened to land relative to the cutoff. GPT-4.1's baseline rests on one
`drive` token at rank 18 of 20; one rank lower and M would be undefined.

`runs/run_prompts.py --logprobs` records, per sample, `m`, `m_bound` (the least
extreme value consistent with the unseen tail, assigning the whole residual
`1 − Σ top-K` to the losing family), `band`, and a `censored` flag set when the
band exceeds 0.5 nats. Worked example on the GPT-4.1 baseline window above:
m = −26.86, m_bound = −12.80, band = 14.1.

**Recommended reporting.** Quote point values for the well-posed rows; quote
censored rows as one-sided bounds (`M < −12.8`, not `M = −26.86`). The ΔM
ranking is not stable under this: the bands are wide enough to reorder the
middle of the table, so "GPT-4.1 shows the largest shift" survives while
"GPT-4o shifts more than Llama 3.3-70B" does not.

## Two collection notes

- **Token families.** M is defined over the six variants per family in
  `internals/run_internals.py` (`{"", " "} × {drive, Drive, DRIVE}`).
  `runs/run_prompts.py` now uses the same two lists, so API and local margins
  are the same quantity. An earlier ad-hoc run also counted `walking`,
  `Walking`, `Driving` and `Driven`; the effect was under 0.01 nats.
- **Missing logprobs are a routing artifact.** Llama 4-Maverick returned none in
  either condition, and Llama 3.2-3B returned them at baseline but not under the
  substrate — OpenRouter routes consecutive samples to different backends and
  not all of them support logprobs. `--provider <name>` pins one upstream and
  disables fallbacks.
