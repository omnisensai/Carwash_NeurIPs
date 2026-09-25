# Qwen2.5-0.5B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 24 · heads 14 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +0.63 | 0.650 | 0.347 | 'Drive<|im_end|>' |
| substrate | -1.11 | 0.247 | 0.751 | 'Walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan -5.4 -0.5 -2.4 -6.4 -3.2 +0.5 -2.0 -1.4 -1.4 -2.9 -2.2 -1.2 -0.3 +2.4 +1.2 +1.0 +3.0 +3.7 +3.2 +1.2 -0.2 -1.2 -0.5 +0.6
substrate: +nan -4.9 -0.3 -1.8 -5.6 -4.0 -2.3 -4.0 -3.4 -2.2 -3.3 -2.3 -1.2 -0.8 +1.7 +0.9 +2.0 +3.4 +3.8 +4.1 +2.2 -0.2 -2.0 -1.5 -1.1
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +0.8 +0.8 +0.8 +0.6 +0.3 +0.1 +0.1 +0.0 -0.1 -0.2 -0.4 -0.1 -0.5 -1.0 -0.6 -0.7 -0.9 -0.7 -0.7 -1.1 -0.9 -0.9 -0.7 -1.1
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +0.68 (model +0.62), sub -1.10 (model -1.12)
top Δ attention layers: L23 -0.50, L20 -0.25, L5 -0.18, L21 -0.17, L14 +0.17
top Δ MLP layers:       L20 -0.75, L15 +0.45, L5 -0.29, L18 +0.28, L16 -0.26
top Δ heads: L23H10 -0.44, L23H7 -0.36, L23H12 +0.33, L21H13 -0.28, L23H3 -0.27, L21H3 +0.19, L21H8 -0.18, L20H7 -0.17

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.314, max layer L11 (0.619)
- hdr_user: mean 0.011, max layer L5 (0.046)
- line1: mean 0.014, max layer L22 (0.047)
- line2: mean 0.013, max layer L6 (0.035)
- hdr_action: mean 0.007, max layer L5 (0.022)
- line3: mean 0.009, max layer L0 (0.027)
- line4: mean 0.006, max layer L22 (0.025)
- line5: mean 0.006, max layer L0 (0.024)
- line6: mean 0.013, max layer L0 (0.049)
- question: mean 0.154, max layer L14 (0.360)
- answer_instr: mean 0.045, max layer L10 (0.195)
- asst_header: mean 0.242, max layer L2 (0.563)
- last: mean 0.117, max layer L23 (0.251)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L22H0 mass 0.26 Δ+0.11, L3H3 mass 0.22 Δ+0.08, L23H12 mass 0.04 Δ+0.33, L23H9 mass 0.16 Δ+0.08, L21H3 mass 0.05 Δ+0.19, L23H11 mass 0.12 Δ+0.08

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -1.11 |
| loo_line2 | -0.49 |
| loo_line3 | -1.23 |
| loo_line4 | -1.09 |
| loo_line5 | -0.93 |
| loo_line6 | -1.10 |
| only_line1 | -0.25 |
| only_line2 | -1.12 |
| only_line3 | -0.48 |
| only_line4 | -0.87 |
| only_line5 | -0.99 |
| only_line6 | -0.87 |
| headers_only | -0.37 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

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
