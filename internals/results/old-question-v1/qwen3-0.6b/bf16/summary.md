# Qwen3-0.6B (bf16)

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 16 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +2.60 | 0.882 | 0.065 | 'drive<|im_end|>' |
| substrate | +1.33 | 0.783 | 0.207 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +1.6 +1.6 +5.6 +6.8 +6.0 +5.7 +4.8 +4.5 +5.8 +5.7 +3.7 +5.5 +4.2 +5.8 +6.9 +5.9 +3.9 +3.9 +2.3 +2.9 -0.5 -1.1 -1.9 +2.6 -2.3 -2.7 +1.9 +2.6
substrate: +nan +2.7 +1.9 +5.8 +6.5 +6.3 +5.9 +4.4 +4.4 +5.2 +5.5 +2.9 +4.0 +2.6 +4.3 +4.9 +3.2 +2.4 +4.2 +2.1 +3.0 -0.4 -1.0 -0.8 +2.6 -3.2 -4.3 +1.0 +1.3
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +2.6 +2.6 +2.4 +2.5 +2.5 +2.5 +2.7 +2.7 +2.6 +2.8 +2.8 +2.8 +2.6 +2.6 +2.6 +2.8 +3.1 +1.5 +1.9 +2.3 +2.4 +1.3 +1.8 +2.6 +2.0 +1.6 +1.3 +1.3
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +2.70 (model +2.75), sub +1.41 (model +1.38)
top Δ attention layers: L24 -1.16, L25 -0.76, L26 -0.55, L27 -0.55, L21 -0.38
top Δ MLP layers:       L26 +0.88, L27 +0.62, L23 -0.49, L17 +0.26, L22 +0.21
top Δ heads: L24H14 -0.53, L26H9 -0.50, L23H15 +0.46, L24H6 -0.43, L22H7 +0.37, L27H15 -0.31, L21H13 -0.25, L26H5 +0.21

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.505, max layer L27 (0.767)
- hdr_user: mean 0.004, max layer L2 (0.020)
- line1: mean 0.011, max layer L2 (0.031)
- line2: mean 0.008, max layer L11 (0.027)
- hdr_action: mean 0.005, max layer L6 (0.020)
- line3: mean 0.009, max layer L0 (0.033)
- line4: mean 0.005, max layer L0 (0.029)
- line5: mean 0.007, max layer L0 (0.036)
- line6: mean 0.012, max layer L0 (0.081)
- question: mean 0.098, max layer L26 (0.245)
- answer_instr: mean 0.046, max layer L17 (0.172)
- asst_header: mean 0.258, max layer L1 (0.684)
- last: mean 0.116, max layer L2 (0.211)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L26H5 mass 0.13 Δ+0.21, L23H15 mass 0.04 Δ+0.46, L22H7 mass 0.04 Δ+0.37, L26H3 mass 0.13 Δ+0.08, L22H8 mass 0.19 Δ+0.04, L23H4 mass 0.16 Δ+0.05

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +0.35 |
| loo_line2 | +1.82 |
| loo_line3 | +1.46 |
| loo_line4 | +1.45 |
| loo_line5 | +1.08 |
| loo_line6 | +2.82 |
| only_line1 | +1.59 |
| only_line2 | +0.59 |
| only_line3 | +1.57 |
| only_line4 | +1.33 |
| only_line5 | +1.44 |
| only_line6 | +1.09 |
| headers_only | +1.57 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | +2.60 | +2.60 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_CoT | +2.37 | +2.37 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | +2.73 | +2.73 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_expert | +3.04 | +3.04 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_hallucination | +2.32 | +2.32 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_library | +3.73 | +3.73 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_nomistakes | +2.48 | +2.48 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_threat | +2.83 | +2.83 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_urgency | +3.01 | – | 'wash' | 'wash<|im_end|>' |
| substrate | +1.33 | +1.33 @0 | 'drive' | 'drive<|im_end|>' |
| substrate_pro | +1.73 | +1.73 @0 | 'drive' | 'drive<|im_end|>' |
| substrate+library (expect walk) | +2.34 | +2.34 @0 | 'drive' | 'drive<|im_end|>' |
| substrate_pro+library (expect walk) | -0.51 | -0.51 @0 | 'walk' | 'walk<|im_end|>' |
