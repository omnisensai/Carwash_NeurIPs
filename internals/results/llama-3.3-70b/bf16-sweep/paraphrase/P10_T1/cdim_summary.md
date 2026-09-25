# CDIM — Llama-3.3-70B-Instruct (bf16), paraphrase/P10_T1 (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +18.109 (greedy 'Drive<|eot_id|>'); 80 layers, 192 tokens; rows = embedding + each layer output; 805.9 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +17.39 | +0.72 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +18.01 | +0.10 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +16.63 | +1.48 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +17.61 | +0.50 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +16.22 | +1.89 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +16.68 | +1.43 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +17.65 | +0.46 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +17.90 | +0.21 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +15.78 | +2.33 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +15.38 | +2.73 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf3 | +1.48 | +1.75 (20) | +1.62 | 28 | 24 | 34 |  |
| cf5 | +1.89 | +2.03 (6) | +1.87 | 28 | None | 36 |  |
| cf6 | +1.43 | +1.71 (12) | +1.46 | 28 | None | 34 |  |
| cf9 | +2.33 | +2.71 (14) | +2.56 | 26 | None | 34 |  |
| cf9s | +2.73 | +3.14 (10) | +2.96 | 26 | None | 36 |  |

## Primary counterfactual cf9s: R and D by group (max over rows ≥ 1, and the row)

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
| line9 | +3.14 (10) | -0.12 (50) | +2.96 (16) | -0.25 (68) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +3.14 (10) | -0.12 (50) | +2.96 (16) | -0.25 (68) |
| question | +0.95 (30) | -0.28 (22) | +1.50 (30) | -0.15 (14) |
| answer_instr | +0.03 (60) | -0.15 (18) | +0.23 (16) | -0.26 (14) |
| asst_header | +1.07 (28) | -0.32 (50) | +1.06 (32) | -0.39 (70) |
| answer_site | +3.12 (74) | -0.12 (14) | +3.08 (44) | -0.14 (8) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf9s run: max |ΔM| = 1.030 nats (vs Δbeh +2.73)
- library question: M(S) = -14.71 ('walk<|eot_id|>'), M(C) = -15.01 ('walk<|eot_id|>'); the largest M reached by any single patch = -14.18 → **stays Walk**

## Path validation: line9 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +2.73 | -0.03 (-1%) | +0.00 (0%) | +0.00 (0%) | +2.73 (100%) |
| 4 | +2.62 | +0.05 (2%) | +0.00 (0%) | -0.12 (-5%) | +2.62 (100%) |
| 8 | +2.73 | +0.03 (1%) | +0.00 (0%) | -0.10 (-4%) | +2.73 (100%) |
| 12 | +2.75 | -0.38 (-14%) | +0.00 (0%) | -0.13 (-5%) | +2.75 (100%) |
| 16 | +2.61 | -0.13 (-5%) | +0.00 (0%) | -0.12 (-5%) | +2.61 (100%) |
| 20 | +2.48 | +0.55 (22%) | +0.00 (0%) | -0.10 (-4%) | +2.48 (100%) |
| 24 | +2.48 | +0.70 (28%) | +0.00 (0%) | -0.10 (-4%) | +2.48 (100%) |
| 28 | +1.07 | +0.28 (26%) | +0.00 (0%) | -0.10 (-9%) | +1.07 (100%) |
| 32 | +0.05 | +0.03 (51%) | +0.00 (0%) | +0.03 (51%) | +0.05 (100%) |
| 36 | +0.03 | +0.00 | +0.00 | +0.00 | +0.03 |
| 40 | -0.00 | +0.03 | +0.00 | -0.00 | -0.00 |
| 44 | -0.10 | -0.10 (100%) | +0.00 (-0%) | -0.00 (0%) | -0.10 (100%) |
| 48 | -0.00 | +0.00 | +0.00 | -0.10 | -0.00 |
| 52 | -0.10 | -0.10 (101%) | +0.00 (-0%) | -0.10 (100%) | -0.10 (100%) |
| 56 | -0.00 | -0.10 | +0.00 | -0.10 | -0.00 |
| 60 | -0.10 | +0.03 (-26%) | +0.00 (-0%) | -0.10 (99%) | -0.10 (100%) |
| 64 | -0.10 | +0.03 (-27%) | +0.00 (-0%) | +0.00 (-0%) | -0.10 (100%) |
| 68 | -0.10 | +0.00 (-0%) | +0.00 (-0%) | -0.10 (100%) | -0.10 (100%) |
| 72 | +0.03 | +0.00 | +0.00 | -0.00 | +0.03 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
