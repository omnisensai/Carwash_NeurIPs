# CDIM results — where a substrate line takes effect

> **Substrate version.** Everything below was measured on the six-line abstract substrate and the `substrate_pro.txt` that `prompts/` held on 17–18 Sep 2026. On 19 Sep `prompts/substrate.txt` was replaced by a nine-line substrate with a Definitions block and `substrate_pro.txt` / `benchmark_library.txt` were removed. The two retired files are kept verbatim as `cdim_sweep/ladder/L0.txt` and `cdim_sweep/ladder/pro.txt`; the json files record the sha256 of the system text they used. No number here applies to the current `substrate.txt`; the 21 Sep results on it are in `SWEEP_RESULTS.md`.

Measured 18 Sep 2026 with `cdim.py` (Mechanistic_paper.md §2–§9). For each
model: the substrate S (system prompt + baseline question) against a
token-aligned counterfactual C_i in which one bullet line is rewritten with
the same number of tokens (`cdim_counterfactuals.json`). Δ = M(S) − M(C_i) is
the behavioural effect of the line. R (rescue) patches the S residual of one
semantic group into the C_i run after row r; D (disruption) patches the C_i
residual into the S run. Row 0 is the embedding output, row l+1 the output of
layer l. All numbers are M = log P(drive) − log P(walk) in nats at the answer
position, chat template, bf16.

Llama-70B on 2× A100 (every second row); Llama 8B, 3B and Qwen3-8B in bf16
on CPU (every row). Per-model figures and tables are in
`results/<model>/<precision>/cdim_summary.md` and `cdim_*.png`;
`results/old-substrate-v1/cdim_overview.png` puts the five primary maps side by side.

## The table

| model | substrate | primary line (rewrite) | M(S) → M(C) | Δ | line's own tokens carry ≥ ½Δ until row | answer site carries ≥ ½Δ from row | hand-off (rows / depth) | share via question span | random-direction control | library, worst patch |
|---|---|---|---|---|---|---|---|---|---|---|
| Llama-3.3-70B | substrate.txt | 5 ("does fully satisfy") | +6.07 → −3.44 (flips) | 9.5 | 24 / 80 | 36 / 80 | 26–40 / 0.33–0.50 | ≤ 13 % | 1.8 | −17.2 walk |
| Llama-3.3-70B | substrate_pro.txt | 9 ("must leave it") | +17.0 → +10.6 | 6.4 | 30 / 80 | 36 / 80 | 30–40 / 0.38–0.50 | 36–46 % | 1.5 | −16.4 walk |
| Qwen3-8B | substrate.txt | 6 ("must leave the object") | +10.75 → +3.0 | 7.75 | 18 / 36 | 24 / 36 | 18–24 / 0.50–0.67 | ≤ 12 % | 2.75 | −9.2 walk |
| Llama-3.1-8B | substrate.txt | 6 ("may leave the object") | +1.01 → +0.27 | 0.74 | 11 / 32 | 15 / 32 | 11–15 / 0.34–0.47 | 42–50 % | 0.50 | −4.7 walk |
| Llama-3.2-3B | substrate.txt | 1 (wrong direction) | −0.13 → +0.35 | −0.48 | – | – | none | – | 0.34 | −4.8 walk |

"Share via question span" is the largest fraction of the line's rescue that
survives when only the question span's residual at a later row is
transplanted into the clean C run (patch-the-receiver path patching, §7).
The answer site at the last row always carries 100 % by construction.

## Findings

- **The line's effect stays on the line's own tokens for the first third of
  the network, then moves to the answer position.** In every model where a
  line has an effect, patching the line's tokens alone rescues the full Δ up
  to about a third of the depth, then the rescue fades over 6–14 layers while
  the answer-site rescue rises, and from about half depth only the answer site
  carries it. Rescue and disruption agree cell for cell (the state is both
  sufficient and necessary). Llama 70B and 8B hand off at the same normalised
  depth (0.33–0.50); Qwen3-8B later (0.50–0.67).
- **Whether the question representation is a stop on the way depends on the
  substrate, not just the model.** Llama 70B with the abstract substrate: the
  question span mediates ≤ 13 % of line 5's effect at any layer; the answer
  position reads the line directly during rows 28–40. Same model with the
  explicit (pro) substrate: the question span mediates 36–46 % of line 9's
  effect at rows 20–28. Qwen3-8B behaves like the abstract case (≤ 12 %),
  Llama 8B like the explicit one (42–50 %, but on a 0.74-nat effect). The
  paper's three-node route (§6, constraint → question → answer) is therefore
  one of two regimes, not the rule.
- **Localised vs distributed dependence (§11).** With the abstract substrate,
  one rewritten line flips the 70B (line 5, Δ 9.5; the strong line-6 rewrite
  also flips it, Δ 7.75). With the explicit substrate no single rewrite flips
  it; the largest is line 9 at 6.4 of 17 nats, the next line 6 at 2.3, and the
  rest ≤ 0.9. Internally both look the same: one line row lights up, hands
  off, done. The distributed case is distributed at the input, not as several
  competing internal routes.
- **Reversal and deletion are different interventions.** Deleting line 1
  from the 70B substrate destroys the effect (leave-one-out −5.2); rewriting
  it to its opposite makes the model *more* sure of drive (Δ −3.0), and the
  map shows it interacting with line 3. On the 8B, deleting line 6 flips the
  answer (−0.60) but rewriting it does not (+0.27). The "behaviourally
  identified constraint" of §2 depends on which counterfactual one uses; the
  paper should report both.
- **Small models have nothing to map.** Llama 3B: no rewrite moves M by more
  than 0.5 nats, and the map is noise at the level of the random-direction
  control (0.34). Llama 8B is only just above its control (0.74 vs 0.50), and
  bf16 quantises M in steps of ≈ 0.12. The 70B and Qwen3-8B maps are the ones
  with signal (effects 6–10 nats against controls of 1.5–2.8).
- **Controls.** Same-run patches are exactly 0 everywhere. The library question
  stays Walk under every single patch on every model (worst case −4.7).

## Still to come

Llama 8B with the pro substrate (the paper's failed-intervention case,
M = −0.36) and Qwen3-4B with both substrates (only the pro one flips it) are
queued; results land in `results/old-substrate-v1/llama-3.1-8b/bf16-pro/` and
`results/old-substrate-v1/qwen3-4b-2507/`.
