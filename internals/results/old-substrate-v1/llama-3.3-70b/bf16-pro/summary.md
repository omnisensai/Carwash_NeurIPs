# Llama-3.3-70B-Instruct (bf16), substrate_pro.txt

substrate file: substrate_pro.txt

quant: bf16 · layers 80 · heads 64 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -13.78 | 0.000 | 1.000 | 'Walk<|eot_id|>' |
| substrate | +17.00 | 1.000 | 0.000 | 'Drive<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -3.8 -1.9 -1.8 -1.9 -1.3 -2.2 -2.1 -1.9 -1.4 -1.2 -1.1 -1.8 -2.9 -1.1 -2.8 -3.2 -3.0 -4.4 -4.3 -5.4 -4.7 -6.7 -5.2 -4.1 -4.1 -3.8 -3.8 -2.8 -1.8 -0.9 -0.8 -0.0 -1.8 -2.1 -2.6 -1.9 -2.6 -2.4 -2.3 -1.6 -3.5 -3.2 -2.7 -2.6 -2.0 -2.7 -5.4 -5.5 -5.2 -4.4 -4.5 -5.1 -10.4 -12.3 -12.6 -12.3 -11.5 -11.1 -11.0 -10.0 -10.1 -9.6 -9.3 -7.3 -8.9 -7.2 -5.9 -5.9 -5.9 -8.8 -8.5 -8.9 -9.6 -8.7 -8.2 -8.2 -8.1 -7.3 -8.5 -8.5 -13.7
substrate: -3.8 -2.5 -2.5 -2.3 -1.7 -2.6 -2.5 -2.1 -1.5 -1.8 -1.7 -2.4 -2.9 -1.3 -3.0 -2.9 -3.1 -4.6 -5.1 -5.8 -5.2 -6.8 -5.5 -5.1 -5.0 -4.1 -3.8 -2.7 -1.7 +0.0 +0.0 +0.7 -1.9 -2.1 -3.2 -2.5 -3.3 -2.9 -2.8 -1.2 -1.7 -1.6 -1.7 -1.8 -2.2 -2.4 -2.9 -2.7 -1.7 -1.3 -1.4 +5.2 +3.8 +3.5 +3.1 +3.4 +3.7 +4.9 +5.0 +11.1 +10.5 +10.1 +9.9 +9.3 +9.6 +13.6 +9.4 +8.8 +9.1 +6.6 +6.5 +6.8 +7.2 +7.4 +8.3 +7.9 +8.9 +4.2 +4.5 +9.6 +17.0
final lens row == model logits: base False, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -13.8 -14.0 -14.0 -14.0 -13.9 -13.8 -13.5 -13.7 -13.8 -13.8 -13.8 -13.5 -13.8 -13.8 -13.7 -13.5 -13.8 -13.7 -13.8 -13.5 -13.5 -13.4 -13.4 -13.2 -13.3 -13.3 -13.2 -12.9 -13.3 -13.1 -11.5 -11.5 -10.8 -9.5 -6.8 -2.6 -2.1 +0.9 +7.8 +9.2 +9.2 +9.0 +9.2 +9.3 +9.2 +9.2 +9.2 +9.3 +9.5 +9.2 +9.2 +9.4 +9.2 +9.0 +9.5 +9.7 +9.5 +9.4 +9.7 +9.5 +9.7 +9.5 +9.6 +9.6 +9.7 +9.7 +9.7 +10.2 +10.0 +9.7 +9.8 +10.4 +10.4 +10.6 +10.9 +13.0 +14.0 +16.0 +17.0 +17.0
layers where the patch alone flips baseline to drive: [37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -13.81 (model -13.75), sub +17.31 (model +17.25)
top Δ attention layers: L50 +1.90, L58 +1.69, L75 +1.55, L51 +1.23, L78 +1.22
top Δ MLP layers:       L79 +12.47, L78 +5.26, L76 -3.73, L65 -2.38, L77 +2.13
top Δ heads: L50H38 +1.94, L58H6 +1.71, L75H37 +1.58, L64H48 +1.34, L75H32 -1.06, L51H30 +1.02, L77H47 +0.84, L73H38 +0.84

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.800, max layer L6 (0.961)
- hdr_user: mean 0.000, max layer L0 (0.006)
- line1: mean 0.001, max layer L0 (0.022)
- line2: mean 0.002, max layer L0 (0.028)
- hdr_action: mean 0.001, max layer L0 (0.007)
- line3: mean 0.002, max layer L0 (0.022)
- line4: mean 0.001, max layer L0 (0.022)
- line5: mean 0.002, max layer L0 (0.040)
- line6: mean 0.003, max layer L0 (0.040)
- question: mean 0.036, max layer L37 (0.152)
- answer_instr: mean 0.022, max layer L23 (0.130)
- asst_header: mean 0.059, max layer L78 (0.192)
- last: mean 0.026, max layer L78 (0.126)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L75H37 mass 0.05 Δ+1.58, L50H38 mass 0.02 Δ+1.94, L51H30 mass 0.03 Δ+1.02, L75H33 mass 0.05 Δ+0.47, L71H4 mass 0.04 Δ+0.47, L71H6 mass 0.05 Δ+0.33

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +16.43 |
| loo_line2 | +16.60 |
| loo_line3 | +16.51 |
| loo_line4 | +17.50 |
| loo_line5 | +16.88 |
| loo_line6 | +15.82 |
| loo_line7 | +16.43 |
| loo_line8 | +17.73 |
| loo_line9 | +17.63 |
| only_line1 | -10.30 |
| only_line2 | -3.80 |
| only_line3 | -13.61 |
| only_line4 | -10.91 |
| only_line5 | -5.51 |
| only_line6 | +9.28 |
| only_line7 | -11.06 |
| only_line8 | -11.80 |
| only_line9 | -9.91 |
| headers_only | -13.98 |

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
| baseline | -13.78 | -13.78 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_CoT | -15.75 | -15.75 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_encourage | -14.50 | -14.50 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_expert | -3.50 | -3.50 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_hallucination | -12.00 | -12.00 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_library | -18.75 | -18.75 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_nomistakes | -12.50 | -12.50 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_threat | -14.25 | -14.25 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| benchmark_urgency | -11.87 | -11.87 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate | +6.07 | +6.07 @0 | 'Drive' | 'Drive<|eot_id|>' |
| substrate_pro | +17.00 | +17.00 @0 | 'Drive' | 'Drive<|eot_id|>' |
| substrate+library (expect walk) | -18.37 | -18.37 @0 | 'Walk' | 'Walk.<|eot_id|>' |
| substrate_pro+library (expect walk) | -17.75 | -17.75 @0 | 'Walk' | 'Walk.<|eot_id|>' |
