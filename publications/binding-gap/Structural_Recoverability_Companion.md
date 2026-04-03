# Structural Recoverability

This note sits alongside The Binding Gap as optional background rather than required scaffolding. The flagship essay stands on its own and makes a narrower claim: current language models exhibit a distinct, high-consequence family of binding-sensitive failures. This companion note offers the broader recoverability frame for readers who want it, and it also states where that larger frame currently stops.

Structural recoverability asks a sharper question than the usual argument about whether a model "knows" something. It asks what kind of structure training preserved, whether that structure remains recoverable through the system's own usable inference paths, and where the chain from representation to expression gives way when task demands change. The frame is promising. It is not yet a finished theory.

## The Missing Middle

Public discussion still swings between two bad pictures. One imagines the model as a library with a chat interface attached to the front. On that story, failure means the relevant content was never on the shelf. The other picture reacts by pointing to hidden states, probes, or embeddings and treating any decodable signal as proof that the knowledge is already there in full. That overcorrects. A trace can remain inside a system long after the architecture has lost a usable path back to the relation the task demands.

Structural recoverability names the missing middle between those pictures.

```text
encoded -> recoverable -> expressed
```

The ladder is ordered by operational strength. Encoded is the weakest category. It means training has left some regularity, trace, or representational residue behind. Recoverable is stronger. It means the system still preserves a usable path by which the relevant structure can be reconstructed in task-ready form. Expressed is stronger again. It means ordinary prompting and decoding surface that structure faithfully for the user.

That distinction matters because those levels often come apart. A model can encode a relation without keeping it recoverable under inversion. It can recover something under a special procedure and still fail to express it in routine interaction. Once that is clear, a large number of arguments about whether models "have" knowledge start collapsing for the right reasons.

## Recoverable Must Stay Narrow

The term only earns its keep if `recoverable` is kept strict. A clever observer can often decode surprising signals from activations or embeddings. That fact settles less than people think. If an external probe can excavate a label the model itself never brings to bear, what has been found may be residue rather than operational knowledge. Structural recoverability asks a harder question: can the architecture itself reassemble the needed relation in the form the task requires, or does that pattern remain available only to outside excavation?

That is why the relevant path can be broader than the default forward pass without becoming arbitrary. Retrieval support, a structured intermediate format, or another procedure native to the system may still count if the architecture can actually use it as part of its own computation. The line is practical rather than metaphysical. Recoverable does not mean "present somewhere." It means "still available for use under the task's demands."

This also marks the first hard limit of the idea. Recoverability under a method is not identical to knowledge in the form a downstream user cares about. An embedding can preserve information that ordinary inference never uses. A probe can decode a signal that plays no causal role in the model's own behavior. Structural recoverability is therefore not a certificate of hidden truth. It is an architectural question about whether the relation a task depends on remains stably available for the system's own use.

## Why Binding Comes First

The broader recoverability frame becomes useful only if it lands on a concrete case. Binding is the strongest such case now visible in the literature. In-context entity binding work shows that models solve simple pairing problems through internal machinery rather than through a vague cloud of semantic association (Feng and Steinhardt, 2023). Follow-up representational analysis goes further by identifying an ordering subspace that directly steers which attribute binds to which entity (Dai, Heinzerling, and Inui, 2024). Work on semantic roles pushes the same issue closer to ordinary language, where role information is present but not always strongly integrated into the broader representational geometry (Denning, Guo, Snefjella, and Blank, 2025; Aljaafari, Carvalho, and Freitas, 2025).

Wang and Sun make the strongest small-case argument. Their Reversal Curse result shows that a model can preserve the ingredients of a fact while failing to keep the relation in a form that survives a change in role assignment (Wang and Sun, 2025). Nothing new has to be learned when the relation flips. The same pair remains in play. What changes is the slot each entity must occupy at retrieval time. If a model cannot keep that relation stable through such a minimal transformation, then larger failures in factuality, attribution, and evidence extraction start to look less like isolated glitches and more like the same weakness under heavier load.

Tan and D'Souza show that the same pattern becomes much less forgivable in precision knowledge work (Tan and D'Souza, 2026). In evidence extraction for meta-analysis, the model may recognize the right entities, methods, and numbers while still failing to preserve the exact role assignments that connect them. Recognition remains too weak. The task only succeeds if the bindings stay intact while structural load rises. That is why the binding gap is the best-supported concrete member of the larger recoverability family.

## Correctness Is A Weak Witness

One reason the recoverability frame is educationally useful is that it explains why surface correctness is such a weak witness. Saynova et al. show that correct factual completions can arise through several different mechanisms, including exact recall, heuristics, guesswork, and generic language-model pressure (Saynova et al., 2024). A correct answer therefore does not show that the relevant relation was preserved in a stable, task-ready form. A wrong answer does not show that every useful trace has vanished either.

Once exact attachment enters the picture, the diagnostic question changes. It is no longer enough to ask whether the answer looked right. The sharper question is what kind of structure was stable enough to survive the retrieval and reconstruction demands of the task. That is the shift in vocabulary this note is trying to make available.

## Format, Provenance, And Other Pressures

