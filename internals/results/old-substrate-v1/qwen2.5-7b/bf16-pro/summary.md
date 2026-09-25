# Qwen2.5-7B-Instruct

substrate file: substrate_pro.txt

quant: bf16 · layers 28 · heads 28 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -10.87 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | -0.25 | 0.438 | 0.562 | 'walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  -1.6 +1.8 +2.0 +1.9 +2.7 +2.4 +0.7 +0.8 +1.7 -0.3 +3.1 +1.1 +1.4 +1.5 -0.5 +1.4 +1.1 +0.3 +0.3 +0.8 -2.2 -1.1 -2.3 -3.4 -10.6 -16.9 -9.7 -9.4 -10.9
substrate: -1.6 +1.3 +2.1 +2.0 +3.3 +1.8 +1.4 +1.2 +2.4 +1.1 +3.2 +0.2 +0.7 +2.0 -0.3 +1.3 +0.7 +0.1 +0.6 +0.4 -0.6 -0.6 -0.9 +0.7 -0.4 -4.7 +0.3 +2.2 -0.5
final lens row == model logits: base True, sub False

## patching (substrate residual into baseline at the answer position)
M per layer: -10.7 -10.6 -10.9 -10.7 -10.6 -10.7 -10.7 -10.4 -10.7 -10.0 -10.4 -10.1 -10.0 -9.9 -10.5 -10.0 -9.9 -10.4 -7.9 -4.5 -1.7 -1.2 -1.2 -1.0 -0.5 -0.7 -0.5 -0.2
layers where the patch alone flips baseline to drive: []

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -10.78 (model -10.88), sub -0.33 (model -0.25)
top Δ attention layers: L26 +2.99, L23 +1.40, L27 +1.05, L25 +0.59, L24 +0.58
top Δ MLP layers:       L24 +2.26, L23 +1.13, L26 -0.38, L22 +0.33, L25 -0.24
top Δ heads: L26H6 +2.24, L25H12 +1.14, L27H24 +0.93, L26H14 +0.84, L26H26 +0.49, L24H27 +0.48, L23H13 +0.37, L23H11 +0.34

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.000, max layer L1 (0.002)
- hdr_user: mean 0.004, max layer L2 (0.020)
- line1: mean 0.006, max layer L2 (0.029)
- line2: mean 0.006, max layer L2 (0.026)
- hdr_action: mean 0.004, max layer L2 (0.026)
- line3: mean 0.008, max layer L2 (0.028)
- line4: mean 0.006, max layer L2 (0.021)
- line5: mean 0.007, max layer L0 (0.047)
- line6: mean 0.013, max layer L0 (0.053)
- question: mean 0.132, max layer L21 (0.305)
- answer_instr: mean 0.053, max layer L9 (0.177)
- asst_header: mean 0.223, max layer L1 (0.474)
- last: mean 0.100, max layer L27 (0.298)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L26H6 mass 0.04 Δ+2.24, L23H0 mass 0.12 Δ+0.24, L25H12 mass 0.02 Δ+1.14, L27H24 mass 0.02 Δ+0.93, L19H22 mass 0.29 Δ+0.07, L21H4 mass 0.10 Δ+0.14

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -0.75 |
| loo_line2 | -1.25 |
| loo_line3 | -0.25 |
| loo_line4 | -0.75 |
| loo_line5 | -1.50 |
| loo_line6 | -0.25 |
| loo_line7 | -0.25 |
| loo_line8 | -0.25 |
| loo_line9 | -2.62 |
| only_line1 | -8.62 |
| only_line2 | -9.25 |
| only_line3 | -11.37 |
| only_line4 | -10.50 |
| only_line5 | -6.12 |
| only_line6 | -5.50 |
| only_line7 | -8.50 |
| only_line8 | -8.87 |
| only_line9 | -4.50 |
| headers_only | -10.87 |

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
| baseline | -10.87 | -10.87 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -8.64 | -8.64 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | -8.51 | -8.51 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -8.25 | -8.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_hallucination | -9.07 | -9.07 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_library | -14.40 | -14.40 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | -9.03 | -9.03 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_threat | -8.73 | -8.73 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | -5.25 | -5.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate | -3.62 | -3.62 @0 | 'walk' | 'walk<|im_end|>' |
| substrate_pro | -0.25 | -0.25 @0 | 'walk' | 'walk<|im_end|>' |
| substrate+library (expect walk) | -6.78 | -6.78 @0 | 'walk' | 'walk<|im_end|>' |
| substrate_pro+library (expect walk) | -11.68 | -11.68 @0 | 'Walk' | 'Walk<|im_end|>' |
