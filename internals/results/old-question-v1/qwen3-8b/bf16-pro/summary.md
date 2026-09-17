# Qwen3-8B (bf16)

substrate file: substrate_pro.txt

quant: bf16 · layers 36 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -11.25 | 0.000 | 1.000 | 'Walk<|im_end|>' |
| substrate | +6.52 | 0.999 | 0.001 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +2.6 +5.5 +2.4 +2.0 +0.5 +0.5 -1.0 -2.1 -3.1 -1.6 -2.9 -2.6 -0.3 +2.0 +7.6 +2.7 +1.0 +2.2 +1.0 +3.4 +2.9 +3.0 +4.0 +1.9 -2.8 -1.9 -3.5 -5.7 -8.9 -7.6 -17.1 -31.1 -27.4 -18.4 -14.2 -7.3 -11.2
substrate: +2.6 +4.8 +1.8 +1.9 +1.7 +1.6 +0.1 -1.9 -3.8 -2.9 -4.6 -4.6 -1.6 +2.6 +8.3 +4.1 +0.7 +1.0 -1.7 +1.2 +1.6 +3.0 +4.3 +2.0 -0.8 +2.8 +1.3 +0.3 -1.3 -0.8 -4.2 -6.7 -5.2 +5.1 +7.1 +3.4 +6.5
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -11.2 -11.2 -11.0 -11.0 -10.2 -10.0 -10.5 -9.7 -10.2 -10.2 -10.2 -9.5 -10.0 -9.2 -8.7 -8.5 -8.2 -7.7 -8.0 -7.8 -10.0 -7.3 -5.4 +0.7 +2.7 +3.6 +4.6 +4.7 +4.3 +4.4 +4.6 +4.6 +4.8 +5.5 +6.2 +6.5
layers where the patch alone flips baseline to drive: [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -10.96 (model -11.25), sub +6.29 (model +6.25)
top Δ attention layers: L33 +5.50, L32 +2.67, L29 +1.82, L31 +1.06, L35 +1.00
top Δ MLP layers:       L30 +10.01, L34 -5.88, L35 -4.38, L33 -2.99, L32 +2.30
top Δ heads: L33H11 +4.82, L32H0 +1.54, L32H2 +1.36, L34H19 +1.04, L33H30 +1.00, L34H29 -0.98, L34H16 -0.95, L35H26 +0.69

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.451, max layer L9 (0.741)
- hdr_user: mean 0.002, max layer L4 (0.010)
- line1: mean 0.006, max layer L4 (0.021)
- line2: mean 0.036, max layer L4 (0.297)
- hdr_action: mean 0.003, max layer L4 (0.010)
- line3: mean 0.008, max layer L2 (0.034)
- line4: mean 0.006, max layer L1 (0.025)
- line5: mean 0.006, max layer L0 (0.036)
- line6: mean 0.011, max layer L0 (0.048)
- question: mean 0.091, max layer L23 (0.350)
- answer_instr: mean 0.039, max layer L18 (0.142)
- asst_header: mean 0.237, max layer L1 (0.523)
- last: mean 0.091, max layer L6 (0.248)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H11 mass 0.22 Δ+4.82, L32H0 mass 0.12 Δ+1.54, L34H19 mass 0.12 Δ+1.04, L32H2 mass 0.08 Δ+1.36, L26H26 mass 0.28 Δ+0.36, L33H30 mass 0.08 Δ+1.00

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +8.69 |
| loo_line2 | +5.51 |
| loo_line3 | +5.51 |
| loo_line4 | +3.76 |
| loo_line5 | +4.58 |
| loo_line6 | -0.70 |
| loo_line7 | +8.77 |
| loo_line8 | +6.35 |
| loo_line9 | -1.65 |
| only_line1 | -11.22 |
| only_line2 | -8.23 |
| only_line3 | -17.09 |
| only_line4 | -7.34 |
| only_line5 | -5.82 |
| only_line6 | -4.91 |
| only_line7 | -10.44 |
| only_line8 | -7.87 |
| only_line9 | -12.32 |
| headers_only | -14.50 |

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
