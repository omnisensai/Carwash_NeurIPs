# CDIM — Llama-3.1-8B-Instruct (bf16), substrate.txt (substrate.txt)

M(S) = +1.512 (greedy 'drive<|eot_id|>'); 32 layers, 188 tokens; rows = embedding + each layer output; 510.8 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +1.89 | -0.38 | 'drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +1.39 | +0.12 | 'drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +1.65 | -0.13 | 'drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +2.38 | -0.86 | 'drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +1.51 | +0.01 | 'drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +1.39 | +0.12 | 'drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +0.14 | +1.38 | 'drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +1.64 | -0.13 | 'drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | -0.23 | +1.74 | 'walk<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | -0.47 | +1.98 | 'walk<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | -0.38 | -0.74 (3) | -0.50 | 6 | 8 | 15 | -0.99 |
| cf2 | +0.12 | +0.25 (4) | +0.24 | 20 | 3 | 9 | +0.37 |
| cf3 | -0.13 | -0.25 (3) | -0.13 | 21 | None | 15 | +0.86 |
| cf4 | -0.86 | -0.86 (2) | -0.75 | 8 | 12 | 15 | -0.37 |
| cf5 | +0.01 | +0.13 (8) | +0.25 | 30 | 2 | 2 | +0.49 |
| cf6 | +0.12 | +0.24 (8) | +0.12 | 25 | 1 | 4 | +0.01 |
| cf7 | +1.38 | +1.38 (4) | +1.50 | 8 | None | 15 | -0.74 |
| cf8 | -0.13 | -0.25 (1) | -0.25 | 21 | None | 21 | +0.37 |
| cf9 | +1.74 | +1.74 (3) | +1.86 | 12 | None | 15 | +1.11 |
| cf9s | +1.98 | +1.99 (2) | +2.11 | 12 | None | 15 | +1.11 |

## Primary counterfactual cf9s: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line2 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line3 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line4 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line5 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line6 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line7 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line8 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line9 | +1.99 (2) | -0.01 (28) | +2.11 (4) | -0.12 (22) |
| headers | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| definitions | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| system | +1.99 (2) | -0.01 (28) | +2.11 (4) | -0.12 (22) |
| question | +0.49 (13) | -0.13 (11) | +0.61 (12) | -0.12 (29) |
| answer_instr | +0.12 (5) | -0.13 (10) | +0.12 (4) | -0.12 (3) |
| asst_header | +0.25 (16) | -0.01 (11) | +0.36 (21) | -0.12 (6) |
| answer_site | +1.98 (31) | -0.01 (7) | +1.98 (32) | -0.12 (7) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf9s run: max |ΔM| = 0.389 nats (vs Δbeh +1.98)

## Path validation: line9 → question / answer site (rows 0…32)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +1.98 | -0.00 (-0%) | +0.00 (0%) | +0.12 (6%) | +1.98 (100%) |
| 2 | +1.99 | -0.00 (-0%) | +0.00 (0%) | -0.00 (-0%) | +1.99 (100%) |
| 4 | +1.87 | +0.00 (0%) | +0.00 (0%) | -0.00 (-0%) | +1.87 (100%) |
| 6 | +1.98 | -0.12 (-6%) | +0.00 (0%) | +0.12 (6%) | +1.98 (100%) |
| 8 | +1.98 | -0.00 (-0%) | +0.00 (0%) | -0.12 (-6%) | +1.98 (100%) |
| 10 | +1.74 | +0.49 (28%) | +0.00 (0%) | -0.00 (-0%) | +1.74 (100%) |
| 12 | +1.24 | +0.12 (10%) | +0.00 (0%) | +0.12 (10%) | +1.24 (100%) |
| 14 | +0.24 | +0.00 (1%) | +0.00 (0%) | +0.12 (51%) | +0.24 (100%) |
| 16 | -0.00 | +0.12 | +0.00 | +0.12 | -0.00 |
| 18 | -0.01 | +0.00 | +0.00 | -0.00 | -0.01 |
| 20 | -0.01 | -0.00 | +0.00 | -0.00 | -0.01 |
| 22 | +0.00 | -0.13 | +0.00 | +0.12 | +0.00 |
| 24 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |
| 26 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |
| 28 | -0.01 | +0.00 | +0.00 | +0.12 | -0.01 |
| 30 | +0.12 | +0.00 (0%) | +0.00 (0%) | +0.12 (100%) | +0.12 (100%) |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
