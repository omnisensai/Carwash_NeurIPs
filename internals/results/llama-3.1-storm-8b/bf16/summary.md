# Llama-3.1-Storm-8B (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -6.22 | 0.002 | 0.998 | 'walk<|eot_id|>' |
| substrate | +5.66 | 0.996 | 0.003 | 'drive<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -0.2 +0.5 +2.4 +3.2 +1.6 -0.8 -0.8 +0.2 -0.8 -1.1 -1.1 -0.6 +1.9 +0.7 +1.3 -2.3 -2.5 -0.6 -2.7 -3.7 -3.9 -3.3 -3.9 -7.2 -13.6 -11.2 -13.2 -10.7 -8.7 -10.5 -4.8 -2.9 -6.2
substrate: -0.2 -0.3 +2.0 +1.7 +0.9 -1.1 -0.6 +1.4 +0.1 -0.8 +0.7 -0.7 +2.3 +1.3 +1.4 -0.3 -0.9 +1.0 -0.6 -1.6 -1.9 -0.4 +0.1 -1.0 -7.8 -0.9 +1.5 +1.6 +3.5 +4.3 +4.9 +7.0 +5.7
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -6.2 -6.0 -6.0 -6.0 -6.3 -6.2 -6.0 -6.0 -6.3 -6.5 -6.3 -6.7 -6.2 -5.5 +0.7 +2.1 +2.1 +3.5 +3.7 +4.0 +3.9 +4.1 +5.0 +4.9 +4.8 +4.7 +4.8 +5.0 +5.2 +5.4 +5.5 +5.7
layers where the patch alone flips baseline to drive: [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -6.74 (model -6.75), sub +5.75 (model +5.62)
top Δ attention layers: L25 +3.73, L31 +1.69, L24 +1.66, L27 +1.11, L28 +0.85
top Δ MLP layers:       L31 +3.56, L29 -3.38, L28 +1.89, L25 -0.84, L22 +0.60
top Δ heads: L25H5 +1.92, L25H15 +1.79, L31H1 +1.44, L24H17 +1.43, L27H7 +0.82, L31H21 +0.55, L28H20 +0.53, L26H15 -0.46

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.557, max layer L2 (0.785)
- hdr_user: mean 0.004, max layer L2 (0.016)
- line1: mean 0.005, max layer L0 (0.019)
- line2: mean 0.007, max layer L0 (0.026)
- line3: mean 0.006, max layer L0 (0.033)
- line4: mean 0.003, max layer L0 (0.023)
- line5: mean 0.004, max layer L0 (0.034)
- line6: mean 0.003, max layer L0 (0.017)
- question: mean 0.075, max layer L13 (0.200)
- answer_instr: mean 0.043, max layer L11 (0.158)
- asst_header: mean 0.157, max layer L12 (0.280)
- last: mean 0.058, max layer L31 (0.213)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L25H5 mass 0.05 Δ+1.92, L27H16 mass 0.18 Δ+0.33, L21H14 mass 0.19 Δ+0.22, L24H17 mass 0.02 Δ+1.43, L28H20 mass 0.06 Δ+0.53, L29H8 mass 0.09 Δ+0.35

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +7.55 |
| loo_line2 | +6.15 |
| loo_line3 | +4.41 |
| loo_line4 | +7.66 |
| loo_line5 | +3.89 |
| loo_line6 | +6.27 |
| loo_line7 | +6.90 |
| loo_line8 | +2.55 |
| loo_line9 | +3.52 |
| only_line1 | -6.89 |
| only_line2 | -6.61 |
| only_line3 | -4.51 |
| only_line4 | -5.69 |
| only_line5 | -1.61 |
| only_line6 | -4.82 |
| only_line7 | +0.91 |
| only_line8 | +5.51 |
| only_line9 | -4.33 |
| headers_only | -6.85 |

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
| baseline | -6.22 | -6.22 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_CoT | -7.99 | -7.99 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_encourage | -8.72 | -8.72 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_expert | -4.52 | -4.52 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_goaloriented | -1.23 | -1.23 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_hallucination | -7.56 | -7.56 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_nomistakes | -7.77 | -7.77 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_threat | -9.31 | -9.31 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_urgency | -1.77 | -1.77 @0 | 'Walk' | 'Walk<|eot_id|>' |
| substrate | +5.66 | +5.66 @0 | 'drive' | 'drive<|eot_id|>' |
