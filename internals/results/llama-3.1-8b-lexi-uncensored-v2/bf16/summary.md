# Llama-3.1-8B-Lexi-Uncensored-V2 (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -2.66 | 0.065 | 0.933 | 'walk<|eot_id|>' |
| substrate | +1.05 | 0.736 | 0.257 | 'drive.<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -0.3 +0.3 +2.0 +2.0 -0.0 -2.1 -1.1 -0.3 -1.3 -0.6 +0.7 +0.4 +1.5 +0.6 +1.7 -2.5 -2.2 -0.7 -3.2 -3.8 -3.5 -3.0 -2.9 -7.1 -13.2 -9.0 -8.6 -7.9 -6.6 -10.5 -3.4 -2.1 -2.7
substrate: -0.3 -0.1 +1.8 +1.2 -0.7 -2.2 -1.2 -0.4 -1.2 -0.1 +0.8 +0.2 +0.5 -0.3 +0.4 -1.9 -1.7 +0.1 -2.1 -2.4 -2.4 -1.3 -1.1 -3.2 -9.6 -3.4 -2.3 -2.5 -1.9 -3.1 +0.9 +2.1 +1.1
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -2.8 -2.7 -2.7 -2.7 -2.7 -2.7 -2.6 -2.6 -2.7 -2.7 -2.6 -2.6 -2.3 -1.9 -0.1 +0.5 +0.6 +0.7 +0.7 +0.8 +0.9 +0.9 +1.0 +0.9 +0.9 +0.8 +0.8 +0.9 +1.0 +1.0 +1.2 +1.1
layers where the patch alone flips baseline to drive: [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -2.67 (model -2.75), sub +1.02 (model +1.00)
top Δ attention layers: L25 +0.78, L24 +0.45, L27 +0.41, L23 -0.40, L31 +0.30
top Δ MLP layers:       L29 -1.63, L28 +1.47, L31 +0.68, L22 +0.62, L23 +0.59
top Δ heads: L24H17 +0.48, L25H5 +0.42, L25H15 +0.35, L23H22 -0.35, L31H1 +0.28, L27H7 +0.28, L28H20 +0.21, L30H27 -0.19

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.549, max layer L2 (0.784)
- hdr_user: mean 0.004, max layer L8 (0.009)
- line1: mean 0.004, max layer L0 (0.018)
- line2: mean 0.006, max layer L0 (0.024)
- line3: mean 0.005, max layer L0 (0.031)
- line4: mean 0.002, max layer L0 (0.022)
- line5: mean 0.004, max layer L0 (0.032)
- line6: mean 0.003, max layer L0 (0.016)
- question: mean 0.073, max layer L13 (0.174)
- answer_instr: mean 0.043, max layer L11 (0.142)
- asst_header: mean 0.146, max layer L31 (0.270)
- last: mean 0.059, max layer L31 (0.217)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L27H16 mass 0.18 Δ+0.10, L25H5 mass 0.04 Δ+0.42, L15H11 mass 0.16 Δ+0.10, L21H14 mass 0.17 Δ+0.07, L28H20 mass 0.06 Δ+0.21, L30H26 mass 0.14 Δ+0.07

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +1.64 |
| loo_line2 | +1.03 |
| loo_line3 | +0.56 |
| loo_line4 | +1.28 |
| loo_line5 | +0.79 |
| loo_line6 | +1.15 |
| loo_line7 | +1.53 |
| loo_line8 | +0.80 |
| loo_line9 | +0.43 |
| only_line1 | -2.55 |
| only_line2 | -2.78 |
| only_line3 | -1.30 |
| only_line4 | -2.55 |
| only_line5 | -0.80 |
| only_line6 | -1.81 |
| only_line7 | +0.04 |
| only_line8 | +1.14 |
| only_line9 | -1.53 |
| headers_only | -3.14 |

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
| baseline | -2.66 | -2.66 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_CoT | -2.35 | -2.35 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_encourage | -2.92 | -2.92 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_expert | -1.72 | -1.72 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_goaloriented | -0.18 | -0.18 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_hallucination | -1.70 | -1.70 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_nomistakes | -1.84 | -1.84 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_threat | -3.31 | -3.31 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_urgency | -0.43 | -0.43 @0 | 'walk' | 'walk<|eot_id|>' |
| substrate | +1.05 | +1.05 @0 | 'drive' | 'drive.<|eot_id|>' |
