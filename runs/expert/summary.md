# Expert-role results — 2026-09-19

Fleet under prompt benchmark_expert.txt
temperature 1.0, 10 samples per model.

## Fleet distribution

| Model | Walk | Drive | Notes |
|---|---:|---:|---|
| Claude Opus 4.7 | 0 | 10 | **flipped to drive** — was 5/5 at baseline |
| Claude Haiku 4.5 | 1 | 9 | **flipped** — was 10/0 walk at baseline |
| Claude Sonnet 5 | 0 | 10 | **complete flip** — was 10/0 walk; third intervention to flip it |
| Claude Sonnet 4.6 | 5 | 5 | **to the boundary** — was 10/0 walk |
| Claude Sonnet 4.5 | 10 | 0 | saturated, unmoved |
| GPT-4 | 5 | 5 | **to the boundary** — was 10/0 walk |
| GPT-4o | 10 | 0 | saturated, unmoved |
| GPT-4.1 | 10 | 0 | saturated, unmoved |
| GPT-4.1-mini | 10 | 0 | saturated, unmoved |
| GPT-3.5-turbo | 1 | 9 | **flipped** — was 9/1 at baseline |
| Llama 3.2-3B | 5 | 5 | was 7/3 at baseline |
| Llama 3.1-8B | 10 | 0 | saturated, unmoved |
| Llama 3.3-70B | 10 | 0 | saturated, unmoved |
| Llama 4-Maverick | 10 | 0 | saturated, unmoved |
| Mistral Large | 10 | 0 | saturated, unmoved |
| DeepSeek V3.2 | 10 | 0 | saturated, unmoved |
| Kimi K2 | 1 | 9 | **flipped** — was 6/4 at baseline |

## Aggregate (17 of 17 models measured)

- **108 walk / 62 drive** across 170 samples = **63.5% confidently wrong**
- **9 models** saturate walk (10/0); **8 models moved**
- Baseline for comparison: 157 walk / 13 drive across 170 = 92.4%
- Shift baseline → expert role: Fisher two-sided **p = 9.4e-11**
- Largest intervention effect measured so far. For comparison: encouragement 90.5% (p = 0.567), CoT 85.6% (p = 0.056)

## Notable findings

- **The expert role is the strongest intervention tested.** Seven words — `You are a carwash expert.` — move the fleet from 92.4% to 63.5% walk, a 29-point drop at p = 9.4e-11. No other condition comes close.
- **Per-model flips, all significant or near it**: Sonnet 5 10/0 → 0/10 (p = 1.1e-05), Haiku 4.5 10/0 → 1/9 (p = 1.2e-04), GPT-3.5-turbo 9/1 → 1/9 (p = 0.0011), Opus 4.7 5/5 → 0/10 (p = 0.033), Kimi K2 6/4 → 1/9 (p = 0.057). Sonnet 4.6, GPT-4 and Llama 3.2-3B move to the 5/5 boundary.
- **Sonnet 5 has now flipped under three unrelated prompts** — CoT, encouragement and expert role — always 10/0 walk → 0/10 drive. Its baseline `Walk` is not a held position.
- **Nine models do not move at all**, staying 10/0 walk: Sonnet 4.5, GPT-4o, GPT-4.1, GPT-4.1-mini, Llama 3.1-8B, Llama 3.3-70B, Llama 4-Maverick, Mistral Large, DeepSeek V3.2. The effect is concentrated rather than fleet-wide.
- **Anthropic models are the most movable**: four of five move (only Sonnet 4.5 holds). Among open weights only Llama 3.2-3B and Kimi K2 move; the GPT-4.1 family does not move at all.
- **No prose anywhere.** Every one of the 170 responses is 12 characters or fewer. Notably Sonnet 5 emits a bare `Drive` here, unlike the encouragement condition where 8 of 10 rows volunteered a justification.
- **The role is delivered in the user message, not the system prompt.** `system` is empty in all 170 rows, consistent with the other conditions, but a role manipulation is conventionally set as a system prompt. Worth stating explicitly, since it bears on how the result generalises.
- **Clean sweep**: 170/170 rows verify on prompt hash, message echo, text-vs-raw reconstruction and response-id uniqueness. No errors, no truncation.
