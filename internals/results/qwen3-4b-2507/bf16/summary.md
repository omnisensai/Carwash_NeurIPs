# Qwen/Qwen3-4B-Instruct-2507

substrate file: substrate.txt

quant: bf16 · layers 36 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -21.75 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | -5.75 | 0.003 | 0.997 | 'walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +1.4 +4.0 +2.9 +3.5 +2.5 +2.7 -0.1 +0.6 +3.3 +1.0 +1.7 +2.0 +1.7 +3.8 +2.2 +2.0 +3.3 +2.7 +2.5 +0.8 +0.1 -0.0 -0.6 -2.2 -3.7 -3.3 -4.0 -4.3 -4.4 -11.9 -11.8 -15.2 -13.9 -16.6 -15.2 -21.7
substrate: +nan +1.2 +4.2 +3.4 +4.3 +2.7 +2.9 +0.1 +0.7 +3.3 +2.5 +1.7 +2.0 +1.8 +3.5 +1.8 +1.0 +2.3 +1.7 +1.3 -0.0 -1.7 -0.0 -0.6 -1.7 -1.8 -1.3 -2.1 -2.3 -2.7 -3.9 -3.7 -6.2 -1.3 -3.7 -4.3 -5.7
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -22.2 -22.2 -22.0 -21.9 -22.1 -22.0 -22.1 -22.1 -22.0 -22.2 -22.5 -22.4 -22.4 -22.0 -21.9 -22.6 -22.2 -21.7 -21.2 -20.5 -19.0 -16.5 -15.9 -13.6 -10.9 -10.2 -8.5 -8.0 -9.0 -8.2 -7.7 -7.7 -7.0 -6.5 -5.7 -5.7
layers where the patch alone flips baseline to drive: []

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -21.63 (model -21.75), sub -5.86 (model -5.75)
top Δ attention layers: L33 +5.56, L32 +3.17, L29 +1.99, L35 +1.97, L31 +0.99
top Δ MLP layers:       L33 -2.47, L35 -2.26, L32 +1.95, L29 +1.11, L30 +0.97
top Δ heads: L33H11 +4.57, L32H0 +2.14, L32H2 +0.96, L33H30 +0.77, L29H27 +0.77, L35H23 +0.58, L35H26 +0.53, L31H4 +0.49

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.427, max layer L30 (0.803)
- hdr_user: mean 0.005, max layer L1 (0.020)
- line1: mean 0.006, max layer L0 (0.025)
- line2: mean 0.028, max layer L5 (0.159)
- line3: mean 0.022, max layer L4 (0.125)
- line4: mean 0.012, max layer L4 (0.055)
- line5: mean 0.008, max layer L0 (0.039)
- line6: mean 0.005, max layer L0 (0.021)
- question: mean 0.073, max layer L0 (0.149)
- answer_instr: mean 0.051, max layer L17 (0.165)
- asst_header: mean 0.191, max layer L1 (0.428)
- last: mean 0.086, max layer L35 (0.226)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H11 mass 0.05 Δ+4.57, L29H27 mass 0.15 Δ+0.77, L32H0 mass 0.05 Δ+2.14, L23H10 mass 0.34 Δ+0.13, L34H19 mass 0.07 Δ+0.40, L29H6 mass 0.06 Δ+0.36

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +0.25 |
| loo_line2 | -2.75 |
| loo_line3 | -7.00 |
| loo_line4 | -4.50 |
| loo_line5 | -14.50 |
| loo_line6 | -11.50 |
| loo_line7 | -4.50 |
| loo_line8 | -8.50 |
| loo_line9 | -8.75 |
| only_line1 | -27.75 |
| only_line2 | -25.62 |
| only_line3 | -24.62 |
| only_line4 | -26.62 |
| only_line5 | -25.75 |
| only_line6 | -22.37 |
| only_line7 | -10.25 |
| only_line8 | -15.25 |
| only_line9 | -21.62 |
| headers_only | -25.62 |

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
| baseline | -21.75 | -21.75 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -22.49 | -22.49 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_correct | +26.12 | +26.12 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | -24.50 | -24.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_expert | -22.37 | -22.37 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -21.87 | -21.87 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -23.87 | -23.87 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -22.50 | -22.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_urgency | -14.37 | -14.37 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | -5.75 | -5.75 @0 | 'walk' | 'walk<|im_end|>' |
