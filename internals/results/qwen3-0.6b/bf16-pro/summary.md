# Qwen3-0.6B

substrate file: substrate_pro.txt

quant: bf16 · layers 28 · heads 16 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +2.12 | 0.892 | 0.107 | 'drive<|im_end|>' |
| substrate | +5.25 | 0.994 | 0.005 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +1.3 +1.2 +5.4 +6.6 +5.9 +5.5 +4.7 +4.5 +5.9 +5.3 +3.3 +4.8 +3.3 +5.2 +6.5 +5.4 +3.0 +3.6 +2.3 +2.5 +1.2 +0.7 -1.6 +2.7 -1.4 -1.6 +1.7 +2.1
substrate: +nan +2.5 +1.4 +5.5 +6.5 +6.1 +5.7 +3.8 +4.2 +5.3 +4.7 +2.8 +3.3 +2.3 +4.0 +4.9 +3.5 +1.5 +2.8 +1.1 +2.4 +1.7 +2.5 +0.3 +4.5 +1.3 +0.9 +3.9 +5.2
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +2.0 +2.1 +1.5 +2.1 +2.1 +1.7 +1.7 +2.0 +2.2 +2.4 +2.6 +2.2 +2.4 +2.4 +2.1 +2.5 +2.2 +2.2 +3.0 +2.9 +3.4 +4.1 +5.0 +5.2 +5.0 +5.0 +5.1 +5.2
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +2.07 (model +2.12), sub +5.23 (model +5.25)
top Δ attention layers: L24 +0.96, L23 +0.65, L27 +0.64, L21 +0.59, L25 +0.41
top Δ MLP layers:       L27 -0.62, L26 -0.28, L19 +0.24, L25 +0.23, L14 -0.14
top Δ heads: L27H15 +0.63, L26H7 -0.60, L26H15 +0.56, L23H15 +0.48, L22H9 +0.41, L24H14 +0.40, L22H7 -0.38, L24H6 +0.38

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.487, max layer L27 (0.796)
- hdr_user: mean 0.002, max layer L2 (0.007)
- line1: mean 0.003, max layer L2 (0.009)
- line2: mean 0.003, max layer L0 (0.014)
- hdr_action: mean 0.003, max layer L6 (0.018)
- line3: mean 0.006, max layer L11 (0.039)
- line4: mean 0.003, max layer L0 (0.017)
- line5: mean 0.003, max layer L0 (0.024)
- line6: mean 0.007, max layer L0 (0.043)
- question: mean 0.049, max layer L0 (0.116)
- answer_instr: mean 0.040, max layer L11 (0.132)
- asst_header: mean 0.267, max layer L1 (0.700)
- last: mean 0.114, max layer L2 (0.208)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L22H9 mass 0.12 Δ+0.41, L26H15 mass 0.09 Δ+0.56, L21H13 mass 0.11 Δ+0.24, L27H15 mass 0.03 Δ+0.63, L24H14 mass 0.04 Δ+0.40, L26H4 mass 0.06 Δ+0.21

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +4.62 |
| loo_line2 | +4.87 |
| loo_line3 | +5.37 |
| loo_line4 | +4.87 |
| loo_line5 | +6.00 |
| loo_line6 | +5.37 |
| loo_line7 | +4.75 |
| loo_line8 | +5.50 |
| loo_line9 | +4.12 |
| only_line1 | +5.62 |
| only_line2 | +5.37 |
| only_line3 | +4.75 |
| only_line4 | +5.75 |
| only_line5 | +5.75 |
| only_line6 | +5.00 |
| only_line7 | +5.12 |
| only_line8 | +6.12 |
| only_line9 | +6.12 |
| headers_only | +5.12 |

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
| baseline | +2.12 | +2.12 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_CoT | +2.37 | +2.37 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | +2.73 | +2.73 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_expert | +3.04 | +3.04 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_hallucination | +2.32 | +2.32 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_library | +3.73 | +3.73 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_nomistakes | +2.48 | +2.48 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_threat | +2.83 | +2.83 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_urgency | +3.01 | – | 'wash' | 'wash<|im_end|>' |
| substrate | +3.87 | +3.87 @0 | 'drive' | 'drive<|im_end|>' |
| substrate_pro | +5.25 | +5.25 @0 | 'drive' | 'drive<|im_end|>' |
| substrate+library (expect walk) | +2.34 | +2.34 @0 | 'drive' | 'drive<|im_end|>' |
| substrate_pro+library (expect walk) | -0.51 | -0.51 @0 | 'walk' | 'walk<|im_end|>' |
