# CDIM — Llama-3.3-70B-Instruct (bf16), paraphrase/P1_T1 (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +16.306 (greedy 'Drive<|eot_id|>'); 80 layers, 189 tokens; rows = embedding + each layer output; 812.3 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +15.07 | +1.24 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +16.31 | -0.01 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +15.31 | +0.99 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +15.56 | +0.75 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +13.90 | +2.40 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +14.50 | +1.81 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +15.56 | +0.75 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +16.20 | +0.11 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +13.98 | +2.32 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +14.00 | +2.31 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | +1.24 | +1.48 (2) | +1.10 | 12 | 20 | 34 |  |
| cf5 | +2.40 | +2.54 (16) | +2.39 | 26 | None | 36 |  |
| cf6 | +1.81 | +2.06 (12) | +1.93 | 28 | None | 36 |  |
| cf9 | +2.32 | +2.70 (12) | +2.70 | 26 | 30 | 36 |  |
| cf9s | +2.31 | +2.68 (22) | +2.98 | 26 | 30 | 36 |  |

## Primary counterfactual cf5: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +2.54 (16) | -0.00 (66) | +2.39 (6) | -0.25 (48) |
| line6 | +0.51 (24) | -0.11 (16) | +0.13 (12) | -0.38 (16) |
| line7 | +0.39 (26) | -0.11 (18) | +0.12 (2) | -0.26 (10) |
| line8 | +0.37 (24) | -0.00 (10) | +0.13 (24) | -0.25 (14) |
| line9 | +0.64 (26) | -0.00 (74) | +0.37 (18) | -0.37 (12) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +2.65 (4) | -0.00 (40) | +2.39 (2) | -0.25 (42) |
| question | +0.90 (30) | +0.00 (68) | +0.76 (30) | -0.26 (12) |
| answer_instr | +0.37 (40) | -0.00 (20) | +0.13 (10) | -0.25 (42) |
| asst_header | +0.89 (32) | -0.00 (10) | +0.76 (32) | -0.26 (6) |
| answer_site | +2.40 (76) | +0.01 (8) | +2.40 (76) | -0.25 (4) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf5 run: max |ΔM| = 1.011 nats (vs Δbeh +2.40)
- library question: M(S) = -17.03 ('Walk<|eot_id|>'), M(C) = -17.52 ('Walk<|eot_id|>'); the largest M reached by any single patch = -16.65 → **stays Walk**

## Path validation: line5 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +2.40 | +0.01 (0%) | +0.00 (0%) | +0.12 (5%) | +2.40 (100%) |
| 4 | +2.28 | -0.11 (-5%) | +0.00 (0%) | +0.01 (1%) | +2.28 (100%) |
| 8 | +2.40 | +0.26 (11%) | +0.00 (0%) | +0.26 (11%) | +2.40 (100%) |
| 12 | +2.27 | +0.25 (11%) | +0.00 (0%) | +0.01 (1%) | +2.27 (100%) |
| 16 | +2.54 | +0.39 (15%) | +0.00 (0%) | +0.37 (15%) | +2.54 (100%) |
| 20 | +1.90 | +0.40 (21%) | +0.00 (0%) | +0.26 (14%) | +1.90 (100%) |
| 24 | +1.02 | -0.11 (-11%) | +0.00 (0%) | +0.13 (12%) | +1.02 (100%) |
| 28 | +1.15 | +0.01 (1%) | +0.00 (0%) | +0.39 (34%) | +1.15 (100%) |
| 32 | +0.51 | +0.00 (0%) | +0.00 (0%) | +0.37 (73%) | +0.51 (100%) |
| 36 | +0.12 | +0.25 (200%) | +0.00 (0%) | +0.01 (9%) | +0.12 (100%) |
| 40 | +0.26 | +0.25 (96%) | +0.00 (0%) | +0.01 (4%) | +0.26 (100%) |
| 44 | +0.26 | +0.25 (96%) | +0.00 (0%) | +0.00 (0%) | +0.26 (100%) |
| 48 | +0.26 | +0.25 (96%) | +0.00 (0%) | +0.12 (48%) | +0.26 (100%) |
| 52 | +0.26 | +0.01 (4%) | +0.00 (0%) | +0.25 (96%) | +0.26 (100%) |
| 56 | +0.01 | +0.26 | +0.00 | +0.00 | +0.01 |
| 60 | +0.26 | +0.00 (0%) | +0.00 (0%) | +0.26 (100%) | +0.26 (100%) |
| 64 | +0.01 | +0.25 | +0.00 | +0.26 | +0.01 |
| 68 | +0.01 | +0.00 | +0.00 | +0.26 | +0.01 |
| 72 | +0.26 | +0.26 (100%) | +0.00 (0%) | +0.26 (100%) | +0.26 (100%) |
| 76 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
