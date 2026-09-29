# Qwen/Qwen3-8B

substrate file: substrate.txt

quant: bf16 · layers 36 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -13.66 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | +7.50 | 0.999 | 0.001 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +2.6 +5.7 +2.7 +2.1 +0.4 +1.0 -0.7 -2.1 -3.1 -1.8 -2.5 -2.7 -0.0 +2.8 +7.7 +3.0 +0.9 +2.5 +1.4 +4.0 +3.1 +3.8 +4.0 +3.0 -1.8 -3.9 -3.0 -4.3 -6.5 -6.1 -11.9 -17.4 -21.2 -14.2 -15.5 -8.7 -13.7
substrate: +2.6 +5.7 +2.5 +2.3 +1.3 +1.5 +0.2 -1.7 -3.6 -2.7 -3.8 -3.6 -1.1 +3.3 +8.1 +4.1 +0.6 +1.0 -1.4 +1.8 +1.8 +2.8 +4.7 +3.4 -1.7 +0.0 -0.8 -1.3 -2.4 -2.0 -1.7 -1.8 -3.9 +6.6 +8.8 +3.4 +7.2
final lens row == model logits: base True, sub False

## patching (substrate residual into baseline at the answer position)
M per layer: -14.0 -13.8 -13.8 -13.9 -12.7 -13.0 -13.0 -12.5 -12.7 -12.4 -12.9 -12.4 -12.5 -12.9 -13.5 -14.2 -13.2 -13.0 -12.5 -13.0 -12.5 -11.5 -10.2 -1.0 +1.8 +2.2 +5.0 +5.2 +5.0 +5.8 +5.8 +5.5 +5.5 +6.5 +6.5 +7.5
layers where the patch alone flips baseline to drive: [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -14.13 (model -14.00), sub +7.44 (model +7.50)
top Δ attention layers: L33 +11.32, L32 +5.63, L29 +3.15, L31 +2.71, L34 +2.38
top Δ MLP layers:       L34 -10.28, L35 -5.64, L30 +4.82, L32 +1.28, L29 +1.28
top Δ heads: L33H11 +8.62, L32H2 +3.04, L32H0 +2.83, L34H19 +1.52, L33H30 +1.52, L31H15 +1.48, L33H23 +1.46, L31H4 +1.18

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.464, max layer L30 (0.782)
- hdr_user: mean 0.005, max layer L4 (0.021)
- line1: mean 0.008, max layer L4 (0.035)
- line2: mean 0.031, max layer L4 (0.212)
- line3: mean 0.023, max layer L2 (0.147)
- line4: mean 0.007, max layer L2 (0.035)
- line5: mean 0.008, max layer L2 (0.048)
- line6: mean 0.003, max layer L0 (0.017)
- question: mean 0.061, max layer L23 (0.189)
- answer_instr: mean 0.033, max layer L18 (0.134)
- asst_header: mean 0.237, max layer L6 (0.527)
- last: mean 0.095, max layer L6 (0.261)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H11 mass 0.10 Δ+8.62, L32H0 mass 0.05 Δ+2.83, L33H23 mass 0.09 Δ+1.46, L34H19 mass 0.09 Δ+1.52, L29H27 mass 0.10 Δ+0.91, L26H26 mass 0.21 Δ+0.40

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +6.25 |
| loo_line2 | +10.00 |
| loo_line3 | +7.25 |
| loo_line4 | +10.25 |
| loo_line5 | +10.75 |
| loo_line6 | +5.25 |
| loo_line7 | +3.25 |
| loo_line8 | +6.00 |
| loo_line9 | +4.50 |
| only_line1 | -16.75 |
| only_line2 | -14.50 |
| only_line3 | -11.00 |
| only_line4 | -11.50 |
| only_line5 | -10.50 |
| only_line6 | -10.75 |
| only_line7 | -5.50 |
| only_line8 | +2.00 |
| only_line9 | -11.00 |
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
| baseline | -13.66 | -13.66 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -17.97 | -17.97 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_correct | +20.00 | +20.00 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | -15.26 | -15.26 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -11.52 | -11.52 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -16.19 | -16.19 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -15.88 | -15.88 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -13.75 | -13.75 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | -8.47 | -8.47 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | +7.50 | +7.50 @0 | 'drive' | 'drive<|im_end|>' |
