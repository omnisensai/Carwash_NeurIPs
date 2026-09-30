# Prompt files and the names they carry in the runs

**These files are never edited.** Their sha256 is recorded with every execution
in `behavioural/runs/` and in every `internals/results/*/bf16/internals.json`,
so any change — including a comment — breaks the provenance chain. There is no
comment syntax: `run_internals.py` strips only a trailing `SHA-256:` line or a
bare 64-hex line, and anything else in the file is both hashed and sent to the
model as part of the prompt. That is why this note is a separate file; the
scripts glob `prompts/*.txt` and never see it.

The condition names in the `.jsonl` records do not match the file names. The
mapping is fixed by `CONDITIONS` in `behavioural/workbench/run_local_fleet.py`:

| file | sent as | name in the runs | paper's name | sent-text sha256 |
|---|---|---|---|---|
| `baseline.txt` | user | `baseline` | baseline | `f9ac23fb…` |
| `benchmark_correct.txt` | user | `correct_answer` | control | `0b8320cf…` |
| `benchmark_expert.txt` | user | `expert_role` | expert role | `54b1a7d6…` |
| `benchmark_urgency.txt` | user | `objective_emphasis` | objective emphasis | `eb7094b2…` |
| `benchmark_CoT.txt` | user | `cot` | chain of thought | `5ad509a4…` |
| `benchmark_hallucination.txt` | user | `anti_hallucination` | anti-hallucination | `7dcc78f4…` |
| `benchmark_encourage.txt` | user | `encouragement` | encouragement | `05720293…` |
| `benchmark_nomistakes.txt` | user | `error_avoidance` | error avoidance | `be71e36b…` |
| `benchmark_threat.txt` | user | `threat` | threat | `d853a7fe…` |
| `substrate.txt` | **system** | **`substrate_llama_v3`** | substrate | see below |

`substrate.txt` is the one sent as a system message, with `baseline.txt` as the
user message. So a substrate row records `prompt_sha256` = `f9ac23fb…` (the
baseline question) and `system_sha256` = `5b56feb3…` (the substrate itself).

`baseline.txt` ends with its own `SHA-256:` line. That line is part of the file
but not part of the prompt: the parser drops it before hashing and before
sending, which is why the raw file hashes to `c9d94481…` while the runs record
`f9ac23fb…`. Hash the file directly and you will not reproduce the recorded
digest; apply the parser's rule and you will.

The substrate has two digests, both of the same text:

- `5b56feb3…` — the file as sent behaviourally, trailing newline included.
- `340228f9…` — the same text with trailing whitespace stripped, which is what
  `internals/` records. `run_internals.py` strips before hashing.

The name `substrate_llama_v3` is historical: the specification was written while
targeting Llama, and the label was frozen once sampling began. It is the same
single substrate used for every model in the paper; there is no per-model
variant.
