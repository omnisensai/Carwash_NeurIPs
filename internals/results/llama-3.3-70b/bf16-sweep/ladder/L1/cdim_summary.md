# CDIM — Llama-3.3-70B-Instruct (bf16), ladder/L1 (internals/cdim_sweep/generated/substrates/carwash/L1.txt)

M(S) = +5.185 (greedy 'Drive<|eot_id|>'); 80 layers, 197 tokens; rows = embedding + each layer output; 828.7 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +11.54 | -6.35 | 'Drive<|eot_id|>' | - Perform an activity on an object, without transporting the object from location A to B. |
| cf2 | 2 | reverse | True | +6.79 | -1.60 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +8.18 | -2.99 | 'Drive<|eot_id|>' | - Activities require the object to stay at location A while the user moves to location B, whether the user walks or drives. |
| cf4 | 4 | reverse | True | +6.74 | -1.56 | 'Drive<|eot_id|>' | - The object is never initially with the user at location A. |
| cf5 | 5 | reverse | True | -2.80 | +7.98 | 'walk<|eot_id|>' | - Moving the user without moving the object, as when the user walks away from it, does fully satisfy the objective. |
| cf6 | 6 | reverse | True | -0.09 | +5.27 | 'Drive<|eot_id|>' | - If the object is a vehicle, the user may leave it, that is walk off, in order to perform the activity at location B. |
| cf6s | 6 | strong-reverse | True | -5.14 | +10.33 | 'walk<|eot_id|>' | - If the object is a vehicle, the user must leave it, that is walk off, in order to perform the activity at location B. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf1 | -6.35 | -6.74 (12) | -6.63 | 16 | None | 40 |  |
| cf2 | -1.60 | -2.00 (4) | -1.80 | 16 | 22 | 36 |  |
| cf3 | -2.99 | -3.79 (8) | -4.39 | 16 | 18 | 40 |  |
| cf4 | -1.56 | -2.99 (16) | -2.57 | 28 | None | 36 |  |
| cf5 | +7.98 | +8.07 (4) | +8.64 | 22 | None | 36 |  |
| cf6 | +5.27 | +7.28 (16) | +6.49 | 28 | 30 | 38 |  |
| cf6s | +10.33 | +12.15 (16) | +11.70 | 28 | 30 | 40 |  |

## Primary counterfactual cf6s: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line6 | +12.15 (16) | +0.00 (76) | +11.70 (16) | -0.00 (72) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +12.15 (16) | +0.00 (76) | +11.70 (16) | -0.00 (72) |
| question | +5.50 (30) | -1.24 (16) | +5.93 (30) | -1.82 (16) |
| answer_instr | +0.36 (50) | -0.04 (20) | +0.56 (14) | -0.07 (36) |
| asst_header | +1.24 (32) | -0.24 (22) | +2.05 (32) | -0.32 (26) |
| answer_site | +10.35 (78) | -0.01 (20) | +10.33 (80) | -0.22 (10) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf6s run: max |ΔM| = 2.367 nats (vs Δbeh +10.33)
- library question: M(S) = -18.98 ('Walk<|eot_id|>'), M(C) = -18.08 ('Walk<|eot_id|>'); the largest M reached by any single patch = -17.35 → **stays Walk**

## Path validation: line6 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +10.33 | +0.25 (2%) | +0.00 (0%) | +0.35 (3%) | +10.33 (100%) |
| 4 | +10.37 | +0.26 (2%) | +0.00 (0%) | +0.11 (1%) | +10.37 (100%) |
| 8 | +10.20 | -0.50 (-5%) | +0.00 (0%) | +0.11 (1%) | +10.20 (100%) |
| 12 | +11.02 | -0.26 (-2%) | +0.00 (0%) | -0.00 (-0%) | +11.02 (100%) |
| 16 | +12.15 | +0.14 (1%) | +0.00 (0%) | +0.01 (0%) | +12.15 (100%) |
| 20 | +11.46 | +1.24 (11%) | +0.00 (0%) | +0.01 (0%) | +11.46 (100%) |
| 24 | +8.82 | +0.76 (9%) | +0.00 (0%) | -0.01 (-0%) | +8.82 (100%) |
| 28 | +5.59 | +2.11 (38%) | +0.00 (0%) | +0.26 (5%) | +5.59 (100%) |
| 32 | +0.61 | -0.13 (-22%) | +0.00 (0%) | +0.11 (18%) | +0.61 (100%) |
| 36 | +0.61 | +0.24 (40%) | +0.00 (0%) | +0.36 (60%) | +0.61 (100%) |
| 40 | +0.24 | -0.00 (-0%) | +0.00 (0%) | -0.00 (-0%) | +0.24 (100%) |
| 44 | +0.49 | +0.12 (24%) | +0.00 (0%) | +0.36 (72%) | +0.49 (100%) |
| 48 | +0.24 | +0.24 (98%) | +0.00 (0%) | -0.01 (-2%) | +0.24 (100%) |
| 52 | +0.24 | +0.24 (98%) | +0.00 (0%) | +0.24 (100%) | +0.24 (100%) |
| 56 | +0.24 | +0.24 (98%) | +0.00 (0%) | -0.01 (-2%) | +0.24 (100%) |
| 60 | +0.36 | +0.12 (32%) | +0.00 (0%) | +0.24 (66%) | +0.36 (100%) |
| 64 | +0.24 | +0.12 (48%) | +0.00 (0%) | +0.36 (146%) | +0.24 (100%) |
| 68 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 72 | +0.00 | -0.00 | +0.00 | +0.00 | +0.00 |
| 76 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
