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

### 1. The CoT condition does not measure chain-of-thought across the fleet

`prompts/benchmark_CoT.txt` contains two conflicting instructions —
`Let's think step by step!` and `Answer with exactly one word: walk or drive`.
All 170 CoT rows share one prompt sha (`5ad509a4...`), so every model got the
same conflict. Which instruction wins is model-dependent:

| Outcome | Models |
|---|---|
| Prose in all 10 rows | Sonnet 4.5 |
| Prose in 6 of 10 | Llama 4-Maverick |
| Reasoned invisibly (tokens billed, not returned) | Kimi K2 |
| No reasoning tokens at all | DeepSeek, GPT-3.5/4/4o/4.1/4.1-mini, Llama 3B/8B/70B, Opus 4.7, Sonnet 5 |
| `output_tokens_details` absent — unmeasurable from the file | Haiku 4.5, Sonnet 4.6 |

The one-word rows are not refusals: those models complied with the instruction
the prompt gave them. But only 2 of 17 reasoned visibly, so the condition is not
comparable across the fleet. A clean CoT run needs the constraint removed —
`--verbatim` or `--two-turn`.

Two results that are in the data regardless:

- **Sonnet 5 flips completely**: 10/10 `Walk` at baseline to 10/10 `Drive` under
  CoT (Fisher exact p = 1.1e-05), with `thinking_tokens: 0` and a 5-token
  output. No reasoning occurred — the context change alone moved the answer.
- **Sonnet 4.5 states the decisive fact and does not act on it.** Rows 0, 6 and
  9 note that the car has to be driven back, then conclude `walk`. The two rows
  that follow the fact through conclude `drive`.

Fleet-wide, with the re-run Mistral rows included: **92.4% walk at baseline
(157/13, n=170) vs 85.6% under CoT (143/24, n=167)**, Fisher two-sided
**p = 0.056** — short of significance at 0.05.

This is worth flagging: before Mistral was re-run its 10 rows were absent and
the same comparison gave 84.9% and p = 0.037. Restoring 8 genuine `walk` rows
moved the shift from nominally significant to not. The fleet-level
baseline-vs-CoT effect does not survive completing the data, and should not be
reported as significant. The per-model effects below are unaffected.

### 2. Rows that cannot be used as measurements

- **`CoT/cot_kimi`**: row 2 hit the cap (`completion_tokens: 2000`,
  `finish_reason: length`, `content: null`) — reasoned, never answered. Row 3
  generated 1,220 reasoning tokens that are absent from the file; its `drive`
  decision is usable, its reasoning is not. Kimi's `max_tokens: 2000` is a
  *reasoning* budget and is too small.
- **`CoT/cot_mistral`**: re-run 2026-09-19T09:30Z through OpenRouter (the
  original attempt used a direct Mistral API with no key and lost all 10 rows).
  8 of 10 rows now carry data — all `walk`. Samples 7 and 8 still fail with an
  upstream `429` after backoff. Note this file ran at `max_tokens: 80` while the
  other 16 CoT files used `500`; nothing truncated (all `finish_reason: stop`,
  2 tokens), but it is not the same configuration as the rest of the sweep.

### 3. `baseline/summary.md`'s aggregate does not match its own table

The per-model table agrees with the rows exactly. The aggregate line beneath it
reads `148 walk / 12 drive across 160 samples` from `16 of 17 models` (92.5%);
the 17 files hold **157 walk / 13 drive across 170 samples** (92.35%). The
difference is exactly GPT-3.5-turbo's 9/1 — a model that *was* measured and *is*
in the table. Recount before the number is cited.

The same file's note that Kimi K2 needs `max_tokens=2000` for reasoning tokens
is correct, and describes the CoT runs: Kimi reports
`reasoning_tokens: [0, 1220, 1999]` there (and 0 at baseline).

### 4. Cite a commit, not a path

These files are re-uploaded as runs are repeated — `cot_opus` changed from
`max_tokens: 80` to `500` mid-review, and the CoT directory went from 1 file to
17. Any figure quoted in the paper should name the commit it was computed from.

### 5. Cosmetic

`baseline/baseline_opus_206-09-19.jsonl` — `206` should be `2026`.
