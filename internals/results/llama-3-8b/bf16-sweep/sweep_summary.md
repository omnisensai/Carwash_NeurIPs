# cdim_sweep — llama-3-8b-Instruct (bf16)

grid.json: 4272 cells, 496.4 s

## Behavioural grid A: every question under every substrate

Drive tasks = scenarios whose rules imply drive; walk tasks = portable-object controls. P(drive) = fraction of cells whose argmax is a drive token. Selectivity = P(drive | drive task) − P(drive | walk task).

| substrate | drive tasks: mean M | P(drive) | walk tasks: mean M | P(drive) | selectivity | carwash P0+T1: M |
|---|---|---|---|---|---|---|
| none | -1.89 | 0.37 | -9.95 | 0.05 | +0.32 | -9.64 |
| L0 | +6.95 | 0.98 | -3.03 | 0.23 | +0.75 | +0.66 |
| L1 | +8.29 | 0.97 | -4.61 | 0.19 | +0.78 | +0.19 |
| L2 | +6.07 | 0.90 | -8.32 | 0.12 | +0.78 | -2.30 |
| L3 | +9.27 | 0.99 | -10.50 | 0.02 | +0.97 | +1.14 |
| L4 | +15.80 | 1.00 | -14.58 | 0.00 | +1.00 | +14.77 |
| L5 | +16.77 | 1.00 | -16.39 | 0.00 | +1.00 | +16.17 |
| S | +6.39 | 1.00 | -0.63 | 0.40 | +0.60 | +0.75 |
| pro | +6.28 | 1.00 | -4.61 | 0.11 | +0.89 | +0.14 |

## Operating envelope: M over the 12 question bodies × 3 tails

