# Qwen3-8B (bf16)

substrate file: substrate.txt

quant: bf16 · layers 36 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -11.25 | 0.000 | 1.000 | 'Walk<|im_end|>' |
| substrate | +2.87 | 0.946 | 0.054 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +2.6 +5.5 +2.4 +2.0 +0.5 +0.5 -1.0 -2.1 -3.1 -1.6 -2.9 -2.6 -0.3 +2.0 +7.6 +2.7 +1.0 +2.2 +1.0 +3.4 +2.9 +3.0 +4.0 +1.9 -2.8 -1.9 -3.5 -5.7 -8.9 -7.6 -17.1 -31.1 -27.4 -18.4 -14.2 -7.3 -11.2
substrate: +2.6 +5.0 +2.1 +1.8 +1.1 +1.2 +0.2 -1.5 -3.4 -2.6 -4.5 -4.1 -1.0 +2.1 +7.4 +3.1 +0.8 +1.8 -0.8 +1.5 +1.9 +2.8 +4.9 +1.6 -1.1 +2.4 +0.4 -1.2 -2.0 -1.9 -4.9 -7.3 -7.3 +3.8 +4.9 +1.3 +2.9
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -11.0 -11.5 -11.2 -10.7 -11.0 -10.7 -11.0 -10.0 -10.5 -10.2 -10.0 -9.7 -9.0 -9.2 -9.0 -9.0 -9.0 -8.2 -8.3 -8.3 -8.8 -6.1 -4.7 +0.5 +1.1 +1.7 +2.6 +2.7 +2.6 +2.4 +2.6 +2.6 +2.3 +2.4 +2.7 +2.9
layers where the patch alone flips baseline to drive: [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -10.96 (model -11.25), sub +2.47 (model +2.75)
top Δ attention layers: L33 +5.05, L32 +2.40, L29 +1.80, L35 +0.62, L26 +0.58
top Δ MLP layers:       L30 +10.25, L34 -7.27, L33 -3.80, L35 -3.24, L32 +2.77
top Δ heads: L33H11 +6.11, L33H23 -2.36, L32H0 +2.05, L34H19 +1.19, L31H15 -1.00, L31H4 +0.94, L34H16 -0.94, L33H30 +0.91

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.461, max layer L9 (0.754)
- hdr_user: mean 0.005, max layer L4 (0.026)
- line1: mean 0.036, max layer L4 (0.219)
- line2: mean 0.028, max layer L4 (0.174)
- hdr_action: mean 0.005, max layer L4 (0.017)
- line3: mean 0.010, max layer L0 (0.044)
- line4: mean 0.008, max layer L0 (0.037)
- line5: mean 0.009, max layer L1 (0.038)
- line6: mean 0.017, max layer L0 (0.081)
- question: mean 0.096, max layer L23 (0.335)
- answer_instr: mean 0.039, max layer L18 (0.146)
- asst_header: mean 0.240, max layer L1 (0.544)
- last: mean 0.093, max layer L6 (0.253)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H11 mass 0.13 Δ+6.11, L34H19 mass 0.11 Δ+1.19, L32H0 mass 0.06 Δ+2.05, L31H4 mass 0.10 Δ+0.94, L34H21 mass 0.11 Δ+0.59, L26H26 mass 0.19 Δ+0.31

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +0.13 |
| loo_line2 | +1.31 |
| loo_line3 | +3.81 |
| loo_line4 | +0.95 |
| loo_line5 | +1.06 |
| loo_line6 | -3.96 |
| only_line1 | -9.56 |
| only_line2 | -11.25 |
| only_line3 | -10.50 |
| only_line4 | -9.50 |
| only_line5 | -3.50 |
| only_line6 | -0.15 |
| headers_only | -10.25 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | -11.25 | -11.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_CoT | -9.50 | -9.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | -10.00 | -10.00 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -8.00 | -8.00 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_hallucination | -14.00 | -14.00 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_library | -14.00 | -14.00 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | -13.50 | -13.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_threat | -7.50 | -7.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | -3.25 | -3.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate | +2.87 | +2.87 @0 | 'drive' | 'drive<|im_end|>' |
| substrate_pro | +6.52 | +6.52 @0 | 'drive' | 'drive<|im_end|>' |
| substrate+library (expect walk) | -11.65 | -11.65 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate_pro+library (expect walk) | -16.65 | -16.65 @0 | 'walk' | 'walk<|im_end|>' |
