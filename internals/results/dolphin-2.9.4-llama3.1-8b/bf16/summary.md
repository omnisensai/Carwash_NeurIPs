# dolphin-2.9.4-llama3.1-8b (bf16), substrate.txt

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token 'drive' · walk token 'walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -1.23 | 0.000 | 0.000 | 'I need to wash' |
| substrate | -0.73 | 0.000 | 0.000 | 'I need to wash' |

## logit lens (M per layer, emb first)
baseline:  +0.6 -0.3 +0.6 +0.9 +1.2 -3.5 +0.3 +3.4 +0.4 -0.7 -1.2 -3.3 -1.0 -2.4 -1.2 -2.7 -0.7 -0.4 +1.2 +0.7 +0.6 +1.0 +3.7 +3.3 +2.5 +3.9 +3.7 +3.5 +3.1 +3.7 +3.4 +3.3 +3.6
substrate: +0.6 -0.5 +0.7 +0.6 +1.0 -3.6 -0.1 -0.7 -0.3 -0.4 +0.1 -3.8 -1.5 -1.8 -1.3 -2.4 -2.7 -1.0 +0.2 +1.5 +1.6 +1.4 +3.4 +2.2 +1.3 +2.6 +2.2 +1.9 +2.1 +2.2 +1.8 +1.9 +3.0
final lens row == model logits: base False, sub False

## patching (substrate residual into baseline at the answer position)
M per layer: +2.0 +2.3 +2.4 +1.9 +2.0 +1.8 +2.3 +2.4 +2.3 +2.4 +2.5 +2.5 +2.2 +2.3 +2.6 +3.0 +3.0 +2.8 +3.1 +3.0 +3.1 +3.1 +2.9 +2.7 +2.8 +2.6 +2.5 +2.4 +2.1 +2.4 +2.4 +3.0
layers where the patch alone flips baseline to drive: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base +3.14 (model -1.98), sub +2.52 (model -0.81)
top Δ attention layers: L31 +0.64, L28 -0.32, L25 -0.26, L21 -0.24, L27 +0.13
top Δ MLP layers:       L31 +0.40, L15 -0.23, L6 -0.19, L24 -0.17, L18 +0.16
top Δ heads: L31H21 +0.17, L29H31 -0.17, L31H22 +0.16, L28H0 +0.12, L28H20 -0.12, L16H30 +0.11, L30H30 +0.10, L17H29 -0.09

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.390, max layer L20 (0.674)
- hdr_user: mean 0.011, max layer L30 (0.027)
- line1: mean 0.015, max layer L25 (0.037)
- line2: mean 0.011, max layer L0 (0.037)
- line3: mean 0.007, max layer L0 (0.036)
- line4: mean 0.003, max layer L0 (0.026)
- line5: mean 0.003, max layer L0 (0.040)
- line6: mean 0.002, max layer L0 (0.020)
- question: mean 0.041, max layer L0 (0.231)
- answer_instr: mean 0.027, max layer L11 (0.079)
- asst_header: mean 0.356, max layer L31 (0.735)
- last: mean 0.140, max layer L31 (0.453)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L31H21 mass 0.12 Δ+0.17, L31H22 mass 0.12 Δ+0.16, L30H30 mass 0.19 Δ+0.10, L31H19 mass 0.74 Δ+0.02, L28H0 mass 0.09 Δ+0.12, L27H6 mass 0.14 Δ+0.07

## substrate line ablations (M)
| variant | M |
|---|---|
| loo_line1 | -0.87 |
| loo_line2 | -1.19 |
| loo_line3 | -0.96 |
| loo_line4 | -0.87 |
| loo_line5 | -1.10 |
| loo_line6 | -1.02 |
| loo_line7 | -0.63 |
| loo_line8 | -0.77 |
| loo_line9 | -0.90 |
| only_line1 | -1.12 |
| only_line2 | -0.32 |
| only_line3 | -1.14 |
| only_line4 | -0.21 |
| only_line5 | -0.84 |
| only_line6 | -0.35 |
| only_line7 | -1.35 |
| only_line8 | -1.20 |
| only_line9 | -0.39 |
| headers_only | -0.40 |

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
| baseline | -1.23 | – | 'I' | 'I need to wash' |
| benchmark_CoT | -0.51 | – | 'I' | 'I need to wash' |
| benchmark_encourage | -2.29 | – | 'I' | 'I need to wash' |
| benchmark_expert | -1.14 | – | 'I' | 'I am a car' |
| benchmark_goaloriented | -1.44 | – | 'I' | 'I need to wash' |
| benchmark_hallucination | -0.51 | – | 'I' | 'I need to wash' |
| benchmark_nomistakes | -0.77 | – | 'I' | 'I need to wash' |
| benchmark_threat | -0.87 | – | 'I' | 'I need to wash' |
| benchmark_urgency | -0.73 | – | 'I' | 'I need to wash' |
| substrate | -0.73 | – | 'I' | 'I need to wash' |
