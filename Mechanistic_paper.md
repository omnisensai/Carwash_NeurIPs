

# Working Title

## **From Rule to Decision: Causal Mapping of Semantic Constraints Through Transformer Computation**

Alternative:

## **Where Do Instructions Take Effect? Causal Tracing of Semantic Constraints Across Transformer Depth and Position**

More tool-forward:

## **Constraint–Depth Intervention Maps: Tracing Structured Context Through Transformer Computation**

---

# Core Question

Structured context can radically change an LLM's final decision.

But when a particular semantic constraint changes behavior, we still do not know how the computational effect of that constraint propagates through the network.

We ask:

> **Where, across transformer depth and sequence position, does a behaviorally verified semantic constraint become causally consequential for the final decision?**

The problem has two levels.

At the input level, we can establish that a semantic rule matters by removing or counterfactually modifying it and observing the final decision.

At the internal level, we then ask where the representation induced by that rule becomes sufficient or necessary to recover the corresponding decision.

The objective is therefore not to decode an intermediate state into vocabulary space.

It is to follow the causal effect of a known semantic intervention through the model.

---

# Core Hypothesis

A semantic constraint does not necessarily exert its causal effect at the same sequence position where it was originally written.

Instead, the constraint may progressively alter representations at other positions before becoming sufficient at the final prediction site.

A possible computation is therefore:

$$
\text{written constraint}
\rightarrow
\text{constraint-conditioned state}
\rightarrow
\text{question representation}
\rightarrow
\text{answer-site state}
\rightarrow
\text{decision}.
$$

The intermediate states need not directly encode the eventual output token.

The claim being tested is narrower:

> **The causal effect induced by a semantic constraint can be localized across layer and position by intervening on the internal state and measuring its effect on the final decision margin.**

---

# Methodological Contribution

We introduce a controlled intervention protocol that we call a:

# **Constraint–Depth Intervention Map (CDIM)**

The underlying operation—activation patching—is not itself new.

The contribution is the experimental construction around it:

$$
\boxed{
\text{behaviorally identified semantic constraint}
\rightarrow
\text{token-aligned counterfactual}
\rightarrow
\text{layer}\times\text{semantic-position interventions}
\rightarrow
\text{final decision effect}
}
$$

CDIM therefore connects two levels that are usually studied separately:

$$
\text{semantic input ablation}
\longleftrightarrow
\text{internal causal intervention}.
$$

Unlike a vocabulary decoder, CDIM does not ask:

> What token can be read from this state?

It asks:

> If this internal state is exchanged between two controlled computational trajectories, what happens to the eventual decision?

The remaining transformer layers themselves are the downstream decoder.

---

# Motivating Observation

The substrate experiments already provide the necessary starting point.

For Llama-3.1-8B, the full substrate moves the carwash decision toward Drive.

Input-level ablation shows that the vehicle-operation constraint is particularly important:

$$
M(S)>0,
$$

while removing the critical rule produces:

$$
M(S_{-6})<0.
$$

However, the rule in isolation remains insufficient:

$$
M(\{c_6\})<0.
$$

Thus the critical constraint is behaviorally necessary in the full semantic structure but not independently sufficient.

At the same time, answer-position residual patching shows that a substrate-conditioned state becomes sufficient to change the downstream baseline computation around:

$$
\ell \approx 16/32.
$$

These two findings leave an unresolved mechanistic question:

> **How does the effect of the behaviorally necessary constraint get from the written rule to the causally sufficient answer-site state?**

CDIM is designed to measure that missing transformation.

The same framework also accommodates qualitatively different substrate structures.

For example, preliminary Llama-70B ablations suggest one standard-substrate line can be individually important, while the more explicit substrate has no single leave-one-out rule whose removal destroys the decision.

This provides contrasting cases of localized versus distributed semantic dependence.

---

# 1. Introduction — From Semantic Rules to Internal Computation

Prompt interventions are often treated as monolithic changes to model input.

If changing a system prompt changes the answer, we know only that:

$$
x_A \neq x_B
$$

produced:

$$
y_A \neq y_B.
$$

That observation says little about how the semantic difference propagates internally.

Mechanistic studies can intervene on activations, but causal tracing normally begins with internal states and searches for consequential components.

Structured semantic inputs give us an additional advantage:

**the causal variable can first be identified externally.**

A substrate consists of explicitly authored semantic constraints.

Individual constraints can therefore be removed, altered, or counterfactually inverted before any internal analysis occurs.

