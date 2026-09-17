# Qwen3-4B-Instruct-2507 (bf16)

substrate file: substrate_pro.txt

quant: bf16 · layers 36 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +0.25 | 0.562 | 0.438 | 'Drive<|im_end|>' |
| substrate | +9.50 | 1.000 | 0.000 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +1.5 +3.8 +2.8 +3.3 +2.2 +2.5 -0.4 +0.7 +3.1 +1.1 +1.2 +1.4 +1.2 +2.9 +2.3 +2.2 +3.7 +2.8 +2.7 +2.1 +0.7 +1.6 +0.8 -0.9 -0.6 -3.0 -4.5 -3.8 -4.9 -9.6 -10.7 -10.3 -2.7 +0.8 +0.4 +0.3
substrate: +nan +1.0 +4.1 +3.2 +4.1 +2.7 +2.8 +0.3 +1.2 +3.1 +2.7 +1.3 +1.9 +1.6 +3.1 +1.6 +0.6 +2.4 +2.4 +1.7 +0.3 -1.5 +0.0 -0.8 -0.2 +0.7 -0.7 -1.4 -1.4 -0.6 +0.0 +0.1 -0.4 +10.2 +9.1 +6.6 +9.5
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +0.2 +0.2 -0.5 -0.0 +0.5 +0.2 +0.2 +0.5 +0.5 +0.5 -0.1 +0.2 +0.0 -0.4 -0.4 -0.5 -1.6 -0.8 -1.7 -0.5 -0.7 -1.5 -5.5 +4.5 +3.5 +6.2 +5.8 +6.0 +7.0 +8.7 +8.7 +8.2 +8.2 +9.0 +9.2 +9.5
layers where the patch alone flips baseline to drive: [0, 1, 4, 5, 6, 7, 8, 9, 11, 12, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +0.18 (model +0.25), sub +9.45 (model +9.50)
top Δ attention layers: L32 +2.80, L35 +1.24, L33 +1.06, L29 +0.86, L24 +0.42
top Δ MLP layers:       L33 -3.90, L29 +2.44, L30 +2.25, L32 +0.79, L28 +0.51
top Δ heads: L33H11 +1.64, L32H2 +1.61, L33H22 -0.99, L32H0 +0.86, L33H30 +0.70, L35H26 +0.54, L33H21 -0.47, L29H27 +0.44

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.421, max layer L30 (0.810)
- hdr_user: mean 0.003, max layer L1 (0.009)
- line1: mean 0.007, max layer L0 (0.020)
- line2: mean 0.039, max layer L5 (0.274)
- hdr_action: mean 0.004, max layer L8 (0.012)
- line3: mean 0.008, max layer L0 (0.039)
- line4: mean 0.006, max layer L0 (0.027)
- line5: mean 0.008, max layer L0 (0.043)
- line6: mean 0.013, max layer L0 (0.040)
- question: mean 0.119, max layer L21 (0.316)
- answer_instr: mean 0.058, max layer L17 (0.188)
- asst_header: mean 0.181, max layer L1 (0.428)
- last: mean 0.083, max layer L35 (0.212)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H11 mass 0.15 Δ+1.64, L32H0 mass 0.10 Δ+0.86, L29H27 mass 0.19 Δ+0.44, L32H2 mass 0.05 Δ+1.61, L29H0 mass 0.37 Δ+0.13, L33H30 mass 0.05 Δ+0.70

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +12.25 |
| loo_line2 | +3.75 |
| loo_line3 | +8.25 |
| loo_line4 | +8.00 |
| loo_line5 | +11.00 |
| loo_line6 | +13.50 |
| loo_line7 | +2.50 |
| loo_line8 | +7.25 |
| loo_line9 | +0.50 |
| only_line1 | -14.62 |
| only_line2 | -9.00 |
| only_line3 | -11.25 |
| only_line4 | -12.87 |
| only_line5 | -10.12 |
| only_line6 | +10.50 |
| only_line7 | +5.75 |
| only_line8 | -2.25 |
| only_line9 | -10.87 |
| headers_only | -8.75 |

line1: - Perform an activity on an object at a service location.
line2: - The object must be at the service location for the activity to complete.
line3: - No other objectives or goals are relevant for the user.
line4: - The object is initially with the user at location A.
line5: - The activity is performed at location B (the service location). The object must be present at location B.
line6: - Vehicles are not portable. Walking leaves a vehicle behind. Leaving the object behind fails the objective.
line7: - Books are portable. Walking transports both the user and the book.
line8: - Leaving the object behind fails the objective.
line9: - To transport a vehicle from A to B, the user must operate it.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | +0.25 | +0.25 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_CoT | -4.51 | -4.51 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | -4.00 | -4.00 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -0.50 | -0.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_hallucination | -6.55 | -6.55 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_library | -22.05 | -22.05 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | -3.44 | -3.44 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -3.74 | -3.74 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | +6.25 | +6.25 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate | +0.25 | +0.25 @0 | 'drive' | 'drive<|im_end|>' |
| substrate_pro | +9.50 | +9.50 @0 | 'drive' | 'drive<|im_end|>' |
| substrate+library (expect walk) | -19.00 | -19.00 @0 | 'walk' | 'walk<|im_end|>' |
| substrate_pro+library (expect walk) | -22.50 | -22.50 @0 | 'walk' | 'walk<|im_end|>' |
