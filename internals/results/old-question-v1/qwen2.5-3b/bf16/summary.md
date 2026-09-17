# Qwen2.5-3B-Instruct (bf16)

substrate file: substrate.txt

quant: bf16 · layers 36 · heads 16 · drive token 'Drive' · walk token 'Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +9.00 | 1.000 | 0.000 | 'Drive.<|im_end|>' |
| substrate | +14.25 | 1.000 | 0.000 | 'Drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan -7.0 -0.7 -3.0 -2.4 -4.5 -5.6 -4.1 -5.4 -4.1 -1.4 -4.6 -5.5 +0.2 -2.6 -1.6 -3.2 +0.8 -0.3 -1.0 +1.0 +0.4 -0.2 +0.2 +1.0 +0.4 +2.4 +2.4 +4.0 +3.3 +3.4 -0.2 +10.3 +6.8 +8.1 +7.5 +9.0
substrate: +nan -7.4 -1.1 -3.5 -3.7 -6.2 -6.8 -4.3 -5.6 -3.0 -0.7 -4.4 -5.8 +0.7 -1.6 -0.9 -2.6 +0.7 -0.1 -1.1 +1.0 +0.1 +0.8 +0.7 +2.2 +1.5 +3.7 +1.9 +3.8 +3.4 +4.2 +1.6 +11.0 +11.7 +12.4 +9.8 +14.3
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +9.0 +9.0 +9.0 +9.0 +9.0 +9.3 +9.3 +9.3 +8.5 +8.5 +8.8 +8.5 +8.3 +8.5 +8.8 +8.3 +8.4 +8.1 +8.4 +8.6 +7.9 +9.0 +8.5 +10.0 +10.5 +10.5 +12.9 +13.3 +13.9 +13.9 +13.9 +13.8 +14.4 +14.1 +14.3 +14.3
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +9.06 (model +9.00), sub +14.21 (model +14.25)
top Δ attention layers: L32 +2.91, L33 +1.97, L12 -0.27, L28 +0.21, L20 -0.21
top Δ MLP layers:       L32 +1.33, L34 -1.06, L31 -0.93, L30 +0.70, L33 -0.46
top Δ heads: L33H0 +2.28, L32H9 +1.86, L32H7 +0.91, L33H15 +0.69, L34H10 -0.47, L34H8 -0.47, L34H14 +0.39, L33H5 -0.38

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.330, max layer L5 (0.751)
- hdr_user: mean 0.011, max layer L8 (0.056)
- line1: mean 0.015, max layer L8 (0.038)
- line2: mean 0.016, max layer L8 (0.044)
- hdr_action: mean 0.006, max layer L8 (0.022)
- line3: mean 0.010, max layer L0 (0.044)
- line4: mean 0.019, max layer L32 (0.124)
- line5: mean 0.010, max layer L0 (0.042)
- line6: mean 0.020, max layer L0 (0.083)
- question: mean 0.168, max layer L26 (0.431)
- answer_instr: mean 0.074, max layer L16 (0.275)
- asst_header: mean 0.222, max layer L2 (0.592)
- last: mean 0.116, max layer L0 (0.267)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H0 mass 0.21 Δ+2.28, L32H9 mass 0.11 Δ+1.86, L33H15 mass 0.20 Δ+0.69, L32H7 mass 0.08 Δ+0.91, L24H4 mass 0.53 Δ+0.08, L34H15 mass 0.20 Δ+0.22

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +13.88 |
| loo_line2 | +13.62 |
| loo_line3 | +16.63 |
| loo_line4 | +13.90 |
| loo_line5 | +13.76 |
| loo_line6 | +12.87 |
| only_line1 | +16.00 |
| only_line2 | +10.50 |
| only_line3 | +17.37 |
| only_line4 | +15.12 |
| only_line5 | +21.00 |
| only_line6 | +21.88 |
| headers_only | +12.75 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

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
