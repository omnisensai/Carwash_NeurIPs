# Qwen3-4B-Instruct-2507

substrate file: substrate_pro.txt

quant: bf16 · layers 36 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -22.12 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | +18.38 | 1.000 | 0.000 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +nan +1.4 +4.0 +2.9 +3.5 +2.5 +2.7 -0.1 +0.6 +3.3 +1.0 +1.7 +2.0 +1.7 +3.8 +2.2 +2.1 +3.3 +2.7 +2.5 +0.8 +0.1 -0.0 -0.6 -2.3 -3.7 -3.3 -4.2 -4.6 -4.6 -12.3 -12.2 -15.5 -14.2 -16.7 -15.3 -22.0
substrate: +nan +1.0 +4.2 +3.3 +4.3 +2.7 +2.9 +0.2 +0.8 +3.0 +2.3 +1.6 +2.0 +1.9 +3.4 +1.8 +0.9 +2.1 +1.9 +1.2 -0.6 -2.3 +0.4 +0.2 +0.3 +1.7 +1.3 +0.3 +0.5 +1.2 +5.2 +5.5 +5.1 +14.1 +14.0 +10.1 +18.4
final lens row == model logits: base False, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -22.1 -22.0 -21.5 -22.0 -21.9 -21.6 -21.9 -21.9 -21.7 -21.7 -21.9 -22.2 -21.9 -22.1 -22.1 -21.9 -21.9 -21.0 -20.5 -19.6 -17.1 -12.7 -14.6 -0.2 +2.3 +4.0 +8.0 +8.2 +8.8 +10.5 +11.2 +11.5 +12.5 +16.1 +17.1 +18.4
layers where the patch alone flips baseline to drive: [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -22.09 (model -22.12), sub +18.42 (model +18.38)
top Δ attention layers: L33 +14.73, L32 +7.88, L29 +4.33, L31 +3.83, L35 +3.68
top Δ MLP layers:       L33 -4.59, L32 +3.06, L35 -2.95, L29 +2.15, L34 +2.13
top Δ heads: L33H11 +7.46, L33H23 +5.43, L32H2 +4.07, L32H0 +3.48, L31H15 +2.60, L35H26 +2.46, L33H30 +2.17, L31H28 +1.40

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.421, max layer L30 (0.811)
- hdr_user: mean 0.003, max layer L1 (0.009)
- line1: mean 0.006, max layer L0 (0.020)
- line2: mean 0.038, max layer L4 (0.274)
- hdr_action: mean 0.004, max layer L8 (0.011)
- line3: mean 0.008, max layer L0 (0.038)
- line4: mean 0.006, max layer L0 (0.026)
- line5: mean 0.007, max layer L0 (0.043)
- line6: mean 0.011, max layer L0 (0.037)
- question: mean 0.081, max layer L21 (0.201)
- answer_instr: mean 0.046, max layer L17 (0.156)
- asst_header: mean 0.188, max layer L1 (0.433)
- last: mean 0.083, max layer L35 (0.203)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L33H11 mass 0.11 Δ+7.46, L33H23 mass 0.12 Δ+5.43, L32H0 mass 0.07 Δ+3.48, L31H15 mass 0.07 Δ+2.60, L29H27 mass 0.15 Δ+1.01, L32H2 mass 0.03 Δ+4.07

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +18.88 |
| loo_line2 | +11.25 |
| loo_line3 | +16.88 |
| loo_line4 | +20.12 |
| loo_line5 | +18.75 |
| loo_line6 | +9.00 |
| loo_line7 | -3.25 |
| loo_line8 | +18.38 |
| loo_line9 | +6.25 |
| only_line1 | -20.87 |
| only_line2 | -19.25 |
| only_line3 | -18.37 |
| only_line4 | -17.50 |
| only_line5 | -18.37 |
| only_line6 | +20.12 |
| only_line7 | +3.25 |
| only_line8 | -13.75 |
| only_line9 | -17.12 |
| headers_only | -17.00 |

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
| baseline | -22.12 | -22.12 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -4.51 | -4.51 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_encourage | -4.00 | -4.00 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_expert | -0.50 | -0.50 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_hallucination | -6.55 | -6.55 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_library | -22.05 | -22.05 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_nomistakes | -3.44 | -3.44 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -3.74 | -3.74 @0 | 'Walk' | 'Walk<|im_end|>' |
| benchmark_urgency | +6.25 | +6.25 @0 | 'Drive' | 'Drive<|im_end|>' |
| substrate | -9.75 | -9.75 @0 | 'walk' | 'walk<|im_end|>' |
| substrate_pro | +18.38 | +18.38 @0 | 'drive' | 'drive<|im_end|>' |
| substrate+library (expect walk) | -19.00 | -19.00 @0 | 'walk' | 'walk<|im_end|>' |
| substrate_pro+library (expect walk) | -22.50 | -22.50 @0 | 'walk' | 'walk<|im_end|>' |
