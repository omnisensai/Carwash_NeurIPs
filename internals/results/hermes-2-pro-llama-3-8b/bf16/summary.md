# Hermes-2-Pro-Llama-3-8B (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -7.26 | 0.001 | 0.999 | 'walk<|im_end|>' |
| substrate | +5.43 | 0.988 | 0.004 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  -0.3 +2.0 +0.3 +3.7 +2.7 -0.9 -2.9 -1.4 -0.6 -0.1 +1.0 +1.9 +1.4 -0.8 +2.4 -0.5 -1.3 -1.4 -4.3 -5.4 -4.6 -3.4 -4.2 -7.0 -11.6 -10.2 -11.8 -10.9 -10.6 -12.7 -6.8 -5.8 -7.3
substrate: -0.3 +0.8 -0.7 +2.6 +0.9 -2.1 -2.6 -1.2 +0.1 -1.0 +0.9 +2.1 +1.0 -1.2 +1.8 +0.4 +0.9 +0.8 +0.6 -1.0 -0.7 +2.2 +2.9 +2.5 -2.6 +4.6 +6.4 +5.2 +4.8 +4.6 +5.1 +6.3 +5.4
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -7.3 -7.3 -7.3 -7.3 -7.3 -7.2 -7.2 -7.5 -7.1 -7.5 -7.1 -7.3 -7.0 -5.4 +2.6 +3.0 +2.9 +4.0 +4.1 +4.1 +4.1 +4.5 +4.9 +4.9 +5.0 +5.2 +5.1 +5.1 +5.3 +5.3 +5.3 +5.4
layers where the patch alone flips baseline to drive: [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -7.28 (model -7.25), sub +5.71 (model +5.62)
top Δ attention layers: L25 +3.09, L24 +1.97, L27 +0.81, L29 +0.64, L30 +0.60
top Δ MLP layers:       L31 +3.28, L29 -3.07, L28 +1.66, L30 +0.90, L25 -0.75
top Δ heads: L25H5 +2.11, L24H17 +1.39, L31H1 +1.10, L25H15 +1.04, L27H7 +1.00, L24H22 +0.46, L23H22 +0.42, L31H11 -0.38

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.548, max layer L2 (0.838)
- hdr_user: mean 0.004, max layer L6 (0.014)
- line1: mean 0.005, max layer L0 (0.015)
- line2: mean 0.007, max layer L0 (0.028)
- line3: mean 0.005, max layer L0 (0.027)
- line4: mean 0.003, max layer L0 (0.019)
- line5: mean 0.004, max layer L0 (0.028)
- line6: mean 0.004, max layer L0 (0.015)
- question: mean 0.089, max layer L13 (0.225)
- answer_instr: mean 0.043, max layer L9 (0.165)
- asst_header: mean 0.127, max layer L31 (0.262)
- last: mean 0.052, max layer L31 (0.206)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L25H5 mass 0.06 Δ+2.11, L23H22 mass 0.08 Δ+0.42, L24H17 mass 0.02 Δ+1.39, L27H7 mass 0.03 Δ+1.00, L21H14 mass 0.09 Δ+0.31, L24H22 mass 0.04 Δ+0.46

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +5.39 |
| loo_line2 | +5.19 |
| loo_line3 | +4.56 |
| loo_line4 | +5.54 |
| loo_line5 | +5.17 |
| loo_line6 | +5.14 |
| loo_line7 | +5.66 |
| loo_line8 | +4.79 |
| loo_line9 | +4.54 |
| only_line1 | -1.38 |
| only_line2 | -3.37 |
| only_line3 | -0.29 |
| only_line4 | -2.63 |
| only_line5 | -0.79 |
| only_line6 | -2.37 |
| only_line7 | +0.06 |
| only_line8 | +2.28 |
| only_line9 | -1.39 |
| headers_only | -3.49 |

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
| baseline | -7.26 | -7.26 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -6.62 | -6.62 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_encourage | -5.99 | -5.99 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_expert | -9.39 | -9.39 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_goaloriented | -4.01 | -4.01 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -6.59 | -6.59 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -5.86 | -5.86 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -6.62 | -6.62 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_urgency | -4.38 | -4.38 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | +5.43 | +5.43 @0 | 'drive' | 'drive<|im_end|>' |
