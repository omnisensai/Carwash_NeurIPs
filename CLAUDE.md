# Carwash_NeurIPs — instructions for coding agents

This repo is a reproducibility bundle for a NeurIPS submission. `prompts/`
and the `*.md` at the root are the paper's material. `internals/` is a
residual-stream analysis of the same prompts on open-weight Llamas
(logit lens, activation patching, direct logit attribution, attention,
line ablations). Read `internals/README.md` for what each readout means and
`internals/RESULTS.md` for what came out on 3B / 8B.

## Ground rules

- **Never edit anything in `prompts/`.** Not even whitespace. The prompt
  files are the experiment. If a file looks odd (e.g. a trailing
  `SHA-256:` line), leave it; the scripts already handle that.
- **Never push to `main`.** Work on a branch named `results-<model>` (e.g.
  `results-llama-70b`) and open a pull request. Commit only what you
  produced under `internals/results/<model>/` (the run log is written there).
- Result folders follow `internals/results/<model>/<precision>[-<substrate>][-raw]/`,
  e.g. `llama-3.1-8b/bf16`, `llama-3.1-8b/nf4`, `llama-3.1-8b/bf16-pro`.
  `runpod.sh` does this for you; do not invent other names.
- **Do not rewrite `internals/run_internals.py` or `plot_internals.py`** to
  make a run pass. If something fails, fix the environment or report the
  traceback in the PR; a small compatibility patch is fine if it is
  clearly explained in the commit message.
- Commit messages: one short line, no trailers.
- Report what actually ran. If a step was skipped or errored, say so in the
  PR text; do not paraphrase numbers you did not measure.

## The job: run the internals sweep on Llama-3.3-70B

Everything is a few dozen short forward passes (prompts are < 300 tokens),
so compute is minutes. The 70B download (~140 GB in bf16) dominates.

### 1. Pod

- GPU: **2× A100 80 GB or 2× H100 80 GB for bf16** (preferred: the 8B
  numbers move by ~0.6 nats between bf16 and nf4, so bf16 is the reference).
  Fallback: 1× 80 GB card runs 8-bit; a 48 GB card runs 4-bit. The script
  picks the precision from the GPU memory it finds; say which one ran.
- Template: any recent PyTorch CUDA image (RunPod "PyTorch 2.x" is fine).
- **Volume: ≥ 250 GB**, mounted at `/workspace`. Put the HF cache on it.
- No HF token is needed: `unsloth/Llama-3.3-70B-Instruct` is an ungated
  mirror of Meta's weights (identical tensors).

### 2. Setup (inside the pod)

```bash
cd /workspace
git clone https://github.com/omnisensai/Carwash_NeurIPs && cd Carwash_NeurIPs
git checkout -b results-llama-70b
export HF_HOME=/workspace/hf HF_HUB_ENABLE_HF_TRANSFER=1
pip install -q "torch>=2.4" "transformers>=4.45" accelerate bitsandbytes numpy matplotlib hf_transfer
cd internals
```

Sanity check on a small model first (2–3 minutes, catches environment
problems before the 140 GB download):

```bash
MODEL=unsloth/Llama-3.2-3B-Instruct bash runpod.sh
```

Expected: `results/llama-3.2-3b/bf16/summary.md` with baseline
M ≈ −3.5 and substrate M ≈ −1.8 (both Walk). If the numbers are within
±0.3 of that, the environment matches ours.

### 3. The 70B runs

```bash
bash runpod.sh                                # substrate.txt      → results/llama-3.3-70b/<precision>/
SUBSTRATE=substrate_pro.txt bash runpod.sh    # substrate_pro.txt  → results/llama-3.3-70b/<precision>-pro/
python plot_internals.py results/llama-3.3-70b/*/            # + results/llama-3.3-70b/overview.png
```

Run in `tmux` or `nohup` so a dropped SSH session does not kill the run.
The first run downloads the weights; the second reuses the cache.

If the pod has one card and the script chose 4-bit/8-bit, also note the
`quantize` field in `internals.json` in the PR text.

### 4. Deliver

```bash
cd /workspace/Carwash_NeurIPs
git add internals/results/
git commit -m "internals: Llama-3.3-70B results"
git push -u origin results-llama-70b
```

Then open a PR against `main` with: pod GPU(s), precision that ran,
the two headline M values (baseline / substrate) per substrate file, and
the sanity-check numbers from step 2. Paste the `summary.md` of the 70B
runs into the PR description.

### What to look at (and mention in the PR)

- `summary.md` → the first table (baseline vs substrate M, greedy answer).
- `patching` line → the first layer from which the substrate residual alone
  flips the baseline (was L17/32 on 8B, L15 with substrate_pro).
- `substrate line ablations` → whether one line carries the effect (8B:
  line 6 for substrate.txt; spread out for substrate_pro).
- `anti_test` rows → the library question must stay Walk under every
  substrate; if it goes Drive, say so prominently.

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
