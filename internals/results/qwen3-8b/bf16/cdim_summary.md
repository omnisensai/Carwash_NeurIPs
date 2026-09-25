# CDIM — Qwen3-8B (bf16), substrate.txt (substrate.txt)

M(S) = +7.250 (greedy 'drive<|im_end|>'); 36 layers, 171 tokens; rows = embedding + each layer output; 658.0 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +10.50 | -3.25 | 'drive<|im_end|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +7.75 | -0.50 | 'drive<|im_end|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +11.25 | -4.00 | 'drive<|im_end|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +6.00 | +1.25 | 'drive<|im_end|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +4.75 | +2.50 | 'drive<|im_end|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +4.25 | +3.00 | 'drive<|im_end|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | -7.25 | +14.50 | 'walk<|im_end|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +6.50 | +0.75 | 'drive<|im_end|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +0.75 | +6.50 | 'drive<|im_end|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +0.50 | +6.75 | 'drive<|im_end|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | -3.25 | -4.00 (1) | -3.00 | 16 | 10 | 24 | +2.50 |
| cf2 | -0.50 | -1.50 (9) | -1.00 | 27 | 1 | 1 | -3.00 |
| cf3 | -4.00 | -5.00 (4) | -5.25 | 10 | None | 23 | +0.00 |
| cf4 | +1.25 | +1.75 (14) | +2.25 | 16 | 1 | 3 | -3.50 |
| cf5 | +2.50 | +3.75 (4) | +3.25 | 19 | 7 | 23 | -1.75 |
| cf6 | +3.00 | +3.75 (1) | +3.75 | 18 | 15 | 24 | +2.50 |
| cf7 | +14.50 | +14.75 (4) | +14.75 | 15 | None | 25 | +3.50 |
| cf8 | +0.75 | +2.25 (15) | +2.00 | 20 | 2 | 1 | +0.50 |
| cf9 | +6.50 | +6.75 (6) | +8.25 | 18 | 19 | 24 | +3.50 |
| cf9s | +6.75 | +7.50 (15) | +9.50 | 20 | 21 | 24 | +3.50 |

## Primary counterfactual cf7: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line2 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line3 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line4 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line5 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line6 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line7 | +14.75 (4) | +0.00 (28) | +14.75 (6) | +0.00 (21) |
| line8 | +2.25 (15) | -0.25 (2) | +3.25 (15) | -0.50 (10) |
| line9 | +1.75 (19) | +0.00 (6) | +1.50 (13) | -0.50 (9) |
| headers | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| definitions | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| system | +14.75 (2) | +0.00 (30) | +15.00 (14) | +0.00 (26) |
| question | +4.00 (18) | -0.25 (14) | +5.75 (16) | +0.00 (34) |
| answer_instr | +1.00 (13) | +0.00 (4) | +1.00 (4) | -0.25 (21) |
| asst_header | +1.50 (22) | -0.25 (17) | +1.50 (23) | -0.50 (19) |
| answer_site | +14.50 (35) | +0.00 (4) | +14.50 (35) | -0.50 (2) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf7 run: max |ΔM| = 2.000 nats (vs Δbeh +14.50)

## Path validation: line7 → question / answer site (rows 0…36)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +14.50 | +0.50 (3%) | +0.00 (0%) | +0.50 (3%) | +14.50 (100%) |
| 2 | +13.75 | +0.50 (4%) | +0.00 (0%) | +0.50 (4%) | +13.75 (100%) |
| 4 | +14.75 | +1.00 (7%) | +0.00 (0%) | +0.25 (2%) | +14.75 (100%) |
| 6 | +14.50 | +0.00 (0%) | +0.00 (0%) | +0.50 (3%) | +14.50 (100%) |
| 8 | +14.25 | +0.25 (2%) | +0.00 (0%) | +0.00 (0%) | +14.25 (100%) |
| 10 | +13.50 | +0.50 (4%) | +0.00 (0%) | +0.75 (6%) | +13.50 (100%) |
| 12 | +13.00 | +0.25 (2%) | +0.00 (0%) | +0.25 (2%) | +13.00 (100%) |
| 14 | +11.00 | +2.50 (23%) | +0.00 (0%) | +0.25 (2%) | +11.00 (100%) |
| 16 | +6.75 | +1.50 (22%) | +0.00 (0%) | +0.00 (0%) | +6.75 (100%) |
| 18 | +2.50 | +1.00 (40%) | +0.00 (0%) | +0.00 (0%) | +2.50 (100%) |
| 20 | +1.00 | +0.50 (50%) | +0.00 (0%) | +0.25 (25%) | +1.00 (100%) |
| 22 | +1.25 | +0.25 (20%) | +0.00 (0%) | +0.50 (40%) | +1.25 (100%) |
| 24 | +0.50 | +0.25 (50%) | +0.00 (0%) | +0.50 (100%) | +0.50 (100%) |
| 26 | +0.25 | +0.25 (100%) | +0.00 (0%) | +0.25 (100%) | +0.25 (100%) |
| 28 | +0.00 | +0.25 | +0.00 | +0.25 | +0.00 |
| 30 | +0.00 | +0.25 | +0.00 | +0.25 | +0.00 |
| 32 | +0.00 | +0.00 | +0.00 | +0.25 | +0.00 |
| 34 | +0.25 | +0.00 (0%) | +0.00 (0%) | +0.25 (100%) | +0.25 (100%) |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
