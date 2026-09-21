# CDIM — Llama-3.3-70B-Instruct (bf16), paraphrase/P8_T1 (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +14.071 (greedy 'Drive<|eot_id|>'); 80 layers, 188 tokens; rows = embedding + each layer output; 807.0 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +13.71 | +0.36 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +13.32 | +0.75 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +11.25 | +2.82 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +13.69 | +0.38 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +12.01 | +2.06 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +12.75 | +1.32 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +13.17 | +0.90 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +13.70 | +0.37 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +10.48 | +3.59 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +10.39 | +3.68 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf3 | +2.82 | +2.81 (12) | +2.82 | 26 | None | 38 |  |
| cf5 | +2.06 | +2.04 (14) | +2.20 | 20 | None | 38 |  |
| cf6 | +1.32 | +1.83 (16) | +2.02 | 28 | 26 | 40 |  |
| cf9 | +3.59 | +3.59 (4) | +3.70 | 22 | None | 36 |  |
| cf9s | +3.68 | +3.43 (10) | +3.67 | 24 | None | 36 |  |

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
| line9 | +3.43 (10) | -0.12 (34) | +3.67 (10) | -0.12 (52) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +3.43 (10) | -0.12 (34) | +3.67 (10) | -0.12 (52) |
| question | +1.27 (30) | -0.23 (6) | +0.87 (22) | +0.00 (42) |
| answer_instr | +0.14 (4) | -0.35 (20) | +0.26 (34) | -0.12 (12) |
| asst_header | +2.43 (32) | -0.10 (6) | +2.09 (32) | -0.12 (14) |
| answer_site | +3.68 (80) | -0.12 (16) | +3.68 (80) | -0.12 (8) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf9s run: max |ΔM| = 0.875 nats (vs Δbeh +3.68)
- library question: M(S) = -13.61 ('Walk<|eot_id|>'), M(C) = -14.06 ('Walk<|eot_id|>'); the largest M reached by any single patch = -13.17 → **stays Walk**

## Path validation: line9 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +3.68 | +0.00 (0%) | +0.00 (0%) | +0.01 (0%) | +3.68 (100%) |
| 4 | +3.43 | -0.11 (-3%) | +0.00 (0%) | +0.01 (0%) | +3.43 (100%) |
| 8 | +3.43 | +0.02 (1%) | +0.00 (0%) | +0.00 (0%) | +3.43 (100%) |
| 12 | +3.29 | -0.11 (-3%) | +0.00 (0%) | +0.00 (0%) | +3.29 (100%) |
| 16 | +3.17 | +0.37 (12%) | +0.00 (0%) | +0.00 (0%) | +3.17 (100%) |
| 20 | +2.41 | +0.51 (21%) | +0.00 (0%) | +0.00 (0%) | +2.41 (100%) |
| 24 | +2.00 | +0.40 (20%) | +0.00 (0%) | +0.01 (1%) | +2.00 (100%) |
| 28 | +0.86 | +0.02 (3%) | +0.00 (0%) | +0.01 (2%) | +0.86 (100%) |
| 32 | +0.00 | +0.01 | +0.00 | +0.01 | +0.00 |
| 36 | +0.02 | -0.01 | +0.00 | +0.01 | +0.02 |
| 40 | +0.00 | +0.00 | +0.00 | +0.01 | +0.00 |
| 44 | -0.00 | +0.00 | +0.00 | +0.00 | -0.00 |
| 48 | +0.00 | +0.00 | +0.00 | +0.01 | +0.00 |
| 52 | -0.11 | +0.00 (-0%) | +0.00 (-0%) | +0.01 (-11%) | -0.11 (100%) |
| 56 | -0.11 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.11 (100%) |
| 60 | +0.00 | +0.01 | +0.00 | +0.00 | +0.00 |
| 64 | +0.00 | +0.01 | +0.00 | +0.00 | +0.00 |
| 68 | -0.11 | +0.00 (-0%) | +0.00 (-0%) | +0.01 (-11%) | -0.11 (100%) |
| 72 | +0.00 | +0.01 | +0.00 | +0.00 | +0.00 |
| 76 | +0.01 | +0.00 | +0.00 | +0.01 | +0.01 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
