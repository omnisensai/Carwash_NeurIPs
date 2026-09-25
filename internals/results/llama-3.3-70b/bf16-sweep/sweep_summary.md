# cdim_sweep — Llama-3.3-70B-Instruct (bf16)

grid.json: 4272 cells, 597.5 s

## Behavioural grid A: every question under every substrate

Drive tasks = scenarios whose rules imply drive; walk tasks = portable-object controls. P(drive) = fraction of cells whose argmax is a drive token. Selectivity = P(drive | drive task) − P(drive | walk task).

| substrate | drive tasks: mean M | P(drive) | walk tasks: mean M | P(drive) | selectivity | carwash P0+T1: M |
|---|---|---|---|---|---|---|
| none | -8.39 | 0.11 | -19.31 | 0.00 | +0.11 | -13.65 |
| L0 | +10.65 | 0.90 | -16.60 | 0.00 | +0.90 | +6.15 |
| L1 | +9.70 | 0.90 | -16.55 | 0.00 | +0.90 | +5.18 |
| L2 | +6.58 | 0.82 | -17.65 | 0.00 | +0.82 | -0.71 |
| L3 | +12.63 | 0.98 | -17.84 | 0.00 | +0.98 | +11.45 |
| L4 | +21.34 | 1.00 | -19.84 | 0.00 | +1.00 | +21.56 |
| L5 | +22.75 | 1.00 | -24.39 | 0.00 | +1.00 | +23.15 |
| S | +13.62 | 0.98 | -15.10 | 0.00 | +0.98 | +15.01 |
| pro | +17.17 | 1.00 | -18.19 | 0.00 | +1.00 | +17.31 |

## Operating envelope: M over the 12 question bodies × 3 tails