This creates a natural experimental sequence:

$$
\text{identify a behaviorally consequential semantic rule}
$$

$$
\downarrow
$$

$$
\text{construct a matched semantic counterfactual}
$$

$$
\downarrow
$$

$$
\text{trace the internal state differences caused by that rule}.
$$

The paper studies that mapping.

---

# 2. Behavioral Identification of Semantic Constraints

Let the final binary decision margin be:

$$
M(x)
=
\log P(y^*\mid x)
-
\log P(y'\mid x).
$$

For the carwash task:

$$
M
=
\log P(\texttt{drive})
-
\log P(\texttt{walk}).
$$

Let:

$$
S
$$

denote the full structured semantic input.

For constraint \(c_i\), construct an input-level counterfactual:

$$
C_i.
$$

Unlike a simple deletion, \(C_i\) should preserve prompt structure and sequence alignment as closely as possible while changing the operative semantics of \(c_i\).

Define its behavioral effect:

$$
\Delta_i^{\mathrm{beh}}
=
M(S)-M(C_i).
$$

A large:

$$
|\Delta_i^{\mathrm{beh}}|
$$

identifies a semantic constraint whose presence materially changes the decision trajectory.

This behavioral test occurs **before** internal tracing.

Thus the mechanistic analysis is conditioned on a known external intervention rather than discovered retrospectively from an activation heatmap.

---

# 3. Matched Semantic Counterfactuals

The clean and counterfactual computations should differ in the smallest semantic quantity necessary for the experiment.

For each model, counterfactual prompts should therefore aim to preserve:

* total sequence structure,
* position of the question,
* position of the answer site,
* semantic-group boundaries,
* and, where practical, token count under the model's tokenizer.

The goal is not to compare:

$$
\text{six-line substrate}
$$

against:

$$
\text{no system prompt}.
$$

Such a comparison entangles the semantic effect with large differences in token identity, length, position, and context.

Instead, the primary mechanistic comparison should be:

$$
S
$$

versus:

$$
C_i,
$$

where only the relevant semantic constraint has been neutralized or counterfactually altered.

This makes internal state transplantation substantially easier to interpret.

---

# 4. Constraint–Depth Intervention Map

Let:

$$
r_{\ell,p}^{S}
$$

denote the residual state at layer \(\ell\), position \(p\), in the substrate run.

Likewise:

$$
r_{\ell,p}^{C}
$$

for the matched counterfactual.

The primary intervention is not restricted to individual BPE tokens.

Positions are first organized into meaningful semantic groups:

$$
g \in
\{
c_1,\ldots,c_k,
\text{question},
\text{answer site}
\}.
$$

All token states belonging to a semantic group can be patched jointly.

This avoids interpreting independently patched subword tokens as independently meaningful semantic variables.

---

## 4.1 Forward Rescue

Insert the substrate-conditioned state into the counterfactual run:

$$
r_{\ell,g}^{C}
\leftarrow
r_{\ell,g}^{S}.
$$

Define:

$$
\boxed{
R_{\ell,g}
=
M\left(
C\mid
r_{\ell,g}^{C}\leftarrow r_{\ell,g}^{S}
\right)
-
M(C)
}
$$

This asks:

> **How much does the substrate-conditioned state at this layer and semantic position rescue the target decision in the counterfactual computation?**

Large positive \(R_{\ell,g}\) indicates causal sufficiency under the remaining counterfactual downstream computation.

---

## 4.2 Reverse Disruption

Perform the reverse intervention:

$$
r_{\ell,g}^{S}
\leftarrow
r_{\ell,g}^{C}.
$$

Define:

$$
\boxed{
D_{\ell,g}
=
M(S)
-
M\left(
S\mid
r_{\ell,g}^{S}\leftarrow r_{\ell,g}^{C}
\right)
}
$$

This asks:

> **How much of the substrate decision is lost when the substrate-conditioned state at this location is replaced by its counterfactual counterpart?**

Large positive \(D_{\ell,g}\) indicates local causal necessity under the intact substrate computation.

---

# 5. Why Forward and Reverse Maps Matter

Forward and reverse interventions answer different causal questions.

A state can be highly sufficient without being individually necessary if multiple internal copies or redundant pathways exist.

Likewise, a state can be necessary within the intact substrate computation while being insufficient by itself to reconstruct the decision in the counterfactual trajectory.

Therefore CDIM does not produce a single scalar “causal weight.”

It produces two intervention surfaces:

$$
R_{\ell,g}
$$

and:

$$
D_{\ell,g}.
$$

The combination provides a richer interpretation.

High rescue + high disruption suggests a particularly consequential state.

High rescue + low disruption is consistent with sufficient but replaceable information.

Low rescue + high disruption is consistent with dependence on surrounding substrate-conditioned context.

Low rescue + low disruption indicates that exchanging that group at that depth has little measurable effect under the tested intervention.

These are intervention patterns, not claims about unique internal features.

---

# 6. The Position Dimension

Existing answer-position patching measures only one trajectory:

$$
g=\text{answer site}.
$$

CDIM expands the experiment over semantic position.

For the substrate task, the initial map should contain at minimum:

$$
\text{critical constraint}
$$

$$
\text{other substrate constraints}
$$

$$
\text{question span}
$$

$$
\text{answer site}.
$$

This allows the paper to ask whether causal sensitivity changes location with depth.

A possible empirical pattern would be:

| Network depth | Critical constraint |   Question | Answer site |
| ------------- | ------------------: | ---------: | ----------: |
| Early         |              strong |       weak |        weak |
| Middle        |           declining |     strong |    emerging |
| Late          |      weak/redundant | persistent |      strong |

Such a pattern would be consistent with a redistribution of constraint-conditioned information.

But node interventions alone would **not** establish a literal route.

The paper should initially describe this as:

> **a depth-dependent relocation of causal sensitivity across sequence positions.**

---

# 7. Path Validation

If the CDIM suggests a pattern such as:

$$
\text{constraint span}
\rightarrow
\text{question span}
\rightarrow
\text{answer site},
$$

a second experiment tests that hypothesized flow directly.

Use path-specific patching on a restricted set of candidate layers and positions.

The purpose is not to exhaustively recover the entire model circuit.

It is to discriminate between:

$$
\text{co-occurring causal states}
$$

and:

$$
\text{a causally relevant communication pathway}.
$$

Thus the study has two stages:

$$
\text{node map}
\rightarrow
\text{candidate path}
\rightarrow
\text{path intervention}.
$$

This prevents a position-by-layer heatmap from being overinterpreted as proof of information flow.

---

# 8. Experimental Scope

The first paper does not require five unrelated benchmark families.

The cleanest initial study uses cases where the semantic intervention is already externally interpretable.

Primary cases:

* Llama-3.1-8B, where line 6 is behaviorally important.
* Llama-3.3-70B, where the standard substrate shows a different constraint-dependence structure.
* Qwen3 models, where substrate behavior differs substantially across model scale and substrate formulation.

The experimental matrix should include both:

$$
\text{successful substrate decision change}
$$

and:

$$
\text{failed or degraded substrate intervention}.
$$

That second category is important.

If CDIM merely lights up whenever system text is present, it is not measuring task-specific causal structure.

---

# 9. Control Tasks

The library control becomes mechanistically important.

For the carwash task, Drive is the intended target.

For the library-book control, Walk remains appropriate.

Run the same semantic structure and causal mapping procedure on both.

This tests whether a state associated with the vehicle rule is genuinely task-sensitive or merely contributes a generic Drive bias.

Likewise include:

### Headers-only control

The 8B behavioral ablation already indicates that structural headers alone can make the decision margin worse.

If CDIM is causally meaningful, these states may show:

$$
R_{\ell,g}<0
$$

or otherwise differ from useful semantic constraints.

### Same-run patch

$$
S\rightarrow S
$$

and:

$$
C\rightarrow C
$$

should leave behavior unchanged apart from numerical error.

### Unrelated-state control

Patch residual states from unrelated semantic positions or matched controls to establish that arbitrary vector replacement is insufficient to produce the observed effect.

---

# 10. Cross-Scale Analysis

The paper can then ask whether similar semantic roles produce similar causal organization across model scale.

Current answer-position results suggest approximately mid-stack causal sufficiency in several Llama models:

$$
14/28\approx0.50,
$$

$$
16/32=0.50,
$$

$$
41/80\approx0.51.
$$

This is intriguing but remains preliminary.

CDIM adds a more informative question:

> Does the entire spatial-temporal organization of the semantic constraint scale similarly?

For example, larger models may:

* retain constraint-specific states longer,
* redistribute them earlier,
* maintain multiple sufficient copies,
* or require different semantic rules entirely.

Therefore normalized depth alone is not the primary object.

The object is the **causal transformation of the authored constraint**.

---

# 11. Constraint Dependence Across Models

The existing behavioral ablations already suggest that the same substrate need not operate through the same semantic bottleneck in every model.

For example:

$$
\text{8B: line 6 behaviorally important}
$$

while:

$$
\text{70B standard: line 1 behaviorally important}.
$$

In the more explicit 70B substrate, no single leave-one-out rule appears individually necessary.

CDIM can test whether this corresponds internally to:

* a localized bottleneck,
* multiple sufficient representations,
* distributed constraint dependence,
* or qualitatively different computation.

This provides a mechanistic counterpart to one of Substrate Engineering's central empirical findings:

> identical semantic specifications can interact differently with different frozen models.

---

# 12. Optional Token-Level Resolution

The initial analysis should patch semantic groups jointly.

Only after a meaningful group is identified should the experiment zoom into individual token positions.

For a critical rule \(c_i\):

$$
g=c_i
$$

can be decomposed into:

$$
p_1,\ldots,p_n.
$$

Per-token intervention maps can then ask whether particular positions disproportionately influence the effect.

However, token effects should not simply be summed and interpreted as the effect of the full rule:

$$
\Delta M(p_1)+\Delta M(p_2)
\neq
\Delta M(\{p_1,p_2\})
$$

in general.

The semantic group remains the primary experimental unit.

---

# 13. Optional Relationship to Readout Methods

Logit lens and tuned lens are **not required for the paper's central claim**.

CDIM already measures what the study cares about:

$$
\text{effect on final behavior}.
$$

A secondary appendix experiment may compare:

$$
M_\ell^{\mathrm{raw}}
$$

against:

$$
R_{\ell,\text{answer}}.
$$

This can illustrate that direct vocabulary visibility and causal sufficiency need not coincide.

But the paper should not require the stronger statement that one decoder is the correct representation of what the model “believes.”

The primary measurement is intervention-based.

Thus the interpretive hierarchy becomes:

$$
\text{behavioral semantic effect}
$$

$$
\downarrow
$$

$$
\text{internal intervention effect}
$$

$$
\downarrow
$$

$$
\text{optional decoded representation}.
$$

Not the reverse.

I would completely drop tuned lens from v1 unless it becomes necessary for a reviewer-facing control.

---

# 14. Relationship to Existing Causal-Tracing Methods

The novelty boundary needs to be explicit.

The paper does **not** claim to invent activation patching, causal tracing, or path patching.

Instead, it introduces a structured protocol for connecting an externally interpretable semantic intervention to internal causal states.

The distinction is:

$$
\text{ordinary causal tracing:}
\quad
\text{internal component}
\rightarrow
\text{behavior}
$$

versus:

$$
\text{CDIM:}
\quad
\text{known semantic constraint}
\rightarrow
\text{behavioral necessity}
\rightarrow
\text{internal causal localization}.
$$

This makes authored semantic rules experimental variables.

That is the methodological contribution to defend.

---

# 15. Primary Measurements

For every model \(m\), constraint \(i\), layer \(\ell\), and semantic group \(g\):

$$
M(S)
$$

$$
M(C_i)
$$

$$
\Delta_{i}^{\mathrm{beh}}
=
M(S)-M(C_i)
$$

$$
R_{\ell,g}
$$

$$
D_{\ell,g}.
$$

For comparisons across models, raw decision-margin effects should remain available.

A within-model normalized form may additionally be reported:

$$
\rho_{\ell,g}^{R}
=
\frac{R_{\ell,g}}
{\Delta_i^{\mathrm{beh}}}
$$

and:

$$
\rho_{\ell,g}^{D}
=
\frac{D_{\ell,g}}
{\Delta_i^{\mathrm{beh}}},
$$

provided that:

$$
|\Delta_i^{\mathrm{beh}}|
$$

is sufficiently large.

These normalized quantities are not probabilities and need not remain between zero and one.

Overshoot is itself possible because internal interventions can create hybrid computational states.

---

# 16. Primary Claims

The paper should again use a claim ladder.

### Claim 1

Behaviorally consequential semantic constraints can be linked to specific internal states whose transplantation materially changes the final decision margin.

### Claim 2

The causal effect associated with a semantic constraint is not necessarily localized to the token positions where the constraint was originally written.

### Claim 3

Across depth, causal sensitivity can redistribute from authored constraint positions toward downstream contextual and prediction-site representations.

This claim requires position-level evidence.

### Claim 4

For selected cases, path interventions confirm causal communication between the sequence positions identified by the intervention map.

This requires actual path patching.

### Claim 5

Different model scales or families can implement the same externally specified semantic constraint through different internal causal organizations.

This requires replicated cross-model maps.

No claim should say:

> “the model decided at layer \(l\).”

The defensible statement is:

> **a substrate-conditioned state at layer \(l\) and semantic position \(g\) was sufficient and/or necessary, under the specified intervention, to alter the downstream decision.**

---

# 17. Main Figures

### Figure 1 — Experimental Logic

$$
\text{semantic rule}
$$

$$
\downarrow
$$

$$
\text{behavioral counterfactual}
$$

$$
\downarrow
$$

$$
\text{constraint-depth intervention map}
$$

$$
\downarrow
$$

$$
\text{candidate internal path}
$$

$$
\downarrow
$$

$$
\text{final decision}.
$$

### Figure 2 — Canonical 8B CDIM

Two heatmaps:

$$
R_{\ell,g}
$$

and:

$$
D_{\ell,g}.
$$

Rows:

* substrate line 1–6,
* question,
* answer site.

Columns:

$$
1\ldots32.
$$

This should be the flagship tool figure.

### Figure 3 — Behavioral and Internal Agreement

Show that the input-level critical constraint identified by the semantic ablation also produces a distinctive causal-intervention signature internally.

For example:

$$
\text{LOO semantic effect}
\leftrightarrow
\text{CDIM causal effect}.
$$

### Figure 4 — Cross-Model Maps

8B versus 70B versus Qwen.

Not just onset points.

Show whether the causal organization itself changes.

### Figure 5 — Path Validation

A focused experiment validating one apparent:

$$
\text{constraint}
\rightarrow
\text{question}
\rightarrow
\text{answer}
$$

handoff.

---

# 18. Interpretation Boundaries

The study should be explicit about what CDIM does **not** establish.

A residual patch exchanges a high-dimensional state.

Therefore a successful intervention does not identify the unique feature inside that vector responsible for the effect.

Likewise:

$$
R_{\ell,g}>0
$$

does not imply that the model explicitly represents the final answer at \((\ell,g)\).

It establishes only that the substrate-conditioned state at that location contains a difference that is causally sufficient, under the remaining downstream computation, to alter the final margin.

Reverse disruption establishes intervention-specific necessity, not philosophical necessity of a representation.

Node-level maps do not establish paths.

Path claims require path-specific interventions.

And a successful result on one semantic rule does not imply that all instructions propagate through the same computational architecture.

---

# 19. Mechanistic Follow-Up

Once the causal map identifies important layers and positions, finer analysis can ask what computation produces the effect.

Candidate follow-ups include:

* attention-head versus MLP decomposition,
* subspace intervention,
* component patching,
* path-specific patching,
* feature-direction removal,
* redundancy tests,
* and interaction between multiple semantic rules.

These should follow the causal map rather than precede it.

CDIM therefore serves as a search instrument:

$$
\text{semantic intervention}
\rightarrow
\text{causal localization}
\rightarrow
\text{circuit analysis}.
$$

---

# 20. Conclusion

Structured semantic inputs give mechanistic interpretability something unusually valuable:

**an externally meaningful causal variable.**

If removing or altering a specific rule changes model behavior, the resulting pair of computational trajectories can be used to ask where the internal consequences of that semantic difference become causally important.

Constraint–Depth Intervention Mapping connects these levels.

It begins with:

$$
\text{what rule changed behavior?}
$$

and proceeds to:

$$
\text{where does the state induced by that rule matter?}
$$

and finally:

$$
\text{how does that influence reach the eventual decision?}
$$

The methodological goal is therefore not to assign vocabulary meaning to every intermediate residual state.

It is to trace the causal transformation of an authored semantic constraint through the computation that produces the model's decision.

---

I think this is **much cleaner than the old Paper 2**.

The old spine's central object was:

$$
G=\frac{\ell_{\mathrm{readout}}-\ell_{\mathrm{causal}}}{L}.
$$

The new paper's central object is instead the pair of surfaces:

$$
\boxed{R_{\ell,g},\;D_{\ell,g}}
$$

with the input-level behavioral effect:

$$
\boxed{\Delta_i^{\mathrm{beh}}}
$$

anchoring them.

So you now have a beautiful three-level chain:

$$
\boxed{
\text{Semantic necessity}
\rightarrow
\text{Internal causal effect}
\rightarrow
\text{Decision}
}
$$

