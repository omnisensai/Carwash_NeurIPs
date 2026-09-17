# Qwen2.5-0.5B-Instruct (bf16)

substrate file: substrate.txt

quant: bf16 · layers 24 · heads 14 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -1.37 | 0.201 | 0.795 | 'Walk<|im_end|>' |
| substrate | -0.62 | 0.348 | 0.650 | 'Walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan -5.7 -0.7 -2.5 -6.7 -3.4 +0.1 -2.1 -1.6 -1.9 -3.3 -2.5 -0.8 +0.1 +2.7 +1.9 -0.0 +0.4 +1.6 +1.6 -0.9 -3.0 -4.1 -3.0 -1.4
substrate: +nan -4.9 -0.1 -1.9 -5.8 -4.0 -2.1 -3.6 -3.4 -2.4 -3.3 -2.3 -0.4 -0.2 +2.3 +1.5 +0.1 +2.6 +3.1 +3.7 +0.6 -1.0 -2.0 -0.9 -0.6
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -1.5 -1.6 -1.5 -1.5 -1.7 -1.4 -1.4 -1.6 -1.7 -1.7 -2.1 -1.9 -2.0 -1.7 -0.6 -0.4 -0.4 -0.4 -0.4 -0.4 -0.6 -0.2 -0.2 -0.6
layers where the patch alone flips baseline to drive: []

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -1.42 (model -1.38), sub -0.59 (model -0.62)
top Δ attention layers: L16 +0.63, L23 -0.54, L20 +0.44, L21 +0.23, L7 +0.20
top Δ MLP layers:       L23 -0.98, L22 +0.71, L19 -0.55, L21 +0.30, L12 -0.25
top Δ heads: L16H7 +0.56, L23H10 -0.50, L21H3 +0.44, L23H3 -0.22, L20H11 +0.18, L21H0 -0.16, L20H6 +0.16, L23H12 +0.14

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.329, max layer L16 (0.707)
- hdr_user: mean 0.011, max layer L22 (0.048)
- line1: mean 0.015, max layer L22 (0.055)
- line2: mean 0.013, max layer L10 (0.034)
- hdr_action: mean 0.007, max layer L5 (0.021)
- line3: mean 0.011, max layer L22 (0.031)
- line4: mean 0.007, max layer L22 (0.031)
- line5: mean 0.007, max layer L0 (0.026)
- line6: mean 0.015, max layer L22 (0.067)
- question: mean 0.237, max layer L15 (0.572)
- answer_instr: mean 0.053, max layer L10 (0.218)
- asst_header: mean 0.227, max layer L2 (0.555)
- last: mean 0.113, max layer L23 (0.253)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L21H3 mass 0.10 Δ+0.44, L16H7 mass 0.06 Δ+0.56, L20H11 mass 0.14 Δ+0.18, L23H9 mass 0.18 Δ+0.11, L3H3 mass 0.25 Δ+0.08, L22H0 mass 0.27 Δ+0.04

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -0.25 |
| loo_line2 | -0.87 |
| loo_line3 | -0.75 |
| loo_line4 | -0.75 |
| loo_line5 | -0.62 |
| loo_line6 | -0.37 |
| only_line1 | -0.37 |
| only_line2 | -0.87 |
| only_line3 | -0.12 |
| only_line4 | -0.12 |
| only_line5 | -0.25 |
| only_line6 | -0.75 |
| headers_only | -0.62 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

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