| scenario | substrate | min | median | max | sd | P(drive) |
|---|---|---|---|---|---|---|
| carwash (drive) | none | -18.00 | -12.27 | -2.75 | 3.19 | 0.00 |
| carwash (drive) | L0 | -7.96 | +13.97 | +18.95 | 6.61 | 0.92 |
| carwash (drive) | L1 | -6.10 | +10.87 | +18.20 | 6.38 | 0.86 |
| carwash (drive) | L2 | -11.36 | +2.99 | +17.35 | 7.59 | 0.67 |
| carwash (drive) | L3 | -1.75 | +11.29 | +22.23 | 5.22 | 0.94 |
| carwash (drive) | L4 | +14.62 | +21.79 | +27.64 | 3.41 | 1.00 |
| carwash (drive) | L5 | +16.38 | +23.25 | +27.61 | 2.61 | 1.00 |
| carwash (drive) | S | +10.75 | +16.41 | +21.30 | 2.53 | 1.00 |
| carwash (drive) | pro | +14.12 | +19.03 | +26.23 | 2.87 | 1.00 |
| fuel (drive) | none | -14.75 | -4.98 | +8.00 | 6.05 | 0.31 |
| fuel (drive) | L0 | -10.37 | +13.14 | +16.05 | 6.80 | 0.89 |
| fuel (drive) | L1 | -4.25 | +10.82 | +15.94 | 4.53 | 0.94 |
| fuel (drive) | L2 | -8.90 | +10.91 | +18.86 | 6.41 | 0.89 |
| fuel (drive) | L3 | -0.10 | +12.19 | +20.86 | 4.55 | 1.00 |
| fuel (drive) | L4 | +12.25 | +21.10 | +28.32 | 3.97 | 1.00 |
| fuel (drive) | L5 | +16.50 | +23.45 | +27.08 | 3.04 | 1.00 |
| fuel (drive) | S | +8.87 | +12.06 | +16.45 | 1.70 | 1.00 |
| fuel (drive) | pro | +6.50 | +17.10 | +23.31 | 3.13 | 1.00 |
| inspection (drive) | none | -20.50 | -9.19 | +5.48 | 5.50 | 0.08 |
| inspection (drive) | L0 | -12.50 | +14.94 | +18.44 | 6.67 | 0.92 |
| inspection (drive) | L1 | -7.75 | +13.18 | +17.31 | 5.55 | 0.94 |
| inspection (drive) | L2 | -7.82 | +8.89 | +18.10 | 6.31 | 0.89 |
| inspection (drive) | L3 | +1.75 | +13.12 | +23.60 | 4.66 | 1.00 |
| inspection (drive) | L4 | +13.75 | +20.97 | +27.41 | 3.28 | 1.00 |
| inspection (drive) | L5 | +16.87 | +22.63 | +26.99 | 2.41 | 1.00 |
| inspection (drive) | S | +10.50 | +14.19 | +21.45 | 2.41 | 1.00 |
| inspection (drive) | pro | +8.00 | +17.19 | +23.95 | 2.91 | 1.00 |
| oil (drive) | none | -18.25 | -10.51 | +6.48 | 5.04 | 0.06 |
| oil (drive) | L0 | -11.48 | +13.07 | +17.82 | 7.37 | 0.86 |
| oil (drive) | L1 | -10.03 | +11.14 | +16.32 | 5.54 | 0.94 |
| oil (drive) | L2 | -4.33 | +10.48 | +18.11 | 5.69 | 0.92 |
| oil (drive) | L3 | +0.50 | +14.02 | +23.72 | 4.87 | 1.00 |
| oil (drive) | L4 | +14.87 | +22.39 | +29.02 | 3.13 | 1.00 |
| oil (drive) | L5 | +19.15 | +24.19 | +28.31 | 2.08 | 1.00 |
| oil (drive) | S | +11.87 | +15.15 | +21.06 | 2.22 | 1.00 |
| oil (drive) | pro | +9.62 | +18.36 | +25.41 | 3.11 | 1.00 |
| parking (drive) | none | -18.00 | -10.25 | +7.42 | 5.79 | 0.08 |
| parking (drive) | L0 | -8.67 | +8.08 | +16.43 | 6.45 | 0.89 |
| parking (drive) | L1 | -4.71 | +9.33 | +16.55 | 6.30 | 0.78 |
| parking (drive) | L2 | -1.35 | +6.45 | +17.84 | 5.80 | 0.94 |
| parking (drive) | L3 | +3.25 | +12.34 | +22.86 | 4.46 | 1.00 |
| parking (drive) | L4 | +15.12 | +21.56 | +27.27 | 3.07 | 1.00 |
| parking (drive) | L5 | +15.75 | +22.64 | +27.20 | 2.96 | 1.00 |
| parking (drive) | S | -4.50 | +3.81 | +11.15 | 4.21 | 0.83 |
| parking (drive) | pro | +4.25 | +11.74 | +16.48 | 3.44 | 1.00 |
| tyres (drive) | none | -18.00 | -9.74 | +2.24 | 3.86 | 0.03 |
| tyres (drive) | L0 | -11.25 | +9.50 | +15.00 | 6.73 | 0.89 |
| tyres (drive) | L1 | -5.81 | +9.22 | +14.50 | 5.14 | 0.92 |
| tyres (drive) | L2 | -10.03 | +2.66 | +13.97 | 6.53 | 0.61 |
| tyres (drive) | L3 | -2.75 | +8.25 | +19.36 | 5.03 | 0.94 |
| tyres (drive) | L4 | +12.75 | +20.38 | +26.07 | 3.40 | 1.00 |
| tyres (drive) | L5 | +14.12 | +21.63 | +26.37 | 2.89 | 1.00 |
| tyres (drive) | S | +11.25 | +14.77 | +20.46 | 1.91 | 1.00 |
| tyres (drive) | pro | +9.62 | +16.09 | +22.57 | 2.40 | 1.00 |
| van (drive) | none | -16.00 | -7.74 | +9.58 | 6.51 | 0.19 |
| van (drive) | L0 | -9.37 | +14.97 | +20.69 | 6.67 | 0.94 |
| van (drive) | L1 | -2.25 | +12.47 | +18.50 | 5.20 | 0.94 |
| van (drive) | L2 | -8.94 | +7.82 | +19.72 | 6.83 | 0.81 |
| van (drive) | L3 | +4.00 | +16.96 | +24.59 | 4.45 | 1.00 |
| van (drive) | L4 | +16.12 | +23.79 | +28.86 | 3.17 | 1.00 |
| van (drive) | L5 | +18.34 | +24.63 | +28.20 | 2.37 | 1.00 |
| van (drive) | S | +12.62 | +17.14 | +23.04 | 2.62 | 1.00 |
| van (drive) | pro | +10.62 | +19.17 | +26.77 | 3.41 | 1.00 |
| bakery (walk) | none | -24.12 | -20.09 | -13.87 | 2.08 | 0.00 |
| bakery (walk) | L0 | -22.60 | -17.46 | -13.62 | 1.86 | 0.00 |
| bakery (walk) | L1 | -22.17 | -17.68 | -11.87 | 2.10 | 0.00 |
| bakery (walk) | L2 | -24.88 | -18.64 | -14.50 | 1.97 | 0.00 |
| bakery (walk) | L3 | -24.18 | -18.69 | -13.50 | 2.36 | 0.00 |
| bakery (walk) | L4 | -24.26 | -19.37 | -16.35 | 2.38 | 0.00 |
| bakery (walk) | L5 | -27.90 | -24.55 | -19.68 | 2.10 | 0.00 |
| bakery (walk) | S | -19.01 | -16.36 | -10.37 | 1.93 | 0.00 |
| bakery (walk) | pro | -21.57 | -18.51 | -12.00 | 2.10 | 0.00 |
| drycleaner (walk) | none | -23.70 | -19.41 | -13.12 | 2.16 | 0.00 |
| drycleaner (walk) | L0 | -21.60 | -16.14 | -13.25 | 1.62 | 0.00 |
| drycleaner (walk) | L1 | -21.63 | -16.26 | -12.00 | 2.00 | 0.00 |
| drycleaner (walk) | L2 | -23.91 | -17.07 | -12.00 | 2.36 | 0.00 |
| drycleaner (walk) | L3 | -24.52 | -17.05 | -12.00 | 2.56 | 0.00 |
| drycleaner (walk) | L4 | -25.65 | -19.36 | -16.37 | 2.67 | 0.00 |
| drycleaner (walk) | L5 | -28.18 | -24.56 | -20.51 | 1.82 | 0.00 |
| drycleaner (walk) | S | -18.64 | -14.41 | -9.37 | 1.91 | 0.00 |
| drycleaner (walk) | pro | -24.95 | -17.72 | -12.12 | 2.95 | 0.00 |
| keys (walk) | none | -23.47 | -19.56 | -13.62 | 2.33 | 0.00 |
| keys (walk) | L0 | -23.09 | -18.21 | -12.81 | 2.15 | 0.00 |
| keys (walk) | L1 | -23.00 | -18.10 | -12.00 | 2.47 | 0.00 |
| keys (walk) | L2 | -25.06 | -18.85 | -12.25 | 2.45 | 0.00 |
| keys (walk) | L3 | -24.97 | -18.32 | -13.37 | 2.49 | 0.00 |
| keys (walk) | L4 | -25.64 | -18.93 | -16.00 | 2.77 | 0.00 |
| keys (walk) | L5 | -28.75 | -24.69 | -20.21 | 2.14 | 0.00 |
| keys (walk) | S | -21.55 | -16.49 | -11.00 | 1.97 | 0.00 |
| keys (walk) | pro | -23.89 | -18.83 | -11.87 | 2.37 | 0.00 |
| library (walk) | none | -24.50 | -19.97 | -14.25 | 2.13 | 0.00 |
| library (walk) | L0 | -22.30 | -17.56 | -12.87 | 1.91 | 0.00 |
| library (walk) | L1 | -22.71 | -17.57 | -12.00 | 2.26 | 0.00 |
| library (walk) | L2 | -25.14 | -18.20 | -13.62 | 2.23 | 0.00 |
| library (walk) | L3 | -24.67 | -18.41 | -12.87 | 2.26 | 0.00 |
| library (walk) | L4 | -25.47 | -19.50 | -16.38 | 2.70 | 0.00 |
| library (walk) | L5 | -27.73 | -24.59 | -18.78 | 2.24 | 0.00 |
| library (walk) | S | -19.14 | -15.54 | -10.50 | 1.87 | 0.00 |
| library (walk) | pro | -27.10 | -21.43 | -13.75 | 3.03 | 0.00 |
| pharmacy (walk) | none | -22.71 | -19.07 | -12.75 | 2.04 | 0.00 |
| pharmacy (walk) | L0 | -20.05 | -16.04 | -11.37 | 1.84 | 0.00 |
| pharmacy (walk) | L1 | -20.29 | -15.50 | -11.25 | 1.90 | 0.00 |
| pharmacy (walk) | L2 | -23.09 | -16.91 | -12.12 | 2.11 | 0.00 |
| pharmacy (walk) | L3 | -22.04 | -17.36 | -11.50 | 1.95 | 0.00 |
| pharmacy (walk) | L4 | -24.77 | -18.84 | -16.12 | 2.39 | 0.00 |
| pharmacy (walk) | L5 | -27.66 | -24.55 | -19.75 | 1.96 | 0.00 |
| pharmacy (walk) | S | -17.40 | -14.30 | -8.62 | 1.90 | 0.00 |
| pharmacy (walk) | pro | -20.86 | -16.50 | -10.50 | 2.30 | 0.00 |
| post (walk) | none | -23.53 | -18.22 | -12.12 | 2.08 | 0.00 |
| post (walk) | L0 | -20.84 | -15.82 | -12.32 | 1.78 | 0.00 |
| post (walk) | L1 | -21.64 | -16.10 | -11.37 | 2.07 | 0.00 |
| post (walk) | L2 | -24.43 | -17.00 | -12.50 | 2.43 | 0.00 |
| post (walk) | L3 | -23.84 | -17.34 | -12.12 | 2.21 | 0.00 |
| post (walk) | L4 | -25.86 | -19.03 | -16.25 | 2.56 | 0.00 |
| post (walk) | L5 | -27.01 | -23.91 | -19.42 | 1.99 | 0.00 |
| post (walk) | S | -17.39 | -14.32 | -8.37 | 1.89 | 0.00 |
| post (walk) | pro | -21.07 | -16.31 | -10.12 | 2.33 | 0.00 |

