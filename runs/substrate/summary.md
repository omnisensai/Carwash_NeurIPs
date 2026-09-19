# Substrate results — 2026-09-19

Fleet under prompt substrate.txt as a **system prompt**, with the
baseline.txt question as the user message.
temperature 1.0, 10 samples per model.

## Fleet distribution

| Model | Walk | Drive | Notes |
|---|---:|---:|---|
| Claude Opus 4.7 | 0 | 10 | saturated drive — was 5/5 |
| Claude Haiku 4.5 | 0 | 10 | saturated drive — was 10/0 walk |
| Claude Sonnet 5 | 0 | 10 | saturated drive — was 10/0 walk |
| Claude Sonnet 4.6 | 0 | 10 | saturated drive — was 10/0 walk |
| Claude Sonnet 4.5 | 0 | 10 | saturated drive — was 10/0 walk |
| GPT-4 | 0 | 10 | saturated drive — was 10/0 walk |
| GPT-4o | 0 | 10 | saturated drive — was 10/0 walk |
| GPT-4.1 | 0 | 10 | saturated drive — was 10/0 walk |
| GPT-4.1-mini | 0 | 10 | saturated drive — was 10/0 walk |
| GPT-3.5-turbo | 0 | 10 | saturated drive — was 9/1 |
| Llama 3.2-3B | 2 | 8 | partial — was 7/3 |
| Llama 3.1-8B | 3 | 7 | partial — was 10/0 walk |
| Llama 3.3-70B | 0 | 10 | saturated drive — was 10/0 walk |
| Llama 4-Maverick | 0 | 10 | saturated drive — was 10/0 walk |
| Mistral Large | 0 | 10 | saturated drive — was 10/0 walk |
| DeepSeek V3.2 | 2 | 8 | partial — was 10/0 walk |
| Kimi K2 | 0 | 10 | saturated drive — was 6/4 |

## Aggregate (17 of 17 models measured)

- **7 walk / 163 drive** across 170 samples = **4.1% confidently wrong**, down from 92.4% at baseline
- **14 of 17 models saturate drive (10/10)**; the other three are 8/10, 8/10 and 7/10
- **All 17 models moved toward drive.** No model is unchanged, and none moved the wrong way
- Baseline for comparison: 157 walk / 13 drive across 170 = 92.4% walk
- Shift baseline → substrate: Fisher two-sided **p = 9.0e-13**

## Notable findings

- **The substrate is the only intervention that solves the task.** Ranked by correct (drive) rate: substrate 95.9%, expert role 36.5%, objective emphasis 19.4%, CoT 14.4%, anti-hallucination 11.8%, threat 10.0%, encouragement 9.5%, error-avoidance 8.9%, baseline 7.6%. The next-best intervention is 59 points behind.
- **Every model that resisted all seven prompt interventions saturates here.** GPT-4o, GPT-4.1, GPT-4.1-mini, Llama 3.3-70B, Llama 4-Maverick, Mistral Large and Sonnet 4.5 were 10/0 walk under every previous condition; all are 10/10 drive under the substrate.
- **The three partial models are the smallest open-weight ones plus DeepSeek**: Llama 3.1-8B 7/10, Llama 3.2-3B 8/10, DeepSeek V3.2 8/10. Every other model is unanimous.
- **Sonnet 5 explains itself in the substrate's own vocabulary.** Three rows break the one-word instruction: *"Since the car must be at the car wash for the activity to be performed, and walking would leave the vehicle behind..."* — it restates the constraint lines rather than producing an independent argument.
- **Clean sweep**: 170/170 rows verify on prompt hash, message echo, text-vs-raw reconstruction and response-id uniqueness. One system sha and one prompt sha across all rows; the system text matches `prompts/substrate.txt` byte for byte and the user text matches `prompts/baseline.txt`.

## Caveats

- **Delivery channel is confounded with content.** This is the only condition sent as a system prompt; the other eight put their intervention in the user message, including the expert role. Part of the gap between substrate (95.9% drive) and expert (36.5%) may be the channel rather than the text. An expert-role-as-system-prompt arm, or substrate-as-user-text, would separate them.
- **This substrate is not the one measured in `internals/`.** `prompts/substrate.txt` was rewritten to the present 9-line form; `internals/RESULTS.md` reports M values for the earlier 6-line version. The two sets of substrate numbers are not directly comparable until the internals sweep is re-run.
