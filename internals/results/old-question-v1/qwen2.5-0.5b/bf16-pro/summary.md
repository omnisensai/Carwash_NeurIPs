# Qwen2.5-0.5B-Instruct (bf16)

substrate file: substrate_pro.txt

quant: bf16 · layers 24 · heads 14 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -1.37 | 0.201 | 0.795 | 'Walk<|im_end|>' |
| substrate | -0.24 | 0.439 | 0.559 | 'Walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan -5.7 -0.7 -2.5 -6.7 -3.4 +0.1 -2.1 -1.6 -1.9 -3.3 -2.5 -0.8 +0.1 +2.7 +1.9 -0.0 +0.4 +1.6 +1.6 -0.9 -3.0 -4.1 -3.0 -1.4
substrate: +nan -5.1 -0.7 -2.1 -5.7 -4.0 -1.7 -3.7 -2.9 -2.3 -3.3 -2.7 -1.1 -1.1 +1.9 +1.3 +0.7 +2.9 +3.2 +4.1 +1.4 -0.4 -1.7 -0.6 -0.2
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -1.4 -1.6 -1.5 -1.6 -1.7 -1.4 -1.5 -1.5 -1.6 -1.9 -2.0 -1.9 -2.0 -1.6 -0.7 -0.1 +0.0 -0.1 +0.0 -0.4 -0.2 -0.1 +0.1 -0.2
layers where the patch alone flips baseline to drive: [16, 18, 22]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -1.42 (model -1.38), sub -0.32 (model -0.25)
top Δ attention layers: L16 +0.65, L23 -0.55, L20 +0.49, L7 +0.22, L14 +0.20
top Δ MLP layers:       L23 -1.07, L22 +0.84, L21 +0.38, L12 -0.35, L19 -0.23
top Δ heads: L16H7 +0.53, L23H10 -0.43, L15H0 +0.25, L21H3 +0.21, L23H3 -0.18, L21H8 -0.16, L21H0 -0.13, L21H1 +0.12

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.321, max layer L16 (0.647)
- hdr_user: mean 0.005, max layer L6 (0.015)
- line1: mean 0.008, max layer L0 (0.040)
- line2: mean 0.006, max layer L22 (0.023)
- hdr_action: mean 0.004, max layer L5 (0.014)
- line3: mean 0.006, max layer L6 (0.019)
- line4: mean 0.007, max layer L22 (0.029)
- line5: mean 0.009, max layer L22 (0.036)
- line6: mean 0.010, max layer L22 (0.034)
- question: mean 0.210, max layer L15 (0.566)
- answer_instr: mean 0.052, max layer L10 (0.206)
- asst_header: mean 0.226, max layer L2 (0.538)
- last: mean 0.114, max layer L23 (0.247)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L16H7 mass 0.08 Δ+0.53, L21H3 mass 0.13 Δ+0.21, L3H3 mass 0.25 Δ+0.08, L23H0 mass 0.25 Δ+0.06, L20H11 mass 0.12 Δ+0.11, L20H6 mass 0.11 Δ+0.12

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -0.23 |
| loo_line2 | -0.37 |
| loo_line3 | -0.36 |
| loo_line4 | -0.24 |
| loo_line5 | -0.49 |
| loo_line6 | -1.24 |
| loo_line7 | -0.12 |
| loo_line8 | -0.62 |
| loo_line9 | -0.24 |
| only_line1 | -0.63 |
| only_line2 | -0.25 |
| only_line3 | -0.50 |
| only_line4 | -0.01 |
| only_line5 | -0.63 |
| only_line6 | -0.50 |
| only_line7 | -2.01 |
| only_line8 | -0.50 |
| only_line9 | -0.38 |
| headers_only | -0.51 |

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
| baseline | -1.37 | -1.37 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_CoT | -1.25 | -1.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | -3.63 | -3.63 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -0.50 | -0.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_hallucination | -1.50 | -1.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_library | -0.50 | -0.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | -2.37 | -2.37 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_threat | -2.62 | -2.62 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | -1.25 | -1.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate | -0.62 | -0.62 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate_pro | -0.24 | -0.24 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate+library (expect walk) | -1.50 | -1.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate_pro+library (expect walk) | +0.27 | +0.27 @0 | 'Drive' | 'Drive<|im_end|>' |
