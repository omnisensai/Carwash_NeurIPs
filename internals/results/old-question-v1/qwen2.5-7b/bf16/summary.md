# Qwen2.5-7B-Instruct (bf16)

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 28 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -8.01 | 0.000 | 0.999 | 'Walk<|im_end|>' |
| substrate | -0.39 | 0.403 | 0.595 | 'Walk<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  -1.6 +2.0 +2.3 +2.2 +3.0 +3.0 +1.2 +1.5 +2.8 +0.4 +3.1 +1.0 +0.9 +1.1 -0.2 +0.9 +1.3 -0.6 -1.3 -0.4 -1.8 -1.3 -3.0 -2.6 -8.8 -14.9 -12.8 -9.7 -8.0
substrate: -1.6 +1.4 +2.0 +1.8 +3.3 +2.8 +1.6 +2.1 +3.0 +1.6 +2.4 -0.2 +0.5 +0.9 +0.2 +1.4 +1.3 -0.4 -0.9 +0.2 -0.2 +0.4 -1.4 +0.1 -2.0 -6.2 -3.9 -0.8 -0.4
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -7.9 -7.4 -8.1 -8.4 -8.5 -8.1 -8.3 -7.6 -8.4 -8.4 -8.3 -8.8 -8.0 -8.7 -8.5 -8.8 -8.9 -9.0 -7.0 -4.2 -2.5 -2.1 -1.5 -1.4 -1.0 -0.9 -0.8 -0.4
layers where the patch alone flips baseline to drive: []

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -7.95 (model -8.00), sub -0.22 (model -0.12)
top Δ attention layers: L25 +0.84, L24 +0.57, L26 +0.56, L27 +0.55, L9 -0.42
top Δ MLP layers:       L24 +1.53, L23 +1.35, L27 +0.55, L19 +0.26, L9 +0.22
top Δ heads: L26H6 +0.91, L25H12 +0.77, L27H24 +0.60, L26H2 -0.56, L26H16 +0.37, L24H21 +0.30, L23H0 +0.20, L25H7 +0.18

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.000, max layer L2 (0.002)
- hdr_user: mean 0.010, max layer L9 (0.076)
- line1: mean 0.019, max layer L2 (0.111)
- line2: mean 0.017, max layer L2 (0.064)
- hdr_action: mean 0.006, max layer L2 (0.037)
- line3: mean 0.012, max layer L0 (0.058)
- line4: mean 0.009, max layer L0 (0.044)
- line5: mean 0.011, max layer L0 (0.045)
- line6: mean 0.020, max layer L0 (0.088)
- question: mean 0.210, max layer L22 (0.472)
- answer_instr: mean 0.069, max layer L9 (0.237)
- asst_header: mean 0.210, max layer L1 (0.492)
- last: mean 0.104, max layer L27 (0.284)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L26H6 mass 0.10 Δ+0.91, L25H12 mass 0.04 Δ+0.77, L27H24 mass 0.05 Δ+0.60, L21H25 mass 0.37 Δ+0.06, L19H22 mass 0.29 Δ+0.06, L26H16 mass 0.04 Δ+0.37

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -3.19 |
| loo_line2 | -2.40 |
| loo_line3 | +1.80 |
| loo_line4 | -1.06 |
| loo_line5 | +2.83 |
| loo_line6 | -2.13 |
| only_line1 | -3.93 |
| only_line2 | -9.82 |
| only_line3 | -5.02 |
| only_line4 | -5.06 |
| only_line5 | -3.15 |
| only_line6 | +0.63 |
| headers_only | -9.73 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | -8.01 | -8.01 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_CoT | -8.64 | -8.64 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | -8.51 | -8.51 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -8.25 | -8.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_hallucination | -9.07 | -9.07 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_library | -14.40 | -14.40 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | -9.03 | -9.03 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_threat | -8.73 | -8.73 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | -5.25 | -5.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate | -0.39 | -0.39 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate_pro | +3.52 | +3.52 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate+library (expect walk) | -6.78 | -6.78 @0 | 'walk' | 'walk<|im_end|>' |
| substrate_pro+library (expect walk) | -11.68 | -11.68 @0 | 'Walk' | 'Walk<|im_end|>' |
