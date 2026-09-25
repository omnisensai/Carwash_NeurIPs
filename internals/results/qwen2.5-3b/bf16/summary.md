# Qwen2.5-3B-Instruct (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 36 · heads 16 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +4.50 | 0.989 | 0.011 | 'drive<|im_end|>' |
| substrate | +12.87 | 1.000 | 0.000 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan -7.0 -0.9 -3.2 -2.8 -4.8 -6.1 -4.5 -5.3 -4.4 -1.4 -3.8 -5.2 +0.4 -2.0 -1.1 -2.7 -0.2 -0.9 -1.8 +0.5 -1.2 -0.9 -1.3 -0.1 -1.4 +0.2 -2.6 +3.7 +1.2 +0.7 -0.1 +6.0 +5.2 +5.0 +4.6 +4.5
substrate: +nan -7.3 -1.5 -3.5 -4.0 -6.4 -6.9 -4.8 -5.6 -4.0 -1.4 -4.2 -5.7 +1.0 -1.4 -0.7 -2.7 +0.2 -1.1 -1.5 +0.2 -1.1 +0.1 -0.9 +0.3 +0.2 +3.3 -0.2 +4.3 +1.9 +2.0 +0.8 +10.6 +13.1 +15.4 +10.9 +12.9
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +4.8 +5.0 +5.0 +5.0 +5.0 +5.2 +4.7 +5.2 +5.0 +5.2 +5.2 +5.0 +4.7 +5.0 +5.0 +5.2 +5.0 +5.2 +5.0 +5.0 +4.7 +4.7 +5.7 +6.7 +8.9 +8.0 +9.5 +9.5 +10.9 +10.2 +9.7 +8.2 +10.2 +13.2 +13.0 +12.9
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +4.63 (model +4.50), sub +12.98 (model +12.88)
top Δ attention layers: L33 +5.77, L32 +3.17, L31 +1.06, L24 +0.30, L28 +0.28
top Δ MLP layers:       L34 -2.19, L31 +1.41, L35 -1.41, L33 -0.61, L27 -0.47
top Δ heads: L33H0 +3.26, L32H9 +1.99, L33H15 +1.35, L32H7 +1.18, L34H10 -0.86, L34H8 -0.85, L34H9 +0.74, L31H5 +0.64

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.326, max layer L5 (0.759)
- hdr_user: mean 0.008, max layer L8 (0.031)
- line1: mean 0.008, max layer L8 (0.021)
- line2: mean 0.011, max layer L21 (0.043)
- line3: mean 0.007, max layer L0 (0.032)
- line4: mean 0.004, max layer L0 (0.027)
- line5: mean 0.006, max layer L0 (0.041)
- line6: mean 0.004, max layer L0 (0.020)
- question: mean 0.093, max layer L27 (0.205)
- answer_instr: mean 0.055, max layer L12 (0.182)
- asst_header: mean 0.238, max layer L2 (0.567)
- last: mean 0.112, max layer L0 (0.266)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H0 mass 0.08 Δ+3.26, L32H9 mass 0.04 Δ+1.99, L33H15 mass 0.05 Δ+1.35, L34H15 mass 0.09 Δ+0.56, L33H5 mass 0.11 Δ+0.36, L33H10 mass 0.05 Δ+0.56

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +13.25 |
| loo_line2 | +12.12 |
| loo_line3 | +15.37 |
| loo_line4 | +13.62 |
| loo_line5 | +13.37 |
| loo_line6 | +13.87 |
| loo_line7 | +13.87 |
| loo_line8 | +14.62 |
| loo_line9 | +14.50 |
| only_line1 | +9.00 |
| only_line2 | +8.50 |
| only_line3 | +10.00 |
| only_line4 | +10.12 |
| only_line5 | +10.25 |
| only_line6 | +9.00 |
| only_line7 | +14.00 |
| only_line8 | +16.12 |
| only_line9 | +12.25 |
| headers_only | +7.25 |

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
| baseline | +4.50 | +4.50 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_CoT | +4.25 | +4.25 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | +4.25 | +4.25 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_expert | +3.75 | +3.75 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_goaloriented | +6.50 | +6.50 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_hallucination | +7.25 | +7.25 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_nomistakes | +4.75 | +4.75 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_threat | +5.00 | +5.00 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_urgency | +7.50 | +7.50 @0 | 'drive' | 'drive<|im_end|>' |
| substrate | +12.87 | +12.87 @0 | 'drive' | 'drive<|im_end|>' |
