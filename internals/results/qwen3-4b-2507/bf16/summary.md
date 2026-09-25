# Qwen3-4B-Instruct-2507 (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 36 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -22.00 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | -5.50 | 0.004 | 0.996 | 'walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +1.4 +4.0 +2.9 +3.5 +2.5 +2.8 -0.0 +0.7 +3.3 +1.0 +1.7 +2.0 +1.7 +3.8 +2.1 +2.0 +3.3 +2.8 +2.5 +0.9 +0.1 -0.0 -0.7 -2.3 -3.7 -3.3 -4.1 -4.4 -4.5 -12.1 -12.1 -15.3 -14.0 -16.6 -15.2 -22.0
substrate: +nan +1.2 +4.2 +3.4 +4.3 +2.7 +3.0 +0.2 +0.7 +3.2 +2.5 +1.7 +2.0 +1.8 +3.5 +1.8 +1.0 +2.4 +1.8 +1.4 -0.0 -1.7 -0.0 -0.7 -1.8 -1.8 -1.4 -2.1 -2.3 -2.7 -3.8 -3.6 -6.1 -1.2 -3.6 -4.2 -5.5
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -22.0 -21.9 -21.7 -21.9 -21.9 -22.1 -21.7 -21.9 -21.9 -21.9 -21.9 -22.1 -22.1 -22.1 -22.1 -22.0 -22.0 -21.7 -20.7 -20.5 -18.6 -15.6 -15.6 -12.7 -9.7 -9.5 -7.7 -7.2 -8.2 -7.5 -7.0 -7.0 -6.7 -6.0 -5.5 -5.5
layers where the patch alone flips baseline to drive: []

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -21.98 (model -22.00), sub -5.47 (model -5.50)
top Δ attention layers: L33 +5.48, L32 +3.15, L35 +2.03, L29 +2.01, L34 +0.96
top Δ MLP layers:       L33 -2.47, L32 +2.07, L35 -1.75, L29 +1.25, L30 +1.05
top Δ heads: L33H11 +4.54, L32H0 +2.18, L32H2 +0.93, L33H30 +0.80, L29H27 +0.76, L35H26 +0.66, L35H23 +0.60, L31H4 +0.54

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.427, max layer L30 (0.801)
- hdr_user: mean 0.005, max layer L1 (0.020)
- line1: mean 0.007, max layer L0 (0.025)
- line2: mean 0.028, max layer L5 (0.162)
- line3: mean 0.022, max layer L4 (0.122)
- line4: mean 0.011, max layer L4 (0.052)
- line5: mean 0.008, max layer L0 (0.039)
- line6: mean 0.005, max layer L0 (0.021)
- question: mean 0.073, max layer L0 (0.148)
- answer_instr: mean 0.051, max layer L17 (0.164)
- asst_header: mean 0.191, max layer L1 (0.428)
- last: mean 0.085, max layer L35 (0.226)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H11 mass 0.05 Δ+4.54, L29H27 mass 0.14 Δ+0.76, L32H0 mass 0.05 Δ+2.18, L23H10 mass 0.34 Δ+0.12, L34H19 mass 0.07 Δ+0.41, L29H12 mass 0.10 Δ+0.24

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -0.25 |
| loo_line2 | -4.50 |
| loo_line3 | -6.25 |
| loo_line4 | -5.00 |
| loo_line5 | -15.00 |
| loo_line6 | -10.75 |
| loo_line7 | -4.25 |
| loo_line8 | -9.25 |
| loo_line9 | -8.00 |
| only_line1 | -27.75 |
| only_line2 | -26.00 |
| only_line3 | -24.25 |
| only_line4 | -27.00 |
| only_line5 | -25.87 |
| only_line6 | -22.37 |
| only_line7 | -9.50 |
| only_line8 | -14.00 |
| only_line9 | -22.12 |
| headers_only | -26.37 |

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
| baseline | -22.00 | -22.00 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -22.11 | -22.11 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_encourage | -24.87 | -24.87 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_expert | -22.50 | -22.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_goaloriented | -18.87 | -18.87 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -22.12 | -22.12 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -23.12 | -23.12 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -22.12 | -22.12 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_urgency | -15.37 | -15.37 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | -5.50 | -5.50 @0 | 'walk' | 'walk<|im_end|>' |
