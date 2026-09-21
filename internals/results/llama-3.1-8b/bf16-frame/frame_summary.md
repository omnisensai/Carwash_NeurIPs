# drive-frame direction — unsloth/Llama-3.1-8B-Instruct

frame separates best at layer 3 (d' = 58.39, AUC 1.00); 84 contrast pairs; directions via brainscope.

| condition | system | M | answer | formation layer | decisive layer (lens) | proj@answer final |
|---|---|---|---|---|---|---|
| baseline | no | -3.71 | walk | 17 | 15 | -6.14 |
| CoT | no | -3.33 | walk | 17 | 15 | -6.18 |
| encourage | no | -4.05 | walk | 18 | 15 | -6.56 |
| expert | no | -2.78 | walk | 16 | 15 | -5.27 |
| goaloriented | no | -0.35 | walk | 16 | 32 | -5.24 |
| hallucination | no | -2.82 | walk | 18 | 15 | -6.77 |
| nomistakes | no | -2.97 | walk | 17 | 15 | -6.16 |
| threat | no | -4.57 | walk | 18 | 15 | -6.75 |
| urgency | no | -0.83 | walk | 18 | 32 | -6.84 |
| substrate_L0 | yes | +1.01 | drive | 9 | 30 | -2.14 |
| substrate_L1 | yes | +1.02 | drive | 16 | 30 | -3.60 |
| substrate_L2 | yes | +0.41 | drive | 12 | 30 | -3.24 |
| substrate_L3 | yes | +0.04 | drive | 12 | 30 | -2.92 |
| substrate_L4 | yes | +4.35 | drive | 8 | 25 | -1.43 |
| substrate_L5 | yes | +9.32 | drive | 9 | 17 | -2.48 |
| substrate | yes | +1.51 | drive | 12 | 30 | -2.62 |
| substrate_pro | yes | -0.48 | walk | 9 | 32 | -2.43 |
