# CDIM — Llama-3.3-70B-Instruct (bf16), substrate.txt (substrate.txt)

M(S) = +6.075 (greedy 'Drive<|eot_id|>'); 80 layers, 173 tokens; rows = embedding + each layer output; 2015.9 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +9.04 | -2.96 | 'Drive<|eot_id|>' | - Perform an activity on an object, without transporting the object from location A to B. |
| cf2 | 2 | reverse | True | +6.52 | -0.44 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +5.56 | +0.51 | 'Drive<|eot_id|>' | - Activities require the object to stay at location A while the user moves to location B. |
| cf4 | 4 | reverse | True | +4.59 | +1.49 | 'Drive<|eot_id|>' | - The object is never initially with the user at location A. |
| cf5 | 5 | reverse | True | -3.44 | +9.52 | 'walk<|eot_id|>' | - Moving the user without moving the object does fully satisfy the objective. |
| cf6 | 6 | reverse | True | +2.57 | +3.50 | 'Drive<|eot_id|>' | - If the object is a vehicle, the user may leave the object in order to perform the activity at location B. |
| cf6n | 6 | neutral | True | +0.06 | +6.01 | 'Drive<|eot_id|>' | - If the object is a vehicle, the user must inspect the object in order to perform the activity at location B. |
| cf6s | 6 | strong-reverse | True | -1.68 | +7.75 | 'walk<|eot_id|>' | - If the object is a vehicle, the user must leave the object in order to perform the activity at location B. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | -2.96 | -3.06 (22) | -4.24 | 14 | 16 | 40 | +11.30 |
| cf2 | -0.44 | -0.65 (24) | -0.39 | 38 | 2 | 20 | +2.98 |
| cf3 | +0.51 | +6.42 (22) | +6.75 | 34 | 14 | 30 | +2.26 |
| cf4 | +1.49 | +2.81 (20) | +0.84 | 24 | 2 | 40 | -0.51 |
| cf5 | +9.52 | +10.53 (12) | +10.34 | 24 | None | 36 | +3.75 |
| cf6 | +3.50 | +6.07 (16) | +5.48 | 30 | 30 | 38 | +7.86 |
| cf6n | +6.01 | +8.81 (22) | +6.91 | 30 | 30 | 36 | +7.86 |
| cf6s | +7.75 | +10.97 (18) | +9.54 | 28 | 30 | 40 | +7.86 |

## Primary counterfactual cf5: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +10.53 (12) | -0.27 (32) | +10.34 (12) | -0.20 (50) |
| line6 | +1.74 (22) | -0.39 (32) | +1.88 (22) | -0.39 (32) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +10.16 (12) | -0.16 (58) | +10.17 (12) | -0.15 (40) |
| question | +2.60 (30) | -0.33 (10) | +2.75 (30) | -0.69 (14) |
| answer_instr | +0.50 (6) | -0.32 (2) | +0.00 (26) | -0.39 (32) |
| asst_header | +2.67 (28) | -0.33 (16) | +1.92 (28) | -0.58 (22) |
| answer_site | +9.71 (56) | -0.16 (10) | +9.52 (78) | -0.39 (2) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf5 run: max |ΔM| = 1.845 nats (vs Δbeh +9.52)
- library question: M(S) = -18.37 ('Walk.<|eot_id|>'), M(C) = -17.62 ('Walk.<|eot_id|>'); the largest M reached by any single patch = -17.25 → **stays Walk**

## Path validation: line5 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +9.52 | +0.10 (1%) | +0.00 (0%) | -0.15 (-2%) | +9.52 (100%) |
| 4 | +10.08 | -0.15 (-2%) | +0.00 (0%) | +0.00 (0%) | +10.08 (100%) |
| 8 | +9.28 | -0.16 (-2%) | +0.00 (0%) | -0.00 (-0%) | +9.28 (100%) |
| 12 | +10.53 | +0.34 (3%) | +0.00 (0%) | +0.01 (0%) | +10.53 (100%) |
| 16 | +9.47 | +0.43 (5%) | +0.00 (0%) | -0.16 (-2%) | +9.47 (100%) |
| 20 | +8.02 | +0.85 (11%) | +0.00 (0%) | -0.15 (-2%) | +8.02 (100%) |
| 24 | +5.11 | +0.67 (13%) | +0.00 (0%) | +0.25 (5%) | +5.11 (100%) |
| 28 | +0.80 | -0.15 (-19%) | +0.00 (0%) | +0.01 (1%) | +0.80 (100%) |
| 32 | -0.27 | -0.16 (59%) | +0.00 (-0%) | +0.01 (-3%) | -0.27 (100%) |
| 36 | -0.15 | +0.00 (-3%) | +0.00 (-0%) | -0.16 (103%) | -0.15 (100%) |
| 40 | -0.16 | -0.16 (100%) | +0.00 (-0%) | -0.16 (98%) | -0.16 (100%) |
| 44 | -0.16 | -0.00 (0%) | +0.00 (-0%) | -0.00 (0%) | -0.16 (100%) |
| 48 | -0.00 | -0.00 | +0.00 | -0.00 | -0.00 |
| 52 | -0.00 | +0.00 | +0.00 | +0.01 | -0.00 |
| 56 | +0.00 | -0.00 | +0.00 | -0.00 | +0.00 |
| 60 | -0.16 | +0.00 (-0%) | +0.00 (-0%) | +0.00 (-2%) | -0.16 (100%) |
| 64 | +0.00 | +0.00 | +0.00 | -0.00 | +0.00 |
| 68 | -0.00 | +0.00 | +0.00 | -0.00 | -0.00 |
| 72 | +0.00 | -0.00 | +0.00 | +0.00 | +0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
