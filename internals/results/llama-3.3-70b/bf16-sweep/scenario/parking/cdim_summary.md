# CDIM — Llama-3.3-70B-Instruct (bf16), scenario/parking (internals/cdim_sweep/generated/substrates/parking/S.txt)

M(S) = +2.042 (greedy 'Drive<|eot_id|>'); 80 layers, 189 tokens; rows = embedding + each layer output; 1170.4 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +1.81 | +0.23 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +0.20 | +1.84 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | -4.66 | +6.70 | 'walk<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +2.79 | -0.75 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +0.88 | +1.16 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +0.60 | +1.44 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +9.27 | -7.23 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +3.51 | -1.46 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | -3.99 | +6.03 | 'Walk<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | -2.99 | +5.03 | 'Walk<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf2 | +1.84 | +1.99 (14) | +2.34 | 26 | 20 | 40 |  |
| cf3 | +6.70 | +7.12 (12) | +6.96 | 24 | None | 40 |  |
| cf5 | +1.16 | +1.91 (28) | +1.91 | 28 | None | 34 |  |
| cf6 | +1.44 | +2.61 (26) | +4.14 | 32 | None | 34 |  |
| cf7 | -7.23 | -7.32 (2) | -7.04 | 20 | None | 40 |  |
| cf8 | -1.46 | -1.97 (14) | -2.15 | 22 | None | 40 |  |
| cf9 | +6.03 | +6.55 (22) | +7.94 | 28 | 30 | 36 |  |
| cf9s | +5.03 | +7.51 (22) | +7.57 | 28 | 30 | 36 |  |

## Primary counterfactual cf7: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line6 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line7 | +0.00 (76) | -7.32 (2) | +0.21 (38) | -7.04 (4) |
| line8 | +0.00 (50) | -2.17 (14) | +0.47 (32) | -1.40 (28) |
| line9 | +0.00 (2) | -1.42 (30) | +0.85 (14) | -1.54 (30) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +0.00 (78) | -7.69 (8) | +0.00 (80) | -7.24 (16) |
| question | +0.00 (58) | -1.19 (28) | +0.35 (14) | -2.11 (26) |
| answer_instr | +0.00 (34) | -0.42 (32) | +0.59 (4) | -0.15 (26) |
| asst_header | +0.00 (80) | -1.80 (36) | +0.25 (4) | -2.41 (34) |
| answer_site | -0.00 (18) | -7.23 (80) | +0.34 (26) | -7.23 (80) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf7 run: max |ΔM| = 1.810 nats (vs Δbeh -7.23)
- library question: M(S) = -17.17 ('walk<|eot_id|>'), M(C) = -16.54 ('walk<|eot_id|>'); the largest M reached by any single patch = -16.10 → **stays Walk**

## Path validation: line7 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | -7.23 | -0.36 (5%) | +0.00 (-0%) | -0.00 (0%) | -7.23 (100%) |
| 4 | -6.98 | -0.13 (2%) | +0.00 (-0%) | -0.19 (3%) | -6.98 (100%) |
| 8 | -6.82 | +0.00 (-0%) | +0.00 (-0%) | -0.30 (4%) | -6.82 (100%) |
| 12 | -5.98 | -0.00 (0%) | +0.00 (-0%) | -0.06 (1%) | -5.98 (100%) |
| 16 | -5.95 | -0.19 (3%) | +0.00 (-0%) | -0.37 (6%) | -5.95 (100%) |
| 20 | -3.89 | -0.80 (21%) | +0.00 (-0%) | -0.12 (3%) | -3.89 (100%) |
| 24 | -2.12 | -0.25 (12%) | +0.00 (-0%) | -0.12 (6%) | -2.12 (100%) |
| 28 | -1.56 | -0.25 (16%) | +0.00 (-0%) | -0.00 (0%) | -1.56 (100%) |
| 32 | -0.68 | -0.43 (63%) | +0.00 (-0%) | -0.20 (30%) | -0.68 (100%) |
| 36 | -0.13 | -0.37 (293%) | +0.00 (-0%) | -0.12 (100%) | -0.13 (100%) |
| 40 | -0.37 | -0.30 (82%) | +0.00 (-0%) | -0.30 (82%) | -0.37 (100%) |
| 44 | -0.12 | -0.30 (242%) | +0.00 (-0%) | -0.12 (100%) | -0.12 (100%) |
| 48 | -0.12 | -0.07 (55%) | +0.00 (-0%) | +0.05 (-40%) | -0.12 (100%) |
| 52 | -0.00 | -0.06 | +0.00 | -0.12 | -0.00 |
| 56 | -0.31 | -0.07 (22%) | +0.00 (-0%) | -0.31 (100%) | -0.31 (100%) |
| 60 | -0.24 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.24 (100%) |
| 64 | -0.31 | -0.07 (22%) | +0.00 (-0%) | -0.07 (24%) | -0.31 (100%) |
| 68 | -0.00 | +0.00 | +0.00 | +0.00 | -0.00 |
| 72 | -0.31 | -0.07 (22%) | +0.00 (-0%) | -0.32 (103%) | -0.31 (100%) |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
