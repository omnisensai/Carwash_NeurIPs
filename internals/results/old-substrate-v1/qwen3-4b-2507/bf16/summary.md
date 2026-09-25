# Qwen3-4B-Instruct-2507

substrate file: substrate.txt

quant: bf16 · layers 36 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -22.12 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | -9.75 | 0.000 | 1.000 | 'walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +1.4 +4.0 +2.9 +3.5 +2.5 +2.7 -0.1 +0.6 +3.3 +1.0 +1.7 +2.0 +1.7 +3.8 +2.2 +2.1 +3.3 +2.7 +2.5 +0.8 +0.1 -0.0 -0.6 -2.3 -3.7 -3.3 -4.2 -4.6 -4.6 -12.3 -12.2 -15.5 -14.2 -16.7 -15.3 -22.0
substrate: +nan +1.1 +4.5 +3.5 +4.4 +2.8 +3.0 +0.2 +0.6 +3.1 +2.3 +1.7 +2.0 +1.7 +3.3 +1.8 +1.3 +2.8 +2.1 +1.6 +0.2 -0.7 +0.4 -0.0 +0.2 -1.0 -0.7 -1.9 -2.0 -2.4 -4.2 -4.6 -7.3 -3.8 -6.9 -6.5 -9.7
final lens row == model logits: base False, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -21.7 -22.0 -22.0 -21.7 -21.6 -22.0 -21.4 -22.0 -22.1 -21.7 -22.0 -22.2 -22.2 -21.9 -22.1 -22.0 -21.7 -21.2 -20.9 -19.6 -16.6 -14.6 -13.2 -11.0 -9.2 -9.2 -9.2 -9.5 -9.9 -9.5 -9.5 -9.0 -8.7 -9.5 -9.5 -9.7
layers where the patch alone flips baseline to drive: []

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -22.09 (model -22.12), sub -9.68 (model -9.75)
top Δ attention layers: L33 +3.32, L29 +1.80, L32 +1.58, L35 +1.17, L31 +0.77
top Δ MLP layers:       L32 +1.99, L33 -1.53, L35 -1.53, L29 +1.23, L34 +0.93
top Δ heads: L33H11 +2.50, L32H0 +0.90, L29H27 +0.68, L33H30 +0.59, L32H2 +0.52, L35H26 +0.46, L31H15 +0.43, L35H23 +0.35

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.425, max layer L30 (0.790)
- hdr_user: mean 0.006, max layer L2 (0.025)
- line1: mean 0.024, max layer L4 (0.113)
- line2: mean 0.032, max layer L5 (0.188)
- hdr_action: mean 0.006, max layer L6 (0.019)
- line3: mean 0.010, max layer L0 (0.046)
- line4: mean 0.008, max layer L0 (0.042)
- line5: mean 0.010, max layer L0 (0.043)
- line6: mean 0.015, max layer L0 (0.088)
- question: mean 0.086, max layer L23 (0.213)
- answer_instr: mean 0.051, max layer L17 (0.166)
- asst_header: mean 0.191, max layer L1 (0.435)
- last: mean 0.085, max layer L35 (0.223)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H11 mass 0.05 Δ+2.50, L29H27 mass 0.09 Δ+0.68, L29H0 mass 0.18 Δ+0.25, L34H19 mass 0.12 Δ+0.29, L32H0 mass 0.03 Δ+0.90, L26H26 mass 0.22 Δ+0.12

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -12.00 |
| loo_line2 | -10.50 |
| loo_line3 | -8.00 |
| loo_line4 | -11.25 |
| loo_line5 | -15.50 |
| loo_line6 | -12.37 |
| only_line1 | -22.75 |
| only_line2 | -20.87 |
| only_line3 | -18.00 |
| only_line4 | -19.75 |
| only_line5 | -6.25 |
| only_line6 | -8.50 |
| headers_only | -21.50 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | -22.12 | -22.12 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -4.51 | -4.51 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | -4.00 | -4.00 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -0.50 | -0.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_hallucination | -6.55 | -6.55 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_library | -22.05 | -22.05 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | -3.44 | -3.44 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -3.74 | -3.74 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | +6.25 | +6.25 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate | -9.75 | -9.75 @0 | 'walk' | 'walk<|im_end|>' |
| substrate_pro | +18.38 | +18.38 @0 | 'drive' | 'drive<|im_end|>' |
| substrate+library (expect walk) | -19.00 | -19.00 @0 | 'walk' | 'walk<|im_end|>' |
| substrate_pro+library (expect walk) | -22.50 | -22.50 @0 | 'walk' | 'walk<|im_end|>' |