| scenario | substrate | min | median | max | sd | P(drive) |
|---|---|---|---|---|---|---|
| carwash (drive) | none | -11.01 | -5.50 | +11.13 | 5.21 | 0.28 |
| carwash (drive) | L0 | +0.48 | +6.11 | +15.23 | 4.58 | 1.00 |
| carwash (drive) | L1 | -0.56 | +7.76 | +15.46 | 4.98 | 0.94 |
| carwash (drive) | L2 | -4.69 | +4.44 | +13.48 | 4.76 | 0.75 |
| carwash (drive) | L3 | +0.18 | +10.06 | +14.27 | 4.33 | 0.97 |
| carwash (drive) | L4 | +13.32 | +16.09 | +17.52 | 1.15 | 1.00 |
| carwash (drive) | L5 | +14.85 | +16.66 | +18.30 | 0.96 | 1.00 |
| carwash (drive) | S | +0.75 | +6.19 | +13.07 | 3.46 | 1.00 |
| carwash (drive) | pro | +0.14 | +4.06 | +14.27 | 3.96 | 1.00 |
| fuel (drive) | none | -8.25 | -0.49 | +12.28 | 4.81 | 0.47 |
| fuel (drive) | L0 | +1.39 | +7.94 | +15.20 | 4.13 | 1.00 |
| fuel (drive) | L1 | +0.94 | +10.08 | +15.71 | 4.41 | 1.00 |
| fuel (drive) | L2 | -0.19 | +5.69 | +13.63 | 4.43 | 0.97 |
| fuel (drive) | L3 | +1.35 | +11.31 | +15.00 | 4.12 | 1.00 |
| fuel (drive) | L4 | +12.25 | +16.21 | +17.28 | 1.38 | 1.00 |
| fuel (drive) | L5 | +14.65 | +16.74 | +18.54 | 1.19 | 1.00 |
| fuel (drive) | S | +1.41 | +5.80 | +13.41 | 3.78 | 1.00 |
| fuel (drive) | pro | +2.49 | +8.26 | +15.12 | 3.95 | 1.00 |
| inspection (drive) | none | -11.87 | -3.87 | +7.73 | 4.62 | 0.31 |
| inspection (drive) | L0 | +0.75 | +6.81 | +14.32 | 3.90 | 1.00 |
| inspection (drive) | L1 | +0.03 | +7.87 | +14.44 | 4.32 | 0.97 |
| inspection (drive) | L2 | -1.07 | +6.94 | +14.59 | 4.62 | 0.94 |
| inspection (drive) | L3 | +1.30 | +9.94 | +14.92 | 4.05 | 1.00 |
| inspection (drive) | L4 | +13.93 | +16.38 | +17.41 | 1.01 | 1.00 |
| inspection (drive) | L5 | +15.19 | +16.63 | +18.34 | 0.93 | 1.00 |
| inspection (drive) | S | +1.00 | +5.30 | +11.38 | 3.09 | 1.00 |
| inspection (drive) | pro | +0.86 | +4.46 | +12.34 | 3.38 | 1.00 |
| oil (drive) | none | -8.12 | -1.41 | +12.41 | 4.88 | 0.44 |
| oil (drive) | L0 | +1.66 | +8.00 | +15.38 | 4.01 | 1.00 |
| oil (drive) | L1 | +1.45 | +9.63 | +15.20 | 4.03 | 1.00 |
| oil (drive) | L2 | +0.39 | +7.37 | +14.13 | 4.29 | 1.00 |
| oil (drive) | L3 | +2.15 | +12.32 | +15.30 | 3.71 | 1.00 |
| oil (drive) | L4 | +14.14 | +16.42 | +17.55 | 0.96 | 1.00 |
| oil (drive) | L5 | +15.25 | +16.60 | +18.28 | 0.95 | 1.00 |
| oil (drive) | S | +1.73 | +7.17 | +12.02 | 3.33 | 1.00 |
| oil (drive) | pro | +1.67 | +6.63 | +13.76 | 3.51 | 1.00 |
| parking (drive) | none | -11.49 | -3.02 | +8.99 | 5.15 | 0.28 |
| parking (drive) | L0 | -1.50 | +4.17 | +14.04 | 4.43 | 0.89 |
| parking (drive) | L1 | -2.08 | +4.91 | +14.00 | 4.76 | 0.86 |
| parking (drive) | L2 | -2.48 | +4.22 | +13.75 | 4.69 | 0.89 |
| parking (drive) | L3 | -0.24 | +9.62 | +14.08 | 4.60 | 0.97 |
| parking (drive) | L4 | +11.91 | +16.12 | +17.27 | 1.56 | 1.00 |
| parking (drive) | L5 | +14.61 | +16.79 | +18.49 | 1.11 | 1.00 |
| parking (drive) | S | +0.08 | +4.08 | +11.88 | 3.32 | 0.97 |
| parking (drive) | pro | +0.11 | +3.44 | +10.67 | 3.04 | 1.00 |
| tyres (drive) | none | -7.11 | -2.37 | +11.19 | 4.43 | 0.44 |
| tyres (drive) | L0 | +0.50 | +5.84 | +14.43 | 4.28 | 1.00 |
| tyres (drive) | L1 | +0.26 | +7.99 | +15.12 | 4.79 | 1.00 |
| tyres (drive) | L2 | -0.93 | +5.15 | +13.91 | 4.48 | 0.83 |
| tyres (drive) | L3 | +0.38 | +9.75 | +15.03 | 4.42 | 1.00 |
| tyres (drive) | L4 | +14.17 | +16.53 | +17.63 | 0.91 | 1.00 |
| tyres (drive) | L5 | +15.06 | +16.92 | +18.71 | 1.04 | 1.00 |
| tyres (drive) | S | +1.27 | +5.66 | +12.64 | 3.37 | 1.00 |
| tyres (drive) | pro | +1.42 | +5.44 | +14.16 | 3.56 | 1.00 |
| van (drive) | none | -9.37 | -2.62 | +11.75 | 4.81 | 0.33 |
| van (drive) | L0 | +0.80 | +7.55 | +15.53 | 4.63 | 1.00 |
| van (drive) | L1 | +0.69 | +9.38 | +15.34 | 4.77 | 1.00 |
| van (drive) | L2 | -3.09 | +6.50 | +13.25 | 4.52 | 0.92 |
| van (drive) | L3 | +2.92 | +12.87 | +15.54 | 3.60 | 1.00 |
| van (drive) | L4 | +13.77 | +16.12 | +17.72 | 1.05 | 1.00 |
| van (drive) | L5 | +15.11 | +16.77 | +18.29 | 0.96 | 1.00 |
| van (drive) | S | +1.59 | +8.44 | +13.72 | 3.81 | 1.00 |
| van (drive) | pro | +1.34 | +5.69 | +15.22 | 4.09 | 1.00 |
| bakery (walk) | none | -16.73 | -13.78 | +2.04 | 5.47 | 0.06 |
| bakery (walk) | L0 | -9.25 | -3.09 | +7.50 | 3.77 | 0.14 |
| bakery (walk) | L1 | -13.62 | -4.29 | +6.38 | 5.04 | 0.19 |
| bakery (walk) | L2 | -17.30 | -10.43 | +3.71 | 6.07 | 0.14 |
| bakery (walk) | L3 | -17.23 | -12.74 | -1.94 | 5.00 | 0.00 |
| bakery (walk) | L4 | -17.11 | -15.10 | -8.03 | 2.90 | 0.00 |
| bakery (walk) | L5 | -18.97 | -16.01 | -11.71 | 1.92 | 0.00 |
| bakery (walk) | S | -3.81 | -0.46 | +2.53 | 1.72 | 0.39 |
| bakery (walk) | pro | -9.10 | -4.15 | +0.63 | 2.96 | 0.11 |
| drycleaner (walk) | none | -16.43 | -12.47 | +4.21 | 5.63 | 0.06 |
| drycleaner (walk) | L0 | -7.75 | -3.67 | +8.03 | 3.75 | 0.28 |
| drycleaner (walk) | L1 | -10.87 | -3.04 | +8.61 | 4.71 | 0.22 |
| drycleaner (walk) | L2 | -16.99 | -8.44 | +5.78 | 6.23 | 0.17 |
| drycleaner (walk) | L3 | -16.93 | -12.10 | +0.14 | 5.41 | 0.03 |
| drycleaner (walk) | L4 | -17.36 | -15.66 | -10.09 | 1.75 | 0.00 |
| drycleaner (walk) | L5 | -19.22 | -16.50 | -13.51 | 1.26 | 0.00 |
| drycleaner (walk) | S | -3.36 | -0.47 | +4.25 | 2.06 | 0.44 |
| drycleaner (walk) | pro | -7.83 | -2.97 | +2.17 | 2.71 | 0.22 |
| keys (walk) | none | -16.39 | -12.67 | +1.59 | 5.50 | 0.06 |
| keys (walk) | L0 | -9.25 | -4.45 | +6.47 | 4.05 | 0.22 |
| keys (walk) | L1 | -13.11 | -6.62 | +5.75 | 5.20 | 0.17 |
| keys (walk) | L2 | -16.61 | -10.29 | +4.90 | 6.19 | 0.14 |
| keys (walk) | L3 | -16.59 | -12.22 | +0.72 | 5.51 | 0.08 |
| keys (walk) | L4 | -17.29 | -15.95 | -10.35 | 2.24 | 0.00 |
| keys (walk) | L5 | -18.46 | -16.29 | -12.35 | 1.47 | 0.00 |
| keys (walk) | S | -4.22 | -1.08 | +3.25 | 2.23 | 0.36 |
| keys (walk) | pro | -7.55 | -4.92 | +0.91 | 2.77 | 0.06 |
| library (walk) | none | -16.87 | -13.87 | +1.67 | 5.45 | 0.03 |
| library (walk) | L0 | -12.99 | -4.55 | +7.10 | 4.40 | 0.19 |
| library (walk) | L1 | -13.99 | -5.84 | +5.71 | 5.13 | 0.17 |
| library (walk) | L2 | -17.61 | -12.59 | +2.34 | 5.74 | 0.06 |
| library (walk) | L3 | -17.34 | -14.19 | -0.88 | 5.25 | 0.00 |
| library (walk) | L4 | -17.92 | -16.08 | -9.51 | 2.09 | 0.00 |
| library (walk) | L5 | -19.03 | -16.12 | -12.69 | 1.61 | 0.00 |
| library (walk) | S | -7.11 | -0.63 | +2.86 | 2.62 | 0.33 |
| library (walk) | pro | -14.36 | -9.81 | -1.05 | 3.77 | 0.00 |
| pharmacy (walk) | none | -15.87 | -12.57 | +2.02 | 5.20 | 0.03 |
| pharmacy (walk) | L0 | -8.75 | -4.07 | +8.00 | 3.86 | 0.25 |
| pharmacy (walk) | L1 | -13.49 | -4.48 | +7.25 | 4.80 | 0.17 |
| pharmacy (walk) | L2 | -16.74 | -8.81 | +4.91 | 6.02 | 0.11 |
| pharmacy (walk) | L3 | -16.61 | -12.33 | +0.10 | 5.57 | 0.00 |
| pharmacy (walk) | L4 | -17.36 | -15.48 | -9.69 | 2.26 | 0.00 |
| pharmacy (walk) | L5 | -19.15 | -16.07 | -13.39 | 1.50 | 0.00 |
| pharmacy (walk) | S | -4.48 | -0.18 | +3.49 | 2.00 | 0.44 |
| pharmacy (walk) | pro | -9.61 | -4.19 | +1.53 | 3.04 | 0.17 |
| post (walk) | none | -15.49 | -11.19 | +5.21 | 5.83 | 0.06 |
| post (walk) | L0 | -8.62 | -3.23 | +9.35 | 4.04 | 0.31 |
| post (walk) | L1 | -11.12 | -3.01 | +7.38 | 4.80 | 0.19 |
| post (walk) | L2 | -16.61 | -7.89 | +4.94 | 6.20 | 0.14 |
| post (walk) | L3 | -16.49 | -12.80 | -1.15 | 5.44 | 0.00 |
| post (walk) | L4 | -17.79 | -15.81 | -8.89 | 2.39 | 0.00 |
| post (walk) | L5 | -19.27 | -16.02 | -13.74 | 1.44 | 0.00 |
| post (walk) | S | -4.22 | -0.50 | +2.92 | 1.92 | 0.42 |
| post (walk) | pro | -8.49 | -4.15 | +1.27 | 2.94 | 0.11 |

