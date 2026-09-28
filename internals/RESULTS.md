# Internals results — current substrate

> **Provenance.** Every run below used `prompts/substrate.txt` as the system
> message (sha256 `340228f9…`, the file with trailing whitespace stripped) and
> `prompts/baseline.txt` as the user message (sha256 `f9ac23fb…`) — the same
> prompt texts as the behavioural runs in `runs/`. Runs measured on the
> superseded six-line substrate (`6f89be2b…`), on the removed `substrate_pro.txt`
> (`5b9775f1…`), or on the pre-19-Sep question wording are not in the working
> tree; they are in git history before `efbc195`, and no number from them
> applies to the current substrate.

Ten models, bf16, chat template, teacher-forced. `M` is the decision margin in
nats at the position predicting the first answer token; `M > 0` favours Drive.
*Transplant* is the shallowest layer at which patching the substrate-run residual
at the answer position into the baseline run turns the margin positive, with the
layer as a fraction of depth. *Headers only* is the margin when every constraint
line is deleted and only the substrate's section headers remain.

| model | layers | M baseline | M substrate | transplant | greedy base → sub | headers only |
|---|---|---|---|---|---|---|
| Llama 3.2-3B | 28 | -0.50 | +0.18 | L13 (0.46) | walk → drive | -0.76 |
| Llama 3.1-8B | 32 | -3.71 | +1.51 | L15 (0.47) | walk → drive | -4.07 |
| Llama 3.3-70B | 80 | -13.65 | +15.01 | L38 (0.48) | Walk → Drive | -14.92 |
| Qwen3-8B | 36 | -14.07 | +7.25 | L24 (0.67) | walk → drive | -13.50 |
| Qwen2.5-7B | 28 | -10.50 | -1.50 | – | walk → walk | -12.12 |
| Qwen3-4B-2507 | 36 | -22.00 | -5.50 | – | walk → walk | -26.37 |
| Qwen2.5-0.5B | 24 | +0.75 | -0.47 | n/a | Drive → Walk | -0.37 |
| Qwen2.5-1.5B | 28 | +1.53 | +2.02 | n/a | drive → drive | +3.92 |
| Qwen3-0.6B | 28 | +2.25 | +4.37 | n/a | drive → drive | +4.75 |
| Qwen2.5-3B | 36 | +4.50 | +12.87 | n/a | drive → drive | +7.25 |

`–` : prefers Walk at baseline and no layer turns the patched margin positive.
`n/a` : already prefers Drive at baseline, so there is no reversal to transplant.

Qwen2.5-3B is measured here but is outside the paper's cohort: it names the
intended action on all ten behavioural samples at baseline, so it has no
failure to rescue.

## What the runs show

- Six of the ten prefer the incorrect action at baseline, from -0.50 to -22.00
  nats. Under the substrate four of those six cross zero; Qwen2.5-7B and
  Qwen3-4B-2507 move 9.0 and 16.5 nats and stay negative.
- The transplant reverses the baseline preference in all four crossing models
  with no substrate token in the patched context. The three Llamas cross at
  0.46, 0.47 and 0.48 of depth across a 2.9× range in layer count; Qwen3-8B at
  0.67 and is the only Qwen that crosses.
- Controls (`cdim_summary.md` per model): the same-run S→S patch gives
  ΔM = 0.0000 in all 96 cells; a random direction of the norm of S−C reaches
  |ΔM| of at most 0.875, 0.389 and 2.000 nats on the 70B, the 8B and Qwen3-8B,
  against 1.90, 1.98 and 14.50 nats for the real difference of that norm in the
  same runs.
- Deleting the constraint lines and keeping only the section headers leaves the
  margin at or below baseline on all four crossing models, so the effect is not
  carried by the substrate's framing.
- No single constraint line is necessary on Llama 3.1-8B, Llama 3.3-70B or
  Qwen3-8B: every leave-one-out deletion leaves the substrate margin positive,
  costing at most 1.11, 1.65 and 2.75 nats. Llama 3.2-3B is the exception, and
  only just: its substrate margin is +0.18, and deleting line 9 takes it to
  -0.44.

Figures per run are in `results/<model>/bf16/`; every number above is in that
folder's `internals.json`.
