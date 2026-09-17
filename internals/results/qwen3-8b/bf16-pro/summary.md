# Qwen3-8B

substrate file: substrate_pro.txt

quant: bf16 · layers 36 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -14.40 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | +15.75 | 1.000 | 0.000 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +2.6 +5.6 +2.6 +2.1 +0.4 +1.0 -0.7 -2.1 -3.0 -1.8 -2.5 -2.8 -0.1 +2.7 +7.8 +3.0 +0.9 +2.7 +1.5 +4.0 +3.1 +3.9 +4.0 +3.2 -1.7 -3.8 -3.0 -4.2 -6.4 -6.0 -11.7 -17.0 -21.2 -14.3 -15.6 -8.8 -14.4
substrate: +2.6 +5.1 +2.4 +2.3 +1.7 +1.8 +0.3 -1.8 -3.9 -2.8 -4.6 -4.6 -1.8 +2.3 +8.3 +4.2 +0.5 +0.9 -1.2 +1.7 +1.7 +3.0 +4.4 +3.2 -1.3 +1.6 +0.9 +1.4 -0.0 -0.1 +1.9 +2.7 +1.2 +11.9 +15.2 +7.7 +15.7
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -14.2 -14.1 -14.1 -13.7 -13.2 -13.5 -13.2 -12.7 -13.2 -12.7 -12.7 -12.0 -12.6 -13.6 -13.7 -14.2 -13.9 -13.5 -14.0 -14.2 -14.5 -11.7 -10.5 +6.5 +8.7 +10.2 +12.5 +12.2 +13.0 +13.2 +13.2 +13.2 +13.0 +14.0 +14.5 +15.7
layers where the patch alone flips baseline to drive: [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -14.75 (model -14.75), sub +15.80 (model +15.75)
top Δ attention layers: L33 +14.60, L32 +6.73, L31 +4.04, L29 +3.75, L34 +1.75
top Δ MLP layers:       L34 -9.58, L35 -7.56, L30 +5.87, L29 +2.10, L32 +1.62
top Δ heads: L33H11 +9.47, L32H2 +3.77, L33H23 +3.63, L32H0 +3.23, L31H15 +2.80, L33H30 +1.81, L35H26 +1.60, L34H19 +1.41

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.460, max layer L30 (0.781)
- hdr_user: mean 0.003, max layer L4 (0.011)
- line1: mean 0.005, max layer L4 (0.021)
- line2: mean 0.036, max layer L4 (0.297)
- hdr_action: mean 0.003, max layer L4 (0.009)
- line3: mean 0.009, max layer L2 (0.036)
- line4: mean 0.006, max layer L1 (0.026)
- line5: mean 0.006, max layer L0 (0.036)
- line6: mean 0.009, max layer L0 (0.048)
- question: mean 0.059, max layer L23 (0.191)
- answer_instr: mean 0.033, max layer L18 (0.126)
- asst_header: mean 0.235, max layer L1 (0.508)
- last: mean 0.092, max layer L6 (0.244)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H11 mass 0.15 Δ+9.47, L33H23 mass 0.10 Δ+3.63, L32H0 mass 0.07 Δ+3.23, L31H15 mass 0.06 Δ+2.80, L34H19 mass 0.11 Δ+1.41, L32H2 mass 0.04 Δ+3.77

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +15.75 |
| loo_line2 | +14.50 |
| loo_line3 | +13.50 |
| loo_line4 | +12.75 |
| loo_line5 | +13.50 |
| loo_line6 | +11.00 |
| loo_line7 | +14.25 |
| loo_line8 | +15.75 |
| loo_line9 | +8.50 |
| only_line1 | -8.50 |
| only_line2 | -5.50 |
| only_line3 | -11.25 |
| only_line4 | -2.00 |
| only_line5 | -3.00 |
| only_line6 | +2.00 |
| only_line7 | -2.00 |
| only_line8 | -5.00 |
| only_line9 | -9.50 |
| headers_only | -9.75 |

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
