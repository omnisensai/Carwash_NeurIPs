# CDIM — Llama-3.3-70B-Instruct (bf16), paraphrase/P3_T1 (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +15.814 (greedy 'Drive<|eot_id|>'); 80 layers, 193 tokens; rows = embedding + each layer output; 709.0 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +14.56 | +1.25 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +15.82 | -0.01 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +14.56 | +1.25 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +15.70 | +0.12 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +15.08 | +0.74 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +14.78 | +1.04 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +17.47 | -1.66 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +15.83 | -0.01 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +15.80 | +0.02 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +15.05 | +0.77 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | +1.25 | +1.37 (4) | +1.37 | 12 | 28 | 36 |  |
| cf3 | +1.25 | +1.76 (22) | +1.62 | 28 | 24 | 40 |  |
| cf6 | +1.04 | +1.28 (4) | +1.05 | 28 | 30 | 36 |  |
| cf7 | -1.66 | -1.66 (8) | -1.53 | 26 | 24 | 40 |  |

## Primary counterfactual cf7: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line6 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line7 | +0.25 (70) | -1.66 (8) | +0.00 (50) | -1.53 (2) |
| line8 | +0.37 (38) | -0.37 (8) | +0.26 (20) | -0.37 (12) |
| line9 | +0.25 (28) | -0.25 (18) | +0.52 (24) | -0.25 (8) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +0.13 (64) | -1.79 (16) | +0.01 (46) | -1.66 (14) |
| question | +0.13 (54) | -0.88 (24) | +0.12 (14) | -0.89 (24) |
| answer_instr | +0.25 (56) | -0.13 (2) | +0.01 (22) | -0.38 (4) |
| asst_header | +0.13 (12) | -0.63 (36) | +0.12 (6) | -0.64 (36) |
| answer_site | +0.12 (16) | -1.66 (80) | +0.01 (16) | -1.66 (78) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf7 run: max |ΔM| = 0.508 nats (vs Δbeh -1.66)
- library question: M(S) = -14.16 ('Walk<|eot_id|>'), M(C) = -13.78 ('walk<|eot_id|>'); the largest M reached by any single patch = -13.16 → **stays Walk**

## Path validation: line7 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | -1.66 | -0.12 (8%) | +0.00 (-0%) | -0.12 (7%) | -1.66 (100%) |
| 4 | -1.28 | -0.12 (10%) | +0.00 (-0%) | -0.00 (0%) | -1.28 (100%) |
| 8 | -1.66 | -0.12 (8%) | +0.00 (-0%) | -0.12 (8%) | -1.66 (100%) |
| 12 | -1.41 | +0.25 (-18%) | +0.00 (-0%) | +0.00 (-0%) | -1.41 (100%) |
| 16 | -1.66 | -0.26 (16%) | +0.00 (-0%) | -0.12 (8%) | -1.66 (100%) |
| 20 | -1.66 | -0.38 (23%) | +0.00 (-0%) | -0.12 (8%) | -1.66 (100%) |
| 24 | -1.02 | -0.25 (25%) | +0.00 (-0%) | +0.00 (-0%) | -1.02 (100%) |
| 28 | -0.38 | -0.13 (34%) | +0.00 (-0%) | -0.00 (1%) | -0.38 (100%) |
| 32 | -0.25 | -0.12 (51%) | +0.00 (-0%) | +0.25 (-101%) | -0.25 (100%) |
| 36 | +0.12 | -0.12 (-103%) | +0.00 (0%) | -0.00 (-0%) | +0.12 (100%) |
| 40 | -0.12 | -0.12 (100%) | +0.00 (-0%) | -0.00 (0%) | -0.12 (100%) |
| 44 | -0.13 | -0.12 (97%) | +0.00 (-0%) | -0.12 (94%) | -0.13 (100%) |
| 48 | +0.12 | -0.12 (-100%) | +0.00 (0%) | +0.00 (3%) | +0.12 (100%) |
| 52 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | -0.12 (97%) | -0.12 (100%) |
| 56 | -0.12 | -0.12 (97%) | +0.00 (-0%) | -0.12 (97%) | -0.12 (100%) |
| 60 | +0.00 | -0.12 | +0.00 | -0.12 | +0.00 |
| 64 | +0.13 | +0.00 (0%) | +0.00 (0%) | +0.00 (0%) | +0.13 (100%) |
| 68 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) | -0.12 (100%) |
| 72 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 76 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
