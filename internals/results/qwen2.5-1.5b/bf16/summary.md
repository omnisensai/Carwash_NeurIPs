# Qwen/Qwen2.5-1.5B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 12 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +0.90 | 0.711 | 0.289 | 'drive<|im_end|>' |
| substrate | +2.02 | 0.883 | 0.117 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +5.0 -0.3 +2.2 +2.0 +1.6 +1.5 +2.4 +1.6 +0.1 -0.1 +0.3 +1.5 +2.0 +2.5 +0.8 +0.6 +1.3 +2.4 +0.8 +1.5 -2.8 -2.4 -2.4 -4.8 -2.4 -2.5 +0.4 +1.0
substrate: +nan +7.0 +0.6 +2.5 +2.8 +3.6 +4.8 +4.2 +3.3 +0.7 +0.7 +1.5 +2.5 +3.0 +2.5 +1.6 +1.0 +2.5 +3.1 +2.0 +2.4 -1.4 -0.9 -2.1 -3.5 -0.7 -1.4 +1.5 +2.0
final lens row == model logits: base False, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +0.5 +0.4 +0.5 +0.6 +0.5 +0.7 +0.7 +0.8 +1.0 +1.1 +1.3 +1.2 +1.4 +1.5 +1.5 +1.6 +1.8 +0.6 +0.1 -0.1 +2.3 +2.1 +2.0 +2.3 +2.3 +2.1 +2.1 +2.0
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +0.88 (model +0.88), sub +2.01 (model +2.00)
top Δ attention layers: L27 +0.91, L20 +0.50, L25 -0.46, L11 -0.31, L22 -0.25
top Δ MLP layers:       L27 -0.78, L23 +0.60, L20 -0.41, L11 +0.35, L24 +0.33
top Δ heads: L27H4 +0.89, L21H1 +0.25, L25H4 -0.24, L22H7 -0.24, L20H4 +0.23, L27H10 +0.20, L24H8 -0.18, L27H11 -0.18

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.312, max layer L25 (0.621)
- hdr_user: mean 0.007, max layer L5 (0.024)
- line1: mean 0.009, max layer L27 (0.028)
- line2: mean 0.008, max layer L11 (0.028)
- line3: mean 0.008, max layer L0 (0.023)
- line4: mean 0.004, max layer L0 (0.018)
- line5: mean 0.005, max layer L0 (0.027)
- line6: mean 0.004, max layer L0 (0.014)
- question: mean 0.139, max layer L20 (0.497)
- answer_instr: mean 0.056, max layer L11 (0.192)
- asst_header: mean 0.235, max layer L0 (0.497)
- last: mean 0.119, max layer L0 (0.311)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L27H4 mass 0.08 Δ+0.89, L5H5 mass 0.23 Δ+0.17, L21H1 mass 0.11 Δ+0.25, L27H10 mass 0.14 Δ+0.20, L12H3 mass 0.14 Δ+0.11, L26H3 mass 0.07 Δ+0.17

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +2.03 |
| loo_line2 | +1.65 |
| loo_line3 | +2.66 |
| loo_line4 | +1.90 |
| loo_line5 | +2.03 |
| loo_line6 | +2.65 |
| loo_line7 | +2.52 |
| loo_line8 | +3.03 |
| loo_line9 | +1.76 |
| only_line1 | +3.91 |
| only_line2 | +3.92 |
| only_line3 | +3.05 |
| only_line4 | +3.92 |
| only_line5 | +2.93 |
| only_line6 | +2.53 |
| only_line7 | +2.78 |
| only_line8 | +2.40 |
| only_line9 | +4.30 |
| headers_only | +3.90 |

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
| baseline | +0.90 | +0.90 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_CoT | +0.07 | +0.07 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_correct | +5.01 | +5.01 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | -0.85 | -0.85 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_expert | +1.21 | +1.21 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_hallucination | +2.02 | +2.02 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_nomistakes | +2.25 | +2.25 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_threat | +1.78 | +1.78 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_urgency | +0.53 | +0.53 @0 | 'drive' | 'drive<|im_end|>' |
| substrate | +2.02 | +2.02 @0 | 'drive' | 'drive<|im_end|>' |
