# Llama-3.2-3B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 24 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -0.48 | 0.375 | 0.606 | 'walk<|eot_id|>' |
| substrate | -0.01 | 0.491 | 0.497 | 'walk<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  +0.0 -2.4 -1.7 -0.6 +0.8 -0.1 -0.4 -0.5 +0.1 +1.3 +0.7 -0.5 -1.1 -0.3 -2.7 -0.9 -3.4 -2.6 -2.1 -1.2 -1.9 -10.2 -15.1 -5.1 -4.4 -1.8 -2.2 -0.5 -0.5
substrate: +0.0 -2.1 -1.1 -0.8 +1.0 -0.4 -0.4 -0.6 +0.8 +1.6 +1.1 -0.4 -0.8 -0.6 -3.1 -0.6 -2.7 -1.6 -1.2 -0.3 -1.1 -9.9 -14.4 -3.1 -2.6 -0.1 -0.8 +1.0 -0.0
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -0.4 -0.5 -0.4 -0.3 -0.4 -0.4 -0.5 -0.5 -0.4 -0.4 -0.4 -0.4 -0.3 -0.2 +0.2 +0.2 +0.4 +0.5 +0.3 +0.4 +0.3 +0.1 -0.0 +0.3 +0.1 +0.1 +0.0 -0.0
layers where the patch alone flips baseline to drive: [14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -0.57 (model -0.62), sub -0.16 (model -0.12)
top Δ attention layers: L22 +0.55, L24 +0.43, L21 +0.38, L27 -0.27, L20 -0.21
top Δ MLP layers:       L27 -0.31, L22 -0.24, L24 -0.23, L26 +0.16, L23 +0.13
top Δ heads: L22H11 +0.59, L21H17 +0.26, L24H5 +0.18, L27H16 -0.18, L24H12 +0.14, L20H16 -0.14, L27H1 +0.13, L23H11 -0.11

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.585, max layer L2 (0.871)
- hdr_user: mean 0.002, max layer L5 (0.005)
- line1: mean 0.006, max layer L0 (0.017)
- line2: mean 0.005, max layer L5 (0.014)
- hdr_action: mean 0.003, max layer L4 (0.007)
- line3: mean 0.005, max layer L0 (0.019)
- line4: mean 0.003, max layer L0 (0.016)
- line5: mean 0.004, max layer L0 (0.018)
- line6: mean 0.007, max layer L0 (0.048)
- question: mean 0.081, max layer L12 (0.234)
- answer_instr: mean 0.046, max layer L7 (0.125)
- asst_header: mean 0.137, max layer L27 (0.295)
- last: mean 0.054, max layer L27 (0.227)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L24H12 mass 0.03 Δ+0.14, L12H0 mass 0.13 Δ+0.03, L15H20 mass 0.12 Δ+0.03, L10H9 mass 0.09 Δ+0.03, L12H9 mass 0.13 Δ+0.02, L4H1 mass 0.16 Δ+0.02

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -0.39 |
| loo_line2 | +0.51 |
| loo_line3 | -0.00 |
| loo_line4 | -0.11 |
| loo_line5 | +0.26 |
| loo_line6 | -0.98 |
| only_line1 | -0.06 |
| only_line2 | -0.88 |
| only_line3 | -0.84 |
| only_line4 | -0.49 |
| only_line5 | -0.12 |
| only_line6 | +0.39 |
| headers_only | -0.20 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

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
