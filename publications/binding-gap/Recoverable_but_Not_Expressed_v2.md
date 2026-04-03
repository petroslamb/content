# The Binding Gap

Relation reversal is such a small failure that it is easy to miss what it reveals. Give a language model the fact that Tom Smith's wife is Mary Stone. Then ask for the reverse relation. If the system had really learned the pair in a structurally stable way, the second query should be trivial. Yet performance often collapses. Boshi Wang and Huan Sun use this Reversal Curse to show something more serious than a missing benchmark skill. Current models can absorb a fact in one orientation and still fail when the same content has to be recovered under a different role assignment. The words survive. The binding does not.

That matters because it breaks two bad pictures at once. The first imagines the model as a library with a chat box bolted to the front. On that story, failure means the relevant book was never on the shelf. The second reacts by pointing to hidden states, probes, or embeddings and treating any decodable signal as proof that the knowledge is already there in full. That overcorrects. A pattern can leave a trace inside a model without remaining available in the form a task requires. The decisive question is whether the system can still recover the relevant structure when the task changes its demands.

That is the missing middle in the usual vocabulary:

```text
encoded -> recoverable -> expressed
```

Encoded is the weakest category. It means training has left some internal regularity or representational trace behind. Recoverable is stronger. It means the system still has a usable path by which the relevant structure can be reconstructed in task-ready form, whether through the default forward pass, retrieval support, a better intermediate format, or another procedure the architecture can actually work with. Expressed is stronger again. It means ordinary prompting and decoding surface that structure faithfully for the user. These levels often come apart. A model can encode a relation without keeping it recoverable under inversion. It can recover something under a special procedure and still fail to express it in routine interaction.

The distinction only becomes useful if `recoverable` is kept narrow. A clever observer can often decode surprising signals from activations or embeddings. That fact, on its own, settles less than people think. If an external probe can excavate a label the model itself never brings to bear, what has been found may be residue rather than operational knowledge. Structural recoverability asks for something stricter: a path the architecture can actually use to reassemble the needed relation in the form the task demands. The real test is practical. Can the system bring that pattern to bear as part of its own computation, or does it remain available only to outside excavation?

Once the problem is stated that way, a large class of model failures stops looking mysterious. Many near misses are not cases of total ignorance. They are failures of exact binding. The model keeps the semantic neighborhood of a fact while losing the precise attachments that make the answer faithful. Who did what to whom. Which date belongs to which event. Which number modifies which variable. Which citation supports which sentence. The broad shape survives. The bound form does not. That is why a system can sound uncannily close to correct while remaining unreliable exactly where the task becomes serious.

The Reversal Curse is the smallest clean example because it strips the issue down to bare structure. Nothing new has to be learned when the relation flips. The same pair is still in play. What changes is the role each entity must occupy at retrieval time. Wang and Sun argue that this exposes a binding problem in transformer generalization rather than a mere shortage of examples. Their point matters beyond toy reversals. If a model cannot keep a relation stable under such a minimal transformation, then higher-level failures in factuality, attribution, or evidence extraction start looking less like isolated glitches and more like larger versions of the same architectural weakness.

This is why correct answers can be so misleading as an evaluation target. Denitsa Saynova and her collaborators show that factual completions can arrive through several different mechanisms. Sometimes the model is recalling the fact. Sometimes it is leaning on shallow heuristics. Sometimes it is guessing its way through a prompt that happens to point in the right direction. Output correctness alone does not tell you which structure the model actually used. A correct answer can hide a weak internal route just as easily as a wrong answer can hide a stronger one. Once exact binding enters the picture, the question shifts from "did it get the answer right?" to "what kind of structure was stable enough to survive retrieval?"

Zhiyin Tan and Jennifer D'Souza push the same issue into a setting where failure is harder to romanticize. In evidence extraction for meta-analysis, the model may recognize the right entities and local claims while still failing to preserve the role assignments that connect interventions, measurements, and effect sizes. That is a more unforgiving environment than an isolated trivia question, but the underlying pattern is familiar. Recognition and coarse semantic presence still fall short here. The task only succeeds if the bindings remain intact across dense local structure. In that sense, precision knowledge work reveals the same weakness that reversal tasks reveal, only under a heavier load.

From here the discussion of interface format stops being cosmetic. Natural language is the public medium of current systems because humans need readable outputs, inspectable reasoning, and collaborative workflows. It is an extraordinary interface for all of that. It is also a selective one. Weize Chen and colleagues show that models can sometimes reason or communicate more efficiently when they are allowed to choose structured alternatives such as tables, code-like forms, or logical notation. Coconut reports something similar in a narrower setting, where continuous latent reasoning helps preserve multiple live alternatives on search-heavy tasks that textual chains tend to flatten into a single sequence too early. The durable lesson is modest and important. Format changes what remains recoverable. The medium is part of the computation, not just a wrapper around it.

