# Llama-3.1-8B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -3.69 | 0.024 | 0.975 | 'walk<|eot_id|>' |
| substrate | +1.01 | 0.728 | 0.266 | 'drive<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -0.3 +0.3 +2.0 +2.0 +0.0 -2.1 -1.2 -0.5 -1.4 -0.5 +0.4 +0.4 +1.5 +0.9 +2.0 -2.5 -2.8 -1.2 -3.6 -4.3 -4.1 -3.8 -3.9 -8.3 -14.0 -10.3 -10.3 -9.3 -7.3 -11.7 -3.9 -2.6 -3.7
substrate: -0.3 +0.2 +1.9 +1.5 -0.6 -1.9 -0.9 -0.6 -1.0 -0.3 +0.6 +1.1 +1.0 -0.4 +1.0 -1.7 -1.5 -0.0 -2.2 -3.6 -3.0 -2.0 -0.9 -2.2 -8.9 -2.7 -2.0 -2.0 -1.1 -2.6 +1.0 +2.4 +1.0
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -3.6 -3.7 -3.6 -3.6 -3.6 -3.7 -3.6 -3.6 -3.7 -3.6 -3.6 -3.5 -3.4 -3.1 -1.7 -0.1 +0.1 +0.4 +0.6 +0.6 +0.6 +0.8 +0.9 +0.9 +0.8 +0.9 +0.9 +0.9 +1.0 +0.9 +1.0 +1.0
layers where the patch alone flips baseline to drive: [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -3.70 (model -3.75), sub +1.01 (model +1.00)
top Δ attention layers: L25 +1.17, L31 +0.75, L24 +0.46, L27 +0.37, L21 +0.28
top Δ MLP layers:       L29 -2.40, L28 +1.76, L31 +0.82, L22 +0.80, L27 -0.49
top Δ heads: L25H15 +0.62, L25H5 +0.55, L24H17 +0.43, L31H1 +0.41, L27H7 +0.27, L31H21 +0.20, L27H16 +0.19, L30H27 -0.19

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.549, max layer L2 (0.792)
- hdr_user: mean 0.003, max layer L2 (0.009)
- line1: mean 0.008, max layer L0 (0.036)
- line2: mean 0.008, max layer L0 (0.030)
- hdr_action: mean 0.003, max layer L8 (0.011)
- line3: mean 0.006, max layer L0 (0.040)
- line4: mean 0.005, max layer L0 (0.034)
- line5: mean 0.006, max layer L0 (0.035)
- line6: mean 0.011, max layer L0 (0.083)
- question: mean 0.086, max layer L13 (0.188)
- answer_instr: mean 0.044, max layer L9 (0.143)
- asst_header: mean 0.147, max layer L31 (0.283)
- last: mean 0.058, max layer L31 (0.224)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L27H16 mass 0.11 Δ+0.19, L21H14 mass 0.09 Δ+0.17, L22H8 mass 0.12 Δ+0.11, L30H26 mass 0.09 Δ+0.12, L30H12 mass 0.12 Δ+0.09, L28H0 mass 0.10 Δ+0.11

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +0.53 |
| loo_line2 | +1.02 |
| loo_line3 | +1.13 |
| loo_line4 | +0.64 |
| loo_line5 | +0.39 |
| loo_line6 | -0.60 |
| only_line1 | -2.56 |
| only_line2 | -5.81 |
| only_line3 | -3.94 |
| only_line4 | -4.94 |
| only_line5 | -3.94 |
| only_line6 | -1.83 |
| headers_only | -5.52 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

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
