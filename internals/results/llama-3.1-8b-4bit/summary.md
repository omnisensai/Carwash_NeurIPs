# Llama-3.1-8B-Instruct (nf4)

quant: 4bit · layers 32 · heads 32 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -6.97 | 0.001 | 0.991 | 'Walk.<|eot_id|>' |
| substrate | +0.87 | 0.693 | 0.291 | 'Drive.<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -0.3 +0.2 +2.1 +1.7 +0.5 -1.9 -0.3 +0.6 -1.3 +1.1 +1.1 +2.5 +3.1 +1.2 +2.7 -1.9 -1.9 -0.6 -4.7 -6.6 -6.0 -5.5 -5.0 -12.1 -17.7 -15.4 -14.6 -13.8 -10.1 -17.4 -6.1 -5.1 -7.0
substrate: -0.3 -0.0 +1.9 +1.2 +0.5 -1.2 -0.0 +0.7 -0.2 +1.8 +1.9 +3.7 +3.8 +1.1 +2.2 -1.1 -0.5 -0.3 -2.5 -4.3 -3.2 -2.8 -2.6 -6.7 -12.1 -6.6 -5.5 -5.6 -2.7 -5.5 +0.8 +2.5 +0.9
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -6.8 -6.7 -6.7 -6.7 -6.6 -6.5 -6.5 -6.5 -6.6 -6.8 -6.7 -6.3 -5.5 -4.5 -2.6 -1.6 -1.7 +0.3 +0.3 +0.3 +0.4 +0.7 +0.8 +0.6 +0.5 +0.5 +0.6 +0.8 +0.9 +0.7 +0.9 +0.9
layers where the patch alone flips baseline to drive: [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -6.97 (model -7.00), sub +0.91 (model +0.88)
top Δ attention layers: L31 +1.42, L25 +1.17, L28 +0.61, L23 -0.34, L24 +0.32
top Δ MLP layers:       L29 -3.00, L28 +2.88, L31 +1.83, L22 +1.02, L23 +0.93
top Δ heads: L25H15 +1.28, L31H3 +1.16, L24H17 +0.58, L30H25 -0.40, L27H16 +0.36, L28H13 +0.34, L30H27 +0.33, L28H20 +0.27

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.548, max layer L2 (0.789)
- hdr_user: mean 0.003, max layer L2 (0.008)
- line1: mean 0.010, max layer L0 (0.046)
- line2: mean 0.008, max layer L0 (0.031)
- hdr_action: mean 0.003, max layer L8 (0.009)
- line3: mean 0.008, max layer L0 (0.041)
- line4: mean 0.005, max layer L0 (0.036)
- line5: mean 0.008, max layer L0 (0.036)
- line6: mean 0.015, max layer L0 (0.085)
- question: mean 0.144, max layer L13 (0.362)
- answer_instr: mean 0.053, max layer L9 (0.183)
- asst_header: mean 0.135, max layer L31 (0.276)
- last: mean 0.060, max layer L31 (0.210)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L28H20 mass 0.17 Δ+0.27, L27H16 mass 0.12 Δ+0.36, L24H17 mass 0.07 Δ+0.58, L25H15 mass 0.03 Δ+1.28, L28H0 mass 0.13 Δ+0.24, L13H21 mass 0.44 Δ+0.07

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +1.12 |
| loo_line2 | +1.25 |
| loo_line3 | +1.36 |
| loo_line4 | +0.62 |
| loo_line5 | +0.24 |
| loo_line6 | -1.99 |
| only_line1 | -2.98 |
| only_line2 | -7.32 |
| only_line3 | -4.98 |
| only_line4 | -6.09 |
| only_line5 | -3.97 |
| only_line6 | -0.77 |
| headers_only | -8.68 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

## all prompts
| prompt | M | argmax | greedy |
|---|---|---|---|
| baseline | -6.97 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_CoT | -4.61 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_encourage | -7.61 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_expert | -4.25 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_hallucination | -6.11 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_library | -13.13 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_nomistakes | -7.93 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_threat | -8.22 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_urgency | -0.75 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate | +0.87 | 'Drive' | 'Drive.<|eot_id|>' |
