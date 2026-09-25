# CDIM — Llama-3.3-70B-Instruct (bf16), paraphrase/P2_T1 (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +14.939 (greedy 'Drive<|eot_id|>'); 80 layers, 187 tokens; rows = embedding + each layer output; 810.6 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +12.45 | +2.49 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +14.94 | -0.00 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +14.20 | +0.74 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +14.06 | +0.87 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +12.79 | +2.15 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +12.25 | +2.69 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +14.06 | +0.87 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +14.34 | +0.60 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +13.66 | +1.28 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +13.80 | +1.14 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | +2.49 | +2.24 (2) | +2.50 | 12 | 24 | 36 |  |
| cf5 | +2.15 | +2.15 (16) | +2.28 | 20 | None | 36 |  |
| cf6 | +2.69 | +3.20 (16) | +3.26 | 28 | None | 40 |  |
| cf9 | +1.28 | +1.65 (16) | +1.66 | 26 | 30 | 34 |  |
| cf9s | +1.14 | +1.78 (22) | +1.79 | 28 | 30 | 36 |  |

## Primary counterfactual cf6: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line6 | +3.20 (16) | -0.11 (44) | +3.26 (18) | -0.01 (40) |
| line7 | +0.39 (22) | -0.37 (4) | +0.37 (24) | -0.14 (16) |
| line8 | +0.25 (30) | -0.52 (26) | +0.37 (8) | -0.51 (26) |
| line9 | +0.40 (30) | -0.39 (22) | +0.49 (30) | -0.01 (46) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +2.69 (6) | -0.12 (54) | +2.81 (10) | -0.01 (46) |
| question | +0.75 (30) | -0.14 (8) | +0.87 (30) | -0.12 (8) |
| answer_instr | +0.12 (26) | -0.11 (14) | +0.26 (28) | -0.13 (6) |
| asst_header | +1.54 (34) | -0.39 (28) | +1.38 (32) | -0.01 (18) |
| answer_site | +2.69 (80) | -0.02 (2) | +2.69 (78) | -0.01 (8) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf6 run: max |ΔM| = 0.641 nats (vs Δbeh +2.69)
- library question: M(S) = -13.54 ('Walk<|eot_id|>'), M(C) = -12.96 ('Walk<|eot_id|>'); the largest M reached by any single patch = -12.39 → **stays Walk**

## Path validation: line6 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +2.69 | -0.13 (-5%) | +0.00 (0%) | +0.00 (0%) | +2.69 (100%) |
| 4 | +2.43 | -0.02 (-1%) | +0.00 (0%) | +0.00 (0%) | +2.43 (100%) |
| 8 | +2.69 | -0.00 (-0%) | +0.00 (0%) | +0.01 (0%) | +2.69 (100%) |
| 12 | +2.69 | -0.11 (-4%) | +0.00 (0%) | +0.00 (0%) | +2.69 (100%) |
| 16 | +3.20 | +0.01 (0%) | +0.00 (0%) | +0.00 (0%) | +3.20 (100%) |
| 20 | +2.33 | +0.26 (11%) | +0.00 (0%) | +0.00 (0%) | +2.33 (100%) |
| 24 | +1.94 | +0.14 (7%) | +0.00 (0%) | +0.00 (0%) | +1.94 (100%) |
| 28 | +2.19 | +0.15 (7%) | +0.00 (0%) | +0.14 (6%) | +2.19 (100%) |
| 32 | +0.55 | +0.01 (2%) | +0.00 (0%) | +0.14 (25%) | +0.55 (100%) |
| 36 | -0.09 | +0.00 (-0%) | +0.00 (-0%) | +0.03 (-30%) | -0.09 (100%) |
| 40 | +0.01 | +0.01 | +0.00 | +0.01 | +0.01 |
| 44 | -0.11 | +0.01 (-12%) | +0.00 (-0%) | -0.00 (1%) | -0.11 (100%) |
| 48 | +0.00 | +0.00 | +0.00 | -0.00 | +0.00 |
| 52 | +0.01 | +0.00 | +0.00 | -0.11 | +0.01 |
| 56 | +0.00 | -0.00 | +0.00 | +0.00 | +0.00 |
| 60 | +0.00 | -0.00 | +0.00 | -0.00 | +0.00 |
| 64 | -0.00 | -0.00 | +0.00 | +0.00 | -0.00 |
| 68 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 72 | -0.00 | -0.00 | +0.00 | +0.00 | -0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
