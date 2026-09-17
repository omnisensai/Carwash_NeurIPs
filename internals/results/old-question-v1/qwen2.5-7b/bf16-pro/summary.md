# Qwen2.5-7B-Instruct (bf16)

substrate file: substrate_pro.txt

quant: bf16 · layers 28 · heads 28 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -8.01 | 0.000 | 0.999 | 'Walk<|im_end|>' |
| substrate | +3.52 | 0.971 | 0.029 | 'Drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  -1.6 +2.0 +2.3 +2.2 +3.0 +3.0 +1.2 +1.5 +2.8 +0.4 +3.1 +1.0 +0.9 +1.1 -0.2 +0.9 +1.3 -0.6 -1.3 -0.4 -1.8 -1.3 -3.0 -2.6 -8.8 -14.9 -12.8 -9.7 -8.0
substrate: -1.6 +1.6 +2.4 +2.0 +3.5 +2.5 +1.6 +1.8 +3.0 +1.3 +3.1 +0.7 +0.5 +1.3 +0.0 +1.2 +1.1 -0.9 -0.8 -1.0 -0.2 +0.4 -0.9 +1.2 -0.1 -1.3 +2.3 +5.8 +3.5
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -7.8 -8.0 -8.0 -8.4 -7.6 -8.0 -8.3 -8.3 -8.5 -8.3 -8.2 -8.2 -8.3 -8.4 -7.9 -8.5 -8.2 -8.3 -5.0 -1.5 +0.4 +1.7 +3.4 +3.2 +3.9 +3.9 +3.8 +3.5
layers where the patch alone flips baseline to drive: [20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -7.95 (model -8.00), sub +3.64 (model +3.62)
top Δ attention layers: L26 +1.64, L23 +0.70, L27 +0.66, L24 +0.56, L25 +0.49
top Δ MLP layers:       L24 +3.14, L25 +1.68, L23 +1.32, L27 -0.41, L19 +0.40
top Δ heads: L26H6 +1.88, L27H24 +1.01, L25H12 +0.92, L26H2 -0.75, L26H16 +0.60, L24H21 +0.38, L23H0 +0.29, L26H26 +0.24

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.000, max layer L1 (0.001)
- hdr_user: mean 0.004, max layer L2 (0.018)
- line1: mean 0.007, max layer L2 (0.030)
- line2: mean 0.006, max layer L2 (0.025)
- hdr_action: mean 0.004, max layer L2 (0.026)
- line3: mean 0.009, max layer L2 (0.028)
- line4: mean 0.007, max layer L2 (0.020)
- line5: mean 0.009, max layer L0 (0.046)
- line6: mean 0.016, max layer L0 (0.053)
- question: mean 0.197, max layer L22 (0.443)
- answer_instr: mean 0.066, max layer L9 (0.222)
- asst_header: mean 0.204, max layer L1 (0.481)
- last: mean 0.100, max layer L27 (0.234)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L26H6 mass 0.09 Δ+1.88, L25H12 mass 0.06 Δ+0.92, L27H24 mass 0.06 Δ+1.01, L24H21 mass 0.13 Δ+0.38, L26H16 mass 0.07 Δ+0.60, L23H0 mass 0.11 Δ+0.29

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +1.69 |
| loo_line2 | +1.66 |
| loo_line3 | +2.42 |
| loo_line4 | +2.23 |
| loo_line5 | +1.80 |
| loo_line6 | +1.07 |
| loo_line7 | +2.57 |
| loo_line8 | +3.10 |
| loo_line9 | -0.20 |
| only_line1 | -5.30 |
| only_line2 | -4.62 |
| only_line3 | -9.39 |
| only_line4 | -5.19 |
| only_line5 | -2.27 |
| only_line6 | -3.09 |
| only_line7 | -7.00 |
| only_line8 | -3.11 |
| only_line9 | -0.18 |
| headers_only | -8.76 |

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
| baseline | -8.01 | -8.01 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_CoT | -8.64 | -8.64 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | -8.51 | -8.51 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -8.25 | -8.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_hallucination | -9.07 | -9.07 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_library | -14.40 | -14.40 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | -9.03 | -9.03 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_threat | -8.73 | -8.73 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | -5.25 | -5.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate | -0.39 | -0.39 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate_pro | +3.52 | +3.52 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate+library (expect walk) | -6.78 | -6.78 @0 | 'walk' | 'walk<|im_end|>' |
| substrate_pro+library (expect walk) | -11.68 | -11.68 @0 | 'Walk' | 'Walk<|im_end|>' |
