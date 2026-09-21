# Llama-3.3-70B-Instruct (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 80 · heads 64 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -13.65 | 0.000 | 1.000 | 'Walk<|eot_id|>' |
| substrate | +15.01 | 1.000 | 0.000 | 'Drive<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -3.8 -1.8 -1.8 -1.9 -1.3 -2.2 -2.0 -1.8 -1.4 -1.2 -1.2 -1.8 -3.0 -1.1 -2.8 -3.2 -3.0 -4.5 -4.2 -5.3 -4.7 -6.7 -5.2 -4.1 -4.1 -3.8 -3.8 -2.8 -1.8 -0.9 -0.9 -0.1 -1.8 -2.1 -2.6 -1.9 -2.6 -2.4 -2.3 -1.6 -3.5 -3.2 -2.7 -2.6 -1.9 -2.6 -5.4 -5.5 -5.1 -4.3 -4.4 -5.0 -10.1 -12.2 -12.4 -12.2 -11.4 -11.1 -10.9 -9.9 -10.1 -9.6 -9.3 -7.2 -8.8 -7.1 -5.9 -5.9 -5.8 -8.7 -8.4 -8.9 -9.5 -8.6 -8.1 -8.1 -8.1 -7.2 -8.4 -8.5 -13.7
substrate: -3.8 -2.2 -2.2 -2.0 -1.4 -2.4 -2.4 -2.0 -1.4 -1.6 -1.5 -2.1 -2.8 -1.3 -2.9 -3.0 -3.1 -4.7 -5.1 -5.8 -5.1 -6.8 -5.6 -5.0 -5.1 -4.3 -4.1 -3.1 -2.1 -0.6 -0.4 +0.5 -1.7 -2.1 -3.3 -3.0 -3.4 -3.3 -3.3 -2.0 -2.7 -2.6 -2.4 -2.5 -2.6 -2.8 -3.4 -3.2 -2.0 -1.5 -1.5 +5.1 +2.8 +2.4 +2.1 +2.3 +2.6 +4.0 +4.1 +10.1 +9.8 +9.4 +9.3 +8.8 +8.9 +11.8 +8.4 +7.8 +7.9 +5.2 +5.0 +5.2 +5.6 +5.7 +6.4 +6.1 +7.4 +3.1 +3.1 +8.7 +15.0
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -13.7 -13.7 -13.7 -13.7 -13.8 -13.7 -14.0 -13.7 -13.7 -13.5 -13.7 -13.7 -13.7 -13.7 -13.7 -13.5 -13.4 -13.4 -13.7 -13.5 -13.7 -13.5 -13.4 -13.4 -13.4 -13.2 -13.1 -13.0 -13.1 -13.0 -11.5 -11.3 -10.8 -9.1 -7.8 -3.8 -3.5 -1.3 +6.3 +7.7 +8.0 +7.8 +7.8 +7.8 +7.7 +8.0 +8.0 +7.8 +8.0 +7.8 +7.9 +8.0 +7.8 +8.0 +8.1 +8.3 +8.3 +8.3 +8.3 +8.3 +8.6 +8.5 +8.6 +8.6 +8.6 +8.6 +8.7 +8.7 +8.7 +8.7 +8.7 +9.3 +9.4 +9.4 +9.8 +11.6 +12.3 +14.0 +15.0 +15.0
layers where the patch alone flips baseline to drive: [38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -13.69 (model -13.62), sub +15.21 (model +15.12)
top Δ attention layers: L50 +1.85, L58 +1.69, L75 +1.60, L78 +1.27, L71 +1.05
top Δ MLP layers:       L79 +11.47, L78 +5.25, L76 -3.67, L65 -2.05, L77 +1.85
top Δ heads: L50H38 +1.87, L58H6 +1.72, L75H37 +1.53, L75H32 -1.00, L64H48 +0.96, L73H34 -0.85, L51H30 +0.82, L77H47 +0.79

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.804, max layer L6 (0.961)
- hdr_user: mean 0.001, max layer L0 (0.007)
- line1: mean 0.002, max layer L0 (0.026)
- line2: mean 0.002, max layer L0 (0.027)
- line3: mean 0.002, max layer L0 (0.029)
- line4: mean 0.001, max layer L0 (0.023)
- line5: mean 0.002, max layer L0 (0.032)
- line6: mean 0.001, max layer L0 (0.014)
- question: mean 0.035, max layer L37 (0.147)
- answer_instr: mean 0.023, max layer L23 (0.131)
- asst_header: mean 0.060, max layer L78 (0.195)
- last: mean 0.026, max layer L78 (0.129)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L75H37 mass 0.04 Δ+1.53, L50H38 mass 0.01 Δ+1.87, L75H33 mass 0.05 Δ+0.48, L51H30 mass 0.02 Δ+0.82, L39H11 mass 0.09 Δ+0.16, L71H6 mass 0.05 Δ+0.26

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +13.36 |
| loo_line2 | +14.02 |
| loo_line3 | +13.65 |
| loo_line4 | +14.48 |
| loo_line5 | +14.36 |
| loo_line6 | +14.40 |
| loo_line7 | +16.38 |
| loo_line8 | +13.95 |
| loo_line9 | +15.59 |
| only_line1 | -13.65 |
| only_line2 | -15.10 |
| only_line3 | -10.39 |
| only_line4 | -11.64 |
| only_line5 | -7.57 |
| only_line6 | -4.24 |
| only_line7 | -7.32 |
| only_line8 | +6.87 |
| only_line9 | -3.59 |
| headers_only | -14.92 |

line1: - Perform an activity on an object at a service location.
line2: - No other objectives or goals are relevant for the user.
line3: - The object is initially with the user at the same location.
line4: - The activity is performed at the service location.
line5: - The object must be at the service location for the activity performance.
line6: - Vehicles are not portable.
line7: - Walking leaves a vehicle behind.
line8: - Walking does not transport a vehicle.
line9: - To transport a vehicle from one location to another, the user must operate it.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | -13.65 | -13.65 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_CoT | -18.21 | -18.21 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_encourage | -14.84 | -14.84 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_expert | -5.51 | -5.51 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_goaloriented | -4.67 | -4.67 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_hallucination | -13.92 | -13.92 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_nomistakes | -13.87 | -13.87 @0 | 'walk' | 'walk<|eot_id|>' |
| benchmark_threat | -14.86 | -14.86 @0 | 'Walk' | 'Walk<|eot_id|>' |
| benchmark_urgency | -12.15 | -12.15 @0 | 'Walk' | 'Walk<|eot_id|>' |
| substrate | +15.01 | +15.01 @0 | 'Drive' | 'Drive<|eot_id|>' |
