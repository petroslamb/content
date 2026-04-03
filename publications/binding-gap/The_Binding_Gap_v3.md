# The Binding Gap

![Binding gap thesis](artifacts/slides/The_Binding_Gap_detailed/01_binding-gap-thesis.png)

Tell a language model that Tom Smith's wife is Mary Stone. Then ask who Mary Stone's husband is. Nothing new has been added. The same pair is still in play, the same relation, the same world. Yet performance often drops sharply. Boshi Wang and Huan Sun use this Reversal Curse to show something more serious than a missing benchmark skill. Current transformer models can retain the ingredients of a fact while failing to keep the relation in a form that survives a change in role assignment. The names remain available. The relation remains familiar. What gives way is the attachment that tells the system which entity belongs in which slot. The words survive. The binding does not.

![Relation reversal anomaly](artifacts/slides/The_Binding_Gap_detailed/02_relation-reversal-anomaly.png)

That failure deserves a more precise name than hallucination or ignorance. I will call it the binding gap: the class of failures in which a model preserves enough semantic material to sound close to correct while losing the exact attachment that makes the answer faithful. Inversion, reassignment, attribution, precise numerical reconstruction. The failure becomes visible exactly where these are required. The outputs that matter here are rarely absurd. They are annoyingly adjacent to truth. The model keeps the scene while dropping the wiring. It remembers the paper but misplaces the citation. It keeps the variable names but assigns the number to the wrong pair.

The binding gap names what goes wrong. The complementary term names what needs to hold. Exact binding is stable attachment of content to the role, source, or slot that makes it actionable. Which number belongs to which variable. Which claim traces to which paper. Who did what to whom. When exact binding holds, the output is faithful. When it breaks, the output drifts into the binding gap: plausible, fluent, structurally compromised.

Anyone who has debugged a model-assisted literature review has met this failure. The system returns confidently sourced claims where the source is real, the claim is real, and the attribution is wrong. Not fabricated. Misbound.

![Defining the binding gap](artifacts/slides/The_Binding_Gap_detailed/03_defining-the-binding-gap.png)

## Binding Is Real

This would be a weak essay if binding were only an external description laid over outputs after the fact. The literature now says more than that. Work on in-context entity binding shows that language models solve simple binding problems through an internal mechanism, not through a vague cloud of semantic association. Causal interventions on binding-related activations change pairing behavior directly. Follow-up representational analysis goes further and makes the machinery vivid. It identifies a low-rank ordering subspace that steers which attribute gets bound to which entity. The same physical box, described in the same context, can be made to contain the stone rather than the coffee by patching a single direction in activation space. The representation of the box does not change. The representation of the objects does not change. What changes is the binding between them. Attachment is a manipulable part of the model's internal geometry, not a metaphor.

![Binding as manipulable circuitry](artifacts/slides/The_Binding_Gap_detailed/05_binding-as-manipulable-circuitry.png)

Entity-attribute binding is a controlled setting. The harder question is whether the same fragility appears in ordinary language. It does. The smallest natural-language version of the binding problem is thematic role assignment: who did what to whom. For a human listener, role assignment is the dominant axis of sentence meaning. The difference between the dog bit the man and the man bit the dog reorganizes the entire mental scene, the entire set of consequences, the entire appropriate response. Recent work finds that large language models can extract agent and patient information, but that this role structure influences overall sentence representations far more weakly than it does in human cognition. The circuitry exists. Compact semantic-role mechanisms have been localized inside large models. But it does not dominate. Surface fluency can coexist with unstable attachment underneath. That is exactly the setting in which a binding gap opens.

![Fragility of thematic roles](artifacts/slides/The_Binding_Gap_detailed/06_fragility-of-thematic-roles.png)

Wang and Sun make the Reversal Curse informative because they add a concrete account of where the fragility comes from. On their view, reversal failure reflects two pressures in transformer representations: inconsistency, where the same entity is represented differently when it occupies different roles, and entanglement, where nearby concepts interfere with one another during learning and recombination. Their JEPA-based intervention matters because it turns the paper from diagnosis into evidence. The curse becomes less a benchmark oddity and more a design problem that can be reduced by architectural changes aimed at role-stable representations. That still falls short of a universal theory of model failure, but it is enough to establish that attachment is a tractable part of the mechanism.

