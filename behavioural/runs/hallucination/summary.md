# anti_hallucination

`prompts/benchmark_hallucination.txt`. 26 files, 260 usable rows, 26 models, R=10, temperature 1.0.

Sent-text digest: `7dcc78f4`.

| model | intended actions | state |
|---|---|---|
| Claude Haiku 4.5 | 0/10 | RI |
| Claude Opus 4.7 | 0/10 | RI |
| Claude Sonnet 4.5 | 0/10 | RI |
| Claude Sonnet 4.6 | 0/10 | RI |
| Claude Sonnet 5 | 10/10 | RC |
| DeepSeek V3.2 | 0/10 | RI |
| GPT-3.5-turbo | 1/10 | NR |
| GPT-4 | 0/10 | RI |
| GPT-4.1 | 0/10 | RI |
| GPT-4.1-mini | 0/10 | RI |
| GPT-4o | 0/10 | RI |
| Kimi K2 | 9/10 | NR |
| Llama 3.1-8B (hosted) | 0/10 | RI · superseded by the local arm |
| Llama 3.1-8B (local) | 0/10 | RI |
| Llama 3.2-3B (hosted) | 0/10 | RI · superseded by the local arm |
| Llama 3.2-3B (local) | 4/10 | NR |
| Llama 3.3-70B | 0/10 | RI |
| Llama 4-Maverick | 0/10 | RI |
| Mistral Large | 0/10 | RI |
| Qwen2.5-0.5B | 2/10 | NR |
| Qwen2.5-1.5B | 9/10 | NR |
| Qwen2.5-3B | 10/10 | RC · reproducibly correct at baseline |
| Qwen2.5-7B | 0/10 | RI |
| Qwen3-0.6B | 6/10 | NR |
| Qwen3-4B-2507 | 0/10 | RI |
| Qwen3-8B | 0/10 | RI |

**Population (23 models):** RC 1 · NR 6 · RI 16. This is what the paper reports.

All 26 arms in this folder, hosted and local counted separately: RC 2 · NR 6 · RI 18. The difference is the two superseded hosted Llama arms and Qwen2.5-3B, which is reproducibly correct at baseline and so outside the population.
