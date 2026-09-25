# Hermes-3-Llama-3.1-8B (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -5.05 | 0.006 | 0.993 | 'walk<|im_end|>' |
| substrate | +3.00 | 0.947 | 0.047 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  -0.3 +1.0 -0.4 +3.7 +2.1 -0.7 -1.7 -0.4 +0.4 +1.5 +0.5 +0.9 +0.2 -2.5 +0.5 -2.9 -3.7 -3.2 -4.3 -6.2 -6.2 -5.1 -4.7 -6.8 -12.5 -10.1 -9.9 -8.5 -7.9 -10.2 -4.9 -3.7 -5.1
substrate: -0.3 +0.0 -1.1 +2.5 +0.9 -0.4 +0.2 +0.1 +1.0 +0.3 +0.4 +0.1 -1.7 -2.2 -0.5 -2.1 -0.8 +1.3 +0.3 -0.7 -1.2 +0.6 +1.6 +1.9 -4.5 +1.8 +4.3 +3.4 +3.2 +3.2 +3.9 +4.5 +3.0
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -5.0 -5.1 -5.0 -5.1 -4.8 -5.1 -4.8 -5.1 -5.1 -5.6 -5.8 -5.6 -5.3 -5.0 +1.4 +2.0 +2.2 +2.9 +2.9 +3.0 +3.0 +3.0 +3.1 +2.9 +2.7 +2.5 +2.6 +2.6 +2.6 +3.0 +3.0 +3.0
layers where the patch alone flips baseline to drive: [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -5.05 (model -5.12), sub +2.97 (model +3.00)
top Δ attention layers: L25 +2.47, L24 +1.52, L27 +0.61, L28 +0.45, L31 +0.41
top Δ MLP layers:       L29 -2.65, L28 +1.74, L31 +1.41, L30 +1.12, L25 -0.82
top Δ heads: L25H5 +1.63, L24H17 +1.29, L25H15 +0.95, L31H1 +0.88, L27H7 +0.53, L28H20 +0.47, L27H16 +0.36, L24H22 +0.35

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.548, max layer L3 (0.861)
- hdr_user: mean 0.004, max layer L9 (0.013)
- line1: mean 0.004, max layer L0 (0.017)
- line2: mean 0.007, max layer L0 (0.030)
- line3: mean 0.005, max layer L0 (0.029)
- line4: mean 0.003, max layer L0 (0.022)
- line5: mean 0.006, max layer L0 (0.031)
- line6: mean 0.003, max layer L0 (0.016)
- question: mean 0.073, max layer L13 (0.217)
- answer_instr: mean 0.045, max layer L9 (0.168)
- asst_header: mean 0.153, max layer L31 (0.298)
- last: mean 0.063, max layer L31 (0.216)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L14H5 mass 0.38 Δ+0.19, L25H5 mass 0.04 Δ+1.63, L15H11 mass 0.33 Δ+0.12, L21H14 mass 0.12 Δ+0.25, L24H17 mass 0.02 Δ+1.29, L27H16 mass 0.07 Δ+0.36

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +4.25 |
| loo_line2 | +3.49 |
| loo_line3 | +2.75 |
| loo_line4 | +4.00 |
| loo_line5 | +3.37 |
| loo_line6 | +3.87 |
| loo_line7 | +3.25 |
| loo_line8 | +3.00 |
| loo_line9 | +1.00 |
| only_line1 | -1.87 |
| only_line2 | -2.74 |
| only_line3 | +0.62 |
| only_line4 | -1.87 |
| only_line5 | +0.75 |
| only_line6 | +0.00 |
| only_line7 | +2.74 |
| only_line8 | +3.24 |
| only_line9 | +1.12 |
| headers_only | -4.23 |

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
| baseline | -5.05 | -5.05 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -4.36 | -4.36 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_encourage | -5.06 | -5.06 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_expert | -4.25 | -4.25 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_goaloriented | -2.94 | -2.94 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -4.89 | -4.89 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -4.69 | -4.69 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -4.84 | -4.84 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_urgency | -3.61 | -3.61 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | +3.00 | +3.00 @0 | 'drive' | 'drive<|im_end|>' |
