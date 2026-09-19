
# Substrate Engineering: From Engineered Behavioral Convergence to Controlled Mechanistic Measurement

## Central thesis

LLM-native systems can produce different operational outcomes under the same nominal task. This behavioral multiplicity complicates both reproducible execution and mechanistic comparison across models.

We investigate an experimental approach in which a shared, task-faithful semantic specification is used to engineer reproducible behavioral convergence across otherwise divergent frozen models.

The resulting consistency is not merely an endpoint. It establishes a controlled reference condition.

We then systematically perturb the semantic specification, measure the resulting behavioral changes, and use internal activation interventions to characterize how those changes are causally realized inside the models.

The central methodological distinction is:

> We do not select models that happen to behave consistently. We engineer consistency, then study the behavioral and internal changes that produce and maintain it.

The same experiment therefore connects three levels:

Semantic intervention→measured behavioral displacement→internal causal response\boxed{ \text{Semantic intervention} \rightarrow \text{measured behavioral displacement} \rightarrow \text{internal causal response} }Semantic intervention→measured behavioral displacement→internal causal response

# 1. Introduction — Operational multiplicity and the measurement problem

## 1.1 The systems problem

LLM-native systems increasingly use model outputs to determine downstream operational actions.

Consider:

Invoice + policy→LLM→{APPROVE,REJECT}.\text{Invoice + policy} \rightarrow \text{LLM} \rightarrow \{\texttt{APPROVE},\texttt{REJECT}\}.Invoice + policy→LLM→{APPROVE,REJECT}.

If the same governed input can produce both APPROVE and REJECT, the system lacks reproducible operational behavior over those executions.

Our original systems experiment exposed this problem across four frontier models, producing 80 distinct output hashes across the test matrix.

Restructuring the input's semantic specification brought the tested executions into one byte-identical output class without modifying model weights.

This motivated Substrate Engineering: the construction of semantic input structures that constrain a model's interpretation of a task sufficiently to establish reproducible operational behavior.

## 1.2 Why behavioral convergence creates a measurement opportunity

A nominally identical task does not necessarily produce identical behavior across models.

When models disagree, an internal comparison may conflate architectural differences with differences in their responses to the input.

Rather than selecting examples on which models happen to agree, we deliberately engineer a shared behavioral reference.

We then perturb that reference under fixed within-model conditions.

This allows us to study:

What changed internally when a known semantic intervention changed behavior?\text{What changed internally when a known semantic intervention changed behavior?}What changed internally when a known semantic intervention changed behavior?

The object of analysis is the controlled behavioral transition, not an uncontrolled final state.

## 1.3 Contributions

The paper makes three connected contributions.

Engineered behavioral convergence. We demonstrate that one task-semantic specification can establish a common operational outcome across a declared set of initially divergent frozen models.

Characterization of semantic control. We compare conventional prompting interventions, explicit semantic constraints, counter-directional specifications, and individual constraint ablations to identify which input properties produce measurable behavioral displacement.

Mechanistic measurement under controlled behavior. We freeze successful model–substrate conditions and causally trace the internal effects of defined semantic perturbations, relating activation-level interventions to the externally measured behavioral change.

# 2. Problem formulation — Semantic control of a frozen model

Let the operational output be:

y=F(θ,q,S,d,e),y=F(\theta,q,S,d,e),y=F(θ,q,S,d,e),

where θ\thetaθ denotes the frozen model, qqq the user task, SSS the engineered semantic specification, ddd the decoding configuration, and eee the execution environment.

For the binary carwash task, define the output preference margin:

M=log⁡P(drive)−log⁡P(walk)\boxed{ M= \log P(\texttt{drive}) - \log P(\texttt{walk}) }M=logP(drive)−logP(walk)

with:

M>0⇒Drive,M<0⇒Walk.M>0\Rightarrow\texttt{Drive}, \qquad M<0\Rightarrow\texttt{Walk}.M>0⇒Drive,M<0⇒Walk.

This is a declared binary preference measure, not a complete characterization of the model's output distribution.

For an intervention uuu, the observed margin displacement is:

ΔMm(u)=Mm(q,u)−Mm(q).\boxed{ \Delta M_m(u) = M_m(q,u)-M_m(q). }ΔMm(u)=Mm(q,u)−Mm(q).

The empirical question is which changes to the input produce a reproducible transition across the intended operational boundary.