## When Binding Load Rises

A concept built on a toy case becomes interesting only if the same failure shape reappears under more serious pressure. Zhiyin Tan and Jennifer D'Souza provide the strongest version of that scaling step. Their setting is evidence extraction for meta-analysis, where the task is to turn scientific prose into structured, numerically grounded study records. The difficulty here is not spotting isolated atoms. It is preserving the relations that make those atoms analytically usable: which variables are paired, which role each variable plays, which method produced which effect size, which conditions go with which result. Models perform moderately on single-property queries, then degrade sharply once the task requires stable binding between variables, roles, statistical methods, and effect sizes. Full association tuples are extracted with near-zero reliability.

What makes the paper so useful is the error pattern. The dominant failures are role reversals, cross-analysis binding drift, instance compression in dense result sections, and numeric misattribution. The papers are there. The variables are often recognized. The methods and numbers are often recognized as well. The collapse happens when they have to remain attached across local density and changing scope. A system that identifies the correct effect size but binds it to the wrong variable pair has not been almost right in any meaningful research setting. The output keeps enough of the structure to sound plausible while the exact attachment fails at the point where faithful use begins.

![Meta-analysis load collapse](artifacts/slides/The_Binding_Gap_detailed/07_meta-analysis-load-collapse.png)

These cases form a family. Reversal failure is exact binding under minimal transformation. Role confusion in sentence understanding is exact binding at the level of event structure. Meta-analysis extraction is exact binding under dense local structure and numeric load. The pattern is consistent: broad semantic material survives while exact role, source, or numeric attachment does not.

If the pattern is real, the same shape should appear wherever exact binding meets real stakes. A coding assistant that keeps variable names but assigns the return value to the wrong one. A legal summarizer that cites a real statute and attributes it to the wrong party. A clinical system that carries a valid diagnosis code to the wrong patient encounter. These are not confirmed members of the family in the way reversal and meta-analysis extraction are. They are predictions. If binding-gap analysis turns out to be the right lens for them, the concept is more general than the current evidence base alone can prove. If it does not, the borders drawn here still hold for the cases the evidence does cover.

## Borders

The concept earns its keep only if its borders stay clear. A retrieval miss is different: the needed evidence never enters the working context. A decomposition failure is different: the system heads into the wrong subproblem entirely. Generic hallucination is looser still: content untethered from any factual support, not miswired content that stays close. There is also a subtler neighbor. A model can fail after retrieval not because it miswired the content but because it ignored the retrieved passage almost entirely, defaulting to prior training instead of engaging the provided context. That is a context-use failure, not a binding failure. The binding gap is narrower: the content enters the computation enough that the answer stays near the mark, but the precise role, source, or numeric attachment does not survive. The binding gap requires all three marks: the relevant pieces are present enough that the answer feels close, the error becomes visible exactly when role, source, or numeric attachment matters, and the failure is not better explained by missing retrieval, ignored context, or solving the wrong subtask.

Surface correctness is a weak witness here. Denitsa Saynova and collaborators show that correct factual completions can arise through several distinct mechanisms, including exact recall, heuristics, guesswork, and generic language modeling pressure. A correct answer does not prove that the relevant relation was preserved in stable, task-ready form. This prevents the binding gap from hardening into a hidden-knowledge story. The claim is narrower: one specific failure family matters whenever attachment matters more than topical familiarity, and ordinary accuracy metrics can miss the difference entirely.

![Mirage of surface correctness](artifacts/slides/The_Binding_Gap_detailed/08_mirage-of-surface-correctness.png)

## What This Changes

Once the family is visible and its mechanistic roots are partly tractable, the productive question stops being whether the model knew the answer. It becomes whether the answer stayed attached to the structure the task required. That is a different question, and it leads to different engineering.

