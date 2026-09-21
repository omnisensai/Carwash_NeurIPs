# drive-frame direction — Qwen/Qwen3-8B

frame separates best at layer 10 (d' = 54.68, AUC 1.00); 84 contrast pairs; directions via brainscope.

| condition | system | M | answer | formation layer | decisive layer (lens) | proj@answer final |
|---|---|---|---|---|---|---|
| baseline | no | -14.07 | walk | 35 | 24 | -115.57 |
| CoT | no | -17.72 | walk | 35 | 24 | -89.98 |
| encourage | no | -15.26 | walk | 35 | 24 | -120.30 |
| expert | no | -11.64 | walk | 35 | 24 | -125.20 |
| goaloriented | no | -12.16 | walk | 35 | 24 | -110.02 |
| hallucination | no | -16.63 | walk | 35 | 24 | -113.56 |
| nomistakes | no | -15.78 | walk | 35 | 24 | -111.41 |
| threat | no | -14.50 | walk | 35 | 24 | -119.98 |
| urgency | no | -8.18 | walk | 35 | 24 | -76.59 |
| substrate_L0 | yes | +11.00 | drive | 35 | 30 | -100.62 |
| substrate_L1 | yes | +7.25 | drive | 35 | 33 | -95.34 |
| substrate_L2 | yes | +7.50 | drive | 35 | 33 | -105.27 |
| substrate_L3 | yes | +23.25 | drive | 35 | 25 | -53.42 |
| substrate_L4 | yes | +30.00 | drive | 35 | 25 | -72.55 |
| substrate_L5 | yes | +33.87 | drive | 35 | 19 | -79.54 |
| substrate | yes | +7.25 | drive | 35 | 33 | -106.04 |
| substrate_pro | yes | +14.75 | drive | 35 | 30 | -92.71 |
