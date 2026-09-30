# Qwen/Qwen2.5-14B-Instruct

substrate file: substrate.txt

quant: bf16 · layers 48 · heads 40 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -15.75 | 0.000 | 1.000 | 'walk<|im_end|>' |
| substrate | +16.00 | 1.000 | 0.000 | 'drive<|im_end|>' |

## logit lens (M per layer, emb first)
baseline:  +3.4 +1.6 +1.7 +1.9 +1.2 -0.0 +0.4 -0.6 -1.0 +0.6 +1.0 +2.4 +0.5 +0.9 +0.8 +1.8 -2.1 -2.1 -1.0 -2.5 +0.8 -0.3 +0.5 +1.2 +1.6 +0.5 +2.5 +3.4 +4.9 +2.4 +2.4 -0.3 -0.8 -4.5 -6.2 -9.6 -16.8 -19.4 -17.4 -18.1 -23.0 -19.0 -15.2 -18.9 -16.9 -14.0 -12.4 -8.9 -15.7
substrate: +3.4 +1.6 +2.0 +2.0 +1.1 +0.1 -0.3 -0.7 -1.0 +0.3 +1.0 +1.9 +0.6 +1.7 +1.6 +2.8 -2.2 -2.1 -0.5 -1.6 +1.7 +0.1 +1.8 +2.6 +2.9 +1.9 +3.7 +4.1 +3.9 +1.2 +1.3 +0.8 +0.8 -1.3 -2.1 -2.2 -1.3 +2.5 +3.8 +3.3 +5.3 +8.8 +10.9 +7.4 +16.0 +18.5 +14.0 +8.7 +16.0
final lens row == model logits: base True, sub True

## patching (substrate residual into baseline at the answer position)
M per layer: -15.7 -15.5 -15.5 -15.5 -15.7 -15.5 -15.7 -15.7 -15.7 -15.5 -15.7 -15.7 -15.7 -15.7 -15.7 -15.7 -16.0 -16.0 -15.7 -16.2 -16.2 -16.2 -15.7 -16.0 -15.7 -16.2 -16.2 -15.0 -11.7 -10.5 -8.0 +3.5 +7.7 +8.0 +9.0 +10.0 +11.7 +12.5 +12.2 +14.0 +14.7 +14.7 +14.7 +15.0 +15.0 +15.5 +16.0 +16.0
layers where the patch alone flips baseline to drive: [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -15.62 (model -15.75), sub +15.99 (model +16.00)
top Δ attention layers: L43 +6.06, L46 +4.22, L40 +2.57, L36 +2.09, L41 +1.46
top Δ MLP layers:       L46 -6.66, L47 +5.79, L44 +3.61, L39 +3.25, L35 +2.33
top Δ heads: L46H12 +1.69, L46H14 +1.62, L43H18 +1.48, L41H22 +1.43, L43H35 +1.43, L46H10 -1.41, L40H25 +1.38, L43H17 +1.27

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.001, max layer L5 (0.012)
- hdr_user: mean 0.004, max layer L3 (0.014)
- line1: mean 0.006, max layer L1 (0.032)
- line2: mean 0.009, max layer L1 (0.035)
- line3: mean 0.009, max layer L1 (0.049)
- line4: mean 0.005, max layer L1 (0.032)
- line5: mean 0.007, max layer L1 (0.049)
- line6: mean 0.006, max layer L2 (0.028)
- question: mean 0.104, max layer L28 (0.279)
- answer_instr: mean 0.038, max layer L15 (0.127)
- asst_header: mean 0.174, max layer L4 (0.441)
- last: mean 0.080, max layer L47 (0.197)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L31H19 mass 0.81 Δ+0.25, L32H32 mass 0.74 Δ+0.23, L34H29 mass 0.71 Δ+0.22, L40H26 mass 0.12 Δ+0.96, L41H22 mass 0.06 Δ+1.43, L34H37 mass 0.71 Δ+0.11

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | +15.75 |
| loo_line2 | +15.00 |
| loo_line3 | +12.00 |
| loo_line4 | +15.75 |
| loo_line5 | +14.50 |
| loo_line6 | +12.25 |
| loo_line7 | +17.25 |
| loo_line8 | +13.00 |
| loo_line9 | +14.75 |
| only_line1 | +4.25 |
| only_line2 | -8.25 |
| only_line3 | +0.50 |
| only_line4 | -6.25 |
| only_line5 | +6.75 |
| only_line6 | +6.25 |
| only_line7 | +4.50 |
| only_line8 | +8.75 |
| only_line9 | -1.25 |
| headers_only | -7.00 |

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
| baseline | -15.75 | -15.75 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_CoT | -15.00 | -15.00 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_correct | +18.75 | +18.75 @0 | 'drive' | 'drive<|im_end|>' |
| benchmark_encourage | -14.25 | -14.25 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_expert | -13.50 | -13.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_hallucination | -12.75 | -12.75 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_nomistakes | -12.00 | -12.00 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_threat | -11.50 | -11.50 @0 | 'walk' | 'walk<|im_end|>' |
| benchmark_urgency | -10.00 | -10.00 @0 | 'walk' | 'walk<|im_end|>' |
| substrate | +16.00 | +16.00 @0 | 'drive' | 'drive<|im_end|>' |
