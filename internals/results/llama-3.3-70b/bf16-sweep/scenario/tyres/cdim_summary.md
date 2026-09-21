# CDIM — Llama-3.3-70B-Instruct (bf16), scenario/tyres (internals/cdim_sweep/generated/substrates/tyres/S.txt)

M(S) = +13.401 (greedy 'Drive<|eot_id|>'); 80 layers, 192 tokens; rows = embedding + each layer output; 692.7 s.

## Counterfactuals (token-aligned, one line replaced)

| name | line | kind | aligned | M(C) | Δbeh = M(S)−M(C) | greedy | counterfactual line |
|---|---|---|---|---|---|---|---|
| cf1 | 1 | reverse | True | +12.93 | +0.47 | 'Drive<|eot_id|>' | - Perform an activity on an object at the starting location. |
| cf2 | 2 | reverse | True | +13.29 | +0.11 | 'Drive<|eot_id|>' | - All other objectives or goals are relevant for the user. |
| cf3 | 3 | reverse | True | +12.91 | +0.49 | 'Drive<|eot_id|>' | - The object is initially away from the user at another location. |
| cf4 | 4 | reverse | True | +13.30 | +0.10 | 'Drive<|eot_id|>' | - The activity is performed at the starting location. |
| cf5 | 5 | reverse | True | +11.54 | +1.86 | 'Drive<|eot_id|>' | - The object need not reach the service location for the activity performance. |
| cf6 | 6 | reverse | True | +12.36 | +1.04 | 'Drive<|eot_id|>' | - Vehicles are fully portable. |
| cf7 | 7 | reverse | True | +13.56 | -0.16 | 'Drive<|eot_id|>' | - Walking brings a vehicle along. |
| cf8 | 8 | reverse | True | +13.32 | +0.08 | 'Drive<|eot_id|>' | - Walking does fully transport a vehicle. |
| cf9 | 9 | reverse | True | +10.36 | +3.04 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user may leave it. |
| cf9s | 9 | strong-reverse | True | +9.48 | +3.92 | 'Drive<|eot_id|>' | - To transport a vehicle from one location to another, the user must leave it. |

## Where the line's effect sits (rows ≥ 1, i.e. inside the network)

| cf | Δbeh | peak R on own line (row) | peak D on own line | last row where R(line) ≥ ½Δ | first row where R(question) ≥ ½Δ | first row where R(answer site) ≥ ½Δ | LOO deletion |
|---|---|---|---|---|---|---|---|
| cf5 | +1.86 | +2.12 (6) | +1.85 | 28 | None | 38 |  |
| cf6 | +1.04 | +1.19 (12) | +1.29 | 20 | None | 36 |  |
| cf9 | +3.04 | +3.30 (2) | +3.28 | 28 | 30 | 36 |  |
| cf9s | +3.92 | +4.29 (22) | +4.04 | 28 | 30 | 36 |  |

## Primary counterfactual cf9s: R and D by group (max over rows ≥ 1, and the row)

| group | max R (row) | min R (row) | max D (row) | min D (row) |
|---|---|---|---|---|
| line1 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line2 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line3 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line4 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line5 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line6 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line7 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line8 | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| line9 | +4.29 (22) | -0.00 (56) | +4.04 (4) | -0.27 (56) |
| headers | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| definitions | +0.00 (2) | +0.00 (2) | +0.00 (2) | +0.00 (2) |
| system | +4.29 (22) | -0.00 (56) | +4.04 (4) | -0.27 (56) |
| question | +2.78 (30) | -0.48 (22) | +1.01 (30) | -0.51 (26) |
| answer_instr | +0.13 (26) | -0.02 (8) | +0.12 (28) | -0.26 (12) |
| asst_header | +1.64 (28) | -0.27 (72) | +1.15 (32) | -0.26 (2) |
| answer_site | +3.92 (80) | -0.02 (8) | +3.92 (80) | -0.26 (6) |

## Controls

- same-run patch S→S: max |ΔM| = 0.0000 nats
- random direction of the same norm as S−C in the cf9s run: max |ΔM| = 1.765 nats (vs Δbeh +3.92)
- library question: M(S) = -12.78 ('walk<|eot_id|>'), M(C) = -13.73 ('Walk<|eot_id|>'); the largest M reached by any single patch = -12.32 → **stays Walk**

## Path validation: line9 → question / answer site (rows 0…80)

Fraction of the source rescue that survives when only the receiver state is transplanted (receiver row = the first grid row after the source, and the last grid row):

| source row | total R | via question @next | via question @last | via answer site @next | via answer site @last |
|---|---|---|---|---|---|
| 0 | +3.92 | +0.00 (0%) | +0.00 (0%) | +0.03 (1%) | +3.92 (100%) |
| 4 | +4.05 | +0.13 (3%) | +0.00 (0%) | +0.00 (0%) | +4.05 (100%) |
| 8 | +4.17 | +0.39 (9%) | +0.00 (0%) | +0.12 (3%) | +4.17 (100%) |
| 12 | +4.18 | +0.14 (3%) | +0.00 (0%) | +0.00 (0%) | +4.18 (100%) |
| 16 | +4.04 | +0.25 (6%) | +0.00 (0%) | +0.02 (0%) | +4.04 (100%) |
| 20 | +4.17 | +0.84 (20%) | +0.00 (0%) | +0.11 (3%) | +4.17 (100%) |
| 24 | +3.92 | +1.15 (29%) | +0.00 (0%) | +0.11 (3%) | +3.92 (100%) |
| 28 | +3.02 | +1.51 (50%) | +0.00 (0%) | +0.86 (28%) | +3.02 (100%) |
| 32 | +0.40 | +0.12 (31%) | +0.00 (0%) | +0.13 (31%) | +0.40 (100%) |
| 36 | +0.25 | +0.12 (50%) | +0.00 (0%) | +0.13 (50%) | +0.25 (100%) |
| 40 | +0.11 | +0.12 (116%) | +0.00 (0%) | +0.11 (100%) | +0.11 (100%) |
| 44 | +0.11 | +0.13 (116%) | +0.00 (0%) | +0.12 (116%) | +0.11 (100%) |
| 48 | +0.12 | +0.00 (1%) | +0.00 (0%) | +0.12 (100%) | +0.12 (100%) |
| 52 | +0.12 | +0.00 (0%) | +0.00 (0%) | +0.02 (13%) | +0.12 (100%) |
| 56 | -0.00 | +0.12 | +0.00 | +0.00 | -0.00 |
| 60 | +0.02 | +0.12 | +0.00 | +0.00 | +0.02 |
| 64 | +0.02 | +0.12 | +0.00 | +0.00 | +0.02 |
| 68 | +0.12 | +0.12 (100%) | +0.00 (0%) | +0.02 (13%) | +0.12 (100%) |
| 72 | -0.00 | +0.11 | +0.00 | +0.00 | -0.00 |
| 76 | +0.12 | +0.00 (0%) | +0.00 (0%) | +0.12 (100%) | +0.12 (100%) |

Figures: cdim_map.png (Fig. 2), cdim_maps_all.png, cdim_agreement.png (Fig. 3), cdim_path.png (Fig. 5), cdim_library.png, cdim_lens_vs_rescue.png.
