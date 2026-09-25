# CDIM — Llama-3.3-70B-Instruct (bf16), ladder/L3 (internals/cdim_sweep/generated/substrates/carwash/L3.txt)

M(S) = +11.451 (greedy 'Drive<|eot_id|>'); 80 layers, 201 tokens; rows = embedding + each layer output; 734.0 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +14.26 | -2.81 | 'Drive<|eot_id|>' | - Wash the car at the car wash, leaving the car home instead of the car wash. |
| cf2 | 2 | reverse | True | +5.34 | +6.11 | 'Drive<|eot_id|>' | - The user has many goals other than to wash the car at the car wash. |
| cf3 | 3 | reverse | True | +13.55 | -2.10 | 'Drive<|eot_id|>' | - To wash the car at the car wash, the car can stay at home while the user goes to the car wash, whether the user walks or drives. |
| cf4 | 4 | reverse | True | +10.88 | +0.57 | 'Drive<|eot_id|>' | - The car is far away from the user at the start. |
| cf5 | 5 | reverse | True | +2.67 | +8.78 | 'Drive<|eot_id|>' | - If the user walks to the car wash and the car stays at home, the user can wash the car. |
| cf6 | 6 | reverse | True | -7.98 | +19.43 | 'Walk<|eot_id|>' | - A car is a vehicle: the user may leave the car and walk alone to the car wash. |
| cf6s | 6 | strong-reverse | True | -1.61 | +13.06 | 'Walk<|eot_id|>' | - A car is a vehicle: the user must leave the car and walk alone to the car wash. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | -2.81 | -2.81 (4) | -3.19 | 14 | 24 | 36 |  |
| cf2 | +6.11 | +6.48 (10) | +6.00 | 26 | None | 38 |  |
| cf3 | -2.10 | -2.26 (4) | -2.48 | 10 | None | 40 |  |
| cf5 | +8.78 | +9.03 (6) | +9.04 | 26 | None | 36 |  |
| cf6 | +19.43 | +20.02 (10) | +19.43 | 26 | None | 40 |  |
| cf6s | +13.06 | +13.47 (12) | +13.56 | 28 | None | 38 |  |

## Primary counterfactual cf6: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line6 | +20.02 (10) | +0.00 (76) | +19.43 (8) | +0.00 (80) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +20.02 (10) | +0.00 (76) | +19.43 (8) | +0.00 (80) |
| question | +3.44 (20) | -0.18 (32) | +3.83 (20) | -0.37 (8) |
| answer_instr | +0.29 (18) | -0.00 (66) | +0.12 (60) | -0.28 (12) |
| asst_header | +6.27 (32) | -0.00 (12) | +4.81 (34) | -0.09 (16) |
| answer_site | +19.43 (80) | -0.04 (26) | +19.43 (80) | -0.15 (22) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf6 run: max |ΔM| = 1.465 nats (vs Δbeh +19.43)
- library question: M(S) = -18.76 ('Walk<|eot_id|>'), M(C) = -20.45 ('Walk<|eot_id|>'); the largest M reached by any single patch = -17.85 → **stays Walk**

## Path validation: line6 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +19.43 | +0.17 (1%) | +0.00 (0%) | +0.00 (0%) | +19.43 (100%) |
| 4 | +19.68 | -0.00 (-0%) | +0.00 (0%) | +0.00 (0%) | +19.68 (100%) |
| 8 | +19.80 | +0.41 (2%) | +0.00 (0%) | -0.00 (-0%) | +19.80 (100%) |
| 12 | +19.96 | +1.19 (6%) | +0.00 (0%) | +0.17 (1%) | +19.96 (100%) |
| 16 | +19.02 | +1.65 (9%) | +0.00 (0%) | +0.16 (1%) | +19.02 (100%) |
| 20 | +13.31 | -0.13 (-1%) | +0.00 (0%) | -0.00 (-0%) | +13.31 (100%) |
| 24 | +11.81 | +0.25 (2%) | +0.00 (0%) | -0.08 (-1%) | +11.81 (100%) |
| 28 | +4.93 | +0.04 (1%) | +0.00 (0%) | +0.42 (8%) | +4.93 (100%) |
| 32 | +0.94 | +0.29 (31%) | +0.00 (0%) | +0.12 (13%) | +0.94 (100%) |
| 36 | +0.66 | +0.12 (19%) | +0.00 (0%) | +0.00 (0%) | +0.66 (100%) |
| 40 | +0.25 | +0.12 (50%) | +0.00 (0%) | +0.16 (65%) | +0.25 (100%) |
| 44 | +0.41 | -0.00 (-0%) | +0.00 (0%) | +0.00 (0%) | +0.41 (100%) |
| 48 | +0.41 | +0.00 (0%) | +0.00 (0%) | -0.00 (-1%) | +0.41 (100%) |
| 52 | +0.25 | +0.00 (0%) | +0.00 (0%) | +0.12 (49%) | +0.25 (100%) |
| 56 | +0.37 | +0.00 (0%) | +0.00 (0%) | +0.07 (20%) | +0.37 (100%) |
| 60 | +0.20 | +0.07 (35%) | +0.00 (0%) | +0.07 (37%) | +0.20 (100%) |
| 64 | +0.32 | +0.00 (0%) | +0.00 (0%) | +0.25 (78%) | +0.32 (100%) |
| 68 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 72 | +0.20 | +0.00 (0%) | +0.00 (0%) | +0.07 (38%) | +0.20 (100%) |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
