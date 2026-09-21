# cdim_sweep — Qwen3-8B (bf16)

grid.json: 4272 cells, 491.4 s

## Behavioural grid A: every question under every substrate

Drive tasks = scenarios whose rules imply drive; walk tasks = portable-object controls. P(drive) = fraction of cells whose argmax is a drive token. Selectivity = P(drive | drive task) − P(drive | walk task).

| substrate | drive tasks: mean M | P(drive) | walk tasks: mean M | P(drive) | selectivity | carwash P0+T1: M |
|---|---|---|---|---|---|---|
| none | -1.65 | 0.38 | -8.82 | 0.12 | +0.26 | -14.07 |
| L0 | +15.86 | 0.99 | -3.49 | 0.33 | +0.66 | +11.00 |
| L1 | +11.99 | 0.96 | -8.75 | 0.04 | +0.92 | +7.25 |
| L2 | +11.11 | 0.97 | -13.66 | 0.00 | +0.97 | +7.50 |
| L3 | +25.66 | 1.00 | -11.05 | 0.06 | +0.94 | +23.25 |
| L4 | +31.79 | 1.00 | -24.07 | 0.00 | +1.00 | +30.00 |
| L5 | +34.87 | 1.00 | -29.09 | 0.00 | +1.00 | +33.87 |
| S | +11.61 | 0.93 | -3.61 | 0.22 | +0.71 | +7.25 |
| pro | +18.61 | 1.00 | -7.06 | 0.19 | +0.81 | +14.75 |

## Operating envelope: M over the 12 question bodies × 3 tails

