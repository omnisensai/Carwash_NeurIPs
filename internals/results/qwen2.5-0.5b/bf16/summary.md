# Qwen/Qwen2.5-0.5B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 24 · heads 14 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +0.50 | 0.621 | 0.376 | 'Drive<|im_end|>' |
| substrate | -0.43 | 0.394 | 0.603 | 'Walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan -5.5 -0.5 -2.3 -6.5 -3.1 +0.5 -2.1 -1.4 -1.4 -2.8 -2.3 -1.3 -0.4 +2.3 +1.1 +1.0 +2.9 +3.6 +3.1 +1.1 -0.4 -1.4 -0.7 +0.5
substrate: +nan -5.5 -0.7 -2.4 -5.9 -4.3 -2.2 -4.3 -3.3 -2.2 -3.0 -2.3 -1.4 -1.1 +1.5 +1.1 +1.6 +3.1 +3.4 +3.9 +2.1 +0.3 -1.4 -1.0 -0.4
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +0.5 +0.6 +0.4 +0.5 +0.1 +0.0 -0.2 -0.2 -0.4 -0.5 -0.6 -0.4 -0.7 -1.2 -1.1 -1.2 -1.1 -1.2 -1.2 -1.3 -0.8 -0.4 -0.5 -0.4
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +0.51 (model +0.50), sub -0.51 (model -0.50)
top Δ attention layers: L23 -0.38, L20 +0.17, L14 +0.16, L16 +0.14, L5 -0.12
top Δ MLP layers:       L20 -0.82, L18 +0.37, L23 -0.32, L21 -0.31, L15 +0.28
top Δ heads: L23H10 -0.34, L21H13 -0.20, L23H12 +0.19, L21H9 +0.19, L21H3 +0.18, L23H7 -0.18, L15H10 -0.15, L23H3 -0.14

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.311, max layer L11 (0.620)
- hdr_user: mean 0.011, max layer L5 (0.046)
- line1: mean 0.009, max layer L22 (0.030)
- line2: mean 0.011, max layer L22 (0.030)
- line3: mean 0.009, max layer L22 (0.041)
- line4: mean 0.004, max layer L22 (0.015)
- line5: mean 0.005, max layer L0 (0.018)
- line6: mean 0.003, max layer L0 (0.014)
- question: mean 0.143, max layer L14 (0.341)
- answer_instr: mean 0.044, max layer L10 (0.185)
- asst_header: mean 0.239, max layer L2 (0.552)
- last: mean 0.118, max layer L23 (0.248)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L22H0 mass 0.24 Δ+0.10, L3H3 mass 0.20 Δ+0.09, L23H12 mass 0.06 Δ+0.19, L22H4 mass 0.24 Δ+0.04, L23H11 mass 0.13 Δ+0.07, L21H3 mass 0.04 Δ+0.18

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -0.37 |
| loo_line2 | -0.10 |
| loo_line3 | -0.88 |
| loo_line4 | -0.84 |
| loo_line5 | -0.58 |
| loo_line6 | -0.79 |
| loo_line7 | -0.58 |
| loo_line8 | -0.71 |
| loo_line9 | +0.07 |
| only_line1 | -0.73 |
| only_line2 | -0.92 |
| only_line3 | -0.75 |
| only_line4 | -0.37 |
| only_line5 | -0.48 |
| only_line6 | -0.75 |
| only_line7 | +0.65 |
| only_line8 | +0.27 |
| only_line9 | -0.35 |
| headers_only | -0.50 |

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
| baseline | +0.50 | +0.50 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_CoT | +0.63 | +0.63 @0 | 'Drive' | 'Drive.<|im_end|>' |
| benchmark_correct | +1.29 | +1.29 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_encourage | -0.35 | -0.35 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | +0.75 | +0.75 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_hallucination | -0.12 | -0.12 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | -0.14 | -0.14 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_threat | -0.49 | -0.49 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_urgency | +1.12 | +1.12 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate | -0.43 | -0.43 @0 | 'Walk' | 'Walk<|im_end|>' |
