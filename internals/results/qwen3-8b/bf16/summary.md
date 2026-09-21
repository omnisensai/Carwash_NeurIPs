# Qwen3-8B (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 36 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -14.07 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | +7.25 | 0.999 | 0.001 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +2.6 +5.6 +2.7 +2.1 +0.4 +1.0 -0.7 -2.1 -3.1 -1.8 -2.5 -2.6 +0.0 +2.8 +7.9 +3.1 +1.0 +2.7 +1.5 +4.0 +3.1 +3.9 +4.0 +3.1 -1.8 -3.9 -3.1 -4.3 -6.5 -6.0 -11.8 -17.2 -21.0 -14.1 -15.4 -8.7 -14.1
substrate: +2.6 +5.7 +2.5 +2.4 +1.4 +1.6 +0.3 -1.7 -3.6 -2.8 -3.8 -3.7 -1.1 +3.2 +8.0 +4.0 +0.5 +1.0 -1.5 +1.9 +1.8 +2.7 +4.6 +3.3 -1.9 -0.2 -1.1 -1.2 -2.3 -1.9 -1.6 -1.7 -3.9 +6.4 +8.5 +3.4 +7.0
final lens row == model logits: base True, sub False

## patching (substrate residual into baseline at the answer position)
M per layer: -14.7 -13.8 -14.3 -13.7 -13.2 -13.2 -13.5 -12.7 -13.0 -12.9 -13.1 -12.9 -12.7 -12.9 -13.2 -14.5 -13.7 -13.2 -13.2 -13.5 -13.0 -11.7 -11.2 -1.7 +1.3 +2.2 +5.0 +5.0 +4.8 +5.5 +5.5 +5.2 +5.5 +6.2 +6.5 +7.2
layers where the patch alone flips baseline to drive: [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -14.42 (model -14.50), sub +7.21 (model +7.25)
top Δ attention layers: L33 +11.36, L32 +5.63, L29 +3.13, L31 +2.62, L34 +2.33
top Δ MLP layers:       L34 -10.08, L35 -5.66, L30 +4.83, L29 +1.29, L32 +1.23
top Δ heads: L33H11 +8.56, L32H2 +3.33, L32H0 +2.53, L33H23 +1.56, L34H19 +1.51, L33H30 +1.48, L31H15 +1.37, L31H4 +1.22

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.465, max layer L30 (0.785)
- hdr_user: mean 0.005, max layer L4 (0.021)
- line1: mean 0.008, max layer L4 (0.035)
- line2: mean 0.031, max layer L4 (0.213)
- line3: mean 0.023, max layer L2 (0.146)
- line4: mean 0.007, max layer L2 (0.035)
- line5: mean 0.008, max layer L2 (0.048)
- line6: mean 0.003, max layer L0 (0.017)
- question: mean 0.060, max layer L23 (0.188)
- answer_instr: mean 0.033, max layer L18 (0.136)
- asst_header: mean 0.237, max layer L6 (0.526)
- last: mean 0.095, max layer L6 (0.258)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H11 mass 0.10 Δ+8.56, L33H23 mass 0.09 Δ+1.56, L34H19 mass 0.08 Δ+1.51, L32H0 mass 0.05 Δ+2.53, L26H26 mass 0.22 Δ+0.41, L29H27 mass 0.09 Δ+0.93

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +4.75 |
| loo_line2 | +10.25 |
| loo_line3 | +7.25 |
| loo_line4 | +10.75 |
| loo_line5 | +9.00 |
| loo_line6 | +4.75 |
| loo_line7 | +3.75 |
| loo_line8 | +6.75 |
| loo_line9 | +3.75 |
| only_line1 | -16.75 |
| only_line2 | -14.25 |
| only_line3 | -11.50 |
| only_line4 | -12.00 |
| only_line5 | -10.00 |
| only_line6 | -10.75 |
| only_line7 | -6.25 |
| only_line8 | +2.50 |
| only_line9 | -11.25 |
| headers_only | -13.50 |

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
| baseline | -14.07 | -14.07 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -17.72 | -17.72 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_encourage | -15.26 | -15.26 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -11.64 | -11.64 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_goaloriented | -12.16 | -12.16 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -16.63 | -16.63 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -15.78 | -15.78 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -14.50 | -14.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | -8.18 | -8.18 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | +7.25 | +7.25 @0 | 'drive' | 'drive<|im_end|>' |