None of this licenses the usual frontier fantasies. The evidence here does not say that language is obsolete, or that models are secretly thinking in a hidden inner code that text merely corrupts on the way out. Its force is more practical. Every interface favors some recoveries and obstructs others. If a task demands public accountability, source inspection, and collaboration with humans, natural language remains the right surface even when it is not the most efficient internal format. If a task demands stable branching, dense role assignment, or compression of repeated structural motifs, forcing every intermediate state through ordinary prose can make recovery harder than it needs to be. The tradeoff is architectural, not metaphysical.

Seen from this angle, several current system trends line up in a cleaner way. Retrieval, memory hierarchies, citation-aware pretraining, and alternate intermediate formats are often discussed as if they solved unrelated problems. In practice they answer a common pressure: how to keep the right structures recoverable under finite compute, limited context, and human-facing interfaces. Compression still belongs in the story, but farther back than people usually place it. Finite systems always have to select what survives with high fidelity and what is left at a coarser grain. That background pressure helps explain why broad semantic structure often lasts longer than exact bound form. It cannot by itself tell you which relations will remain usable when a task demands inversion, attribution, or role stability. For that, structural recoverability is the sharper question.

Xie and collaborators make this concrete with citation-aware pretraining. Their work matters less because it promises a total replacement for retrieval than because it treats provenance as something that can be bound during training rather than stapled on after generation. That is a narrow but revealing move. Once a task demands faithful source attachment, the standard of success cannot stop at producing a plausible sentence. The system has to keep the answer tied to the structure that justifies it. The same point appears from another direction in work on embeddings and compact representations. John Morris and his collaborators show that latent representations preserve far more recoverable surface form than casual talk about "lossy compression" suggests. A compact state can hold onto more structure than the default output path reliably exposes. Sparse or unreliable expression does not imply an empty representation.

The strongest objection is also the one that keeps this frame honest. Recoverability under a method is not identical to knowledge in the form a downstream user cares about. A probe can decode a signal that plays no causal role in the model's own behavior. An embedding can preserve information that ordinary inference never uses. A correct answer can emerge from heuristics rather than faithful recall. None of that weakens the essay's central claim. It specifies it. Structural recoverability is not a metaphysical certificate that hidden truth exists inside the model waiting to be liberated. It is an architectural question about which relations remain stably available for use, under which procedures, and where those relations break before reaching the interface.

That narrower claim is enough to reorganize how current models look. The familiar question asks whether the model "knows" a fact. The better question asks what kind of structure the system preserved, whether that structure remained recoverable in the form the task required, and where the chain from representation to expression gave way. In that frame, some failures that look like ignorance turn out to be binding failures. Some successes that look like knowledge turn out to be heuristics riding prompt cues. Some architectural gains come not from packing more content into the weights, but from keeping the right relations intact long enough to surface them faithfully. The frontier then looks less like a race to build larger archives and more like a race to build systems that can keep their own structure attached.

## References

### Wang and Sun (2025): [Is the Reversal Curse a Binding Problem? Uncovering Limitations of Transformers from a Basic Generalization Failure](https://arxiv.org/abs/2504.01928)

The essay's opening example and strongest mechanistic anchor. The paper makes reversal failure look like a structural binding problem rather than a superficial data issue.

### Orgad et al. (2024): [LLMs Know More Than They Show: On the Intrinsic Representation of LLM Hallucinations](https://arxiv.org/abs/2410.02707)

Important because it separates internal truthful encoding from outward error without turning that gap into a mystical theory of hidden knowledge.

### Morris et al. (2023): [Text Embeddings Reveal (Almost) As Much As Text](https://arxiv.org/abs/2310.06816)

A useful corrective against loose "lossy latent space" rhetoric. Compact representations can preserve far more recoverable structure than ordinary intuition suggests.

### Saynova et al. (2024): [Fact Recall, Heuristics or Pure Guesswork? Precise Interpretations of Language Models for Fact Completion](https://arxiv.org/abs/2410.14405)

Essential for blocking the lazy move from output correctness to factual recall. Correct answers can emerge through distinct mechanisms.

### Tan and D'Souza (2026): [Diagnosing Structural Failures in LLM-Based Evidence Extraction for Meta-Analysis](https://arxiv.org/abs/2602.10881)

Extends exact binding failure from toy examples into precision extraction work, where role assignment and relational fidelity actually decide success.

### Chen et al. (2024): [Beyond Natural Language: LLMs Leveraging Alternative Formats for Enhanced Reasoning and Communication](https://arxiv.org/abs/2402.18439)

The cleanest support for the claim that interface format is part of the computation rather than merely presentation.

### Hao et al. (2024): [Training Large Language Models to Reason in a Continuous Latent Space](https://arxiv.org/abs/2412.06769)

Useful as a bounded case where changing the medium of intermediate reasoning changes what remains computationally live.

### Xie et al. (2025): [CitePretrain: Scalable Citation-Enhanced Pretraining for LLMs](https://arxiv.org/abs/2506.17585)

Shows that attribution can be framed as a training-time binding problem, not only as a post-hoc retrieval accessory.
