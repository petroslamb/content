# Recoverable but Not Expressed

Relation reversal is one of the cleanest failure modes in current language models. Give a model a fact in one direction, then ask for the same fact in reverse. The content has not changed. Only the roles have. Yet performance often drops sharply. Boshi Wang and Huan Sun use this Reversal Curse to expose a basic limit in transformer generalization. A model can handle "A's mother is B" and still fail on "Whose son is B?" That matters because it rules out an easy story. The fact is present, yet the relation is not structurally available when the query changes its demands.

Public discussion still swings between two bad pictures. In one, the model is a library with a chat interface attached to the front. In the other, hidden states are treated as if their mere existence settles the question of understanding. Neither picture is useful. Large models are trained under finite budgets. They preserve some structure, discard some detail, and route what remains through a narrow public interface. The useful question is simpler and harder at the same time: what do they encode, what can still be recovered from that encoding, and what does ordinary inference actually make available?

That gives a cleaner frame for the current generation of systems:

```text
encoded -> recoverable -> expressed
```

Encoded means the internal state carries the relevant structure. Recoverable means some procedure, probe, format change, retrieval path, or alternate generation process can draw that structure back out. Expressed means default prompting and decoding actually do so. These are not three sealed chambers. They are three increasingly demanding tests. A system can fail the last one without fully failing the first two. Once that is clear, many familiar arguments about "knowledge" stop collapsing into one vague category.

This is where structural recoverability becomes the right center. The important question is less what the model compresses or stores than which structures remain accessible under real task pressure. Hadas Orgad and colleagues show that large language models can internally represent truthful answers even when their surface outputs hallucinate. Jiahai Feng, Stuart Russell, and Jacob Steinhardt show something similar in a narrower synthetic setting, where propositional probes can recover faithful latent world states from models whose behavior is not always faithful. John Morris and coauthors complicate the usual rhetoric from the other side: embeddings preserve far more recoverable surface form than the casual story about "lossy latent space" suggests. Taken together, these results do not prove that models possess hidden truth waiting to be extracted at will. They support a narrower and more useful claim. Output is not the boundary of what the system still makes accessible.

Call the distortion between recoverable and expressed `expression pressure`. It is the pressure introduced when encoded structure has to pass through ordinary token-level inference, local decoding choices, and a public interface built for readable language rather than faithful reconstruction. That pressure does not create every error. It does create a recognizable class of errors in which the model keeps the broad shape of a problem while failing to surface the exact relation the task demands.

## Exact Binding

The value of this frame appears most clearly when a task demands exact binding rather than broad topical competence. A system may preserve the outline of an event while failing to recover who did what to whom, which date belongs to which claim, or which source supports which sentence. That is a different problem from total ignorance. It is a failure of exact attachment.

The Reversal Curse is the smallest version of this problem. The model has enough structure to answer one direction of the relation, yet cannot reliably invert the roles when the query asks for the reverse direction. The same pattern appears at larger scale. Denitsa Saynova and collaborators show that correct factual completions can arise from several different mechanisms, only one of which is genuine parametric fact recall. A correct answer is not enough to tell you what kind of structure the model actually used. Zhiyin Tan and Jennifer D'Souza push the point into a setting where precision matters. In meta-analysis extraction, models can recognize entities and local facts while failing to preserve the relational bindings that connect variables, methods, and effect sizes across dense scientific text. The entity is there. The structure is not stable enough to survive the task.

That is why so many model failures feel eerily near the mark. The abstraction often survives while the binding fails. A model may carry the semantic neighborhood of a fact while missing the exact statute, citation, quotation, or numerical role assignment that would make the answer faithful. This is also why blanket talk about hallucination quickly stops helping. Some hallucinations are retrieval failures. Some are reward-shaping problems. Some come from poor decomposition. Some are binding failures produced by coarse recovery from a prior that is structurally insufficient for the exact form the task requires. The useful move is not to force every mistake into one cause. It is to ask which kind of structure the task demanded, and whether the system could still recover it in bound form.

## Format Is Not Neutral

Once recoverability moves to the center, interface format stops looking cosmetic. Natural language is the default public medium because it is the only medium humans can read at scale. It remains a strong interface for flexible communication, but not an automatically neutral one, and not always the best medium for preserving every live distinction inside a model's working state.

Weize Chen and collaborators show that language models can often reason or communicate more efficiently when allowed to choose structured alternatives such as tables, logical forms, or code-like formats. The gain is operational rather than metaphysical. A better format can carry the same content with less distortion and less overhead. Coconut pushes the point a bit further. On search-heavy tasks, continuous latent reasoning can preserve multiple live alternatives that ordinary textual chains force into premature sequence. The result is interesting, but it should be kept on a short leash. It does not prove that language is obsolete, or that models possess a hidden inner language waiting to be revealed. It supports a narrower claim: representational format shapes which distinctions remain recoverable and which ones get flattened during expression.

That is the right way to talk about serialization. Text is not inherently bad. Every interface simply favors some recoveries and obstructs others. If the task requires stable branching, dense role assignment, or precise structural carryover, then forcing all intermediate state through ordinary language can distort the computation. If the task requires public accountability, collaboration with humans, or explicit source inspection, then language remains the right medium even when it is not the most efficient one. The medium is part of the system design, not just packaging.

## Design Under Pressure

This shifts the architecture question into a cleaner form. The real design problem is keeping the right structures recoverable under constraints of cost, latency, memory, and interface, rather than trying to pack ever more world content into one parametric body until it resembles a universal archive. Once the frame is stated that way, retrieval systems, memory hierarchies, attribution mechanisms, and alternate formats all start looking like related responses to the same engineering problem.

