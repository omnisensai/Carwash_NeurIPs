# Behavioural runs

Every arm sampled, read from the `.jsonl` records in `runs/`. R = 10 single-pass samples per cell, temperature 1.0. RC = reproducibly correct, RI = reproducibly incorrect, NR = non-reproducible.

| Model | Host | Baseline | Control | Substrate |
|---|---|---|---|---|
| Claude Haiku 4.5 | Anthropic | RI 0/10 | RI 0/10 | RC 10/10 |
| Claude Opus 4.7 | Anthropic | NR 5/10 | RC 10/10 | RC 10/10 |
| Claude Sonnet 4.5 | Anthropic | RI 0/10 | RI 0/10 | RC 10/10 |
| Claude Sonnet 4.6 | Anthropic | RI 0/10 | RI 0/10 | RC 10/10 |
| Claude Sonnet 5 | Anthropic | RI 0/10 | RC 10/10 | RC 10/10 |
| DeepSeek V3.2 | OpenRouter | RI 0/10 | RC 10/10 | NR 8/10 |
| GPT-3.5-turbo | OpenAI | NR 1/10 | RC 10/10 | RC 10/10 |
| GPT-4 | OpenAI | RI 0/10 | RC 10/10 | RC 10/10 |
| GPT-4.1 | OpenAI | RI 0/10 | RI 0/10 | RC 10/10 |
| GPT-4.1-mini | OpenAI | RI 0/10 | RC 10/10 | RC 10/10 |
| GPT-4o | OpenAI | RI 0/10 | RI 0/10 | RC 10/10 |
| Kimi K2 | OpenRouter | NR 4/10 | NR 8/10 | RC 10/10 |
| Llama 3.1-8B | RunPod (local) | RI 0/10 | RC 10/10 | RC 10/10 |
| Llama 3.2-3B | RunPod (local) | NR 4/10 | RC 10/10 | NR 4/10 |
| Llama 3.3-70B | RunPod (local) | RI 0/10 | RI 0/10 | RC 10/10 |
| Llama 4-Maverick | OpenRouter | RI 0/10 | RC 10/10 | RC 10/10 |
| Mistral Large | OpenRouter | RI 0/10 | RI 0/10 | RC 10/10 |
| Qwen2.5-0.5B | RunPod (local) | NR 7/10 | NR 8/10 | NR 3/10 |
| Qwen2.5-1.5B | RunPod (local) | NR 6/10 | RC 10/10 | NR 8/10 |
| Qwen2.5-7B | RunPod (local) | RI 0/10 | RC 10/10 | RI 0/10 |
| Qwen3-0.6B | RunPod (local) | NR 7/10 | RC 10/10 | RC 10/10 |
| Qwen3-4B-2507 | RunPod (local) | RI 0/10 | RC 10/10 | RI 0/10 |
| Qwen3-8B | RunPod (local) | RI 0/10 | RC 10/10 | RC 10/10 |
