# CDIM — Llama-3.3-70B-Instruct (bf16), paraphrase/P6_T1 (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +15.233 (greedy 'Drive<|eot_id|>'); 80 layers, 192 tokens; rows = embedding + each layer output; 807.4 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +14.70 | +0.53 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +15.51 | -0.28 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +13.80 | +1.43 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +15.01 | +0.22 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +13.06 | +2.18 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +11.86 | +3.38 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +15.01 | +0.23 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +15.45 | -0.22 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +13.12 | +2.11 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +13.09 | +2.15 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf3 | +1.43 | +1.68 (12) | +1.71 | 24 | None | 36 |  |
| cf5 | +2.18 | +2.39 (12) | +2.72 | 22 | None | 36 |  |
| cf6 | +3.38 | +3.62 (8) | +3.71 | 26 | None | 36 |  |
| cf9 | +2.11 | +2.45 (22) | +2.48 | 26 | None | 34 |  |
| cf9s | +2.15 | +2.37 (24) | +2.27 | 26 | 28 | 34 |  |

## Primary counterfactual cf6: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line6 | +3.62 (8) | -0.21 (54) | +3.71 (8) | -0.28 (54) |
| line7 | +0.87 (22) | -0.17 (6) | +0.28 (22) | -0.28 (14) |
| line8 | +0.12 (30) | -0.54 (26) | +0.13 (6) | -0.40 (24) |
| line9 | +0.50 (30) | -0.29 (18) | +0.28 (24) | -0.28 (4) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +3.63 (2) | -0.25 (56) | +3.42 (2) | -0.28 (44) |
| question | +1.49 (28) | -0.25 (60) | +1.18 (24) | -0.28 (74) |
| answer_instr | +0.29 (26) | -0.12 (18) | +0.12 (6) | -0.28 (36) |
| asst_header | +1.61 (32) | -0.29 (16) | +1.11 (32) | -0.25 (2) |
| answer_site | +3.62 (78) | -0.12 (4) | +3.46 (74) | -0.28 (6) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf6 run: max |ΔM| = 0.556 nats (vs Δbeh +3.38)
- library question: M(S) = -15.93 ('walk<|eot_id|>'), M(C) = -15.06 ('walk<|eot_id|>'); the largest M reached by any single patch = -14.75 → **stays Walk**

## Path validation: line6 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +3.38 | +0.17 (5%) | +0.00 (0%) | -0.12 (-4%) | +3.38 (100%) |
| 4 | +3.28 | -0.03 (-1%) | +0.00 (0%) | -0.12 (-4%) | +3.28 (100%) |
| 8 | +3.62 | +0.08 (2%) | +0.00 (0%) | +0.00 (0%) | +3.62 (100%) |
| 12 | +3.50 | +0.30 (8%) | +0.00 (0%) | +0.00 (0%) | +3.50 (100%) |
| 16 | +3.50 | +0.33 (9%) | +0.00 (0%) | +0.00 (0%) | +3.50 (100%) |
| 20 | +2.72 | +0.57 (21%) | +0.00 (0%) | +0.04 (2%) | +2.72 (100%) |
| 24 | +1.86 | +0.42 (23%) | +0.00 (0%) | -0.00 (-0%) | +1.86 (100%) |
| 28 | +1.53 | +0.17 (11%) | +0.00 (0%) | +0.00 (0%) | +1.53 (100%) |
| 32 | +0.34 | +0.05 (14%) | +0.00 (0%) | +0.08 (23%) | +0.34 (100%) |
| 36 | +0.07 | +0.00 (0%) | +0.00 (0%) | +0.22 (318%) | +0.07 (100%) |
| 40 | -0.08 | +0.05 (-59%) | +0.00 (-0%) | -0.05 (58%) | -0.08 (100%) |
| 44 | +0.08 | +0.08 (100%) | +0.00 (0%) | +0.00 (0%) | +0.08 (100%) |
| 48 | +0.00 | +0.00 | +0.00 | -0.00 | +0.00 |
| 52 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 56 | +0.00 | -0.00 | +0.00 | -0.12 | +0.00 |
| 60 | +0.00 | -0.00 | +0.00 | -0.05 | +0.00 |
| 64 | +0.00 | -0.00 | +0.00 | +0.00 | +0.00 |
| 68 | -0.00 | -0.00 | +0.00 | -0.05 | -0.00 |
| 72 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
