# Qwen2.5-3B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 36 · heads 16 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +4.25 | 0.986 | 0.014 | 'drive<|im_end|>' |
| substrate | +9.75 | 1.000 | 0.000 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan -7.0 -0.9 -3.1 -2.8 -4.8 -6.1 -4.5 -5.3 -4.3 -1.3 -3.7 -5.1 +0.4 -2.0 -1.1 -2.7 -0.2 -0.9 -1.8 +0.5 -1.3 -1.0 -1.4 -0.3 -1.7 -0.2 -3.2 +3.2 +1.0 +0.4 -0.1 +6.0 +5.2 +4.5 +4.3 +4.3
substrate: +nan -7.4 -1.4 -3.6 -4.0 -6.2 -7.2 -4.8 -5.5 -3.6 -1.1 -4.0 -5.5 +1.1 -1.5 -0.9 -2.5 -0.1 -1.3 -1.8 +0.0 -1.3 +0.6 -0.9 +0.2 -0.7 +1.6 -2.1 +3.6 +1.7 +1.2 +0.5 +7.3 +8.1 +8.8 +7.1 +9.7
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: +4.0 +4.0 +4.5 +4.0 +4.0 +4.0 +4.0 +4.3 +4.5 +4.5 +4.5 +4.2 +4.3 +4.3 +4.5 +4.0 +4.3 +4.5 +4.2 +4.3 +4.2 +4.5 +4.3 +5.2 +5.2 +5.0 +5.7 +7.0 +7.7 +7.2 +7.2 +6.5 +7.7 +9.7 +9.7 +9.7
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +4.20 (model +4.25), sub +9.67 (model +9.75)
top Δ attention layers: L33 +3.07, L32 +2.46, L31 +1.09, L34 +0.30, L21 +0.21
top Δ MLP layers:       L34 -1.00, L32 -0.69, L25 +0.31, L35 -0.30, L12 +0.30
top Δ heads: L33H15 +1.53, L32H7 +1.47, L33H0 +1.11, L32H9 +0.95, L34H9 +0.69, L31H5 +0.67, L34H8 -0.60, L34H10 -0.60

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.330, max layer L5 (0.774)
- hdr_user: mean 0.011, max layer L8 (0.053)
- line1: mean 0.013, max layer L8 (0.037)
- line2: mean 0.015, max layer L21 (0.065)
- hdr_action: mean 0.006, max layer L8 (0.021)
- line3: mean 0.008, max layer L0 (0.043)
- line4: mean 0.017, max layer L32 (0.102)
- line5: mean 0.008, max layer L0 (0.042)
- line6: mean 0.014, max layer L0 (0.085)
- question: mean 0.089, max layer L27 (0.171)
- answer_instr: mean 0.058, max layer L16 (0.174)
- asst_header: mean 0.236, max layer L2 (0.572)
- last: mean 0.111, max layer L0 (0.269)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H15 mass 0.10 Δ+1.53, L33H0 mass 0.11 Δ+1.11, L34H15 mass 0.12 Δ+0.43, L32H7 mass 0.03 Δ+1.47, L32H9 mass 0.04 Δ+0.95, L34H14 mass 0.09 Δ+0.32

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +10.75 |
| loo_line2 | +11.00 |
| loo_line3 | +13.25 |
| loo_line4 | +10.00 |
| loo_line5 | +10.50 |
| loo_line6 | +7.50 |
| only_line1 | +9.62 |
| only_line2 | +7.00 |
| only_line3 | +6.26 |
| only_line4 | +9.87 |
| only_line5 | +11.87 |
| only_line6 | +14.37 |
| headers_only | +6.75 |

line1: - Perform an activity on an object, while transporting the object from location A to B.
line2: - No other objectives or goals are relevant for the user.
line3: - Activities require the object to move from location A to location B together with the user.
line4: - The object is always initially with the user at location A.
line5: - Moving the user without moving the object does not satisfy the objective.
line6: - If the object is a vehicle, the user must operate the object in order to perform the activity at location B.

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | +4.25 | +4.25 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_CoT | +8.75 | +8.75 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | +9.86 | +9.86 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_expert | +10.25 | +10.25 @0 | 'Drive' | 'Drive.<|im_end|>' |
| benchmark_hallucination | +9.51 | +9.51 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_library | -4.75 | -4.75 @0 | 'Walk' | 'Walk.<|im_end|>' |
| benchmark_nomistakes | +7.10 | +7.10 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_threat | +9.48 | +9.48 @0 | 'Drive' | 'Drive<|im_end|>' |
| benchmark_urgency | +8.04 | +8.04 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate | +9.75 | +9.75 @0 | 'drive' | 'drive<|im_end|>' |
| substrate_pro | +5.00 | +5.00 @0 | 'drive' | 'drive<|im_end|>' |
| substrate+library (expect walk) | +4.02 | +4.02 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate_pro+library (expect walk) | -9.50 | -9.50 @0 | 'Walk' | 'Walk<|im_end|>' |