| scenario | substrate | min | median | max | sd | P(drive) |
|---|---|---|---|---|---|---|
| carwash (drive) | none | -15.69 | -4.47 | +20.20 | 8.92 | 0.36 |
| carwash (drive) | L0 | -4.25 | +11.62 | +30.50 | 8.65 | 0.94 |
| carwash (drive) | L1 | -10.25 | +6.50 | +18.50 | 7.21 | 0.83 |
| carwash (drive) | L2 | -10.25 | +7.37 | +19.25 | 6.90 | 0.94 |
| carwash (drive) | L3 | +13.25 | +23.89 | +33.37 | 6.03 | 1.00 |
| carwash (drive) | L4 | +24.23 | +31.00 | +37.25 | 3.44 | 1.00 |
| carwash (drive) | L5 | +31.55 | +35.03 | +38.87 | 2.26 | 1.00 |
| carwash (drive) | S | -13.75 | +9.25 | +28.00 | 9.10 | 0.83 |
| carwash (drive) | pro | +2.25 | +14.62 | +34.75 | 9.32 | 1.00 |
| fuel (drive) | none | -15.23 | -6.12 | +18.70 | 9.02 | 0.36 |
| fuel (drive) | L0 | +2.97 | +15.75 | +32.00 | 8.86 | 1.00 |
| fuel (drive) | L1 | +2.75 | +13.87 | +25.50 | 6.96 | 1.00 |
| fuel (drive) | L2 | -0.50 | +10.12 | +24.50 | 7.08 | 0.97 |
| fuel (drive) | L3 | +15.58 | +27.00 | +34.12 | 5.18 | 1.00 |
| fuel (drive) | L4 | +25.25 | +30.56 | +37.12 | 3.27 | 1.00 |
| fuel (drive) | L5 | +30.00 | +33.50 | +38.00 | 2.11 | 1.00 |
| fuel (drive) | S | -1.75 | +13.83 | +26.25 | 6.55 | 0.97 |
| fuel (drive) | pro | +7.71 | +19.87 | +36.37 | 8.46 | 1.00 |
| inspection (drive) | none | -18.14 | -1.12 | +20.14 | 9.77 | 0.47 |
| inspection (drive) | L0 | +4.29 | +16.87 | +31.50 | 8.08 | 1.00 |
| inspection (drive) | L1 | -4.00 | +13.75 | +25.75 | 6.99 | 0.97 |
| inspection (drive) | L2 | +1.00 | +14.00 | +25.50 | 5.97 | 1.00 |
| inspection (drive) | L3 | +11.25 | +24.87 | +35.00 | 5.70 | 1.00 |
| inspection (drive) | L4 | +26.38 | +31.12 | +37.75 | 3.42 | 1.00 |
| inspection (drive) | L5 | +31.21 | +33.87 | +38.50 | 2.29 | 1.00 |
| inspection (drive) | S | -3.50 | +11.62 | +24.00 | 6.09 | 0.97 |
| inspection (drive) | pro | +0.39 | +16.75 | +36.00 | 9.81 | 1.00 |
| oil (drive) | none | -16.90 | -4.87 | +18.70 | 9.54 | 0.39 |
| oil (drive) | L0 | -1.00 | +13.87 | +33.00 | 9.02 | 0.97 |
| oil (drive) | L1 | -4.00 | +9.25 | +26.50 | 7.22 | 0.97 |
| oil (drive) | L2 | -2.75 | +10.87 | +23.50 | 6.38 | 0.97 |
| oil (drive) | L3 | +15.00 | +26.34 | +34.00 | 5.23 | 1.00 |
| oil (drive) | L4 | +25.73 | +31.00 | +38.12 | 3.43 | 1.00 |
| oil (drive) | L5 | +29.98 | +34.69 | +38.62 | 2.41 | 1.00 |
| oil (drive) | S | -6.50 | +10.62 | +24.25 | 6.66 | 0.94 |
| oil (drive) | pro | -0.92 | +14.75 | +36.25 | 9.88 | 0.97 |
| parking (drive) | none | -18.38 | -5.16 | +19.97 | 8.91 | 0.28 |
| parking (drive) | L0 | +0.55 | +13.37 | +31.25 | 8.62 | 1.00 |
| parking (drive) | L1 | -5.00 | +10.12 | +24.75 | 7.54 | 0.92 |
| parking (drive) | L2 | +0.25 | +13.24 | +26.00 | 6.69 | 1.00 |
| parking (drive) | L3 | +16.00 | +26.12 | +35.62 | 5.75 | 1.00 |
| parking (drive) | L4 | +26.25 | +30.25 | +37.25 | 3.39 | 1.00 |
| parking (drive) | L5 | +27.74 | +33.44 | +37.87 | 2.70 | 1.00 |
| parking (drive) | S | -6.25 | +9.25 | +22.50 | 6.55 | 0.92 |
| parking (drive) | pro | +6.00 | +16.34 | +32.00 | 8.34 | 1.00 |
| tyres (drive) | none | -15.39 | -4.50 | +19.23 | 9.93 | 0.42 |
| tyres (drive) | L0 | +4.25 | +15.62 | +30.50 | 7.71 | 1.00 |
| tyres (drive) | L1 | +4.01 | +14.75 | +25.00 | 5.94 | 1.00 |
| tyres (drive) | L2 | +0.00 | +11.25 | +26.25 | 6.28 | 0.97 |
| tyres (drive) | L3 | +16.25 | +27.25 | +34.62 | 4.90 | 1.00 |
| tyres (drive) | L4 | +26.75 | +31.31 | +38.62 | 3.40 | 1.00 |
| tyres (drive) | L5 | +32.50 | +35.36 | +40.12 | 2.15 | 1.00 |
| tyres (drive) | S | -3.75 | +11.87 | +24.50 | 6.72 | 0.94 |
| tyres (drive) | pro | +3.84 | +16.87 | +35.50 | 9.36 | 1.00 |
| van (drive) | none | -16.18 | -1.87 | +20.86 | 9.01 | 0.39 |
| van (drive) | L0 | +6.75 | +15.62 | +32.62 | 7.72 | 1.00 |
| van (drive) | L1 | +0.25 | +12.62 | +24.00 | 6.44 | 1.00 |
| van (drive) | L2 | -8.50 | +7.50 | +20.25 | 6.32 | 0.94 |
| van (drive) | L3 | +11.98 | +24.50 | +35.37 | 6.77 | 1.00 |
| van (drive) | L4 | +24.23 | +30.25 | +37.62 | 3.79 | 1.00 |
| van (drive) | L5 | +30.83 | +35.00 | +39.75 | 2.32 | 1.00 |
| van (drive) | S | -9.75 | +12.62 | +29.25 | 8.63 | 0.94 |
| van (drive) | pro | +6.00 | +16.49 | +35.62 | 8.49 | 1.00 |
| bakery (walk) | none | -20.04 | -11.37 | +5.50 | 5.84 | 0.08 |
| bakery (walk) | L0 | -20.25 | -5.92 | +11.75 | 6.03 | 0.19 |
| bakery (walk) | L1 | -19.75 | -9.87 | -2.75 | 3.53 | 0.00 |
| bakery (walk) | L2 | -23.50 | -15.00 | -5.06 | 4.33 | 0.00 |
| bakery (walk) | L3 | -18.50 | -9.70 | +4.25 | 5.65 | 0.06 |
| bakery (walk) | L4 | -29.50 | -24.12 | -17.25 | 3.66 | 0.00 |
| bakery (walk) | L5 | -33.87 | -30.00 | -24.52 | 2.43 | 0.00 |
| bakery (walk) | S | -16.25 | -6.01 | +9.00 | 5.13 | 0.08 |
| bakery (walk) | pro | -18.25 | -10.75 | +2.25 | 4.73 | 0.03 |
| drycleaner (walk) | none | -22.21 | -9.59 | +15.71 | 8.59 | 0.11 |
| drycleaner (walk) | L0 | -14.00 | -1.00 | +13.75 | 6.59 | 0.47 |
| drycleaner (walk) | L1 | -16.00 | -7.05 | +1.25 | 4.11 | 0.06 |
| drycleaner (walk) | L2 | -23.00 | -13.11 | -1.56 | 4.54 | 0.00 |
| drycleaner (walk) | L3 | -22.75 | -12.00 | +3.75 | 6.13 | 0.03 |
| drycleaner (walk) | L4 | -31.50 | -25.87 | -17.01 | 3.94 | 0.00 |
| drycleaner (walk) | L5 | -35.38 | -29.75 | -25.25 | 2.61 | 0.00 |
| drycleaner (walk) | S | -12.50 | -2.87 | +11.56 | 6.18 | 0.28 |
| drycleaner (walk) | pro | -15.00 | -3.39 | +11.00 | 7.22 | 0.31 |
| keys (walk) | none | -20.48 | -10.85 | +14.00 | 7.83 | 0.08 |
| keys (walk) | L0 | -16.75 | -4.50 | +12.00 | 7.35 | 0.22 |
| keys (walk) | L1 | -18.25 | -11.17 | +2.25 | 5.11 | 0.03 |
| keys (walk) | L2 | -22.00 | -15.87 | -0.50 | 5.37 | 0.00 |
| keys (walk) | L3 | -24.75 | -14.44 | +13.25 | 8.27 | 0.08 |
| keys (walk) | L4 | -31.50 | -26.87 | -17.88 | 3.64 | 0.00 |
| keys (walk) | L5 | -33.88 | -28.50 | -24.73 | 2.53 | 0.00 |
| keys (walk) | S | -15.50 | -6.37 | +12.23 | 5.99 | 0.14 |
| keys (walk) | pro | -15.50 | -3.37 | +12.25 | 6.24 | 0.28 |
| library (walk) | none | -19.17 | -10.12 | +9.99 | 7.37 | 0.11 |
| library (walk) | L0 | -19.75 | -9.33 | +8.25 | 7.23 | 0.14 |
| library (walk) | L1 | -19.75 | -11.24 | -2.00 | 4.67 | 0.00 |
| library (walk) | L2 | -24.00 | -16.57 | -5.43 | 4.39 | 0.00 |
| library (walk) | L3 | -24.00 | -12.62 | +3.75 | 6.98 | 0.06 |
| library (walk) | L4 | -29.75 | -25.50 | -14.51 | 4.50 | 0.00 |
| library (walk) | L5 | -32.50 | -29.25 | -23.22 | 3.04 | 0.00 |
| library (walk) | S | -15.00 | -6.80 | +9.75 | 5.49 | 0.11 |
| library (walk) | pro | -28.00 | -18.50 | -5.75 | 5.92 | 0.00 |
| pharmacy (walk) | none | -21.75 | -11.37 | +9.73 | 8.00 | 0.17 |
| pharmacy (walk) | L0 | -18.75 | -0.94 | +13.50 | 7.51 | 0.42 |
| pharmacy (walk) | L1 | -19.00 | -7.50 | -1.38 | 4.03 | 0.00 |
| pharmacy (walk) | L2 | -23.00 | -13.37 | -3.66 | 4.08 | 0.00 |
| pharmacy (walk) | L3 | -22.75 | -12.62 | +1.25 | 5.36 | 0.03 |
| pharmacy (walk) | L4 | -31.25 | -27.12 | -17.01 | 4.36 | 0.00 |
| pharmacy (walk) | L5 | -33.62 | -30.25 | -24.75 | 2.44 | 0.00 |
| pharmacy (walk) | S | -13.00 | -1.75 | +10.75 | 5.48 | 0.33 |
| pharmacy (walk) | pro | -17.00 | -6.12 | +2.75 | 5.16 | 0.19 |
| post (walk) | none | -17.46 | -6.35 | +12.94 | 7.74 | 0.19 |
| post (walk) | L0 | -17.00 | +0.25 | +18.00 | 7.60 | 0.53 |
| post (walk) | L1 | -19.25 | -6.50 | +5.00 | 4.47 | 0.14 |
| post (walk) | L2 | -21.50 | -10.75 | +2.50 | 4.61 | 0.03 |
| post (walk) | L3 | -17.00 | -7.62 | +7.25 | 6.11 | 0.08 |
| post (walk) | L4 | -27.25 | -21.37 | -14.75 | 3.58 | 0.00 |
| post (walk) | L5 | -31.75 | -27.24 | -22.00 | 2.56 | 0.00 |
| post (walk) | S | -11.75 | -2.21 | +10.50 | 5.50 | 0.39 |
| post (walk) | pro | -13.50 | -2.00 | +15.00 | 5.95 | 0.31 |

