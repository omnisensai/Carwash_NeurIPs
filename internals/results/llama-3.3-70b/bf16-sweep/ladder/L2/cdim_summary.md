# CDIM — Llama-3.3-70B-Instruct (bf16), ladder/L2 (internals/cdim_sweep/generated/substrates/carwash/L2.txt)

M(S) = -0.708 (greedy 'walk<|eot_id|>'); 80 layers, 225 tokens; rows = embedding + each layer output; 863.4 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +10.42 | -11.13 | 'Drive<|eot_id|>' | - Perform an activity (for example washing a car) on an object (for example a car), without transporting the object from location A to B. |
| cf2 | 2 | reverse | True | +0.92 | -1.63 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +1.95 | -2.66 | 'Drive<|eot_id|>' | - Activities require the object to stay at location A while the user moves alone to location B (for example the car wash), whether the user walks or drives. |
| cf4 | 4 | reverse | True | +4.02 | -4.73 | 'Drive<|eot_id|>' | - The object is never initially with the user at location A (for example home). |
| cf5 | 5 | reverse | True | -6.51 | +5.81 | 'walk<|eot_id|>' | - Moving the user without moving the object, as when the user walks away from it, does fully satisfy the objective. |
| cf6 | 6 | reverse | True | -3.06 | +2.35 | 'Walk.<|eot_id|>' | - If the object is a vehicle (for example a car), the user may leave it, that is walk off, in order to perform the activity at location B. |
| cf6s | 6 | strong-reverse | True | -3.54 | +2.83 | 'walk<|eot_id|>' | - If the object is a vehicle (for example a car), the user must leave it, that is walk off, in order to perform the activity at location B. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | -11.13 | -10.74 (6) | -11.15 | 16 | None | 40 |  |
| cf2 | -1.63 | -1.38 (8) | -1.63 | 10 | None | 34 |  |
| cf3 | -2.66 | -3.53 (28) | -4.56 | 16 | 20 | 36 |  |
| cf4 | -4.73 | -5.09 (16) | -4.89 | 20 | None | 36 |  |
| cf5 | +5.81 | +6.80 (12) | +6.23 | 22 | None | 40 |  |
| cf6 | +2.35 | +4.12 (14) | +3.34 | 30 | 30 | 40 |  |
| cf6s | +2.83 | +6.52 (22) | +4.12 | 30 | 30 | 40 |  |

## Primary counterfactual cf1: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +3.33 (24) | -10.74 (6) | +3.23 (24) | -11.15 (8) |
| line2 | +0.42 (20) | -0.40 (2) | +0.25 (30) | -0.88 (14) |
| line3 | +2.71 (30) | -11.62 (20) | +1.13 (30) | -7.94 (22) |
| line4 | +1.24 (28) | -0.65 (6) | +0.12 (16) | -0.63 (10) |
| line5 | +0.08 (38) | -2.21 (22) | +0.10 (38) | -1.88 (22) |
| line6 | +0.54 (20) | -0.78 (30) | +0.10 (32) | -2.04 (28) |
| headers | +0.27 (14) | -0.35 (8) | +0.11 (6) | -0.64 (18) |
| system | +2.27 (30) | -10.75 (6) | +3.58 (30) | -11.21 (4) |
| question | +0.77 (32) | -5.53 (28) | +0.11 (32) | -7.80 (26) |
| answer_instr | +0.08 (62) | -0.35 (6) | +0.00 (6) | -0.39 (8) |
| asst_header | +0.49 (20) | -5.40 (32) | +0.00 (18) | -6.21 (34) |
| answer_site | +0.32 (14) | -11.13 (80) | -0.01 (14) | -11.13 (80) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf1 run: max |ΔM| = 1.399 nats (vs Δbeh -11.13)
- library question: M(S) = -17.18 ('Walk<|eot_id|>'), M(C) = -13.90 ('Walk<|eot_id|>'); the largest M reached by any single patch = -13.26 → **stays Walk**

## Path validation: line1 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | -11.13 | -0.22 (2%) | +0.00 (-0%) | +0.02 (-0%) | -11.13 (100%) |
| 4 | -10.58 | +0.02 (-0%) | +0.00 (-0%) | +0.08 (-1%) | -10.58 (100%) |
| 8 | -10.39 | -0.59 (6%) | +0.00 (-0%) | +0.02 (-0%) | -10.39 (100%) |
| 12 | -9.65 | +0.07 (-1%) | +0.00 (-0%) | +0.08 (-1%) | -9.65 (100%) |
| 16 | -6.26 | -0.71 (11%) | +0.00 (-0%) | +0.08 (-1%) | -6.26 (100%) |
| 20 | +1.10 | -1.20 (-109%) | +0.00 (0%) | +0.08 (7%) | +1.10 (100%) |
| 24 | +3.33 | -0.21 (-6%) | +0.00 (0%) | +0.08 (2%) | +3.33 (100%) |
| 28 | +2.58 | +0.74 (29%) | +0.00 (0%) | +0.08 (3%) | +2.58 (100%) |
| 32 | -0.30 | +0.17 (-55%) | +0.00 (-0%) | -0.05 (18%) | -0.30 (100%) |
| 36 | +0.24 | +0.20 (81%) | +0.00 (0%) | +0.24 (102%) | +0.24 (100%) |
| 40 | -0.12 | +0.00 (-0%) | +0.00 (-0%) | -0.01 (4%) | -0.12 (100%) |
| 44 | -0.05 | +0.00 | +0.00 | -0.01 | -0.05 |
| 48 | -0.05 | -0.01 | +0.00 | +0.00 | -0.05 |
| 52 | +0.00 | -0.05 | +0.00 | +0.20 | +0.00 |
| 56 | -0.00 | +0.00 | +0.00 | +0.00 | -0.00 |
| 60 | +0.00 | +0.07 | +0.00 | +0.24 | +0.00 |
| 64 | +0.00 | +0.00 | +0.00 | -0.05 | +0.00 |
| 68 | +0.07 | -0.05 (-69%) | +0.00 (0%) | +0.00 (0%) | +0.07 (100%) |
| 72 | +0.00 | +0.00 | +0.00 | +0.07 | +0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
