# internals — what the substrate changes inside the model

Companion to the prompt-level benchmark: the same `baseline.txt` vs
`substrate.txt` comparison, but read out of the residual stream of open-weight
Llamas instead of the API. Everything is measured at the position that
predicts the first answer token (the `Drive` / `Walk` token), teacher-forced,
no sampling.

```
run_internals.py    GPU (or CPU for ≤8B): one model → results/<model>/<precision>[-<substrate>]/internals.json
plot_internals.py   no GPU: json → lens.png, dla.png, heads.png, attention.png,
                    ablations.png, benchmarks.png, diff.png, summary.md (+ overview.png)
runpod.sh           the whole thing on a fresh CUDA box (70B)
```

## Readouts

| readout | what it answers |
|---|---|
| final M | `log P(drive) − log P(walk)` (paper's margin; `M_sum` sums the surface variants `Drive`/` drive`/…, `M_first` uses the best single token of each) |
| logit lens | M when the residual after layer *l* is pushed straight through the final norm + unembedding — *when does the lens see the flip* |
| patching | baseline prompt, but the residual at the answer position after layer *l* is swapped for the substrate run's — *from which layer onward does the residual already carry the decision* (the lens can lag this by many layers) |
| DLA | exact decomposition of M into the contribution of every attention / MLP sublayer and every head (final RMSNorm is linear given the final rms) — *which components write the margin* |
| attention | mass from the answer position onto each substrate line, the headers, the question, the words walk/drive/car, `<bos>` — *what the answer position reads directly* |
| ablations | leave-one-line-out and one-line-only substrates → M — *which of the six lines does the work* |
| benchmarks | every file in `prompts/` → M, argmax and a 4-token greedy answer — reproduces the paper's table locally |
| diff | cosine between the baseline and substrate residuals per layer, and cosine of their difference with the drive−walk unembedding direction |

Not supported: hybrid architectures whose decoder layers have no `self_attn`
(Qwen3.5 / Qwen3-Next style linear-attention blocks) — the hooks fail at load.

Sanity checks stored in the json: the last lens row reproduces the model's
logits (`final_row_matches_model`), and the DLA sums equal the model's
`M_first` (`dla.total` vs `dla.M_first_check`).

## Running

```
# 3B / 8B on one 16 GB card (8B next to other GPU users: --quantize 4bit)
python run_internals.py --model unsloth/Llama-3.2-3B-Instruct --out results/llama-3.2-3b/bf16
python run_internals.py --model meta-llama/Llama-3.1-8B-Instruct --quantize 4bit --out results/llama-3.1-8b/nf4
# exact bf16 reference for 8B without a free GPU: CPU, ~1 min on 16 cores / 30 GB RAM
python run_internals.py --model meta-llama/Llama-3.1-8B-Instruct --device cpu --dtype bfloat16 --out results/llama-3.1-8b/bf16
# figures + summary.md, several dirs → also results/overview.png
python plot_internals.py results/llama-3.2-3b/bf16 results/llama-3.1-8b/bf16
# 70B on RunPod
bash runpod.sh
```

Prompts are fed through the model's chat template (`System:` block → system
message, the rest → user message, then the assistant header); `--raw` feeds
the files verbatim instead. `--no-patching`, `--no-ablations`,
`--no-benchmarks` skip the extra forward passes.

`resid_last.pt` keeps the per-layer residual stacks at the answer position
for both prompts plus the drive−walk unembedding direction, for follow-up
work (steering vectors, cross-model comparison).