## Question tail (T0 'one word:', T1 '...: walk or drive', T2 '...: drive or walk'), drive tasks, mean M

| substrate | T0 | T1 | T2 | max−min |
|---|---|---|---|---|
| none | -3.63 | -5.52 | +3.50 | 9.02 |
| L0 | +6.31 | +3.34 | +11.22 | 7.88 |
| L1 | +8.48 | +3.91 | +12.48 | 8.57 |
| L2 | +5.83 | +1.31 | +11.06 | 9.75 |
| L3 | +10.39 | +4.17 | +13.26 | 9.09 |
| L4 | +16.28 | +14.39 | +16.73 | 2.34 |
| L5 | +17.99 | +15.64 | +16.69 | 2.35 |
| S | +6.76 | +2.76 | +9.66 | 6.90 |
| pro | +6.80 | +2.66 | +9.37 | 6.71 |

## Grid B: walk questions under the carwash-filled concrete substrates (leak test)

| question | L2 | L3 | L4 | L5 | S |
|---|---|---|---|---|---|
| bakery (walk) | -10.80 walk | -8.28 walk | +0.88 drive | +8.13 drive | -3.81 walk |
| drycleaner (walk) | -8.48 walk | -7.18 walk | +1.68 drive | +7.69 drive | -2.91 walk |
| fuel (drive) | -0.03 walk | +0.03 walk | +7.14 drive | +12.34 drive | +1.41 drive |
| inspection (drive) | -0.83 walk | +1.33 drive | +8.70 drive | +14.45 drive | +1.00 drive |
| keys (walk) | -11.31 walk | -9.43 walk | -1.97 walk | +3.62 drive | -4.00 walk |
| library (walk) | -11.80 walk | -8.73 walk | -1.14 walk | +2.72 drive | -4.42 walk |
| oil (drive) | +0.91 drive | +1.76 drive | +11.14 drive | +14.58 drive | +1.73 drive |
| parking (drive) | -1.77 walk | -2.35 walk | +7.40 drive | +13.26 drive | +0.86 drive |
| pharmacy (walk) | -9.15 walk | -6.87 walk | +0.40 drive | +6.59 drive | -2.84 walk |
| post (walk) | -10.46 walk | -8.11 walk | -1.28 walk | +3.91 drive | -3.87 walk |
| tyres (drive) | -0.86 walk | -0.19 walk | +7.51 drive | +13.88 drive | +1.27 drive |
| van (drive) | -0.06 walk | +4.44 drive | +14.82 drive | +16.06 drive | +1.59 drive |

## CDIM: scenario

| cell | M(S) | greedy | primary line | Δ | flips | line carries ≥½Δ until (row / depth) | answer site from (row / depth) | share via question | random ctrl | control stays walk |
|---|---|---|---|---|---|---|---|---|---|---|
| fuel | +1.41 | 'drive<|eot_id|>' | cf9s (line 9) | +1.89 | yes | 12 / 0.38 | 15 / 0.47 | 24% | 0.37 | True |
| inspection | +1.00 | 'drive<|eot_id|>' | cf7 (line 7) | +1.87 | yes | 12 / 0.38 | 15 / 0.47 | 53% | 0.57 | True |
| tyres | +1.27 | 'drive<|eot_id|>' | cf7 (line 7) | +2.03 | yes | 13 / 0.41 | 15 / 0.47 | 47% | 0.55 | True |