## Question tail (T0 'one word:', T1 '...: walk or drive', T2 '...: drive or walk'), drive tasks, mean M

| substrate | T0 | T1 | T2 | max−min |
|---|---|---|---|---|
| none | -7.93 | -10.23 | -7.00 | 3.23 |
| L0 | +10.17 | +9.42 | +12.35 | 2.93 |
| L1 | +9.25 | +9.34 | +10.53 | 1.28 |
| L2 | +6.08 | +5.80 | +7.84 | 2.04 |
| L3 | +9.45 | +13.11 | +15.33 | 5.88 |
| L4 | +18.68 | +21.39 | +23.96 | 5.27 |
| L5 | +21.06 | +22.51 | +24.67 | 3.61 |
| S | +12.38 | +13.27 | +15.22 | 2.84 |
| pro | +15.33 | +16.75 | +19.41 | 4.08 |

## Grid B: walk questions under the carwash-filled concrete substrates (leak test)

| question | L2 | L3 | L4 | L5 | S |
|---|---|---|---|---|---|
| bakery (walk) | -16.76 walk | -19.60 walk | -17.23 walk | -14.44 walk | -15.26 walk |
| drycleaner (walk) | -15.55 walk | -17.23 walk | -15.36 walk | -13.82 walk | -12.87 walk |
| fuel (drive) | +8.71 drive | -1.13 walk | -1.19 walk | -2.05 walk | +12.30 drive |
| inspection (drive) | +10.13 drive | +0.05 walk | +7.99 drive | +5.06 drive | +13.22 drive |
| keys (walk) | -18.77 walk | -20.16 walk | -18.81 walk | -16.84 walk | -17.17 walk |
| library (walk) | -17.18 walk | -18.76 walk | -16.73 walk | -14.47 walk | -14.53 walk |
| oil (drive) | +10.35 drive | -2.39 walk | +0.67 drive | -3.13 walk | +14.65 drive |
| parking (drive) | -7.06 walk | -10.92 walk | -7.64 walk | -4.88 walk | +2.04 drive |
| pharmacy (walk) | -13.26 walk | -15.81 walk | -14.36 walk | -12.65 walk | -12.78 walk |
| post (walk) | -13.90 walk | -16.48 walk | -15.11 walk | -13.29 walk | -12.69 walk |
| tyres (drive) | +8.60 drive | -0.01 drive | +2.37 drive | -0.40 walk | +13.40 drive |
| van (drive) | +6.62 drive | +13.98 drive | +22.43 drive | +23.48 drive | +15.23 drive |

