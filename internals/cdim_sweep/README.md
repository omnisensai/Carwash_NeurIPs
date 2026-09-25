# cdim_sweep — three controlled extensions of the CDIM experiment

Prepared 19 Sep 2026, re-anchored 21 Sep after `prompts/substrate.txt` became the nine-line substrate; nothing run yet on a real model (the pipeline was
smoke-tested end to end on SmolLM2-135M only; those numbers mean nothing).
Everything lives in this folder; `prompts/`, the paper files and the sweep
scripts of the first round are untouched except for `cdim.py`, whose `main()`
was split into a reusable `run_cdim()` and which now accepts paths for
`--substrate` / `--baseline` and a `--library` control question (default
behaviour unchanged).

## Why

`CDIM_RESULTS.md` has two findings worth a paper and one weakness that
undercuts both:

1. Whether a rule's effect travels through the question representation
   depends on how the rule is written (70B: ≤ 13 % via the question span with
   the abstract substrate, 36–46 % with the explicit one). Two points, one model.
2. Three words appended to the question move margins by up to 22 nats, more
   than the substrate itself (`RESULTS.md`). Measured, but not designed.
3. Every number so far is one task, one question, one answer token.

The three experiments below turn 1 and 2 into manipulated variables and fix 3
with the same grid.

## The material

| file | what |
|---|---|
| `ladder.json`, `ladder/L0.txt`, `ladder/L1..L5.txt`, `ladder/pro.txt` | the explicitness ladder. L0 = the six-line abstract substrate of 17 Sep (retired from `prompts/` on 19 Sep, kept here verbatim; the first-round results were measured on it). L1–L5 do one more step of the inference chain each, same six bullet slots: L1 names the answer verbs; L2 adds concrete nouns as examples; L3 replaces every abstraction; L4 states each line's consequence; L5 states the verdict. Templated over the scenario fields, so every level exists for every scenario. **S = the official `prompts/substrate.txt`** (nine lines with a Definitions block, read live). pro = the retired `substrate_pro.txt`. On explicitness, S sits between L2 and L4: definitions name the car and the car wash, consequences are stated, no verdict. |
| `ladder_counterfactuals.json`, `../cdim_counterfactuals.json` | one reversal per line per level (+ a strong reversal of the decisive line), token-aligned under the Llama-3 and Qwen3 tokenizers for every drive scenario. Templated levels here; S / L0 / pro in `../cdim_counterfactuals.json` keyed by file name. `check_align.py` verifies without a model; all rows pass. |
| `scenarios.json` | 13 tasks: 7 where the object is the vehicle (carwash, fuel, tyres, inspection, oil, parking, van → drive) and 6 portable-object controls (library, post, pharmacy, bakery, dry cleaner, keys → walk). |
| `paraphrases.json` | 12 question bodies × 3 answer tails (T0 = old wording, T1 = current, T2 = "drive or walk"). carwash × P0 × T1 is `prompts/baseline.txt` byte for byte. The control question per cell is the paired walk scenario, so the deleted `benchmark_library.txt` is not needed. |
| `build_prompts.py` | renders everything into `generated/` (git-ignored, rebuilt by the runners). |
| `run_grid.py` | behavioural grid: 4212 cells (13 scenarios × 36 questions × {none, L0–L5, S, pro}) + 60 leak-test cells (walk questions under the carwash-filled L2–L5 and S). One pass each. |
| `run_cdim_cells.py` | CDIM maps on the cells that matter, one model load: ladder L1–L5 and S (carwash), 13 paraphrase cells and 6 scenario cells on S (`--level` picks another). Control question per cell = the paired walk scenario under the same substrate. |
| `analyse.py` | `sweep_summary.md` + three figures per result dir. |
| `runpod_sweep.sh` | all of it on a pod; resumable. |

Result folders: `results/<model>/<precision>-sweep/{grid.json, ladder/<L>/, paraphrase/<P>_<T>/, scenario/<s>/}`.
The L0 and pro carwash cells are the first-round cdim.json files, now under `results/old-substrate-v1/<model>/<precision>[-pro]/`; `analyse.py` uses them only when their bullet lines match the retired files. `runpod.sh` reruns on the old models must set `OUT=` so those folders are not overwritten with the new substrate.

## Predictions, written before running

**Ladder (dose-response).** H1: the share of the primary line's effect that
the question span carries rises monotonically from L0 to L5 (70B: ~0.1 at L0,
the pro substrate's 0.4 sits somewhere around L3–L4). H1': the hand-off depth
(last row where the line's own tokens carry ≥ ½Δ) moves earlier with
explicitness. Alternative outcome: the share jumps between two levels rather
than climbing, which localises the switch to one feature (concrete nouns vs
consequences vs verdict). Either result replaces the two-point contrast. If
neither share nor depth moves, the Section 6 route hypothesis is dead and the
paper says so.

**Paraphrases (mechanism vs readout).** H2: M(S) varies across the 36
questions by more than the substrate effect, as in `RESULTS.md`, while the
hand-off depth and the question share stay within the random-direction
control. That decoupling ("the mechanism is stable, the readout is not") is
the headline if it holds. H2 fails if the route metrics track M(S)
(`sweep_stability.png` shows a trend), in which case the route is a function of
the margin and not of the rule.

**Scenarios (generality and selectivity).** H3: on the six other vehicle
tasks the abstract substrate flips or raises M with the same primary line
(70B: line 5 or 6) and the same hand-off depth as carwash; on the six portable
tasks it leaves M below zero (selectivity ≥ 0.8 in grid A). H3': the
carwash-filled concrete substrates (L3–L5) do not leak drive onto walk
questions (grid B). A leak at L5 (verdict line) but not at L3 would show at
which explicitness the model stops applying the rule conditionally.

## Running (GPU only; nothing here runs on CPU by default)

```bash
# pod: 2× A100/H100 80 GB, volume ≥ 250 GB at /workspace, HF_HOME on it (see CLAUDE.md, runpod.sh)
cd /workspace/Carwash_NeurIPs/internals/cdim_sweep
python check_align.py                                     # tokenizers only, ~10 s
nohup bash runpod_sweep.sh > sweep70b.log 2>&1 &          # Llama-3.3-70B, bf16
MODEL=Qwen/Qwen3-8B nohup bash runpod_sweep.sh > sweep_qwen.log 2>&1 &   # afterwards, same pod
python analyse.py ../results/llama-3.3-70b/bf16-sweep ../results/qwen3-8b/bf16-sweep
```

Cost on 70B at row stride 2 (measured 0.2 s per pass in the first round):
grid ≈ 15 min, each CDIM cell with `--map auto` ≈ 5–10 min, 24 cells ≈ 3–4 h.
Qwen3-8B is faster. Budget ≈ $15 at $3.2/h. The pod from 18 Sep was
terminated; start a fresh one (`runpod-access` memory note has the recipe).

Priorities if time is short: ladder first (`PLAN=ladder`), then paraphrase,
then scenario. The grid is cheap and should always run.

## What to look at afterwards

- `sweep_summary.md` → "CDIM: ladder" table and `sweep_ladder.png`: is the
  question share monotone in the level?
- "Operating envelope" table and `sweep_envelope.png`: how wide is M across
  paraphrases per substrate, and does a substrate narrow it?
- `sweep_stability.png`: route metrics against M(S) over paraphrases and
  scenarios. Flat = H2 holds.
- "Grid A" selectivity column and "Grid B" leak table.
- Every cell's `control stays walk` column must be True.
