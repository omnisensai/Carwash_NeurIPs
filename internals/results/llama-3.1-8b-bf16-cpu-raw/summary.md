# Llama-3.1-8B-Instruct (bf16, CPU), raw text

substrate file: substrate.txt

quant: bf16 · layers 32 · heads 32 · drive token ' Drive' · walk token ' Walk'

| prompt | M (nats) | p(drive) | p(walk) | greedy |
|---|---|---|---|---|
| baseline | -0.73 | 0.198 | 0.411 | ' Walk.<|eot_id|>' |
| substrate | +0.71 | 0.462 | 0.226 | ' Drive. \n\nExplanation' |

## logit lens (M per layer, emb first)
baseline:  +0.4 +1.4 +2.8 +1.0 +0.4 +2.3 +1.8 +0.2 -0.3 +1.1 +0.5 +1.5 +1.3 +2.6 +2.1 +0.8 +0.6 +2.7 +1.0 -0.0 -0.8 -0.7 -0.8 -3.2 -9.0 -4.5 -4.1 -2.6 -2.3 -5.4 +0.6 +1.1 -0.7
substrate: +0.4 +1.9 +3.5 +1.3 +0.4 +2.5 +2.8 +1.3 -0.0 +1.3 +1.3 +2.1 +1.2 +1.4 +0.6 -0.6 -0.3 +1.3 +0.4 -1.2 -1.6 -1.6 -0.5 -2.3 -7.4 -1.3 -1.6 -0.4 +0.5 -2.2 +2.7 +3.0 +0.8
final lens row == model logits: base True, sub False

## direct logit attribution (drive−walk), substrate − baseline
DLA sums: base -0.68 (model -0.69), sub +0.81 (model +0.75)
top Δ attention layers: L31 +0.35, L25 +0.25, L23 -0.19, L30 +0.17, L27 +0.15
top Δ MLP layers:       L29 -0.73, L23 +0.62, L25 -0.38, L28 +0.29, L31 +0.29
top Δ heads: L25H15 +0.53, L25H5 -0.28, L24H17 +0.25, L31H3 +0.24, L31H21 +0.24, L31H22 -0.20, L30H25 -0.16, L23H22 -0.14

## attention from the answer position (substrate run, mean over heads and layers)
- bos: mean 0.570, max layer L2 (0.880)
- hdr_user: mean 0.576, max layer L2 (0.881)
- line1: mean 0.034, max layer L1 (0.697)
- line2: mean 0.012, max layer L0 (0.037)
- hdr_action: mean 0.005, max layer L9 (0.019)
- line3: mean 0.007, max layer L0 (0.058)
- line4: mean 0.006, max layer L0 (0.054)
- line5: mean 0.009, max layer L0 (0.048)
- line6: mean 0.018, max layer L0 (0.175)
- question: mean 0.148, max layer L0 (0.317)
- answer_instr: mean 0.133, max layer L12 (0.282)
- last: mean 0.052, max layer L31 (0.209)
heads attending to substrate lines AND pushing drive (mass × ΔDLA): L31H21 mass 0.11 Δ+0.24, L24H17 mass 0.10 Δ+0.25, L25H15 mass 0.04 Δ+0.53, L22H27 mass 0.15 Δ+0.07, L13H1 mass 0.32 Δ+0.03, L28H0 mass 0.11 Δ+0.08

## all prompts
| prompt | M (first token) | M at decision token | argmax | greedy |
|---|---|---|---|---|
| baseline | -0.73 | -0.73 @0 | ' Walk' | ' Walk.<|eot_id|>' |
| benchmark_CoT | -0.87 | -0.87 @0 | ' Walk' | ' Walk.<|eot_id|>' |
| benchmark_encourage | -1.11 | -1.11 @0 | ' Walk' | ' Walk. \n\nExplanation' |
| benchmark_expert | -0.83 | -0.83 @0 | ' Walk' | ' Walk. \n```' |
| benchmark_hallucination | -0.96 | -0.96 @0 | ' Walk' | ' Walk. \n```' |
| benchmark_library | -1.93 | -1.93 @0 | ' Walk' | ' Walk.<|eot_id|>' |
| benchmark_nomistakes | -0.80 | -0.80 @0 | ' Walk' | ' Walk.<|eot_id|>' |
| benchmark_threat | -1.07 | -1.07 @0 | ' Walk' | ' Walk. \n\n(' |
| benchmark_urgency | -0.29 | -0.29 @0 | ' Walk' | ' Walk.<|eot_id|>' |
| substrate | +0.71 | +0.71 @0 | ' Drive' | ' Drive. \n\nExplanation' |
| substrate_pro | +0.84 | +0.84 @0 | ' Drive' | ' Drive. \n``' |
| substrate+library (expect walk) | -0.30 | -0.30 @0 | ' Walk' | ' Walk. \n\nExplanation' |
| substrate_pro+library (expect walk) | -0.52 | -0.52 @0 | ' Walk' | ' Walk. \n``' |
