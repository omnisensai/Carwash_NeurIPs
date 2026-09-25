# CDIM — Llama-3.3-70B-Instruct (bf16), paraphrase/P9_T1 (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +17.047 (greedy 'Drive<|eot_id|>'); 80 layers, 190 tokens; rows = embedding + each layer output; 804.6 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +16.06 | +0.99 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +16.92 | +0.12 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +15.57 | +1.48 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +16.92 | +0.12 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +15.29 | +1.76 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +15.76 | +1.28 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +17.08 | -0.03 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +16.81 | +0.23 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +15.01 | +2.03 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +14.62 | +2.42 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf3 | +1.48 | +1.60 (12) | +1.37 | 22 | 22 | 36 |  |
| cf5 | +1.76 | +1.77 (16) | +1.88 | 28 | None | 36 |  |
| cf6 | +1.28 | +1.40 (6) | +1.44 | 26 | None | 38 |  |
| cf9 | +2.03 | +2.27 (16) | +2.53 | 26 | 30 | 36 |  |
| cf9s | +2.42 | +2.55 (20) | +2.67 | 26 | None | 36 |  |

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
| line9 | +2.55 (20) | -0.12 (42) | +2.67 (16) | -0.00 (62) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +2.55 (20) | -0.12 (42) | +2.67 (16) | -0.00 (62) |
| question | +1.16 (30) | -0.39 (16) | +1.76 (30) | -0.12 (2) |
| answer_instr | +0.01 (12) | -0.12 (4) | +0.25 (38) | -0.12 (16) |
| asst_header | +0.87 (28) | -0.27 (50) | +1.15 (32) | -0.12 (12) |
| answer_site | +2.42 (78) | -0.12 (12) | +2.67 (78) | -0.01 (2) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf9s run: max |ΔM| = 1.015 nats (vs Δbeh +2.42)
- library question: M(S) = -15.07 ('walk<|eot_id|>'), M(C) = -13.67 ('walk<|eot_id|>'); the largest M reached by any single patch = -13.46 → **stays Walk**

## Path validation: line9 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +2.42 | +0.00 (0%) | +0.00 (0%) | +0.00 (0%) | +2.42 (100%) |
| 4 | +2.17 | +0.12 (6%) | +0.00 (0%) | -0.00 (-0%) | +2.17 (100%) |
| 8 | +2.17 | +0.01 (1%) | +0.00 (0%) | -0.00 (-0%) | +2.17 (100%) |
| 12 | +2.17 | -0.50 (-23%) | +0.00 (0%) | +0.00 (0%) | +2.17 (100%) |
| 16 | +2.43 | -0.12 (-5%) | +0.00 (0%) | +0.00 (0%) | +2.43 (100%) |
| 20 | +2.55 | +0.91 (36%) | +0.00 (0%) | +0.00 (0%) | +2.55 (100%) |
| 24 | +2.16 | +0.51 (24%) | +0.00 (0%) | -0.00 (-0%) | +2.16 (100%) |
| 28 | +1.15 | +0.38 (33%) | +0.00 (0%) | +0.14 (12%) | +1.15 (100%) |
| 32 | -0.10 | +0.01 (-14%) | +0.00 (-0%) | +0.03 (-27%) | -0.10 (100%) |
| 36 | +0.00 | +0.12 | +0.00 | +0.00 | +0.00 |
| 40 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 44 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) |
| 48 | -0.11 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.11 (100%) |
| 52 | -0.11 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.11 (100%) |
| 56 | -0.11 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.11 (100%) |
| 60 | -0.11 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.11 (100%) |
| 64 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) |
| 68 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) |
| 72 | +0.00 | +0.00 | +0.00 | -0.11 | +0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
