# Qwen/Qwen2.5-3B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 36 · heads 16 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +5.00 | 0.993 | 0.007 | 'drive<|im_end|>' |
| substrate | +12.62 | 1.000 | 0.000 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan -7.0 -0.8 -3.1 -2.7 -4.7 -6.0 -4.4 -5.2 -4.3 -1.4 -3.7 -5.0 +0.4 -1.9 -1.1 -2.7 -0.2 -0.9 -1.8 +0.4 -1.4 -1.2 -1.5 -0.3 -1.7 -0.1 -2.9 +3.5 +1.1 +0.6 -0.1 +6.0 +5.5 +5.5 +4.8 +5.0
substrate: +nan -7.3 -1.5 -3.5 -3.9 -6.2 -6.9 -4.7 -5.5 -3.8 -1.4 -4.2 -5.7 +0.9 -1.4 -0.6 -2.7 +0.1 -1.3 -1.7 +0.1 -1.1 +0.1 -1.0 +0.1 -0.1 +3.1 -0.2 +4.2 +1.7 +1.5 +0.3 +10.2 +12.6 +14.5 +10.4 +12.6
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +4.8 +4.3 +4.8 +4.8 +4.8 +4.5 +5.0 +4.5 +5.2 +4.7 +4.8 +4.8 +4.8 +4.8 +4.8 +4.7 +5.0 +4.7 +4.7 +4.5 +4.7 +4.7 +5.2 +6.7 +7.7 +7.5 +8.7 +9.2 +10.6 +10.0 +9.5 +8.0 +10.0 +12.6 +12.5 +12.6
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +4.80 (model +5.00), sub +12.56 (model +12.62)
top Δ attention layers: L33 +4.74, L32 +2.95, L31 +1.08, L24 +0.30, L28 +0.25
top Δ MLP layers:       L34 -1.87, L31 +1.33, L35 -1.05, L27 -0.49, L33 -0.40
top Δ heads: L33H0 +3.02, L32H9 +1.74, L32H7 +1.18, L33H15 +1.06, L34H10 -0.85, L34H8 -0.80, L34H9 +0.74, L31H5 +0.64

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.326, max layer L5 (0.759)
- hdr_user: mean 0.008, max layer L8 (0.031)
- line1: mean 0.008, max layer L8 (0.021)
- line2: mean 0.011, max layer L21 (0.044)
- line3: mean 0.007, max layer L0 (0.032)
- line4: mean 0.005, max layer L0 (0.027)
- line5: mean 0.006, max layer L0 (0.041)
- line6: mean 0.004, max layer L0 (0.020)
- question: mean 0.093, max layer L27 (0.199)
- answer_instr: mean 0.055, max layer L12 (0.182)
- asst_header: mean 0.237, max layer L2 (0.562)
- last: mean 0.112, max layer L0 (0.266)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H0 mass 0.08 Δ+3.02, L32H9 mass 0.04 Δ+1.74, L33H15 mass 0.05 Δ+1.06, L34H15 mass 0.09 Δ+0.58, L33H10 mass 0.06 Δ+0.45, L34H13 mass 0.12 Δ+0.18

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +14.50 |
| loo_line2 | +11.87 |
| loo_line3 | +14.87 |
| loo_line4 | +14.25 |
| loo_line5 | +13.37 |
| loo_line6 | +13.75 |
| loo_line7 | +14.12 |
| loo_line8 | +14.37 |
| loo_line9 | +13.75 |
| only_line1 | +9.00 |
| only_line2 | +8.25 |
| only_line3 | +10.00 |
| only_line4 | +10.37 |
| only_line5 | +10.50 |
| only_line6 | +9.75 |
| only_line7 | +13.37 |
| only_line8 | +16.25 |
| only_line9 | +12.00 |
| headers_only | +6.75 |

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
| baseline | +5.00 | +5.00 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_CoT | +4.50 | +4.50 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_correct | +17.12 | +17.12 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | +4.75 | +4.75 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_expert | +4.25 | +4.25 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_hallucination | +6.50 | +6.50 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_nomistakes | +5.00 | +5.00 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_threat | +5.25 | +5.25 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_urgency | +7.25 | +7.25 @0 | 'drive' | 'drive<|im_end|>' |
| substrate | +12.62 | +12.62 @0 | 'drive' | 'drive<|im_end|>' |
