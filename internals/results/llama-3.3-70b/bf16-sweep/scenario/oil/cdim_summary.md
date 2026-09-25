# CDIM — Llama-3.3-70B-Instruct (bf16), scenario/oil (internals/cdim_sweep/generated/substrates/oil/S.txt)

M(S) = +14.651 (greedy 'Drive<|eot_id|>'); 80 layers, 190 tokens; rows = embedding + each layer output; 812.0 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +13.66 | +0.99 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +14.40 | +0.25 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +13.64 | +1.01 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +14.41 | +0.24 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +12.91 | +1.74 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +13.32 | +1.33 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +14.31 | +0.35 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +14.31 | +0.35 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +13.22 | +1.43 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +13.11 | +1.54 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf3 | +1.01 | +1.25 (12) | +1.14 | 22 | 24 | 40 |  |
| cf5 | +1.74 | +1.73 (2) | +1.61 | 28 | None | 38 |  |
| cf6 | +1.33 | +1.34 (12) | +1.72 | 20 | None | 38 |  |
| cf9 | +1.43 | +1.67 (22) | +1.54 | 28 | 30 | 36 |  |
| cf9s | +1.54 | +1.92 (22) | +1.78 | 28 | 30 | 36 |  |

## Primary counterfactual cf5: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +1.73 (2) | -0.01 (56) | +1.61 (2) | -0.14 (36) |
| line6 | +0.36 (24) | -0.01 (48) | +0.25 (20) | -0.13 (14) |
| line7 | +0.24 (24) | -0.02 (18) | +0.26 (24) | -0.11 (20) |
| line8 | +0.35 (2) | -0.14 (10) | +0.26 (16) | -0.12 (10) |
| line9 | +0.36 (26) | -0.01 (2) | +0.37 (16) | -0.12 (40) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +1.85 (2) | -0.01 (60) | +1.75 (2) | -0.01 (44) |
| question | +0.36 (30) | -0.15 (28) | +0.37 (30) | -0.14 (28) |
| answer_instr | +0.11 (14) | -0.02 (2) | +0.25 (32) | -0.13 (40) |
| asst_header | +0.99 (32) | -0.02 (24) | +0.87 (32) | -0.14 (24) |
| answer_site | +1.74 (78) | -0.01 (8) | +1.75 (74) | -0.14 (16) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf5 run: max |ΔM| = 0.510 nats (vs Δbeh +1.74)
- library question: M(S) = -12.87 ('walk<|eot_id|>'), M(C) = -13.66 ('walk<|eot_id|>'); the largest M reached by any single patch = -12.55 → **stays Walk**

## Path validation: line5 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +1.74 | +0.11 (7%) | +0.00 (0%) | -0.01 (-1%) | +1.74 (100%) |
| 4 | +1.49 | +0.11 (8%) | +0.00 (0%) | -0.01 (-1%) | +1.49 (100%) |
| 8 | +1.50 | +0.11 (8%) | +0.00 (0%) | -0.01 (-1%) | +1.50 (100%) |
| 12 | +1.49 | +0.10 (7%) | +0.00 (0%) | -0.01 (-1%) | +1.49 (100%) |
| 16 | +1.50 | -0.15 (-10%) | +0.00 (0%) | -0.01 (-1%) | +1.50 (100%) |
| 20 | +1.24 | -0.01 (-1%) | +0.00 (0%) | -0.00 (-0%) | +1.24 (100%) |
| 24 | +0.99 | -0.02 (-2%) | +0.00 (0%) | +0.10 (10%) | +0.99 (100%) |
| 28 | +1.12 | -0.01 (-1%) | +0.00 (0%) | +0.11 (10%) | +1.12 (100%) |
| 32 | +0.25 | -0.01 (-5%) | +0.00 (0%) | +0.10 (40%) | +0.25 (100%) |
| 36 | +0.11 | -0.01 (-10%) | +0.00 (0%) | -0.01 (-10%) | +0.11 (100%) |
| 40 | -0.01 | +0.00 | +0.00 | -0.01 | -0.01 |
| 44 | +0.11 | -0.01 (-10%) | +0.00 (0%) | +0.11 (100%) | +0.11 (100%) |
| 48 | +0.11 | -0.01 (-10%) | +0.00 (0%) | -0.01 (-10%) | +0.11 (100%) |
| 52 | +0.11 | +0.11 (100%) | +0.00 (0%) | -0.01 (-10%) | +0.11 (100%) |
| 56 | -0.01 | +0.00 | +0.00 | -0.01 | -0.01 |
| 60 | -0.00 | +0.00 | +0.00 | -0.01 | -0.00 |
| 64 | +0.00 | -0.01 | +0.00 | +0.00 | +0.00 |
| 68 | -0.01 | -0.01 | +0.00 | -0.01 | -0.01 |
| 72 | -0.00 | +0.00 | +0.00 | -0.01 | -0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
