# Llama-3.2-3B-Instruct (bf16)

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 24 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -3.50 | 0.027 | 0.909 | 'Walk.<|eot_id|>' |
| substrate | -1.76 | 0.143 | 0.828 | 'Walk.<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  +0.0 -2.4 -1.5 -0.6 +1.0 +0.4 -0.6 -0.5 +0.5 +1.1 +0.9 +0.6 +0.3 +0.3 -2.0 -1.3 -5.1 -4.2 -4.4 -4.0 -4.3 -16.2 -15.9 -12.4 -10.6 -6.5 -7.0 -5.2 -3.5
substrate: +0.0 -2.1 -1.0 -0.8 +0.9 +0.2 -0.5 -0.7 +1.3 +1.5 +1.3 +0.7 +0.6 -0.1 -2.2 -1.0 -4.8 -3.5 -3.8 -3.6 -3.5 -16.0 -15.9 -11.0 -8.9 -4.5 -4.8 -2.7 -1.8
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -3.4 -3.5 -3.4 -3.4 -3.4 -3.4 -3.5 -3.4 -3.3 -3.4 -3.4 -3.1 -2.4 -1.9 -1.8 -1.5 -1.5 -1.4 -1.4 -1.4 -1.5 -1.9 -1.9 -1.8 -1.6 -1.6 -1.6 -1.8
layers where the patch alone flips baseline to drive: []

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -3.41 (model -3.50), sub -1.75 (model -1.75)
top Δ attention layers: L22 +0.61, L24 +0.46, L20 -0.39, L27 +0.34, L26 -0.16
top Δ MLP layers:       L20 +0.57, L24 -0.37, L26 +0.35, L25 +0.28, L16 +0.18
top Δ heads: L22H11 +0.60, L24H12 +0.41, L20H16 -0.35, L27H2 +0.15, L27H16 +0.12, L19H11 +0.09, L25H7 -0.08, L26H18 -0.08

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.601, max layer L2 (0.870)
- hdr_user: mean 0.002, max layer L5 (0.005)
- line1: mean 0.007, max layer L0 (0.024)
- line2: mean 0.005, max layer L5 (0.015)
- hdr_action: mean 0.003, max layer L4 (0.006)
- line3: mean 0.005, max layer L0 (0.020)
- line4: mean 0.003, max layer L0 (0.017)
- line5: mean 0.004, max layer L0 (0.019)
- line6: mean 0.008, max layer L0 (0.050)
- question: mean 0.139, max layer L12 (0.483)
- answer_instr: mean 0.055, max layer L7 (0.161)
- asst_header: mean 0.119, max layer L27 (0.292)
- last: mean 0.056, max layer L27 (0.211)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L24H12 mass 0.05 Δ+0.41, L27H16 mass 0.06 Δ+0.12, L15H20 mass 0.18 Δ+0.04, L22H11 mass 0.01 Δ+0.60, L18H9 mass 0.21 Δ+0.02, L13H18 mass 0.09 Δ+0.04

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -2.63 |
| loo_line2 | -1.63 |
| loo_line3 | -2.01 |
| loo_line4 | -2.13 |
| loo_line5 | -1.50 |
| loo_line6 | -3.51 |
| only_line1 | -3.38 |
| only_line2 | -3.76 |
| only_line3 | -4.13 |
| only_line4 | -3.13 |
| only_line5 | -3.38 |
| only_line6 | -2.63 |
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
