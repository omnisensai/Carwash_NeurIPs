# Qwen3-0.6B

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 16 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +2.12 | 0.892 | 0.107 | 'drive<|im_end|>' |
| substrate | +3.87 | 0.979 | 0.020 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +1.3 +1.2 +5.4 +6.6 +5.9 +5.5 +4.7 +4.5 +5.9 +5.3 +3.3 +4.8 +3.3 +5.2 +6.5 +5.4 +3.0 +3.6 +2.3 +2.5 +1.2 +0.7 -1.6 +2.7 -1.4 -1.6 +1.7 +2.1
substrate: +nan +2.3 +1.4 +5.4 +6.5 +6.2 +5.7 +4.1 +4.2 +4.9 +5.0 +2.6 +3.6 +2.3 +4.1 +4.9 +3.4 +1.8 +3.7 +1.7 +2.8 +2.1 +2.3 +0.3 +4.0 +0.2 -0.2 +2.9 +4.1
final lens row == model logits: base True, sub False

## patching (substrate residual into baseline at the answer position)
M per layer: +1.7 +2.1 +2.0 +2.1 +2.2 +2.1 +2.1 +2.2 +2.0 +2.1 +2.4 +2.2 +2.1 +2.2 +1.9 +2.1 +2.5 +2.1 +2.9 +3.0 +3.5 +4.0 +4.0 +4.5 +4.0 +3.9 +4.0 +3.9
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +2.07 (model +2.12), sub +4.06 (model +3.88)
top Δ attention layers: L27 +0.47, L21 +0.32, L24 +0.31, L23 +0.31, L20 +0.27
top Δ MLP layers:       L27 -0.29, L19 +0.24, L17 +0.18, L18 -0.14, L26 -0.12
top Δ heads: L26H7 -0.48, L26H15 +0.46, L27H15 +0.39, L22H9 +0.25, L20H14 +0.21, L26H9 -0.21, L25H10 +0.20, L21H1 +0.20

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.494, max layer L27 (0.803)
- hdr_user: mean 0.004, max layer L2 (0.021)
- line1: mean 0.010, max layer L2 (0.032)
- line2: mean 0.008, max layer L11 (0.032)
- hdr_action: mean 0.005, max layer L6 (0.023)
- line3: mean 0.007, max layer L0 (0.031)
- line4: mean 0.004, max layer L0 (0.027)
- line5: mean 0.006, max layer L0 (0.034)
- line6: mean 0.009, max layer L0 (0.080)
- question: mean 0.055, max layer L0 (0.129)
- answer_instr: mean 0.039, max layer L11 (0.128)
- asst_header: mean 0.266, max layer L1 (0.712)
- last: mean 0.115, max layer L2 (0.214)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L26H15 mass 0.07 Δ+0.46, L22H9 mass 0.11 Δ+0.25, L27H15 mass 0.03 Δ+0.39, L21H13 mass 0.05 Δ+0.16, L25H10 mass 0.04 Δ+0.20, L21H1 mass 0.04 Δ+0.20

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +3.00 |
| loo_line2 | +4.12 |
| loo_line3 | +4.12 |
| loo_line4 | +3.87 |
| loo_line5 | +4.12 |
| loo_line6 | +4.12 |
| only_line1 | +3.87 |
| only_line2 | +3.25 |
| only_line3 | +4.37 |
| only_line4 | +4.25 |
| only_line5 | +4.00 |
| only_line6 | +4.00 |
| headers_only | +3.75 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

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
