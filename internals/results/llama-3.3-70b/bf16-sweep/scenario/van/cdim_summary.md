# CDIM — Llama-3.3-70B-Instruct (bf16), scenario/van (internals/cdim_sweep/generated/substrates/van/S.txt)

M(S) = +15.235 (greedy 'Drive<|eot_id|>'); 80 layers, 188 tokens; rows = embedding + each layer output; 573.0 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +14.89 | +0.35 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +15.23 | +0.00 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +14.39 | +0.85 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +15.00 | +0.23 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +13.49 | +1.75 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +14.05 | +1.18 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +15.66 | -0.43 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +15.40 | -0.17 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +14.65 | +0.58 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +14.18 | +1.06 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf5 | +1.75 | +2.01 (2) | +1.73 | 28 | None | 38 |  |
| cf6 | +1.18 | +1.57 (12) | +1.36 | 28 | None | 36 |  |
| cf9s | +1.06 | +1.59 (22) | +1.46 | 26 | 28 | 36 |  |

## Primary counterfactual cf5: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +2.01 (2) | -0.02 (42) | +1.73 (2) | -0.11 (42) |
| line6 | +0.39 (10) | -0.00 (38) | +0.02 (10) | -0.25 (18) |
| line7 | +0.37 (26) | -0.02 (46) | +0.02 (28) | -0.39 (4) |
| line8 | +0.37 (22) | -0.02 (50) | +0.02 (50) | -0.12 (6) |
| line9 | +0.52 (24) | -0.02 (68) | +0.38 (18) | -0.12 (6) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +1.87 (8) | -0.00 (46) | +1.75 (2) | -0.12 (44) |
| question | +0.86 (24) | -0.02 (54) | +0.62 (30) | -0.12 (12) |
| answer_instr | +0.37 (20) | -0.02 (48) | +0.02 (8) | -0.27 (32) |
| asst_header | +0.75 (34) | -0.02 (12) | +0.63 (32) | -0.37 (6) |
| answer_site | +2.00 (60) | -0.02 (6) | +1.77 (68) | -0.12 (18) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf5 run: max |ΔM| = 0.529 nats (vs Δbeh +1.75)
- library question: M(S) = -14.53 ('walk<|eot_id|>'), M(C) = -14.51 ('walk<|eot_id|>'); the largest M reached by any single patch = -14.14 → **stays Walk**

## Path validation: line5 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +1.75 | +0.37 (21%) | +0.00 (0%) | -0.00 (-0%) | +1.75 (100%) |
| 4 | +1.86 | +0.25 (13%) | +0.00 (0%) | -0.00 (-0%) | +1.86 (100%) |
| 8 | +1.75 | -0.00 (-0%) | +0.00 (0%) | +0.00 (0%) | +1.75 (100%) |
| 12 | +1.86 | +0.37 (20%) | +0.00 (0%) | -0.02 (-1%) | +1.86 (100%) |
| 16 | +1.62 | +0.23 (14%) | +0.00 (0%) | +0.00 (0%) | +1.62 (100%) |
| 20 | +1.36 | +0.11 (8%) | +0.00 (0%) | -0.00 (-0%) | +1.36 (100%) |
| 24 | +1.12 | +0.00 (0%) | +0.00 (0%) | +0.25 (22%) | +1.12 (100%) |
| 28 | +1.14 | +0.12 (11%) | +0.00 (0%) | +0.00 (0%) | +1.14 (100%) |
| 32 | +0.50 | +0.00 (0%) | +0.00 (0%) | +0.36 (71%) | +0.50 (100%) |
| 36 | +0.12 | -0.00 (-1%) | +0.00 (0%) | -0.00 (-1%) | +0.12 (100%) |
| 40 | +0.00 | +0.00 | +0.00 | -0.02 | +0.00 |
| 44 | +0.11 | +0.11 (100%) | +0.00 (0%) | +0.00 (0%) | +0.11 (100%) |
| 48 | +0.11 | -0.00 (-0%) | +0.00 (0%) | +0.00 (0%) | +0.11 (100%) |
| 52 | +0.11 | +0.11 (99%) | +0.00 (0%) | -0.00 (-0%) | +0.11 (100%) |
| 56 | +0.11 | -0.02 (-16%) | +0.00 (0%) | +0.11 (100%) | +0.11 (100%) |
| 60 | +0.11 | -0.00 (-0%) | +0.00 (0%) | +0.25 (234%) | +0.11 (100%) |
| 64 | +0.00 | +0.23 | +0.00 | +0.00 | +0.00 |
| 68 | -0.00 | -0.02 | +0.00 | +0.00 | -0.00 |
| 72 | +0.11 | +0.00 (0%) | +0.00 (0%) | +0.11 (100%) | +0.11 (100%) |
| 76 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
