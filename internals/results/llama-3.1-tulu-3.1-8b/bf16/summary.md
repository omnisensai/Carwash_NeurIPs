# Llama-3.1-Tulu-3.1-8B (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -2.00 | 0.116 | 0.860 | 'walk<|end_of_text|>' |
| substrate | +2.62 | 0.922 | 0.067 | 'drive<|end_of_text|>' |

## logit lens (M per layer, emb first)
baseline:  -2.4 +2.7 +5.1 +4.2 +0.2 -3.3 -2.5 -2.0 -0.5 -1.0 -0.4 -1.1 +0.2 +1.1 +0.7 -2.9 -2.5 -1.2 -2.5 -3.1 -3.4 -2.8 -2.2 -4.9 -11.9 -7.8 -7.6 -7.0 -6.1 -7.1 -2.2 -0.9 -2.0
substrate: -2.4 +2.2 +4.6 +4.0 -0.2 -3.5 -1.2 -1.1 +0.4 -0.4 -0.1 -0.7 +0.7 +1.8 +2.0 -2.2 -0.6 +0.1 -0.3 -1.2 -1.5 -0.5 +2.0 +1.4 -4.8 +0.3 +1.1 +0.6 +1.6 +1.3 +3.2 +4.7 +2.6
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -2.0 -2.1 -2.1 -2.0 -2.1 -2.1 -2.1 -2.4 -2.4 -2.4 -2.2 -2.4 -2.0 -1.9 -0.7 +0.6 +0.7 +1.4 +1.5 +1.5 +1.5 +1.9 +1.9 +1.9 +1.9 +2.0 +1.9 +2.1 +2.4 +2.4 +2.7 +2.6
layers where the patch alone flips baseline to drive: [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -2.05 (model -2.00), sub +2.62 (model +2.62)
top Δ attention layers: L28 +0.80, L27 +0.68, L30 +0.53, L25 +0.45, L23 +0.43
top Δ MLP layers:       L29 -1.68, L31 +0.73, L22 +0.53, L30 +0.33, L27 -0.30
top Δ heads: L28H20 +0.55, L25H5 +0.55, L31H1 +0.51, L23H22 +0.44, L27H16 +0.43, L30H24 +0.28, L27H7 +0.27, L29H31 +0.22

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.521, max layer L3 (0.823)
- hdr_user: mean 0.003, max layer L9 (0.010)
- line1: mean 0.005, max layer L0 (0.019)
- line2: mean 0.006, max layer L0 (0.033)
- line3: mean 0.005, max layer L0 (0.033)
- line4: mean 0.003, max layer L0 (0.024)
- line5: mean 0.004, max layer L0 (0.036)
- line6: mean 0.003, max layer L0 (0.018)
- question: mean 0.069, max layer L0 (0.213)
- answer_instr: mean 0.051, max layer L11 (0.168)
- asst_header: mean 0.158, max layer L31 (0.301)
- last: mean 0.055, max layer L31 (0.219)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L27H16 mass 0.14 Δ+0.43, L21H14 mass 0.28 Δ+0.20, L23H22 mass 0.13 Δ+0.44, L25H5 mass 0.05 Δ+0.55, L30H26 mass 0.12 Δ+0.21, L22H8 mass 0.20 Δ+0.13

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +2.87 |
| loo_line2 | +3.00 |
| loo_line3 | +2.50 |
| loo_line4 | +3.12 |
| loo_line5 | +2.25 |
| loo_line6 | +2.87 |
| loo_line7 | +2.62 |
| loo_line8 | +2.25 |
| loo_line9 | +0.75 |
| only_line1 | -1.25 |
| only_line2 | -1.12 |
| only_line3 | -0.87 |
| only_line4 | -1.00 |
| only_line5 | +0.00 |
| only_line6 | -0.87 |
| only_line7 | +0.87 |
| only_line8 | +2.62 |
| only_line9 | +1.50 |
| headers_only | -1.00 |

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
| baseline | -2.00 | -2.00 @0 | 'walk' | 'walk<|end_of_text|>' |
| benchmark_CoT | -2.00 | -2.00 @0 | 'walk' | 'walk<|end_of_text|>' |
| benchmark_encourage | -2.37 | -2.37 @0 | 'walk' | 'walk<|end_of_text|>' |
| benchmark_expert | -2.12 | -2.12 @0 | 'walk' | 'walk<|end_of_text|>' |
| benchmark_goaloriented | -1.37 | -1.37 @0 | 'walk' | 'walk<|end_of_text|>' |
| benchmark_hallucination | -2.00 | -2.00 @0 | 'walk' | 'walk<|end_of_text|>' |
| benchmark_nomistakes | -1.50 | -1.50 @0 | 'walk' | 'walk<|end_of_text|>' |
| benchmark_threat | -2.75 | -2.75 @0 | 'walk' | 'walk<|end_of_text|>' |
| benchmark_urgency | -1.12 | -1.12 @0 | 'walk' | 'walk<|end_of_text|>' |
| substrate | +2.62 | +2.62 @0 | 'drive' | 'drive<|end_of_text|>' |
