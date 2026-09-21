# CDIM — Llama-3.3-70B-Instruct (bf16), paraphrase/P11_T1 (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +14.217 (greedy 'Drive<|eot_id|>'); 80 layers, 183 tokens; rows = embedding + each layer output; 817.3 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +13.51 | +0.70 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +14.48 | -0.27 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +11.91 | +2.31 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +14.76 | -0.55 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +12.53 | +1.69 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +13.18 | +1.04 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +14.75 | -0.53 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +14.15 | +0.07 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +11.62 | +2.60 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +11.74 | +2.47 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf3 | +2.31 | +2.58 (14) | +2.44 | 22 | 30 | 36 |  |
| cf5 | +1.69 | +1.71 (4) | +1.81 | 20 | None | 36 |  |
| cf6 | +1.04 | +1.86 (26) | +1.87 | 30 | None | 40 |  |
| cf9 | +2.60 | +3.36 (16) | +3.22 | 26 | 30 | 34 |  |
| cf9s | +2.47 | +3.11 (22) | +3.43 | 28 | None | 36 |  |

## Primary counterfactual cf9: R and D by group (max over rows ≥ 1, and the row)

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
| line9 | +3.36 (16) | -0.12 (34) | +3.22 (18) | -0.27 (30) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +3.36 (16) | -0.12 (34) | +3.22 (18) | -0.27 (30) |
| question | +1.66 (30) | -0.83 (22) | +1.91 (30) | -0.67 (22) |
| answer_instr | +0.16 (12) | -0.12 (74) | +0.11 (38) | -0.27 (10) |
| asst_header | +1.32 (28) | -0.71 (52) | +2.34 (32) | -0.38 (64) |
| answer_site | +2.99 (52) | -0.09 (18) | +3.26 (58) | -0.27 (8) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf9 run: max |ΔM| = 0.708 nats (vs Δbeh +2.60)
- library question: M(S) = -14.63 ('walk<|eot_id|>'), M(C) = -13.81 ('walk<|eot_id|>'); the largest M reached by any single patch = -13.38 → **stays Walk**

## Path validation: line9 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +2.60 | -0.04 (-2%) | +0.00 (0%) | +0.00 (0%) | +2.60 (100%) |
| 4 | +2.88 | -0.16 (-6%) | +0.00 (0%) | +0.00 (0%) | +2.88 (100%) |
| 8 | +2.86 | +0.00 (0%) | +0.00 (0%) | +0.08 (3%) | +2.86 (100%) |
| 12 | +2.86 | -0.12 (-4%) | +0.00 (0%) | -0.04 (-1%) | +2.86 (100%) |
| 16 | +3.36 | -0.41 (-12%) | +0.00 (0%) | +0.00 (0%) | +3.36 (100%) |
| 20 | +2.99 | +0.66 (22%) | +0.00 (0%) | +0.00 (0%) | +2.99 (100%) |
| 24 | +2.03 | +0.66 (33%) | +0.00 (0%) | +0.00 (0%) | +2.03 (100%) |
| 28 | +1.10 | +0.60 (55%) | +0.00 (0%) | +0.13 (11%) | +1.10 (100%) |
| 32 | +0.07 | +0.00 (0%) | +0.00 (0%) | +0.16 (220%) | +0.07 (100%) |
| 36 | -0.09 | -0.12 (144%) | +0.00 (-0%) | -0.09 (100%) | -0.09 (100%) |
| 40 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) |
| 44 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) |
| 48 | -0.04 | -0.12 | +0.00 | +0.00 | -0.04 |
| 52 | -0.09 | -0.12 (144%) | +0.00 (-0%) | +0.00 (-0%) | -0.09 (100%) |
| 56 | -0.09 | -0.09 (100%) | +0.00 (-0%) | +0.00 (-0%) | -0.09 (100%) |
| 60 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) |
| 64 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 68 | -0.09 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.09 (100%) |
| 72 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