For a semantic state sss with intended action r(s)∈{−1,+1}r(s)\in\{-1,+1\}r(s)∈{−1,+1}, define its signed margin:

Mm∗(s,S)=r(s)Mm(q,S).M_m^*(s,S)=r(s)M_m(q,S).Mm∗(s,S)=r(s)Mm(q,S).

A positive signed margin favors the intended action.

Reproducibility is evaluated separately using repeated executions and the declared model, input, and execution matrix. Where an execution-noise bound is empirically estimated, robustness can additionally be expressed through:

Mm∗>εexec,m.M_m^*>\varepsilon_{\mathrm{exec},m}.Mm∗>εexec,m.

Task-preserving wording changes are changes to the input, not execution noise.

# 3. External experiment I — Establishing behavioral convergence

## 3.1 The untreated carwash task

We use a minimal operational decision:

> I need to wash my car. The car wash is only 50 metres away. Should I walk or drive there?

The task is intentionally simple, but the surface request leaves the relationship between the objective, object transport, and available actions partly implicit.

We establish the untreated output and, where available, decision margin for each model.

The baseline is not assumed to be uniformly incorrect: models may begin on either side of the decision boundary.

## 3.2 Conventional prompting interventions

Using the same underlying task, we evaluate the tested prompt-level interventions, including:

- Think step by step, encouragement, expert framing, anti-hallucination instructions, urgency, threats, and emphasis on the user's objective.

Their purpose is to establish how different kinds of input modification affect the same frozen-model output preference.

For each intervention:

ΔMm(ui)=Mm(q,ui)−Mm(q).\Delta M_m(u_i) = M_m(q,u_i)-M_m(q).ΔMm(ui)=Mm(q,ui)−Mm(q).

The analysis distinguishes interventions that leave the categorical result unchanged, move the margin without crossing the boundary, and produce an intended boundary crossing.

We do not assume that every conventional intervention has zero effect merely because its final categorical answer remains Walk.

## 3.3 Semantic substrate intervention

We introduce the complete task-semantic specification.

It explicitly defines the user's objective, the required movement of the object, the condition under which the objective is satisfied, and the action required to transport a vehicle.

The substrate is not an instruction to emit a predetermined answer token.

It specifies the conditions that determine which action satisfies the task.

We apply the same substrate across the declared model set and evaluate the resulting behavioral convergence.

Table 1 — Fleet-wide behavioral results

The primary external result belongs here, before any single-model ablation.

Report baseline and substrate responses for every tested model, including repeated categorical outcomes, formatting failures, and available margins. Distinguish the original 19-model benchmark from later 17-model control experiments wherever their model sets differ.

The paper must distinguish categorical convergence from byte-identical output convergence. The earlier 80-hash experiment motivates exact-artifact reproducibility; the carwash benchmark establishes its own measured level of output agreement.

# 4. External experiment II — Testing semantic control rather than one-directional answer steering

The forward substrate establishes behavior toward Drive.

To characterize whether the input can control the output in other directions, we evaluate independently specified semantic conditions.

These experiments are behavioral controls, not alternative substrates to be compared for their internal superiority.

## 4.1 Counter-directional substrate

We construct a reverse specification that prioritizes short-distance travel on foot.

In the reported 17-model experiment, 156 of 170 outputs were Walk, 10 were Drive, and four were empty.

Sixteen models were Walk-dominant. Claude Opus 4.7 continued to produce Drive in all ten runs.

This establishes that the tested semantic specifications can induce opposite dominant behavioral outcomes across much of the model set.

However, the generic reverse condition changes the objective and directly instructs walking. It is therefore evidence of counter-directional behavioral control, not an isolated test of the same task semantics with one relation reversed.

## 4.2 Counterfactual physics

We retain the object-transport objective while altering the physical affordances of the objects.

Cars are specified as miniature and portable, while books are specified as extremely heavy and nonportable.

The inverted-physics carwash experiment produced Walk in 165 of 170 recorded outputs.

The inverted-library experiment produced a predominantly Drive response, with model-dependent failures and variability.

These results test whether the model's output tracks the authored physical and action constraints rather than a fixed association between familiar object names and response labels.

The physics conditions also contain explicit action-language cues, which should remain visible as a limitation when interpreting their mechanism.

## 4.3 Role-swap control

The role-swap condition changes the lexical assignments of user, car, and object while attempting to preserve the underlying transport requirement.

