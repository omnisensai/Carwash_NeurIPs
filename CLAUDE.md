# Carwash_NeurIPs — instructions for coding agents

Reproducibility bundle for one binary operational decision, measured two ways.

```
prompts/        the experiment. Never edited.
behavioural/    scripts/ + runs/ + models.md, summary.md — what models emit
internals/      scripts/ + results/ + README.md, RESULTS.md — what changes inside
paper/          LaTeX sources and bibliography
```

Read `internals/README.md` for what each readout means and
`internals/RESULTS.md` for the current numbers.

## Ground rules

- **Never edit anything in `prompts/`.** Not even whitespace. The prompt
  files are the experiment. If a file looks odd (e.g. a trailing
  `SHA-256:` line), leave it; the scripts already handle that.
- **Never push to `main`.** Work on a branch and open a pull request.
- **Every internals run must use the same prompt texts as the behavioural
  runs**: substrate sha256 `340228f9…`, baseline sha256 `f9ac23fb…`, both
  recorded in each `internals.json`. A run on any other prompt text does not
  belong in `internals/results/` and must not be mixed into the paper's
  tables. Check before you cite a number:
  `python -c "import json;d=json.load(open(P));print(d['substrate_sha256'][:8],d['baseline_sha256'][:8])"`
- **The existing internals runs carry one prompt that `prompts/` no longer
  holds.** `run_internals.py` sweeps every `prompts/*.txt`, and when the ten
  runs were made the folder still contained `benchmark_goaloriented.txt`
  (deleted in `e2f54cc`). So each `internals.json` has ten `benchmarks` keys
  against the nine conditions the behavioural runs sampled. The extra one is
  `benchmark_goaloriented`, which never had a behavioural counterpart — the
  condition the paper calls *objective emphasis* is `benchmark_urgency.txt`.
  Never include `benchmark_goaloriented` in a range or count reported as "the
  seven conventional conditions"; taking it as the maximum is how `-4.67` and
  `-0.35` reached a draft in place of `-5.51` and `-0.83`. A re-run on the
  current `prompts/` will produce nine keys and drop it.
- **There is no library control on the current prompts.**
  `benchmark_library.txt` was removed from `prompts/` on 19 Sep, so every run
  records `library: null` and an empty `anti_test`. Do not describe a
  generalization control that was not measured.
- Result folders are `internals/results/<model>/bf16/`. `scripts/runpod.sh`
  does this for you; do not invent other names.
- **Do not rewrite `internals/scripts/run_internals.py`, `cdim.py` or
  `plot_internals.py`** to make a run pass. If something fails, fix the
  environment or report the traceback; a small compatibility patch is fine if
  it is clearly explained in the commit message.
- Commit messages: one short line, no trailers.
- Report what actually ran. If a step was skipped or errored, say so; do not
  paraphrase numbers you did not measure.

## Running a model

Compute is minutes — a few dozen short forward passes, prompts under 300
tokens. Weight download dominates (~140 GB for the 70B in bf16).

```bash
cd internals
export HF_HOME=/workspace/hf HF_HUB_ENABLE_HF_TRANSFER=1
pip install -q --break-system-packages "transformers>=4.45" accelerate bitsandbytes numpy matplotlib hf_transfer

MODEL=unsloth/Llama-3.2-3B-Instruct bash scripts/runpod.sh     # internals.json + figures
CDIM=1 MODEL=unsloth/Llama-3.2-3B-Instruct bash scripts/runpod.sh   # + the intervention map and controls
python scripts/plot_internals.py results/llama-3.2-3b/*/
```

`scripts/runpod_qwen.sh` is the driver that produced `results/qwen*/bf16/`: it
runs the seven Qwens in one go and refuses to finish unless every result it
wrote is on the current prompts. `scripts/runpod.sh` is the general one-model
driver.

The script picks precision from the GPU memory it finds and records it as
`quantize` in the json; say which one ran. bf16 is the reference — the 8B
numbers move by ~0.6 nats between bf16 and nf4. Run under `tmux` or `nohup`
so a dropped SSH session does not kill the run.

Sanity check against `internals/RESULTS.md`: Llama 3.2-3B should give
M = −0.50 at baseline and +0.18 under the substrate, transplant at L13.

## Things that went wrong before (so you do not repeat them)

- Full-sequence logits over the 128k vocabulary OOM on small cards; the
  script already passes `logits_to_keep=1`. Do not remove it.
- Feeding the prompt files raw (no chat template) makes Llama open with
  ` **` markdown; the first-token margin is then meaningless. The default
  is the chat template; `--raw` exists for comparison only, and the
  `decision` field in the json is the margin at the token where the word
  actually lands.
- `device_map="auto"` on a shared single card spills layers to CPU and
  bitsandbytes refuses; the script forces `{"": 0}` on one card.
- Two runs of the same model on different pods differ in the second decimal
  (Qwen3-8B: −14.0745 vs −14.0627). Cite one run per model; do not take the
  baseline from one and an ablation from another.
