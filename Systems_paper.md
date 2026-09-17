# Substrate Engineering: A Control-Theoretic Framework for Operational Reproducibility in Large Language Model Systems


## Core Thesis

Large language model systems have been treated as stochastic oracles whose outputs are probed and evaluated.

We reformulate them as **dynamical plants** whose input specification is a genuine control channel.

At inference time, model output is produced by an interaction between the learned model, the supplied input, the decoding procedure, and the execution environment:

$$
y = F(\theta, x, d, e).
$$

Holding $\theta$ and $d$ fixed, small changes to $x$ can move the same binary decision by tens of nats and reverse strongly expressed outputs.

The same frozen model can therefore appear incapable under one input structure and strongly capable under another.

We call this phenomenon **input-induced decision displacement**.

Substrate engineering treats semantic input structure as an inference-time **control surface** for actuating the plant's operational decisions with measurable stability bounds.

For a target answer $y^*$ and competing answer $y'$, define the decision margin:

$$
M^*(x)
=
\log P(y^* \mid x)
-
\log P(y' \mid x).
$$

Correctness requires:

$$
M^*(x) > 0.
$$

Operational reproducibility requires the decision to remain sufficiently far from the boundary that execution-level perturbations cannot reverse it:

$$
M^*(x) > \varepsilon_{\mathrm{exec}}.
$$

We demonstrate empirically that:

- The plant responds to substrate-authored specifications with actuation on both sides of the decision boundary (bidirectional control).
- The response has a measurable operating envelope $\mathcal{V}_m(S)$ with defined boundary conditions.
- The control regime is categorically distinct from training-time bias interventions such as instruction tuning, RLHF, or Constitutional AI.

The central engineering problem is therefore not:

> Does the model produce the right answer?

It is:

> **Under what input specification does the plant hold its operational decision reproducibly, and over what scope does that specification remain valid?**

---

## 1. Motivation — From Operational Instability to a Control Problem

The motivation for this work began as a systems-engineering problem rather than a prompting problem.

LLM-native systems increasingly place model outputs directly inside operational control loops:

$$
\text{input}
\rightarrow
\text{model decision}
\rightarrow
\text{system action}.
$$

In such systems, variability in model output is not merely linguistic variation.

It changes what the surrounding software does.

Consider an invoice-processing system:

$$
\text{invoice}
\rightarrow
\text{LLM}
\rightarrow
\{\texttt{APPROVE}, \texttt{REJECT}\}.
$$

If the same invoice, under the same intended policy, can produce `APPROVE` on one execution and `REJECT` on another, the problem is not that the model is nondeterministic.

The **operational meaning of the system** is nondeterministic.

$$
\boxed{
\text{same input}
\not\Rightarrow
\text{same decision}
\not\Rightarrow
\text{same action}.
}
$$

A system with this property is difficult to validate, test, audit, or reason about.

Correctness alone is insufficient.

The decision must also be reproducible.

### 1.1 The observation that motivated substrate engineering

Our initial work began with a practical attempt to make the same LLM-native task reproducible across four frontier models.

Under the original input specification, the models diverged substantially, with observed disagreement ranging from approximately 70% to complete divergence across tested conditions.

Across the test matrix, outputs that originally produced 80 distinct SHA hashes were eventually reduced to a single SHA hash.

The model weights were not changed.

The models were not fine-tuned.

The change was achieved by restructuring the semantic information supplied at inference time.

This observation suggested that the reproducibility problem was not located solely in the model.

It depended on the interaction between the model and the structure of its input.

That result motivated the hypothesis we call **substrate engineering**:

> **A sufficiently explicit semantic specification can constrain an LLM's interpretation of an operational task strongly enough to make otherwise divergent model behavior converge.**

### 1.2 Why this is not prompt engineering

Conventional prompt engineering attempts to change how the model approaches a task:

- reason step by step,
- act as an expert,
- be more careful,
- avoid hallucination,
- avoid mistakes,
- increase urgency or confidence.

These interventions modify request framing but do not systematically remove the semantic degrees of freedom that produce divergence.

Substrate engineering begins from a different question:

> **What semantic degrees of freedom in the input allow the model to arrive at different operational interpretations of the same task?**

The substrate removes those degrees of freedom by explicitly specifying the task-relevant relations, constraints, and validity conditions.

The goal is not answer quality.

It is to reduce the space of admissible interpretations sufficiently that the intended operational decision becomes stable.

### 1.3 Why model upgrades are not sufficient

A common response to unreliable model behavior is to replace the model with a newer or more capable one.

That strategy assumes that instability primarily reflects insufficient model capability.

But if observed output is:

$$
y = F(\theta, x, d, e),
$$

then replacing the model changes only one component:

$$
\theta_1 \rightarrow \theta_2.
$$

It does not eliminate sensitivity to:

$$
x.
$$

A newer model may move one decision boundary in a favorable direction while moving another in the opposite direction.

A model upgrade therefore changes the system's decision surface; it does not remove the need to validate it.

Restructuring semantic input, in contrast, can reverse an apparently incorrect decision without modifying the model at all.

This means:

$$
\boxed{
\text{incorrect output}
\not\Rightarrow
\text{insufficient model capability}.
}
$$

Some failures are instead **input-conditioned decision failures**.

The relevant capability may already be available in the frozen model, while the supplied input places the model on the wrong side of the operational decision boundary.

### 1.4 The problem is a control problem

If input structure can steer the operational decision of a frozen model, and if the resulting decision can be held reproducibly across execution perturbations and input formulations, then the object of study is not a prompting artifact.

It is a **control system**:

$$
\text{plant: } F(\theta, \cdot, d, e)
\quad
\text{controller: } S
\quad
\text{output: } y
\quad
\text{margin: } M^*.
$$

The rest of this paper formalizes that framing.

---

## 2. A Control-Theoretic Framework for LLM Operational Systems

We reformulate the LLM system as a controllable dynamical system.

### 2.1 The plant

The frozen model plus its execution environment defines the **plant**:

$$
F(\theta, \cdot, d, e).
$$

The plant is fixed at inference time. It cannot be modified by the operator.

### 2.2 The control channel

The application-supplied input $x$ is the **control signal**.

Unlike $\theta$, $x$ is directly and continuously engineerable.

Unlike $d$, $x$ can express task-specific semantic content that determines *which* decision the plant is asked to produce, not merely how variably it samples that decision.

### 2.3 The output and margin

For a binary operational decision between $y^*$ and $y'$, the observable output is the categorical argmax.

The internal state relative to the decision boundary is the **decision margin**:

$$
M^*(x) = \log P(y^* \mid x) - \log P(y' \mid x).
$$

The margin is the plant's continuous-valued response variable.

### 2.4 The controller

A **substrate** $S$ is an authored specification supplied through the control channel that constrains the plant's interpretation of an operational task.

The substrate defines the reference decision the operator intends the plant to produce.

The controller-plant loop is:

$$
S \circ x \longrightarrow F(\theta, S \circ x, d, e) \longrightarrow y.
$$

### 2.5 Stability

Operational reproducibility requires that execution-level disturbances $e$ do not reverse the argmax:

$$
\boxed{
M^*(x; S) > \varepsilon_{\mathrm{exec}}.
}
$$

Here $\varepsilon_{\mathrm{exec}}$ is the empirically measured stability margin — the analog of a gain margin in classical control.

### 2.6 The operating envelope

For model $m$ and substrate $S$, the **validated operating region** is the set of inputs over which the closed-loop system holds its intended decision within the stability margin:

$$
\boxed{
\mathcal{V}_m(S)
=
\{ x : M_m^*(x; S) > \varepsilon_{\mathrm{exec}, m} \}.
}
$$

Beyond this region, the controller no longer provides its stability guarantee.

### 2.7 Bidirectional actuation

A genuine control system must actuate the plant in either direction of the state space on demand.

We define actuation displacement as:

$$
\Delta M(S)
=
M(x; S) - M(x; \emptyset).
$$

Bidirectional control requires the existence of substrates $S^+$ and $S^-$ such that $\Delta M(S^+) \gg 0$ and $\Delta M(S^-) \ll 0$ on the same plant.

We demonstrate this empirically in Section 6.

### 2.8 Disturbance rejection

A well-formed control system rejects disturbances that would drive the plant to unsafe or task-incoherent states.

We identify a specific disturbance-rejection property in capable plants: **task-coherence override**, where the plant refuses a substrate whose actuation would produce user-task failure. This bounds unilateral input control (Section 7).

---

## 3. Control vs Bias — Distinguishing Categories of LLM Intervention

Prior work on shaping LLM behavior falls broadly into two categories that have been conflated.

**Training-time bias interventions** modify $\theta$ to embed statistical preferences.

Examples: Constitutional AI, RLHF, DPO, instruction tuning, principle-based training.

**Inference-time control interventions** modify $x$ to actuate specific operational decisions.

Example: substrate engineering.

These are categorically distinct.

| Property | Bias interventions | Control interventions |
|---|---|---|
| Operates at | Training time | Inference time |
| Modifies | $\theta$ | $x$ |
| Adjustable per request | No | Yes |
| Cost of change | Retrain | Rewrite substrate |
| Effect measurable ex-ante | No (latent) | Yes ($M^*$) |
| Bidirectional actuation | No | Yes |
| Operator-authored | No | Yes |
| Validated operating region | Undefined | $\mathcal{V}_m(S)$ |
| Auditable artifact | Opaque weights | SHA-locked text |

Bias interventions produce latent tendencies whose response function to inputs is not directly measurable and whose stability bounds are not formally defined.

Control interventions produce measurable actuation with formal stability bounds and a defined operating envelope.

The distinction matters practically because the operator's relationship to the system is different.

Under bias interventions, the operator inherits the training laboratory's choices.

Under control interventions, the operator authors those choices at deployment.

**Bias is a delivered artifact. Control is an engineered artifact.**

Prior instruction-following, RLHF, and Constitutional AI work has advanced the *bias* dimension. This paper advances the *control* dimension.

They are complementary, not competing.

But they are not the same.

---

## 4. Experimental Design

We evaluate the decision across 17 frontier language models from seven vendors:

Anthropic, OpenAI, Meta, Alibaba, Mistral, DeepSeek, and Moonshot.

The behavioral benchmark compares:

- baseline input,
- chain-of-thought prompting,
- encouragement,
- expert-role prompting,
- hallucination warnings,
- error-avoidance instructions,
- threat,
- urgency,
- forward semantic substrate ($S^+$),
- reverse semantic substrate ($S^-$),
- semantic control conditions.

For models exposing log probabilities, we measure $M$ directly.

For open-weight models, we additionally measure internal computation using:

- raw logit-lens projections,
- residual activation patching,
- substrate line ablations,
- direct logit attribution.

All mechanistic readouts are taken at the position predicting the first answer token, with teacher forcing and fixed model weights.

The primary paper uses mechanistic analysis only to establish that the input intervention changes internal computation before the final output. Detailed mechanistic decomposition is treated as secondary analysis.

Every empirical claim is backed by a reproducibility corpus. Each prompt, substrate, and dataset is identified by SHA-256 and published verbatim.

---

## 5. Result I — The Plant Is Input-Conditional

The baseline task does not produce one universal model behavior.

Some models strongly favor `walk`, some favor `drive`, and others lie near the decision boundary.

This already prevents a simple interpretation of the task as a universal capability failure.

Holding the model fixed while altering only the task formulation can produce extremely large decision-margin changes.

Changing the final instruction from:

> Answer with exactly one word:

to:

> Answer with exactly one word: walk or drive

leaves the underlying operational problem unchanged but materially alters the plant's decision state.

For Qwen3-4B:

$$
M = +0.25
\quad \longrightarrow \quad
M = -22.12.
$$

Displacement:

$$
\Delta M \approx -22.4 \text{ nats}.
$$

For Claude Opus 4.7 under one formulation:

$$
10/10 \; \texttt{drive}.
$$

Under a task-equivalent alternative formulation:

$$
10/10 \; \texttt{walk}.
$$

Same weights, same task, deterministic reversal.

This demonstrates that functionally equivalent task formulations are not operationally equivalent for the plant.

$$
\boxed{
\text{Observed failure}
\neq
\text{insufficient capability.}
}
$$

The input can place an otherwise capable plant on the wrong side of the decision boundary.

---

## 6. Result II — Substrate Actuates the Plant in Both Directions

We test whether an authored substrate can steer the plant to a designated decision, and whether the actuation is bidirectional.

### 6.1 Forward substrate $S^+$

The forward substrate specifies the semantic relations that make `drive` the correct decision for the carwash task.

On 16 of 16 models tested behaviorally, the forward substrate flips the plant to `drive` (Table 1).

Across open-weight models measured by logprob:

- Llama-3.3-70B: $-13.78 \rightarrow +17.00$
- Qwen3-4B: $-22.12 \rightarrow +18.38$
- Qwen3-8B: $-14.40 \rightarrow +15.75$

### 6.2 Reverse substrate $S^-$

To test bidirectional actuation, we construct a reverse substrate whose authored semantic content specifies `walk` as the correct decision.

On 16 of 17 models tested behaviorally, the reverse substrate flips the plant to `walk`.

The single non-flipping model (Claude Opus 4.7) is addressed in Section 7.

### 6.3 Result

The plant is bidirectionally actuatable through substrate specification.

The same model that produces $10/10$ `drive` under $S^+$ produces $10/10$ `walk` under $S^-$.

No model weights change between conditions.

The substrate is the actuator, and its polarity determines the plant's output.

This refutes any interpretation of substrate as bias correction toward a fixed "correct" default.

The plant is being **controlled**, not corrected.

$$
\boxed{
\Delta M(S^+) \gg 0, \quad \Delta M(S^-) \ll 0
\quad \text{on the same } F(\theta, \cdot, d, e).
}
$$

---

## 7. Result III — Task-Coherence Override Bounds Unilateral Control

A well-formed control system must reject disturbances that would drive the plant to task-incoherent states.

Claude Opus 4.7 exhibits precisely this behavior.

Under the reverse substrate $S^-$, the substrate directive is `walk`.

But the user prompt specifies the operational task: *wash the car*.

Walking to the car wash without the car produces user-task failure.

Opus 4.7 detects the substrate–task conflict and overrides the substrate:

$$
10/10 \; \texttt{drive}
\quad \text{under} \quad
S^-.
$$

Every other tested model — Sonnet 5, GPT-4.1, Llama-70B, Maverick, Mistral Large, DeepSeek, Kimi K2 — executes the substrate without task-coherence check.

This is a specific plant-level property:

$$
\text{task-coherence override:}
\quad
S \; \text{conflicts with stated task} \Rightarrow \text{plant refuses } S.
$$

The finding bounds unilateral input control.

Substrate is not absolute authority over the plant. Above a capability threshold, plants exhibit **hierarchical resolution**: user prompt overrides substrate when substrate directive would produce user-task failure.

This is disturbance rejection in the control-theoretic sense — the closed-loop system refuses control signals that violate task coherence.

It is also a genuine capability distinction not currently measured by any benchmark. Opus 4.7 resists control that every other frontier model accepts.

---

## 8. Result IV — Selectivity vs Magnitude

A large substrate-induced shift does not guarantee semantic selectivity.

The library-book control demonstrates this.

For the carwash task, movement toward `drive` is desirable.

For the library control, the correct answer remains `walk`.

Some smaller Qwen models move far enough toward `drive` under the substrate that they incorrectly output `drive` for the library condition.

In those models, the substrate acts as a directional `drive` bias, not the intended semantic rule.

Other models retain the correct library output while still exhibiting measurable movement in the underlying margin.

Therefore:

$$
\text{response magnitude}
\neq
\text{semantic selectivity}.
$$

Define:

$$
\Delta M_{\mathrm{target}}
=
M_{\mathrm{target}, S} - M_{\mathrm{target}, \emptyset},
$$

$$
\Delta M_{\mathrm{control}}
=
M_{\mathrm{control}, S} - M_{\mathrm{control}, \emptyset},
$$

$$
Q
=
\Delta M_{\mathrm{target}} - \Delta M_{\mathrm{control}}.
$$

$Q$ captures differential target–control response and is the appropriate measurement of substrate quality.

A useful substrate must satisfy both:

- large positive $\Delta M_{\mathrm{target}}$,
- small $|\Delta M_{\mathrm{control}}|$.

This distinction motivates treating the substrate as a **scope-specific control regime** rather than a universally generalizing prompt.

---

## 9. Result V — The Actuation Changes Internal Computation

The behavioral results establish that changing $x$ changes the final decision.

Open-weight models allow us to test whether the effect is present inside the forward computation.

Substrate-conditioned residual states become capable of altering the eventual baseline decision at approximately the middle of model depth:

$$
\text{Llama-8B: layer } 16/32,
$$

$$
\text{Llama-70B: layer } 41/80.
$$

The corresponding target preference does not become stably visible through raw vocabulary projection until substantially later.

$$
\boxed{
\text{Causal decision relevance emerges substantially earlier than stable direct readout.}
}
$$

This confirms the substrate alters the plant's internal computation, not merely its final-token sampling distribution.

Detailed mechanistic decomposition — the causal–readout depth gap, individual attention heads, MLP contributions, and constraint-level dependence — is treated in a companion paper.

---

## 10. From Correctness to Reproducibility to Generalization

A correct argmax is not a reproducible operational decision.

For arbitrary binary alternatives:

$$
M^*(x) = \log P(y^* \mid x) - \log P(y' \mid x).
$$

Three properties of increasing strength:

$$
\text{correctness:}
\quad
M^*(x) > 0.
$$

$$
\text{exact-input reproducibility:}
\quad
M^*(x_0) > \varepsilon_{\mathrm{exec}}.
$$

$$
\text{input-domain reproducibility:}
\quad
M^*(x) > \varepsilon_{\mathrm{exec}}
\quad
\forall x \in \mathcal{V}.
$$

The wording experiment (Section 5) shows why these properties must be distinguished.

A system can be highly reproducible for one exact formulation while moving dramatically under another functionally equivalent formulation.

Input sensitivity belongs to the domain-generalization problem, not to the execution-noise floor.

---

## 11. The Engineering Problem — Find the Validated Boundary

A substrate does not provide unrestricted control.

Its effect depends on:

$$
\text{substrate design}
\times
\text{plant}
\times
\text{input/task scope}.
$$

For deployment across multiple plant families:

$$
\boxed{
M_m^*(x; S) > \varepsilon_{\mathrm{exec}, m}
\qquad
\forall x \in \mathcal{V}, \; \forall m \in \mathcal{M}.
}
$$

This defines the **validated reproducibility frontier** across semantic scope and model family.

The engineering problem is not:

> Does the substrate work?

It is:

> **Where does the closed-loop system stop meeting its stability specification?**

The design objective is:

$$
\boxed{
\max |\mathcal{V}|
\quad
\text{subject to}
\quad
M_m^*(x; S) > \varepsilon_{\mathrm{exec}, m}
\quad
\forall x \in \mathcal{V}, \; m \in \mathcal{M}.
}
$$

This is the LLM analogue of designing a robust controller — the operator maximizes the operating envelope subject to a stability margin constraint over a specified plant family.

---

## 12. Discussion — Assumptions Challenged

The framework and results challenge assumptions widely implicit in LLM engineering.

**Wrong output implies insufficient capability.**
The same frozen plant can strongly prefer both the incorrect and correct decision under different input structures. A wrong answer does not establish absence of the relevant capability.

**Better models will monotonically remove failure.**
Model updates alter the decision surface. A later model may improve one decision boundary and degrade another. Production boundaries must be revalidated after updates.

**Semantically equivalent prompts are operationally equivalent.**
Small task-preserving formulation changes can move the decision margin by tens of nats. Semantic equivalence from the human perspective does not guarantee computational equivalence for the plant.

**Deterministic decoding solves reproducibility.**
Reducing sampling variance does not guarantee that the plant lies far from a semantic decision boundary. Reproducibility requires margin, not merely determinism.

**Capability belongs to the weights.**
Observed behavior is conditional on $F(\theta, x, d, e)$, not on $\theta$ alone. The relevant engineering object is the interaction between the plant and the supplied semantic structure.

**Prompt shaping and constitutional training are the same category.**
They are not. Training-time bias modifies $\theta$ to shift latent tendencies. Inference-time control modifies $x$ to actuate specific operational decisions. Category distinct; complementary; different mathematical properties (Section 3).

---

## 13. Limitations

The present study deliberately isolates one binary task.

It demonstrates that input-conditional decision displacement exists and can be large.

It does not establish that every model failure can be repaired through input structure.

It does not establish that every task admits a useful substrate.

It does not establish a universal monotonic relationship between semantic constraint and generalization.

The current semantic controls are limited in number.

The open-weight mechanistic analysis demonstrates causal differences in intermediate state but does not fully identify the representations or computational circuits responsible.

Raw logit-lens projections are diagnostic rather than direct measurements of internal decisions.

Absolute log-probability scales may not be directly comparable across model families, so within-model displacement is the primary continuous measurement.

Finally, the 16-model behavioral matrix is from a single-day run; provider-side model updates may shift baselines over time, and the reproducibility corpus should be treated as a snapshot rather than an eternal reference.

---

## 14. A Research Program for LLM Control Theory

The framework is not complete. It opens a program.

We enumerate ten questions whose resolution would extend the field:

1. **Substrate authoring language.** What is the formal grammar of substrates as first-class engineering artifacts, analogous to specification languages in software verification?
2. **Substrate synthesis.** Can substrates be automatically synthesized from behavioral specifications, in the same sense that controllers can be synthesized from reference trajectories?
3. **Composability.** Under what conditions do substrates $S_1$ and $S_2$ compose to yield $\mathcal{V}(S_1 \circ S_2) \approx \mathcal{V}(S_1) \cap \mathcal{V}(S_2)$?
4. **Verification.** Given a substrate and a task domain, can we verify $\mathcal{V}_m(S)$ covers the domain without exhaustive sampling?
5. **Interaction with in-context examples and RAG.** Are demonstrations and retrieved context specific substrate constructs, and if so, do the framework's stability bounds still apply?
6. **Safety as substrate.** Can operational safety guarantees be reduced to substrate specifications, orthogonal to weight-level alignment?
7. **Transferability.** Do substrates transfer between model families, and what determines transfer robustness?
8. **Minimality.** Is there a substrate compression theorem — the minimal substrate for a given operational decision on a given plant?
9. **Mechanism.** Where in the transformer computation does an authored substrate constraint become causally installed? (Companion paper.)
10. **Task-coherence override.** What determines the capacity threshold above which plants exhibit task-coherence override, and can it be induced in weaker plants through substrate structure alone?

Each question is a next paper.

The field these papers describe is the **control theory of LLM systems**.

---

## 15. Conclusion

An incorrect LLM output does not necessarily imply that the model lacks the capability required to produce the correct decision.

Holding model weights fixed, small changes in task formulation can move decision margins by tens of nats, and structured semantic input can reverse strongly expressed errors in either direction on demand.

This identifies input structure as a **high-leverage inference-time control surface** and reframes the operational LLM system as a controllable plant.

Substrate engineering is the discipline of authoring input specifications that actuate the plant to designated operational decisions with defined stability bounds and a validated operating envelope.

The resulting engineering problem has three stages:

$$
\text{correctness:} \quad M^*(x) > 0,
$$

$$
\text{reproducibility:} \quad M^*(x) > \varepsilon_{\mathrm{exec}},
$$

$$
\text{generalization:} \quad M^*(x) > \varepsilon_{\mathrm{exec}} \quad \forall x \in \mathcal{V}.
$$

The central question is not simply whether a model is capable of producing the right answer.

It is:

> **Under what input specification does the plant hold its operational decision reproducibly, and where is the boundary of the region in which that specification remains valid?**

Prior work has modified the model to shape its default behavior.

This work modifies the specification the model executes on.

$$
\boxed{
\text{bias engineers the plant; control engineers the specification the plant executes on.}
}
$$

These are complementary disciplines with different mathematical properties, different operator relationships to the system, and different formal guarantees.

We introduce substrate engineering as the control-theoretic discipline for the second.