Its purpose is to probe sensitivity to surface role assignments while retaining the intended relational structure.

Behavioral results should be reported once the corresponding recorded model outputs are included in the final corpus.

## External interpretation

Together, these controls establish that semantic specifications can induce different directions of behavioral change and that the resulting response is dependent on the specified task conditions and model.

They do not establish that every model follows every authored specification, nor do they prove that all conditions act through the same internal mechanism.

Figure 1 — Engineered behavioral control

Baseline divergence → forward convergence → counter-directional response

Display the fleet-wide response matrix, including the reverse and physics-inversion results. Preserve the model-level exceptions rather than reporting only aggregate percentages.

# 5. Freeze the successful substrate — Behavioral ablation as controlled measurement

Having established successful model–substrate conditions, we freeze the validated reference for each model.

The next experiment is not a search across different substrate designs.

It is a series of controlled perturbations of an already established semantic specification.

For model mmm, let:

SmS_mSm

denote its fixed successful reference substrate.

For semantic constraint cic_ici, construct a specified intervention:

Sm(i).S_m^{(i)}.Sm(i).

The behavioral effect is:

ΔMm,i=Mm(q,Sm)−Mm(q,Sm(i)).\boxed{ \Delta M_{m,i} = M_m(q,S_m) - M_m(q,S_m^{(i)}). }ΔMm,i=Mm(q,Sm)−Mm(q,Sm(i)).

The same model, question, decoding configuration, and execution conditions are retained within the paired comparison.

## 5.1 Deletion and reversal are different interventions

Deleting a rule removes a specification.

Reversing a rule introduces an explicitly different semantic relation.

These interventions can produce different behavioral responses and must be reported separately.

## 5.2 Semantic composition

In the tested Llama-3.1-8B configuration, the complete substrate produces approximately:

M(S)=+1.M(S)=+1.M(S)=+1.

Every individually tested rule remains on the Walk side.

Removing line 6 from the complete substrate produces approximately:

M(S−6)=−0.6.M(S_{-6})=-0.6.M(S−6)=−0.6.

Thus line 6 is necessary for the complete substrate's positive result under that intervention, but is insufficient in isolation.

The behavioral effect of the constraint depends on the surrounding semantic structure.

This establishes the external phenomenon to be investigated internally; it does not predetermine how the model computes that dependence.

## 5.3 Characteristics of effective interventions

The complete intervention set allows us to compare different semantic functions performed by input text.

Conventional instructions can request a reasoning procedure, emphasize an objective, or apply pressure to the response.

The substrate specifies relations among entities, goals, required object movement, action feasibility, and task satisfaction.

The experimental question is:

> Which of these specified relations and their interactions causally influence the final preference, and how do those effects differ from interventions that do not establish the intended transition?

This is how the paper begins characterizing the semantic control surface rather than merely reporting that one prompt succeeds.

Figure 2 — Behavioral ablation

Complete substrate versus individual rules and leave-one-out conditions

Show the 8B measurements and the decision boundary. Report the larger 70B rule-reversal effects as a second, model-specific example. Identify the exact intervention used in each condition.

# 6. Internal experiment — Measuring the causal consequences of controlled behavioral change

The mechanistic experiment uses the same fixed reference substrate and a defined perturbation whose external effect has already been measured.

Let:

hℓ,gSh_{\ell,g}^{S}hℓ,gS

denote the residual state under the complete substrate at layer ℓ\ellℓ and semantic-position group ggg.

Let:

hℓ,gCh_{\ell,g}^{C}hℓ,gC

denote the state under its counterfactual.

We intervene between these two computations and measure the final margin.

## 6.1 Forward restoration

Rℓ,g=M(C∣hℓ,gC←hℓ,gS)−M(C).\boxed{ R_{\ell,g} = M\left( C\mid h_{\ell,g}^{C} \leftarrow h_{\ell,g}^{S} \right)-M(C). }Rℓ,g=M(C∣hℓ,gC←hℓ,gS)−M(C).

This measures how much of the reference margin is recovered by transplanting the selected internal state.

## 6.2 Reverse disruption

Dℓ,g=M(S)−M(S∣hℓ,gS←hℓ,gC).\boxed{ D_{\ell,g} = M(S)- M\left( S\mid h_{\ell,g}^{S} \leftarrow h_{\ell,g}^{C} \right). }Dℓ,g=M(S)−M(S∣hℓ,gS←hℓ,gC).

