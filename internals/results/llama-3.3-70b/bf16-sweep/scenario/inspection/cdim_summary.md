# CDIM — Llama-3.3-70B-Instruct (bf16), scenario/inspection (internals/cdim_sweep/generated/substrates/inspection/S.txt)

M(S) = +13.217 (greedy 'Drive<|eot_id|>'); 80 layers, 192 tokens; rows = embedding + each layer output; 810.8 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +12.51 | +0.70 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +12.98 | +0.23 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +12.20 | +1.02 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +13.13 | +0.09 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +11.97 | +1.25 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +11.97 | +1.24 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +13.61 | -0.39 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +13.26 | -0.05 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +11.59 | +1.62 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +11.30 | +1.92 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf3 | +1.02 | +1.37 (12) | +1.27 | 26 | 20 | 40 |  |
| cf5 | +1.25 | +1.41 (28) | +1.50 | 28 | None | 38 |  |
| cf6 | +1.24 | +1.39 (8) | +1.44 | 28 | 30 | 38 |  |
| cf9 | +1.62 | +2.21 (26) | +1.89 | 30 | 30 | 34 |  |
| cf9s | +1.92 | +2.54 (22) | +2.91 | 30 | 30 | 38 |  |

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
| line9 | +2.54 (22) | -0.12 (44) | +2.91 (22) | -0.25 (40) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +2.54 (22) | -0.12 (44) | +2.91 (22) | -0.25 (40) |
| question | +1.40 (30) | -1.02 (22) | +0.52 (32) | -0.64 (22) |
| answer_instr | +0.37 (20) | -0.02 (38) | +0.02 (76) | -0.25 (10) |
| asst_header | +0.56 (32) | -0.42 (70) | +0.74 (32) | -0.27 (72) |
| answer_site | +2.06 (42) | -0.02 (18) | +2.17 (48) | -0.23 (16) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf9s run: max |ΔM| = 0.938 nats (vs Δbeh +1.92)
- library question: M(S) = -15.26 ('walk<|eot_id|>'), M(C) = -16.22 ('Walk<|eot_id|>'); the largest M reached by any single patch = -14.89 → **stays Walk**

## Path validation: line9 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +1.92 | -0.00 (-0%) | +0.00 (0%) | -0.00 (-0%) | +1.92 (100%) |
| 4 | +2.04 | -0.00 (-0%) | +0.00 (0%) | -0.00 (-0%) | +2.04 (100%) |
| 8 | +2.04 | -0.12 (-6%) | +0.00 (0%) | +0.00 (0%) | +2.04 (100%) |
| 12 | +2.06 | -0.48 (-23%) | +0.00 (0%) | +0.00 (0%) | +2.06 (100%) |
| 16 | +2.15 | -0.12 (-6%) | +0.00 (0%) | -0.00 (-0%) | +2.15 (100%) |
| 20 | +2.16 | -0.00 (-0%) | +0.00 (0%) | -0.02 (-1%) | +2.16 (100%) |
| 24 | +2.42 | +0.75 (31%) | +0.00 (0%) | -0.00 (-0%) | +2.42 (100%) |
| 28 | +2.15 | +0.79 (37%) | +0.00 (0%) | +0.13 (6%) | +2.15 (100%) |
| 32 | +0.31 | -0.10 (-34%) | +0.00 (0%) | +0.04 (13%) | +0.31 (100%) |
| 36 | +0.27 | -0.02 (-9%) | +0.00 (0%) | +0.02 (8%) | +0.27 (100%) |
| 40 | -0.02 | +0.10 | +0.00 | +0.00 | -0.02 |
| 44 | -0.12 | -0.00 (0%) | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) |
| 48 | -0.10 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-0%) | -0.10 (100%) |
| 52 | -0.02 | +0.00 | +0.00 | +0.00 | -0.02 |
| 56 | -0.12 | -0.00 (0%) | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) |
| 60 | -0.12 | -0.02 (19%) | +0.00 (-0%) | -0.02 (19%) | -0.12 (100%) |
| 64 | +0.00 | +0.00 | +0.00 | +0.10 | +0.00 |
| 68 | -0.00 | +0.00 | +0.00 | -0.02 | -0.00 |
| 72 | -0.02 | +0.00 | +0.00 | -0.02 | -0.02 |
| 76 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
