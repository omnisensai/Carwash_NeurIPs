# Qwen2.5-3B-Instruct (bf16)

substrate file: substrate_pro.txt

quant: bf16 · layers 36 · heads 16 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +9.00 | 1.000 | 0.000 | 'Drive.<|im_end|>' |
| substrate | +17.00 | 1.000 | 0.000 | 'Drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan -7.0 -0.7 -3.0 -2.4 -4.5 -5.6 -4.1 -5.4 -4.1 -1.4 -4.6 -5.5 +0.2 -2.6 -1.6 -3.2 +0.8 -0.3 -1.0 +1.0 +0.4 -0.2 +0.2 +1.0 +0.4 +2.4 +2.4 +4.0 +3.3 +3.4 -0.2 +10.3 +6.8 +8.1 +7.5 +9.0
substrate: +nan -7.8 -1.6 -4.1 -4.7 -7.3 -7.4 -5.6 -6.6 -4.2 -2.3 -5.5 -6.4 +0.8 -1.6 -1.0 -2.9 +0.7 -0.6 -1.4 +1.1 +0.4 +1.1 +1.4 +2.7 +1.9 +4.8 +3.0 +4.0 +3.4 +4.9 +2.8 +12.2 +13.4 +14.5 +10.8 +17.0
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +8.8 +9.0 +9.5 +9.3 +9.3 +9.3 +9.3 +9.3 +9.3 +9.0 +8.8 +8.8 +8.3 +8.5 +8.5 +9.0 +8.5 +8.5 +9.4 +8.5 +8.3 +9.3 +9.3 +11.0 +10.7 +11.2 +14.0 +13.1 +13.1 +12.2 +13.4 +14.5 +16.1 +16.9 +17.0 +17.0
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +9.06 (model +9.00), sub +17.03 (model +17.00)
top Δ attention layers: L32 +3.22, L33 +2.37, L27 +0.32, L26 -0.26, L31 -0.26
top Δ MLP layers:       L32 +1.74, L34 -1.44, L35 +1.28, L30 +1.13, L29 +0.92
top Δ heads: L33H0 +2.77, L32H9 +1.80, L32H7 +1.21, L33H14 -0.56, L34H8 -0.53, L33H15 +0.51, L34H14 +0.46, L31H3 -0.44

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.317, max layer L5 (0.727)
- hdr_user: mean 0.003, max layer L8 (0.010)
- line1: mean 0.006, max layer L35 (0.018)
- line2: mean 0.005, max layer L0 (0.021)
- hdr_action: mean 0.004, max layer L8 (0.014)
- line3: mean 0.007, max layer L0 (0.021)
- line4: mean 0.005, max layer L0 (0.019)
- line5: mean 0.007, max layer L0 (0.045)
- line6: mean 0.011, max layer L0 (0.047)
- question: mean 0.174, max layer L26 (0.502)
- answer_instr: mean 0.068, max layer L16 (0.260)
- asst_header: mean 0.207, max layer L2 (0.571)
- last: mean 0.110, max layer L0 (0.244)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H0 mass 0.09 Δ+2.77, L32H9 mass 0.08 Δ+1.80, L33H15 mass 0.09 Δ+0.51, L28H10 mass 0.29 Δ+0.11, L32H7 mass 0.03 Δ+1.21, L24H4 mass 0.36 Δ+0.09

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +18.50 |
| loo_line2 | +16.25 |
| loo_line3 | +16.38 |
| loo_line4 | +17.75 |
| loo_line5 | +14.13 |
| loo_line6 | +15.25 |
| loo_line7 | +16.00 |
| loo_line8 | +17.12 |
| loo_line9 | +13.37 |
| only_line1 | +13.25 |
| only_line2 | +16.37 |
| only_line3 | +14.38 |
| only_line4 | +18.50 |
| only_line5 | +15.48 |
| only_line6 | +19.75 |
| only_line7 | +18.75 |
| only_line8 | +17.19 |
| only_line9 | +19.87 |
| headers_only | +14.62 |

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
| baseline | +9.00 | +9.00 @0 | 'Drive' | 'Drive.<|im_end|>' |
| benchmark_CoT | +8.75 | +8.75 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | +9.86 | +9.86 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_expert | +10.25 | +10.25 @0 | 'Drive' | 'Drive.<|im_end|>' |
| benchmark_hallucination | +9.51 | +9.51 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_library | -4.75 | -4.75 @0 | 'Walk' | 'Walk.<|im_end|>' |
| benchmark_nomistakes | +7.10 | +7.10 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_threat | +9.48 | +9.48 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_urgency | +8.04 | +8.04 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate | +14.25 | +14.25 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate_pro | +17.00 | +17.00 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate+library (expect walk) | +4.02 | +4.02 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate_pro+library (expect walk) | -9.50 | -9.50 @0 | 'Walk' | 'Walk<|im_end|>' |
