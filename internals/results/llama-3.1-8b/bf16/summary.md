# Llama-3.1-8B-Instruct (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -3.71 | 0.024 | 0.975 | 'walk<|eot_id|>' |
| substrate | +1.51 | 0.816 | 0.180 | 'drive<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -0.3 +0.3 +2.0 +2.0 -0.0 -2.1 -1.1 -0.4 -1.4 -0.5 +0.4 +0.4 +1.6 +1.0 +2.0 -2.5 -2.8 -1.2 -3.6 -4.3 -4.1 -3.7 -4.0 -8.4 -14.2 -10.5 -10.4 -9.3 -7.5 -11.8 -4.0 -2.6 -3.7
substrate: -0.3 -0.1 +1.8 +1.2 -0.7 -2.2 -1.2 -0.6 -1.4 -0.2 +0.5 +0.3 +0.7 +0.0 +0.6 -1.4 -1.7 -0.1 -1.9 -2.3 -2.4 -1.3 -1.0 -2.9 -9.2 -2.6 -1.6 -1.8 -0.8 -2.2 +1.6 +2.9 +1.5
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -3.8 -3.7 -3.7 -3.7 -3.7 -3.7 -3.6 -3.5 -3.7 -3.7 -3.6 -3.5 -3.3 -2.9 -0.3 +0.5 +0.5 +0.9 +0.9 +0.9 +1.1 +1.1 +1.4 +1.3 +1.3 +1.3 +1.1 +1.4 +1.5 +1.4 +1.5 +1.5
layers where the patch alone flips baseline to drive: [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -3.75 (model -3.75), sub +1.50 (model +1.50)
top Δ attention layers: L25 +1.42, L24 +0.75, L31 +0.61, L27 +0.44, L23 -0.34
top Δ MLP layers:       L29 -2.26, L28 +1.77, L31 +1.18, L22 +0.76, L25 -0.59
top Δ heads: L25H15 +0.81, L24H17 +0.78, L25H5 +0.62, L31H1 +0.49, L27H7 +0.39, L31H21 +0.29, L23H22 -0.26, L30H27 -0.25

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.549, max layer L2 (0.784)
- hdr_user: mean 0.003, max layer L8 (0.009)
- line1: mean 0.004, max layer L0 (0.018)
- line2: mean 0.006, max layer L11 (0.025)
- line3: mean 0.005, max layer L0 (0.031)
- line4: mean 0.003, max layer L0 (0.022)
- line5: mean 0.004, max layer L0 (0.032)
- line6: mean 0.003, max layer L0 (0.016)
- question: mean 0.076, max layer L13 (0.200)
- answer_instr: mean 0.042, max layer L11 (0.141)
- asst_header: mean 0.147, max layer L31 (0.275)
- last: mean 0.059, max layer L31 (0.224)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L25H5 mass 0.04 Δ+0.62, L27H16 mass 0.18 Δ+0.13, L15H11 mass 0.18 Δ+0.12, L21H14 mass 0.18 Δ+0.11, L24H17 mass 0.02 Δ+0.78, L30H26 mass 0.16 Δ+0.10

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +2.50 |
| loo_line2 | +1.14 |
| loo_line3 | +0.65 |
| loo_line4 | +1.88 |
| loo_line5 | +1.02 |
| loo_line6 | +1.50 |
| loo_line7 | +2.25 |
| loo_line8 | +1.14 |
| loo_line9 | +0.40 |
| only_line1 | -3.45 |
| only_line2 | -3.83 |
| only_line3 | -1.83 |
| only_line4 | -3.33 |
| only_line5 | -1.34 |
| only_line6 | -2.46 |
| only_line7 | +0.26 |
| only_line8 | +1.50 |
| only_line9 | -2.06 |
| headers_only | -4.07 |

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
| baseline | -3.71 | -3.71 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_CoT | -3.33 | -3.33 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_encourage | -4.05 | -4.05 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_expert | -2.78 | -2.78 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_goaloriented | -0.35 | -0.35 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_hallucination | -2.82 | -2.82 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_nomistakes | -2.97 | -2.97 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_threat | -4.57 | -4.57 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_urgency | -0.83 | -0.83 @0 | 'walk' | 'walk<|eot_id|>' |
| substrate | +1.51 | +1.51 @0 | 'drive' | 'drive<|eot_id|>' |
