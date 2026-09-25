# Qwen2.5-1.5B-Instruct (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 12 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +1.53 | 0.822 | 0.178 | 'drive<|im_end|>' |
| substrate | +2.02 | 0.883 | 0.117 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +5.6 +0.7 +3.3 +2.0 +2.1 +1.1 +2.5 +1.9 +0.0 -0.2 +0.9 +1.9 +2.3 +3.0 +1.0 +0.7 +1.6 +2.7 +1.3 +1.9 -2.3 -1.6 -1.2 -3.5 -1.1 -1.4 +1.0 +1.5
substrate: +nan +7.0 +0.5 +2.6 +2.7 +3.6 +4.8 +4.3 +3.3 +0.7 +0.6 +1.6 +2.5 +2.8 +2.3 +1.6 +0.9 +2.4 +3.1 +1.9 +2.4 -1.6 -0.9 -2.1 -3.6 -0.8 -1.4 +1.4 +2.0
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +1.7 +1.5 +1.4 +1.7 +1.5 +1.7 +1.6 +1.8 +2.0 +2.0 +2.3 +2.1 +2.3 +2.5 +2.5 +2.6 +2.3 +1.5 +0.7 +0.2 +2.5 +2.3 +2.1 +2.3 +2.1 +2.0 +2.0 +2.0
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +1.50 (model +1.50), sub +1.98 (model +2.00)
top Δ attention layers: L27 +0.70, L22 -0.59, L20 +0.39, L11 -0.33, L25 -0.28
top Δ MLP layers:       L27 -0.57, L23 +0.49, L6 -0.37, L4 -0.36, L20 -0.36
top Δ heads: L27H4 +0.63, L22H7 -0.53, L21H1 +0.27, L20H4 +0.24, L27H10 +0.21, L22H9 -0.20, L27H11 -0.17, L25H4 -0.16

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.312, max layer L25 (0.619)
- hdr_user: mean 0.007, max layer L5 (0.023)
- line1: mean 0.009, max layer L27 (0.029)
- line2: mean 0.009, max layer L11 (0.026)
- line3: mean 0.008, max layer L0 (0.023)
- line4: mean 0.004, max layer L0 (0.018)
- line5: mean 0.005, max layer L0 (0.027)
- line6: mean 0.004, max layer L0 (0.014)
- question: mean 0.141, max layer L20 (0.513)
- answer_instr: mean 0.055, max layer L11 (0.195)
- asst_header: mean 0.234, max layer L0 (0.497)
- last: mean 0.119, max layer L0 (0.311)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L27H4 mass 0.08 Δ+0.63, L27H10 mass 0.15 Δ+0.21, L21H1 mass 0.11 Δ+0.27, L5H5 mass 0.23 Δ+0.13, L12H3 mass 0.15 Δ+0.11, L27H3 mass 0.11 Δ+0.14

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +2.41 |
| loo_line2 | +1.66 |
| loo_line3 | +2.66 |
| loo_line4 | +2.03 |
| loo_line5 | +2.03 |
| loo_line6 | +2.52 |
| loo_line7 | +2.28 |
| loo_line8 | +2.66 |
| loo_line9 | +2.14 |
| only_line1 | +4.28 |
| only_line2 | +4.91 |
| only_line3 | +2.80 |
| only_line4 | +3.81 |
| only_line5 | +2.92 |
| only_line6 | +2.41 |
| only_line7 | +2.53 |
| only_line8 | +2.66 |
| only_line9 | +4.42 |
| headers_only | +3.92 |

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
| baseline | +1.53 | +1.53 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_CoT | +0.20 | +0.20 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_encourage | -0.60 | -0.60 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_expert | +1.55 | +1.55 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_goaloriented | +0.81 | +0.81 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_hallucination | +2.14 | +2.14 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_nomistakes | +2.25 | +2.25 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_threat | +1.53 | +1.53 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_urgency | +0.80 | +0.80 @0 | 'drive' | 'drive<|im_end|>' |
| substrate | +2.02 | +2.02 @0 | 'drive' | 'drive<|im_end|>' |
