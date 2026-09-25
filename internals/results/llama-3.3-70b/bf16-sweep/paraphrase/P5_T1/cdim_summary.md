# CDIM — Llama-3.3-70B-Instruct (bf16), paraphrase/P5_T1 (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +17.563 (greedy 'Drive<|eot_id|>'); 80 layers, 188 tokens; rows = embedding + each layer output; 688.7 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +17.08 | +0.48 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +17.55 | +0.02 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +17.04 | +0.53 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +17.42 | +0.14 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +15.64 | +1.93 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +16.61 | +0.95 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +15.94 | +1.62 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +17.57 | -0.01 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +15.36 | +2.20 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +14.50 | +3.06 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf5 | +1.93 | +2.17 (12) | +2.19 | 26 | 30 | 36 |  |
| cf7 | +1.62 | +1.62 (12) | +1.77 | 20 | None | 36 |  |
| cf9 | +2.20 | +2.31 (8) | +2.33 | 26 | 24 | 34 |  |
| cf9s | +3.06 | +3.18 (8) | +3.21 | 26 | 24 | 36 |  |

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
| line9 | +3.18 (8) | -0.14 (30) | +3.21 (8) | -0.12 (60) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +3.18 (8) | -0.14 (30) | +3.21 (8) | -0.12 (60) |
| question | +1.91 (30) | -0.25 (16) | +1.41 (30) | -0.24 (2) |
| answer_instr | +0.26 (2) | -0.12 (8) | +0.02 (34) | -0.12 (26) |
| asst_header | +1.80 (32) | -0.13 (56) | +1.79 (32) | -0.12 (18) |
| answer_site | +3.30 (44) | -0.12 (14) | +3.31 (44) | -0.12 (28) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf9s run: max |ΔM| = 1.389 nats (vs Δbeh +3.06)
- library question: M(S) = -16.54 ('walk<|eot_id|>'), M(C) = -16.85 ('Walk<|eot_id|>'); the largest M reached by any single patch = -15.65 → **stays Walk**

## Path validation: line9 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +3.06 | -0.12 (-4%) | +0.00 (0%) | +0.00 (0%) | +3.06 (100%) |
| 4 | +3.17 | -0.14 (-4%) | +0.00 (0%) | +0.00 (0%) | +3.17 (100%) |
| 8 | +3.18 | -0.11 (-3%) | +0.00 (0%) | -0.02 (-0%) | +3.18 (100%) |
| 12 | +3.16 | -0.13 (-4%) | +0.00 (0%) | +0.00 (0%) | +3.16 (100%) |
| 16 | +3.05 | +0.62 (21%) | +0.00 (0%) | +0.00 (0%) | +3.05 (100%) |
| 20 | +2.80 | +1.14 (41%) | +0.00 (0%) | -0.02 (-1%) | +2.80 (100%) |
| 24 | +1.90 | +0.90 (47%) | +0.00 (0%) | +0.00 (0%) | +1.90 (100%) |
| 28 | +0.62 | +0.14 (22%) | +0.00 (0%) | +0.00 (0%) | +0.62 (100%) |
| 32 | +0.01 | -0.11 | +0.00 | +0.13 | +0.01 |
| 36 | -0.11 | +0.00 (-0%) | +0.00 (-0%) | +0.25 (-225%) | -0.11 (100%) |
| 40 | -0.10 | -0.12 (127%) | +0.00 (-0%) | +0.00 (-0%) | -0.10 (100%) |
| 44 | -0.11 | -0.11 (100%) | +0.00 (-0%) | -0.00 (0%) | -0.11 (100%) |
| 48 | -0.12 | -0.12 (100%) | +0.00 (-0%) | -0.12 (100%) | -0.12 (100%) |
| 52 | -0.13 | -0.12 (100%) | +0.00 (-0%) | +0.00 (-0%) | -0.13 (100%) |
| 56 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) |
| 60 | -0.11 | -0.11 (100%) | +0.00 (-0%) | -0.11 (100%) | -0.11 (100%) |
| 64 | -0.11 | -0.00 (0%) | +0.00 (-0%) | -0.11 (100%) | -0.11 (100%) |
| 68 | -0.11 | -0.00 (0%) | +0.00 (-0%) | +0.00 (-0%) | -0.11 (100%) |
| 72 | -0.11 | -0.11 (100%) | +0.00 (-0%) | -0.11 (100%) | -0.11 (100%) |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