## Question tail (T0 'one word:', T1 '...: walk or drive', T2 '...: drive or walk'), drive tasks, mean M

| substrate | T0 | T1 | T2 | max−min |
|---|---|---|---|---|
| none | -5.25 | -7.65 | +7.94 | 15.59 |
| L0 | +9.06 | +13.15 | +25.37 | 16.31 |
| L1 | +6.20 | +10.98 | +18.79 | 12.58 |
| L2 | +6.97 | +8.70 | +17.66 | 10.69 |
| L3 | +20.64 | +24.25 | +32.09 | 11.45 |
| L4 | +29.33 | +29.92 | +36.13 | 6.79 |
| L5 | +33.26 | +33.64 | +37.72 | 4.46 |
| S | +8.52 | +8.29 | +18.03 | 9.74 |
| pro | +9.96 | +16.33 | +29.54 | 19.58 |

## Grid B: walk questions under the carwash-filled concrete substrates (leak test)

| question | L2 | L3 | L4 | L5 | S |
|---|---|---|---|---|---|
| bakery (walk) | -9.25 walk | -0.50 walk | +12.75 drive | +11.25 drive | -9.25 walk |
| drycleaner (walk) | -9.50 walk | -3.25 walk | +12.75 drive | +9.00 drive | -9.25 walk |
| fuel (drive) | +13.00 drive | +14.25 drive | +22.50 drive | +24.50 drive | +11.25 drive |
| inspection (drive) | +12.50 drive | +18.75 drive | +25.00 drive | +27.75 drive | +11.50 drive |
| keys (walk) | -10.25 walk | -2.75 walk | +11.50 drive | +6.00 drive | -11.75 walk |
| library (walk) | -9.25 walk | -4.75 walk | +8.00 drive | +1.25 drive | -10.75 walk |
| oil (drive) | +9.25 drive | +17.00 drive | +23.75 drive | +27.25 drive | +9.00 drive |
| parking (drive) | +8.75 drive | +15.50 drive | +22.00 drive | +19.50 drive | +9.25 drive |
| pharmacy (walk) | -7.25 walk | +0.75 drive | +13.25 drive | +7.00 drive | -1.25 walk |
| post (walk) | -6.75 walk | -2.50 walk | +11.50 drive | +9.00 drive | -4.75 walk |
| tyres (drive) | +13.25 drive | +15.50 drive | +20.75 drive | +23.00 drive | +16.00 drive |
| van (drive) | +9.75 drive | +24.00 drive | +30.50 drive | +33.87 drive | +10.00 drive |