The larger frame also helps organize several design trends that are often discussed as if they solved unrelated problems. Alternate intermediate formats matter because the medium changes what remains operationally available. Chen et al. show that models can sometimes reason or communicate more effectively when they are allowed to use structured alternatives such as tables, code-like forms, or logical notation (Chen et al., 2024). Hao et al. show a narrower version of the same point in continuous latent reasoning, where changing the medium of intermediate computation changes what remains live during search-heavy tasks (Hao et al., 2024). The lesson is not that language is obsolete. It is that interface format is part of the computation.

The same pressure appears in provenance and attribution. Xie et al. are useful because they treat citation as something that can be bound during training rather than stapled on after generation (Xie et al., 2025). That does not solve attribution in the abstract, but it sharpens the design question. Once a task demands faithful source attachment, the standard of success cannot stop at producing a plausible sentence. The system has to keep the answer tied to the structure that justifies it.

There is a matching caution on the representation side. Orgad et al. and Morris et al. both show, in different ways, that compact or latent states can preserve more recoverable structure than ordinary output behavior suggests (Orgad et al., 2024; Morris et al., 2023). That matters because it blocks the lazy inference from sparse expression to empty representation. It does not mean the system secretly "knows" everything it fails to say. It means outward failure is a weak witness to what remains encoded, which is exactly why the difference between encoded and recoverable has to be kept explicit.

## Stopping Point

This is where the companion note should stop. Binding is the strongest supported case. The larger structural recoverability frame is not yet equally well grounded across the full range of model failures it might want to organize.

The blocker is straightforward to state. A stronger theory would need a principled way to identify the same native inference path across meaning-preserving task changes such as role reversal, paraphrase, or format shift. Without that, `recoverable` can slide into a post-hoc label for success rather than a genuinely independent explanatory category. The current evidence is strong enough to justify the narrower claim that many high-consequence failures are binding-sensitive. It is not yet strong enough to establish structural recoverability as the master explanation for a wide terrain.

That limit is not a weakness in the note. It is the point of the note. The right educational use of structural recoverability is to give readers a disciplined larger frame, not to smuggle a grander thesis back into the flagship essay. If future mechanistic work shows that role-stable, recombinable representations predict where exact recovery survives and where it breaks, the frame can grow. If not, the narrower binding-gap claim remains the durable contribution.

## References

### Wang and Sun (2025): [Is the Reversal Curse a Binding Problem? Uncovering Limitations of Transformers from a Basic Generalization Failure](https://arxiv.org/abs/2504.01928)

The core anchor for the companion note. It makes reversal failure look like a structural binding problem rather than a simple data or prompting issue.

### Feng and Steinhardt (2023): [How do Language Models Bind Entities in Context?](https://arxiv.org/abs/2310.17191)

Important because it shows that entity-attribute binding is an internal, causally manipulable mechanism rather than a loose behavioral label.

### Dai, Heinzerling, and Inui (2024): [Representational Analysis of Binding in Language Models](https://arxiv.org/abs/2409.05448)

Useful because it identifies an ordering subspace that directly affects which entities bind to which attributes.

### Denning, Guo, Snefjella, and Blank (2025): [Do Large Language Models know who did what to whom?](https://arxiv.org/abs/2504.16884)

The key bridge from entity binding to semantic roles. It suggests that role information is present but weakly integrated into overall sentence representations.

### Aljaafari, Carvalho, and Freitas (2025): [Emergence and Localisation of Semantic Role Circuits in LLMs](https://arxiv.org/abs/2511.20910)

Supports the claim that semantic-role structure has compact, causally localized circuitry inside large models.

### Tan and D'Souza (2026): [Diagnosing Structural Failures in LLM-Based Evidence Extraction for Meta-Analysis](https://arxiv.org/abs/2602.10881)

The strongest heavy-load case. It shows that role assignment and numeric attachment degrade sharply once structured extraction becomes demanding.

### Saynova et al. (2024): [Fact Recall, Heuristics or Pure Guesswork? Precise Interpretations of Language Models for Fact Completion](https://arxiv.org/abs/2410.14405)

Essential for showing that output correctness is a weak witness to the mechanism that produced the answer.

### Chen et al. (2024): [Beyond Natural Language: LLMs Leveraging Alternative Formats for Enhanced Reasoning and Communication](https://arxiv.org/abs/2402.18439)

Supports the narrower point that interface format changes what remains operationally available.

### Hao et al. (2024): [Training Large Language Models to Reason in a Continuous Latent Space](https://arxiv.org/abs/2412.06769)

Useful as a bounded case where changing the medium of intermediate reasoning changes what remains computationally live.

### Xie et al. (2025): [CitePretrain: Scalable Citation-Enhanced Pretraining for LLMs](https://arxiv.org/abs/2506.17585)

Useful because it treats attribution as a problem of keeping provenance attached during training rather than only after generation.

### Orgad et al. (2024): [LLMs Know More Than They Show: On the Intrinsic Representation of LLM Hallucinations](https://arxiv.org/abs/2410.02707)

Important because it separates internal truthful encoding from outward error without turning that gap into a mystical theory of hidden knowledge.

### Morris et al. (2023): [Text Embeddings Reveal (Almost) As Much As Text](https://arxiv.org/abs/2310.06816)

A useful corrective against loose "lossy latent space" rhetoric. Compact representations can preserve far more recoverable structure than ordinary intuition suggests.
