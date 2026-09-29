# unsloth/Llama-3.2-3B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 24 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -0.38 | 0.400 | 0.583 | 'walk.<|eot_id|>' |
| substrate | +0.17 | 0.535 | 0.451 | 'drive<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  +0.0 -2.4 -1.7 -0.6 +0.8 -0.0 -0.4 -0.4 +0.1 +1.3 +0.7 -0.4 -1.1 -0.2 -2.6 -0.8 -3.3 -2.4 -2.0 -1.1 -1.8 -10.1 -15.1 -5.0 -4.3 -1.6 -2.1 -0.2 -0.4
substrate: +0.0 -2.2 -1.3 -0.8 +0.9 +0.2 +0.1 -0.3 +0.4 +1.5 +0.9 -0.3 -0.5 -0.4 -2.8 -0.8 -2.5 -1.2 -1.0 +0.0 -1.0 -9.4 -14.4 -2.8 -2.3 +0.0 -0.6 +1.3 +0.2
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -0.4 -0.3 -0.4 -0.3 -0.4 -0.4 -0.4 -0.4 -0.4 -0.4 -0.3 -0.2 -0.3 +0.0 +0.5 +0.8 +0.8 +0.8 +0.8 +0.8 +0.8 +0.4 +0.4 +0.5 +0.4 +0.4 +0.2 +0.2
layers where the patch alone flips baseline to drive: [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -0.53 (model -0.50), sub +0.10 (model +0.12)
top Δ attention layers: L22 +0.57, L24 +0.50, L26 -0.34, L27 -0.27, L21 +0.26
top Δ MLP layers:       L24 -0.42, L26 +0.31, L20 +0.24, L22 -0.21, L23 +0.19
top Δ heads: L22H11 +0.61, L24H12 +0.19, L23H11 -0.18, L24H5 +0.16, L27H1 +0.13, L21H17 +0.13, L20H16 -0.11, L27H11 -0.10

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.585, max layer L2 (0.865)
- hdr_user: mean 0.002, max layer L5 (0.005)
- line1: mean 0.003, max layer L0 (0.008)
- line2: mean 0.005, max layer L10 (0.013)
- line3: mean 0.004, max layer L0 (0.013)
- line4: mean 0.002, max layer L0 (0.011)
- line5: mean 0.003, max layer L0 (0.016)
- line6: mean 0.002, max layer L0 (0.010)
- question: mean 0.072, max layer L12 (0.214)
- answer_instr: mean 0.045, max layer L7 (0.128)
- asst_header: mean 0.136, max layer L27 (0.296)
- last: mean 0.053, max layer L27 (0.221)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L15H20 mass 0.21 Δ+0.08, L24H12 mass 0.06 Δ+0.19, L16H16 mass 0.08 Δ+0.05, L12H16 mass 0.13 Δ+0.03, L26H2 mass 0.13 Δ+0.03, L12H8 mass 0.12 Δ+0.03

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +0.41 |
| loo_line2 | +0.42 |
| loo_line3 | +0.17 |
| loo_line4 | +0.30 |
| loo_line5 | +0.05 |
| loo_line6 | +0.17 |
| loo_line7 | +0.79 |
| loo_line8 | +0.55 |
| loo_line9 | -0.32 |
| only_line1 | -0.53 |
| only_line2 | -1.05 |
| only_line3 | +0.05 |
| only_line4 | -0.81 |
| only_line5 | -0.43 |
| only_line6 | -0.07 |
| only_line7 | -0.22 |
| only_line8 | -0.46 |
| only_line9 | -0.05 |
| headers_only | -0.67 |

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
| baseline | -0.38 | -0.38 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_CoT | -0.40 | -0.40 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_correct | +6.00 | +6.00 @0 | 'drive' | 'drive.<|eot_id|>' |
| benchmark_encourage | -1.10 | -1.10 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_expert | +0.03 | +0.03 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_hallucination | -0.19 | -0.19 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_nomistakes | -0.70 | -0.70 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_threat | -0.72 | -0.72 @0 | 'walk' | 'walk.<|eot_id|>' |
| benchmark_urgency | -1.14 | -1.14 @0 | 'walk' | 'walk.<|eot_id|>' |
| substrate | +0.17 | +0.17 @0 | 'drive' | 'drive<|eot_id|>' |
