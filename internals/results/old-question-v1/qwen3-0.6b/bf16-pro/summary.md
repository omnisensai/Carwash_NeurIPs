# Qwen3-0.6B (bf16)

substrate file: substrate_pro.txt

quant: bf16 · layers 28 · heads 16 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +2.60 | 0.882 | 0.065 | 'drive<|im_end|>' |
| substrate | +1.73 | 0.842 | 0.149 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +1.6 +1.6 +5.6 +6.8 +6.0 +5.7 +4.8 +4.5 +5.8 +5.7 +3.7 +5.5 +4.2 +5.8 +6.9 +5.9 +3.9 +3.9 +2.3 +2.9 -0.5 -1.1 -1.9 +2.6 -2.3 -2.7 +1.9 +2.6
substrate: +nan +2.8 +1.6 +5.7 +6.6 +6.2 +5.8 +3.9 +4.2 +5.2 +5.0 +2.9 +3.6 +2.5 +4.1 +4.8 +3.4 +2.4 +3.3 +1.7 +2.8 +0.1 +0.0 -0.7 +3.4 -2.8 -3.3 +1.7 +1.7
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +2.8 +2.4 +2.1 +2.2 +2.2 +2.1 +2.5 +2.5 +2.5 +2.8 +2.6 +2.3 +2.2 +2.4 +2.5 +2.7 +2.3 +1.2 +1.8 +1.9 +1.6 +1.4 +1.5 +1.4 +1.5 +1.4 +1.7 +1.7
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +2.70 (model +2.75), sub +1.74 (model +1.75)
top Δ attention layers: L24 -1.12, L25 -0.62, L23 +0.51, L27 -0.50, L20 -0.23
top Δ MLP layers:       L26 +0.58, L23 -0.50, L25 +0.43, L27 +0.32, L21 +0.28
top Δ heads: L24H14 -0.85, L23H15 +0.67, L26H9 -0.57, L24H6 -0.35, L27H15 -0.32, L25H9 -0.23, L21H13 -0.22, L20H14 -0.20

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.491, max layer L27 (0.754)
- hdr_user: mean 0.002, max layer L2 (0.007)
- line1: mean 0.003, max layer L2 (0.010)
- line2: mean 0.003, max layer L0 (0.014)
- hdr_action: mean 0.004, max layer L6 (0.015)
- line3: mean 0.007, max layer L11 (0.040)
- line4: mean 0.004, max layer L0 (0.017)
- line5: mean 0.004, max layer L0 (0.024)
- line6: mean 0.011, max layer L0 (0.043)
- question: mean 0.087, max layer L26 (0.224)
- answer_instr: mean 0.046, max layer L17 (0.167)
- asst_header: mean 0.263, max layer L1 (0.677)
- last: mean 0.115, max layer L2 (0.207)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L26H7 mass 0.26 Δ+0.20, L23H15 mass 0.05 Δ+0.67, L26H5 mass 0.16 Δ+0.19, L26H3 mass 0.16 Δ+0.15, L21H0 mass 0.20 Δ+0.09, L22H7 mass 0.13 Δ+0.13

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +1.23 |
| loo_line2 | +1.99 |
| loo_line3 | +1.60 |
| loo_line4 | +1.48 |
| loo_line5 | +2.60 |
| loo_line6 | +2.86 |
| loo_line7 | +2.23 |
| loo_line8 | +1.86 |
| loo_line9 | +1.24 |
| only_line1 | +1.61 |
| only_line2 | +1.11 |
| only_line3 | +0.24 |
| only_line4 | +2.24 |
| only_line5 | +1.74 |
| only_line6 | -0.03 |
| only_line7 | +0.72 |
| only_line8 | +2.36 |
| only_line9 | +1.48 |
| headers_only | +0.86 |

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
| baseline | +2.60 | +2.60 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_CoT | +2.37 | +2.37 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | +2.73 | +2.73 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_expert | +3.04 | +3.04 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_hallucination | +2.32 | +2.32 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_library | +3.73 | +3.73 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_nomistakes | +2.48 | +2.48 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_threat | +2.83 | +2.83 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_urgency | +3.01 | – | 'wash' | 'wash<|im_end|>' |
| substrate | +1.33 | +1.33 @0 | 'drive' | 'drive<|im_end|>' |
| substrate_pro | +1.73 | +1.73 @0 | 'drive' | 'drive<|im_end|>' |
| substrate+library (expect walk) | +2.34 | +2.34 @0 | 'drive' | 'drive<|im_end|>' |
| substrate_pro+library (expect walk) | -0.51 | -0.51 @0 | 'walk' | 'walk<|im_end|>' |
