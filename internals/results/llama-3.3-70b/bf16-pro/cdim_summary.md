# CDIM — Llama-3.3-70B-Instruct (bf16), substrate_pro.txt (substrate_pro.txt)

M(S) = +17.005 (greedy 'Drive<|eot_id|>'); 80 layers, 247 tokens; rows = embedding + each layer output; 3095.1 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| p1 | 1 | reverse | True | +17.40 | -0.40 | 'Drive<|eot_id|>' | - Perform an activity on an object at a starting location. |
| p2 | 2 | reverse | True | +16.51 | +0.50 | 'Drive<|eot_id|>' | - The object must be at the starting location for the activity to complete. |
| p3 | 3 | reverse | True | +17.03 | -0.03 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| p4 | 4 | reverse | True | +16.07 | +0.93 | 'Drive<|eot_id|>' | - The object is initially with the user at location B. |
| p5 | 5 | reverse | True | +16.70 | +0.31 | 'Drive<|eot_id|>' | - The activity is performed at location B (the service location). The object may be absent at location B. |
| p6 | 6 | reverse | True | +14.66 | +2.35 | 'Drive<|eot_id|>' | - Vehicles are fully portable. Walking brings a vehicle along. Leaving the object behind fails the objective. |
| p7 | 7 | reverse | True | +17.13 | -0.12 | 'Drive<|eot_id|>' | - Books are portable. Driving transports both the user and the book. |
| p8 | 8 | reverse | True | +16.79 | +0.21 | 'Drive<|eot_id|>' | - Leaving the object behind meets the objective. |
| p9 | 9 | reverse | True | +12.53 | +4.48 | 'Drive<|eot_id|>' | - To transport a vehicle from A to B, the user may leave it. |
| p9s | 9 | strong-reverse | True | +10.56 | +6.45 | 'Drive<|eot_id|>' | - To transport a vehicle from A to B, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| p1 | -0.40 | -0.53 (4) | -0.55 | 28 | 4 | 6 | +0.57 |
| p2 | +0.50 | +0.62 (14) | +0.25 | 26 | 12 | 36 | +0.40 |
| p3 | -0.03 | -0.25 (22) | -0.28 | 50 | 4 | 4 | +0.50 |
| p4 | +0.93 | +1.31 (4) | +1.02 | 16 | None | 36 | -0.50 |
| p5 | +0.31 | +0.43 (2) | +0.37 | 30 | 28 | 40 | +0.12 |
| p6 | +2.35 | +2.75 (4) | +2.16 | 28 | 30 | 34 | +1.18 |
| p7 | -0.12 | -0.72 (32) | -0.53 | 72 | 2 | 2 | +0.58 |
| p8 | +0.21 | +0.31 (42) | +0.40 | 28 | 16 | 36 | -0.72 |
| p9 | +4.48 | +4.86 (16) | +4.95 | 30 | 28 | 36 | -0.62 |
| p9s | +6.45 | +7.00 (22) | +6.45 | 30 | 28 | 36 | -0.62 |

## Primary counterfactual p9s: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line6 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line7 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line8 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line9 | +7.00 (22) | -0.05 (64) | +6.45 (8) | -0.40 (44) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +7.00 (22) | -0.05 (64) | +6.45 (8) | -0.40 (44) |
| question | +5.62 (30) | +0.00 (80) | +2.16 (30) | -0.70 (22) |
| answer_instr | +0.34 (16) | -0.24 (52) | +0.10 (36) | -0.28 (14) |
| asst_header | +1.88 (34) | -0.99 (58) | +1.00 (34) | -0.28 (12) |
| answer_site | +6.45 (52) | -0.17 (16) | +7.19 (54) | -0.37 (4) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the p9s run: max |ΔM| = 1.460 nats (vs Δbeh +6.45)
- library question: M(S) = -17.75 ('Walk.<|eot_id|>'), M(C) = -16.50 ('Walk.<|eot_id|>'); the largest M reached by any single patch = -16.37 → **stays Walk**

## Path validation: line9 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +6.45 | +0.39 (6%) | +0.00 (0%) | +0.08 (1%) | +6.45 (100%) |
| 4 | +6.55 | +0.00 (0%) | +0.00 (0%) | +0.14 (2%) | +6.55 (100%) |
| 8 | +6.55 | +0.08 (1%) | +0.00 (0%) | -0.24 (-4%) | +6.55 (100%) |
| 12 | +6.70 | +0.25 (4%) | +0.00 (0%) | +0.08 (1%) | +6.70 (100%) |
| 16 | +6.55 | +0.68 (10%) | +0.00 (0%) | +0.08 (1%) | +6.55 (100%) |
| 20 | +6.70 | +2.38 (36%) | +0.00 (0%) | +0.07 (1%) | +6.70 (100%) |
| 24 | +6.42 | +2.98 (46%) | +0.00 (0%) | -0.05 (-1%) | +6.42 (100%) |
| 28 | +5.32 | +2.40 (45%) | +0.00 (0%) | +0.84 (16%) | +5.32 (100%) |
| 32 | +1.81 | +0.05 (3%) | +0.00 (0%) | +0.59 (32%) | +1.81 (100%) |
| 36 | +0.70 | +0.00 (0%) | +0.00 (0%) | +0.15 (21%) | +0.70 (100%) |
| 40 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 44 | +0.08 | +0.08 (100%) | +0.00 (0%) | +0.08 (100%) | +0.08 (100%) |
| 48 | +0.00 | +0.00 | +0.00 | +0.07 | +0.00 |
| 52 | +0.00 | +0.00 | +0.00 | +0.08 | +0.00 |
| 56 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 60 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 64 | -0.05 | +0.08 | +0.00 | +0.00 | -0.05 |
| 68 | +0.00 | +0.00 | +0.00 | -0.24 | +0.00 |
| 72 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
