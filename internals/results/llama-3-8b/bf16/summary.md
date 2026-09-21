# llama-3-8b-Instruct (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token 'drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -9.64 | 0.000 | 1.000 | 'Walk<|eot_id|>' |
| substrate | +0.75 | 0.677 | 0.320 | 'drive<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -0.3 +0.9 +1.9 +1.3 +0.2 -3.1 -2.9 -2.9 -2.3 -2.2 -0.5 +1.1 +2.1 +1.4 +3.0 -1.6 -1.5 +0.2 -3.8 -4.8 -5.1 -4.4 -5.5 -9.6 -15.2 -13.0 -16.3 -14.2 -12.4 -18.6 -9.3 -7.8 -9.8
substrate: -0.3 +0.2 +1.7 +1.4 +0.7 -2.8 -2.9 -2.9 -2.4 -2.1 -0.2 +1.1 +2.4 +1.5 +2.3 -1.0 -0.3 +1.2 -3.1 -3.8 -3.6 -2.1 -2.6 -4.2 -10.1 -3.1 -2.8 -2.4 -1.9 -4.7 +0.9 +2.3 +0.8
final lens row == model logits: base False, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -9.8 -9.6 -9.6 -9.6 -9.9 -10.0 -9.7 -10.0 -10.1 -10.1 -9.5 -9.6 -9.0 -7.7 -3.0 -0.1 +0.0 +0.2 +0.1 +0.1 +0.2 +0.4 +0.5 +0.6 +0.2 +0.3 +0.3 +0.5 +0.5 +0.5 +0.7 +0.8
layers where the patch alone flips baseline to drive: [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -10.52 (model -10.50), sub +0.74 (model +0.75)
top Δ attention layers: L25 +3.36, L31 +1.70, L24 +1.14, L28 +0.75, L29 +0.40
top Δ MLP layers:       L31 +3.53, L29 -2.66, L28 +2.43, L25 -1.17, L23 +0.71
top Δ heads: L25H15 +2.38, L24H17 +1.29, L25H5 +1.07, L31H3 +0.80, L31H1 +0.59, L27H5 +0.50, L28H20 +0.38, L30H25 -0.30

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.581, max layer L2 (0.858)
- hdr_user: mean 0.003, max layer L2 (0.014)
- line1: mean 0.003, max layer L0 (0.015)
- line2: mean 0.004, max layer L0 (0.020)
- line3: mean 0.004, max layer L0 (0.028)
- line4: mean 0.002, max layer L0 (0.020)
- line5: mean 0.003, max layer L0 (0.029)
- line6: mean 0.002, max layer L0 (0.015)
- question: mean 0.079, max layer L14 (0.189)
- answer_instr: mean 0.045, max layer L9 (0.165)
- asst_header: mean 0.136, max layer L31 (0.277)
- last: mean 0.053, max layer L31 (0.204)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L25H5 mass 0.03 Δ+1.07, L24H17 mass 0.01 Δ+1.29, L28H20 mass 0.04 Δ+0.38, L29H8 mass 0.06 Δ+0.21, L28H0 mass 0.07 Δ+0.17, L27H16 mass 0.09 Δ+0.14

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +1.48 |
| loo_line2 | +0.73 |
| loo_line3 | +0.48 |
| loo_line4 | +1.41 |
| loo_line5 | +0.07 |
| loo_line6 | +1.50 |
| loo_line7 | +1.97 |
| loo_line8 | +0.89 |
| loo_line9 | -0.47 |
| only_line1 | -6.18 |
| only_line2 | -5.82 |
| only_line3 | -3.45 |
| only_line4 | -4.76 |
| only_line5 | -1.21 |
| only_line6 | -2.98 |
| only_line7 | +1.27 |
| only_line8 | +4.59 |
| only_line9 | -3.06 |
| headers_only | -5.64 |

line1: - Perform an activity on an object at a service location.
line2: - No other objectives or goals are relevant for the user.
line3: - The object is initially with the user at the same location.
line4: - The activity is performed at the service location.
line5: - The object must be at the service location for the activity performance.
line6: - Vehicles are not portable.
line7: - Walking leaves a vehicle behind.
line8: - Walking does not transport a vehicle.
line9: - To transport a vehicle from one location to another, the user must operate it.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | -9.64 | -9.64 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_CoT | -8.99 | -8.99 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_encourage | -12.34 | -12.34 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_expert | -7.86 | -7.86 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_goaloriented | -5.50 | -5.50 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_hallucination | -11.30 | -11.30 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_nomistakes | -9.23 | -9.23 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_threat | -10.26 | – | 'W' | 'WALK<|eot_id|>' |
| benchmark_urgency | -4.28 | -4.28 @0 | 'Walk' | 'Walk<|eot_id|>' |
| substrate | +0.75 | +0.75 @0 | 'drive' | 'drive<|eot_id|>' |
