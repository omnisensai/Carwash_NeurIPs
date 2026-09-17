# Llama-3.2-3B-Instruct (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 24 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -3.38 | 0.031 | 0.902 | 'Walk.<|eot_id|>' |
| substrate | -1.76 | 0.143 | 0.827 | 'Walk.<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  +0.0 -2.4 -1.5 -0.7 +0.9 +0.4 -0.6 -0.5 +0.5 +1.1 +0.9 +0.7 +0.3 +0.3 -2.0 -1.3 -5.1 -4.1 -4.4 -3.9 -4.3 -16.2 -15.8 -12.5 -10.5 -6.5 -7.1 -5.2 -3.4
substrate: +0.0 -2.1 -1.0 -0.8 +0.9 +0.1 -0.5 -0.7 +1.3 +1.5 +1.4 +0.8 +0.6 -0.1 -2.2 -0.9 -4.8 -3.6 -3.8 -3.7 -3.7 -16.1 -15.9 -11.1 -9.0 -4.4 -4.9 -2.6 -1.8
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -3.5 -3.5 -3.5 -3.4 -3.4 -3.5 -3.4 -3.3 -3.3 -3.4 -3.5 -3.1 -2.3 -1.8 -1.8 -1.5 -1.6 -1.4 -1.4 -1.4 -1.6 -2.0 -2.0 -1.8 -1.8 -1.6 -1.8 -1.8
layers where the patch alone flips baseline to drive: []

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -3.40 (model -3.38), sub -1.80 (model -1.75)
top Δ attention layers: L22 +0.59, L24 +0.47, L20 -0.38, L27 +0.31, L26 -0.17
top Δ MLP layers:       L20 +0.56, L24 -0.34, L26 +0.34, L25 +0.29, L16 +0.17
top Δ heads: L22H11 +0.58, L24H12 +0.42, L20H16 -0.36, L27H2 +0.14, L27H16 +0.11, L19H11 +0.08, L25H7 -0.08, L26H18 -0.07

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.601, max layer L2 (0.869)
- hdr_user: mean 0.002, max layer L5 (0.005)
- line1: mean 0.007, max layer L0 (0.024)
- line2: mean 0.005, max layer L5 (0.015)
- hdr_action: mean 0.003, max layer L4 (0.006)
- line3: mean 0.005, max layer L0 (0.020)
- line4: mean 0.003, max layer L0 (0.017)
- line5: mean 0.004, max layer L0 (0.019)
- line6: mean 0.008, max layer L0 (0.050)
- question: mean 0.139, max layer L12 (0.482)
- answer_instr: mean 0.055, max layer L7 (0.160)
- asst_header: mean 0.119, max layer L27 (0.291)
- last: mean 0.056, max layer L27 (0.210)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L24H12 mass 0.05 Δ+0.42, L27H16 mass 0.06 Δ+0.11, L15H20 mass 0.18 Δ+0.04, L22H11 mass 0.01 Δ+0.58, L18H9 mass 0.20 Δ+0.02, L13H18 mass 0.09 Δ+0.04

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -2.63 |
| loo_line2 | -1.63 |
| loo_line3 | -2.13 |
| loo_line4 | -2.13 |
| loo_line5 | -1.63 |
| loo_line6 | -3.38 |
| only_line1 | -3.38 |
| only_line2 | -3.88 |
| only_line3 | -4.13 |
| only_line4 | -3.00 |
| only_line5 | -3.50 |
| only_line6 | -2.76 |
| headers_only | -3.13 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | -3.38 | -3.38 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_CoT | -3.00 | -3.00 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_encourage | -3.25 | -3.25 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_expert | -2.75 | -2.75 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_hallucination | -2.13 | -2.13 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_library | -6.94 | -6.94 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_nomistakes | -2.50 | -2.50 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_threat | -3.13 | -3.13 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_urgency | -2.50 | -2.50 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate | -1.76 | -1.76 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate_pro | -1.27 | -1.27 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate+library (expect walk) | -5.38 | -5.38 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate_pro+library (expect walk) | -5.31 | -5.31 @0 | 'Walk' | 'Walk.<|eot_id|>' |
