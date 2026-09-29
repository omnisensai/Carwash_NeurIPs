# unsloth/Llama-3.1-8B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -3.69 | 0.024 | 0.975 | 'walk<|eot_id|>' |
| substrate | +1.39 | 0.796 | 0.199 | 'drive<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -0.3 +0.3 +2.0 +2.0 -0.0 -2.1 -1.1 -0.5 -1.4 -0.5 +0.5 +0.5 +1.6 +0.9 +2.1 -2.4 -2.8 -1.2 -3.6 -4.4 -4.2 -3.8 -4.0 -8.3 -14.1 -10.4 -10.3 -9.3 -7.3 -11.7 -3.8 -2.5 -3.7
substrate: -0.3 -0.1 +1.8 +1.2 -0.7 -2.2 -1.2 -0.5 -1.4 -0.1 +0.5 +0.4 +0.7 +0.1 +0.6 -1.4 -1.7 -0.1 -1.9 -2.3 -2.5 -1.3 -1.1 -3.0 -9.4 -2.7 -1.8 -2.0 -1.0 -2.5 +1.4 +2.8 +1.4
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -3.7 -3.7 -3.6 -3.7 -3.7 -3.4 -3.6 -3.6 -3.6 -3.6 -3.4 -3.4 -3.2 -2.9 -0.3 +0.5 +0.5 +0.9 +0.8 +0.9 +1.0 +1.0 +1.3 +1.2 +1.3 +1.1 +1.1 +1.1 +1.4 +1.3 +1.4 +1.4
layers where the patch alone flips baseline to drive: [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -3.68 (model -3.75), sub +1.42 (model +1.38)
top Δ attention layers: L25 +1.38, L24 +0.70, L31 +0.57, L27 +0.41, L23 -0.36
top Δ MLP layers:       L29 -2.17, L28 +1.75, L31 +1.19, L22 +0.74, L25 -0.61
top Δ heads: L25H15 +0.82, L24H17 +0.75, L25H5 +0.56, L31H1 +0.46, L27H7 +0.36, L23H22 -0.30, L31H21 +0.26, L30H27 -0.24

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.549, max layer L2 (0.786)
- hdr_user: mean 0.003, max layer L8 (0.009)
- line1: mean 0.004, max layer L0 (0.018)
- line2: mean 0.006, max layer L11 (0.024)
- line3: mean 0.005, max layer L0 (0.031)
- line4: mean 0.003, max layer L0 (0.022)
- line5: mean 0.004, max layer L0 (0.032)
- line6: mean 0.003, max layer L0 (0.016)
- question: mean 0.077, max layer L13 (0.203)
- answer_instr: mean 0.042, max layer L11 (0.142)
- asst_header: mean 0.147, max layer L31 (0.274)
- last: mean 0.059, max layer L31 (0.223)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L25H5 mass 0.04 Δ+0.56, L27H16 mass 0.19 Δ+0.13, L15H11 mass 0.17 Δ+0.11, L21H14 mass 0.18 Δ+0.11, L24H17 mass 0.02 Δ+0.75, L30H26 mass 0.17 Δ+0.09

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +2.38 |
| loo_line2 | +1.15 |
| loo_line3 | +0.77 |
| loo_line4 | +2.00 |
| loo_line5 | +1.01 |
| loo_line6 | +1.63 |
| loo_line7 | +2.38 |
| loo_line8 | +1.26 |
| loo_line9 | +0.40 |
| only_line1 | -3.69 |
| only_line2 | -4.07 |
| only_line3 | -1.83 |
| only_line4 | -3.33 |
| only_line5 | -1.34 |
| only_line6 | -2.47 |
| only_line7 | +0.26 |
| only_line8 | +1.38 |
| only_line9 | -2.18 |
| headers_only | -4.20 |

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
| baseline | -3.69 | -3.69 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_CoT | -3.22 | -3.22 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_correct | +9.55 | +9.55 @0 | 'drive' | 'drive<|eot_id|>' |
| benchmark_encourage | -4.05 | -4.05 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_expert | -2.80 | -2.80 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_hallucination | -2.58 | -2.58 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_nomistakes | -3.09 | -3.09 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_threat | -4.53 | -4.53 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_urgency | -0.93 | -0.93 @0 | 'walk' | 'walk<|eot_id|>' |
| substrate | +1.39 | +1.39 @0 | 'drive' | 'drive<|eot_id|>' |
