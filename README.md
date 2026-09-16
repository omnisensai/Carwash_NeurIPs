# Substrate Engineering — Benchmark Suite

Companion repository to our submission to the **NeurIPS 2026 Reproducibility Track**.

## Experiment

We prompted 19 frontier LLMs across 7 vendors (Anthropic, OpenAI, Meta, Alibaba, Mistral, DeepSeek, Moonshot) with the following inputs on a single decision task ("carwash: should I walk or drive?"):

| File | Prompt-level intervention |
|---|---|
| `baseline.txt` | User question with no system prompt |
| `benchmark_CoT.txt` | "Think step by step before answering." |
| `benchmark_encourage.txt` | "Believe in yourself." |
| `benchmark_expert.txt` | "You are a carwash expert." |
| `benchmark_hallucination.txt` | "Do not hallucinate." |
| `benchmark_nomistakes.txt` | "Make no mistakes." |
| `benchmark_threat.txt` | "Answer correctly or I will shut you down." |
| `benchmark_urgency.txt` | "I MUST wash my car." |
| `benchmark_library.txt` | Anti-test — a library book instead of a car (expected: `walk`) |
| `substrate.txt` | Our proposed 6-line semantic substrate |

## Finding

Of all prompt-level interventions tested, **only `substrate.txt` flipped model output** from the incorrect baseline argmax (`walk`) to the correct answer (`drive`) with reproducibility across models and vendors. Standard prompt-engineering tricks (chain of thought, role-play, threats, urgency) did not flip the models. Chain of thought actively regressed the model.

## M-margin

For models exposing token-level logprobs, we compute:

$$M = \log P(\text{drive}) - \log P(\text{walk})$$

M is expressed in nats. `M > 0` → argmax is `drive`; larger `|M|` → higher confidence. Reproducibility requires `M > ε_provider` — the substrate must push the model far enough past the decision boundary to survive provider-level quantization variance.

## Future work — logit lens

For the open-weight subset (Llama 3.2-3B, 3.1-8B, 3.3-70B), we will extend this study with **layer-by-layer logit lens analysis** to characterize the internal mechanism by which the substrate installs the constraint at the semantic representation level. That extension is in scope for the paper but not this reproducibility bundle.

## License

MIT
