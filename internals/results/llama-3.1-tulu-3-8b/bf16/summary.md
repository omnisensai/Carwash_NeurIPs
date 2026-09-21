# Llama-3.1-Tulu-3-8B (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -4.79 | 0.008 | 0.991 | 'Walk<|end_of_text|>' |
| substrate | +0.89 | 0.707 | 0.291 | 'drive<|end_of_text|>' |

## logit lens (M per layer, emb first)
baseline:  -2.4 +2.5 +5.1 +4.6 +0.5 -3.4 -2.9 -2.1 -1.4 -0.0 -0.7 -2.3 -1.6 -1.2 -2.0 -4.7 -4.7 -2.3 -4.2 -5.0 -4.9 -4.5 -3.1 -6.5 -13.5 -10.0 -10.6 -9.8 -8.0 -11.2 -4.2 -2.9 -4.8
substrate: -2.4 +2.0 +4.6 +4.3 +0.1 -3.7 -1.5 -1.0 -0.3 -0.1 -1.2 -3.2 -1.7 -0.2 -0.6 -3.8 -3.1 -1.2 -2.2 -3.4 -3.0 -2.0 +1.4 +1.0 -6.5 -1.4 -1.5 -2.0 -0.7 -3.6 +0.5 +2.0 +0.9
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -4.8 -4.8 -4.8 -4.8 -4.8 -4.9 -4.9 -5.0 -5.0 -4.9 -4.5 -4.7 -4.6 -4.0 -2.1 -0.5 -0.3 +0.4 +0.2 +0.4 +0.6 +0.8 +0.9 +0.9 +0.8 +0.8 +0.7 +0.9 +1.0 +0.9 +1.0 +0.9
layers where the patch alone flips baseline to drive: [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -4.25 (model -4.25), sub +1.01 (model +1.00)
top Δ attention layers: L25 +0.85, L28 +0.58, L27 +0.50, L31 +0.31, L30 +0.27
top Δ MLP layers:       L29 -1.70, L31 +1.39, L22 +0.77, L30 +0.64, L27 -0.50
top Δ heads: L25H5 +0.68, L31H1 +0.57, L28H20 +0.46, L27H16 +0.36, L23H22 +0.33, L25H15 +0.25, L21H14 +0.20, L27H7 +0.18

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.535, max layer L2 (0.806)
- hdr_user: mean 0.003, max layer L9 (0.011)
- line1: mean 0.005, max layer L0 (0.019)
- line2: mean 0.006, max layer L0 (0.033)
- line3: mean 0.006, max layer L0 (0.033)
- line4: mean 0.003, max layer L0 (0.024)
- line5: mean 0.004, max layer L0 (0.036)
- line6: mean 0.003, max layer L0 (0.018)
- question: mean 0.073, max layer L0 (0.210)
- answer_instr: mean 0.041, max layer L8 (0.125)
- asst_header: mean 0.157, max layer L31 (0.291)
- last: mean 0.057, max layer L31 (0.220)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L27H16 mass 0.15 Δ+0.36, L23H22 mass 0.14 Δ+0.33, L21H14 mass 0.21 Δ+0.20, L15H11 mass 0.27 Δ+0.15, L25H5 mass 0.06 Δ+0.68, L22H8 mass 0.22 Δ+0.16

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +1.45 |
| loo_line2 | +1.35 |
| loo_line3 | +0.29 |
| loo_line4 | +1.75 |
| loo_line5 | +0.04 |
| loo_line6 | +1.25 |
| loo_line7 | +1.13 |
| loo_line8 | +0.03 |
| loo_line9 | -1.80 |
| only_line1 | -3.33 |
| only_line2 | -3.92 |
| only_line3 | -3.22 |
| only_line4 | -4.02 |
| only_line5 | -2.90 |
| only_line6 | -3.56 |
| only_line7 | -1.01 |
| only_line8 | +1.28 |
| only_line9 | -1.81 |
| headers_only | -4.36 |

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
| baseline | -4.79 | -4.79 @0 | 'Walk' | 'Walk<|end_of_text|>' |
| benchmark_CoT | -4.71 | -4.71 @0 | 'Walk' | 'Walk<|end_of_text|>' |
| benchmark_encourage | -6.28 | -6.28 @0 | 'Walk' | 'Walk<|end_of_text|>' |
| benchmark_expert | -5.66 | -5.66 @0 | 'Walk' | 'Walk<|end_of_text|>' |
| benchmark_goaloriented | -4.42 | -4.42 @0 | 'Walk' | 'Walk<|end_of_text|>' |
| benchmark_hallucination | -4.89 | -4.89 @0 | 'Walk' | 'Walk<|end_of_text|>' |
| benchmark_nomistakes | -4.80 | -4.80 @0 | 'Walk' | 'Walk<|end_of_text|>' |
| benchmark_threat | -5.50 | -5.50 @0 | 'Walk' | 'Walk<|end_of_text|>' |
| benchmark_urgency | -4.74 | -4.74 @0 | 'Walk' | 'Walk<|end_of_text|>' |
| substrate | +0.89 | +0.89 @0 | 'drive' | 'drive<|end_of_text|>' |
