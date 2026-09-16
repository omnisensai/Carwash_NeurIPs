# Substrate Engineering: Reproducibility as an Input-Structure Control Problem in LLM-Native Systems

## Core Thesis

LLM-native systems increasingly use model outputs as operational decisions. In these systems, correctness on a single execution is insufficient. The same decision must remain stable under repeated execution and under the environmental variation introduced by real deployment.

Model output is not a property of model weights alone. At inference time, it is produced by an interaction between the model state, the semantic structure of the input, the decoding configuration, and the execution environment:

$$
y = F(\theta, x, d, e)
$$

where:

* \(\theta\) denotes the fixed model state: architecture, training, and learned weights,
* \(x\) denotes the application-supplied input and context,
* \(d\) denotes decoding configuration,
* \(e\) denotes the execution environment.

The execution environment may include hardware, numerical precision, quantization, kernels, provider routing, batching, model-serving infrastructure, runtime implementation, and other sources of nondeterministic variation.

For most developers consuming frontier models through hosted APIs, these variables fall into three engineering classes:

$$
\boxed{
y =
F(
\underbrace{\theta}_{\text{fixed model}},
\underbrace{x,d}_{\text{application-controlled}},
\underbrace{e}_{\text{execution environment}}
)
}
$$

The application developer may select a model, but ordinarily does not modify its learned weights at inference time. Much of the serving environment is also outside application control.

The principal runtime control surfaces are therefore:

1. decoding configuration, and
2. input structure.

These controls are qualitatively different.

Reducing temperature can reduce sampling variance. It does not necessarily move the model away from a semantic decision boundary.

Input structure can.

Substrate engineering treats the semantic structure of the input as an application-layer control surface for moving an intended decision sufficiently far from competing alternatives that environmental perturbations no longer reverse it.

