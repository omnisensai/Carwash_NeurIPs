# Llama-3.1-8B-Instruct (bf16, CPU)

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -4.00 | 0.018 | 0.967 | 'Walk.<|eot_id|>' |
| substrate | +1.50 | 0.808 | 0.181 | 'Drive.<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -0.3 +0.4 +2.0 +2.1 -0.1 -2.1 -0.5 +0.0 -0.7 +1.8 +2.0 +2.4 +3.3 +2.5 +3.0 -1.5 -1.6 -0.9 -3.6 -5.1 -4.1 -3.4 -2.4 -8.9 -15.7 -12.5 -12.3 -11.6 -8.1 -14.3 -4.4 -3.2 -4.0
substrate: -0.3 +0.3 +1.9 +1.6 -0.6 -1.5 -0.2 -0.1 +0.1 +2.1 +2.4 +3.8 +3.9 +1.9 +2.5 -0.9 -0.2 -0.2 -1.7 -3.3 -2.4 -2.3 -0.0 -2.9 -8.9 -2.3 -3.1 -3.4 -0.8 -4.5 +0.8 +2.5 +1.5
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -3.9 -4.0 -3.7 -3.9 -3.9 -3.7 -3.7 -3.6 -3.7 -3.9 -4.1 -3.9 -3.5 -3.2 -1.5 -0.9 -0.9 +0.5 +0.5 +0.7 +0.7 +1.1 +1.2 +1.1 +1.0 +1.0 +1.1 +1.1 +1.2 +1.2 +1.4 +1.5
layers where the patch alone flips baseline to drive: [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -3.99 (model -4.00), sub +1.52 (model +1.50)
top Δ attention layers: L31 +1.20, L25 +0.94, L28 +0.52, L23 -0.41, L24 +0.37
top Δ MLP layers:       L29 -2.94, L28 +1.89, L23 +1.21, L25 -0.97, L22 +0.97
top Δ heads: L25H15 +1.00, L31H3 +0.93, L24H17 +0.47, L30H25 -0.36, L28H0 +0.31, L30H27 +0.31, L28H20 +0.29, L27H16 +0.29

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.548, max layer L2 (0.800)
- hdr_user: mean 0.003, max layer L2 (0.009)
- line1: mean 0.010, max layer L0 (0.045)
- line2: mean 0.009, max layer L0 (0.031)
- hdr_action: mean 0.003, max layer L11 (0.010)
- line3: mean 0.007, max layer L0 (0.041)
- line4: mean 0.005, max layer L0 (0.035)
- line5: mean 0.008, max layer L0 (0.035)
- line6: mean 0.016, max layer L0 (0.085)
- question: mean 0.143, max layer L13 (0.383)
- answer_instr: mean 0.055, max layer L9 (0.177)
- asst_header: mean 0.130, max layer L31 (0.267)
- last: mean 0.060, max layer L31 (0.212)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L28H20 mass 0.19 Δ+0.29, L28H0 mass 0.15 Δ+0.31, L27H16 mass 0.13 Δ+0.29, L30H26 mass 0.13 Δ+0.27, L24H17 mass 0.06 Δ+0.47, L25H15 mass 0.02 Δ+1.00

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +1.62 |
| loo_line2 | +1.87 |
| loo_line3 | +2.24 |
| loo_line4 | +1.37 |
| loo_line5 | +0.50 |
| loo_line6 | -0.75 |
| only_line1 | -1.37 |
| only_line2 | -6.00 |
| only_line3 | -3.75 |
| only_line4 | -4.75 |
| only_line5 | -2.75 |
| only_line6 | -0.75 |
| headers_only | -7.12 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | -4.00 | – | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_CoT | -1.75 | – | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_encourage | -5.87 | – | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_expert | -1.25 | – | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_hallucination | -3.62 | – | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_library | -12.67 | – | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_nomistakes | -4.74 | – | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_threat | -5.74 | – | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_urgency | -1.00 | – | 'Walk' | 'Walk.<|eot_id|>' |
| substrate | +1.50 | – | 'Drive' | 'Drive.<|eot_id|>' |
