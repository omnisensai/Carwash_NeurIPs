# CDIM — Llama-3.3-70B-Instruct (bf16), paraphrase/P0_T0 (internals/cdim_sweep/generated/substrates/carwash/S.txt)

M(S) = +15.250 (greedy 'Drive.<|eot_id|>'); 80 layers, 185 tokens; rows = embedding + each layer output; 929.3 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +13.50 | +1.75 | 'Drive.<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +14.50 | +0.75 | 'Drive.<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +13.62 | +1.62 | 'Drive.<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +15.37 | -0.13 | 'Drive.<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +12.87 | +2.37 | 'Drive.<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +13.12 | +2.12 | 'Drive.<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +15.25 | -0.00 | 'Drive.<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +14.87 | +0.37 | 'Drive.<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +11.75 | +3.50 | 'Drive.<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +11.75 | +3.50 | 'Drive.<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | +1.75 | +1.75 (6) | +1.75 | 14 | 28 | 44 |  |
| cf3 | +1.62 | +2.12 (12) | +1.88 | 26 | None | 38 |  |
| cf5 | +2.37 | +2.50 (6) | +2.37 | 28 | None | 40 |  |
| cf6 | +2.12 | +2.50 (12) | +2.00 | 28 | None | 42 |  |
| cf9 | +3.50 | +3.87 (22) | +3.75 | 26 | 30 | 40 |  |
| cf9s | +3.50 | +4.25 (22) | +4.37 | 28 | 30 | 40 |  |

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
| line9 | +4.25 (22) | -0.25 (42) | +4.37 (22) | -0.25 (46) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +4.25 (22) | -0.25 (42) | +4.37 (22) | -0.25 (46) |
| question | +1.75 (30) | -1.37 (22) | +2.12 (30) | -1.13 (22) |
| answer_instr | +0.25 (8) | -0.12 (20) | +0.25 (34) | -0.00 (38) |
| asst_header | +1.00 (32) | -0.12 (2) | +1.12 (32) | -0.13 (2) |
| answer_site | +3.50 (80) | -0.12 (4) | +3.62 (78) | -0.00 (12) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf9s run: max |ΔM| = 1.000 nats (vs Δbeh +3.50)
- library question: M(S) = -15.37 ('Walk.<|eot_id|>'), M(C) = -14.87 ('Walk.<|eot_id|>'); the largest M reached by any single patch = -14.62 → **stays Walk**

## Path validation: line9 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +3.50 | -0.12 (-4%) | +0.00 (0%) | -0.12 (-4%) | +3.50 (100%) |
| 4 | +3.62 | +0.00 (0%) | +0.00 (0%) | -0.12 (-3%) | +3.62 (100%) |
| 8 | +3.50 | -0.25 (-7%) | +0.00 (0%) | -0.12 (-4%) | +3.50 (100%) |
| 12 | +3.50 | -0.12 (-4%) | +0.00 (0%) | +0.00 (0%) | +3.50 (100%) |
| 16 | +3.62 | -0.25 (-7%) | +0.00 (0%) | -0.12 (-3%) | +3.62 (100%) |
| 20 | +4.00 | +0.00 (0%) | +0.00 (0%) | -0.12 (-3%) | +4.00 (100%) |
| 24 | +3.87 | +1.37 (35%) | +0.00 (0%) | -0.12 (-3%) | +3.87 (100%) |
| 28 | +1.88 | +0.88 (47%) | +0.00 (0%) | +0.00 (0%) | +1.88 (100%) |
| 32 | +0.00 | +0.00 | +0.00 | -0.12 | +0.00 |
| 36 | +0.00 | -0.25 | +0.00 | -0.00 | +0.00 |
| 40 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) | -0.12 (100%) |
| 44 | -0.25 | +0.00 (-0%) | +0.00 (-0%) | -0.12 (50%) | -0.25 (100%) |
| 48 | -0.25 | +0.00 (-0%) | +0.00 (-0%) | -0.12 (50%) | -0.25 (100%) |
| 52 | -0.12 | -0.12 (100%) | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) |
| 56 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) | -0.12 (100%) |
| 60 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) | -0.12 (100%) |
| 64 | -0.12 | -0.12 (100%) | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) |
| 68 | -0.12 | -0.12 (100%) | +0.00 (-0%) | +0.00 (-0%) | -0.12 (100%) |
| 72 | -0.00 | +0.00 | +0.00 | -0.12 | -0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
