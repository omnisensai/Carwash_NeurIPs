# Qwen/Qwen2.5-7B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 28 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -10.50 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | -1.87 | 0.133 | 0.867 | 'walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  -1.6 +1.7 +2.1 +2.0 +2.7 +2.4 +0.8 +0.9 +1.8 -0.1 +3.2 +1.1 +1.4 +1.5 -0.5 +1.4 +1.1 +0.4 +0.3 +0.8 -2.1 -1.1 -2.0 -3.1 -10.1 -16.5 -9.3 -9.2 -10.5
substrate: -1.6 +1.3 +2.2 +2.2 +3.3 +1.6 +1.0 +0.9 +1.9 +0.7 +3.0 +0.1 +0.6 +1.6 -0.9 +1.1 +0.4 +0.2 -0.0 +0.5 -1.3 -0.9 -2.0 -1.0 -3.4 -6.3 -1.9 -0.1 -1.9
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -10.5 -10.9 -10.7 -10.4 -10.2 -10.4 -10.4 -10.0 -10.4 -10.0 -10.2 -9.1 -10.1 -10.5 -9.5 -10.2 -9.7 -11.5 -9.6 -6.5 -3.5 -3.7 -3.1 -2.9 -2.1 -2.6 -2.1 -1.9
layers where the patch alone flips baseline to drive: []

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -10.45 (model -10.50), sub -1.80 (model -1.88)
top Δ attention layers: L26 +2.50, L27 +0.92, L23 +0.84, L24 +0.62, L22 +0.51
top Δ MLP layers:       L24 +2.44, L23 +1.11, L25 -0.61, L27 +0.50, L26 -0.19
top Δ heads: L26H6 +1.67, L26H14 +0.72, L25H12 +0.63, L27H24 +0.61, L27H19 +0.44, L24H27 +0.44, L26H26 +0.40, L26H2 +0.30

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.000, max layer L3 (0.001)
- hdr_user: mean 0.007, max layer L2 (0.040)
- line1: mean 0.008, max layer L2 (0.064)
- line2: mean 0.013, max layer L2 (0.059)
- line3: mean 0.009, max layer L0 (0.043)
- line4: mean 0.005, max layer L0 (0.027)
- line5: mean 0.006, max layer L0 (0.044)
- line6: mean 0.005, max layer L0 (0.019)
- question: mean 0.129, max layer L21 (0.297)
- answer_instr: mean 0.058, max layer L9 (0.209)
- asst_header: mean 0.234, max layer L1 (0.489)
- last: mean 0.102, max layer L27 (0.265)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L26H6 mass 0.04 Δ+1.67, L21H3 mass 0.25 Δ+0.07, L23H0 mass 0.09 Δ+0.15, L19H21 mass 0.29 Δ+0.05, L19H22 mass 0.26 Δ+0.04, L27H24 mass 0.02 Δ+0.61

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -2.12 |
| loo_line2 | -1.87 |
| loo_line3 | -2.25 |
| loo_line4 | -1.62 |
| loo_line5 | -2.75 |
| loo_line6 | -0.75 |
| loo_line7 | -4.50 |
| loo_line8 | -3.62 |
| loo_line9 | -3.00 |
| only_line1 | -10.99 |
| only_line2 | -12.24 |
| only_line3 | -11.60 |
| only_line4 | -12.11 |
| only_line5 | -11.86 |
| only_line6 | -13.24 |
| only_line7 | -8.87 |
| only_line8 | -7.37 |
| only_line9 | -7.87 |
| headers_only | -11.36 |

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
| benchmark_CoT | -12.49 | -12.49 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_correct | +6.38 | +6.38 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | -9.87 | -9.87 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_expert | -11.87 | -11.87 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -11.25 | -11.25 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -10.50 | -10.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -12.12 | -12.12 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_urgency | -10.75 | -10.75 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | -1.87 | -1.87 @0 | 'walk' | 'walk<|im_end|>' |
