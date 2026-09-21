# CDIM — Qwen3-8B (substrate.txt)

M(S) = +10.750 (greedy 'drive<|im_end|>'); 36 layers, 156 tokens; rows = embedding + each layer output; 10573.2 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +8.00 | +2.75 | 'drive<|im_end|>' | - Perform an activity on an object, without transporting the object from location A to B. |
| cf2 | 2 | reverse | True | +9.25 | +1.50 | 'drive<|im_end|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +9.75 | +1.00 | 'drive<|im_end|>' | - Activities require the object to stay at location A while the user moves to location B. |
| cf4 | 4 | reverse | True | +9.00 | +1.75 | 'drive<|im_end|>' | - The object is never initially with the user at location A. |
| cf5 | 5 | reverse | True | +10.75 | +0.00 | 'drive<|im_end|>' | - Moving the user without moving the object does fully satisfy the objective. |
| cf6 | 6 | reverse | True | +6.25 | +4.50 | 'drive<|im_end|>' | - If the object is a vehicle, the user may leave the object in order to perform the activity at location B. |
| cf6n | 6 | neutral | True | +5.00 | +5.75 | 'drive<|im_end|>' | - If the object is a vehicle, the user must inspect the object in order to perform the activity at location B. |
| cf6s | 6 | strong-reverse | True | +3.00 | +7.75 | 'drive<|im_end|>' | - If the object is a vehicle, the user must leave the object in order to perform the activity at location B. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | +2.75 | +3.25 (7) | +3.50 | 16 | None | 23 | +3.75 |
| cf2 | +1.50 | +1.75 (3) | +2.00 | 16 | 4 | 23 | +2.25 |
| cf3 | +1.00 | +3.00 (13) | +1.75 | 30 | 1 | 1 | -1.00 |
| cf4 | +1.75 | +2.25 (6) | +2.50 | 16 | 16 | 24 | +2.25 |
| cf5 | +0.00 | +0.25 (9) | +0.50 | None | None | None | +3.00 |
| cf6 | +4.50 | +4.75 (6) | +5.25 | 19 | None | 23 | +14.50 |
| cf6n | +5.75 | +7.50 (16) | +6.75 | 19 | None | 24 | +14.50 |
| cf6s | +7.75 | +8.75 (7) | +8.50 | 18 | None | 24 | +14.50 |

## Primary counterfactual cf6s: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line2 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line3 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line4 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line5 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line6 | +8.75 (7) | -0.25 (32) | +8.50 (14) | -0.50 (32) |
| headers | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| system | +8.75 (7) | -0.25 (32) | +8.50 (14) | -0.50 (32) |
| question | +2.50 (21) | -1.00 (15) | +1.75 (21) | -0.75 (8) |
| answer_instr | +1.00 (5) | +0.00 (1) | +0.50 (2) | -0.50 (7) |
| asst_header | +1.00 (5) | +0.00 (1) | +0.50 (6) | -0.50 (1) |
| answer_site | +7.75 (33) | -0.25 (14) | +7.75 (34) | -0.50 (18) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf6s run: max |ΔM| = 2.750 nats (vs Δbeh +7.75)
- library question: M(S) = -11.65 ('Walk<|im_end|>'), M(C) = -9.82 ('Walk<|im_end|>'); the largest M reached by any single patch = -9.19 → **stays Walk**

## Path validation: line6 → question / answer site (rows 0…36)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +7.75 | -0.25 (-3%) | +0.00 (0%) | +0.50 (6%) | +7.75 (100%) |
| 2 | +7.50 | +0.00 (0%) | +0.00 (0%) | +0.50 (7%) | +7.50 (100%) |
| 4 | +7.75 | +0.50 (6%) | +0.00 (0%) | +0.25 (3%) | +7.75 (100%) |
| 6 | +8.25 | +0.25 (3%) | +0.00 (0%) | +0.50 (6%) | +8.25 (100%) |
| 8 | +8.25 | +1.00 (12%) | +0.00 (0%) | +0.00 (0%) | +8.25 (100%) |
| 10 | +7.25 | +0.75 (10%) | +0.00 (0%) | +0.50 (7%) | +7.25 (100%) |
| 12 | +7.00 | -0.50 (-7%) | +0.00 (0%) | +0.25 (4%) | +7.00 (100%) |
| 14 | +8.50 | +1.25 (15%) | +0.00 (0%) | +0.75 (9%) | +8.50 (100%) |
| 16 | +7.50 | +1.00 (13%) | +0.00 (0%) | +0.50 (7%) | +7.50 (100%) |
| 18 | +5.25 | +1.25 (24%) | +0.00 (0%) | +0.25 (5%) | +5.25 (100%) |
| 20 | +2.25 | +0.00 (0%) | +0.00 (0%) | +0.75 (33%) | +2.25 (100%) |
| 22 | +0.50 | +0.25 (50%) | +0.00 (0%) | +0.25 (50%) | +0.50 (100%) |
| 24 | +0.50 | +0.25 (50%) | +0.00 (0%) | +0.25 (50%) | +0.50 (100%) |
| 26 | +0.25 | +0.25 (100%) | +0.00 (0%) | +0.25 (100%) | +0.25 (100%) |
| 28 | +0.25 | +0.00 (0%) | +0.00 (0%) | +0.25 (100%) | +0.25 (100%) |
| 30 | +0.25 | +0.25 (100%) | +0.00 (0%) | +0.25 (100%) | +0.25 (100%) |
| 32 | -0.25 | +0.00 (-0%) | +0.00 (-0%) | -0.25 (100%) | -0.25 (100%) |
| 34 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
