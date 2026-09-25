# Qwen2.5-0.5B-Instruct

substrate file: substrate_pro.txt

quant: bf16 · layers 24 · heads 14 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +0.63 | 0.650 | 0.347 | 'Drive<|im_end|>' |
| substrate | -0.94 | 0.280 | 0.716 | 'walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan -5.4 -0.5 -2.4 -6.4 -3.2 +0.5 -2.0 -1.4 -1.4 -2.9 -2.2 -1.2 -0.3 +2.4 +1.2 +1.0 +3.0 +3.7 +3.2 +1.2 -0.2 -1.2 -0.5 +0.6
substrate: +nan -5.0 -0.7 -2.5 -6.0 -4.1 -1.5 -3.7 -2.7 -1.9 -2.9 -2.2 -1.3 -1.2 +1.7 +1.1 +1.9 +3.0 +3.5 +3.9 +2.2 +0.3 -1.7 -1.2 -0.9
final lens row == model logits: base True, sub False

## patching (substrate residual into baseline at the answer position)
M per layer: +0.6 +0.5 +0.5 +0.5 +0.3 +0.3 -0.1 -0.1 -0.2 -0.2 -0.6 -0.4 -0.8 -1.4 -1.2 -1.3 -1.1 -1.0 -1.0 -1.2 -1.1 -0.9 -0.8 -0.9
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +0.81 (model +0.62), sub -0.94 (model -1.00)
top Δ attention layers: L23 -0.58, L5 -0.32, L15 +0.16, L8 +0.14, L7 +0.14
top Δ MLP layers:       L22 -0.64, L20 -0.60, L15 +0.47, L21 -0.41, L16 -0.35
top Δ heads: L23H10 -0.55, L23H7 -0.45, L21H9 +0.32, L21H13 -0.27, L20H10 +0.26, L23H3 -0.25, L23H12 +0.21, L23H1 +0.18

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.304, max layer L11 (0.622)
- hdr_user: mean 0.005, max layer L6 (0.016)
- line1: mean 0.006, max layer L22 (0.016)
- line2: mean 0.006, max layer L0 (0.032)
- hdr_action: mean 0.004, max layer L5 (0.015)
- line3: mean 0.007, max layer L6 (0.021)
- line4: mean 0.006, max layer L22 (0.021)
- line5: mean 0.007, max layer L22 (0.025)
- line6: mean 0.007, max layer L0 (0.024)
- question: mean 0.133, max layer L14 (0.338)
- answer_instr: mean 0.044, max layer L10 (0.186)
- asst_header: mean 0.245, max layer L2 (0.568)
- last: mean 0.119, max layer L23 (0.249)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L22H4 mass 0.23 Δ+0.09, L3H3 mass 0.22 Δ+0.07, L23H9 mass 0.15 Δ+0.11, L23H0 mass 0.19 Δ+0.08, L23H11 mass 0.12 Δ+0.12, L22H0 mass 0.22 Δ+0.06

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -0.75 |
| loo_line2 | -0.75 |
| loo_line3 | -0.68 |
| loo_line4 | -0.75 |
| loo_line5 | -1.05 |
| loo_line6 | -1.06 |
| loo_line7 | -0.73 |
| loo_line8 | -1.25 |
| loo_line9 | -0.56 |
| only_line1 | -0.94 |
| only_line2 | -0.37 |
| only_line3 | -0.85 |
| only_line4 | -1.02 |
| only_line5 | -0.98 |
| only_line6 | -0.61 |
| only_line7 | -1.49 |
| only_line8 | -0.94 |
| only_line9 | -0.81 |
| headers_only | -0.64 |

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
| baseline | +0.63 | +0.63 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_CoT | -1.25 | -1.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | -3.63 | -3.63 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -0.50 | -0.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_hallucination | -1.50 | -1.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_library | -0.50 | -0.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | -2.37 | -2.37 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_threat | -2.62 | -2.62 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | -1.25 | -1.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate | -1.11 | -1.11 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate_pro | -0.94 | -0.94 @0 | 'walk' | 'walk<|im_end|>' |
| substrate+library (expect walk) | -1.50 | -1.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate_pro+library (expect walk) | +0.27 | +0.27 @0 | 'Drive' | 'Drive<|im_end|>' |
