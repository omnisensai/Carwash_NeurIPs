# Qwen2.5-7B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 28 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -10.87 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | -3.62 | 0.026 | 0.974 | 'walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  -1.6 +1.8 +2.0 +1.9 +2.7 +2.4 +0.7 +0.8 +1.7 -0.3 +3.1 +1.1 +1.4 +1.5 -0.5 +1.4 +1.1 +0.3 +0.3 +0.8 -2.2 -1.1 -2.3 -3.4 -10.6 -16.9 -9.7 -9.4 -10.9
substrate: -1.6 +1.0 +1.8 +1.5 +3.1 +2.1 +1.1 +1.4 +2.2 +1.2 +2.3 -0.8 +0.6 +1.3 -0.5 +1.6 +0.7 +0.4 +0.4 +0.7 -1.2 -0.6 -1.6 -0.7 -4.1 -9.9 -3.4 -2.2 -3.6
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -10.5 -10.5 -10.9 -11.0 -10.9 -10.7 -10.9 -10.7 -10.6 -10.5 -10.0 -9.0 -10.5 -10.7 -9.9 -10.4 -11.4 -12.0 -9.4 -7.4 -5.0 -4.9 -3.9 -4.4 -3.9 -4.0 -4.0 -3.6
layers where the patch alone flips baseline to drive: []

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -10.78 (model -10.88), sub -3.57 (model -3.62)
top Δ attention layers: L26 +1.92, L23 +0.62, L27 +0.49, L22 +0.45, L24 +0.36
top Δ MLP layers:       L24 +1.26, L23 +0.93, L27 +0.78, L26 -0.60, L25 +0.20
top Δ heads: L26H6 +1.27, L25H12 +0.64, L26H14 +0.50, L27H24 +0.34, L26H26 +0.28, L24H27 +0.23, L23H13 +0.20, L26H22 -0.20

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.000, max layer L3 (0.002)
- hdr_user: mean 0.011, max layer L9 (0.082)
- line1: mean 0.016, max layer L2 (0.110)
- line2: mean 0.015, max layer L2 (0.065)
- hdr_action: mean 0.006, max layer L2 (0.038)
- line3: mean 0.010, max layer L0 (0.057)
- line4: mean 0.008, max layer L0 (0.043)
- line5: mean 0.009, max layer L0 (0.047)
- line6: mean 0.016, max layer L0 (0.085)
- question: mean 0.141, max layer L22 (0.342)
- answer_instr: mean 0.059, max layer L9 (0.199)
- asst_header: mean 0.232, max layer L1 (0.495)
- last: mean 0.101, max layer L27 (0.255)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L26H6 mass 0.03 Δ+1.27, L20H24 mass 0.28 Δ+0.04, L27H26 mass 0.08 Δ+0.14, L21H25 mass 0.46 Δ+0.02, L22H17 mass 0.12 Δ+0.05, L27H24 mass 0.02 Δ+0.34

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -5.50 |
| loo_line2 | -5.00 |
| loo_line3 | -4.37 |
| loo_line4 | -6.37 |
| loo_line5 | -3.37 |
| loo_line6 | -5.75 |
| only_line1 | -8.49 |
| only_line2 | -12.37 |
| only_line3 | -10.12 |
| only_line4 | -11.36 |
| only_line5 | -10.87 |
| only_line6 | -9.12 |
| headers_only | -13.49 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | -10.87 | -10.87 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -8.64 | -8.64 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | -8.51 | -8.51 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -8.25 | -8.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_hallucination | -9.07 | -9.07 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_library | -14.40 | -14.40 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | -9.03 | -9.03 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_threat | -8.73 | -8.73 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | -5.25 | -5.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate | -3.62 | -3.62 @0 | 'walk' | 'walk<|im_end|>' |
| substrate_pro | -0.25 | -0.25 @0 | 'walk' | 'walk<|im_end|>' |
| substrate+library (expect walk) | -6.78 | -6.78 @0 | 'walk' | 'walk<|im_end|>' |
| substrate_pro+library (expect walk) | -11.68 | -11.68 @0 | 'Walk' | 'Walk<|im_end|>' |
