# CDIM — Llama-3.2-3B-Instruct (substrate.txt)

M(S) = -0.127 (greedy 'walk<|eot_id|>'); 28 layers, 173 tokens; rows = embedding + each layer output; 3839.9 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +0.35 | -0.48 | 'drive<|eot_id|>' | - Perform an activity on an object, without transporting the object from location A to B. |
| cf2 | 2 | reverse | True | +0.00 | -0.13 | 'walk<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +0.01 | -0.13 | 'walk<|eot_id|>' | - Activities require the object to stay at location A while the user moves to location B. |
| cf4 | 4 | reverse | True | -0.14 | +0.01 | 'walk<|eot_id|>' | - The object is never initially with the user at location A. |
| cf5 | 5 | reverse | True | +0.13 | -0.25 | 'walk<|eot_id|>' | - Moving the user without moving the object does fully satisfy the objective. |
| cf6 | 6 | reverse | True | -0.13 | +0.00 | 'walk<|eot_id|>' | - If the object is a vehicle, the user may leave the object in order to perform the activity at location B. |
| cf6n | 6 | neutral | True | -0.22 | +0.09 | 'walk<|eot_id|>' | - If the object is a vehicle, the user must inspect the object in order to perform the activity at location B. |
| cf6s | 6 | strong-reverse | True | -0.13 | +0.00 | 'walk<|eot_id|>' | - If the object is a vehicle, the user must leave the object in order to perform the activity at location B. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | -0.48 | -0.47 (10) | -0.48 | 10 | 11 | 16 | +0.38 |
| cf2 | -0.13 | -0.11 (11) | -0.25 | 5 | None | 27 | -0.53 |
| cf3 | -0.13 | -0.16 (6) | -0.25 | 12 | 10 | 13 | -0.01 |
| cf4 | +0.01 | +0.15 (6) | +0.11 | 21 | 2 | 1 | +0.10 |
| cf5 | -0.25 | -0.36 (6) | -0.38 | 10 | None | 14 | -0.28 |
| cf6 | +0.00 | +0.13 (2) | +0.01 | 27 | 1 | 1 | +0.97 |
| cf6n | +0.09 | +0.22 (7) | +0.12 | 25 | 6 | 1 | +0.97 |
| cf6s | +0.00 | +0.12 (8) | +0.12 | 15 | 2 | 20 | +0.97 |

## Primary counterfactual cf1: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.12 (13) | -0.47 (10) | +0.24 (11) | -0.48 (2) |
| line2 | +0.12 (24) | -0.12 (3) | +0.01 (5) | -0.13 (8) |
| line3 | +0.12 (22) | -0.23 (12) | +0.01 (22) | -0.13 (1) |
| line4 | +0.11 (22) | -0.12 (9) | +0.01 (15) | -0.11 (23) |
| line5 | +0.02 (25) | -0.12 (10) | +0.01 (12) | -0.14 (10) |
| line6 | +0.12 (22) | -0.12 (4) | +0.01 (17) | -0.13 (9) |
| headers | +0.13 (26) | -0.12 (3) | +0.01 (14) | -0.13 (6) |
| system | +0.12 (21) | -0.60 (10) | +0.12 (12) | -0.48 (6) |
| question | +0.02 (2) | -0.59 (11) | +0.24 (10) | -0.50 (11) |
| answer_instr | +0.02 (8) | -0.12 (1) | +0.01 (15) | -0.13 (12) |
| asst_header | +0.02 (27) | -0.12 (16) | +0.01 (7) | -0.14 (24) |
| answer_site | +0.02 (8) | -0.48 (28) | +0.01 (9) | -0.49 (27) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf1 run: max |ΔM| = 0.344 nats (vs Δbeh -0.48)
- library question: M(S) = -5.38 ('Walk.<|eot_id|>'), M(C) = -5.01 ('Walk.<|eot_id|>'); the largest M reached by any single patch = -4.76 → **stays Walk**

## Path validation: line1 → question / answer site (rows 0…28)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | -0.48 | +0.02 (-5%) | +0.00 (-0%) | +0.02 (-5%) | -0.48 (100%) |
| 2 | -0.35 | -0.09 (27%) | +0.00 (-0%) | +0.02 (-6%) | -0.35 (100%) |
| 4 | -0.35 | -0.00 (0%) | +0.00 (-0%) | -0.12 (33%) | -0.35 (100%) |
| 6 | -0.24 | -0.00 (0%) | +0.00 (-0%) | +0.02 (-9%) | -0.24 (100%) |
| 8 | -0.24 | +0.01 (-4%) | +0.00 (-0%) | -0.00 (0%) | -0.24 (100%) |
| 10 | -0.47 | -0.48 (103%) | +0.00 (-0%) | -0.12 (25%) | -0.47 (100%) |
| 12 | +0.01 | -0.10 | +0.00 | +0.02 | +0.01 |
| 14 | +0.02 | -0.09 | +0.00 | -0.00 | +0.02 |
| 16 | -0.00 | -0.00 | +0.00 | -0.00 | -0.00 |
| 18 | +0.00 | +0.12 | +0.00 | +0.00 | +0.00 |
| 20 | -0.12 | +0.01 (-8%) | +0.00 (-0%) | -0.00 (0%) | -0.12 (100%) |
| 22 | +0.02 | -0.00 | +0.00 | +0.01 | +0.02 |
| 24 | -0.00 | +0.01 | +0.00 | -0.01 | -0.00 |
| 26 | +0.01 | +0.00 | +0.00 | +0.01 | +0.01 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
