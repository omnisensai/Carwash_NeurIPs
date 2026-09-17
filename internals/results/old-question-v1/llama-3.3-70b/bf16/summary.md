# Llama-3.3-70B-Instruct (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 80 · heads 64 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -14.00 | 0.000 | 1.000 | 'Walk.<|eot_id|>' |
| substrate | +6.75 | 0.999 | 0.001 | 'Drive.<|eot_id|>' |

## logit lens (M per layer, emb first)
baseline:  -3.8 -2.0 -1.9 -2.3 -1.5 -2.4 -2.2 -2.1 -1.4 -1.0 -0.8 -1.6 -3.0 -1.4 -3.4 -4.1 -2.8 -3.8 -3.7 -4.5 -3.6 -5.7 -4.0 -2.7 -4.2 -3.8 -4.0 -4.2 -2.9 -2.1 -2.3 -1.6 -2.5 -2.9 -2.8 -2.9 -3.2 -2.5 -1.9 -1.3 -3.3 -3.4 -3.1 -3.0 -2.5 -2.7 -6.8 -7.1 -7.3 -5.7 -5.8 -4.6 -7.2 -10.5 -10.3 -10.0 -9.6 -9.6 -9.5 -10.5 -10.4 -10.2 -10.1 -7.8 -6.4 -5.1 -4.4 -4.5 -3.9 -5.3 -5.2 -5.8 -6.9 -6.3 -5.7 -5.4 -6.0 -8.0 -9.1 -10.3 -14.0
substrate: -3.8 -2.4 -2.5 -2.6 -1.9 -2.7 -2.7 -2.5 -1.6 -1.6 -1.4 -2.2 -3.1 -1.5 -3.4 -4.0 -3.0 -3.9 -4.6 -4.8 -3.9 -5.9 -4.4 -3.2 -4.7 -4.0 -4.1 -4.3 -2.8 -2.2 -1.8 -0.7 -2.0 -2.8 -3.1 -2.8 -3.3 -2.4 -1.5 -0.8 -1.9 -1.6 -0.5 -1.0 -1.0 -1.1 -3.1 -3.7 -3.4 -2.0 -1.9 +3.4 +1.8 -1.1 -1.2 -0.9 -0.7 -0.2 -0.7 +0.1 +0.2 +0.3 +0.2 +0.3 +1.7 +3.9 +2.5 +2.4 +3.1 +1.8 +1.7 +1.8 +2.0 +2.6 +3.7 +3.2 +4.4 +0.1 +0.0 +4.0 +6.6
final lens row == model logits: base True, sub False

## patching (substrate residual into baseline at the answer position)
M per layer: -14.0 -14.0 -14.0 -14.0 -14.0 -14.0 -14.0 -13.9 -14.0 -14.0 -13.9 -13.9 -13.9 -13.9 -13.9 -13.9 -13.7 -14.0 -13.7 -13.9 -13.9 -13.9 -13.6 -13.7 -13.6 -13.5 -13.0 -12.7 -12.9 -12.7 -12.0 -12.1 -12.0 -11.7 -11.2 -10.9 -11.1 -10.7 -6.5 -4.5 -4.2 -4.0 -4.0 -4.0 -4.0 -3.7 -3.7 -4.0 -3.7 -4.0 -3.7 -3.7 -3.6 -3.5 -3.5 -3.2 -3.1 -3.2 -3.1 -3.0 -3.0 -3.1 -3.1 -3.1 -3.0 -3.0 -3.2 -3.2 -3.5 -3.5 -3.2 -2.0 -2.0 -1.7 -0.2 +2.7 +3.5 +5.6 +6.4 +6.7
layers where the patch alone flips baseline to drive: [75, 76, 77, 78, 79]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -14.08 (model -14.00), sub +6.68 (model +6.75)
top Δ attention layers: L78 +1.33, L50 +1.16, L71 +1.08, L75 +0.99, L58 +0.88
top Δ MLP layers:       L79 +7.60, L78 +4.16, L77 +1.20, L76 -1.04, L62 -0.93
top Δ heads: L50H38 +1.20, L75H37 +1.04, L58H6 +0.87, L78H30 +0.63, L75H32 -0.61, L71H12 +0.59, L64H48 +0.56, L77H47 +0.56

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.813, max layer L6 (0.963)
- hdr_user: mean 0.001, max layer L0 (0.008)
- line1: mean 0.003, max layer L0 (0.044)
- line2: mean 0.003, max layer L0 (0.029)
- hdr_action: mean 0.001, max layer L0 (0.009)
- line3: mean 0.003, max layer L0 (0.044)
- line4: mean 0.002, max layer L0 (0.032)
- line5: mean 0.003, max layer L0 (0.036)
- line6: mean 0.005, max layer L0 (0.068)
- question: mean 0.048, max layer L35 (0.202)
- answer_instr: mean 0.029, max layer L23 (0.158)
- asst_header: mean 0.062, max layer L75 (0.242)
- last: mean 0.024, max layer L78 (0.101)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L75H37 mass 0.03 Δ+1.04, L50H38 mass 0.02 Δ+1.20, L75H33 mass 0.06 Δ+0.32, L78H1 mass 0.07 Δ+0.23, L75H34 mass 0.04 Δ+0.35, L56H34 mass 0.04 Δ+0.22

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -6.00 |
| loo_line2 | +5.50 |
| loo_line3 | +5.50 |
| loo_line4 | +8.00 |
| loo_line5 | +2.75 |
| loo_line6 | +0.00 |
| only_line1 | -6.25 |
| only_line2 | -15.75 |
| only_line3 | -12.50 |
| only_line4 | -14.50 |
| only_line5 | -12.87 |
| only_line6 | -6.25 |
| headers_only | -16.37 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

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
