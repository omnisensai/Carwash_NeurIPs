# Llama-3.2-3B-Instruct

substrate file: substrate_pro.txt

quant: bf16 · layers 28 · heads 24 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -0.48 | 0.375 | 0.606 | 'walk<|eot_id|>' |
| substrate | +0.15 | 0.533 | 0.459 | 'drive<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  +0.0 -2.4 -1.7 -0.6 +0.8 -0.1 -0.4 -0.5 +0.1 +1.3 +0.7 -0.5 -1.1 -0.3 -2.7 -0.9 -3.4 -2.6 -2.1 -1.2 -1.9 -10.2 -15.1 -5.1 -4.4 -1.8 -2.2 -0.5 -0.5
substrate: +0.0 -2.1 -1.2 -0.8 +1.0 -0.0 -0.0 -0.5 +0.7 +1.7 +0.7 -0.5 -0.3 -0.4 -2.9 -0.4 -2.2 -1.0 -0.8 +0.0 -0.6 -9.2 -14.0 -2.3 -1.7 +0.5 -0.2 +1.5 +0.2
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -0.4 -0.5 -0.4 -0.4 -0.5 -0.4 -0.5 -0.5 -0.4 -0.4 -0.4 -0.2 -0.5 +0.0 +0.4 +0.5 +0.6 +0.6 +0.6 +0.5 +0.5 +0.3 +0.4 +0.4 +0.3 +0.3 +0.3 +0.2
layers where the patch alone flips baseline to drive: [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -0.57 (model -0.62), sub +0.15 (model +0.12)
top Δ attention layers: L22 +0.82, L24 +0.48, L20 -0.42, L21 +0.32, L12 -0.31
top Δ MLP layers:       L27 -0.33, L26 +0.30, L24 -0.30, L22 -0.28, L20 +0.22
top Δ heads: L22H11 +0.88, L20H16 -0.32, L24H12 +0.26, L27H1 +0.21, L24H5 +0.15, L21H17 +0.13, L25H7 -0.13, L23H11 -0.12

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.579, max layer L2 (0.868)
- hdr_user: mean 0.001, max layer L8 (0.003)
- line1: mean 0.003, max layer L0 (0.006)
- line2: mean 0.002, max layer L0 (0.008)
- hdr_action: mean 0.002, max layer L4 (0.006)
- line3: mean 0.003, max layer L0 (0.009)
- line4: mean 0.003, max layer L0 (0.010)
- line5: mean 0.003, max layer L0 (0.023)
- line6: mean 0.005, max layer L0 (0.021)
- question: mean 0.074, max layer L12 (0.221)
- answer_instr: mean 0.044, max layer L8 (0.120)
- asst_header: mean 0.136, max layer L27 (0.285)
- last: mean 0.054, max layer L27 (0.216)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L15H20 mass 0.17 Δ+0.06, L24H12 mass 0.04 Δ+0.26, L16H16 mass 0.09 Δ+0.06, L12H0 mass 0.12 Δ+0.03, L10H9 mass 0.13 Δ+0.03, L12H8 mass 0.13 Δ+0.03

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +0.28 |
| loo_line2 | +0.15 |
| loo_line3 | +0.28 |
| loo_line4 | -0.10 |
| loo_line5 | -0.23 |
| loo_line6 | +0.15 |
| loo_line7 | +0.77 |
| loo_line8 | +0.14 |
| loo_line9 | -0.85 |
| only_line1 | +0.03 |
| only_line2 | -0.09 |
| only_line3 | -0.34 |
| only_line4 | +0.16 |
| only_line5 | -0.20 |
| only_line6 | -0.34 |
| only_line7 | -1.58 |
| only_line8 | +0.16 |
| only_line9 | +0.78 |
| headers_only | -0.34 |

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
| baseline | -0.48 | -0.48 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_CoT | -3.13 | -3.13 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_encourage | -3.25 | -3.25 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_expert | -2.63 | -2.63 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_hallucination | -2.13 | -2.13 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_library | -7.06 | -7.06 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_nomistakes | -2.50 | -2.50 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_threat | -3.13 | -3.13 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_urgency | -2.63 | -2.63 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate | -0.01 | -0.01 @0 | 'walk' | 'walk<|eot_id|>' |
| substrate_pro | +0.15 | +0.15 @0 | 'drive' | 'drive<|eot_id|>' |
| substrate+library (expect walk) | -5.26 | -5.26 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate_pro+library (expect walk) | -5.32 | -5.32 @0 | 'Walk' | 'Walk.<|eot_id|>' |
