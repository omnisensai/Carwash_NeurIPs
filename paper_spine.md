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
