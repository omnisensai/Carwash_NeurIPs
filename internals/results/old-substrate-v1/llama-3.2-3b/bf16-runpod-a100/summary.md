# Llama-3.2-3B-Instruct (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 24 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -0.36 | 0.402 | 0.579 | 'walk<|eot_id|>' |
| substrate | -0.14 | 0.460 | 0.528 | 'walk<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  +0.0 -2.4 -1.7 -0.6 +0.8 -0.1 -0.4 -0.4 +0.1 +1.2 +0.6 -0.5 -1.1 -0.3 -2.6 -0.9 -3.4 -2.5 -2.1 -1.2 -1.9 -10.2 -15.1 -4.9 -4.2 -1.7 -2.2 -0.3 -0.4
substrate: +0.0 -2.1 -1.1 -0.8 +1.0 -0.3 -0.4 -0.6 +0.7 +1.7 +1.1 -0.4 -0.8 -0.6 -3.1 -0.6 -2.7 -1.7 -1.2 -0.4 -1.1 -9.8 -14.4 -3.2 -2.7 -0.2 -0.8 +0.8 -0.0
final lens row == model logits: base True, sub False

## patching (substrate residual into baseline at the answer position)
M per layer: -0.4 -0.4 -0.3 -0.3 -0.4 -0.4 -0.4 -0.3 -0.4 -0.3 -0.3 -0.3 -0.4 -0.1 +0.2 +0.2 +0.4 +0.3 +0.3 +0.4 +0.4 +0.1 +0.1 +0.2 +0.1 +0.1 -0.0 -0.1
layers where the patch alone flips baseline to drive: [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -0.49 (model -0.50), sub -0.21 (model -0.25)
top Δ attention layers: L22 +0.43, L24 +0.36, L21 +0.35, L27 -0.30, L20 -0.22
top Δ MLP layers:       L24 -0.24, L27 -0.21, L22 -0.19, L23 +0.15, L26 +0.14
top Δ heads: L22H11 +0.47, L21H17 +0.23, L27H16 -0.19, L20H16 -0.14, L24H5 +0.13, L23H11 -0.12, L24H12 +0.12, L20H15 -0.11

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.585, max layer L2 (0.872)
- hdr_user: mean 0.002, max layer L5 (0.005)
- line1: mean 0.006, max layer L0 (0.017)
- line2: mean 0.005, max layer L5 (0.013)
- hdr_action: mean 0.003, max layer L4 (0.007)
- line3: mean 0.005, max layer L0 (0.019)
- line4: mean 0.003, max layer L0 (0.016)
- line5: mean 0.004, max layer L0 (0.018)
- line6: mean 0.007, max layer L0 (0.048)
- question: mean 0.081, max layer L12 (0.237)
- answer_instr: mean 0.046, max layer L7 (0.125)
- asst_header: mean 0.137, max layer L27 (0.295)
- last: mean 0.055, max layer L27 (0.226)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L12H0 mass 0.13 Δ+0.03, L24H12 mass 0.03 Δ+0.12, L12H9 mass 0.13 Δ+0.02, L4H1 mass 0.16 Δ+0.02, L10H9 mass 0.09 Δ+0.03, L13H5 mass 0.06 Δ+0.05

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -0.37 |
| loo_line2 | +0.39 |
| loo_line3 | -0.00 |
| loo_line4 | -0.11 |
| loo_line5 | +0.28 |
| loo_line6 | -0.88 |
| only_line1 | -0.06 |
| only_line2 | -0.88 |
| only_line3 | -0.82 |
| only_line4 | -0.39 |
| only_line5 | -0.03 |
| only_line6 | +0.25 |
| headers_only | -0.11 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | -0.36 | -0.36 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_CoT | -3.00 | -3.00 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_encourage | -3.25 | -3.25 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_expert | -2.75 | -2.75 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_hallucination | -2.13 | -2.13 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_library | -6.94 | -6.94 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_nomistakes | -2.50 | -2.50 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_threat | -3.13 | -3.13 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_urgency | -2.50 | -2.50 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate | -0.14 | -0.14 @0 | 'walk' | 'walk<|eot_id|>' |
| substrate_pro | +0.15 | +0.15 @0 | 'drive' | 'drive<|eot_id|>' |
| substrate+library (expect walk) | -5.38 | -5.38 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate_pro+library (expect walk) | -5.31 | -5.31 @0 | 'Walk' | 'Walk.<|eot_id|>' |
