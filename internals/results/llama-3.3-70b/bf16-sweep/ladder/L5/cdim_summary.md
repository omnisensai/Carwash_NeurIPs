# CDIM — Llama-3.3-70B-Instruct (bf16), ladder/L5 (internals/cdim_sweep/generated/substrates/carwash/L5.txt)

M(S) = +23.151 (greedy 'Drive<|eot_id|>'); 80 layers, 235 tokens; rows = embedding + each layer output; 860.7 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +19.01 | +4.14 | 'Drive<|eot_id|>' | - Wash the car at the car wash, leaving the car home instead of the car wash; the car need not arrive there. |
| cf2 | 2 | reverse | True | +16.86 | +6.29 | 'Drive<|eot_id|>' | - The user has many goals other than to wash the car at the car wash; distance and effort matter a lot. |
| cf3 | 3 | reverse | True | +19.89 | +3.26 | 'Drive<|eot_id|>' | - To wash the car at the car wash, the car can stay at home while the user goes to the car wash; walking moves the user, which is quite enough. |
| cf4 | 4 | reverse | True | +21.40 | +1.75 | 'Drive<|eot_id|>' | - The car is far away from the user at the start, so it never has to be moved. |
| cf5 | 5 | reverse | True | +12.87 | +10.28 | 'Drive<|eot_id|>' | - If the user walks to the car wash, the car stays at home but the user can wash the car; walking works. |
| cf6 | 6 | reverse | True | -15.25 | +38.40 | 'walk<|eot_id|>' | - A car is a vehicle: the user may simply walk over to the car wash. The correct answer is walk, not drive. |
| cf6s | 6 | strong-reverse | True | -9.54 | +32.69 | 'walk<|eot_id|>' | - A car is a vehicle: the user must simply walk over to the car wash. The correct answer is walk, not drive. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | +4.14 | +4.26 (4) | +4.14 | 28 | None | 34 |  |
| cf2 | +6.29 | +6.53 (14) | +6.67 | 22 | 24 | 34 |  |
| cf3 | +3.26 | +3.62 (14) | +3.89 | 26 | None | 34 |  |
| cf4 | +1.75 | +2.00 (4) | +1.75 | 24 | 16 | 34 |  |
| cf5 | +10.28 | +10.50 (6) | +10.20 | 28 | None | 36 |  |
| cf6 | +38.40 | +38.88 (6) | +40.02 | 30 | None | 36 |  |
| cf6s | +32.69 | +32.93 (6) | +37.06 | 30 | None | 36 |  |

## Primary counterfactual cf6: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line6 | +38.88 (6) | +0.00 (80) | +40.02 (24) | -0.11 (76) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +38.88 (6) | +0.00 (80) | +40.02 (24) | -0.11 (76) |
| question | +3.81 (30) | -0.66 (18) | +4.40 (30) | -0.24 (2) |
| answer_instr | +0.32 (20) | -0.23 (30) | +0.14 (34) | -0.24 (24) |
| asst_header | +7.11 (34) | -0.37 (16) | +5.43 (32) | -0.24 (8) |
| answer_site | +38.40 (80) | -0.06 (10) | +38.40 (80) | -0.22 (18) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf6 run: max |ΔM| = 6.672 nats (vs Δbeh +38.40)
- library question: M(S) = -14.47 ('walk<|eot_id|>'), M(C) = -19.51 ('walk<|eot_id|>'); the largest M reached by any single patch = -13.78 → **stays Walk**

## Path validation: line6 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +38.40 | -0.07 (-0%) | +0.00 (0%) | +0.19 (1%) | +38.40 (100%) |
| 4 | +38.38 | +0.00 (0%) | +0.00 (0%) | -0.06 (-0%) | +38.38 (100%) |
| 8 | +38.51 | -0.06 (-0%) | +0.00 (0%) | -0.06 (-0%) | +38.51 (100%) |
| 12 | +38.63 | +0.32 (1%) | +0.00 (0%) | -0.06 (-0%) | +38.63 (100%) |
| 16 | +37.71 | -0.28 (-1%) | +0.00 (0%) | +0.32 (1%) | +37.71 (100%) |
| 20 | +35.75 | -0.07 (-0%) | +0.00 (0%) | +0.25 (1%) | +35.75 (100%) |
| 24 | +35.53 | +0.72 (2%) | +0.00 (0%) | -0.13 (-0%) | +35.53 (100%) |
| 28 | +33.89 | +2.25 (7%) | +0.00 (0%) | +1.14 (3%) | +33.89 (100%) |
| 32 | +12.17 | +0.18 (2%) | +0.00 (0%) | +0.37 (3%) | +12.17 (100%) |
| 36 | +4.64 | -0.00 (-0%) | +0.00 (0%) | +1.44 (31%) | +4.64 (100%) |
| 40 | +1.44 | -0.18 (-13%) | +0.00 (0%) | +0.02 (1%) | +1.44 (100%) |
| 44 | +1.38 | -0.12 (-9%) | +0.00 (0%) | -0.31 (-22%) | +1.38 (100%) |
| 48 | +1.50 | +0.19 (13%) | +0.00 (0%) | +0.00 (0%) | +1.50 (100%) |
| 52 | +1.50 | -0.06 (-4%) | +0.00 (0%) | +0.00 (0%) | +1.50 (100%) |
| 56 | +1.50 | -0.06 (-4%) | +0.00 (0%) | +0.32 (21%) | +1.50 (100%) |
| 60 | +1.12 | -0.06 (-5%) | +0.00 (0%) | +0.25 (22%) | +1.12 (100%) |
| 64 | +1.06 | +0.19 (18%) | +0.00 (0%) | +0.44 (42%) | +1.06 (100%) |
| 68 | +0.81 | +0.00 (0%) | +0.00 (0%) | +0.25 (31%) | +0.81 (100%) |
| 72 | +0.81 | +0.25 (31%) | +0.00 (0%) | +0.68 (85%) | +0.81 (100%) |
| 76 | +0.32 | +0.00 (0%) | +0.00 (0%) | +0.32 (100%) | +0.32 (100%) |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
