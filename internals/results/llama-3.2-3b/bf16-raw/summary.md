# Llama-3.2-3B-Instruct (bf16), raw text

substrate file: substrate.txt

quant: bf16 · layers 28 · heads 24 · drive token ' Drive' · walk token ' Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | +1.46 | 0.045 | 0.011 | ' **Walk**.' |
| substrate | +0.99 | 0.130 | 0.048 | ' **Drive**.' |

## logit lens (M per layer, emb first)
baseline:  +0.0 -0.8 -0.2 -0.0 +1.3 +0.5 +1.4 -0.5 -0.9 -0.1 +1.6 +0.3 -0.0 -0.6 -1.1 -0.2 -2.4 -1.8 -1.7 -0.4 -1.8 -8.3 -9.0 -7.3 -5.5 -4.0 -3.0 -0.1 -0.2
substrate: +0.0 -0.9 +0.0 +0.3 +0.8 -0.1 +1.5 +0.7 +0.6 +1.9 +2.8 +0.9 +0.7 -0.1 -0.8 +0.0 -1.8 -0.8 -0.9 -0.3 +0.6 -5.1 -5.4 -2.4 -1.4 -0.2 +1.1 +3.1 +1.7
final lens row == model logits: base False, sub False

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -0.50 (model +1.75), sub +0.66 (model +1.06)
top Δ attention layers: L27 +0.92, L22 +0.76, L19 +0.60, L24 +0.57, L21 +0.30
top Δ MLP layers:       L27 -1.18, L20 +0.76, L24 -0.72, L23 -0.37, L26 -0.16
top Δ heads: L22H11 +0.68, L24H12 +0.41, L27H1 +0.35, L19H11 +0.31, L27H11 +0.24, L14H3 -0.23, L26H0 -0.23, L27H2 +0.22

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.639, max layer L2 (0.910)
- hdr_user: mean 0.646, max layer L2 (0.911)
- line1: mean 0.031, max layer L1 (0.628)
- line2: mean 0.008, max layer L0 (0.022)
- hdr_action: mean 0.005, max layer L0 (0.009)
- line3: mean 0.005, max layer L0 (0.034)
- line4: mean 0.004, max layer L0 (0.034)
- line5: mean 0.005, max layer L0 (0.034)
- line6: mean 0.013, max layer L0 (0.145)
- question: mean 0.116, max layer L0 (0.356)
- answer_instr: mean 0.118, max layer L0 (0.227)
- last: mean 0.050, max layer L27 (0.193)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L19H9 mass 0.21 Δ+0.21, L19H11 mass 0.09 Δ+0.31, L24H12 mass 0.05 Δ+0.41, L25H23 mass 0.14 Δ+0.14, L23H23 mass 0.32 Δ+0.06, L22H11 mass 0.02 Δ+0.68

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | +1.46 | -0.20 @1 | ' **' | ' **Walk**.' |
| benchmark_CoT | +0.70 | +0.52 @1 | ' **' | ' **Drive**.' |
| benchmark_encourage | -0.19 | -0.19 @0 | ' Walk' | ' Walk. \n\nExplanation' |
| benchmark_expert | +0.70 | – | ' Run' | ' Run. \n\nYou' |
| benchmark_hallucination | +0.04 | – | ' Yes' | ' Yes. \n\nExplanation' |
| benchmark_library | -0.19 | -1.53 @1 | ' **' | ' **Walk**.' |
| benchmark_nomistakes | +0.49 | +0.59 @1 | ' **' | ' **Drive**.' |
| benchmark_threat | +0.58 | – | ' W' | ' WALK. \n\n' |
| benchmark_urgency | +0.57 | – | ' W' | ' WALK. \n\n' |
| substrate | +0.99 | +1.70 @1 | ' **' | ' **Drive**.' |
| substrate_pro | +0.37 | +1.39 @1 | ' **' | ' **Drive**\n\nExplanation' |
| substrate+library (expect walk) | +0.32 | +0.49 @1 | ' **' | ' **Drive**.\n\n' |
| substrate_pro+library (expect walk) | -0.23 | +0.62 @1 | ' **' | ' **Drive**\n\nReason' |
