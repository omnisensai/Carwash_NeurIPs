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
python scripts/run_internals.py --model unsloth/Llama-3.2-3B-Instruct --out results/llama-3.2-3b/bf16
python scripts/run_internals.py --model meta-llama/Llama-3.1-8B-Instruct --quantize 4bit --out results/llama-3.1-8b/bf16
# exact bf16 reference for 8B without a free GPU: CPU, ~1 min on 16 cores / 30 GB RAM
python scripts/run_internals.py --model meta-llama/Llama-3.1-8B-Instruct --device cpu --dtype bfloat16 --out results/llama-3.1-8b/bf16
# figures + summary.md, several dirs → also results/overview.png
python scripts/plot_internals.py results/llama-3.2-3b/bf16 results/llama-3.1-8b/bf16
# 70B on RunPod
bash scripts/runpod.sh
```

Prompts are fed through the model's chat template (`System:` block → system
message, the rest → user message, then the assistant header); `--raw` feeds
the files verbatim instead. `--no-patching`, `--no-ablations`,
`--no-benchmarks` skip the extra forward passes.

`resid_last.pt` keeps the per-layer residual stacks at the answer position
for both prompts plus the drive−walk unembedding direction, for follow-up
work (steering vectors, cross-model comparison).

## CDIM — constraint–depth intervention map (`cdim.py`, `plot_cdim.py`)

The experiment of `Mechanistic_paper.md` §2–§9. Instead of substrate vs. no
system prompt, it compares the substrate S with a **token-aligned
counterfactual C_i**: the same prompt with bullet line i replaced by a line of
identical token count that reverses or neutralises its meaning
(`cdim_counterfactuals.json`; the script refuses a line whose token count
differs). Everything is M at the answer position, chat template, teacher-forced.

| readout | what it answers |
|---|---|
| `delta_beh` | M(S) − M(C_i): does the line matter behaviourally (before any tracing) |
| `R[group][row]` forward rescue | C_i run, the S residual of one semantic group (a line, the headers, the whole system block, the question, the answer instruction, the assistant header, the answer site) patched in after row *r* → M − M(C_i): *where is the substrate-conditioned state sufficient* |
| `D[group][row]` reverse disruption | S run, the C_i residual patched in → M(S) − M: *where is it necessary* |
| controls | same-run patch S→S (must be 0), random direction of the same norm as S−C (must be small). The script can also run a control question that must stay Walk, but `benchmark_library.txt` was removed from `prompts/` on 19 Sep, so every current run records `library: null` and no such control was measured. |
| path | patch-the-receiver path patching for the primary line: its S state inserted at row r_src, then only the resulting question-span / answer-site state at row r_dst inserted into a clean C_i run → how much of the rescue is mediated by that receiver |

Row 0 is the embedding output (patching the line there = the input-level
counterfactual, so `R[line_i][0]` must equal `delta_beh`), row l+1 the output
of layer l.

```
python scripts/cdim.py --model meta-llama/Llama-3.1-8B-Instruct --device cpu --dtype bfloat16 --out results/llama-3.1-8b/bf16
python scripts/cdim.py --model unsloth/Llama-3.3-70B-Instruct --row-stride 2 --path-stride 4 --out results/llama-3.3-70b/bf16
python scripts/plot_cdim.py results/llama-3.1-8b/bf16 results/llama-3.3-70b/bf16      # + results/<model>/bf16/cdim_map.png
```

Outputs next to `internals.json`: `cdim.json`, `cdim_resid.pt` (full S / C
residual stacks of the primary counterfactual), `cdim_map.png` (Fig. 2),
`cdim_maps_all.png`, `cdim_agreement.png` (Fig. 3), `cdim_path.png` (Fig. 5),
`cdim_library.png`, `cdim_lens_vs_rescue.png`, `cdim_summary.md`.
Cost: (rows × groups × 2) forward passes per mapped counterfactual, ≈ 800 on
8B; `--map auto` maps only the lines with |Δ| ≥ `--min-delta`.
