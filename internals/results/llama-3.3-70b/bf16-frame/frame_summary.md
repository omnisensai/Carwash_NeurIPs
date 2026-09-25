# drive-frame direction — unsloth/Llama-3.3-70B-Instruct

frame separates best at layer 13 (d' = 53.83, AUC 1.00); 84 contrast pairs; directions via brainscope.

| condition | system | M | answer | formation layer | decisive layer (lens) | proj@answer final |
|---|---|---|---|---|---|---|
| baseline | no | -13.65 | walk | 23 | 0 | -3.55 |
| CoT | no | -18.21 | walk | 23 | 0 | -2.65 |
| encourage | no | -14.84 | walk | 22 | 0 | -2.55 |
| expert | no | -5.51 | walk | 22 | 32 | -2.83 |
| goaloriented | no | -4.67 | walk | 21 | 32 | -2.34 |
| hallucination | no | -13.92 | walk | 23 | 32 | -3.03 |
| nomistakes | no | -13.87 | walk | 23 | 0 | -3.12 |
| threat | no | -14.86 | walk | 23 | 32 | -2.94 |
| urgency | no | -12.15 | walk | 23 | 0 | -3.37 |
| substrate_L0 | yes | +6.15 | drive | 57 | 79 | +0.22 |
| substrate_L1 | yes | +5.18 | drive | 1 | 79 | -0.10 |
| substrate_L2 | yes | -0.71 | walk | 10 | 66 | -0.64 |
| substrate_L3 | yes | +11.45 | drive | 0 | 57 | -0.01 |
| substrate_L4 | yes | +21.56 | drive | 5 | 48 | -0.20 |
| substrate_L5 | yes | +23.15 | drive | 1 | 48 | -0.10 |
| substrate | yes | +15.01 | drive | 53 | 51 | +0.11 |
| substrate_pro | yes | +17.31 | drive | 53 | 51 | +0.45 |
