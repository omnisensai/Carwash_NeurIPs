# CDIM — Llama-3.3-70B-Instruct (bf16), paraphrase/P0_T2 (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +15.555 (greedy 'Drive<|eot_id|>'); 80 layers, 188 tokens; rows = embedding + each layer output; 922.3 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +14.19 | +1.36 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +15.05 | +0.50 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +13.06 | +2.50 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +15.18 | +0.37 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +12.79 | +2.76 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +14.14 | +1.42 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +16.19 | -0.63 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +15.06 | +0.50 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +13.29 | +2.26 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +13.05 | +2.50 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | +1.36 | +1.35 (2) | +1.48 | 10 | 30 | 36 |  |
| cf3 | +2.50 | +2.61 (12) | +2.75 | 26 | None | 38 |  |
| cf5 | +2.76 | +2.64 (2) | +2.65 | 26 | None | 38 |  |
| cf6 | +1.42 | +1.67 (12) | +1.66 | 28 | None | 34 |  |
| cf9 | +2.26 | +2.88 (22) | +2.76 | 28 | 30 | 40 |  |
| cf9s | +2.50 | +3.50 (22) | +4.14 | 28 | 30 | 38 |  |

## Primary counterfactual cf5: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +2.64 (2) | -0.12 (48) | +2.65 (12) | -0.11 (64) |
| line6 | +0.50 (12) | -0.12 (46) | +0.51 (30) | -0.11 (74) |
| line7 | +0.37 (4) | -0.12 (46) | +0.50 (28) | -0.11 (70) |
| line8 | +0.37 (8) | -0.01 (44) | +0.38 (16) | -0.12 (6) |
| line9 | +0.74 (28) | -0.11 (40) | +0.75 (26) | -0.11 (42) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +2.62 (4) | -0.12 (48) | +2.64 (4) | -0.11 (76) |
| question | +0.75 (30) | +0.00 (60) | +0.63 (30) | +0.00 (74) |
| answer_instr | +0.37 (2) | -0.11 (46) | +0.37 (16) | -0.12 (30) |
| asst_header | +0.50 (34) | -0.12 (56) | +0.51 (30) | -0.11 (74) |
| answer_site | +2.76 (76) | -0.12 (12) | +2.76 (76) | -0.11 (8) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf5 run: max |ΔM| = 0.750 nats (vs Δbeh +2.76)
- library question: M(S) = -17.51 ('walk<|eot_id|>'), M(C) = -17.33 ('walk<|eot_id|>'); the largest M reached by any single patch = -16.88 → **stays Walk**

## Path validation: line5 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +2.76 | +0.26 (9%) | +0.00 (0%) | -0.00 (-0%) | +2.76 (100%) |
| 4 | +2.64 | +0.37 (14%) | +0.00 (0%) | +0.00 (0%) | +2.64 (100%) |
| 8 | +2.39 | +0.38 (16%) | +0.00 (0%) | -0.01 (-0%) | +2.39 (100%) |
| 12 | +2.62 | +0.62 (24%) | +0.00 (0%) | -0.00 (-0%) | +2.62 (100%) |
| 16 | +2.12 | -0.12 (-6%) | +0.00 (0%) | -0.00 (-0%) | +2.12 (100%) |
| 20 | +1.75 | +0.00 (0%) | +0.00 (0%) | -0.01 (-1%) | +1.75 (100%) |
| 24 | +1.38 | -0.00 (-0%) | +0.00 (0%) | +0.00 (0%) | +1.38 (100%) |
| 28 | +1.25 | +0.25 (20%) | +0.00 (0%) | +0.12 (10%) | +1.25 (100%) |
| 32 | +0.63 | +0.00 (0%) | +0.00 (0%) | +0.12 (18%) | +0.63 (100%) |
| 36 | +0.11 | -0.00 (-0%) | +0.00 (0%) | +0.00 (0%) | +0.11 (100%) |
| 40 | +0.00 | +0.00 | +0.00 | -0.01 | +0.00 |
| 44 | +0.00 | -0.00 | +0.00 | -0.00 | +0.00 |
| 48 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) | -0.12 (100%) |
| 52 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |
| 56 | -0.01 | -0.00 | +0.00 | +0.00 | -0.01 |
| 60 | -0.00 | -0.00 | +0.00 | -0.11 | -0.00 |
| 64 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |
| 68 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |
| 72 | -0.00 | +0.00 | +0.00 | +0.00 | -0.00 |
| 76 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
