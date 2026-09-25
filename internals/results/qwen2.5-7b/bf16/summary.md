# Qwen2.5-7B-Instruct (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 28 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -10.50 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | -1.50 | 0.183 | 0.817 | 'walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  -1.6 +1.7 +2.1 +1.9 +2.7 +2.4 +0.8 +0.8 +1.8 -0.1 +3.2 +1.1 +1.4 +1.6 -0.5 +1.4 +1.1 +0.3 +0.3 +0.8 -2.2 -1.0 -2.0 -3.2 -10.2 -16.6 -9.6 -9.2 -10.5
substrate: -1.6 +1.3 +2.2 +2.2 +3.3 +1.6 +1.0 +0.9 +1.8 +0.7 +3.0 +0.0 +0.6 +1.7 -0.8 +1.1 +0.4 +0.2 -0.0 +0.4 -1.4 -1.0 -2.1 -0.8 -3.0 -5.8 -1.5 +0.4 -1.5
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -10.6 -10.5 -10.4 -10.4 -10.6 -9.7 -9.7 -10.2 -9.7 -10.0 -10.0 -10.1 -9.7 -10.1 -10.4 -9.4 -10.5 -11.6 -9.0 -6.0 -3.2 -3.1 -2.6 -2.6 -1.9 -2.2 -1.9 -1.5
layers where the patch alone flips baseline to drive: []

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -10.59 (model -10.50), sub -1.52 (model -1.50)
top Δ attention layers: L26 +2.65, L27 +1.01, L23 +0.90, L24 +0.63, L22 +0.56
top Δ MLP layers:       L24 +2.36, L23 +1.15, L27 +0.54, L25 -0.49, L26 -0.24
top Δ heads: L26H6 +1.76, L26H14 +0.74, L27H24 +0.67, L25H12 +0.65, L24H27 +0.46, L26H26 +0.41, L27H19 +0.39, L26H2 +0.33

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.000, max layer L3 (0.001)
- hdr_user: mean 0.007, max layer L2 (0.040)
- line1: mean 0.008, max layer L2 (0.064)
- line2: mean 0.013, max layer L2 (0.059)
- line3: mean 0.009, max layer L0 (0.043)
- line4: mean 0.005, max layer L0 (0.027)
- line5: mean 0.006, max layer L0 (0.044)
- line6: mean 0.005, max layer L0 (0.019)
- question: mean 0.129, max layer L21 (0.299)
- answer_instr: mean 0.058, max layer L9 (0.211)
- asst_header: mean 0.233, max layer L1 (0.489)
- last: mean 0.103, max layer L27 (0.252)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L26H6 mass 0.04 Δ+1.76, L23H0 mass 0.10 Δ+0.17, L21H3 mass 0.25 Δ+0.07, L19H21 mass 0.29 Δ+0.04, L27H24 mass 0.02 Δ+0.67, L19H22 mass 0.28 Δ+0.04

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -2.62 |
| loo_line2 | -2.62 |
| loo_line3 | -3.12 |
| loo_line4 | -2.37 |
| loo_line5 | -4.25 |
| loo_line6 | -1.00 |
| loo_line7 | -5.50 |
| loo_line8 | -3.50 |
| loo_line9 | -3.00 |
| only_line1 | -10.87 |
| only_line2 | -12.25 |
| only_line3 | -12.37 |
| only_line4 | -12.12 |
| only_line5 | -10.74 |
| only_line6 | -13.62 |
| only_line7 | -8.75 |
| only_line8 | -8.50 |
| only_line9 | -7.75 |
| headers_only | -12.12 |

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
| baseline | -10.50 | -10.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -11.74 | -11.74 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_encourage | -9.37 | -9.37 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_expert | -10.25 | -10.25 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_goaloriented | -10.50 | -10.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -9.50 | -9.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -10.50 | -10.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -10.62 | -10.62 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_urgency | -9.62 | -9.62 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | -1.50 | -1.50 @0 | 'walk' | 'walk<|im_end|>' |
