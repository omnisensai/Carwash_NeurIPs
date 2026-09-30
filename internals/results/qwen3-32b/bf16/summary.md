# Qwen/Qwen3-32B

substrate file: substrate.txt

quant: bf16 · layers 64 · heads 64 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -8.49 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | +6.86 | 0.999 | 0.001 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  -1.7 +3.8 +5.2 +5.0 +3.9 +3.6 +3.1 +2.5 +1.5 +1.2 +1.3 +1.7 +1.3 +1.7 +1.6 +1.0 +1.9 +2.1 +2.7 +3.3 +2.8 +2.7 +1.5 +2.2 +2.2 +3.5 +4.2 +3.1 +2.4 +3.1 +3.7 +4.4 +3.3 +2.8 +2.7 +3.5 +3.9 +2.7 +1.9 +2.1 +1.8 +2.4 +3.6 +3.6 +2.9 +3.9 +2.7 +3.3 +2.9 +1.5 -1.0 -1.0 -1.3 +0.3 -0.3 -0.8 -2.6 -2.4 -5.8 -8.1 -14.5 -12.8 -11.2 -10.5 -8.2
substrate: -1.7 +3.5 +4.9 +4.8 +3.2 +3.2 +3.0 +2.3 +1.3 +1.2 +1.4 +1.7 +1.4 +1.5 +1.9 +1.5 +1.6 +1.5 +2.7 +3.3 +3.7 +4.3 +3.5 +3.7 +4.6 +3.7 +4.3 +3.6 +2.4 +2.8 +3.0 +3.9 +3.0 +2.5 +1.8 +2.8 +4.2 +2.1 +2.5 +2.0 +2.4 +3.5 +5.1 +4.7 +5.1 +5.0 +3.1 +3.9 +3.2 +2.3 +1.0 +1.5 +1.5 +6.4 +7.3 +8.4 +8.5 +13.4 +16.3 +16.5 +18.4 +19.5 +12.9 +6.8 +6.9
final lens row == model logits: base False, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -8.2 -8.2 -8.2 -8.2 -8.2 -8.0 -8.2 -8.2 -8.2 -8.2 -8.2 -8.5 -8.2 -8.2 -8.2 -8.2 -8.2 -8.2 -8.5 -8.2 -8.2 -8.2 -8.2 -8.2 -8.2 -8.0 -8.0 -8.2 -8.2 -8.2 -8.5 -8.2 -8.2 -8.2 -8.2 -8.5 -8.5 -8.0 -8.2 -8.2 -8.2 -8.5 -8.2 -8.2 -8.0 -8.5 -8.0 -7.2 -6.2 -2.8 -0.5 +1.0 +2.0 +2.5 +4.2 +4.2 +4.2 +4.2 +4.4 +5.2 +5.9 +5.9 +6.6 +6.9
layers where the patch alone flips baseline to drive: [51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -8.29 (model -8.50), sub +7.10 (model +7.00)
top Δ attention layers: L59 +5.24, L63 +2.57, L62 +2.00, L60 +1.77, L56 +1.04
top Δ MLP layers:       L63 -6.26, L62 -2.73, L60 +2.14, L58 +2.07, L57 +1.92
top Δ heads: L59H8 +2.07, L63H19 +1.53, L59H11 +1.41, L59H21 +1.07, L62H35 -0.83, L63H23 -0.69, L56H12 +0.65, L62H28 +0.64

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.552, max layer L7 (0.864)
- hdr_user: mean 0.006, max layer L26 (0.025)
- line1: mean 0.008, max layer L6 (0.035)
- line2: mean 0.018, max layer L5 (0.197)
- line3: mean 0.007, max layer L0 (0.036)
- line4: mean 0.004, max layer L0 (0.026)
- line5: mean 0.006, max layer L1 (0.034)
- line6: mean 0.004, max layer L1 (0.013)
- question: mean 0.065, max layer L0 (0.187)
- answer_instr: mean 0.043, max layer L21 (0.141)
- asst_header: mean 0.172, max layer L1 (0.401)
- last: mean 0.063, max layer L63 (0.223)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L59H8 mass 0.23 Δ+2.07, L59H11 mass 0.12 Δ+1.41, L55H7 mass 0.33 Δ+0.25, L61H24 mass 0.13 Δ+0.59, L62H28 mass 0.11 Δ+0.64, L54H43 mass 0.68 Δ+0.08

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +4.88 |
| loo_line2 | +7.09 |
| loo_line3 | +1.97 |
| loo_line4 | +7.12 |
| loo_line5 | +7.11 |
| loo_line6 | +7.59 |
| loo_line7 | +9.30 |
| loo_line8 | +6.09 |
| loo_line9 | +2.21 |
| only_line1 | -7.73 |
| only_line2 | -7.23 |
| only_line3 | -5.76 |
| only_line4 | -7.23 |
| only_line5 | -5.03 |
| only_line6 | -5.51 |
| only_line7 | -3.80 |
| only_line8 | +1.44 |
| only_line9 | -2.78 |
| headers_only | -7.72 |

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
| baseline | -8.49 | -8.49 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -10.32 | -10.32 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_correct | +7.99 | +7.99 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | -6.74 | -6.74 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_expert | -3.50 | -3.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -8.24 | -8.24 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -6.99 | -6.99 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -3.50 | -3.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_urgency | -3.00 | -3.00 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | +6.86 | +6.86 @0 | 'drive' | 'drive<|im_end|>' |
