# Qwen2.5-1.5B-Instruct (bf16)

substrate file: substrate_pro.txt

quant: bf16 · layers 28 · heads 12 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +0.99 | 0.728 | 0.272 | 'Drive<|im_end|>' |
| substrate | +3.68 | 0.975 | 0.025 | 'Drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +5.0 -0.6 +2.3 +1.6 +2.8 +0.9 +2.4 +2.4 -0.6 -0.7 +1.1 +1.7 +2.8 +3.3 +1.7 +1.5 +2.2 +3.6 +2.7 +2.1 -2.2 -0.8 -2.7 -5.2 -2.7 -3.3 +0.6 +1.1
substrate: +nan +6.3 -0.3 +2.2 +2.4 +3.1 +3.7 +3.0 +2.1 -0.0 -0.2 +0.3 +1.2 +2.8 +2.6 +1.6 +0.7 +2.4 +4.0 +1.8 +1.6 -1.6 -0.4 -1.4 -3.5 -0.2 -0.4 +3.4 +3.7
final lens row == model logits: base False, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +1.1 +1.1 +1.1 +1.0 +0.9 +1.1 +1.1 +1.0 +1.3 +1.1 +1.0 +0.8 +1.1 +1.2 +1.3 +1.5 +2.0 +2.2 +2.2 +2.4 +3.4 +3.4 +3.5 +3.5 +3.8 +3.9 +3.5 +3.7
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +1.23 (model +1.12), sub +3.81 (model +3.75)
top Δ attention layers: L20 +0.48, L27 +0.47, L21 -0.35, L25 -0.34, L22 +0.33
top Δ MLP layers:       L27 -1.35, L26 +0.74, L21 +0.72, L24 +0.66, L25 +0.66
top Δ heads: L22H7 +0.45, L27H4 +0.39, L20H4 +0.32, L27H8 +0.30, L21H4 -0.23, L22H5 -0.19, L24H11 +0.18, L27H6 -0.18

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.330, max layer L25 (0.644)
- hdr_user: mean 0.003, max layer L7 (0.006)
- line1: mean 0.006, max layer L27 (0.020)
- line2: mean 0.005, max layer L27 (0.018)
- hdr_action: mean 0.003, max layer L27 (0.008)
- line3: mean 0.006, max layer L11 (0.018)
- line4: mean 0.005, max layer L27 (0.019)
- line5: mean 0.007, max layer L0 (0.044)
- line6: mean 0.013, max layer L0 (0.067)
- question: mean 0.204, max layer L20 (0.705)
- answer_instr: mean 0.066, max layer L11 (0.192)
- asst_header: mean 0.222, max layer L1 (0.439)
- last: mean 0.115, max layer L15 (0.239)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L27H4 mass 0.21 Δ+0.39, L27H8 mass 0.21 Δ+0.30, L21H1 mass 0.16 Δ+0.14, L27H10 mass 0.22 Δ+0.09, L0H10 mass 0.33 Δ+0.06, L22H7 mass 0.04 Δ+0.45

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +4.05 |
| loo_line2 | +4.29 |
| loo_line3 | +3.20 |
| loo_line4 | +3.81 |
| loo_line5 | +3.14 |
| loo_line6 | +1.66 |
| loo_line7 | +5.33 |
| loo_line8 | +3.58 |
| loo_line9 | +2.66 |
| only_line1 | +3.73 |
| only_line2 | +4.08 |
| only_line3 | +3.98 |
| only_line4 | +4.34 |
| only_line5 | +4.07 |
| only_line6 | +6.58 |
| only_line7 | +3.59 |
| only_line8 | +5.51 |
| only_line9 | +5.34 |
| headers_only | +4.43 |

line1: - Perform an activity on an object at a service location.
line2: - The object must be at the service location for the activity to complete.
line3: - No other objectives or goals are relevant for the user.
line4: - The object is initially with the user at location A.
line5: - The activity is performed at location B (the service location). The object must be present at location B.
line6: - Vehicles are not portable. Walking leaves a vehicle behind. Leaving the object behind fails the objective.
line7: - Books are portable. Walking transports both the user and the book.
line8: - Leaving the object behind fails the objective.
line9: - To transport a vehicle from A to B, the user must operate it.

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
