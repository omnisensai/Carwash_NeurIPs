# CDIM — Llama-3.3-70B-Instruct (bf16), paraphrase/P7_T1 (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +16.037 (greedy 'Drive<|eot_id|>'); 80 layers, 186 tokens; rows = embedding + each layer output; 687.3 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +15.30 | +0.74 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +16.04 | +0.00 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +14.29 | +1.75 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +15.66 | +0.38 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +14.26 | +1.77 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +14.37 | +1.66 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +16.94 | -0.90 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +16.18 | -0.14 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +15.14 | +0.90 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +14.50 | +1.54 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf3 | +1.75 | +2.12 (22) | +2.51 | 26 | None | 40 |  |
| cf5 | +1.77 | +1.76 (6) | +1.90 | 20 | None | 36 |  |
| cf6 | +1.66 | +1.91 (16) | +1.93 | 28 | None | 38 |  |
| cf9s | +1.54 | +1.90 (20) | +2.29 | 28 | None | 34 |  |

## Primary counterfactual cf5: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +1.76 (6) | -0.11 (62) | +1.90 (2) | -0.35 (44) |
| line6 | +0.62 (24) | -0.14 (16) | +0.26 (20) | -0.36 (74) |
| line7 | +0.13 (30) | -0.14 (16) | +0.26 (28) | -0.36 (66) |
| line8 | +0.36 (28) | -0.25 (18) | +0.26 (30) | -0.25 (74) |
| line9 | +0.64 (24) | -0.13 (8) | +0.65 (20) | -0.25 (74) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +2.00 (8) | -0.11 (62) | +2.02 (20) | +0.00 (46) |
| question | +0.61 (30) | -0.13 (6) | +0.51 (30) | -0.34 (4) |
| answer_instr | +0.26 (24) | -0.13 (4) | +0.14 (20) | -0.36 (70) |
| asst_header | +0.26 (34) | -0.38 (30) | +0.26 (34) | -0.60 (30) |
| answer_site | +2.14 (78) | -0.01 (8) | +1.89 (64) | -0.24 (16) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf5 run: max |ΔM| = 0.523 nats (vs Δbeh +1.77)
- library question: M(S) = -15.91 ('walk<|eot_id|>'), M(C) = -15.31 ('walk<|eot_id|>'); the largest M reached by any single patch = -14.88 → **stays Walk**

## Path validation: line5 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +1.77 | -0.00 (-0%) | +0.00 (0%) | +0.00 (0%) | +1.77 (100%) |
| 4 | +1.75 | -0.13 (-7%) | +0.00 (0%) | +0.01 (1%) | +1.75 (100%) |
| 8 | +1.75 | -0.01 (-1%) | +0.00 (0%) | -0.00 (-0%) | +1.75 (100%) |
| 12 | +1.75 | -0.11 (-6%) | +0.00 (0%) | -0.01 (-1%) | +1.75 (100%) |
| 16 | +1.52 | -0.12 (-8%) | +0.00 (0%) | +0.00 (0%) | +1.52 (100%) |
| 20 | +0.89 | -0.00 (-0%) | +0.00 (0%) | +0.00 (0%) | +0.89 (100%) |
| 24 | +0.61 | -0.13 (-21%) | +0.00 (0%) | -0.01 (-2%) | +0.61 (100%) |
| 28 | +0.77 | +0.00 (0%) | +0.00 (0%) | +0.12 (16%) | +0.77 (100%) |
| 32 | +0.13 | +0.01 (10%) | +0.00 (0%) | +0.11 (89%) | +0.13 (100%) |
| 36 | +0.12 | -0.00 (-0%) | +0.00 (0%) | +0.11 (89%) | +0.12 (100%) |
| 40 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |
| 44 | -0.00 | +0.00 | +0.00 | +0.00 | -0.00 |
| 48 | +0.00 | -0.00 | +0.00 | +0.00 | +0.00 |
| 52 | -0.00 | -0.00 | +0.00 | -0.00 | -0.00 |
| 56 | -0.00 | +0.00 | +0.00 | +0.00 | -0.00 |
| 60 | -0.00 | -0.00 | +0.00 | -0.00 | -0.00 |
| 64 | -0.00 | -0.00 | +0.00 | -0.12 | -0.00 |
| 68 | -0.00 | -0.00 | +0.00 | -0.00 | -0.00 |
| 72 | -0.00 | -0.00 | +0.00 | -0.00 | -0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
