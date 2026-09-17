# Llama-3.2-3B-Instruct (bf16), substrate_pro

substrate file: substrate_pro.txt

quant: bf16 · layers 28 · heads 24 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -3.50 | 0.027 | 0.909 | 'Walk.<|eot_id|>' |
| substrate | -1.28 | 0.210 | 0.754 | 'Walk.<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  +0.0 -2.4 -1.5 -0.6 +1.0 +0.4 -0.6 -0.5 +0.5 +1.1 +0.9 +0.6 +0.3 +0.3 -2.0 -1.3 -5.1 -4.2 -4.4 -4.0 -4.3 -16.2 -15.9 -12.4 -10.6 -6.5 -7.0 -5.2 -3.5
substrate: +0.0 -2.1 -1.0 -0.8 +1.0 +0.5 -0.1 -0.5 +1.4 +1.5 +1.1 +0.7 +0.8 -0.2 -1.9 -0.9 -4.4 -2.6 -3.1 -2.7 -3.1 -13.4 -14.7 -8.7 -6.5 -3.6 -3.6 -1.5 -1.3
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -3.4 -3.5 -3.4 -3.4 -3.4 -3.4 -3.4 -3.3 -3.4 -3.4 -3.3 -3.1 -2.4 -1.8 -1.8 -1.3 -1.3 -1.1 -1.1 -0.9 -1.0 -1.5 -1.4 -1.3 -1.2 -1.2 -1.3 -1.3
layers where the patch alone flips baseline to drive: []

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -3.41 (model -3.50), sub -1.27 (model -1.25)
top Δ attention layers: L22 +1.31, L20 -0.50, L27 +0.47, L24 +0.33, L26 -0.22
top Δ MLP layers:       L20 +1.45, L24 -0.82, L25 +0.43, L22 -0.42, L26 +0.41
top Δ heads: L22H11 +1.29, L20H16 -0.36, L27H2 +0.32, L24H12 +0.28, L26H18 -0.19, L20H15 -0.14, L19H11 +0.14, L27H1 +0.11

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.595, max layer L2 (0.867)
- hdr_user: mean 0.001, max layer L8 (0.003)
- line1: mean 0.003, max layer L0 (0.006)
- line2: mean 0.003, max layer L0 (0.008)
- hdr_action: mean 0.002, max layer L4 (0.005)
- line3: mean 0.003, max layer L0 (0.010)
- line4: mean 0.003, max layer L0 (0.009)
- line5: mean 0.003, max layer L0 (0.023)
- line6: mean 0.007, max layer L0 (0.022)
- question: mean 0.129, max layer L12 (0.463)
- answer_instr: mean 0.052, max layer L7 (0.154)
- asst_header: mean 0.119, max layer L27 (0.285)
- last: mean 0.055, max layer L27 (0.205)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L15H20 mass 0.29 Δ+0.08, L16H16 mass 0.21 Δ+0.10, L24H12 mass 0.07 Δ+0.28, L22H11 mass 0.02 Δ+1.29, L19H11 mass 0.06 Δ+0.14, L26H2 mass 0.14 Δ+0.06

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -1.02 |
| loo_line2 | -1.65 |
| loo_line3 | -1.27 |
| loo_line4 | -1.78 |
| loo_line5 | -1.66 |
| loo_line6 | -1.28 |
| loo_line7 | -0.77 |
| loo_line8 | -1.40 |
| loo_line9 | -2.41 |
| only_line1 | -3.29 |
| only_line2 | -3.29 |
| only_line3 | -3.42 |
| only_line4 | -2.67 |
| only_line5 | -3.66 |
| only_line6 | -2.27 |
| only_line7 | -3.78 |
| only_line8 | -2.66 |
| only_line9 | -2.28 |
| headers_only | -3.67 |

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
| baseline | -3.50 | -3.50 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_CoT | -3.13 | -3.13 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_encourage | -3.25 | -3.25 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_expert | -2.63 | -2.63 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_hallucination | -2.13 | -2.13 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_library | -7.06 | -7.06 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_nomistakes | -2.50 | -2.50 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_threat | -3.13 | -3.13 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_urgency | -2.63 | -2.63 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate | -1.76 | -1.76 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate_pro | -1.28 | -1.28 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate+library (expect walk) | -5.26 | -5.26 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate_pro+library (expect walk) | -5.32 | -5.32 @0 | 'Walk' | 'Walk.<|eot_id|>' |