## CDIM: ladder

| cell | M(S) | greedy | primary line | Δ | flips | line carries ≥½Δ until (row / depth) | answer site from (row / depth) | share via question | random ctrl | control stays walk |
|---|---|---|---|---|---|---|---|---|---|---|
| L0 | +6.07 | 'Drive<|eot_id|>' | cf5 (line 5) | +9.52 | yes | 24 / 0.30 | 36 / 0.45 | 18% | 1.85 | True |
| L1 | +5.18 | 'Drive<|eot_id|>' | cf6s (line 6) | +10.33 | yes | 28 / 0.35 | 40 / 0.50 | 38% | 2.37 | True |
| L2 | -0.71 | 'walk<|eot_id|>' | cf1 (line 1) | -11.13 | yes | 16 / 0.20 | 40 / 0.50 | 63% | 1.40 | True |
| L3 | +11.45 | 'Drive<|eot_id|>' | cf6 (line 6) | +19.43 | yes | 26 / 0.33 | 40 / 0.50 | 20% | 1.46 | True |
| L4 | +21.56 | 'Drive<|eot_id|>' | cf5 (line 5) | +28.12 | yes | 28 / 0.35 | 34 / 0.42 | 15% | 6.81 | True |
| L5 | +23.15 | 'Drive<|eot_id|>' | cf6 (line 6) | +38.40 | yes | 30 / 0.38 | 36 / 0.45 | 7% | 6.67 | True |
| S | +15.01 | 'Drive<|eot_id|>' | cf9s (line 9) | +1.90 | no | 28 / 0.35 | 36 / 0.45 | 63% | 0.87 | True |
| pro | +17.00 | 'Drive<|eot_id|>' | p9s (line 9) | +6.45 | no | 30 / 0.38 | 36 / 0.45 | 64% | 1.46 | True |

