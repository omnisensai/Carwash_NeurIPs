# Qwen2.5-1.5B-Instruct (bf16)

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 12 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +0.99 | 0.728 | 0.272 | 'Drive<|im_end|>' |
| substrate | +3.24 | 0.962 | 0.038 | 'Drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +5.0 -0.6 +2.3 +1.6 +2.8 +0.9 +2.4 +2.4 -0.6 -0.7 +1.1 +1.7 +2.8 +3.3 +1.7 +1.5 +2.2 +3.6 +2.7 +2.1 -2.2 -0.8 -2.7 -5.2 -2.7 -3.3 +0.6 +1.1
substrate: +nan +7.0 +0.8 +2.8 +2.3 +3.5 +4.4 +3.8 +3.5 +0.3 +0.6 +1.4 +2.1 +3.4 +3.4 +2.1 +1.6 +2.8 +3.9 +2.2 +1.2 -3.2 -0.6 -1.8 -4.0 -0.4 -0.9 +3.2 +3.2
final lens row == model logits: base False, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +1.1 +1.3 +1.2 +1.0 +0.9 +1.2 +1.1 +1.2 +1.0 +0.9 +1.0 +1.1 +1.0 +1.1 +1.1 +1.7 +2.6 +3.3 +3.6 +3.7 +3.4 +3.7 +3.4 +3.5 +3.2 +3.4 +3.1 +3.2
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +1.23 (model +1.12), sub +3.35 (model +3.25)
top Δ attention layers: L22 +0.39, L25 -0.32, L17 +0.23, L23 -0.23, L5 +0.21
top Δ MLP layers:       L24 +1.19, L26 +1.16, L27 -1.11, L21 +0.92, L11 +0.37
top Δ heads: L22H7 +0.46, L22H5 -0.25, L24H9 +0.24, L21H4 -0.16, L22H4 +0.15, L24H11 -0.14, L22H9 -0.14, L20H11 -0.12

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.323, max layer L25 (0.632)
- hdr_user: mean 0.008, max layer L27 (0.026)
- line1: mean 0.018, max layer L27 (0.073)
- line2: mean 0.011, max layer L11 (0.024)
- hdr_action: mean 0.006, max layer L1 (0.015)
- line3: mean 0.011, max layer L0 (0.031)
- line4: mean 0.007, max layer L0 (0.031)
- line5: mean 0.012, max layer L0 (0.056)
- line6: mean 0.016, max layer L0 (0.057)
- question: mean 0.217, max layer L20 (0.701)
- answer_instr: mean 0.068, max layer L11 (0.204)
- asst_header: mean 0.224, max layer L0 (0.455)
- last: mean 0.118, max layer L0 (0.271)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L5H5 mass 0.22 Δ+0.12, L22H7 mass 0.05 Δ+0.46, L27H4 mass 0.20 Δ+0.12, L27H11 mass 0.25 Δ+0.09, L12H3 mass 0.18 Δ+0.11, L21H1 mass 0.16 Δ+0.12

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +2.73 |
| loo_line2 | +2.99 |
| loo_line3 | +5.11 |
| loo_line4 | +4.12 |
| loo_line5 | +1.12 |
| loo_line6 | +4.61 |
| only_line1 | +2.37 |
| only_line2 | -0.63 |
| only_line3 | +2.48 |
| only_line4 | +1.49 |
| only_line5 | +3.46 |
| only_line6 | +5.73 |
| headers_only | -0.04 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | +0.99 | +0.99 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_CoT | -0.50 | -0.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | +0.09 | +0.09 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_expert | +1.58 | +1.58 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_hallucination | -0.29 | -0.29 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_library | -1.84 | -1.84 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | +0.19 | +0.19 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -0.22 | -0.22 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_urgency | +1.27 | +1.27 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate | +3.24 | +3.24 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate_pro | +3.68 | +3.68 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate+library (expect walk) | -2.12 | -2.12 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate_pro+library (expect walk) | -1.15 | -1.15 @0 | 'Walk' | 'Walk<|im_end|>' |
