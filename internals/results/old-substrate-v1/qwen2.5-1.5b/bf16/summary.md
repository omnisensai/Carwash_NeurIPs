# Qwen2.5-1.5B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 12 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +1.65 | 0.839 | 0.161 | 'drive<|im_end|>' |
| substrate | +3.53 | 0.971 | 0.029 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +5.5 +0.7 +3.3 +2.1 +2.3 +1.2 +2.6 +1.9 +0.0 -0.3 +0.9 +1.9 +2.3 +3.0 +1.0 +0.8 +1.6 +2.6 +1.1 +1.8 -2.4 -1.8 -1.5 -3.8 -1.2 -1.6 +0.9 +1.7
substrate: +nan +6.8 +0.8 +2.7 +3.1 +3.2 +4.7 +3.9 +3.0 +0.2 +0.8 +0.9 +1.9 +2.0 +2.1 +1.1 +0.6 +2.2 +3.2 +2.3 +2.0 -1.8 -0.8 -0.9 -2.4 +0.8 +0.2 +2.7 +3.5
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +1.6 +1.5 +1.6 +1.6 +1.6 +1.6 +1.8 +2.0 +1.9 +2.0 +2.3 +2.3 +2.1 +2.5 +2.5 +2.6 +2.6 +2.9 +3.1 +3.1 +4.3 +4.0 +3.9 +3.8 +3.8 +3.8 +3.8 +3.5
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +1.52 (model +1.62), sub +3.51 (model +3.50)
top Δ attention layers: L27 +0.93, L25 -0.33, L20 +0.33, L11 -0.28, L4 +0.21
top Δ MLP layers:       L27 -1.29, L24 +0.68, L25 +0.51, L23 +0.47, L4 -0.43
top Δ heads: L27H4 +0.91, L20H9 +0.22, L22H9 -0.20, L5H5 +0.15, L27H11 -0.15, L24H9 +0.15, L20H7 -0.14, L23H2 +0.13

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.319, max layer L25 (0.629)
- hdr_user: mean 0.008, max layer L2 (0.025)
- line1: mean 0.014, max layer L27 (0.038)
- line2: mean 0.009, max layer L11 (0.026)
- hdr_action: mean 0.005, max layer L1 (0.016)
- line3: mean 0.008, max layer L0 (0.029)
- line4: mean 0.008, max layer L0 (0.075)
- line5: mean 0.009, max layer L0 (0.056)
- line6: mean 0.012, max layer L0 (0.058)
- question: mean 0.148, max layer L20 (0.489)
- answer_instr: mean 0.055, max layer L11 (0.189)
- asst_header: mean 0.236, max layer L0 (0.461)
- last: mean 0.120, max layer L0 (0.272)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L27H4 mass 0.06 Δ+0.91, L0H10 mass 0.50 Δ+0.09, L5H5 mass 0.19 Δ+0.15, L16H3 mass 0.26 Δ+0.08, L27H10 mass 0.15 Δ+0.13, L21H1 mass 0.13 Δ+0.13

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +3.64 |
| loo_line2 | +2.91 |
| loo_line3 | +4.41 |
| loo_line4 | +3.66 |
| loo_line5 | +1.57 |
| loo_line6 | +4.27 |
| only_line1 | +2.69 |
| only_line2 | +0.86 |
| only_line3 | +1.84 |
| only_line4 | +1.38 |
| only_line5 | +2.42 |
| only_line6 | +4.66 |
| headers_only | +1.18 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

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
