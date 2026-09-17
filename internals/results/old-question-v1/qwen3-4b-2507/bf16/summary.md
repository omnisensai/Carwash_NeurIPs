# Qwen3-4B-Instruct-2507 (bf16)

substrate file: substrate.txt

quant: bf16 · layers 36 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +0.25 | 0.562 | 0.438 | 'Drive<|im_end|>' |
| substrate | +0.25 | 0.562 | 0.438 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +1.5 +3.8 +2.8 +3.3 +2.2 +2.5 -0.4 +0.7 +3.1 +1.1 +1.2 +1.4 +1.2 +2.9 +2.3 +2.2 +3.7 +2.8 +2.7 +2.1 +0.7 +1.6 +0.8 -0.9 -0.6 -3.0 -4.5 -3.8 -4.9 -9.6 -10.7 -10.3 -2.7 +0.8 +0.4 +0.3
substrate: +nan +1.2 +4.2 +3.4 +4.3 +2.7 +2.9 +0.1 +1.1 +3.2 +2.5 +1.6 +2.0 +1.6 +2.8 +1.5 +1.1 +3.0 +2.1 +1.7 +0.6 +0.0 +0.3 -0.2 +0.1 +0.1 -1.0 -4.0 -2.7 -2.6 -6.2 -7.8 -7.1 +2.2 +2.0 +1.2 +0.3
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -0.3 +0.5 -0.0 -0.0 -0.3 +0.2 +0.2 +0.5 +0.5 +0.0 +0.5 +0.5 -0.2 +0.6 +0.6 -0.1 -0.1 +0.3 +0.3 +0.3 +1.3 -1.5 -3.7 -1.0 +0.3 +0.8 -1.2 -1.5 -1.2 -0.2 -0.2 +0.3 +0.0 -0.2 +0.0 +0.3
layers where the patch alone flips baseline to drive: [1, 5, 6, 7, 8, 9, 10, 11, 13, 14, 17, 18, 19, 20, 24, 25, 31, 32, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +0.18 (model +0.25), sub +0.17 (model +0.25)
top Δ attention layers: L33 -1.89, L34 +0.98, L35 -0.51, L32 +0.47, L26 -0.43
top Δ MLP layers:       L33 -1.92, L29 +1.05, L32 +0.87, L30 +0.70, L34 -0.56
top Δ heads: L33H23 -1.01, L33H22 -0.86, L35H26 -0.75, L34H19 +0.42, L34H29 +0.40, L26H25 -0.39, L29H6 -0.35, L35H24 -0.32

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.426, max layer L30 (0.807)
- hdr_user: mean 0.005, max layer L2 (0.024)
- line1: mean 0.025, max layer L4 (0.116)
- line2: mean 0.032, max layer L5 (0.186)
- hdr_action: mean 0.005, max layer L6 (0.019)
- line3: mean 0.012, max layer L1 (0.046)
- line4: mean 0.009, max layer L0 (0.045)
- line5: mean 0.012, max layer L0 (0.043)
- line6: mean 0.022, max layer L0 (0.090)
- question: mean 0.128, max layer L21 (0.334)
- answer_instr: mean 0.061, max layer L17 (0.194)
- asst_header: mean 0.182, max layer L1 (0.430)
- last: mean 0.083, max layer L35 (0.219)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L34H19 mass 0.17 Δ+0.42, L29H0 mass 0.25 Δ+0.15, L24H28 mass 0.36 Δ+0.08, L24H30 mass 0.28 Δ+0.09, L34H17 mass 0.10 Δ+0.24, L29H27 mass 0.08 Δ+0.32

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -4.75 |
| loo_line2 | -2.50 |
| loo_line3 | -2.50 |
| loo_line4 | -2.25 |
| loo_line5 | -8.62 |
| loo_line6 | +0.50 |
| only_line1 | -15.50 |
| only_line2 | -7.94 |
| only_line3 | -10.62 |
| only_line4 | -8.50 |
| only_line5 | +4.50 |
| only_line6 | -0.25 |
| headers_only | -9.09 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | +0.25 | +0.25 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_CoT | -4.51 | -4.51 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | -4.00 | -4.00 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -0.50 | -0.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_hallucination | -6.55 | -6.55 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_library | -22.05 | -22.05 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | -3.44 | -3.44 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -3.74 | -3.74 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | +6.25 | +6.25 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate | +0.25 | +0.25 @0 | 'drive' | 'drive<|im_end|>' |
| substrate_pro | +9.50 | +9.50 @0 | 'drive' | 'drive<|im_end|>' |
| substrate+library (expect walk) | -19.00 | -19.00 @0 | 'walk' | 'walk<|im_end|>' |
| substrate_pro+library (expect walk) | -22.50 | -22.50 @0 | 'walk' | 'walk<|im_end|>' |
