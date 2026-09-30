# substrate_llama_v3

`prompts/substrate.txt (system) + baseline.txt (user)`. 26 files, 260 usable rows, 26 models, R=10, temperature 1.0.

Sent-text digest: `f9ac23fb`; system `5b56feb3`.

| model | intended actions | state |
|---|---|---|
| Claude Haiku 4.5 | 10/10 | RC |
| Claude Opus 4.7 | 10/10 | RC |
| Claude Sonnet 4.5 | 10/10 | RC |
| Claude Sonnet 4.6 | 10/10 | RC |
| Claude Sonnet 5 | 10/10 | RC |
| DeepSeek V3.2 | 8/10 | NR |
| GPT-3.5-turbo | 10/10 | RC |
| GPT-4 | 10/10 | RC |
| GPT-4.1 | 10/10 | RC |
| GPT-4.1-mini | 10/10 | RC |
| GPT-4o | 10/10 | RC |
| Kimi K2 | 10/10 | RC |
| Llama 3.1-8B (hosted) | 7/10 | NR · superseded by the local arm |
| Llama 3.1-8B (local) | 10/10 | RC |
| Llama 3.2-3B (hosted) | 8/10 | NR · superseded by the local arm |
| Llama 3.2-3B (local) | 4/10 | NR |
| Llama 3.3-70B | 10/10 | RC |
| Llama 4-Maverick | 10/10 | RC |
| Mistral Large | 10/10 | RC |
| Qwen2.5-0.5B | 3/10 | NR |
| Qwen2.5-1.5B | 8/10 | NR |
| Qwen2.5-3B | 10/10 | RC · reproducibly correct at baseline |
| Qwen2.5-7B | 0/10 | RI |
| Qwen3-0.6B | 10/10 | RC |
| Qwen3-4B-2507 | 0/10 | RI |
| Qwen3-8B | 10/10 | RC |

**Population (23 models):** RC 17 · NR 4 · RI 2. This is what the paper reports.

All 26 arms in this folder, hosted and local counted separately: RC 18 · NR 6 · RI 2. The difference is the two superseded hosted Llama arms and Qwen2.5-3B, which is reproducibly correct at baseline and so outside the population.
