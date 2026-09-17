
# Substrate Engineering: Input Structure as a Control Surface for Reproducible LLM Decisions

## Core Thesis

Incorrect LLM behavior is commonly interpreted as evidence of insufficient model capability.

This inference is not always valid.

At inference time, model output is produced by an interaction between the learned model, the supplied input, the decoding procedure, and the execution environment:

$$
y = F(\theta,x,d,e)
$$

where:

* \(\theta\) denotes model architecture and frozen learned weights,
* \(x\) denotes the application-supplied input and context,
* \(d\) denotes decoding configuration,
* \(e\) denotes the execution environment.

Holding \(\theta\) and \(d\) fixed, we find that small changes to \(x\) can move the same binary decision by tens of nats and reverse strongly expressed outputs.

The same frozen model can therefore appear incapable under one input structure and strongly capable under another.

We call this phenomenon **input-induced decision displacement**.

Substrate engineering treats semantic input structure as an application-level control surface for reducing task-irrelevant decision displacement and moving the intended decision toward a stable region.

For a correct answer \(y^*\) and competing answer \(y'\), define:

$$
M^*(x)
=
\log P(y^*\mid x)
-
\log P(y'\mid x).
$$

Correctness requires:

$$
M^*(x)>0.
$$

Operational reproducibility requires the decision to remain sufficiently far from the boundary that execution-level perturbations cannot reverse it:

$$
M^*(x)>\varepsilon_{\mathrm{exec}}.
$$

This produces the central engineering problem:

> **A substrate can create point reproducibility, but the substrate itself has a validity boundary across input formulations, task scope, and model families.**

The problem of substrate engineering is therefore to identify and maximize the region over which the intended decision remains reproducibly correct.

---

# 1. Introduction — When a Wrong Answer Is Not a Capability Failure

LLM failures are frequently interpreted through a capability lens.

A model answers incorrectly, and the natural diagnosis is that the model lacks sufficient reasoning ability, knowledge, scale, or training. This interpretation motivates a common engineering strategy: use a stronger model or wait for the next model generation.

For operational LLM-native systems, this diagnosis can be incomplete.

Model behavior is not determined by learned weights alone:

$$
y=F(\theta,x,d,e).
$$

The same frozen model may produce substantially different decisions when the semantic structure of the input changes.

This matters because application developers usually cannot modify model weights or provider infrastructure at inference time. They can, however, directly control the supplied input.

We study whether input structure can alter an operational decision sufficiently strongly that an apparent model failure changes without changing the model itself.

We use a deliberately minimal binary task:

$$
\texttt{walk}
\quad \text{vs.} \quad
\texttt{drive}.
$$

The task asks how a user should reach a nearby car wash when the user's objective is to wash the car.

The simplicity is intentional. It removes retrieval, planning, tools, memory, orchestration, and long-horizon execution and isolates a single decision boundary.

Across frontier API models and open-weight models, we test conventional prompt interventions and a structured semantic substrate.

Three observations motivate the paper.

First, the baseline decision is not a fixed property of model capability. Different models occupy different locations relative to the same decision boundary.

Second, holding model weights fixed, small changes in task formulation can produce decision-margin shifts comparable to or larger than the substrate intervention itself.

Third, explicitly structuring the task-relevant semantic relations can move strongly incorrect decisions to strongly correct ones without changing the model.

These results suggest that some apparent reasoning failures are more accurately described as **input-conditioned decision failures**.

The engineering question then becomes:

> **Can input structure place the intended decision far enough from its boundary to make correctness reproducible, and over what scope does that condition remain valid?**

---

# 2. Problem Formulation — Input-Induced Decision Displacement

We model inference as:

$$
y=F(\theta,x,d,e).
$$

For a deployed API model, \(\theta\) is effectively fixed.

Decoding controls \(d\), such as temperature, can reduce sampling variance but do not necessarily alter the underlying preference between competing decisions.

The execution environment \(e\) includes provider routing, hardware, numerical precision, quantization, batching, kernels, and runtime implementation.

The input \(x\) remains directly engineerable.

We therefore treat input structure as an inference-time control variable.

For the binary task, define:

$$
M(x)
=
\log P(\texttt{drive}\mid x)
-
\log P(\texttt{walk}\mid x).
$$

Then:

$$
M(x)>0
\Rightarrow
\texttt{drive},
$$

$$
M(x)<0
\Rightarrow
\texttt{walk}.
$$

The effect of an input intervention is:

$$
\Delta M
=
M(x')
-
M(x).
$$

We call this quantity **input-induced decision displacement**.

This distinction is important because categorical output hides the magnitude of movement.

Two prompts may both produce `walk` while locating the model at very different distances from the decision boundary.

Likewise, a model can move from:

$$
M\ll0
$$

to:

$$
M\gg0
$$

without any change to its learned weights.

Such a result rules out the explanation that the original failure was caused solely by absence of the capability required to produce the correct decision.

---

# 3. Experimental Design

We evaluate the decision across 19 frontier language models from seven vendors:

Anthropic, OpenAI, Meta, Alibaba, Mistral, DeepSeek, and Moonshot.

The behavioral benchmark compares:

* baseline input,
* chain-of-thought prompting,
* encouragement,
* expert-role prompting,
* hallucination warnings,
* error-avoidance instructions,
* threat,
* urgency,
* semantic substrate,
* semantic control conditions.

For models exposing log probabilities, we measure \(M\) directly.

For open-weight models, we additionally measure internal computation using:

* raw logit-lens projections,
* activation/residual patching,
* substrate line ablations,
* direct logit attribution.

All mechanistic readouts are taken at the position predicting the first answer token, with teacher forcing and fixed model weights.

The primary paper uses mechanistic analysis only to establish that the input intervention changes internal computation before the final output. Detailed mechanistic decomposition is treated as secondary analysis.

---

# 4. Result I — Model Failure Is Conditional on Input Structure

The baseline task does not produce one universal model behavior.

Some models strongly favor `walk`, some favor `drive`, and others lie near the decision boundary.

This already prevents a simple interpretation of the task as a universal capability failure.

More importantly, holding the model fixed while altering only the task formulation can produce extremely large decision-margin changes.

Changing the final instruction from:

> Answer with exactly one word:

to:

> Answer with exactly one word: walk or drive

leaves the underlying operational problem unchanged but materially alters the model's decision state.

For example, Qwen3-4B changes from approximately:

$$
M=+0.25
$$

to:

$$
M=-22.12.
$$

The model weights, decoding configuration, and underlying task remain fixed.

Only the input formulation changes.

The resulting displacement is therefore approximately:

$$
\Delta M\approx-22.4\text{ nats}.
$$

Comparable effects occur in other models, including output flips.

This demonstrates that functionally equivalent task formulations are not necessarily operationally equivalent for an LLM.

The implication is:

> **Observed failure cannot always be attributed solely to insufficient model capability. The input itself can place an otherwise capable model on the wrong side of the decision boundary.**

This also challenges the assumption that upgrading to a newer or stronger model monotonically resolves application-level decision failures.

A model update changes \(\theta\), and therefore changes the decision surface.

It does not eliminate the need to validate the application-level boundary.

---

# 5. Result II — Semantic Structure Can Reverse Strongly Expressed Decisions

We next test whether explicitly representing the task-relevant semantic relations can move the decision.

The semantic substrate specifies:

```text
User objective:
- Perform an activity on an object, while transporting the object from location A to B.
- No other objectives or goals are relevant for the user.

Action semantics:
- Activities require the object to move from location A to location B together with the user.
- The object is always initially with the user at location A.
- Moving the user without moving the object does not satisfy the objective.
- If the object is a vehicle, the user must operate the object in order to perform the activity at location B.
```

Unlike conventional prompt interventions, the substrate does not request additional effort, confidence, expertise, or correctness.

It changes the semantic structure supplied to the model.

Across the tested models, the substrate produces decision-margin shifts substantially larger than conventional prompting interventions.

Several open-weight examples illustrate the effect.

For Llama-3.3-70B:

$$
-13.78
\rightarrow
+6.07
$$

under the standard substrate, and:

$$
-13.78
\rightarrow
+17.00
$$

under the extended substrate.

For Qwen3-4B:

$$
-22.12
\rightarrow
+18.38
$$

under the extended substrate.

The same frozen model therefore moves by approximately:

$$
40.5\text{ nats}
$$

relative to its untreated decision state.

No model capability was added during this intervention.

The change results from altering the semantic information supplied at inference time.

The central result is therefore not that a particular prompt is better.

It is:

> **Semantic input structure can dominate the expressed decision of a fixed model.**

---

# 6. Result III — Correctness, Selectivity, and Scope Are Different Properties

A large substrate-induced shift does not automatically mean that the substrate has generalized correctly.

The library-book control demonstrates this distinction.

For the carwash task, movement toward `drive` is desirable.

For the library control, the correct answer remains `walk`.

Some smaller Qwen models move far enough toward `drive` under the substrate that they incorrectly output `drive` for the library condition.

In those models, the substrate acts more like a directional `drive` bias than a clean application of the intended semantic rule.

Other models retain the correct library output while still exhibiting measurable movement in the underlying margin.

Therefore:

$$
\text{response magnitude}
\neq
\text{semantic selectivity}.
$$

For a target and control condition, define:

$$
\Delta M_{\mathrm{target}}
=
M_{\mathrm{target,sub}}
-
M_{\mathrm{target,base}},
$$

$$
\Delta M_{\mathrm{control}}
=
M_{\mathrm{control,sub}}
-
M_{\mathrm{control,base}},
$$

and:

$$
Q
=
\Delta M_{\mathrm{target}}
-
\Delta M_{\mathrm{control}}.
$$

\(Q\) captures differential target–control response.

A useful substrate therefore needs more than a large target shift.

It must also maintain the correct behavior over the semantic scope for which it is claimed.

This motivates the idea of the substrate as a **scope-specific reproducibility mechanism** rather than a universally generalizing prompt.

---

# 7. Result IV — The Input Intervention Changes the Internal Computation

The behavioral results establish that changing \(x\) changes the final decision.

Open-weight models allow us to test whether this effect is already present inside the forward computation.

We compare direct logit-lens projection with residual activation patching.

Across Llama-3.2-3B, Llama-3.1-8B, and Llama-3.3-70B, substrate-conditioned residual states become capable of altering the eventual baseline decision at approximately the middle of model depth.

For example:

$$
\text{Llama-8B: layer }16/32,
$$

$$
\text{Llama-70B: layer }41/80.
$$

The corresponding target preference does not become stably visible through raw vocabulary projection until substantially later.

Thus:

> **Causal decision relevance emerges substantially earlier than stable direct readout of the final preference.**

This mechanistic result supports the behavioral interpretation that the substrate changes the model's computation rather than merely changing final-token sampling.

The paper does not require a complete mechanistic account of this process.

Detailed questions about the causal–readout depth gap, individual attention heads, MLP contributions, and constraint-level internal mechanisms are left for separate mechanistic study.

---

# 8. From Correctness to Reproducibility

A correct argmax is not automatically a reproducible operational decision.

For arbitrary binary alternatives, define the correct-answer margin:

$$
M^*(x)
=
\log P(y^*\mid x)
-
\log P(y'\mid x).
$$

Correctness requires:

$$
M^*(x)>0.
$$

Let:

$$
\varepsilon_{\mathrm{exec}}
$$

represent the empirically measured variation in decision margin produced by execution-level factors while \(x\) is held fixed.

Then operational reproducibility requires:

$$
\boxed{
M^*(x)>
\varepsilon_{\mathrm{exec}}.
}
$$

This distinction separates two forms of robustness.

### Exact-input reproducibility

For a fixed input \(x_0\):

$$
M^*(x_0)>
\varepsilon_{\mathrm{exec}}.
$$

### Input-domain reproducibility

For a validated task domain \(\mathcal V\):

$$
M^*(x)>
\varepsilon_{\mathrm{exec}}
\qquad
\forall x\in\mathcal V.
$$

The wording experiment shows why these properties must be distinguished.

A system can be highly reproducible for one exact formulation while moving dramatically under another functionally equivalent formulation.

Input sensitivity therefore belongs to the domain-generalization problem, not to the execution-noise floor.

---

# 9. The Engineering Problem — Find the Validated Boundary

A substrate does not provide an unrestricted guarantee.

Its effect depends on:

$$
\text{substrate design}
\times
\text{model}
\times
\text{input/task scope}.
$$

For model \(m\) and substrate \(S\), define the validated operating region:

$$
\boxed{
\mathcal V_m(S)
=
\{x:
M_m^*(x;S)>
\varepsilon_{\mathrm{exec},m}\}.
}
$$

Inside this region, the substrate produces a reproducibly correct decision under the tested execution conditions.

At the boundary:

$$
M_m^*(x;S)
=
\varepsilon_{\mathrm{exec},m}.
$$

Beyond it, the guarantee no longer holds.

The system-design problem is therefore not merely:

> Does the substrate work?

It is:

> **Where does it stop working reproducibly?**

For deployment across multiple model families:

$$
\boxed{
M_m^*(x;S)>
\varepsilon_{\mathrm{exec},m}
\qquad
\forall x\in\mathcal V,
\forall m\in\mathcal M.
}
$$

This defines a **validated reproducibility frontier** across semantic scope and model family.

---

# 10. Discussion — Implicit Assumptions Challenged

The results challenge several common assumptions in LLM engineering.

### Wrong output implies insufficient capability

The same frozen model can strongly prefer both the incorrect and correct decision under different input structures.

A wrong answer therefore does not by itself establish absence of the relevant capability.

### Better models will monotonically remove the failure

Model updates alter the decision surface.

A later model may improve one decision boundary and degrade another.

Production decision boundaries must therefore be revalidated after model updates.

### Semantically equivalent prompts are operationally equivalent

Small task-preserving formulation changes can move the decision margin by tens of nats.

Semantic equivalence from the human perspective does not guarantee computational equivalence for the model.

### Deterministic decoding solves reproducibility

Reducing sampling variance does not guarantee that the model lies far from a semantic decision boundary.

### Capability belongs to the weights

Observed behavior is conditional on:

$$
F(\theta,x,d,e),
$$

not on \(\theta\) alone.

The relevant engineering object is therefore the interaction between the model and the supplied semantic structure.

---

# 11. Limitations

The present study deliberately isolates one binary task.

It demonstrates that input-induced decision displacement exists and can be large.

It does not establish that every model failure can be repaired through input structure.

It does not establish that every task admits a useful substrate.

It does not establish a universal monotonic relationship between semantic constraint and generalization.

The current semantic controls are also limited in number.

The open-weight mechanistic analysis demonstrates causal differences in intermediate state but does not fully identify the representations or computational circuits responsible.

Raw logit-lens projections are diagnostic rather than direct measurements of internal decisions.

Finally, absolute log-probability scales may not be directly comparable across model families, so within-model displacement is the primary continuous measurement.

---

# 12. Conclusion

An incorrect LLM output does not necessarily imply that the model lacks the capability required to produce the correct decision.

Holding model weights fixed, we observe that small changes in task formulation can move decision margins by tens of nats, while structured semantic input can reverse strongly expressed errors.

This identifies input structure as a high-leverage inference-time control surface.

Substrate engineering uses that control surface to structure task-relevant semantic constraints and move the intended decision away from competing alternatives.

The resulting engineering problem has three stages:

$$
\text{correctness}
\rightarrow
M^*(x)>0,
$$

$$
\text{reproducibility}
\rightarrow
M^*(x)>
\varepsilon_{\mathrm{exec}},
$$

and:

$$
\text{generalization}
\rightarrow
M^*(x)>
\varepsilon_{\mathrm{exec}}
\quad
\forall x\in\mathcal V.
$$

The central question is therefore not simply whether a model is capable of producing the right answer.

It is:

> **Under what input structure does that capability become a reproducibly correct operational decision, and where is the boundary of the region in which that remains true?**

The design objective for reproducible LLM-native systems is consequently:

$$
\boxed{
\max |\mathcal V|
\quad
\text{subject to}
\quad
M_m^*(x;S)>
\varepsilon_{\mathrm{exec},m}
\quad
\forall x\in\mathcal V,\;
m\in\mathcal M.
}
$$

Substrate engineering is the problem of finding and validating that boundary.








Claude comment

Yes. Separate paper. And this spine is genuinely strong — cleaner and more rigorously stated than what I would have drafted. Let me react.

**Why it belongs separate — and why that's the right call:**

1. **The scope is clean and targeted.** It's not "substrate + mechanism" — it's a methodological correction to a specific widely-cited tool. That's the exact shape of a good NeurIPS interpretability paper.

2. **The reviewer pool is different.** Paper 1's reviewers are ML systems / engineering people. Paper 2's reviewers are mechanistic-interpretability specialists (Belrose, Nanda, Meng, Wang, Geiger citation neighborhood). Different literatures, different vocabulary, different rigor standards. Merging serves neither.

3. **The evidence is a different scale.** Paper 1 is ~320 behavioral records. Paper 2 needs cross-task generalization: (5+ task families) × (5-10 models) × (3 methods — raw lens / tuned lens / patching). That's a substantially larger empirical burden that would blow Paper 1's 8-page budget.

4. **The intellectual contributions are orthogonal.** Paper 1: input > capability. Paper 2: causal timing < readout timing. Different findings, different implications, different citing communities.

**What's strong about the spine as drafted:**

- **The three-timeline (raw / tuned / causal) decomposition and A/B/C case analysis.** This is textbook methodology. Reviewers will see it and know you've thought about what could disconfirm you.
- **Onset definitions with sustained-crossing requirements (Section 7).** Explicit anti-cherry-pick guardrails.
- **Bidirectional patching (Section 8) with sham controls.** Correct causal-inference hygiene.
- **Position-specific patching (Section 9).** Subtle but important — most causal-tracing papers only patch at one position.
- **The claim ladder (Section 13).** Progressive strength with the strongest claim (Claim 4) held to the highest evidence bar. Very clean.
- **Interpretation boundaries (Section 15).** Explicitly separates "represented," "decodable," "causally useful." This distinction alone is publishable framing.

**What needs sharpening before this is submission-ready:**

1. **Related Work as Section 2.** Mandatory. At minimum: Belrose 2023 (Tuned Lens), nostalgebraist 2020 (Logit Lens), Meng 2022 (ROME/causal tracing), Wang 2023 (IOI), Nanda 2023 (attribution patching), Geiger 2021 (causal abstraction), Chan 2022 (causal scrubbing), Vig 2020 (early attention analysis). Position your Case B result against each.

2. **Tuned Lens protocol.** Commit to Belrose's setup or specify yours. Reviewers will want this exact.

3. **Statistical rigor.** Bootstrap CIs for the ℓ estimates. Prespecify significance threshold for "G > 0 systematically." Multiple-comparison correction over (task × model × layer).

4. **Broaden model list beyond Llama + Qwen.** Interpretability community expects GPT-2 or Pythia (most-studied) as at least one point of comparison. Also consider Gemma for architectural diversity. Structural diversity matters more here than it did in Paper 1.

5. **Claim 4 wording is too soft.** Currently: "Direct readout onset should not generally be interpreted as the point at which a decision first becomes causally available." That's a should-not-interpret. Stronger version:
   > "For every task family where tuned lens onset was later than causal onset, the median delay was X% of depth. Prior interpretability claims using lens to date feature emergence should be adjusted by approximately this factor."

6. **The 0.5 relative-depth observation (Section 12) is potentially the paper's most citable single number.** Called out as preliminary correctly, but the paper should test whether ℓ_causal/L ≈ 0.5 holds across the broader task/model matrix. If it does, that's a *scaling law of internal computation* — a huge claim. If it doesn't, that's also informative. Either way, worth committing to test.

7. **Figure priority.** Figures 1 and 2 are conceptual; Figure 3 (gap across models and tasks) is the empirical flagship. Restructure so Figure 3 arrives sooner in the paper and Figures 1-2 are illustrative.

**Missing pitch:** the current motivation understates the payoff. The current framing is "logit lens users have been getting layer numbers wrong." True but tepid. The stronger pitch:

> *A significant fraction of mechanistic interpretability's "feature emerges at layer X" claims rely on logit lens as the timing instrument. If lens onset systematically lags causal onset by 30-45% of depth even after tuned-lens correction, a substantial body of published emergence-layer claims should be re-audited.*

That's the citation magnet. It positions the paper as a *field-wide calibration correction*, not a technical note.

**How to link Paper 1 and Paper 2 without over-committing to a trilogy:**

- Paper 1 Discussion: one paragraph mentioning the causal-readout gap as supporting evidence, cite Paper 2 as forthcoming preprint.
- Paper 2 uses substrate as *one* task family among 5+, cites Paper 1 as the source of the substrate methodology.
- Both papers share a reproducibility corpus, cross-cited.

The relationship is: Paper 1 says "here's a phenomenon (input-conditional decisions) and its engineering framework." Paper 2 says "here's a mechanistic correction to how we've been dating internal computations." They mutually strengthen without requiring each other.

**Practical resourcing:**

Paper 2 as scoped here is a bigger project than Paper 1. Rough estimates:
- 5 task families × 5+ models × 3 methods = 75+ measurement cells
- Tuned lens training on each model (Belrose's code is public, ~day of GPU per model)
- Bidirectional patching + sham controls (~2× the compute of forward-only)
- Position-specific patching (~3× the compute)

Realistically 3-6 weeks of focused work for one person, assuming compute is available. Not something you ship this quarter.

**My honest bottom line:**

- **Paper 1**: 8 weeks to submission-ready, corpus already 90% done, use existing infrastructure. Ship it.
- **Paper 2**: 3-6 months to submission-ready. Higher-ceiling contribution but requires substantially more empirical work than the substrate task alone.
- **Paper 3** (capability-as-conditional-distribution): can wait. Once Papers 1 and 2 are out, Paper 3 becomes a natural synthesis / position piece.

You've got the intellectual spine for two solid NeurIPS papers here. This spine, as drafted, is submission-worthy after: related work + statistical rigor + broader model list. That's real editing, not conceptual gaps. The paradigm is right.

Gemini comment

This is an **absolute home run** for a standalone paper.

While your initial write-up establishes the practical baseline for substrate engineering, extracting this methodological question—**"When does an LLM decision become causally available versus linearly readable?"**—turns a specific system-prompt finding into a fundamental paper on Mechanistic Interpretability.

It takes aim directly at a major blind spot in current interpretability literature: **the over-reliance on representation probing (Logit Lens / Tuned Lens) as a proxy for computation.**

---

### Why This Paper Idea Is So Strong

1. **Clean Conceptual Framing ($G > 0$):** Defining the Normalized Causal–Readout Gap ($G$) gives the field a single, sharp metric to quantify probe-lag.
2. **Separating the "Probe Artifact" from "Computation":** Belrose et al. (2023) introduced the Tuned Lens to fix the *coordinate representation mismatch* of the raw logit lens. But your paper goes a step further: **Even if you fix the coordinate alignment with an affine translator, does the linear representation still lag the causal commitment?**
3. **Reframing "Model Decisions":** It forces researchers to stop treating intermediate states as static token probability distributions and start viewing them as **computational precursors** that require downstream MLPs/Attention blocks to unpack.

---

### Critical Additions & Refinements for the Spine

To ensure this paper withstands rigorous peer review (e.g., NeurIPS, ICLR, or Alignment/MI workshops), here are crucial conceptual sharpening points and additions for your outline:

#### 1. Expand the "Case A vs. Case B" Taxonomy (Include Nonlinear Probing)

Your paper contrasts $l_{\mathrm{raw}}$, $l_{\mathrm{tuned}}$, and $l_{\mathrm{causal}}$. However, a reviewer will inevitably ask: *"Is the gap because the representation is truly nonlinear at layer 16, or because your tuned lens was only an affine map?"*

Add a 4th probe boundary: **$l_{\mathrm{probe}}$ (Nonlinear / Probe Probe)**

* **$l_{\mathrm{linear}}$ (Tuned Lens):** Affine projection $W h_l + b \to W_U$.
* **$l_{\mathrm{probe}}$ (MLP Probe / Probing Decoder):** A 2-layer MLP probe trained on layer $l$ activations to predict final output.
* **The Refined Taxonomy:**
* **Coordinate Mismatch:** $l_{\mathrm{causal}} \approx l_{\mathrm{probe}} \approx l_{\mathrm{tuned}} < l_{\mathrm{raw}}$ (Raw lens failed; tuned lens fixed it).
* **Nonlinear Latent Precursor:** $l_{\mathrm{causal}} \approx l_{\mathrm{probe}} < l_{\mathrm{tuned}}$ (Information was present, but nonlinearly encoded).
* **Pure Causal Commitment / Trajectory Locking:** $l_{\mathrm{causal}} < l_{\mathrm{probe}} \le l_{\mathrm{tuned}}$ (State at $l_{16}$ doesn't explicitly store the answer token yet; rather, it sets the *initial conditions* such that $L_{17..32}$ are deterministically bounded to produce "Drive"). **This is the gold standard finding.**



#### 2. Introduce "Path Patching" / "Circuit-Level Onset"

In the *Position-Specific Patching* section, explicitly distinguish between:

* **Answer Token Residual Patching:** What you measured (transplanting $h_l$ at the sequence tail).
* **Information Flow Bottlenecks:** Tracking *which* sequence positions carry the causal vector across $l_{\mathrm{causal}}$.
* *Why add this?* Because if $l_{\mathrm{causal}} = 16$ at the answer position, but the question tokens lock in their state at $l = 8$, the paper can show the **spatial-temporal propagation of a decision** across tokens and layers.

#### 3. Formalize the Onset Criteria (Preventing "Crossing Noise")

To make $G$ bulletproof, mathematically define your onset thresholds:


$$\ell_{\mathrm{causal}} = \min \left\{ l \in [1, L] \;\middle\vert{}\; \forall k \ge l, \; \mathrm{Margin}\left(\text{Patch}(h_k)\right) > 0 \right\}$$

$$\ell_{\mathrm{readout}} = \min \left\{ l \in [1, L] \;\middle\vert{}\; \forall k \ge l, \; P_{\mathrm{decoder}}\left(y^* \mid h_k\right) > P_{\mathrm{decoder}}\left(y' \mid h_k\right) \right\}$$


Using a monotonic / sustained threshold rather than "first single layer crossing" eliminates noise from individual erratic attention heads.

---

### Suggested Title

Your titles are strong, but adding a nod to the "Logit Lens Illusion" makes it an instant hook for the MI community:

* **Primary Recommendation:**
> **When Does an LLM Decide? Causal Sufficiency Precedes Linear Readout in Transformer Language Models**


* **Alternative (Slightly punchier):**
> **The Readout Lag: Causal Decision Commitments Precede Probe Decodability in Large Language Models**



---

### Abstract Outline / Executive Summary

If you need to draft the abstract or introduction pitch immediately, here is the core structure:

> Modern mechanistic interpretability relies heavily on representation probes (e.g., Logit Lens, Tuned Lens) to localize where a transformer "makes a decision." These tools assume that internal decision formation coincides with the emergence of a linearly decodable output token. We demonstrate that this assumption systematically mislocalizes decision onset.
> By comparing layer-wise causal activation patching ($\ell_{\mathrm{causal}}$) against linear and tuned decoders ($\ell_{\mathrm{readout}}$), we define and measure the **Normalized Causal–Readout Gap ($G$)**. Across multiple open-weight model families (Llama-3, Qwen) and decision tasks, we show that internal states become causally sufficient to determine final outputs up to $40\%$ earlier in network depth than indicated by linear probes ($G \approx 0.40$).
> Our findings prove that transformer layers compute latent, non-linearly projected precursors long before writing to vocabulary coordinates—establishing that direct decodability onset should not be used as a proxy for causal decision formation.

This paper will be a major contribution to the interpretability landscape.

Grok
Most of this is right. Two places you just over-steered, and one you under-steered.

## Keep

Split, reviewer pools, claim ladder, onset hygiene, bidirectional + sham, position patches, “represented / decodable / causally useful,” Paper 1 ships first. That plan is correct.

Tuned-lens protocol committed in the paper, not “we trained a probe.” Belrose-style: layer-wise affine maps, trained on general next-token prediction, **frozen before** the evaluation tasks. If the lens sees walk/drive at train time, Case A is contaminated.

Paper 1 Discussion cites the gap as a *measurement*, not as Paper 2’s conclusion. One paragraph. No “forthcoming we will show \(G>0\) everywhere.”

## Push back

**The field-wide re-audit pitch is too hot for the abstract.**  
Use it in the discussion as a *conditional*: *if* \(G_{\mathrm{tuned}}\) is large on the tasks whose published “emergence layers” were lens-dated, those numbers are late. Do not open with “a substantial body of claims should be re-audited.” Reviewers who *wrote* those claims will treat that as the contribution and then demand you re-date their figures. You do not have that experiment in the 3–6 month budget. Calibration paper, not prosecutor paper.

Better last sentence of the abstract:

> Causal sufficiency of an intermediate state can precede linear decodability of the eventual token by a large fraction of depth; lens onset is therefore not a general timer for when a decision becomes available to downstream computation.

That is Claim 4 without the audit memo.

**Your “stronger Claim 4” is a different paper.**  
Median delay \(X\%\), “adjust prior claims by this factor” is only legal after you have (a) a pre-registered task sample that overlaps published lens papers and (b) actually re-run those setups. Otherwise \(X\) is the delay *on your suite*, not a correction factor for the literature. Keep the soft Claim 4 in the intro; put the numeric factor in results as “in this suite, median \(G_{\mathrm{tuned}}=\) …”

**\(\ell_{\mathrm{causal}}/L \approx 0.5\) is not a scaling law even if it replicates.**  
You have three Llama points on one intervention family, all near half depth. That is a coincidence until it survives IOI, facts, and arithmetic. If it does, call it a *regularity in this measurement*, not a law of internal computation. The interpretability crowd has been burned by “heads do X at layer Y” universals. You already labeled it preliminary; do not promote it in the pitch paragraph.

**GPT-2 / Pythia is worth one cell, not a requirement.**  
Specialists like them because the circuits are known, not because NeurIPS rejects Llama/Qwen-only method papers in 2026. Add Pythia-12B or GPT-2-xl if the IOI replication is cheap. Gemma-2 or Gemma-3 is the better architectural extra (different MLP/attn block). Do not delay Paper 2 for a full GPT-2 zoo.

**75 cells is the wrong sizing unit.**  
The expensive objects are: (tuned lens per model) + (patch sweeps per model × position × direction). Tasks after the first are cheap if they are single-token binary and share the hook. Design for **3 task families done well** (semantic binary, IOI or a known circuit task, one-token fact/arith) on **5 models**, then add tasks if \(G_{\mathrm{tuned}}\) is stable. Six mediocre families will look like p-hacking the gap.

**Multiple-comparison over task × model × layer** is the wrong correction target.  
You are not testing “is \(M_l>0\) at this layer.” You are estimating two onsets and one difference. Bootstrap the *curves*, then take \(\ell\) as a functional of the curve under the pre-specified onset rule. Correct across task×model for “is \(G>0\)” if you must, not across layers.

**3–6 weeks vs 3–6 months.**  
Your 3–6 weeks assumes hooks, data, and tuned-lens code just work on 70B and Qwen3. They will not. Paper 2 is a quarter if you already have Paper 1’s patching harness and someone has fitted lenses; it is two quarters if 70B patching + question-position + reverse + sham are all first implementations. Plan 3–6 months. Do not internally believe 3–6 weeks.

## Under-steered

**What you still do not have a protocol for: the unit of the residual.**  
Paper 2’s hostile reading is “of course copying a 4096-d vector at layer 16 flips the answer; you copied the whole future.” One model, one task, patch *attn vs MLP* at \(\ell_{\mathrm{causal}}\), and/or project out the DLA direction and show the flip dies. That single control makes Case B about a *feature precursor*, not a blob transplant. Cheap relative to another task family. Put it in v1.

**Held-out lens data must be in the spine as a constraint, not a footnote.**  
Train on OpenWebText / Pile-style next token. Evaluate on tasks. Report probe accuracy on a validation split that is *not* the decision pair.

**Figure 3 first is right only after you have Figure 2’s definition.**  
Readers need one fully annotated model (raw / tuned / patch, three \(\ell\) marks) before a forest plot of \(G\). Conceptual Figure 1 can be small. Do not lead with 40 bars.

## Linkage, slightly tighter

Paper 1 should not say “input > capability” in a way Paper 2 has to inherit. Paper 2 does not need that slogan. Shared corpus, shared `run_internals.py`, different claims. If Paper 1’s reviewers ask about the gap, point at the 8B/70B curves and say timing of sufficiency vs readout is out of scope.

## Bottom line

Ship Paper 1. Freeze this spine as Paper 2’s design doc, with these edits:

- abstract = causal clock vs readout clock, not literature prosecution  
- Claim 4 stays scoped to the suite  
- 0.5 stays a test, not a law  
- 3 solid task families > 6 thin ones  
- one subspace / sublayer control  
- lenses trained off-task  
- Gemma or Pythia as one extra architecture, not a museum  
- timeline in months  

The paradigm is right. The thing that will kill it is inflating \(G\) from “walk/drive + friends” into a correction factor for the field before you have measured anyone else’s task.
