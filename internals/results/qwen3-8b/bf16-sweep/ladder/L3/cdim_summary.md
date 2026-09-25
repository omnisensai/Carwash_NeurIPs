# CDIM — Qwen3-8B (bf16), ladder/L3 (internals/cdim_sweep/generated/substrates/carwash/L3.txt)

M(S) = +23.250 (greedy 'drive<|im_end|>'); 36 layers, 184 tokens; rows = embedding + each layer output; 380.6 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +15.00 | +8.25 | 'drive<|im_end|>' | - Wash the car at the car wash, leaving the car home instead of the car wash. |
| cf2 | 2 | reverse | True | +17.50 | +5.75 | 'drive<|im_end|>' | - The user has many goals other than to wash the car at the car wash. |
| cf3 | 3 | reverse | True | +13.25 | +10.00 | 'drive<|im_end|>' | - To wash the car at the car wash, the car can stay at home while the user goes to the car wash, whether the user walks or drives. |
| cf4 | 4 | reverse | True | +23.25 | +0.00 | 'drive<|im_end|>' | - The car is far away from the user at the start. |
| cf5 | 5 | reverse | True | +0.00 | +23.25 | 'walk<|im_end|>' | - If the user walks to the car wash and the car stays at home, the user can wash the car. |
| cf6 | 6 | reverse | True | -4.25 | +27.50 | 'walk<|im_end|>' | - A car is a vehicle: the user may leave the car and walk alone to the car wash. |
| cf6s | 6 | strong-reverse | True | -8.25 | +31.50 | 'walk<|im_end|>' | - A car is a vehicle: the user must leave the car and walk alone to the car wash. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | +8.25 | +9.00 (3) | +8.50 | 14 | None | 24 |  |
| cf2 | +5.75 | +6.00 (5) | +6.25 | 16 | None | 23 |  |
| cf3 | +10.00 | +10.00 (1) | +13.00 | 16 | None | 24 |  |
| cf5 | +23.25 | +23.50 (2) | +23.75 | 16 | None | 23 |  |
| cf6 | +27.50 | +28.00 (8) | +29.75 | 19 | None | 24 |  |
| cf6s | +31.50 | +31.75 (8) | +32.75 | 19 | None | 24 |  |

## Primary counterfactual cf6s: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line2 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line3 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line4 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line5 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line6 | +31.75 (8) | +0.00 (34) | +32.75 (14) | +0.00 (35) |
| headers | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| system | +31.75 (8) | +0.00 (34) | +32.75 (14) | +0.00 (35) |
| question | +1.50 (21) | -2.50 (19) | +1.50 (16) | -0.25 (3) |
| answer_instr | +0.25 (6) | -0.75 (15) | +1.00 (6) | +0.00 (1) |
| asst_header | +5.75 (22) | -0.50 (2) | +2.00 (22) | -0.75 (21) |
| answer_site | +31.50 (35) | -0.75 (13) | +31.50 (36) | +0.25 (6) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf6s run: max |ΔM| = 9.500 nats (vs Δbeh +31.50)
- library question: M(S) = -4.75 ('walk<|im_end|>'), M(C) = -10.50 ('walk<|im_end|>'); the largest M reached by any single patch = -2.00 → **stays Walk**

## Path validation: line6 → question / answer site (rows 0…36)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +31.50 | -1.00 (-3%) | +0.00 (0%) | +0.00 (0%) | +31.50 (100%) |
| 2 | +31.00 | +0.50 (2%) | +0.00 (0%) | +0.00 (0%) | +31.00 (100%) |
| 4 | +31.00 | -0.75 (-2%) | +0.00 (0%) | -0.25 (-1%) | +31.00 (100%) |
| 6 | +31.25 | +0.00 (0%) | +0.00 (0%) | -0.25 (-1%) | +31.25 (100%) |
| 8 | +31.75 | -0.25 (-1%) | +0.00 (0%) | -0.75 (-2%) | +31.75 (100%) |
| 10 | +30.50 | +0.50 (2%) | +0.00 (0%) | -0.50 (-2%) | +30.50 (100%) |
| 12 | +29.50 | -2.50 (-8%) | +0.00 (0%) | -0.25 (-1%) | +29.50 (100%) |
| 14 | +29.50 | +3.50 (12%) | +0.00 (0%) | -0.25 (-1%) | +29.50 (100%) |
| 16 | +27.75 | +0.00 (0%) | +0.00 (0%) | +0.00 (0%) | +27.75 (100%) |
| 18 | +23.25 | +0.25 (1%) | +0.00 (0%) | -0.25 (-1%) | +23.25 (100%) |
| 20 | +13.75 | +0.25 (2%) | +0.00 (0%) | +2.00 (15%) | +13.75 (100%) |
| 22 | +5.50 | -0.25 (-5%) | +0.00 (0%) | +3.25 (59%) | +5.50 (100%) |
| 24 | +2.00 | -0.25 (-12%) | +0.00 (0%) | +0.75 (38%) | +2.00 (100%) |
| 26 | +1.00 | +0.00 (0%) | +0.00 (0%) | +0.50 (50%) | +1.00 (100%) |
| 28 | +0.50 | -0.25 (-50%) | +0.00 (0%) | +0.25 (50%) | +0.50 (100%) |
| 30 | +0.25 | +0.00 (0%) | +0.00 (0%) | +0.00 (0%) | +0.25 (100%) |
| 32 | +0.25 | -0.25 (-100%) | +0.00 (0%) | +0.00 (0%) | +0.25 (100%) |
| 34 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
