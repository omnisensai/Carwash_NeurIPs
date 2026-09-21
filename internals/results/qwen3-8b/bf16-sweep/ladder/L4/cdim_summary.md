# CDIM — Qwen3-8B (bf16), ladder/L4 (internals/cdim_sweep/generated/substrates/carwash/L4.txt)

M(S) = +30.000 (greedy 'drive<|im_end|>'); 36 layers, 215 tokens; rows = embedding + each layer output; 378.8 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +27.25 | +2.75 | 'drive<|im_end|>' | - Wash the car at the car wash, leaving the car home instead of the car wash; the car need not arrive there. |
| cf2 | 2 | reverse | True | +24.75 | +5.25 | 'drive<|im_end|>' | - The user has many goals other than to wash the car at the car wash; distance and effort matter a lot. |
| cf3 | 3 | reverse | True | +22.50 | +7.50 | 'drive<|im_end|>' | - To wash the car at the car wash, the car can stay at home while the user goes to the car wash; walking moves the user, which is quite enough. |
| cf4 | 4 | reverse | True | +30.25 | -0.25 | 'drive<|im_end|>' | - The car is far away from the user at the start, so it never has to be moved. |
| cf5 | 5 | reverse | True | -3.75 | +33.75 | 'walk<|im_end|>' | - If the user walks to the car wash, the car stays at home but the user can wash the car; walking works. |
| cf6 | 6 | reverse | True | +15.50 | +14.50 | 'drive<|im_end|>' | - A car is a vehicle: the user may leave the car and walk alone to the car wash; walking succeeds. |
| cf6s | 6 | strong-reverse | True | +16.00 | +14.00 | 'drive<|im_end|>' | - A car is a vehicle: the user must leave the car and walk alone to the car wash; walking succeeds. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | +2.75 | +4.75 (9) | +4.25 | 19 | None | 22 |  |
| cf2 | +5.25 | +6.25 (5) | +5.75 | 18 | None | 22 |  |
| cf3 | +7.50 | +8.00 (11) | +7.00 | 17 | None | 23 |  |
| cf5 | +33.75 | +34.00 (6) | +34.00 | 19 | None | 23 |  |
| cf6 | +14.50 | +15.50 (8) | +16.50 | 20 | None | 23 |  |
| cf6s | +14.00 | +15.00 (1) | +19.75 | 20 | None | 23 |  |

## Primary counterfactual cf5: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line2 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line3 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line4 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line5 | +34.00 (6) | -0.25 (35) | +34.00 (5) | -0.25 (25) |
| line6 | +14.75 (17) | -0.75 (8) | +4.25 (19) | -0.75 (2) |
| headers | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| system | +34.50 (9) | -0.25 (27) | +34.00 (10) | +0.00 (34) |
| question | +7.75 (21) | -0.75 (3) | +1.25 (18) | -0.75 (6) |
| answer_instr | +0.50 (19) | -0.75 (9) | +0.50 (20) | -0.50 (2) |
| asst_header | +7.75 (22) | -0.50 (2) | +2.75 (22) | -0.50 (7) |
| answer_site | +33.75 (36) | -0.50 (2) | +33.75 (35) | -0.75 (12) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf5 run: max |ΔM| = 5.000 nats (vs Δbeh +33.75)
- library question: M(S) = +8.00 ('drive<|im_end|>'), M(C) = -9.25 ('walk<|im_end|>'); the largest M reached by any single patch = +9.25 → **GOES DRIVE**

## Path validation: line5 → question / answer site (rows 0…36)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +33.75 | +0.00 (0%) | +0.00 (0%) | -0.50 (-1%) | +33.75 (100%) |
| 2 | +34.00 | +0.50 (1%) | +0.00 (0%) | +0.00 (0%) | +34.00 (100%) |
| 4 | +33.75 | -0.25 (-1%) | +0.00 (0%) | -0.25 (-1%) | +33.75 (100%) |
| 6 | +34.00 | +0.25 (1%) | +0.00 (0%) | -0.50 (-1%) | +34.00 (100%) |
| 8 | +33.50 | -0.25 (-1%) | +0.00 (0%) | -0.25 (-1%) | +33.50 (100%) |
| 10 | +34.00 | +0.25 (1%) | +0.00 (0%) | -0.50 (-1%) | +34.00 (100%) |
| 12 | +32.75 | +0.25 (1%) | +0.00 (0%) | -0.75 (-2%) | +32.75 (100%) |
| 14 | +33.50 | +1.50 (4%) | +0.00 (0%) | -0.25 (-1%) | +33.50 (100%) |
| 16 | +32.50 | +2.75 (8%) | +0.00 (0%) | +0.00 (0%) | +32.50 (100%) |
| 18 | +25.50 | +1.00 (4%) | +0.00 (0%) | +0.00 (0%) | +25.50 (100%) |
| 20 | +7.75 | +0.75 (10%) | +0.00 (0%) | +0.25 (3%) | +7.75 (100%) |
| 22 | +3.50 | +0.25 (7%) | +0.00 (0%) | +2.50 (71%) | +3.50 (100%) |
| 24 | +1.50 | +0.00 (0%) | +0.00 (0%) | +1.00 (67%) | +1.50 (100%) |
| 26 | +0.50 | +0.00 (0%) | +0.00 (0%) | +0.50 (100%) | +0.50 (100%) |
| 28 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 30 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 32 | +0.00 | +0.25 | +0.00 | +0.00 | +0.00 |
| 34 | +0.25 | +0.00 (0%) | +0.00 (0%) | +0.25 (100%) | +0.25 (100%) |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
