# Qwen/Qwen3-0.6B

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 16 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +2.25 | 0.903 | 0.095 | 'drive<|im_end|>' |
| substrate | +4.62 | 0.990 | 0.010 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +1.3 +1.2 +5.4 +6.6 +5.8 +5.4 +4.6 +4.5 +5.8 +5.0 +3.1 +4.5 +3.1 +5.0 +6.4 +5.3 +3.0 +3.6 +2.3 +2.6 +1.2 +0.9 -1.4 +2.7 -1.3 -1.4 +1.9 +2.2
substrate: +nan +2.4 +1.4 +5.4 +6.4 +6.0 +5.8 +4.5 +4.6 +5.1 +5.0 +2.2 +3.2 +2.1 +3.8 +5.1 +3.5 +2.0 +3.6 +1.5 +1.9 +1.5 +2.2 +0.3 +4.0 +0.5 -0.3 +3.0 +4.6
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +2.4 +2.2 +2.1 +2.4 +2.2 +2.2 +2.2 +2.2 +2.2 +2.2 +2.5 +2.4 +2.5 +2.2 +2.4 +2.4 +2.2 +2.6 +3.1 +3.2 +3.9 +4.5 +5.0 +5.1 +5.0 +4.6 +4.5 +4.6
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +2.24 (model +2.25), sub +4.64 (model +4.62)
top Δ attention layers: L24 +0.61, L27 +0.51, L21 +0.47, L23 +0.44, L20 +0.26
top Δ MLP layers:       L25 +0.29, L18 -0.20, L20 +0.19, L17 +0.17, L22 +0.14
top Δ heads: L27H15 +0.49, L24H6 +0.36, L26H7 -0.36, L23H15 +0.33, L22H7 -0.24, L26H9 -0.22, L21H13 +0.22, L23H6 +0.22

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.489, max layer L27 (0.802)
- hdr_user: mean 0.004, max layer L2 (0.017)
- line1: mean 0.006, max layer L3 (0.022)
- line2: mean 0.007, max layer L11 (0.039)
- line3: mean 0.004, max layer L0 (0.019)
- line4: mean 0.003, max layer L0 (0.017)
- line5: mean 0.004, max layer L0 (0.028)
- line6: mean 0.003, max layer L0 (0.015)
- question: mean 0.048, max layer L0 (0.119)
- answer_instr: mean 0.040, max layer L11 (0.129)
- asst_header: mean 0.267, max layer L1 (0.700)
- last: mean 0.118, max layer L9 (0.215)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L21H0 mass 0.15 Δ+0.20, L26H15 mass 0.12 Δ+0.20, L22H9 mass 0.11 Δ+0.20, L21H13 mass 0.09 Δ+0.22, L24H6 mass 0.03 Δ+0.36, L27H15 mass 0.02 Δ+0.49

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +4.62 |
| loo_line2 | +5.87 |
| loo_line3 | +5.12 |
| loo_line4 | +5.37 |
| loo_line5 | +4.87 |
| loo_line6 | +6.00 |
| loo_line7 | +5.62 |
| loo_line8 | +5.75 |
| loo_line9 | +5.00 |
| only_line1 | +5.25 |
| only_line2 | +4.37 |
| only_line3 | +5.25 |
| only_line4 | +5.12 |
| only_line5 | +4.62 |
| only_line6 | +5.25 |
| only_line7 | +5.75 |
| only_line8 | +7.50 |
| only_line9 | +6.37 |
| headers_only | +5.12 |

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
| baseline | +2.25 | +2.25 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_CoT | +2.50 | +2.50 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_correct | +14.00 | +14.00 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | +0.62 | +0.62 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_expert | +2.37 | +2.37 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_hallucination | +1.00 | +1.00 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_nomistakes | +1.50 | +1.50 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_threat | +1.25 | +1.25 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_urgency | +0.75 | +0.75 @0 | 'drive' | 'drive<|im_end|>' |
| substrate | +4.62 | +4.62 @0 | 'drive' | 'drive<|im_end|>' |
