# CDIM — Llama-3.3-70B-Instruct (bf16), paraphrase/P4_T1 (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +12.156 (greedy 'Drive<|eot_id|>'); 80 layers, 187 tokens; rows = embedding + each layer output; 692.2 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +10.60 | +1.56 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +12.12 | +0.04 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +9.69 | +2.47 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +12.07 | +0.09 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +10.60 | +1.56 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +10.45 | +1.70 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +12.85 | -0.69 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +12.07 | +0.08 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +11.28 | +0.87 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +11.40 | +0.75 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | +1.56 | +1.43 (4) | +1.53 | 10 | None | 40 |  |
| cf3 | +2.47 | +2.60 (10) | +2.71 | 20 | None | 38 |  |
| cf5 | +1.56 | +1.52 (4) | +1.81 | 18 | None | 38 |  |
| cf6 | +1.70 | +1.99 (10) | +2.30 | 28 | None | 38 |  |

## Primary counterfactual cf3: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +2.60 (10) | -0.19 (28) | +2.71 (8) | -0.16 (28) |
| line4 | +0.50 (22) | -0.25 (52) | +0.45 (20) | -0.09 (50) |
| line5 | +0.30 (6) | -0.25 (60) | +0.45 (8) | -0.50 (24) |
| line6 | +0.19 (30) | -0.18 (2) | +0.41 (28) | -0.09 (46) |
| line7 | +0.25 (8) | -0.18 (30) | +0.29 (14) | -0.16 (24) |
| line8 | +0.32 (28) | -0.24 (54) | +0.29 (12) | -0.09 (44) |
| line9 | +1.05 (28) | -0.36 (16) | +0.79 (30) | -0.12 (20) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +2.38 (12) | -0.18 (54) | +2.65 (2) | -0.00 (76) |
| question | +1.06 (30) | -0.24 (2) | +1.17 (20) | -0.09 (68) |
| answer_instr | +0.25 (18) | -0.25 (52) | +0.29 (28) | -0.12 (48) |
| asst_header | +0.60 (36) | -0.25 (78) | +0.83 (32) | -0.09 (56) |
| answer_site | +2.47 (68) | -0.18 (6) | +2.47 (78) | -0.09 (16) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf3 run: max |ΔM| = 0.679 nats (vs Δbeh +2.47)
- library question: M(S) = -19.14 ('walk<|eot_id|>'), M(C) = -19.54 ('walk<|eot_id|>'); the largest M reached by any single patch = -18.42 → **stays Walk**

## Path validation: line3 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +2.47 | -0.24 (-10%) | +0.00 (0%) | +0.13 (5%) | +2.47 (100%) |
| 4 | +2.56 | -0.37 (-15%) | +0.00 (0%) | +0.13 (5%) | +2.56 (100%) |
| 8 | +2.18 | -0.12 (-5%) | +0.00 (0%) | +0.12 (6%) | +2.18 (100%) |
| 12 | +2.47 | +0.93 (38%) | +0.00 (0%) | -0.07 (-3%) | +2.47 (100%) |
| 16 | +1.27 | +0.18 (14%) | +0.00 (0%) | +0.00 (0%) | +1.27 (100%) |
| 20 | +1.39 | +0.25 (18%) | +0.00 (0%) | +0.07 (5%) | +1.39 (100%) |
| 24 | +0.72 | +0.00 (0%) | +0.00 (0%) | -0.12 (-17%) | +0.72 (100%) |
| 28 | -0.19 | +0.07 (-37%) | +0.00 (-0%) | +0.05 (-27%) | -0.19 (100%) |
| 32 | -0.11 | +0.12 (-114%) | +0.00 (-0%) | +0.05 (-48%) | -0.11 (100%) |
| 36 | +0.07 | +0.00 (4%) | +0.00 (0%) | -0.12 (-171%) | +0.07 (100%) |
| 40 | +0.05 | +0.12 (237%) | +0.00 (0%) | +0.12 (237%) | +0.05 (100%) |
| 44 | +0.00 | +0.00 | +0.00 | -0.25 | +0.00 |
| 48 | +0.00 | +0.00 | +0.00 | -0.18 | +0.00 |
| 52 | +0.07 | +0.07 (100%) | +0.00 (0%) | +0.07 (105%) | +0.07 (100%) |
| 56 | +0.07 | +0.00 (0%) | +0.00 (0%) | +0.00 (5%) | +0.07 (100%) |
| 60 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 64 | +0.00 | +0.12 | +0.00 | +0.00 | +0.00 |
| 68 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 72 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
