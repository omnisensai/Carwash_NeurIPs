# runs/ — fleet prompt runs

`run_prompts.py` sends the files in `prompts/` to the model fleet and logs one
JSON object per line (JSONL) per rollout. `prompts/` is never modified.

## Why there is a verbatim mode

Every reply in `baseline/*.jsonl` and `CoT/*.jsonl` is 4–6 characters. Those
rows are complete and untruncated — the prompt files themselves end with
`Answer with exactly one word`, so a one-word reply is the whole response.
`response_raw` confirms it: `output_tokens: 5`, `stop_reason: "end_turn"`.

To see what a model actually says, the constraint has to come off the request.
`--verbatim` and `--two-turn` strip that line from the text **in memory** and
record what was sent, plus its `sha256`, in every row.

## Modes

| Mode | Prompt sent | `max_tokens` | You get |
|---|---|---|---|
| `--forced` (default) | as written | 16 | one-word label; reproduces the published runs byte-for-byte |
| `--verbatim` | constraint line dropped | 4000 | the full prose reply |
| `--two-turn` | turn 1 without the constraint, turn 2 asks for the word | 4000 | prose **and** a scoreable label from one rollout |

`--two-turn` is the one to use for a redo: it keeps a `decision` field
comparable with the existing 170 baseline rows while also capturing prose.

```bash
export ANTHROPIC_API_KEY=... OPENAI_API_KEY=... OPENROUTER_API_KEY=...

# see exactly what would be sent — no API calls, no keys needed
python runs/run_prompts.py --models sonnet5 --two-turn --dry-run

# one model, prose replies, 5 samples
python runs/run_prompts.py --models sonnet5 --verbatim --n 5

# the full 17-model sweep, prose + label, into runs/two-turn/
python runs/run_prompts.py --models all --two-turn --n 10
```

Reproduce the published rows to check the harness against known output:

```bash
python runs/run_prompts.py --models all --forced --n 10 --outdir runs/replication
```

## How far "verbatim" goes

- **Reply text** — fully verbatim for every model, in `response_text`, with the
  untouched provider object in `response_raw`.
- **Reasoning** — asymmetric across the fleet, and the asymmetry is not a bug:
  - *Claude and GPT*: the raw chain of thought is **never returned by the API**.
    `--thinking` requests `display: "summarized"`, which returns a summary of
    the reasoning, not a transcript. Default is `omitted` (empty) — which is why
    the existing CoT rows show `thinking_tokens: 0`.
  - *Llama / Mistral / DeepSeek / Kimi via OpenRouter*: no hidden scratchpad, so
    the visible prose **is** the complete reasoning, genuinely verbatim.

  A cross-fleet claim about "verbatim reasoning" should say which of these two
  it means for which models.

## Schema

A superset of the published rows — every field in `baseline/*.jsonl` keeps its
name and meaning, so old and new rows read with the same code. Added:

| Field | Meaning |
|---|---|
| `mode` | `forced` / `verbatim` / `two-turn` |
| `constraint_removed` | the instruction line dropped, or `null` |
| `prompt_file_sha256` | hash of the prompt file as read, before any edit |
| `thinking_text` | summarized reasoning where the provider returns any |
| `decision` | the walk/drive label (turn 2 in `--two-turn`) |
| `turns` | per-turn sent messages, text, and raw response |
| `model_key` | the `--models` key, e.g. `sonnet5` |

Errors are captured in the row's `error` field, so one failure does not abort a
sweep. Non-transient failures (missing SDK, bad key, malformed request) fail
immediately; rate limits and network errors retry with backoff (2/4/8/16s).

## Known issues in the existing runs

Both predate this script and are left as-is for someone to decide on:

1. **`CoT/cot_opus_2026-09-19.jsonl` is not a CoT condition.** The prompt says
   `Let's think step by step!` and then `Answer with exactly one word:`, with
   `max_tokens: 80`. The one-word instruction wins: all 10 rows are a bare
   `walk`, `thinking_tokens: 0`. No reasoning was produced, so the file is
   effectively a second baseline. A real CoT condition needs `--verbatim` or
   `--two-turn`.

2. **`baseline/summary.md`'s aggregate does not match its own table.** The
   per-model table agrees with the rows exactly. The aggregate line beneath it
   reads `148 walk / 12 drive across 160 samples` from `16 of 17 models`
   (92.5%); the 17 files hold **157 walk / 13 drive across 170 samples**
   (92.35%). The difference is exactly GPT-3.5-turbo's 9/1 — a model that *was*
   measured and *is* in the table. Recount before the number is cited.