Compression still belongs in the story, but farther back than before. Finite compute forces selection. Models cannot preserve every feature of the training stream at equal fidelity. That background pressure explains why coarse semantic structure often survives where exact recovery does not. It does not, by itself, explain which structures remain accessible when the task changes, or which failures arise from the gap between stored regularity and usable reconstruction. Compression is the selection regime. Structural recoverability is the operational question.

This is also where provenance becomes interesting again. CitePretrain matters less as a replacement for retrieval than as a demonstration that attribution can be treated as a training-time binding problem rather than a purely post-hoc system add-on. The paper asks whether facts can be learned together with persistent document identifiers so that source linkage becomes more directly recoverable at inference time. That is a narrow technical move, but it points in the right direction. When a task demands exact source attachment, the system should not be judged only by whether it can generate a plausible answer. It should be judged by whether the answer remains recoverably tied to the structure that justifies it.

The upper-bound work on embedding capacity sharpens the point from another side. A surprisingly large amount of surface form can be packed into compact representations and recovered later under heavy optimization. That does not mean current models use those representations this way in ordinary inference. It means the ordinary output path is often a weak witness to what remains structurally available in principle. Once again, the important distinction is not between "stored" and "not stored." It is between what is encoded, what can still be recovered with a specific procedure, and what the default interface routinely surfaces.

## What This Lens Does Not Solve

This frame earns its keep only if it stays narrow. It does not settle whether a probing method has accessed genuine knowledge or a useful correlate of knowledge. That is the deepest objection, and it should be taken seriously. A probe can show recoverability under a method. It cannot, on its own, prove that the recovered structure is identical to the form of knowledge a downstream user cares about. For the same reason, a correct answer cannot prove that the model used genuine factual encoding rather than heuristic pattern completion. The right conclusion is diagnostic rather than triumphalist. Surface behavior and internal recoverability come apart often enough that neither one should be treated as the whole story.

Nor does this lens explain planning, agency, social reasoning, or tool use by itself. It does not tell us how a model ought to be aligned. It does not turn every near miss into hidden truth. What it does give is a better vocabulary for a large and growing class of failures that current public language still handles poorly. Instead of asking whether the model "knows" something, we can ask what it encoded, what remained structurally recoverable, what the interface demanded, and where exact binding broke. The claim is smaller than a theory of intelligence, and stronger for that reason.

## References

### Chen et al. (2024): [Beyond Natural Language: LLMs Leveraging Alternative Formats for Enhanced Reasoning and Communication](https://arxiv.org/abs/2402.18439)

Chen et al. show that allowing language models to select structured formats can improve efficiency and sometimes improve task performance. The paper matters here because it makes format choice look like a real design variable rather than decorative wrapping.

### Feng, Russell, and Steinhardt (2024): [Monitoring Latent World States in Language Models with Propositional Probes](https://arxiv.org/abs/2406.19501)

Feng and colleagues show that faithful latent world states can remain recoverable even when outward behavior is not perfectly faithful. The paper is narrow, but it gives the recoverability claim a clean experimental form.

### Hao et al. (2024): [Training Large Language Models to Reason in a Continuous Latent Space](https://arxiv.org/abs/2412.06769)

Hao and collaborators show that continuous latent reasoning can outperform textual reasoning on some search-heavy tasks. The paper matters here because it supports a narrow claim about format-sensitive computation rather than a broad anti-language thesis.

### Kuratov et al. (2025): [Cramming 1568 Tokens into a Single Vector and Back Again: Exploring the Limits of Embedding Space Capacity](https://arxiv.org/abs/2502.13063)

Kuratov and collaborators show that compact representations can retain far more recoverable information than ordinary inference exposes. The paper matters because it separates upper-bound recoverability from normal model behavior.

### Morris et al. (2023): [Text Embeddings Reveal (Almost) As Much As Text](https://arxiv.org/abs/2310.06816)

Morris and collaborators show that compact embeddings preserve much more recoverable surface form than casual latent-space rhetoric suggests. The paper is a useful corrective against sloppy talk about compression as simple erasure.

### Orgad et al. (2024): [LLMs Know More Than They Show: On the Intrinsic Representation of LLM Hallucinations](https://arxiv.org/abs/2410.02707)

Orgad et al. argue that models can internally represent truthful answers even when their generated outputs hallucinate. The key contribution is not hidden truth in the abstract, but the sharper separation between recoverable internal structure and ordinary expression.

### Saynova et al. (2024): [Fact Recall, Heuristics or Pure Guesswork? Precise Interpretations of Language Models for Fact Completion](https://arxiv.org/abs/2410.14405)

Saynova and collaborators show that correct factual outputs can arise through different mechanisms, only one of which is genuine fact recall. The paper matters because it blocks the lazy assumption that output correctness directly reveals the kind of structure the model used.

### Tan and D'Souza (2026): [Diagnosing Structural Failures in LLM-Based Evidence Extraction for Meta-Analysis](https://arxiv.org/abs/2602.10881)

Tan and D'Souza show that models can recognize entities yet fail to preserve the relational bindings needed for reliable evidence extraction. Their paper brings exact binding failure out of toy settings and into precision knowledge work.

### Wang and Sun (2025): [Is the Reversal Curse a Binding Problem? Uncovering Limitations of Transformers from a Basic Generalization Failure](https://arxiv.org/abs/2504.01928)

Wang and Sun use reversal failure to expose a basic structural weakness in transformer generalization. Their paper provides the essay's cleanest opening example because it isolates binding failure without hiding behind broad benchmark aggregates.

### Xie et al. (2025): [CitePretrain: Scalable Citation-Enhanced Pretraining for LLMs](https://arxiv.org/abs/2506.17585)

Xie and collaborators treat attribution as a binding problem that can be engineered during training rather than added only after the fact. The paper matters because it makes provenance look like a recoverability question, not just a retrieval accessory.
