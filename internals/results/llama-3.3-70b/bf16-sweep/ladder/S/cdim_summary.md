# CDIM — Llama-3.3-70B-Instruct (bf16), ladder/S (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +15.014 (greedy 'Drive<|eot_id|>'); 80 layers, 188 tokens; rows = embedding + each layer output; 804.7 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +14.53 | +0.49 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +14.78 | +0.24 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +13.50 | +1.51 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +14.91 | +0.10 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +13.15 | +1.86 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +13.80 | +1.21 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +15.05 | -0.03 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +14.67 | +0.34 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +13.22 | +1.80 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +13.11 | +1.90 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf3 | +1.51 | +1.64 (4) | +1.61 | 26 | 20 | 42 |  |
| cf5 | +1.86 | +1.74 (2) | +1.75 | 26 | None | 38 |  |
| cf6 | +1.21 | +1.35 (10) | +1.46 | 20 | None | 38 |  |
| cf9 | +1.80 | +2.14 (22) | +1.82 | 26 | 28 | 34 |  |
| cf9s | +1.90 | +2.29 (22) | +2.94 | 28 | 30 | 36 |  |

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
| line9 | +2.29 (22) | -0.37 (34) | +2.94 (22) | -0.13 (58) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +2.29 (22) | -0.37 (34) | +2.94 (22) | -0.13 (58) |
| question | +1.52 (30) | -1.18 (22) | +1.14 (30) | -0.52 (22) |
| answer_instr | +0.25 (10) | -0.12 (40) | +0.25 (24) | -0.13 (52) |
| asst_header | +1.14 (28) | -0.27 (74) | +0.80 (32) | -0.25 (42) |
| answer_site | +1.90 (72) | -0.11 (16) | +2.15 (46) | -0.24 (14) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf9s run: max |ΔM| = 0.875 nats (vs Δbeh +1.90)
- library question: M(S) = -14.53 ('walk<|eot_id|>'), M(C) = -14.13 ('walk<|eot_id|>'); the largest M reached by any single patch = -13.54 → **stays Walk**

## Path validation: line9 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +1.90 | -0.00 (-0%) | +0.00 (0%) | -0.02 (-1%) | +1.90 (100%) |
| 4 | +1.65 | +0.02 (1%) | +0.00 (0%) | -0.02 (-1%) | +1.65 (100%) |
| 8 | +1.78 | +0.11 (6%) | +0.00 (0%) | +0.00 (0%) | +1.78 (100%) |
| 12 | +1.78 | -0.02 (-1%) | +0.00 (0%) | -0.02 (-1%) | +1.78 (100%) |
| 16 | +1.90 | -0.29 (-15%) | +0.00 (0%) | +0.00 (0%) | +1.90 (100%) |
| 20 | +2.04 | +0.37 (18%) | +0.00 (0%) | -0.00 (-0%) | +2.04 (100%) |
| 24 | +1.90 | +0.89 (47%) | +0.00 (0%) | -0.00 (-0%) | +1.90 (100%) |
| 28 | +0.98 | +0.29 (30%) | +0.00 (0%) | +0.12 (13%) | +0.98 (100%) |
| 32 | -0.11 | -0.11 (100%) | +0.00 (-0%) | -0.12 (114%) | -0.11 (100%) |
| 36 | -0.00 | -0.02 | +0.00 | +0.00 | -0.00 |
| 40 | -0.12 | -0.00 (0%) | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) |
| 44 | -0.02 | -0.02 | +0.00 | +0.00 | -0.02 |
| 48 | -0.02 | +0.00 | +0.00 | -0.00 | -0.02 |
| 52 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | -0.02 (14%) | -0.12 (100%) |
| 56 | -0.02 | +0.00 | +0.00 | +0.00 | -0.02 |
| 60 | -0.02 | -0.00 | +0.00 | -0.02 | -0.02 |
| 64 | +0.00 | +0.00 | +0.00 | -0.02 | +0.00 |
| 68 | +0.00 | -0.02 | +0.00 | +0.00 | +0.00 |
| 72 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
