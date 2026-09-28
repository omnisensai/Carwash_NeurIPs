# CDIM — Llama-3.2-3B-Instruct (bf16), substrate.txt (substrate.txt)

M(S) = +0.177 (greedy 'drive<|eot_id|>'); 28 layers, 188 tokens; rows = embedding + each layer output; 410.3 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +0.30 | -0.12 | 'drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +0.18 | +0.00 | 'drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +0.06 | +0.11 | 'walk<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +0.18 | -0.01 | 'drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +0.30 | -0.12 | 'drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +0.66 | -0.48 | 'drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | -0.45 | +0.62 | 'walk<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +0.30 | -0.12 | 'drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | -0.33 | +0.50 | 'walk<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | -0.32 | +0.50 | 'walk<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | -0.12 | -0.13 (10) | -0.24 | 12 | 12 | 19 | -0.12 |
| cf2 | +0.00 | +0.12 (15) | +0.13 | 26 | 2 | 15 | -0.13 |
| cf3 | +0.11 | +0.12 (13) | +0.24 | 3 | 9 | 19 | +0.11 |
| cf4 | -0.01 | -0.01 (12) | -0.01 | 17 | 1 | 17 | -0.12 |
| cf5 | -0.12 | -0.25 (9) | -0.24 | 11 | 6 | 16 | +0.13 |
| cf6 | -0.48 | -0.61 (8) | -0.61 | 10 | None | 16 | +0.01 |
| cf7 | +0.62 | +0.86 (9) | +0.75 | 12 | 11 | 15 | -0.63 |
| cf8 | -0.12 | -0.25 (1) | -0.12 | 16 | 1 | 6 | -0.25 |
| cf9 | +0.50 | +0.51 (5) | +0.50 | 10 | 10 | 16 | +0.61 |
| cf9s | +0.50 | +0.50 (1) | +0.50 | 9 | 11 | 16 | +0.61 |

## Primary counterfactual cf7: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line2 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line3 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line4 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line5 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line6 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line7 | +0.86 (9) | -0.00 (22) | +0.75 (9) | -0.12 (27) |
| line8 | +0.12 (2) | -0.12 (11) | +0.12 (3) | -0.12 (11) |
| line9 | +0.12 (3) | -0.00 (23) | +0.12 (8) | -0.12 (27) |
| headers | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| definitions | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| system | +0.75 (3) | -0.00 (23) | +0.63 (6) | -0.12 (27) |
| question | +0.49 (12) | -0.00 (24) | +0.37 (13) | -0.12 (3) |
| answer_instr | +0.12 (4) | -0.00 (7) | +0.12 (1) | -0.01 (14) |
| asst_header | +0.25 (16) | -0.00 (4) | +0.13 (16) | -0.01 (3) |
| answer_site | +0.74 (21) | -0.00 (4) | +0.62 (28) | -0.01 (2) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf7 run: max |ΔM| = 0.492 nats (vs Δbeh +0.62)

## Path validation: line7 → question / answer site (rows 0…28)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +0.62 | +0.00 (0%) | +0.00 (0%) | -0.00 (-0%) | +0.62 (100%) |
| 2 | +0.50 | -0.00 (-0%) | +0.00 (0%) | +0.00 (0%) | +0.50 (100%) |
| 4 | +0.63 | +0.12 (19%) | +0.00 (0%) | +0.00 (0%) | +0.63 (100%) |
| 6 | +0.74 | +0.01 (1%) | +0.00 (0%) | +0.00 (0%) | +0.74 (100%) |
| 8 | +0.76 | +0.12 (16%) | +0.00 (0%) | +0.12 (15%) | +0.76 (100%) |
| 10 | +0.51 | +0.24 (48%) | +0.00 (0%) | +0.00 (0%) | +0.51 (100%) |
| 12 | +0.37 | +0.24 (65%) | +0.00 (0%) | +0.12 (33%) | +0.37 (100%) |
| 14 | +0.12 | +0.00 (2%) | +0.00 (0%) | +0.12 (100%) | +0.12 (100%) |
| 16 | +0.12 | +0.00 (2%) | +0.00 (0%) | +0.00 (2%) | +0.12 (100%) |
| 18 | +0.00 | +0.00 | +0.00 | +0.12 | +0.00 |
| 20 | +0.00 | -0.00 | +0.00 | +0.00 | +0.00 |
| 22 | -0.00 | -0.00 | +0.00 | +0.00 | -0.00 |
| 24 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |
| 26 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
