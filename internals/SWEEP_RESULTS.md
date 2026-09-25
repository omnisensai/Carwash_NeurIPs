# 21 Sep 2026 — the nine-line substrate, the explicitness ladder, paraphrases, scenarios, the 8B family, and the drive-frame direction

One pod (2× H100 80 GB, bf16, 06:55–18:40 UTC). Everything is M = log P(drive) − log P(walk)
in nats at the answer position, chat template, teacher-forced, on the current `prompts/`
(nine-line `substrate.txt`, question tail "walk or drive"). Per-run tables: `results/<model>/bf16/summary.md`,
`cdim_summary.md`; sweeps: `results/<model>/bf16-sweep/sweep_summary.md`; frames:
`results/<model>/bf16-frame/frame_summary.md`; the family gate: `results/family_gate.log`.
Ladder levels are in `cdim_sweep/ladder/` (L0 = the retired six-line abstract substrate, S = the current
`substrate.txt`, pro = the retired `substrate_pro.txt`); the 17–18 Sep results on L0/pro live in
`results/old-substrate-v1/` and appear here as the L0 and pro rows.

## 1. The new substrate, four models

| model | baseline | substrate S | API (runs/substrate/margins.md) | patch flips from layer | reversing one line |
|---|---|---|---|---|---|
| Llama-3.2-3B | −0.50 | +0.18 drive | (no logprobs) | – | – |
| Llama-3.1-8B | −3.71 | +1.51 drive | +1.63 | 15 / 32 | line 9 ("must operate it" → "may leave it") back to walk (Δ 2.0); line 7 Δ 1.4 |
| Llama-3.3-70B | −13.65 | +15.01 drive | +14.65 | 38 / 80 | **no single line**: max Δ 1.9 of 15 (line 9, then 5, 3, 6); leave-one-out ≥ +13.4 |
| Qwen3-8B | −14.07 | +7.25 drive | – | 24 / 36 | line 7 ("walking leaves a vehicle behind" → "brings it along") alone drops it to −7.25 (Δ 14.5); line 9 Δ 6.5 |

The local and API margins agree within 0.4 nats on the two models that have both. The old six-line
substrate left the 3B at −0.01; the new one flips it. On the 70B the new substrate is redundant (every
rule backs up the others, no line necessary), where the old one hung on one line (reverse line 5 → walk);
on Qwen3-8B one line still carries it. Where a single line shows up, it is line 7 or 9, the two that say
what walking does to a vehicle; the goal lines and the definitions never matter on their own.

## 2. The explicitness ladder (carwash question, CDIM map per level)

Δ = effect of reversing the primary line; "line until / answer from" = last row where the line's own tokens
carry ≥ ½Δ and first row where the answer site does, as a fraction of depth; "via question" = largest
fraction of the line's rescue that the question span carries alone (path patching); control = the paired
walk question under the same substrate stays Walk under every patch.

**Llama-3.3-70B**

| level | M | primary line, Δ | flips | line until | answer from | via question | control |
|---|---|---|---|---|---|---|---|
| L0 abstract | +6.1 | 5, +9.5 | yes | 0.30 | 0.45 | 18 % | walk |
| L1 + answer verbs | +5.2 | 6, +10.3 | yes | 0.35 | 0.50 | 38 % | walk |
| L2 + examples | **−0.7 walk** | 1, −11.1 | yes | 0.20 | 0.50 | 63 % | walk |
| L3 concrete nouns | +11.5 | 6, +19.4 | yes | 0.33 | 0.50 | 20 % | walk |
| L4 + consequences | +21.6 | 5, +28.1 | yes | 0.35 | 0.42 | 15 % | walk |
| L5 + verdict | +23.2 | 6, +38.4 | yes | 0.38 | 0.45 | 7 % | walk |
| S (official) | +15.0 | 9, +1.9 | no | 0.35 | 0.45 | 63 % | walk |
| pro (retired) | +17.0 | 9, +6.5 | no | 0.38 | 0.45 | 64 % | walk |

**Qwen3-8B**

| level | M | primary line, Δ | flips | line until | answer from | via question | control |
|---|---|---|---|---|---|---|---|
| L0 | +10.8 | 6, +7.8 | no | 0.50 | 0.67 | 27 % | walk |
| L1 | +7.3 | 6, +8.8 | yes | 0.50 | 0.69 | 26 % | walk |
| L2 | +7.5 | 6, +11.5 | yes | 0.53 | 0.69 | 25 % | walk |
| L3 | +23.3 | 6, +31.5 | yes | 0.53 | 0.67 | 12 % | walk |
| L4 | +30.0 | 5, +33.8 | yes | 0.53 | 0.64 | 16 % | **drive** |
| L5 | +33.9 | 6, +58.9 | yes | 0.53 | 0.67 | 2 % | **drive** |
| S | +7.3 | 7, +14.5 | yes | 0.42 | 0.69 | 35 % | walk |

Findings.

- **Prediction H1 is rejected.** The share carried by the question span does not rise with explicitness;
  for the concrete levels it falls (70B: 20 → 15 → 7 %; Qwen: 12 → 16 → 2 %). The more explicitly a line
  states the rule, the more directly the answer position reads it. The two definition-style substrates
  (S, pro) have the highest shares (63–64 %) but also the smallest per-line effects (Δ 1.9 / 6.5 against
  a random-direction control of 0.9 / 1.5), so on them the share is a ratio of two small numbers. Across
  all cells the share tracks 1/Δ more than it tracks the wording.
