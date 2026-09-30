# Qwen/Qwen2.5-72B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 80 · heads 64 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -9.37 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | +7.87 | 1.000 | 0.000 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  -3.7 -1.7 -1.0 -1.3 +0.1 -0.5 -0.2 +0.2 -0.1 -0.3 -0.3 -0.6 -0.6 -1.7 -1.7 -1.8 -1.7 -1.9 -2.2 -2.0 -1.4 -0.9 -0.2 -0.1 +0.3 +0.4 -0.0 -0.6 -0.6 -0.5 -0.0 +0.3 +0.4 +0.4 +0.8 +1.4 +1.5 +1.5 +2.5 +2.4 +2.8 +2.9 +2.9 +2.7 +2.6 +2.6 +3.1 +2.4 +2.1 +2.8 +2.7 +3.0 +3.1 +3.5 +3.4 +2.9 +1.8 +2.4 +1.4 +1.5 +1.1 +1.6 -0.1 +0.5 -0.2 +0.0 -1.4 -2.7 -4.8 -4.4 -6.2 -5.5 -4.1 -4.2 -2.6 -7.0 -5.6 -8.5 -6.1 -7.4 -9.4
substrate: -3.7 -2.6 -1.4 -0.9 -0.0 -0.3 -0.5 -0.1 -0.3 -0.7 -0.7 -0.8 -0.5 -1.7 -1.4 -1.6 -1.8 -1.8 -1.9 -1.7 -1.5 -0.9 -0.4 -0.5 +0.0 -0.1 -0.3 -1.3 -1.1 -0.9 -0.1 -0.1 -0.2 -0.1 +0.4 +0.7 +0.7 +0.7 +1.2 +1.0 +1.2 +1.3 +1.2 +1.5 +1.8 +1.7 +2.5 +2.1 +2.0 +2.7 +2.6 +3.0 +3.3 +3.9 +3.4 +3.4 +2.4 +3.1 +1.9 +1.8 +1.8 +3.2 +4.0 +4.8 +4.7 +5.3 +5.2 +5.5 +7.8 +8.1 +7.3 +10.0 +12.4 +13.1 +15.6 +14.9 +17.8 +18.5 +14.3 +6.4 +8.0
final lens row == model logits: base True, sub False

## patching (substrate residual into baseline at the answer position)
M per layer: -9.2 -9.4 -9.2 -9.1 -9.4 -9.2 -9.1 -9.1 -9.2 -9.0 -9.4 -9.2 -9.4 -9.1 -9.2 -9.5 -9.4 -9.5 -9.5 -9.4 -9.4 -9.6 -9.5 -9.6 -9.5 -9.4 -9.5 -9.5 -9.6 -9.4 -9.4 -9.4 -9.5 -9.5 -9.2 -9.5 -9.5 -9.4 -9.4 -9.2 -9.4 -9.6 -9.5 -9.2 -9.4 -9.6 -9.2 -9.5 -9.6 -10.0 -9.6 -9.7 -9.0 -8.7 -8.1 -7.5 -6.7 -6.4 -5.5 -4.2 +4.6 +7.0 +7.4 +7.6 +7.4 +7.6 +7.7 +8.2 +8.2 +8.2 +8.4 +8.5 +8.5 +8.0 +8.5 +8.2 +8.2 +8.2 +7.9 +7.9
layers where the patch alone flips baseline to drive: [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -9.23 (model -9.38), sub +7.93 (model +7.88)
top Δ attention layers: L74 +0.70, L78 +0.59, L76 +0.57, L75 -0.48, L70 +0.45
top Δ MLP layers:       L76 +3.08, L75 +2.48, L79 +2.24, L74 +1.97, L77 -1.50
top Δ heads: L76H56 +0.82, L76H59 -0.64, L76H14 +0.42, L78H60 +0.37, L78H58 +0.35, L78H14 -0.34, L69H26 +0.31, L67H13 +0.26

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.659, max layer L5 (0.944)
- hdr_user: mean 0.002, max layer L0 (0.020)
- line1: mean 0.005, max layer L0 (0.052)
- line2: mean 0.006, max layer L1 (0.046)
- line3: mean 0.006, max layer L0 (0.060)
- line4: mean 0.004, max layer L0 (0.057)
- line5: mean 0.005, max layer L0 (0.102)
- line6: mean 0.005, max layer L0 (0.047)
- question: mean 0.073, max layer L60 (0.283)
- answer_instr: mean 0.028, max layer L47 (0.124)
- asst_header: mean 0.089, max layer L78 (0.410)
- last: mean 0.041, max layer L78 (0.283)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L61H24 mass 0.54 Δ+0.15, L60H57 mass 0.47 Δ+0.06, L60H42 mass 0.79 Δ+0.03, L59H48 mass 0.54 Δ+0.04, L59H55 mass 0.40 Δ+0.05, L65H38 mass 0.45 Δ+0.04

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +6.12 |
| loo_line2 | +6.87 |
| loo_line3 | +7.00 |
| loo_line4 | +7.62 |
| loo_line5 | +5.75 |
| loo_line6 | +3.37 |
| loo_line7 | +11.00 |
| loo_line8 | +8.50 |
| loo_line9 | +8.37 |
| only_line1 | -7.25 |
| only_line2 | -9.62 |
| only_line3 | -6.50 |
| only_line4 | -7.37 |
| only_line5 | -6.37 |
| only_line6 | -6.12 |
| only_line7 | +1.00 |
| only_line8 | +0.75 |
| only_line9 | -6.12 |
| headers_only | -9.62 |

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
| baseline | -9.37 | -9.37 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -9.62 | -9.62 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_correct | -2.62 | -2.62 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_encourage | -9.62 | -9.62 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_expert | -7.75 | -7.75 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -9.37 | -9.37 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -9.12 | -9.12 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -8.75 | -8.75 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_urgency | -5.62 | -5.62 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | +7.87 | +7.87 @0 | 'drive' | 'drive<|im_end|>' |