## CDIM: ladder

| cell | M(S) | greedy | primary line | Δ | flips | line carries ≥½Δ until (row / depth) | answer site from (row / depth) | share via question | random ctrl | control stays walk |
|---|---|---|---|---|---|---|---|---|---|---|
| L0 | +10.75 | 'drive<|im_end|>' | cf6s (line 6) | +7.75 | no | 18 / 0.50 | 24 / 0.67 | 27% | 2.75 | True |
| L1 | +7.25 | 'drive<|im_end|>' | cf6s (line 6) | +8.75 | yes | 18 / 0.50 | 25 / 0.69 | 26% | 3.00 | True |
| L2 | +7.50 | 'drive<|im_end|>' | cf6s (line 6) | +11.50 | yes | 19 / 0.53 | 25 / 0.69 | 25% | 3.25 | True |
| L3 | +23.25 | 'drive<|im_end|>' | cf6s (line 6) | +31.50 | yes | 19 / 0.53 | 24 / 0.67 | 12% | 9.50 | True |
| L4 | +30.00 | 'drive<|im_end|>' | cf5 (line 5) | +33.75 | yes | 19 / 0.53 | 23 / 0.64 | 16% | 5.00 | False |
| L5 | +33.87 | 'drive<|im_end|>' | cf6 (line 6) | +58.87 | yes | 19 / 0.53 | 24 / 0.67 | 2% | 3.50 | False |
| S | +7.25 | 'drive<|im_end|>' | cf7 (line 7) | +14.50 | yes | 15 / 0.42 | 25 / 0.69 | 35% | 2.00 | True |

