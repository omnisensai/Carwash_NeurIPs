# CDIM — Qwen3-8B (bf16), ladder/L2 (internals/cdim_sweep/generated/substrates/carwash/L2.txt)

M(S) = +7.500 (greedy 'drive<|im_end|>'); 36 layers, 208 tokens; rows = embedding + each layer output; 325.9 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +8.00 | -0.50 | 'drive<|im_end|>' | - Perform an activity (for example washing a car) on an object (for example a car), without transporting the object from location A to B. |
| cf2 | 2 | reverse | True | +5.25 | +2.25 | 'drive<|im_end|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +12.75 | -5.25 | 'drive<|im_end|>' | - Activities require the object to stay at location A while the user moves alone to location B (for example the car wash), whether the user walks or drives. |
| cf4 | 4 | reverse | True | +8.00 | -0.50 | 'drive<|im_end|>' | - The object is never initially with the user at location A (for example home). |
| cf5 | 5 | reverse | True | +4.75 | +2.75 | 'drive<|im_end|>' | - Moving the user without moving the object, as when the user walks away from it, does fully satisfy the objective. |
| cf6 | 6 | reverse | True | -2.25 | +9.75 | 'walk<|im_end|>' | - If the object is a vehicle (for example a car), the user may leave it, that is walk off, in order to perform the activity at location B. |
| cf6s | 6 | strong-reverse | True | -4.00 | +11.50 | 'walk<|im_end|>' | - If the object is a vehicle (for example a car), the user must leave it, that is walk off, in order to perform the activity at location B. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf2 | +2.25 | +3.25 (6) | +2.50 | 13 | 16 | 23 |  |
| cf3 | -5.25 | -5.25 (2) | -5.25 | 13 | 17 | 24 |  |
| cf5 | +2.75 | +4.25 (11) | +4.50 | 18 | None | 24 |  |
| cf6 | +9.75 | +11.50 (7) | +11.25 | 15 | None | 25 |  |
| cf6s | +11.50 | +14.00 (8) | +15.50 | 19 | None | 25 |  |

## Primary counterfactual cf6s: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line2 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line3 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line4 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line5 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line6 | +14.00 (8) | +0.00 (33) | +15.50 (15) | +0.00 (30) |
| headers | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| system | +14.00 (8) | +0.00 (33) | +15.50 (15) | +0.00 (30) |
| question | +2.25 (21) | -3.50 (15) | +1.50 (21) | -3.00 (18) |
| answer_instr | +0.50 (11) | -0.25 (7) | +0.25 (6) | -0.75 (1) |
| asst_header | +0.75 (25) | -1.00 (21) | +0.50 (25) | -1.25 (21) |
| answer_site | +11.75 (35) | -0.50 (15) | +11.50 (36) | -0.50 (15) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf6s run: max |ΔM| = 3.250 nats (vs Δbeh +11.50)
- library question: M(S) = -9.25 ('walk<|im_end|>'), M(C) = -14.75 ('walk<|im_end|>'); the largest M reached by any single patch = -8.50 → **stays Walk**

## Path validation: line6 → question / answer site (rows 0…36)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +11.50 | -1.50 (-13%) | +0.00 (0%) | -0.25 (-2%) | +11.50 (100%) |
| 2 | +12.00 | +0.50 (4%) | +0.00 (0%) | +0.00 (0%) | +12.00 (100%) |
| 4 | +12.75 | -0.50 (-4%) | +0.00 (0%) | +0.00 (0%) | +12.75 (100%) |
| 6 | +13.25 | +0.50 (4%) | +0.00 (0%) | -0.25 (-2%) | +13.25 (100%) |
| 8 | +14.00 | +0.25 (2%) | +0.00 (0%) | +0.00 (0%) | +14.00 (100%) |
| 10 | +13.25 | +0.50 (4%) | +0.00 (0%) | +0.00 (0%) | +13.25 (100%) |
| 12 | +13.25 | -1.00 (-8%) | +0.00 (0%) | +0.00 (0%) | +13.25 (100%) |
| 14 | +12.25 | +2.25 (18%) | +0.00 (0%) | -0.25 (-2%) | +12.25 (100%) |
| 16 | +8.50 | -1.25 (-15%) | +0.00 (0%) | +0.00 (0%) | +8.50 (100%) |
| 18 | +8.75 | +1.75 (20%) | +0.00 (0%) | -0.25 (-3%) | +8.75 (100%) |
| 20 | +5.25 | +0.00 (0%) | +0.00 (0%) | +1.00 (19%) | +5.25 (100%) |
| 22 | +1.50 | +0.00 (0%) | +0.00 (0%) | -0.50 (-33%) | +1.50 (100%) |
| 24 | +1.25 | +0.25 (20%) | +0.00 (0%) | +0.25 (20%) | +1.25 (100%) |
| 26 | +1.00 | +0.25 (25%) | +0.00 (0%) | +0.50 (50%) | +1.00 (100%) |
| 28 | +0.50 | +0.00 (0%) | +0.00 (0%) | +0.50 (100%) | +0.50 (100%) |
| 30 | +0.25 | +0.25 (100%) | +0.00 (0%) | +0.25 (100%) | +0.25 (100%) |
| 32 | +0.25 | +0.00 (0%) | +0.00 (0%) | +0.25 (100%) | +0.25 (100%) |
| 34 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