A retrieval pipeline that chunks documents by paragraph boundary can sever the binding between a result and the method that produced it. A workflow that summarizes a paper into free text before extracting structured fields forces every binding to survive two reconstruction passes instead of one. When a model carries its reasoning through free prose alone, bindings that a structured representation would keep explicit have to be reconstructed from context at each step. Format, in this light, is binding infrastructure. These are attachment failures with identifiable design causes, and they become visible only when you have a name for the pattern.

![Attachment-first architecture](artifacts/slides/The_Binding_Gap_detailed/09_attachment-first-architecture.png)

That leads to a wager sharp enough to be wrong. If the binding gap names a real and important family of failures, then binding-heavy tasks should break earlier and more consistently than broad topical tasks. Role reversal should expose weakness before open-ended explanation does. Source attribution should fail before generic summarization. Multi-field scientific extraction should collapse before simple entity spotting. Interventions that improve role stability, provenance attachment, or numeric grounding should buy their first serious gains on these tasks, before they make the model any better at producing generic fluent output. If those asymmetries do not appear, the concept is too loose or too ambitious. If they do appear, the productive gains will come not from packing more content into the weights but from keeping the right relations intact long enough to surface them faithfully.

The next time a model output looks almost right, the question worth asking is not whether the system knew enough. It is whether what it knew stayed wired to the slot the task required. If the answer is no, you are looking at the binding gap.

![Architectural pressures and binding wager](artifacts/slides/The_Binding_Gap_detailed/10_architectural-pressures-and-binding-wager.png)

Companion note: [Structural Recoverability](Structural_Recoverability_Companion.md). This optional background note develops the broader `encoded -> recoverable -> expressed` frame behind the essay and states where that larger argument currently stops.

## References

### Wang and Sun (2025): [Is the Reversal Curse a Binding Problem? Uncovering Limitations of Transformers from a Basic Generalization Failure](https://arxiv.org/abs/2504.01928)

The essay's opening anchor. It connects reversal failure to inconsistency and entanglement in conceptual binding and shows that targeted architectural changes can reduce the failure.

### Feng and Steinhardt (2023): [How do Language Models Bind Entities in Context?](https://arxiv.org/abs/2310.17191)

Important because it shows that entity-attribute binding is an internal, causally manipulable mechanism rather than a loose behavioral label.

### Dai, Heinzerling, and Inui (2024): [Representational Analysis of Binding in Language Models](https://arxiv.org/abs/2409.05448)

Sharpens the mechanistic side of the essay by identifying an ordering subspace that directly affects which entities bind to which attributes.

### Denning, Guo, Snefjella, and Blank (2025): [Do Large Language Models know who did what to whom?](https://arxiv.org/abs/2504.16884)

The key bridge from entity binding to semantic roles. It suggests that role information is present but weakly integrated into overall sentence representations.

### Aljaafari, Carvalho, and Freitas (2025): [Emergence and Localisation of Semantic Role Circuits in LLMs](https://arxiv.org/abs/2511.20910)

Supports the claim that semantic-role structure has compact, causally localised circuitry inside large models.

### Tan and D'Souza (2026): [Diagnosing Structural Failures in LLM-Based Evidence Extraction for Meta-Analysis](https://arxiv.org/abs/2602.10881)

The serious extension case. It shows that failures under role, method, and effect-size attachment are not reducible to simple entity-recognition errors.

### Boulos et al. (2026): [RAG-X: Systematic Diagnosis of Retrieval-Augmented Generation for Medical Question Answering](https://arxiv.org/abs/2603.03541)

Useful because it separates retrieval failures from generator-side failures and helps define what a binding-gap case is not.

### Pandey (2026): [Can Small Language Models Use What They Retrieve? An Empirical Study of Retrieval Utilization Across Model Scale](https://arxiv.org/abs/2603.11513)

Useful for boundary-setting. It shows that some post-retrieval failures are really context-utilization failures rather than binding-sensitive misattachment.

### Saynova et al. (2024): [Fact Recall, Heuristics or Pure Guesswork? Precise Interpretations of Language Models for Fact Completion](https://arxiv.org/abs/2410.14405)

The discipline section's key paper. It shows that surface correctness is a weak witness to the mechanism that produced the answer.
