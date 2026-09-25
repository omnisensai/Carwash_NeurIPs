# CDIM — Llama-3.3-70B-Instruct (bf16), scenario/fuel (internals/cdim_sweep/generated/substrates/fuel/S.txt)

M(S) = +12.301 (greedy 'Drive<|eot_id|>'); 80 layers, 191 tokens; rows = embedding + each layer output; 339.7 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +11.84 | +0.46 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +11.82 | +0.48 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +11.30 | +1.00 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +12.61 | -0.31 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +12.12 | +0.18 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +10.74 | +1.56 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +12.57 | -0.27 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +12.11 | +0.19 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +11.81 | +0.49 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +11.78 | +0.52 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf6 | +1.56 | +1.72 (12) | +1.89 | 20 | None | 38 |  |

## Primary counterfactual cf6: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line6 | +1.72 (12) | -0.25 (42) | +1.89 (6) | -0.27 (54) |
| line7 | +0.71 (20) | -0.25 (48) | +0.27 (22) | -0.27 (66) |
| line8 | +0.25 (24) | -0.34 (8) | +0.10 (30) | -0.27 (50) |
| line9 | +0.33 (16) | -0.25 (50) | +0.25 (30) | -0.27 (66) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +1.83 (12) | -0.25 (70) | +1.77 (10) | -0.27 (60) |
| question | +0.54 (26) | -0.34 (70) | +0.27 (22) | -0.40 (70) |
| answer_instr | +0.12 (34) | -0.25 (20) | +0.13 (10) | -0.27 (42) |
| asst_header | +0.79 (34) | -0.25 (2) | +0.50 (34) | -0.25 (16) |
| answer_site | +1.83 (78) | -0.17 (24) | +1.81 (76) | -0.25 (14) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf6 run: max |ΔM| = 0.375 nats (vs Δbeh +1.56)
- library question: M(S) = -12.69 ('Walk<|eot_id|>'), M(C) = -11.66 ('Walk<|eot_id|>'); the largest M reached by any single patch = -11.36 → **stays Walk**

## Path validation: line6 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +1.56 | -0.17 (-11%) | +0.00 (0%) | -0.13 (-8%) | +1.56 (100%) |
| 4 | +1.58 | -0.29 (-18%) | +0.00 (0%) | -0.12 (-8%) | +1.58 (100%) |
| 8 | +1.45 | -0.21 (-14%) | +0.00 (0%) | +0.00 (0%) | +1.45 (100%) |
| 12 | +1.72 | +0.16 (9%) | +0.00 (0%) | -0.13 (-7%) | +1.72 (100%) |
| 16 | +1.45 | +0.21 (14%) | +0.00 (0%) | -0.13 (-9%) | +1.45 (100%) |
| 20 | +0.93 | +0.21 (22%) | +0.00 (0%) | -0.13 (-13%) | +0.93 (100%) |
| 24 | +0.43 | -0.17 (-38%) | +0.00 (0%) | -0.25 (-58%) | +0.43 (100%) |
| 28 | +0.76 | -0.17 (-22%) | +0.00 (0%) | +0.12 (16%) | +0.76 (100%) |
| 32 | +0.20 | -0.13 (-63%) | +0.00 (0%) | -0.09 (-44%) | +0.20 (100%) |
| 36 | +0.04 | -0.21 | +0.00 | +0.07 | +0.04 |
| 40 | -0.17 | -0.25 (151%) | +0.00 (-0%) | -0.25 (151%) | -0.17 (100%) |
| 44 | -0.25 | -0.13 (50%) | +0.00 (-0%) | -0.21 (85%) | -0.25 (100%) |
| 48 | -0.17 | -0.00 (0%) | +0.00 (-0%) | -0.00 (1%) | -0.17 (100%) |
| 52 | -0.00 | +0.04 | +0.00 | +0.04 | -0.00 |
| 56 | -0.25 | -0.00 (0%) | +0.00 (-0%) | +0.04 (-15%) | -0.25 (100%) |
| 60 | +0.12 | -0.00 (-1%) | +0.00 (0%) | -0.00 (-0%) | +0.12 (100%) |
| 64 | +0.00 | -0.00 | +0.00 | -0.00 | +0.00 |
| 68 | -0.25 | -0.00 (0%) | +0.00 (-0%) | -0.00 (0%) | -0.25 (100%) |
| 72 | -0.25 | -0.00 (0%) | +0.00 (-0%) | -0.00 (0%) | -0.25 (100%) |
| 76 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
