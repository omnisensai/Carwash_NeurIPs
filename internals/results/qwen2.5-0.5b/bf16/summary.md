# Qwen2.5-0.5B-Instruct (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 24 · heads 14 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +0.75 | 0.678 | 0.320 | 'Drive<|im_end|>' |
| substrate | -0.47 | 0.383 | 0.613 | 'Walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan -5.3 -0.5 -2.2 -6.3 -3.1 +0.5 -2.0 -1.4 -1.3 -2.7 -2.2 -1.2 -0.3 +2.3 +1.1 +1.0 +3.0 +3.5 +3.0 +1.1 -0.2 -1.1 -0.4 +0.8
substrate: +nan -4.8 -0.5 -2.3 -6.0 -4.1 -2.2 -4.1 -3.1 -2.1 -2.8 -2.2 -1.3 -1.0 +1.6 +1.0 +1.6 +2.8 +3.2 +3.7 +2.0 +0.3 -1.4 -1.0 -0.5
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +0.6 +0.6 +0.6 +0.6 +0.3 +0.3 -0.1 -0.1 -0.2 -0.4 -0.5 -0.1 -0.6 -1.1 -1.1 -1.1 -1.1 -1.2 -1.1 -1.4 -0.9 -0.7 -0.6 -0.5
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +0.70 (model +0.75), sub -0.55 (model -0.50)
top Δ attention layers: L23 -0.32, L14 +0.18, L5 -0.14, L7 +0.12, L17 +0.09
top Δ MLP layers:       L20 -0.77, L18 +0.34, L21 -0.33, L23 -0.30, L5 -0.29
top Δ heads: L23H10 -0.33, L21H13 -0.23, L23H12 +0.22, L21H9 +0.20, L23H3 -0.18, L23H7 -0.16, L15H10 -0.16, L21H3 +0.15

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.310, max layer L11 (0.617)
- hdr_user: mean 0.011, max layer L5 (0.048)
- line1: mean 0.010, max layer L22 (0.030)
- line2: mean 0.011, max layer L22 (0.030)
- line3: mean 0.009, max layer L22 (0.041)
- line4: mean 0.004, max layer L22 (0.015)
- line5: mean 0.005, max layer L0 (0.018)
- line6: mean 0.003, max layer L0 (0.014)
- question: mean 0.142, max layer L14 (0.339)
- answer_instr: mean 0.043, max layer L10 (0.186)
- asst_header: mean 0.240, max layer L2 (0.552)
- last: mean 0.117, max layer L23 (0.252)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L22H0 mass 0.24 Δ+0.11, L3H3 mass 0.19 Δ+0.09, L23H12 mass 0.06 Δ+0.22, L22H4 mass 0.24 Δ+0.04, L23H11 mass 0.12 Δ+0.07, L14H9 mass 0.08 Δ+0.09

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -0.12 |
| loo_line2 | -0.22 |
| loo_line3 | -0.78 |
| loo_line4 | -0.71 |
| loo_line5 | -0.90 |
| loo_line6 | -0.72 |
| loo_line7 | -0.71 |
| loo_line8 | -0.60 |
| loo_line9 | -0.07 |
| only_line1 | -0.61 |
| only_line2 | -0.78 |
| only_line3 | -0.60 |
| only_line4 | -0.74 |
| only_line5 | -0.36 |
| only_line6 | -0.76 |
| only_line7 | +0.88 |
| only_line8 | +0.25 |
| only_line9 | -0.49 |
| headers_only | -0.37 |

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
| baseline | +0.75 | +0.75 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_CoT | +0.63 | +0.63 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_encourage | -0.22 | -0.22 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | +0.50 | +0.50 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_goaloriented | +1.00 | +1.00 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_hallucination | +0.00 | +0.00 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_nomistakes | -0.26 | -0.26 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_threat | -0.65 | -0.65 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | +1.25 | +1.25 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate | -0.47 | -0.47 @0 | 'Walk' | 'Walk<|im_end|>' |