This measures how much the reference margin changes when the corresponding counterfactual state is inserted.

For sufficiently large external effects, normalized recovery can be expressed as:

ρℓ,g=Rℓ,gΔMi.\rho_{\ell,g} = \frac{R_{\ell,g}}{\Delta M_i}.ρℓ,g=ΔMiRℓ,g.

These measurements characterize intervention-specific causal effects. They are not additive attributions of the output to individual tokens.

The full downstream network remains part of the patched computation.

# 7. Internal result I — A known semantic intervention becomes causally consequential across depth

The first result is the existing answer-position patching experiment in Llama-3.1-8B.

The untreated computation favors Walk, while the complete substrate moves the model toward Drive.

Transplanting the substrate-conditioned answer-position residual into the untreated computation begins to recover the intended final behavior around layers 14–16.

By approximately layer 16, the patched final margin crosses zero.

This establishes that the substrate-conditioned state at that depth is sufficient, under the remaining baseline computation, to change the eventual output preference.

It does not establish a discrete internal decision event.

Figure 3 — Answer-position causal response

Llama-3.1-8B: patched final margin by intervention layer

Foreground the causal patching curve. Direct vocabulary readout, if retained, is supplementary rather than the primary measurement.

# 8. Internal result II — Mapping an individual semantic constraint

The Llama-3.3-70B experiment provides a localized intervention.

With the complete standard substrate:

M(S)≈+6.1.M(S)\approx+6.1.M(S)≈+6.1.

Reversing rule 5 gives:

M(C)≈−3.4.M(C)\approx-3.4.M(C)≈−3.4.

The external behavioral effect is:

ΔM5≈9.5.\boxed{\Delta M_5\approx9.5.}ΔM5≈9.5.

We then perform activation transplantation between these two controlled conditions.

At earlier layers, the effect is recoverable primarily from the rule-5 token positions.

Across approximately layers 28–40, recoverability decreases at those source positions and increases at the final prediction position.

At later layers, transplanting the answer-position state recovers nearly the complete measured effect under the tested intervention protocol.

The forward-restoration and reverse-disruption maps exhibit broadly corresponding patterns.

This is a causal map of a known semantic treatment effect.

The semantic meaning of the experimental contrast was established before inspecting the activations.

The result does not require claiming that a single representation travels intact through the network or that every intermediate state has been decoded.

Figure 4 — Flagship internal result

Llama-3.3-70B: rule-5 restoration and disruption maps

Show the externally measured transition +6.1→−3.4+6.1\rightarrow-3.4+6.1→−3.4 alongside both layer-by-position maps. Explain which intervention produced every cell and distinguish causal recoverability from a verified communication pathway.

# 9. Internal controls — What happens when the intervention does not establish the intended transition?

This section is the important addition to the current spine.

The complete substrate shows what happens internally when an engineered semantic specification establishes the intended behavior.

We also have conventional interventions that do not establish the same transition.

Those are experimentally informative controls.

For each tested open-weight model, compare the baseline, a conventional intervention such as “Think step by step,” and the successful substrate.

Measure:

ΔMCoT=M(q,uCoT)−M(q)\Delta M_{\mathrm{CoT}} = M(q,u_{\mathrm{CoT}})-M(q)ΔMCoT=M(q,uCoT)−M(q)

and:

ΔMsubstrate=M(q,S)−M(q).\Delta M_{\mathrm{substrate}} = M(q,S)-M(q).ΔMsubstrate=M(q,S)−M(q).

Then map the internal response to each intervention using the same final-margin measurement.

The experiment distinguishes several possibilities: a conventional instruction may produce little output-relevant causal change, produce intermediate effects subsequently attenuated, or produce a substantial final-margin shift that nevertheless fails to cross the boundary.

The results should determine which description applies.

We must also distinguish an instruction to “think step by step” from a run in which the model actually generates an intermediate reasoning sequence.

## Why this matters

We have already authored the input interventions and know their intended semantic roles.

Therefore the internal experiment can compare changes associated with response-level instructions against changes associated with explicit task-satisfaction constraints.

This provides evidence about which properties of semantic input acquire causal influence over the operational preference.

It is not necessary to label the conventional intervention as internally ineffective merely because it failed to produce the desired categorical result.

Figure 5 — Conventional instruction versus semantic specification

Same model · same task · different controlled input interventions

