# CDIM — llama-3-8b-Instruct (bf16), substrate.txt (substrate.txt)

M(S) = +0.750 (greedy 'drive<|eot_id|>'); 32 layers, 168 tokens; rows = embedding + each layer output; 502.2 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +1.43 | -0.68 | 'drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +0.47 | +0.28 | 'drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +1.72 | -0.97 | 'drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +1.50 | -0.75 | 'drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +0.08 | +0.67 | 'Walk<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +0.57 | +0.18 | 'drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | -2.20 | +2.95 | 'Walk<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +1.05 | -0.30 | 'drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | -1.50 | +2.25 | 'Walk<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | -1.32 | +2.07 | 'Walk<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | -0.68 | -0.96 (3) | -0.81 | 7 | None | 15 | -0.73 |
| cf2 | +0.28 | +0.45 (4) | +0.47 | 8 | None | 16 | +0.02 |
| cf3 | -0.97 | -0.79 (1) | -1.03 | 7 | None | 15 | +0.27 |
| cf4 | -0.75 | -0.77 (2) | -0.75 | 6 | None | 15 | -0.66 |
| cf5 | +0.67 | +0.98 (9) | +0.97 | 12 | None | 16 | +0.68 |
| cf6 | +0.18 | +0.29 (8) | +0.19 | 17 | 12 | 15 | -0.75 |
| cf7 | +2.95 | +3.25 (6) | +3.03 | 11 | None | 15 | -1.22 |
| cf8 | -0.30 | -0.37 (8) | -0.36 | 8 | 7 | 15 | -0.14 |
| cf9 | +2.25 | +2.34 (4) | +2.31 | 12 | None | 15 | +1.22 |
| cf9s | +2.07 | +2.24 (1) | +2.19 | 12 | None | 15 | +1.22 |

## Primary counterfactual cf7: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line2 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line3 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line4 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line5 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line6 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line7 | +3.25 (6) | -0.07 (17) | +3.03 (7) | -0.07 (18) |
| line8 | +0.57 (10) | -0.14 (12) | +0.32 (10) | -0.31 (6) |
| line9 | +0.31 (14) | -0.14 (10) | +0.20 (11) | -0.18 (8) |
| headers | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| definitions | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| system | +3.18 (7) | -0.07 (20) | +3.14 (8) | -0.07 (18) |
| question | +1.46 (12) | -0.14 (8) | +1.06 (12) | -0.18 (7) |
| answer_instr | +0.12 (14) | -0.07 (17) | +0.07 (21) | -0.12 (1) |
| asst_header | +0.59 (21) | -0.07 (12) | +0.45 (21) | -0.12 (6) |
| answer_site | +2.95 (32) | -0.07 (8) | +2.95 (32) | -0.06 (9) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf7 run: max |ΔM| = 0.754 nats (vs Δbeh +2.95)

## Path validation: line7 → question / answer site (rows 0…32)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +2.95 | -0.07 (-2%) | +0.00 (0%) | +0.11 (4%) | +2.95 (100%) |
| 2 | +3.04 | +0.06 (2%) | +0.00 (0%) | -0.02 (-1%) | +3.04 (100%) |
| 4 | +3.24 | -0.07 (-2%) | +0.00 (0%) | -0.02 (-1%) | +3.24 (100%) |
| 6 | +3.25 | +0.00 (0%) | +0.00 (0%) | -0.02 (-1%) | +3.25 (100%) |
| 8 | +2.88 | +0.54 (19%) | +0.00 (0%) | -0.02 (-1%) | +2.88 (100%) |
| 10 | +2.15 | +0.93 (43%) | +0.00 (0%) | -0.02 (-1%) | +2.15 (100%) |
| 12 | +1.28 | +0.32 (25%) | +0.00 (0%) | +0.12 (10%) | +1.28 (100%) |
| 14 | +0.20 | -0.00 (-0%) | +0.00 (0%) | -0.02 (-10%) | +0.20 (100%) |
| 16 | +0.07 | +0.00 (5%) | +0.00 (0%) | -0.07 (-95%) | +0.07 (100%) |
| 18 | +0.00 | -0.07 | +0.00 | +0.06 | +0.00 |
| 20 | +0.00 | +0.00 | +0.00 | -0.07 | +0.00 |
| 22 | +0.07 | -0.07 (-95%) | +0.00 (0%) | +0.00 (0%) | +0.07 (100%) |
| 24 | -0.07 | -0.07 (100%) | +0.00 (-0%) | +0.00 (-6%) | -0.07 (100%) |
| 26 | +0.06 | -0.07 (-121%) | +0.00 (0%) | -0.07 (-121%) | +0.06 (100%) |
| 28 | -0.00 | -0.07 | +0.00 | +0.00 | -0.00 |
| 30 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
