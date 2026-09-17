# Qwen2.5-1.5B-Instruct

substrate file: substrate_pro.txt

quant: bf16 · layers 28 · heads 12 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +1.65 | 0.839 | 0.161 | 'drive<|im_end|>' |
| substrate | +4.14 | 0.984 | 0.016 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +5.5 +0.7 +3.3 +2.1 +2.3 +1.2 +2.6 +1.9 +0.0 -0.3 +0.9 +1.9 +2.3 +3.0 +1.0 +0.8 +1.6 +2.6 +1.1 +1.8 -2.4 -1.8 -1.5 -3.8 -1.2 -1.6 +0.9 +1.7
substrate: +nan +6.5 +0.1 +2.5 +2.6 +3.0 +4.0 +3.4 +2.2 -0.0 +0.1 +0.7 +1.9 +2.0 +1.7 +1.0 +0.2 +2.4 +3.6 +1.8 +2.9 +0.0 +0.3 -0.0 -1.7 +1.8 +0.7 +2.8 +4.3
final lens row == model logits: base True, sub False

## patching (substrate residual into baseline at the answer position)
M per layer: +1.5 +1.7 +1.5 +1.5 +1.8 +1.7 +1.8 +1.9 +2.1 +2.2 +2.0 +2.4 +2.6 +2.6 +2.9 +3.5 +3.3 +2.8 +2.1 +2.3 +3.9 +3.6 +3.5 +4.3 +4.1 +4.1 +4.0 +4.1
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +1.52 (model +1.62), sub +4.03 (model +4.12)
top Δ attention layers: L27 +1.20, L20 +0.74, L24 +0.65, L25 -0.47, L11 -0.23
top Δ MLP layers:       L27 -1.37, L23 +0.54, L24 +0.42, L25 +0.38, L14 +0.37
top Δ heads: L27H4 +1.16, L24H11 +0.44, L25H4 -0.32, L20H4 +0.23, L22H9 -0.22, L22H7 +0.20, L21H1 +0.19, L20H5 +0.19

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.313, max layer L4 (0.636)
- hdr_user: mean 0.003, max layer L7 (0.008)
- line1: mean 0.006, max layer L0 (0.016)
- line2: mean 0.004, max layer L0 (0.016)
- hdr_action: mean 0.003, max layer L1 (0.008)
- line3: mean 0.005, max layer L11 (0.026)
- line4: mean 0.004, max layer L0 (0.019)
- line5: mean 0.006, max layer L0 (0.044)
- line6: mean 0.008, max layer L0 (0.037)
- question: mean 0.138, max layer L20 (0.498)
- answer_instr: mean 0.055, max layer L11 (0.173)
- asst_header: mean 0.238, max layer L1 (0.439)
- last: mean 0.116, max layer L15 (0.239)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L27H4 mass 0.07 Δ+1.16, L27H10 mass 0.17 Δ+0.18, L5H5 mass 0.17 Δ+0.14, L21H1 mass 0.12 Δ+0.19, L20H5 mass 0.08 Δ+0.19, L26H11 mass 0.13 Δ+0.09

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +3.65 |
| loo_line2 | +3.90 |
| loo_line3 | +3.16 |
| loo_line4 | +3.28 |
| loo_line5 | +3.39 |
| loo_line6 | +3.39 |
| loo_line7 | +4.39 |
| loo_line8 | +3.15 |
| loo_line9 | +2.52 |
| only_line1 | +4.55 |
| only_line2 | +5.03 |
| only_line3 | +5.04 |
| only_line4 | +4.66 |
| only_line5 | +4.39 |
| only_line6 | +5.77 |
| only_line7 | +3.78 |
| only_line8 | +5.02 |
| only_line9 | +5.27 |
| headers_only | +4.92 |

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
| baseline | +1.65 | +1.65 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_CoT | -0.50 | -0.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | +0.09 | +0.09 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_expert | +1.58 | +1.58 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_hallucination | -0.29 | -0.29 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_library | -1.84 | -1.84 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | +0.19 | +0.19 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -0.22 | -0.22 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_urgency | +1.27 | +1.27 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate | +3.53 | +3.53 @0 | 'drive' | 'drive<|im_end|>' |
| substrate_pro | +4.14 | +4.14 @0 | 'drive' | 'drive<|im_end|>' |
| substrate+library (expect walk) | -2.12 | -2.12 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate_pro+library (expect walk) | -1.15 | -1.15 @0 | 'Walk' | 'Walk<|im_end|>' |
