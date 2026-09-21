# CDIM — Llama-3.3-70B-Instruct (bf16), ladder/L4 (internals/cdim_sweep/generated/substrates/carwash/L4.txt)

M(S) = +21.563 (greedy 'Drive<|eot_id|>'); 80 layers, 232 tokens; rows = embedding + each layer output; 850.5 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +19.19 | +2.38 | 'Drive<|eot_id|>' | - Wash the car at the car wash, leaving the car home instead of the car wash; the car need not arrive there. |
| cf2 | 2 | reverse | True | +16.31 | +5.25 | 'Drive<|eot_id|>' | - The user has many goals other than to wash the car at the car wash; distance and effort matter a lot. |
| cf3 | 3 | reverse | True | +19.64 | +1.93 | 'Drive<|eot_id|>' | - To wash the car at the car wash, the car can stay at home while the user goes to the car wash; walking moves the user, which is quite enough. |
| cf4 | 4 | reverse | True | +19.43 | +2.13 | 'Drive<|eot_id|>' | - The car is far away from the user at the start, so it never has to be moved. |
| cf5 | 5 | reverse | True | -6.56 | +28.12 | 'walk<|eot_id|>' | - If the user walks to the car wash, the car stays at home but the user can wash the car; walking works. |
| cf6 | 6 | reverse | True | +12.38 | +9.18 | 'Drive<|eot_id|>' | - A car is a vehicle: the user may leave the car and walk alone to the car wash; walking succeeds. |
| cf6s | 6 | strong-reverse | True | +14.12 | +7.44 | 'Drive<|eot_id|>' | - A car is a vehicle: the user must leave the car and walk alone to the car wash; walking succeeds. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | +2.38 | +2.49 (4) | +2.51 | 28 | None | 34 |  |
| cf2 | +5.25 | +5.25 (2) | +5.37 | 22 | 24 | 34 |  |
| cf3 | +1.93 | +2.55 (16) | +2.68 | 30 | 28 | 32 |  |
| cf4 | +2.13 | +2.37 (8) | +2.37 | 16 | None | 34 |  |
| cf5 | +28.12 | +28.12 (4) | +28.00 | 28 | None | 34 |  |
| cf6 | +9.18 | +9.44 (10) | +9.19 | 28 | None | 36 |  |
| cf6s | +7.44 | +7.56 (12) | +7.51 | 30 | None | 36 |  |

## Primary counterfactual cf5: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +28.12 (4) | -0.25 (42) | +28.00 (8) | -0.25 (44) |
| line6 | +14.07 (26) | -0.22 (56) | +3.01 (28) | -0.00 (6) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +28.12 (16) | -0.25 (50) | +29.83 (18) | -0.12 (40) |
| question | +6.08 (30) | -1.23 (20) | +2.77 (30) | -0.25 (14) |
| answer_instr | +0.29 (6) | -0.34 (28) | +0.37 (6) | -0.12 (4) |
| asst_header | +15.38 (34) | -0.10 (16) | +5.55 (32) | -0.13 (12) |
| answer_site | +28.12 (80) | -0.25 (2) | +28.22 (78) | -0.12 (16) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf5 run: max |ΔM| = 6.807 nats (vs Δbeh +28.12)
- library question: M(S) = -16.73 ('Walk<|eot_id|>'), M(C) = -19.42 ('Walk<|eot_id|>'); the largest M reached by any single patch = -16.41 → **stays Walk**

## Path validation: line5 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +28.12 | -0.25 (-1%) | +0.00 (0%) | -0.03 (-0%) | +28.12 (100%) |
| 4 | +28.12 | -0.12 (-0%) | +0.00 (0%) | -0.03 (-0%) | +28.12 (100%) |
| 8 | +28.00 | -0.04 (-0%) | +0.00 (0%) | -0.04 (-0%) | +28.00 (100%) |
| 12 | +27.75 | -0.17 (-1%) | +0.00 (0%) | -0.25 (-1%) | +27.75 (100%) |
| 16 | +26.88 | -1.11 (-4%) | +0.00 (0%) | -0.03 (-0%) | +26.88 (100%) |
| 20 | +25.02 | +0.37 (1%) | +0.00 (0%) | +0.08 (0%) | +25.02 (100%) |
| 24 | +24.50 | +2.03 (8%) | +0.00 (0%) | +0.24 (1%) | +24.50 (100%) |
| 28 | +20.63 | +0.20 (1%) | +0.00 (0%) | +1.58 (8%) | +20.63 (100%) |
| 32 | +1.14 | +0.08 (7%) | +0.00 (0%) | +0.25 (22%) | +1.14 (100%) |
| 36 | -0.00 | +0.00 | +0.00 | +0.12 | -0.00 |
| 40 | -0.25 | -0.22 (89%) | +0.00 (-0%) | -0.25 (100%) | -0.25 (100%) |
| 44 | -0.25 | -0.22 (89%) | +0.00 (-0%) | -0.13 (50%) | -0.25 (100%) |
| 48 | -0.13 | -0.03 (25%) | +0.00 (-0%) | -0.22 (168%) | -0.13 (100%) |
| 52 | -0.25 | +0.00 (-0%) | +0.00 (-0%) | -0.24 (96%) | -0.25 (100%) |
| 56 | -0.25 | +0.00 (-0%) | +0.00 (-0%) | -0.04 (17%) | -0.25 (100%) |
| 60 | -0.11 | +0.00 (-0%) | +0.00 (-0%) | -0.22 (210%) | -0.11 (100%) |
| 64 | +0.12 | +0.00 (0%) | +0.00 (0%) | -0.22 (-191%) | +0.12 (100%) |
| 68 | +0.12 | +0.00 (0%) | +0.00 (0%) | -0.22 (-191%) | +0.12 (100%) |
| 72 | +0.00 | +0.00 | +0.00 | +0.12 | +0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
