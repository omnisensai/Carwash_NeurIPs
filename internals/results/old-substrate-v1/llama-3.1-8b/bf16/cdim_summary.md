# CDIM — Llama-3.1-8B-Instruct (substrate.txt)

M(S) = +1.007 (greedy 'drive<|eot_id|>'); 32 layers, 173 tokens; rows = embedding + each layer output; 9125.1 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +0.63 | +0.37 | 'drive<|eot_id|>' | - Perform an activity on an object, without transporting the object from location A to B. |
| cf2 | 2 | reverse | True | +1.01 | -0.01 | 'drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +0.89 | +0.12 | 'drive<|eot_id|>' | - Activities require the object to stay at location A while the user moves to location B. |
| cf4 | 4 | reverse | True | +1.13 | -0.12 | 'drive<|eot_id|>' | - The object is never initially with the user at location A. |
| cf5 | 5 | reverse | True | +0.52 | +0.49 | 'drive<|eot_id|>' | - Moving the user without moving the object does fully satisfy the objective. |
| cf6 | 6 | reverse | True | +0.27 | +0.74 | 'drive<|eot_id|>' | - If the object is a vehicle, the user may leave the object in order to perform the activity at location B. |
| cf6n | 6 | neutral | True | +0.64 | +0.37 | 'drive<|eot_id|>' | - If the object is a vehicle, the user must inspect the object in order to perform the activity at location B. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | +0.37 | +0.50 (6) | +0.50 | 10 | 12 | 15 | +0.48 |
| cf2 | -0.01 | -0.01 (25) | -0.13 | 4 | 4 | 3 | -0.01 |
| cf3 | +0.12 | +0.25 (13) | +0.13 | 30 | 1 | 2 | -0.12 |
| cf4 | -0.12 | -0.24 (11) | -0.26 | 22 | 12 | 1 | +0.37 |
| cf5 | +0.49 | +0.61 (3) | +0.49 | 13 | None | 16 | +0.61 |
| cf6 | +0.74 | +0.86 (3) | +0.73 | 11 | 12 | 15 | +1.61 |
| cf6n | +0.37 | +0.49 (2) | +0.37 | 11 | None | 16 | +1.61 |

## Primary counterfactual cf6: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line2 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line3 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line4 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line5 | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| line6 | +0.86 (3) | -0.00 (21) | +0.73 (3) | -0.13 (16) |
| headers | +0.00 (1) | +0.00 (1) | +0.00 (1) | +0.00 (1) |
| system | +0.86 (3) | -0.00 (21) | +0.73 (3) | -0.13 (16) |
| question | +0.50 (12) | +0.00 (32) | +0.36 (12) | -0.13 (2) |
| answer_instr | +0.13 (11) | +0.00 (32) | +0.12 (3) | -0.12 (21) |
| asst_header | +0.14 (14) | +0.00 (32) | +0.12 (20) | -0.12 (12) |
| answer_site | +0.74 (26) | +0.01 (6) | +0.74 (32) | -0.12 (9) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf6 run: max |ΔM| = 0.500 nats (vs Δbeh +0.74)
- library question: M(S) = -5.36 ('Walk.<|eot_id|>'), M(C) = -5.11 ('Walk.<|eot_id|>'); the largest M reached by any single patch = -4.74 → **stays Walk**

## Path validation: line6 → question / answer site (rows 0…32)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +0.74 | +0.13 (17%) | +0.00 (0%) | +0.12 (17%) | +0.74 (100%) |
| 2 | +0.74 | +0.01 (2%) | +0.00 (0%) | +0.12 (17%) | +0.74 (100%) |
| 4 | +0.74 | +0.13 (17%) | +0.00 (0%) | +0.01 (1%) | +0.74 (100%) |
| 6 | +0.74 | +0.13 (17%) | +0.00 (0%) | -0.00 (-0%) | +0.74 (100%) |
| 8 | +0.74 | +0.13 (17%) | +0.00 (0%) | +0.12 (17%) | +0.74 (100%) |
| 10 | +0.62 | +0.26 (42%) | +0.00 (0%) | +0.12 (20%) | +0.62 (100%) |
| 12 | +0.25 | +0.12 (50%) | +0.00 (0%) | +0.13 (53%) | +0.25 (100%) |
| 14 | +0.00 | +0.00 | +0.00 | +0.01 | +0.00 |
| 16 | +0.00 | +0.01 | +0.00 | +0.13 | +0.00 |
| 18 | +0.01 | +0.00 | +0.00 | +0.01 | +0.01 |
| 20 | +0.00 | +0.01 | +0.00 | +0.12 | +0.00 |
| 22 | +0.00 | +0.00 | +0.00 | +0.01 | +0.00 |
| 24 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 26 | +0.01 | +0.00 | +0.00 | -0.00 | +0.01 |
| 28 | +0.01 | +0.00 | +0.00 | +0.00 | +0.01 |
| 30 | +0.01 | +0.00 | +0.00 | +0.01 | +0.01 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