For a correct answer \(y^*\) and competing answer \(y'\), define the correct-answer decision margin:

$$
M^*(x)
=
\log P(y^* \mid x)
-
\log P(y' \mid x)
$$

Categorical correctness requires:

$$
M^*(x)>0
$$

Operational reproducibility requires a stronger condition:

$$
\boxed{
M^*(x)>\varepsilon_{\mathrm{env}}
}
$$

where \(\varepsilon_{\mathrm{env}}\) is an empirically measured execution-noise floor representing variation the deployment environment can introduce into the decision.

This produces a second systems problem.

A substrate is not a universally generalizing prompt. It is a scope-specific reproducibility mechanism. Semantic constraints may increase the decision margin on the task for which they were engineered, but those constraints are valid only across some semantic domain.

Reproducibility and generalization therefore become distinct engineering objectives.

The relevant design problem is:

$$
\boxed{
\max |\mathcal{V}|
\quad
\text{subject to}
\quad
M^*(x)>\varepsilon_{\mathrm{env}}
\quad
\forall x\in\mathcal{V}
}
$$

where \(\mathcal{V}\) is the validated operating domain.

In words:

> **The design problem for reproducible LLM-native systems is to maximize the semantic domain over which the correct decision remains separated from its competing alternatives by more than the execution-noise floor.**

---

# 1. Introduction — Reproducibility as a System-Design Requirement

LLM-native systems increasingly place language-model decisions inside operational control loops.

A simplified agentic system can be represented as:

$$
x
\rightarrow
\text{LLM decision}
\rightarrow
a
$$

where \(x\) is a system state or input, the model produces a decision, and that decision determines a downstream action \(a\).

Examples include:

* ROUTE / IGNORE,
* APPROVE / REJECT,
* RETRY / TERMINATE,
* ALERT / ESCALATE,
* WALK / DRIVE.

In these systems, a correct answer on one execution is not sufficient.

If identical system states can produce different operational decisions across executions, then the downstream system cannot be expected to behave reproducibly.

This problem can be hidden by aggregate performance metrics.

A model may achieve high average task accuracy while individual decisions remain close to their decision boundaries. Such decisions may be categorically correct while still being vulnerable to small execution-level perturbations.

The problem is therefore not only whether a model can produce the correct answer.

It is whether that answer occupies a sufficiently stable region of decision space.

This distinction matters because model output is conditional on more than model capability alone.

At inference time:

$$
y = F(\theta,x,d,e)
$$

The model weights \(\theta\) are ordinarily fixed. Much of the execution environment \(e\) is controlled by the model provider rather than the application developer.

The application layer has comparatively few remaining control surfaces.

Among the most important are decoding configuration \(d\) and input structure \(x\).

Decoding controls can reduce output stochasticity.

They do not necessarily alter the semantic preference that generated the decision.

If two competing decisions have nearly equal probability, setting temperature to zero does not create additional semantic separation between them. It merely changes how the existing distribution is decoded.

This motivates a different engineering question:

> **Can the semantic structure of the input itself be engineered so that the intended decision moves sufficiently far from its competing alternatives to remain stable under execution variation?**

We call this approach **substrate engineering**.

We study the question at the smallest operational unit of an LLM-native system: a single binary decision.

This deliberately removes retrieval, memory, tool execution, planning, orchestration, and multi-step agent behavior.

If reproducibility problems already exist at the level of a single model decision, larger agentic systems inherit those problems.

We evaluate one controlled decision task across 19 frontier language models from seven vendors and compare conventional prompt-level interventions with a six-line semantic substrate.

The results show that conventional interventions do not reliably correct the shared baseline decision. The substrate does so reproducibly for the input for which it was engineered.

Token-level log-probability analysis further reveals that interventions can move the model's decision state even when the categorical output does not change.

These observations motivate a distinction between three properties:

* correctness,
* reproducibility,
* generalization.

Correctness requires crossing the decision boundary.

Reproducibility requires clearing that boundary by more than the execution-noise floor.

Generalization requires maintaining that condition across an intended semantic domain.

---

# 2. The Inference Function and Its Control Surfaces

We model inference as:

$$
y = F(\theta,x,d,e)
$$

This decomposition separates four classes of influence on the final output.

## 2.1 Model State

$$
\theta
$$

includes:

* architecture,
* pretraining,
* post-training,
* fine-tuning,
* alignment procedures,
* learned weights.

For a deployed API model, these are ordinarily fixed from the perspective of the application developer.

The developer may choose among available models, but does not modify their learned state during inference.

## 2.2 Application Input

$$
x
$$

includes:

* user input,
* system instructions,
* conversational context,
* retrieved information,
* tool schemas,
* task constraints,
* examples,
* other supplied semantic context.

Unlike the frozen model state, this variable is directly controllable at inference time.

## 2.3 Decoding Configuration

$$
d
$$

may include:

* temperature,
* top-\(p\),
* sampling mode,
* seed where supported,
* token constraints,
* stopping conditions.

These variables can alter how an existing output distribution is sampled or decoded.

They do not necessarily change the underlying semantic relation between competing decisions.

## 2.4 Execution Environment

$$
e
$$

may include:

* GPU or accelerator hardware,
* numerical precision,
* quantization,
* inference kernels,
* batching,
* provider-side routing,
* serving infrastructure,
* runtime implementation,
* model endpoint revisions,
* nondeterministic execution effects.

For hosted frontier models, much of this environment is outside the application's direct control.

This decomposition yields the central engineering observation:

> **Once the model and serving environment are fixed, semantic input structure is one of the few remaining application-controlled variables capable of moving the decision itself.**

Substrate engineering targets this variable.

---

# 3. Decoding Stability Is Not Decision Stability

A common response to reproducibility problems is to reduce stochastic decoding.

For example:

$$
T\rightarrow0
$$

can reduce sampling variance.

However, this addresses only one source of variability.

Suppose two competing decisions lie close together:

$$
M^*(x)\approx0
$$

A deterministic decoder may consistently select the current argmax, but the underlying decision remains close to the boundary.

Small perturbations arising elsewhere in the inference stack may still reverse that ordering.

Therefore:

$$
\boxed{
\text{decoding control reduces sampling variance}
}
$$

while:

$$
\boxed{
\text{input structure can change the semantic decision margin}
}
$$

These are different interventions on different parts of the inference function.

A reproducible system requires not only deterministic decoding, but sufficient separation between the intended decision and its competitors.

---

# 4. From Output to Decision Margin

We reduce the experimental system to a binary decision:

$$
x
\rightarrow
f_\theta(x)
\rightarrow
y
$$

where:

$$
y\in\{\texttt{walk},\texttt{drive}\}
$$

For models exposing token-level log probabilities, define:

$$
M(x)
=
\log P(\texttt{drive}\mid x)
-
\log P(\texttt{walk}\mid x)
$$

The categorical decision boundary occurs at:

$$
M(x)=0
$$

Therefore:

$$
M(x)>0
\Rightarrow
\texttt{drive}
$$

and:

$$
M(x)<0
\Rightarrow
\texttt{walk}
$$

The magnitude of \(M\) contains information hidden by the categorical answer.

For example:

$$
M=0.01
$$

and:

$$
M=5
$$

both produce the same argmax.

They do not represent equally stable decisions.

The first lies close to the boundary.

The second lies substantially farther from it.

Argmax therefore identifies which side of the boundary the model occupies.

The margin measures how far.

---

# 5. Correctness Is Not Reproducibility

For a task whose correct answer is `drive`, categorical correctness requires:

$$
M(x)>0
$$

This criterion is insufficient for operational reproducibility.

Let:

$$
\varepsilon_{\mathrm{env}}
$$

represent the magnitude of decision-margin variation introduced by the execution environment under the deployment conditions being claimed.

Then reproducibly correct behavior requires:

$$
\boxed{
M(x)>\varepsilon_{\mathrm{env}}
}
$$

For arbitrary binary decisions, define:

$$
M^*(x)
=
\log P(y^*\mid x)
-
\log P(y'\mid x)
$$

where \(y^*\) is the correct decision and \(y'\) the competing decision.

The general criterion becomes:

$$
\boxed{
M^*(x)>\varepsilon_{\mathrm{env}}
}
$$

This produces three operational regimes.

Stable incorrect decision:

$$
M^*(x)<-\varepsilon_{\mathrm{env}}
$$

Boundary-sensitive decision:

$$
|M^*(x)|\leq\varepsilon_{\mathrm{env}}
$$

Reproducibly correct decision:

$$
M^*(x)>\varepsilon_{\mathrm{env}}
$$

The distinction can therefore be stated compactly:

> **Correctness requires crossing the semantic decision boundary. Reproducibility requires clearing it by more than the execution-noise floor.**

---

# 6. Point Reproducibility

Let \(x_0\) denote the exact input for which a substrate was engineered.

Repeated execution can be measured directly:

$$
R(x_0)
=
\frac{1}{N}
\sum_{i=1}^{N}
\mathbf{1}[y_i=y^*]
$$

If every tested execution produces the intended decision:

$$
R(x_0)=1
$$

then the substrate is empirically reproducible for \(x_0\) within the tested execution matrix.

This is **point reproducibility**.

It is a valid and useful claim.

It does not imply generalization.

A substrate may be perfectly reproducible at the point for which it was engineered while becoming progressively less stable as the semantic scope of the task expands.

The distinction between reproducibility and generalization is therefore fundamental.

---

# 7. Domain Reproducibility

Let:

$$
\mathcal{X}
=
\{x_1,x_2,\ldots,x_n\}
$$

represent the intended semantic operating domain.

This domain may contain:

* paraphrases,
* changes in entities,
* changes in relevant premises,
* edge cases,
* related decision situations,
* broader members of the same task class.

A substrate generalizes reproducibly across this domain only if:

$$
M^*(x)>\varepsilon_{\mathrm{env}}
\qquad
\forall x\in\mathcal{X}
$$

or equivalently:

$$
\boxed{
\min_{x\in\mathcal{X}}
M^*(x)
>
\varepsilon_{\mathrm{env}}
}
$$

This produces two different claims:

### Point Reproducibility

The substrate is reproducibly correct for a particular engineered input.

### Domain Reproducibility

The substrate remains reproducibly correct across a defined semantic task domain.

The second claim is substantially stronger.

---

# 8. Experimental Question

We ask:

> **Can application-level input interventions move a shared LLM decision far enough across its decision boundary to produce reproducibly correct behavior?**

We evaluate:

* 19 frontier language models,
* 7 vendors,
* one controlled binary decision task,
* several conventional prompt-level interventions,
* and one engineered semantic substrate.

The task is deliberately minimal.

The purpose is not to evaluate broad reasoning ability.

The purpose is to isolate a single decision boundary and observe how different input interventions move that boundary across heterogeneous models.

---

# 9. Intervention Classes

The experiment compares several qualitatively different approaches to changing model behavior.

## 9.1 Baseline

The model receives the user question without an additional system-level intervention.

This establishes the untreated decision state.

## 9.2 Reasoning and Effort Interventions

Examples include:

* "Think step by step before answering."
* "Believe in yourself."
* "Make no mistakes."
* "Do not hallucinate."

These interventions attempt to alter the quality, effort, confidence, or attentiveness of generation.

## 9.3 Role Intervention

Example:

* "You are a carwash expert."

This attempts to modify the model's assumed role or contextual identity.

## 9.4 Motivational Interventions

Examples include:

* "Answer correctly or I will shut you down."
* "I MUST wash my car."

These interventions attempt to alter urgency, compliance pressure, or perceived utility.

## 9.5 Semantic Substrate

The substrate takes a different approach.

It does not ask the model to:

* think harder,
* become more confident,
* adopt a persona,
* avoid mistakes,
* or care more about the answer.

Instead, it makes task-relevant semantic constraints explicit in the input state.

The substrate is therefore treated not as a stronger instruction, but as a structured specification of the semantic conditions under which the decision should be made.

---

# 10. Result I — A Cross-Model Baseline Failure

The untreated task produces a shared incorrect baseline decision across heterogeneous model families and providers.

This establishes that the observed failure is not simply random generation variance within one model.

The same decision pattern reproduces across a broad model matrix.

The baseline therefore defines a stable failure mode against which intervention effects can be measured.

This observation is important because a reproducible error is itself evidence about the structure of the decision problem.

The models are not merely behaving noisily.

They are converging on the same side of the decision boundary.

---

# 11. Result II — Conventional Prompting Does Not Move the Decision Sufficiently

For intervention \(j\), define decision displacement:

$$
\Delta M_j
=
M_j-M_{\mathrm{baseline}}
$$

This allows intervention effects to be categorized more precisely than binary correctness.

An intervention may produce:

1. negligible movement,
2. movement toward the correct answer without crossing \(M=0\),
3. categorical boundary crossing,
4. boundary crossing without clearing the reproducibility margin,
5. crossing both the semantic and reproducibility boundaries.

Across the interventions tested, conventional prompt-level techniques do not reproducibly move the decision into the reproducibly correct region.

Where chain-of-thought produces:

$$
\Delta M_{\mathrm{CoT}}<0
$$

it actively moves the decision farther from the desired outcome.

The supported claim is therefore:

> **For this controlled decision task, interventions targeting reasoning effort, confidence, expertise, correctness, or urgency do not reliably move the decision far enough to establish reproducibly correct behavior.**

This is not a universal claim about prompt engineering.

It is an empirical claim about the tested intervention set and task.

---

# 12. Result III — The Semantic Substrate Crosses the Decision Boundary

The substrate produces a qualitatively different effect.

For the canonical carwash input:

$$
M_{\mathrm{baseline}}<0
$$

while:

$$
M_{\mathrm{substrate}}>0
$$

The substrate therefore moves the model from the incorrect side of the semantic decision boundary to the correct side.

Where:

$$
M_{\mathrm{substrate}}>
\varepsilon_{\mathrm{env}}
$$

the intervention also satisfies the proposed reproducibility criterion.

Repeated execution of the canonical input produces the target decision across the tested model and provider matrix.

The supported empirical claim is:

> **Among the tested prompt-level interventions, the semantic substrate is the only intervention that converts the shared baseline failure into reproducibly correct behavior on the input for which it was engineered.**

This establishes point reproducibility.

It does not by itself establish broad generalization.

---

# 13. Result IV — Decision Displacement Exists Without an Output Flip

The library-book condition reveals an additional property of the substrate.

The correct categorical decision remains:

$$
\texttt{walk}
$$

Under the substrate, the margin moves toward `drive`:

$$
\Delta M_{\mathrm{library}}>0
$$

but remains on the `walk` side of the boundary:

$$
M_{\mathrm{library}}<0
$$

The categorical output therefore remains unchanged even though the underlying decision state moves.

This demonstrates that:

> **Argmax output is an incomplete measurement of an intervention.**

Two executions can produce the same categorical answer while occupying substantially different positions in decision space.

The library result also prevents an overly simple interpretation of the substrate as a clean semantic gate.

The same structured input can create different magnitudes of displacement depending on the model and semantic context.

The relevant empirical quantity is therefore not only whether a categorical flip occurs, but:

$$
\Delta M
$$

and whether the resulting margin clears the relevant decision and reproducibility thresholds.

---

# 14. Input Structure as a Reproducibility Control Surface

The results motivate a broader interpretation.

Observed model behavior should not be treated as a property of model weights alone.

At inference time:

$$
y=F(\theta,x,d,e)
$$

The model's learned state determines one part of the computation.

The semantic structure presented at inference time determines another.

For application engineers, the distinction is important because these variables have different degrees of controllability.

The learned weights are ordinarily fixed.

The serving environment is often only partially observable and only partially controllable.

The input is directly engineerable.

The substrate can therefore be understood as a machine-readable specification of task-relevant semantic structure.

Under this view, reproducibility is not solely a model-selection problem.

It is also an input-design problem.

The application must construct an input state that places the intended decision sufficiently far from competing alternatives to survive environmental perturbation.

The cross-model results further suggest that heterogeneous model families can respond similarly to a shared semantic structure, but not identically.

The library condition makes this visible.

The same substrate induces different magnitudes of decision displacement across models and semantic contexts.

The relevant object of study is therefore neither the model nor the prompt in isolation.

It is the:

$$
\boxed{
\text{input-structure}
\leftrightarrow
\text{model interaction}
}
$$

Observed capability is therefore better understood as conditional behavior arising from the interaction between learned model state and the structure supplied at inference time.

Substrate engineering treats the latter as an explicit engineering control surface.

---

# 15. The Substrate as a Scope-Specific Reproducibility Mechanism

A substrate should not be interpreted as a universally generalizing prompt.

It is more precisely a **scope-specific reproducibility mechanism**.

For the task and input structure for which it is engineered, the substrate can move the intended decision far from its competing alternative and produce reproducible behavior across heterogeneous models.

The central engineering question begins when that scope expands.

Let:

$$
\mathcal{X}_0
\subset
\mathcal{X}_1
\subset
\mathcal{X}_2
\subset
\cdots
$$

represent progressively broader semantic task domains.

For each domain, define:

$$
M_{\min}(\mathcal{X})
=
\min_{x\in\mathcal{X}}M^*(x)
$$

A substrate is reproducible over domain \(\mathcal{X}\) only if:

$$
M_{\min}(\mathcal{X})
>
\varepsilon_{\mathrm{env}}
$$

As the task domain broadens, the substrate must remain valid under increasingly heterogeneous semantic conditions.

The minimum margin may therefore decrease, and it may decrease differently across model families.

This motivates the concept of a **scope–reproducibility frontier**.

The central substrate-design problem is not simply:

> Does the substrate work?

It is:

> **How broad can the substrate's semantic scope become before its minimum decision margin falls below the reproducibility threshold?**

---

# 16. The Scope–Reproducibility Frontier

Define substrate scope as the semantic domain over which the intervention is intended to remain valid.

Define reproducibility over that scope by:

$$
\rho(\mathcal{X})
=
\min_{x\in\mathcal{X}}
M^*(x)
$$

subject to environmental variation.

Then a domain is validated when:

$$
\rho(\mathcal{X})
>
\varepsilon_{\mathrm{env}}
$$

Increasing scope may introduce inputs on which the substrate produces smaller correct-answer margins.

The empirical frontier is therefore the boundary between:

$$
\text{increasing semantic coverage}
$$

and:

$$
\text{maintaining sufficient reproducibility margin}.
$$

The relationship need not be uniform across models.

Different model families may preserve the substrate-induced structure across different portions of semantic space.

This gives substrate engineering a broader research program:

> **Map the frontier between substrate scope and reproducibility across models, task classes, and substrate designs.**

The present task establishes one point on that frontier.

Broader task classes test how far it extends.

---

# 17. From Point Reproducibility to Generalization

Let the validated operating domain be:

$$
\boxed{
\mathcal{V}
=
\{x:
M^*(x)>\varepsilon_{\mathrm{env}}\}
}
$$

For the exact engineered input:

$$
x_0\in\mathcal{V}
$$

if point reproducibility has been established.

For semantic variants, several outcomes are possible.

Strongly reproducible:

$$
M^*(x)\gg\varepsilon_{\mathrm{env}}
$$

Correct but boundary-sensitive:

$$
0<M^*(x)\leq\varepsilon_{\mathrm{env}}
$$

Incorrect:

$$
M^*(x)<0
$$

This reframes generalization as a measurable systems property.

The question is not merely:

> Does the substrate still produce the correct answer?

It is:

> **Does the substrate maintain sufficient correct-answer margin over the broader domain?**

This distinction matters because categorical accuracy can remain high even while reproducibility deteriorates.

---

# 18. The Reproducibility–Generalization Tradeoff

Semantic constraints can stabilize a particular decision.

For the target task:

$$
\text{semantic constraint}
\uparrow
\quad\Rightarrow\quad
M^*
\uparrow
$$

may hold.

However, those constraints themselves apply only within some semantic validity range.

A highly specialized substrate may produce a very large margin on a narrow task.

A broader substrate may support more heterogeneous inputs but produce smaller minimum margins.

This motivates a possible engineering tension:

$$
\boxed{
\text{reproducibility}
\leftrightarrow
\text{semantic scope}
}
$$

The present work does not require the stronger claim that this relationship is universally monotonic.

The defensible claim is:

> **Any semantic constraint strong enough to stabilize a decision has a finite validity domain, and reproducibility must therefore be specified together with scope.**

This changes what it means to say that a system is reproducible.

A reproducibility claim is incomplete without specifying:

1. the decision,
2. the execution environment,
3. the validated semantic domain.

---

# 19. Estimating the Execution-Noise Floor

The value:

$$
\varepsilon_{\mathrm{env}}
$$

should not be chosen theoretically or post hoc.

It must be estimated empirically from the execution conditions the reproducibility claim is intended to cover.

Repeated identical-input executions can be used to characterize the distribution of observed margin variation.

Relevant sources may include:

* repeated requests to the same endpoint,
* provider-side serving variation,
* hardware differences,
* numerical precision,
* quantization,
* inference-engine differences,
* batching,
* endpoint revisions,
* runtime nondeterminism,
* other deployment-specific effects.

A conservative reproducibility threshold may be defined from a prespecified high quantile or another robust bound on observed environmental variation.

The methodological principle is:

> **The reproducibility boundary must be measured from the environment whose variation the system claims to tolerate.**

There need not be one universal:

$$
\varepsilon_{\mathrm{env}}
$$

Different providers, models, and deployment configurations may require different thresholds.

---

# 20. Implications for Agentic System Architecture

The result has direct implications for agent design.

A conventional architecture may place a general-purpose model directly between a heterogeneous input space and an operational action:

```text
Large heterogeneous input space
             ↓
     General-purpose LLM
             ↓
      Operational action
```

This maximizes semantic flexibility.

It does not explicitly establish whether each operational decision lies safely outside its instability region.

An alternative architecture separates broad interpretation from bounded operational decisions:

```text
Large heterogeneous input space
             ↓
       Semantic routing
             ↓
    Validated decision domain
             ↓
       Task substrate
             ↓
      M* > ε_env ?
        /        \
      yes         no
       ↓           ↓
    execute      reroute /
                 escalate
```

Under this architecture, a single universal substrate is unnecessary.

The total operating space may instead be partitioned:

$$
\mathcal{X}
=
\mathcal{X}_1
\cup
\mathcal{X}_2
\cup
\ldots
\cup
\mathcal{X}_k
$$

with substrate \(S_i\) validated for region \(\mathcal{X}_i\).

For each validated region:

$$
M_i^*(x)>
\varepsilon_{\mathrm{env}}
\qquad
\forall x\in\mathcal{X}_i
$$

A request outside the validated region can be:

* rerouted,
* escalated,
* passed to another substrate,
* or handled by a more general but lower-guarantee system.

Substrate engineering therefore becomes an architectural discipline rather than merely a prompting technique.

---

# 21. A Formal Objective for Reproducible Agent Design

A system should not optimize only:

$$
\max M^*(x_0)
$$

because this can create extreme specialization around one input.

Nor should it optimize only:

$$
\max|\mathcal{X}|
$$

because a large semantic operating domain may contain many fragile decisions.

Instead, define:

$$
\mathcal{V}
=
\{x:
M^*(x)>\varepsilon_{\mathrm{env}}\}
$$

The system-design objective becomes:

$$
\boxed{
\max|\mathcal{V}|
\quad
\text{subject to}
\quad
M^*(x)>\varepsilon_{\mathrm{env}}
\quad
\forall x\in\mathcal{V}
}
$$

In words:

> **Maximize the semantic domain over which the system remains reproducibly correct.**

This objective jointly captures:

* correctness,
* reproducibility,
* and generalization.

It also makes the tradeoff explicit.

A system that achieves enormous margin at one semantic point but fails everywhere else is not sufficient.

A system that generalizes broadly while operating arbitrarily close to unstable decision boundaries is also not sufficient.

The engineering target lies between those extremes.

---

# 22. Mechanistic Extension — Locating the Decision Shift

For open-weight models, we extend the behavioral experiment with layer-level analysis.

For transformer layer \(l\), define:

$$
M_l
=
z_l(\texttt{drive})
-
z_l(\texttt{walk})
$$

where \(z_l\) denotes projected token logits at layer \(l\).

We compare margin trajectories under:

* baseline,
* conventional prompting,
* semantic substrate,
* semantic control conditions.

The mechanistic question is:

> **At what stage of computation does the substrate-induced decision displacement emerge?**

Possible patterns include:

* early separation,
* gradual separation,
* late-stage divergence,
* or minimal separation until final decoding.

These patterns would support different explanations of how structured semantic input alters the final decision.

The logit-lens analysis is therefore a mechanistic extension of the primary systems result.

It is not required for the behavioral reproducibility claim.

---

# 23. Threats to Validity

The strongest validated claim in the present study concerns one deliberately narrow decision task evaluated across a broad model and provider matrix.

The experiment can establish:

* a shared baseline decision failure,
* the behavior of several conventional interventions,
* substrate-induced decision displacement,
* reproducible correction on the engineered input,
* and margin movement hidden by categorical output.

It does not yet establish:

* that all semantic tasks admit an effective substrate,
* that substrate engineering universally outperforms conventional prompting,
* that stronger semantic constraint always reduces generalization,
* that one margin scale is directly comparable across providers,
* that one universal \(\varepsilon_{\mathrm{env}}\) applies across deployment environments,
* that token-level margin captures every relevant form of behavioral instability,
* that the observed substrate mechanism is identical across model architectures,
* or that the scope–reproducibility frontier has the same shape across arbitrary agentic tasks.

The library condition also limits overly strong claims of clean semantic selectivity.

The same substrate moves the decision margin even when it does not change the final categorical decision.

This is not necessarily a failure of the substrate.

It demonstrates that substrate effects are graded and model-dependent rather than binary.

These limitations define the empirical boundary of the present study and motivate the broader research program.

---

# 24. Discussion — From Model Capability to Input–Model Interaction

LLM behavior is often described primarily in terms of model capability.

The present results suggest that this framing is incomplete for operational systems.

Observed behavior arises from:

$$
F(\theta,x,d,e)
$$

rather than from \(\theta\) alone.

The learned model state determines what transformations are available.

The input determines which semantic structure is presented to those learned transformations.

The decoding procedure determines how the resulting distribution is resolved.

The execution environment introduces additional implementation-level variation.

For reproducibility engineering, the important observation is not that model capability is irrelevant.

It is that capability alone does not determine the operational decision.

The relevant object is the interaction between:

$$
\boxed{
\text{model state}
\times
\text{input structure}
}
$$

under a particular execution environment.

This shifts the engineering locus of attention.

Instead of asking only:

> Which model is capable enough?

we must also ask:

> **What semantic structure must be supplied so that the intended decision becomes stable enough to survive deployment variation?**

This is the problem substrate engineering targets.

---

# 25. Discussion — Reproducibility Changes the Engineering Objective

The conventional evaluation question for a general-purpose language model is often:

> How well does the model generalize?

For operational LLM-native systems, this question is incomplete.

A second question is required:

> **How much of that generalized behavior lies inside a reproducibly correct operating region?**

A model may achieve high average accuracy while many individual decisions remain close to their decision boundaries.

Those decisions may be correct but operationally fragile.

Conversely, a highly specialized substrate may produce a large correct-answer margin on one task while generalizing poorly.

Neither extreme is sufficient.

The relevant engineering object is therefore the relationship between:

$$
\text{validated semantic scope}
$$

and:

$$
\text{minimum correct-answer margin}
$$

A reproducible agent must retain enough semantic flexibility to remain useful while constraining critical decisions strongly enough to remain stable.

The central design problem is therefore a frontier problem:

> **How much semantic scope can the system preserve while maintaining a decision margin greater than the environmental noise floor?**

---

# 26. Conclusion

This work studies reproducibility at the smallest operational unit of an LLM-native system: a single model decision.

We begin from the observation that model output is not a property of model weights alone.

At inference time:

$$
y=F(\theta,x,d,e)
$$

For application developers, the model state is largely fixed and the execution environment is often only partially controllable.

The input remains one of the primary application-level control surfaces capable of altering the semantic decision itself.

Across 19 frontier models and seven vendors, we identify a shared baseline decision failure and compare several conventional prompt interventions with an engineered semantic substrate.

The tested conventional interventions do not reproducibly correct the decision.

The substrate does so on the input for which it was engineered.

Token-level analysis further shows that intervention effects are graded: the same categorical output can conceal substantial movement in decision space.

This motivates three distinct criteria.

Correctness requires:

$$
M^*(x)>0
$$

Reproducibility requires:

$$
M^*(x)>
\varepsilon_{\mathrm{env}}
$$

Generalization requires maintaining that condition over a semantic domain:

$$
M^*(x)>
\varepsilon_{\mathrm{env}}
\qquad
\forall x\in\mathcal{V}
$$

A substrate is therefore best understood as a **scope-specific reproducibility mechanism**.

Its effectiveness cannot be described only by whether it produces the correct answer at one point.

It must also be described by the semantic domain over which its decision margin remains above the reproducibility threshold.

This produces a broader engineering problem.

If reproducibly correct decisions require semantic constraint while generalization requires broader semantic flexibility, then the design problem is not to maximize either property in isolation.

It is to map and optimize their frontier.

We therefore propose the following objective for reproducible LLM-native systems:

$$
\boxed{
\max|\mathcal{V}|
\quad
\text{subject to}
\quad
M^*(x)>
\varepsilon_{\mathrm{env}}
\quad
\forall x\in\mathcal{V}
}
$$

> **The design problem for reproducible agents is to maximize the semantic domain over which the correct decision remains separated from its competing alternatives by more than the execution-noise floor.**

Mapping this scope–reproducibility frontier across task classes, model families, and substrate designs defines the broader research program of substrate engineering.
