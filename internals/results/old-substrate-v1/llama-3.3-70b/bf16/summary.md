# Llama-3.3-70B-Instruct (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 80 · heads 64 · drive token 'Drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -13.78 | 0.000 | 1.000 | 'Walk<|eot_id|>' |
| substrate | +6.07 | 0.998 | 0.002 | 'Drive<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -3.8 -1.9 -1.8 -1.9 -1.3 -2.2 -2.1 -1.9 -1.4 -1.2 -1.1 -1.8 -2.9 -1.1 -2.8 -3.2 -3.0 -4.4 -4.3 -5.4 -4.7 -6.7 -5.2 -4.1 -4.1 -3.8 -3.8 -2.8 -1.8 -0.9 -0.8 -0.0 -1.8 -2.1 -2.6 -1.9 -2.6 -2.4 -2.3 -1.6 -3.5 -3.2 -2.7 -2.6 -2.0 -2.7 -5.4 -5.5 -5.2 -4.4 -4.5 -5.1 -10.4 -12.3 -12.6 -12.3 -11.5 -11.1 -11.0 -10.0 -10.1 -9.6 -9.3 -7.3 -8.9 -7.2 -5.9 -5.9 -5.9 -8.8 -8.5 -8.9 -9.6 -8.7 -8.2 -8.2 -8.1 -7.3 -8.5 -8.5 -13.7
substrate: -3.8 -2.3 -2.4 -2.2 -1.6 -2.6 -2.6 -2.3 -1.6 -1.8 -1.7 -2.3 -2.9 -1.2 -2.6 -2.9 -3.0 -4.5 -5.1 -5.7 -5.2 -7.1 -6.0 -5.2 -5.2 -4.4 -4.2 -3.0 -2.0 -0.4 -0.1 +0.8 -1.5 -2.0 -3.0 -2.2 -3.0 -3.3 -3.0 -2.2 -3.7 -2.9 -2.5 -2.6 -2.8 -2.9 -4.3 -4.6 -4.0 -3.1 -2.9 +0.7 -3.6 -5.6 -5.4 -4.6 -4.1 -3.0 -3.2 +2.1 +2.0 +2.0 +2.1 +1.9 +0.6 +3.9 +2.6 +2.5 +2.6 -0.6 -0.7 -0.7 -0.5 -0.1 +1.7 +1.5 +2.5 -1.4 -1.5 +2.8 +6.1
final lens row == model logits: base False, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -13.8 -13.9 -13.8 -13.9 -14.0 -13.7 -13.8 -14.0 -13.9 -13.5 -13.9 -13.8 -13.8 -13.5 -13.8 -13.8 -13.8 -13.8 -13.9 -13.8 -13.8 -13.8 -13.4 -13.5 -13.6 -13.5 -13.3 -13.3 -13.4 -13.5 -11.6 -11.6 -10.9 -10.1 -8.5 -7.7 -7.7 -7.5 -2.2 -0.2 -0.2 +0.1 +0.1 +0.1 +0.1 +0.1 +0.1 +0.1 +0.1 -0.1 -0.1 -0.1 -0.3 -0.1 +0.4 +0.4 -0.1 -0.1 +0.1 +0.1 +0.3 +0.3 +0.3 +0.3 +0.1 +0.1 +0.1 +0.1 +0.2 +0.1 -0.0 +0.9 +1.2 +1.3 +1.7 +3.3 +3.8 +5.5 +6.0 +6.1
layers where the patch alone flips baseline to drive: [41, 42, 43, 44, 45, 46, 47, 48, 54, 55, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 72, 73, 74, 75, 76, 77, 78, 79]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -10.72 (model -13.75), sub +6.73 (model +6.50)
top Δ attention layers: L58 +1.50, L50 +1.17, L73 +0.78, L78 +0.77, L75 +0.76
top Δ MLP layers:       L79 +7.81, L78 +3.55, L76 -3.43, L77 +1.06, L62 -1.04
top Δ heads: L58H6 +1.52, L50H38 +1.20, L64H48 +1.03, L75H37 +0.87, L73H38 +0.67, L71H12 +0.55, L75H32 -0.55, L77H47 +0.39

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.805, max layer L6 (0.963)
- hdr_user: mean 0.001, max layer L0 (0.008)
- line1: mean 0.003, max layer L0 (0.043)
- line2: mean 0.003, max layer L0 (0.029)
- hdr_action: mean 0.001, max layer L0 (0.009)
- line3: mean 0.003, max layer L0 (0.043)
- line4: mean 0.002, max layer L0 (0.031)
- line5: mean 0.002, max layer L0 (0.035)
- line6: mean 0.004, max layer L0 (0.067)
- question: mean 0.038, max layer L37 (0.178)
- answer_instr: mean 0.022, max layer L23 (0.130)
- asst_header: mean 0.059, max layer L75 (0.197)
- last: mean 0.026, max layer L78 (0.128)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L75H37 mass 0.04 Δ+0.87, L75H33 mass 0.06 Δ+0.27, L50H38 mass 0.01 Δ+1.20, L38H16 mass 0.17 Δ+0.06, L71H6 mass 0.04 Δ+0.22, L71H12 mass 0.01 Δ+0.55

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -5.22 |
| loo_line2 | +3.10 |
| loo_line3 | +3.81 |
| loo_line4 | +6.59 |
| loo_line5 | +2.33 |
| loo_line6 | -1.79 |
| only_line1 | -7.97 |
| only_line2 | -16.88 |
| only_line3 | -12.51 |
| only_line4 | -15.54 |
| only_line5 | -12.85 |
| only_line6 | -3.30 |
| headers_only | -16.89 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

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
