# Meta-Llama-3.1-8B-Instruct-abliterated (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -7.48 | 0.001 | 0.999 | 'walk<|eot_id|>' |
| substrate | +2.05 | 0.882 | 0.113 | 'drive<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -0.4 +0.6 +1.7 +1.1 -0.4 -3.5 -3.2 -3.4 -1.9 -2.0 -0.4 +0.7 +1.8 +0.9 +2.0 -2.3 -1.8 +0.4 -3.7 -4.9 -5.2 -3.9 -4.9 -8.2 -13.8 -11.1 -14.7 -13.0 -11.9 -18.1 -8.1 -6.7 -7.5
substrate: -0.4 -0.1 +1.6 +1.2 +0.2 -3.4 -3.0 -3.2 -2.0 -2.1 +0.1 +0.8 +2.3 +1.1 +1.9 -1.3 -0.0 +1.6 -1.9 -2.8 -2.6 -1.1 -1.0 -1.8 -7.8 -0.1 +0.3 +0.2 +0.6 -1.8 +2.4 +3.6 +2.1
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -7.6 -7.4 -7.6 -7.7 -7.7 -7.8 -7.8 -8.0 -8.0 -8.1 -7.7 -7.6 -7.2 -5.6 -0.5 +1.1 +1.1 +1.4 +1.4 +1.3 +1.4 +1.5 +1.8 +1.9 +1.6 +1.7 +1.7 +1.7 +1.9 +1.9 +1.9 +2.1
layers where the patch alone flips baseline to drive: [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -7.25 (model -7.25), sub +2.07 (model +2.12)
top Δ attention layers: L25 +3.30, L24 +1.33, L28 +0.92, L31 +0.71, L29 +0.61
top Δ MLP layers:       L29 -3.67, L31 +2.53, L28 +2.28, L25 -1.12, L22 +0.57
top Δ heads: L25H15 +2.25, L24H17 +1.34, L25H5 +1.12, L31H1 +0.84, L28H20 +0.52, L27H7 +0.49, L30H27 -0.44, L30H24 +0.36

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.576, max layer L2 (0.854)
- hdr_user: mean 0.003, max layer L2 (0.015)
- line1: mean 0.004, max layer L0 (0.019)
- line2: mean 0.005, max layer L0 (0.024)
- line3: mean 0.004, max layer L0 (0.032)
- line4: mean 0.002, max layer L0 (0.022)
- line5: mean 0.004, max layer L0 (0.033)
- line6: mean 0.003, max layer L0 (0.016)
- question: mean 0.074, max layer L13 (0.172)
- answer_instr: mean 0.044, max layer L9 (0.163)
- asst_header: mean 0.140, max layer L31 (0.285)
- last: mean 0.055, max layer L31 (0.209)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L25H5 mass 0.03 Δ+1.12, L14H5 mass 0.41 Δ+0.06, L15H11 mass 0.18 Δ+0.11, L28H20 mass 0.04 Δ+0.52, L27H16 mass 0.07 Δ+0.26, L24H17 mass 0.01 Δ+1.34

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +2.96 |
| loo_line2 | +2.14 |
| loo_line3 | +1.41 |
| loo_line4 | +2.41 |
| loo_line5 | +1.17 |
| loo_line6 | +2.50 |
| loo_line7 | +3.21 |
| loo_line8 | +1.74 |
| loo_line9 | +0.46 |
| only_line1 | -4.67 |
| only_line2 | -4.08 |
| only_line3 | -2.11 |
| only_line4 | -3.20 |
| only_line5 | -0.25 |
| only_line6 | -1.52 |
| only_line7 | +1.67 |
| only_line8 | +5.13 |
| only_line9 | -2.03 |
| headers_only | -4.31 |

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
| baseline | -7.48 | -7.48 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_CoT | -6.41 | -6.41 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_encourage | -9.78 | – | 'W' | 'WALK<|eot_id|>' |
| benchmark_expert | -6.20 | -6.20 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_goaloriented | -3.98 | -3.98 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_hallucination | -10.92 | -10.92 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_nomistakes | -7.44 | -7.44 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_threat | -8.77 | – | 'W' | 'WALK<|eot_id|>' |
| benchmark_urgency | -3.34 | -3.34 @0 | 'walk' | 'walk<|eot_id|>' |
| substrate | +2.05 | +2.05 @0 | 'drive' | 'drive<|eot_id|>' |