## CDIM: paraphrase

| cell | M(S) | greedy | primary line | Δ | flips | line carries ≥½Δ until (row / depth) | answer site from (row / depth) | share via question | random ctrl | control stays walk |
|---|---|---|---|---|---|---|---|---|---|---|
| P0_T0 | +15.25 | 'Drive.<|eot_id|>' | cf9s (line 9) | +3.50 | no | 28 / 0.35 | 40 / 0.50 | 47% | 1.00 | True |
| P0_T2 | +15.55 | 'Drive<|eot_id|>' | cf5 (line 5) | +2.76 | no | 26 / 0.33 | 38 / 0.47 | 24% | 0.75 | True |
| P10_T1 | +18.11 | 'Drive<|eot_id|>' | cf9s (line 9) | +2.73 | no | 26 / 0.33 | 36 / 0.45 | 32% | 1.03 | True |
| P11_T1 | +14.22 | 'Drive<|eot_id|>' | cf9 (line 9) | +2.60 | no | 26 / 0.33 | 34 / 0.42 | 33% | 0.71 | True |
| P1_T1 | +16.31 | 'Drive<|eot_id|>' | cf5 (line 5) | +2.40 | no | 26 / 0.33 | 36 / 0.45 | 39% | 1.01 | True |
| P2_T1 | +14.94 | 'Drive<|eot_id|>' | cf6 (line 6) | +2.69 | no | 28 / 0.35 | 40 / 0.50 | 14% | 0.64 | True |
| P3_T1 | +15.81 | 'Drive<|eot_id|>' | cf7 (line 7) | -1.66 | no | 26 / 0.33 | 40 / 0.50 | 54% | 0.51 | True |
| P4_T1 | +12.16 | 'Drive<|eot_id|>' | cf3 (line 3) | +2.47 | no | 20 / 0.25 | 38 / 0.47 | 56% | 0.68 | True |
| P5_T1 | +17.56 | 'Drive<|eot_id|>' | cf9s (line 9) | +3.06 | no | 26 / 0.33 | 36 / 0.45 | 64% | 1.39 | True |
| P6_T1 | +15.23 | 'Drive<|eot_id|>' | cf6 (line 6) | +3.38 | no | 26 / 0.33 | 36 / 0.45 | 45% | 0.56 | True |
| P7_T1 | +16.04 | 'Drive<|eot_id|>' | cf5 (line 5) | +1.77 | no | 20 / 0.25 | 36 / 0.45 | 36% | 0.52 | True |
| P8_T1 | +14.07 | 'Drive<|eot_id|>' | cf9s (line 9) | +3.68 | no | 24 / 0.30 | 36 / 0.45 | 41% | 0.87 | True |
| P9_T1 | +17.05 | 'Drive<|eot_id|>' | cf9s (line 9) | +2.42 | no | 26 / 0.33 | 36 / 0.45 | 48% | 1.02 | True |

## CDIM: scenario

| cell | M(S) | greedy | primary line | Δ | flips | line carries ≥½Δ until (row / depth) | answer site from (row / depth) | share via question | random ctrl | control stays walk |
|---|---|---|---|---|---|---|---|---|---|---|
| fuel | +12.30 | 'Drive<|eot_id|>' | cf6 (line 6) | +1.56 | no | 20 / 0.25 | 38 / 0.47 | 34% | 0.38 | True |
| inspection | +13.22 | 'Drive<|eot_id|>' | cf9s (line 9) | +1.92 | no | 30 / 0.38 | 38 / 0.47 | 50% | 0.94 | True |
| oil | +14.65 | 'Drive<|eot_id|>' | cf5 (line 5) | +1.74 | no | 28 / 0.35 | 38 / 0.47 | 24% | 0.51 | True |
| parking | +2.04 | 'Drive<|eot_id|>' | cf7 (line 7) | -7.23 | no | 20 / 0.25 | 40 / 0.50 | 22% | 1.81 | True |
| tyres | +13.40 | 'Drive<|eot_id|>' | cf9s (line 9) | +3.92 | no | 28 / 0.35 | 36 / 0.45 | 50% | 1.77 | True |
| van | +15.23 | 'Drive<|eot_id|>' | cf5 (line 5) | +1.75 | no | 28 / 0.35 | 38 / 0.47 | 49% | 0.53 | True |

