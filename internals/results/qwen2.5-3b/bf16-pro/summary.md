# Qwen2.5-3B-Instruct

substrate file: substrate_pro.txt

quant: bf16 · layers 36 · heads 16 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +4.25 | 0.986 | 0.014 | 'drive<|im_end|>' |
| substrate | +5.00 | 0.993 | 0.007 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan -7.0 -0.9 -3.1 -2.8 -4.8 -6.1 -4.5 -5.3 -4.3 -1.3 -3.7 -5.1 +0.4 -2.0 -1.1 -2.7 -0.2 -0.9 -1.8 +0.5 -1.3 -1.0 -1.4 -0.3 -1.7 -0.2 -3.2 +3.2 +1.0 +0.4 -0.1 +6.0 +5.2 +4.5 +4.3 +4.3
substrate: +nan -7.7 -1.8 -4.1 -4.9 -7.2 -7.7 -5.6 -6.4 -4.7 -2.3 -4.6 -5.6 +1.3 -1.3 -0.9 -2.8 +0.1 -1.6 -1.7 +0.3 -0.8 +1.2 -0.4 +0.7 -0.5 +1.9 -0.7 +2.8 +0.3 -0.4 -1.7 +5.1 +4.4 +5.7 +4.7 +5.0
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +4.0 +3.8 +4.3 +4.0 +4.0 +4.0 +4.0 +4.3 +4.5 +4.7 +4.3 +4.0 +4.3 +4.3 +4.3 +4.5 +4.5 +4.5 +4.3 +4.3 +4.2 +3.5 +4.0 +5.5 +4.8 +3.3 +2.5 +2.5 +3.2 +3.5 +2.7 +2.2 +3.5 +5.0 +4.8 +5.0
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +4.20 (model +4.25), sub +4.79 (model +5.00)
top Δ attention layers: L33 +2.12, L32 +0.50, L27 -0.33, L34 -0.32, L24 +0.21
top Δ MLP layers:       L32 -0.93, L27 -0.53, L21 +0.42, L30 -0.36, L35 -0.31
top Δ heads: L33H0 +1.59, L32H9 +0.52, L33H15 +0.42, L31H5 +0.28, L30H1 +0.23, L34H10 -0.21, L23H0 -0.18, L27H4 -0.18

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.322, max layer L5 (0.754)
- hdr_user: mean 0.003, max layer L8 (0.009)
- line1: mean 0.006, max layer L8 (0.017)
- line2: mean 0.005, max layer L0 (0.022)
- hdr_action: mean 0.004, max layer L8 (0.013)
- line3: mean 0.007, max layer L21 (0.023)
- line4: mean 0.004, max layer L0 (0.018)
- line5: mean 0.006, max layer L0 (0.042)
- line6: mean 0.009, max layer L0 (0.047)
- question: mean 0.092, max layer L27 (0.220)
- answer_instr: mean 0.052, max layer L16 (0.163)
- asst_header: mean 0.218, max layer L2 (0.565)
- last: mean 0.108, max layer L0 (0.247)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H0 mass 0.04 Δ+1.59, L21H4 mass 0.21 Δ+0.10, L24H4 mass 0.26 Δ+0.08, L33H15 mass 0.04 Δ+0.42, L32H9 mass 0.03 Δ+0.52, L22H1 mass 0.32 Δ+0.04

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +10.50 |
| loo_line2 | +5.25 |
| loo_line3 | +5.25 |
| loo_line4 | +6.00 |
| loo_line5 | +3.75 |
| loo_line6 | +1.25 |
| loo_line7 | +7.75 |
| loo_line8 | +5.75 |
| loo_line9 | +2.00 |
| only_line1 | +9.12 |
| only_line2 | +10.75 |
| only_line3 | +9.50 |
| only_line4 | +9.87 |
| only_line5 | +10.12 |
| only_line6 | +11.00 |
| only_line7 | +6.75 |
| only_line8 | +9.00 |
| only_line9 | +13.12 |
| headers_only | +9.50 |

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
| baseline | +4.25 | +4.25 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_CoT | +8.75 | +8.75 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | +9.86 | +9.86 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_expert | +10.25 | +10.25 @0 | 'Drive' | 'Drive.<|im_end|>' |
| benchmark_hallucination | +9.51 | +9.51 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_library | -4.75 | -4.75 @0 | 'Walk' | 'Walk.<|im_end|>' |
| benchmark_nomistakes | +7.10 | +7.10 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_threat | +9.48 | +9.48 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_urgency | +8.04 | +8.04 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate | +9.75 | +9.75 @0 | 'drive' | 'drive<|im_end|>' |
| substrate_pro | +5.00 | +5.00 @0 | 'drive' | 'drive<|im_end|>' |
| substrate+library (expect walk) | +4.02 | +4.02 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate_pro+library (expect walk) | -9.50 | -9.50 @0 | 'Walk' | 'Walk<|im_end|>' |
