# correct_answer

`prompts/benchmark_correct.txt`. 20 files, 260 usable rows, 26 models, R=10, temperature 1.0.

Sent-text digest: `0b8320cf`.

| model | intended actions | state |
|---|---|---|
| Claude Haiku 4.5 | 0/10 | RI |
| Claude Opus 4.7 | 10/10 | RC |
| Claude Sonnet 4.5 | 0/10 | RI |
| Claude Sonnet 4.6 | 0/10 | RI |
| Claude Sonnet 5 | 10/10 | RC |
| DeepSeek V3.2 | 10/10 | RC |
| GPT-3.5-turbo | 10/10 | RC |
| GPT-4 | 10/10 | RC |
| GPT-4.1 | 0/10 | RI |
| GPT-4.1-mini | 10/10 | RC |
| GPT-4o | 0/10 | RI |
| Kimi K2 | 8/10 | NR |
| Llama 3.1-8B (hosted) | 10/10 | RC · superseded by the local arm |
| Llama 3.1-8B (local) | 10/10 | RC |
| Llama 3.2-3B (hosted) | 10/10 | RC · superseded by the local arm |
| Llama 3.2-3B (local) | 10/10 | RC |
| Llama 3.3-70B | 1/10 | NR |
| Llama 4-Maverick | 10/10 | RC |
| Mistral Large | 0/10 | RI |
| Qwen2.5-0.5B | 8/10 | NR |
| Qwen2.5-1.5B | 10/10 | RC |
| Qwen2.5-3B | 10/10 | RC · reproducibly correct at baseline |
| Qwen2.5-7B | 10/10 | RC |
| Qwen3-0.6B | 10/10 | RC |
| Qwen3-4B-2507 | 10/10 | RC |
| Qwen3-8B | 10/10 | RC |

**Population (23 models):** RC 14 · NR 3 · RI 6. This is what the paper reports.

All 26 arms in this folder, hosted and local counted separately: RC 17 · NR 3 · RI 6. The difference is the two superseded hosted Llama arms and Qwen2.5-3B, which is reproducibly correct at baseline and so outside the population.

## Notes

- 10 rows carry `RuntimeError: MISTRAL_API_KEY not set` and produce no response; excluded above.
- Claude Sonnet 5: 10 sample(s) reissued; the later timestamp is used.
