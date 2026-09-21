# CDIM — Qwen3-8B (bf16), ladder/L1 (internals/cdim_sweep/generated/substrates/carwash/L1.txt)

M(S) = +7.250 (greedy 'drive<|im_end|>'); 36 layers, 180 tokens; rows = embedding + each layer output; 376.0 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +6.25 | +1.00 | 'drive<|im_end|>' | - Perform an activity on an object, without transporting the object from location A to B. |
| cf2 | 2 | reverse | True | +6.25 | +1.00 | 'drive<|im_end|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +9.00 | -1.75 | 'drive<|im_end|>' | - Activities require the object to stay at location A while the user moves to location B, whether the user walks or drives. |
| cf4 | 4 | reverse | True | +7.00 | +0.25 | 'drive<|im_end|>' | - The object is never initially with the user at location A. |
| cf5 | 5 | reverse | True | +4.50 | +2.75 | 'drive<|im_end|>' | - Moving the user without moving the object, as when the user walks away from it, does fully satisfy the objective. |
| cf6 | 6 | reverse | True | +1.75 | +5.50 | 'drive<|im_end|>' | - If the object is a vehicle, the user may leave it, that is walk off, in order to perform the activity at location B. |
| cf6s | 6 | strong-reverse | True | -1.50 | +8.75 | 'walk<|im_end|>' | - If the object is a vehicle, the user must leave it, that is walk off, in order to perform the activity at location B. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | +1.00 | +2.25 (11) | +1.50 | 28 | 1 | 3 |  |
| cf2 | +1.00 | +2.00 (2) | +1.25 | 15 | 6 | 1 |  |
| cf3 | -1.75 | -1.75 (1) | -1.75 | 13 | 5 | 24 |  |
| cf5 | +2.75 | +4.00 (2) | +3.25 | 19 | None | 24 |  |
| cf6 | +5.50 | +7.75 (6) | +6.75 | 16 | None | 25 |  |
| cf6s | +8.75 | +11.00 (8) | +10.50 | 18 | None | 25 |  |

## Primary counterfactual cf6s: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line2 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line3 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line4 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line5 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line6 | +11.00 (8) | +0.00 (31) | +10.50 (14) | +0.00 (30) |
| headers | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| system | +11.00 (8) | +0.00 (31) | +10.50 (14) | +0.00 (30) |
| question | +1.25 (21) | -2.25 (15) | +0.50 (24) | -1.75 (4) |
| answer_instr | +0.50 (18) | -0.25 (8) | +0.50 (5) | -0.50 (3) |
| asst_header | +0.75 (21) | -0.25 (3) | +0.75 (22) | -0.50 (4) |
| answer_site | +8.75 (35) | -0.50 (8) | +8.75 (35) | -0.50 (1) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf6s run: max |ΔM| = 3.000 nats (vs Δbeh +8.75)
- library question: M(S) = -16.50 ('walk<|im_end|>'), M(C) = -18.00 ('walk<|im_end|>'); the largest M reached by any single patch = -15.75 → **stays Walk**

## Path validation: line6 → question / answer site (rows 0…36)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +8.75 | +0.25 (3%) | +0.00 (0%) | +0.00 (0%) | +8.75 (100%) |
| 2 | +9.25 | +0.50 (5%) | +0.00 (0%) | +0.00 (0%) | +9.25 (100%) |
| 4 | +9.75 | +0.50 (5%) | +0.00 (0%) | +0.00 (0%) | +9.75 (100%) |
| 6 | +10.75 | +1.00 (9%) | +0.00 (0%) | -0.25 (-2%) | +10.75 (100%) |
| 8 | +11.00 | +0.00 (0%) | +0.00 (0%) | +0.00 (0%) | +11.00 (100%) |
| 10 | +10.25 | +1.00 (10%) | +0.00 (0%) | +0.00 (0%) | +10.25 (100%) |
| 12 | +10.00 | -1.00 (-10%) | +0.00 (0%) | -0.25 (-2%) | +10.00 (100%) |
| 14 | +9.75 | +2.00 (21%) | +0.00 (0%) | +0.00 (0%) | +9.75 (100%) |
| 16 | +7.75 | +1.00 (13%) | +0.00 (0%) | +0.00 (0%) | +7.75 (100%) |
| 18 | +5.50 | +0.75 (14%) | +0.00 (0%) | +0.00 (0%) | +5.50 (100%) |
| 20 | +2.75 | +0.25 (9%) | +0.00 (0%) | +0.75 (27%) | +2.75 (100%) |
| 22 | +0.75 | +0.25 (33%) | +0.00 (0%) | +0.00 (0%) | +0.75 (100%) |
| 24 | +1.00 | +0.00 (0%) | +0.00 (0%) | +0.25 (25%) | +1.00 (100%) |
| 26 | +0.75 | +0.25 (33%) | +0.00 (0%) | +0.25 (33%) | +0.75 (100%) |
| 28 | +0.50 | +0.25 (50%) | +0.00 (0%) | +0.50 (100%) | +0.50 (100%) |
| 30 | +0.25 | +0.25 (100%) | +0.00 (0%) | +0.25 (100%) | +0.25 (100%) |
| 32 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 34 | +0.25 | +0.00 (0%) | +0.00 (0%) | +0.25 (100%) | +0.25 (100%) |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
