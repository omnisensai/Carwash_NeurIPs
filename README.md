# Substrate Engineering — reproducibility bundle

One binary operational decision, measured two ways on the same prompt texts.

```
prompts/        the experiment: baseline question, seven conventional prompts,
                the substrate. Never edited.
behavioural/    what the models emit. scripts/ + runs/ (one .jsonl per model
                per condition, ten samples each) + models.md, summary.md
internals/      what changes inside the open-weight models. scripts/ +
                results/<model>/bf16/ + README.md, RESULTS.md
paper/          the LaTeX sources and the bibliography
```

Every internals run in `internals/results/` used the same prompt texts as the
behavioural runs: substrate sha256 `340228f9…`, baseline sha256 `f9ac23fb…`.
Runs on earlier substrates or an earlier question wording are not in the working
tree; they are in git history before `efbc195`.

## Reproducing

Behavioural, open-weight models (needs a GPU):

```bash
python behavioural/scripts/run_local_fleet.py --help
```

Internals, one model (needs a GPU):

```bash
cd internals
MODEL=unsloth/Llama-3.2-3B-Instruct bash scripts/runpod.sh
python scripts/plot_internals.py results/llama-3.2-3b/*/
```

The hosted-API conditions in `behavioural/runs/` were sampled through provider
APIs; their driver is not in this repo. Each row records the provider, model
slug, temperature, and the sha256 of the text sent, so the conditions can be
reissued against any provider.

## What the numbers are

`behavioural/summary.md` — operational state per model per condition.
`internals/RESULTS.md` — decision margins, transplant layers and controls.
`paper/paper_results.tex` — both, as reported.
