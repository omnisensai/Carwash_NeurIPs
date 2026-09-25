# CDIM — Qwen3-8B (bf16), ladder/L5 (internals/cdim_sweep/generated/substrates/carwash/L5.txt)

M(S) = +33.875 (greedy 'drive<|im_end|>'); 36 layers, 218 tokens; rows = embedding + each layer output; 326.0 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +33.50 | +0.37 | 'drive<|im_end|>' | - Wash the car at the car wash, leaving the car home instead of the car wash; the car need not arrive there. |
| cf2 | 2 | reverse | True | +30.50 | +3.37 | 'drive<|im_end|>' | - The user has many goals other than to wash the car at the car wash; distance and effort matter a lot. |
| cf3 | 3 | reverse | True | +30.50 | +3.37 | 'drive<|im_end|>' | - To wash the car at the car wash, the car can stay at home while the user goes to the car wash; walking moves the user, which is quite enough. |
| cf4 | 4 | reverse | True | +34.00 | -0.13 | 'drive<|im_end|>' | - The car is far away from the user at the start, so it never has to be moved. |
| cf5 | 5 | reverse | True | +27.00 | +6.87 | 'drive<|im_end|>' | - If the user walks to the car wash, the car stays at home but the user can wash the car; walking works. |
| cf6 | 6 | reverse | True | -25.00 | +58.87 | 'walk<|im_end|>' | - A car is a vehicle: the user may simply walk over to the car wash. The correct answer is walk, not drive. |
| cf6s | 6 | strong-reverse | True | -24.75 | +58.62 | 'walk<|im_end|>' | - A car is a vehicle: the user must simply walk over to the car wash. The correct answer is walk, not drive. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf2 | +3.37 | +4.88 (7) | +4.37 | 18 | 19 | 22 |  |
| cf3 | +3.37 | +4.12 (11) | +3.87 | 18 | None | 20 |  |
| cf5 | +6.87 | +8.12 (5) | +7.12 | 19 | None | 23 |  |
| cf6 | +58.87 | +59.87 (4) | +60.37 | 19 | None | 24 |  |
| cf6s | +58.62 | +60.50 (16) | +59.87 | 19 | None | 24 |  |

## Primary counterfactual cf6: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line2 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line3 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line4 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line5 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line6 | +59.87 (4) | +0.00 (35) | +60.37 (10) | +0.00 (35) |
| headers | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| system | +59.87 (4) | +0.00 (35) | +60.37 (10) | +0.00 (35) |
| question | +0.75 (21) | -0.50 (14) | +0.88 (22) | -1.38 (17) |
| answer_instr | +0.50 (3) | -0.50 (7) | +0.12 (33) | -1.25 (17) |
| asst_header | +4.50 (22) | -0.50 (10) | +0.87 (22) | -1.00 (3) |
| answer_site | +58.87 (35) | -0.50 (21) | +58.87 (36) | -1.25 (19) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf6 run: max |ΔM| = 3.500 nats (vs Δbeh +58.87)
- library question: M(S) = +1.25 ('drive<|im_end|>'), M(C) = -16.00 ('walk<|im_end|>'); the largest M reached by any single patch = +6.25 → **GOES DRIVE**

## Path validation: line6 → question / answer site (rows 0…36)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +58.87 | -0.25 (-0%) | +0.00 (0%) | +0.25 (0%) | +58.87 (100%) |
| 2 | +58.62 | -0.75 (-1%) | +0.00 (0%) | +0.00 (0%) | +58.62 (100%) |
| 4 | +59.87 | +0.00 (0%) | +0.00 (0%) | +0.25 (0%) | +59.87 (100%) |
| 6 | +59.75 | +0.25 (0%) | +0.00 (0%) | +0.25 (0%) | +59.75 (100%) |
| 8 | +59.37 | -0.50 (-1%) | +0.00 (0%) | -0.50 (-1%) | +59.37 (100%) |
| 10 | +58.62 | -0.25 (-0%) | +0.00 (0%) | +0.00 (0%) | +58.62 (100%) |
| 12 | +59.25 | -0.25 (-0%) | +0.00 (0%) | -0.25 (-0%) | +59.25 (100%) |
| 14 | +58.75 | +0.25 (0%) | +0.00 (0%) | +0.25 (0%) | +58.75 (100%) |
| 16 | +59.75 | -0.25 (-0%) | +0.00 (0%) | -0.25 (-0%) | +59.75 (100%) |
| 18 | +52.25 | +0.00 (0%) | +0.00 (0%) | -0.25 (-0%) | +52.25 (100%) |
| 20 | +16.75 | +0.50 (3%) | +0.00 (0%) | -0.50 (-3%) | +16.75 (100%) |
| 22 | +6.00 | -0.25 (-4%) | +0.00 (0%) | -0.25 (-4%) | +6.00 (100%) |
| 24 | +6.50 | -0.25 (-4%) | +0.00 (0%) | +0.75 (12%) | +6.50 (100%) |
| 26 | +5.25 | -0.25 (-5%) | +0.00 (0%) | +1.00 (19%) | +5.25 (100%) |
| 28 | +3.75 | +0.00 (0%) | +0.00 (0%) | +0.50 (13%) | +3.75 (100%) |
| 30 | +3.75 | -0.25 (-7%) | +0.00 (0%) | +0.25 (7%) | +3.75 (100%) |
| 32 | +3.50 | +0.00 (0%) | +0.00 (0%) | +2.75 (79%) | +3.50 (100%) |
| 34 | +0.50 | +0.00 (0%) | +0.00 (0%) | +0.50 (100%) | +0.50 (100%) |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
