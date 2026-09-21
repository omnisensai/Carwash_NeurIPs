# Qwen3-8B

substrate file: substrate.txt

quant: bf16 · layers 36 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -14.40 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | +10.75 | 1.000 | 0.000 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +2.6 +5.6 +2.6 +2.1 +0.4 +1.0 -0.7 -2.1 -3.0 -1.8 -2.5 -2.8 -0.1 +2.7 +7.8 +3.0 +0.9 +2.7 +1.5 +4.0 +3.1 +3.9 +4.0 +3.2 -1.7 -3.8 -3.0 -4.2 -6.4 -6.0 -11.7 -17.0 -21.2 -14.3 -15.6 -8.8 -14.4
substrate: +2.6 +5.3 +2.6 +2.3 +1.0 +1.6 +0.2 -1.4 -3.3 -2.6 -4.3 -3.9 -1.2 +1.9 +7.5 +3.2 +0.4 +1.8 -0.5 +2.2 +1.8 +2.5 +4.5 +3.2 -1.0 +1.4 +0.4 +0.2 -0.9 -0.9 +1.0 +2.1 +0.7 +11.6 +14.0 +5.8 +10.7
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -14.0 -14.0 -14.4 -14.2 -14.0 -13.5 -13.7 -13.5 -13.2 -13.6 -13.4 -13.1 -12.4 -12.9 -13.2 -13.5 -12.7 -12.5 -12.7 -12.7 -11.7 -8.5 -6.0 +4.5 +6.2 +6.5 +8.2 +8.5 +8.8 +9.2 +9.0 +8.8 +9.0 +9.2 +9.8 +10.7
layers where the patch alone flips baseline to drive: [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -14.75 (model -14.75), sub +10.91 (model +10.75)
top Δ attention layers: L33 +13.21, L32 +6.27, L29 +3.75, L31 +3.66, L34 +2.36
top Δ MLP layers:       L34 -12.18, L35 -8.09, L30 +6.00, L32 +2.15, L29 +1.87
top Δ heads: L33H11 +10.19, L32H2 +3.47, L32H0 +3.05, L31H15 +2.24, L33H30 +1.82, L34H19 +1.63, L33H23 +1.41, L35H26 +1.31

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.467, max layer L30 (0.778)
- hdr_user: mean 0.005, max layer L4 (0.026)
- line1: mean 0.035, max layer L4 (0.221)
- line2: mean 0.028, max layer L4 (0.170)
- hdr_action: mean 0.005, max layer L4 (0.016)
- line3: mean 0.010, max layer L0 (0.045)
- line4: mean 0.007, max layer L0 (0.036)
- line5: mean 0.008, max layer L1 (0.038)
- line6: mean 0.014, max layer L0 (0.074)
- question: mean 0.066, max layer L23 (0.212)
- answer_instr: mean 0.033, max layer L18 (0.132)
- asst_header: mean 0.238, max layer L1 (0.530)
- last: mean 0.094, max layer L6 (0.257)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H11 mass 0.07 Δ+10.19, L34H19 mass 0.12 Δ+1.63, L29H27 mass 0.11 Δ+1.18, L32H0 mass 0.04 Δ+3.05, L34H21 mass 0.11 Δ+0.68, L26H26 mass 0.17 Δ+0.40

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +7.00 |
| loo_line2 | +8.50 |
| loo_line3 | +11.75 |
| loo_line4 | +8.50 |
| loo_line5 | +7.75 |
| loo_line6 | -3.75 |
| only_line1 | -16.50 |
| only_line2 | -15.75 |
| only_line3 | -14.25 |
| only_line4 | -12.75 |
| only_line5 | -10.00 |
| only_line6 | +0.75 |
| headers_only | -14.24 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | -14.40 | -14.40 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -9.50 | -9.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | -10.00 | -10.00 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -8.00 | -8.00 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_hallucination | -14.00 | -14.00 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_library | -14.00 | -14.00 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | -13.50 | -13.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_threat | -7.50 | -7.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | -3.25 | -3.25 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate | +10.75 | +10.75 @0 | 'drive' | 'drive<|im_end|>' |
| substrate_pro | +15.75 | +15.75 @0 | 'drive' | 'drive<|im_end|>' |
| substrate+library (expect walk) | -11.65 | -11.65 @0 | 'Walk' | 'Walk<|im_end|>' |
| substrate_pro+library (expect walk) | -16.65 | -16.65 @0 | 'walk' | 'walk<|im_end|>' |
