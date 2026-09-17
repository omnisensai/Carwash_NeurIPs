# Llama-3.1-8B-Instruct (bf16, CPU), substrate_pro

substrate file: substrate_pro.txt

quant: bf16 · layers 32 · heads 32 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -4.00 | 0.018 | 0.967 | 'Walk.<|eot_id|>' |
| substrate | +2.98 | 0.947 | 0.048 | 'Drive.<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -0.3 +0.4 +2.0 +2.1 -0.1 -2.1 -0.5 +0.0 -0.7 +1.8 +2.0 +2.4 +3.3 +2.5 +3.0 -1.5 -1.6 -0.9 -3.6 -5.1 -4.1 -3.4 -2.4 -8.9 -15.7 -12.5 -12.3 -11.6 -8.1 -14.3 -4.4 -3.2 -4.0
substrate: -0.3 -0.1 +1.5 +1.3 -0.7 -1.4 -0.0 +0.2 +0.2 +2.3 +2.9 +3.2 +3.4 +2.1 +2.1 -1.5 -1.3 -0.5 -0.2 -1.0 -1.1 -0.7 +1.9 +0.2 -3.8 +1.6 +2.5 +1.6 +2.5 -0.6 +2.0 +3.5 +3.0
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -4.0 -3.9 -3.7 -3.9 -3.9 -3.6 -3.7 -3.5 -3.7 -4.0 -4.1 -4.0 -4.0 -3.6 -0.1 +0.5 +0.4 +2.1 +2.2 +2.4 +2.5 +3.0 +3.1 +2.9 +2.9 +3.0 +2.9 +2.7 +3.1 +3.1 +2.9 +3.0
layers where the patch alone flips baseline to drive: [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -3.99 (model -4.00), sub +3.07 (model +3.00)
top Δ attention layers: L25 +1.64, L31 +1.50, L28 +0.55, L24 +0.54, L21 +0.46
top Δ MLP layers:       L29 -3.96, L28 +2.28, L23 +1.58, L31 +1.44, L22 +1.24
top Δ heads: L31H3 +1.29, L25H15 +1.24, L24H17 +0.53, L30H25 -0.47, L30H27 +0.44, L25H5 +0.44, L21H14 +0.37, L28H20 +0.34

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.547, max layer L2 (0.792)
- hdr_user: mean 0.001, max layer L0 (0.005)
- line1: mean 0.003, max layer L0 (0.013)
- line2: mean 0.004, max layer L0 (0.019)
- hdr_action: mean 0.002, max layer L8 (0.006)
- line3: mean 0.004, max layer L0 (0.021)
- line4: mean 0.004, max layer L0 (0.022)
- line5: mean 0.004, max layer L0 (0.041)
- line6: mean 0.014, max layer L0 (0.038)
- question: mean 0.128, max layer L13 (0.370)
- answer_instr: mean 0.052, max layer L9 (0.164)
- asst_header: mean 0.132, max layer L31 (0.264)
- last: mean 0.060, max layer L31 (0.215)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L25H5 mass 0.18 Δ+0.44, L21H14 mass 0.21 Δ+0.37, L28H20 mass 0.21 Δ+0.34, L22H8 mass 0.39 Δ+0.16, L25H15 mass 0.04 Δ+1.24, L30H26 mass 0.22 Δ+0.24

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +3.59 |
| loo_line2 | +3.10 |
| loo_line3 | +3.47 |
| loo_line4 | +2.73 |
| loo_line5 | +2.11 |
| loo_line6 | +2.60 |
| loo_line7 | +3.97 |
| loo_line8 | +2.73 |
| loo_line9 | +1.00 |
| only_line1 | -0.01 |
| only_line2 | +1.48 |
| only_line3 | +0.24 |
| only_line4 | +1.10 |
| only_line5 | +0.36 |
| only_line6 | +0.61 |
| only_line7 | -0.64 |
| only_line8 | +0.24 |
| only_line9 | +1.09 |
| headers_only | +0.48 |

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
| substrate_pro | +2.98 | – | 'Drive' | 'Drive.<|eot_id|>' |
| substrate+library (expect walk) | -5.36 | – | 'Walk' | 'Walk.<|eot_id|>' |
| substrate_pro+library (expect walk) | -4.58 | – | 'Walk' | 'Walk.<|eot_id|>' |