- **The hand-off depth does not move.** On the 70B the line's own tokens carry the effect until 0.30–0.38
  of depth and the answer site from 0.42–0.50 at every level, every paraphrase and every scenario
  (the one exception is L2, which the 70B answers Walk). Qwen: 0.50–0.53 → 0.64–0.69 throughout.
  The depth at which the rule leaves its tokens is a property of the model, not of the wording.
- **Explicitness buys margin, and on Qwen it costs selectivity.** Qwen L4 and L5 (consequences,
  verdict) push the library / parcel / prescription questions to Drive too (grid B: +8 to +13 nats), and
  their CDIM controls go Drive. The 70B never leaks under any level. S and L2 do not leak on either model.
- **L2 is a surprise:** adding "(for example a car)" style examples to the abstract substrate makes the
  70B say Walk (−0.7); every other level says Drive. Reversing line 1 of L2 makes it *more* Drive.

## 3. Paraphrases and scenarios (70B, substrate S)

Behavioural grid, 36 wordings (12 bodies × 3 tails) per scenario:

| substrate | drive tasks P(drive) | walk tasks P(drive) | carwash M min / median / max | tail effect (max−min of the mean) |
|---|---|---|---|---|
| none | 0.11 | 0.00 | −18.0 / −12.3 / −2.8 | 3.2 |
| L0 | 0.90 | 0.00 | −8.0 / +14.0 / +19.0 | 2.9 |
| S | 0.98 | 0.00 | +10.8 / +16.4 / +21.3 | 2.8 |
| L5 | 1.00 | 0.00 | | |
| pro | 1.00 | 0.00 | +14.1 / +19.0 / +26.2 | 4.1 |

Under S every one of the 36 carwash wordings says Drive and the spread (sd 2.5) is narrower than
without a substrate (sd 3.2). The three answer tails move the 70B by at most 4 nats. On Qwen3-8B the
tails move it by 10–20 nats ("drive or walk" pushes it to Drive), and walk tasks reach P(drive) 0.22–0.33
under L0 / S, so the selectivity the paper wants holds on the 70B and only partly on Qwen.

CDIM cells on S (13 paraphrases, 6 scenarios): M(S) from +2.0 (parking) to +18.1; hand-off 0.25–0.38 →
0.42–0.50 in every cell; primary line 9, 5 or 6 with Δ 1.6–3.9 (parking: reversing line 7 makes it more
Drive, Δ −7.2); question share 14–64 % (noise at these Δ); every control stays Walk. `sweep_stability.png`:
the depth is flat in M(S), the share scatters.

## 4. The 8B family (same architecture, eleven subjects; gate only)

Baseline vs S, one pass each, bf16. Pass = substrate moves M by ≥ 3 nats and lands on Drive.

| subject | baseline | S | |
|---|---|---|---|
| Llama-3-8B-Instruct | −9.6 | +0.8 | pass |
| Llama-3.1-8B-Instruct | −3.7 | +1.5 | pass |
| Hermes-2-Pro (Llama-3) | −7.3 | +5.4 | pass |
| Hermes-3 (Llama-3.1) | −5.1 | +3.0 | pass |
| Tulu-3 | −4.8 | +0.9 | pass |
| Tulu-3.1 | −2.0 | +2.6 | pass |
| Dolphin 2.9.4 | −1.2 | −0.7 | **fail** (ignores the one-word instruction: "I need to wash…") |
| Llama-3.1-8B abliterated | −7.5 | +2.1 | pass |
| OpenBioLLM-8B | – | – | no chat template, could not run |
| Storm-8B | −6.2 | +5.7 | pass |
| Lexi-Uncensored-V2 | −2.7 | +1.1 | pass |

Nine of ten measurable subjects flip, every one from a clear Walk. Maps for the nine are not run yet
(`run_family_8b.sh` does them; ~15 min per subject on one card).

## 5. The drive-frame direction (brainscope, §"concepts in layers")

A per-layer direction extracted with brainscope's `pca_directions` from 84 contrast pairs (each vehicle
question answered with a drive rationale vs a walk rationale), then every condition's prompt projected
on it at the answer position. Departure = first layer from which the condition sits > 3 sd outside the
bundle of the nine prompt-only conditions; lens = first row from which the logit lens stays > 0.

| model | prompt-only conditions (baseline, CoT, expert, goal, threat, …) | every substrate condition (L0–L5, S, pro) | lens |
|---|---|---|---|
| Llama-3.3-70B | never leave the bundle, expert (M −5.5) and goal (−4.7) included | depart at layer 30–34 | 48–79 |
| Llama-3.1-8B | never | depart at layer 14 | 17–30 |
| Qwen3-8B | never | separated by layer 13 (z 5–8), not sustained to the end | 19–33 |

So the persona / goal / threat prompts, which move the margin by up to 9 nats on the 70B, do not touch
the frame direction at all; every substrate does, at the same layer regardless of how it is written,
and 15–45 layers before the lens can read the answer. The departure layers (31 / 14) match the
answer-site patch-flip layers (38 / 15). Caveat: the contrast completions start with the answer word,
so the early-layer direction (d' peak at layer 13 / 10 / 3) is lexical; the mid-stack direction is what
the table uses. A refit with the rationale first and the answer last is queued.

## Not done / caveats

- Mistral Large (cut for time); maps for the nine 8B passers; the frame refit; token-level zoom on the
  decisive line.
- On S the per-line effects on the 70B are at the noise floor (Δ ≤ 1.9 vs control 0.9): the S map is a
  distributed-effect map and its route shares should not be quoted.
- Interrupted: the family sweep at Llama-3-8B (partial `results/llama-3-8b/bf16-sweep/`).
