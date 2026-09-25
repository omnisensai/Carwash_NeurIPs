# Qwen3-8B (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 36 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -14.06 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | +7.25 | 0.999 | 0.001 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +2.6 +5.7 +2.7 +2.1 +0.4 +1.0 -0.8 -2.1 -3.0 -1.8 -2.5 -2.7 -0.0 +2.8 +7.8 +3.0 +1.0 +2.7 +1.6 +4.0 +3.1 +3.9 +4.0 +3.1 -1.7 -3.8 -2.9 -4.1 -6.3 -5.9 -11.9 -17.2 -21.1 -14.1 -15.3 -8.6 -14.1
substrate: +2.6 +5.7 +2.5 +2.3 +1.3 +1.5 +0.3 -1.7 -3.6 -2.8 -3.8 -3.7 -1.1 +3.1 +8.0 +4.1 +0.7 +1.0 -1.3 +2.1 +1.9 +2.8 +4.6 +3.3 -1.7 -0.1 -0.8 -1.1 -2.1 -1.7 -1.1 -1.0 -3.7 +6.4 +8.4 +3.3 +7.2
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -13.9 -13.5 -14.2 -13.7 -13.0 -13.0 -13.0 -12.5 -13.0 -12.7 -12.5 -12.4 -12.4 -12.9 -13.0 -14.2 -13.2 -13.0 -13.0 -13.5 -13.2 -12.0 -11.2 -1.5 +1.5 +2.2 +4.8 +5.2 +5.0 +5.8 +5.8 +5.2 +5.5 +6.2 +6.8 +7.2
layers where the patch alone flips baseline to drive: [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -14.13 (model -14.25), sub +7.34 (model +7.25)
top Δ attention layers: L33 +11.01, L32 +5.48, L29 +3.21, L31 +2.60, L34 +2.23
top Δ MLP layers:       L34 -9.79, L35 -5.57, L30 +4.93, L29 +1.43, L32 +1.11
top Δ heads: L33H11 +8.24, L32H2 +3.01, L32H0 +2.71, L33H23 +1.50, L33H30 +1.48, L34H19 +1.39, L31H15 +1.36, L31H4 +1.20

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.465, max layer L30 (0.785)
- hdr_user: mean 0.005, max layer L4 (0.021)
- line1: mean 0.008, max layer L4 (0.035)
- line2: mean 0.032, max layer L4 (0.214)
- line3: mean 0.022, max layer L2 (0.146)
- line4: mean 0.007, max layer L2 (0.035)
- line5: mean 0.008, max layer L2 (0.048)
- line6: mean 0.003, max layer L0 (0.017)
- question: mean 0.060, max layer L24 (0.187)
- answer_instr: mean 0.033, max layer L18 (0.136)
- asst_header: mean 0.237, max layer L6 (0.527)
- last: mean 0.095, max layer L6 (0.259)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H11 mass 0.10 Δ+8.24, L33H23 mass 0.09 Δ+1.50, L32H0 mass 0.05 Δ+2.71, L34H19 mass 0.08 Δ+1.39, L26H26 mass 0.22 Δ+0.41, L29H27 mass 0.09 Δ+0.95

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +6.50 |
| loo_line2 | +10.00 |
| loo_line3 | +7.25 |
| loo_line4 | +10.25 |
| loo_line5 | +10.25 |
| loo_line6 | +5.25 |
| loo_line7 | +5.25 |
| loo_line8 | +7.50 |
| loo_line9 | +4.50 |
| only_line1 | -16.50 |
| only_line2 | -14.25 |
| only_line3 | -11.50 |
| only_line4 | -12.25 |
| only_line5 | -11.00 |
| only_line6 | -11.25 |
| only_line7 | -6.00 |
| only_line8 | +1.25 |
| only_line9 | -10.50 |
| headers_only | -13.75 |

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
| baseline | -14.06 | -14.06 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -17.95 | -17.95 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_encourage | -14.78 | -14.78 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -11.39 | -11.39 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_goaloriented | -12.14 | -12.14 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -16.10 | -16.10 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -16.13 | -16.13 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -14.00 | -14.00 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | -8.44 | -8.44 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | +7.25 | +7.25 @0 | 'drive' | 'drive<|im_end|>' |
