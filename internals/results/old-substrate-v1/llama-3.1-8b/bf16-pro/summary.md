# Llama-3.1-8B-Instruct

substrate file: substrate_pro.txt

quant: bf16 · layers 32 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -3.69 | 0.024 | 0.975 | 'walk<|eot_id|>' |
| substrate | -0.36 | 0.410 | 0.584 | 'walk<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -0.3 +0.3 +2.0 +2.0 +0.0 -2.1 -1.2 -0.5 -1.4 -0.5 +0.4 +0.4 +1.5 +0.9 +2.0 -2.5 -2.8 -1.2 -3.6 -4.3 -4.1 -3.8 -3.9 -8.3 -14.0 -10.3 -10.3 -9.3 -7.3 -11.7 -3.9 -2.6 -3.7
substrate: -0.3 -0.3 +1.6 +1.2 -0.7 -1.8 -0.7 -0.3 -0.7 -0.1 +0.9 +0.4 +0.4 -0.1 +0.5 -2.2 -2.8 -0.6 -3.1 -3.9 -4.0 -3.4 -3.8 -6.1 -11.4 -6.2 -5.8 -5.5 -4.5 -5.6 -0.4 +1.1 -0.4
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -3.7 -3.7 -3.6 -3.6 -3.6 -3.5 -3.6 -3.6 -3.6 -3.4 -3.3 -3.4 -3.2 -3.0 -1.2 -1.2 -1.1 -0.5 -0.6 -0.6 -0.6 -0.6 -0.5 -0.6 -0.7 -0.6 -0.6 -0.6 -0.5 -0.5 -0.4 -0.4
layers where the patch alone flips baseline to drive: []

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -3.70 (model -3.75), sub -0.39 (model -0.38)
top Δ attention layers: L25 +0.89, L31 +0.49, L24 +0.31, L23 -0.24, L14 +0.16
top Δ MLP layers:       L28 +2.03, L29 -1.48, L23 +0.66, L22 +0.55, L31 +0.47
top Δ heads: L25H15 +0.65, L24H17 +0.35, L23H22 -0.26, L25H5 +0.24, L31H21 +0.22, L31H1 +0.21, L27H7 +0.17, L15H11 +0.11

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.547, max layer L2 (0.783)
- hdr_user: mean 0.001, max layer L8 (0.005)
- line1: mean 0.003, max layer L0 (0.013)
- line2: mean 0.003, max layer L0 (0.019)
- hdr_action: mean 0.002, max layer L8 (0.007)
- line3: mean 0.004, max layer L0 (0.021)
- line4: mean 0.003, max layer L0 (0.022)
- line5: mean 0.003, max layer L0 (0.040)
- line6: mean 0.010, max layer L0 (0.038)
- question: mean 0.079, max layer L13 (0.202)
- answer_instr: mean 0.041, max layer L11 (0.138)
- asst_header: mean 0.144, max layer L31 (0.279)
- last: mean 0.060, max layer L31 (0.226)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L24H17 mass 0.06 Δ+0.35, L25H5 mass 0.08 Δ+0.24, L31H21 mass 0.08 Δ+0.22, L14H4 mass 0.21 Δ+0.07, L13H15 mass 0.31 Δ+0.05, L15H11 mass 0.10 Δ+0.11

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +0.26 |
| loo_line2 | -0.48 |
| loo_line3 | -0.48 |
| loo_line4 | -0.36 |
| loo_line5 | -0.24 |
| loo_line6 | +0.02 |
| loo_line7 | +1.51 |
| loo_line8 | -0.36 |
| loo_line9 | -0.36 |
| only_line1 | -2.59 |
| only_line2 | -0.97 |
| only_line3 | -2.71 |
| only_line4 | -1.97 |
| only_line5 | -1.47 |
| only_line6 | +1.01 |
| only_line7 | -1.36 |
| only_line8 | -0.98 |
| only_line9 | -0.85 |
| headers_only | -3.33 |

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
| baseline | -3.69 | -3.69 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_CoT | -1.75 | -1.75 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_encourage | -5.87 | -5.87 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_expert | -1.25 | -1.25 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_hallucination | -3.62 | -3.62 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_library | -12.67 | -12.67 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_nomistakes | -4.74 | -4.74 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_threat | -5.74 | -5.74 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_urgency | -1.00 | -1.00 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate | +1.01 | +1.01 @0 | 'drive' | 'drive<|eot_id|>' |
| substrate_pro | -0.36 | -0.36 @0 | 'walk' | 'walk<|eot_id|>' |
| substrate+library (expect walk) | -5.36 | -5.36 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate_pro+library (expect walk) | -4.58 | -4.58 @0 | 'Walk' | 'Walk.<|eot_id|>' |
