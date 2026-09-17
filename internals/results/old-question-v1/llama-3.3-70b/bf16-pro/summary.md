# Llama-3.3-70B-Instruct (bf16), substrate_pro.txt

substrate file: substrate_pro.txt

quant: bf16 · layers 80 · heads 64 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -14.00 | 0.000 | 1.000 | 'Walk.<|eot_id|>' |
| substrate | +16.00 | 1.000 | 0.000 | 'Drive.<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -3.8 -2.0 -1.9 -2.3 -1.5 -2.4 -2.2 -2.1 -1.4 -1.0 -0.8 -1.6 -3.0 -1.4 -3.4 -4.1 -2.8 -3.8 -3.7 -4.5 -3.6 -5.7 -4.0 -2.7 -4.2 -3.8 -4.0 -4.2 -2.9 -2.1 -2.3 -1.6 -2.5 -2.9 -2.8 -2.9 -3.2 -2.5 -1.9 -1.3 -3.3 -3.4 -3.1 -3.0 -2.5 -2.7 -6.8 -7.1 -7.3 -5.7 -5.8 -4.6 -7.2 -10.5 -10.3 -10.0 -9.6 -9.6 -9.5 -10.5 -10.4 -10.2 -10.1 -7.8 -6.4 -5.1 -4.4 -4.5 -3.9 -5.3 -5.2 -5.8 -6.9 -6.3 -5.7 -5.4 -6.0 -8.0 -9.1 -10.3 -14.0
substrate: -3.8 -2.5 -2.6 -2.5 -1.8 -2.5 -2.5 -2.2 -1.4 -1.4 -1.2 -2.3 -3.2 -1.7 -3.7 -4.0 -3.1 -4.0 -4.6 -4.7 -3.9 -5.7 -4.3 -3.3 -4.4 -3.7 -3.7 -4.0 -2.5 -1.7 -1.4 -0.5 -2.1 -2.6 -3.1 -2.8 -3.0 -2.2 -1.2 -0.3 -0.7 -0.8 +0.3 +0.0 +0.1 -0.1 -0.6 -0.6 +0.1 +0.8 +0.9 +8.5 +7.6 +6.3 +5.9 +6.0 +6.3 +6.5 +6.3 +7.6 +7.6 +7.6 +7.0 +6.6 +7.5 +10.4 +7.3 +6.9 +7.6 +6.3 +6.1 +6.2 +6.9 +7.6 +9.1 +8.4 +9.3 +5.6 +6.1 +11.3 +16.0
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -14.0 -14.0 -14.0 -14.0 -14.0 -14.0 -14.0 -14.0 -14.0 -14.0 -14.0 -14.0 -14.1 -14.0 -13.9 -13.7 -13.7 -13.7 -13.5 -13.9 -13.7 -13.7 -13.5 -13.4 -13.4 -13.6 -13.0 -12.9 -12.9 -12.7 -11.6 -11.7 -11.4 -11.2 -10.4 -8.9 -9.1 -6.6 -1.0 +1.0 +1.0 +1.3 +1.5 +1.5 +1.5 +1.8 +2.0 +2.0 +2.3 +1.8 +2.3 +2.0 +2.4 +2.4 +2.5 +2.8 +2.9 +2.6 +3.0 +3.3 +3.0 +3.3 +3.1 +3.0 +3.3 +3.3 +3.0 +3.0 +3.0 +3.0 +3.0 +4.7 +4.9 +5.4 +6.9 +10.7 +11.7 +13.9 +15.1 +16.0
layers where the patch alone flips baseline to drive: [39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -14.08 (model -14.00), sub +15.87 (model +16.00)
top Δ attention layers: L78 +1.62, L50 +1.54, L71 +1.45, L75 +1.33, L58 +0.98
top Δ MLP layers:       L79 +10.21, L78 +5.94, L77 +1.71, L65 -1.42, L62 -1.04
top Δ heads: L50H38 +1.59, L75H37 +1.31, L75H32 -1.05, L58H6 +0.98, L78H30 +0.76, L71H12 +0.76, L77H47 +0.72, L64H48 +0.65

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.803, max layer L6 (0.962)
- hdr_user: mean 0.001, max layer L0 (0.006)
- line1: mean 0.002, max layer L0 (0.022)
- line2: mean 0.002, max layer L0 (0.027)
- hdr_action: mean 0.001, max layer L0 (0.007)
- line3: mean 0.002, max layer L0 (0.023)
- line4: mean 0.002, max layer L0 (0.022)
- line5: mean 0.002, max layer L0 (0.040)
- line6: mean 0.004, max layer L0 (0.040)
- question: mean 0.048, max layer L35 (0.187)
- answer_instr: mean 0.030, max layer L23 (0.158)
- asst_header: mean 0.061, max layer L75 (0.229)
- last: mean 0.025, max layer L78 (0.114)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L75H37 mass 0.06 Δ+1.31, L50H38 mass 0.04 Δ+1.59, L59H35 mass 0.09 Δ+0.40, L75H33 mass 0.08 Δ+0.44, L56H34 mass 0.11 Δ+0.28, L71H4 mass 0.06 Δ+0.51

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +14.62 |
| loo_line2 | +15.12 |
| loo_line3 | +15.12 |
| loo_line4 | +16.12 |
| loo_line5 | +15.37 |
| loo_line6 | +15.25 |
| loo_line7 | +14.12 |
| loo_line8 | +16.50 |
| loo_line9 | +16.62 |
| only_line1 | -10.87 |
| only_line2 | -4.50 |
| only_line3 | -12.37 |
| only_line4 | -10.50 |
| only_line5 | -6.25 |
| only_line6 | +8.62 |
| only_line7 | -10.75 |
| only_line8 | -11.50 |
| only_line9 | -9.00 |
| headers_only | -12.62 |

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
| baseline | -14.00 | -14.00 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_CoT | -15.75 | -15.75 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_encourage | -14.50 | -14.50 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_expert | -3.50 | -3.50 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_hallucination | -12.00 | -12.00 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_library | -18.75 | -18.75 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_nomistakes | -12.50 | -12.50 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_threat | -14.25 | -14.25 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_urgency | -11.87 | -11.87 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate | +6.75 | +6.75 @0 | 'Drive' | 'Drive.<|eot_id|>' |
| substrate_pro | +16.00 | +16.00 @0 | 'Drive' | 'Drive.<|eot_id|>' |
| substrate+library (expect walk) | -18.37 | -18.37 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate_pro+library (expect walk) | -17.75 | -17.75 @0 | 'Walk' | 'Walk.<|eot_id|>' |
