# Carwash_NeurIPs — instructions for coding agents

Reproducibility bundle for one binary operational decision, measured two ways.

```
prompts/        the experiment. Never edited. summary.md maps each file to
                the condition name in the runs (substrate.txt is recorded
                as substrate_llama_v3).
behavioural/    workbench/ + scripts/ + runs/<host>/ + summary.md — what
                models emit. runs/ is split by host (Anthropic, OpenAI,
                OpenRouter, RunPod), not by condition: every record carries its
                own `condition` field, so never infer a condition from a path.
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
- **The behavioural population is 23 models, and that is the only number to
  quote — but it is 22 right now.** Llama 3.3-70B was removed from
  `behavioural/runs/` and `internals/results/` pending a re-run that gives it a
  local behavioural arm, a margins pass on the current prompts and a patch grid
  from that same pass. Until those land, every count this file and the paper
  quote is short by one model: do not publish a number generated in this
  window. Re-populate with
  `run_local_fleet.py --models llama-3.3-70b`, then `runpod_margins.sh
  llama-3.3-70b`, then `runpod_patchgrid.sh llama-3.3-70b` — in that order,
  because the grid cross-checks the margins file and fails if they are from
  different passes. A model reproducibly correct at baseline has nothing to rescue, so it
  is excluded *and its runs are removed* — Qwen2.5-3B was, in `d6746f6`. Do not
  write "24 measured, 23 reported"; screen a new model on the baseline condition
  alone before sampling the other nine.
  `behavioural/workbench/paper_numbers.py` asserts this and names any model that
  breaks it. It also prints every population-dependent count the paper cites —
  run it after any change to `runs/` and diff the paper against it rather than
  re-checking counts by hand.
- **Two Llamas were sampled both hosted and locally; the local arm is the one
  kept.** Its precision, device and per-sample seed are recorded, the hosted
  Llama runs were routed across up to five upstream providers within a single
  ten-sample run, and the internals were measured on the local weights. The
  hosted 8B and 3B rows were removed in `4fe2da5`; before that they disagreed
  with the local arm in five of twenty condition cells, including substrate
  7/10 hosted against 10/10 local on Llama 3.1-8B. Llama 3.3-70B and
  Llama 4-Maverick have no local runs and stay hosted.
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
M = −0.38 at baseline and +0.17 under the substrate, transplant at L13
(29 Sep run; the September pass gave −0.50 / +0.18 for the same two cells).

`scripts/patch_grid.py` patches *every* condition into the baseline, not only
the substrate, and writes `patch_grid.json` beside `internals.json`. Run it
after `runpod_margins.sh` on the same pod — it cross-checks its own substrate
row against that file's `patching` array, and the check only means anything if
the two are from the same pass. `scripts/runpod_patchgrid.sh` is the driver and
`scripts/plot_patch_grid.py` draws the figure.

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
- Two runs of the same model on different pods differ, and by more than the
  second decimal: between the September pass and the 29 Sep re-run Qwen3-8B's
  baseline moved −14.07 → −13.66 and Llama 3.2-3B's −0.50 → −0.38, on identical
  prompts, torch and transformers. Signs, crossings and transplant layers did
  not move. Cite one run per model; do not take the baseline from one and an
  ablation from another. The 29 Sep run is the canonical one.
- `analyse_prompt` builds `_stack` *after* calling `decision_margin`, which
  fires the `Capture` hooks again. It is only correct because every real cell
  decides at step 0, so the last hook firing is still a full-prompt pass whose
  last position is the answer position. If a model ever returns
  `decision.step` other than 0, that run's `patching`, `diff`, `lens` and `dla`
  are captured at a *generated* token instead and must not be cited. Check
  `decision.step` before citing anything derived from the residual stream.
- `lens.final_row_matches_model` is the script's own check that the logit lens
  reproduces the model's logits at the last row. It is False for
  qwen2.5-1.5b/baseline and qwen3-8b/substrate in the 29 Sep run. Nothing in
  the paper rests on the lens, but do not start citing it without looking.
