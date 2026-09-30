# Qwen/Qwen3-14B

substrate file: substrate.txt

quant: bf16 · layers 40 · heads 40 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -16.25 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | +12.00 | 1.000 | 0.000 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  -1.9 +0.5 +2.5 +2.4 +5.0 +3.4 +1.9 +3.2 +1.8 +1.8 +2.2 +2.3 +3.5 +4.3 +2.3 +3.4 +3.3 +2.5 +3.8 -1.7 -3.7 -2.7 -0.5 +2.2 -2.5 -1.0 -1.6 -4.1 -2.4 -0.3 -2.5 -3.8 -6.3 -7.7 -9.6 -10.9 -17.1 -18.3 -14.4 -12.3 -16.2
substrate: -1.9 +0.8 +2.6 +2.2 +5.3 +3.3 +3.1 +4.1 +2.6 +2.6 +3.2 +2.8 +3.5 +4.4 +2.9 +6.3 +5.8 +4.1 +5.9 -1.5 -2.5 -0.9 +2.6 +5.2 -0.1 +1.0 +4.0 +3.5 +4.7 +8.0 +6.0 +7.3 +8.2 +12.8 +19.3 +16.9 +22.2 +19.5 +16.6 +8.7 +12.0
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -16.7 -16.5 -16.5 -16.5 -16.2 -16.2 -16.2 -16.5 -16.5 -16.5 -16.7 -17.0 -17.0 -16.2 -16.0 -17.0 -16.2 -16.0 -16.0 -15.5 -15.5 -16.0 -16.5 -15.7 -14.0 -9.0 +4.7 +4.7 +6.2 +7.5 +8.5 +8.0 +8.2 +8.0 +8.2 +9.7 +9.7 +10.5 +11.5 +12.0
layers where the patch alone flips baseline to drive: [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -16.22 (model -16.25), sub +12.04 (model +12.00)
top Δ attention layers: L35 +9.34, L36 +3.84, L38 +2.48, L33 +2.21, L32 +2.16
top Δ MLP layers:       L38 -6.77, L39 -6.01, L33 +3.36, L36 +3.27, L32 +1.69
top Δ heads: L35H5 +6.20, L35H12 +2.60, L39H10 +2.50, L33H9 +2.22, L36H29 +2.05, L38H20 -1.45, L39H14 -1.29, L37H16 +1.23

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.440, max layer L9 (0.758)
- hdr_user: mean 0.007, max layer L13 (0.027)
- line1: mean 0.008, max layer L2 (0.035)
- line2: mean 0.019, max layer L5 (0.148)
- line3: mean 0.008, max layer L2 (0.032)
- line4: mean 0.005, max layer L0 (0.021)
- line5: mean 0.006, max layer L0 (0.027)
- line6: mean 0.004, max layer L26 (0.016)
- question: mean 0.084, max layer L24 (0.208)
- answer_instr: mean 0.037, max layer L21 (0.162)
- asst_header: mean 0.256, max layer L1 (0.495)
- last: mean 0.085, max layer L39 (0.196)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L35H5 mass 0.13 Δ+6.20, L30H25 mass 0.40 Δ+0.47, L35H12 mass 0.07 Δ+2.60, L32H9 mass 0.26 Δ+0.47, L37H17 mass 0.18 Δ+0.58, L38H16 mass 0.18 Δ+0.50

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +3.25 |
| loo_line2 | +13.75 |
| loo_line3 | +7.75 |
| loo_line4 | +15.50 |
| loo_line5 | +6.50 |
| loo_line6 | +7.25 |
| loo_line7 | +15.00 |
| loo_line8 | +12.50 |
| loo_line9 | -9.25 |
| only_line1 | -16.75 |
| only_line2 | -18.25 |
| only_line3 | -16.25 |
| only_line4 | -16.50 |
| only_line5 | -15.00 |
| only_line6 | -16.25 |
| only_line7 | -9.75 |
| only_line8 | -11.75 |
| only_line9 | -9.50 |
| headers_only | -18.75 |

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
| baseline | -16.25 | -16.25 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -19.00 | -19.00 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_correct | +14.25 | +14.25 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | -17.00 | -17.00 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_expert | -15.00 | -15.00 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -15.75 | -15.75 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -18.50 | -18.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -14.50 | -14.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_urgency | -16.50 | -16.50 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | +12.00 | +12.00 @0 | 'drive' | 'drive<|im_end|>' |
