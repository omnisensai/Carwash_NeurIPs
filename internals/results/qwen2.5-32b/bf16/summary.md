# Qwen/Qwen2.5-32B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 64 · heads 40 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -17.75 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | +13.75 | 1.000 | 0.000 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +1.8 +1.0 +2.4 +1.9 +1.0 +0.3 +0.8 +0.2 -1.1 -0.9 -0.9 -0.9 -0.4 -0.3 -1.3 -1.2 -0.8 -1.3 -1.6 -1.6 -1.8 -2.1 -2.2 -1.3 -1.4 -2.6 -3.4 -2.6 -0.9 -3.1 -3.5 -4.8 -3.9 -2.3 -1.7 -1.9 -1.4 -1.8 +0.2 +0.6 +0.4 +0.6 +0.7 +1.8 +2.2 +1.1 -0.2 -1.4 -2.2 -4.5 -5.0 -3.8 -6.3 -8.0 -7.1 -7.2 -10.4 -11.4 -12.3 -15.2 -15.0 -12.6 -10.6 -10.4 -17.7
substrate: +1.8 +1.6 +2.7 +2.2 +1.5 +1.1 +1.4 +0.7 -0.6 -0.1 -0.7 -0.4 +0.3 +0.2 -0.6 -0.9 -0.3 -0.7 -1.2 -0.9 -0.5 -1.0 -0.7 +0.1 +0.4 -1.0 -1.2 -1.3 -0.0 -1.3 -1.4 -3.5 -2.5 -1.1 -0.3 -0.1 -0.1 -0.4 +1.3 +1.0 +1.1 +1.6 +2.3 +3.3 +3.1 +2.3 +0.4 -0.4 +0.2 +2.1 +1.1 +3.0 +5.4 +7.7 +8.7 +8.3 +9.0 +9.7 +10.1 +9.6 +16.4 +17.9 +14.4 +6.9 +13.7
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -17.7 -18.0 -17.7 -17.5 -18.0 -17.7 -17.7 -17.7 -17.7 -17.7 -17.7 -18.0 -17.5 -17.5 -17.7 -17.7 -17.5 -17.7 -17.7 -17.5 -17.5 -17.5 -17.7 -17.5 -17.5 -17.7 -17.5 -17.5 -17.2 -17.0 -17.2 -17.2 -17.2 -17.5 -17.2 -17.0 -17.0 -17.0 -17.0 -16.7 -17.0 -16.5 -17.0 -16.2 -12.5 -7.5 -6.0 +0.3 +6.5 +7.0 +7.5 +7.7 +8.7 +9.0 +9.2 +12.5 +12.5 +12.7 +12.7 +13.2 +13.2 +13.5 +13.5 +13.7
layers where the patch alone flips baseline to drive: [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -17.81 (model -17.75), sub +13.84 (model +13.75)
top Δ attention layers: L59 +5.05, L62 +3.75, L57 +1.59, L56 +1.33, L52 +1.13
top Δ MLP layers:       L63 +4.24, L62 -3.22, L60 +2.49, L59 +2.13, L55 +1.76
top Δ heads: L57H22 +1.52, L62H27 +1.52, L59H35 +1.46, L62H12 +1.16, L59H17 +1.01, L59H18 +0.98, L62H14 +0.94, L59H26 +0.84

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.012, max layer L5 (0.755)
- hdr_user: mean 0.005, max layer L6 (0.019)
- line1: mean 0.007, max layer L1 (0.031)
- line2: mean 0.009, max layer L1 (0.039)
- line3: mean 0.009, max layer L1 (0.047)
- line4: mean 0.006, max layer L1 (0.031)
- line5: mean 0.007, max layer L1 (0.052)
- line6: mean 0.006, max layer L2 (0.025)
- question: mean 0.118, max layer L50 (0.301)
- answer_instr: mean 0.044, max layer L30 (0.166)
- asst_header: mean 0.152, max layer L4 (0.458)
- last: mean 0.061, max layer L62 (0.163)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L48H32 mass 0.64 Δ+0.20, L57H22 mass 0.08 Δ+1.52, L46H38 mass 0.71 Δ+0.10, L62H27 mass 0.04 Δ+1.52, L52H36 mass 0.21 Δ+0.25, L56H26 mass 0.16 Δ+0.30

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +9.50 |
| loo_line2 | +13.50 |
| loo_line3 | +11.75 |
| loo_line4 | +14.25 |
| loo_line5 | +11.25 |
| loo_line6 | +13.25 |
| loo_line7 | +19.50 |
| loo_line8 | +8.25 |
| loo_line9 | -2.75 |
| only_line1 | -14.93 |
| only_line2 | -16.45 |
| only_line3 | -12.74 |
| only_line4 | -13.24 |
| only_line5 | -10.50 |
| only_line6 | -1.75 |
| only_line7 | -0.50 |
| only_line8 | +13.37 |
| only_line9 | +7.25 |
| headers_only | -14.46 |

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
| baseline | -17.75 | -17.75 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -16.00 | -16.00 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_correct | +9.50 | +9.50 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | -15.50 | -15.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_expert | -16.50 | -16.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -16.00 | -16.00 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -14.75 | -14.75 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -15.00 | -15.00 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_urgency | -16.00 | -16.00 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | +13.75 | +13.75 @0 | 'drive' | 'drive<|im_end|>' |