Compare absolute final-margin effects and their internal causal maps. Do not normalize a near-zero conventional-prompt effect by its own near-zero denominator.

# 10. Cross-model measurement — Comparing internal responses to engineered behavioral change

The central methodological contribution is now stated explicitly.

A common task does not, by itself, establish a common behavior.

We first engineer a behavioral reference.

Then we study the model's response to a known intervention.

For a shared semantic treatment Δs\Delta sΔs, each model has its own measured external effect:

τm=Mm(S+)−Mm(S−).\tau_m = M_m(S^+)-M_m(S^-).τm=Mm(S+)−Mm(S−).

We then compare the within-model internal effects associated with that treatment.

This allows us to characterize different internal realizations of the same externally defined behavioral transition without requiring direct alignment of hidden-state coordinates.

The existing cross-model maps show clear intervention effects for the tested 70B and Qwen3-8B cases, with weaker or less interpretable effects in the tested 8B and 3B conditions.

However, the current maps sometimes ablate different semantic relations across models.

Those are valid separate intervention experiments, but they are not yet a controlled replication of one identical semantic perturbation across all architectures.

The stronger cross-model experiment will hold the semantic treatment constant across the compared models, while permitting their internal causal responses to differ.

The intended comparison is:

same semantic treatment+verified behavioral transition→compare internal causal response\boxed{ \text{same semantic treatment} + \text{verified behavioral transition} \rightarrow \text{compare internal causal response} }same semantic treatment+verified behavioral transition→compare internal causal response

This distinguishes engineered functional alignment from selecting naturally convergent model outputs.

# 11. Interpretation — From underspecification to causal control

Substrate Engineering begins with the operational observation that an underspecified task can admit different effective interpretations.

The engineering process identifies task-relevant relations, specifies them, and evaluates whether the resulting output becomes reproducible.

The internal experiments add a second level of description.

By removing or reversing a specified relation from an established substrate, we create a known semantic perturbation with a measured behavioral consequence.

Activation transplantation then identifies where the effects of that perturbation become causally consequential.

For example:

reverse task-satisfaction condition\text{reverse task-satisfaction condition}reverse task-satisfaction condition

↓\downarrow↓

ΔM≈9.5\Delta M\approx9.5ΔM≈9.5

↓\downarrow↓

depth-dependent causal recoverability.\text{depth-dependent causal recoverability}.depth-dependent causal recoverability.

This gives an experimental meaning to an output-relevant semantic degree of freedom.

It does not require assuming that multiple discrete interpretations are simultaneously represented inside the model.

Nor does it require identifying a unique word-level representation of each constraint.

The object being mapped is the relationship between the authored semantic variable, the resulting behavioral displacement, and the internal states through which that displacement can be recovered or disrupted.

# 12. Discussion and limitations

The paper distinguishes four forms of evidence that should not be collapsed into one claim.

Behavioral convergence establishes agreement over the tested outputs and conditions.

Decision-margin displacement establishes a continuous change in the measured preference under a specified intervention.

Behavioral ablation establishes dependence on an input constraint under the tested counterfactual.

Internal patching establishes the causal effects of transplanting selected activation states between those conditions.

The current experiments do not yet identify unique internal semantic features, establish a universal transfer pathway, or prove that the same mechanism is shared across models.

The reverse and physics-inversion results establish model-dependent behavioral responses to counter-directional specifications; they do not imply that every output can be imposed on every model.

The carwash task provides a controlled experimental setting. Mapping the behavior over a broader task domain remains a separate validation question.

The internal measurements are made on open-weight models. Behavioral results from closed models cannot be assumed to imply the same internal realization.

# 13. Conclusion

We first demonstrate that semantic input structure can be engineered to establish reproducible operational behavior across a declared set of otherwise divergent frozen language models.

The resulting behavioral consistency provides a fixed experimental reference.

We then systematically perturb the semantic constraints that maintain the reference, measure the resulting behavioral changes, and use activation transplantation to characterize their internal causal consequences.

By comparing conventional prompting interventions with task-semantic constraints, we begin identifying which properties of input structure acquire causal influence over the intended operational outcome.

By tracing individual semantic ablations through open-weight models, we show how experimentally defined changes in task specification become recoverable at different internal locations and depths.

The resulting approach connects behavioral reproducibility with controlled mechanistic measurement.

> We engineer consistency, perturb it under fixed conditions, and map what changes—externally in the output preference and internally in the computation that produces it.

