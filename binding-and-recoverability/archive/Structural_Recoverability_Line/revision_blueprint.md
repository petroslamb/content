# Revision Blueprint

This file is the control document for the next major revision of the essay. It is not draft prose. Its purpose is to lock the conceptual center, record what changed after the research pass, and make the next revision pass decision-complete.

## North Star

The goal is to produce an ideas essay that changes the reader's operating vocabulary, not a literature review.

The essay must introduce a conceptual move strong enough to reorganize how the reader thinks about modern models, their strengths, and their failures.

The locked center is `structural recoverability`, expressed through the working distinction `encoded vs recoverable vs expressed`, with `exact binding` as the strongest public-facing failure mode and medium or format effects as the main subordinate branch.

## Current Diagnosis

- `compression` drifts across meanings in the current draft: coding-theoretic efficiency, internal abstraction, architecture, and deployment economics.
- `latent meaning` oversells the delivered payload. The draft says something narrower and stronger than the title implies.
- factuality is the strongest existing branch because it already points toward the difference between coarse semantic structure and exact required recovery.
- breadth currently exceeds explanatory force. Too many domains are touched before the main idea has fully earned its authority.

## What Changed From The Previous Frame

- The prior framing treated `compression` as the leading noun. The revision demotes compression to background mechanism.
- The center is no longer just mismatch between internal state and output. It is `structural recoverability`: what remains accessible under specific procedures, and what default inference still fails to express.
- The research pass moved `exact binding` from a late application to the decisive failure mode that reveals the architecture.
- The opening example is now locked: the Reversal Curse, not generic hallucination.
- The language branch survived, but only as a medium or format argument. It is no longer allowed to pose as the master theory of the essay.

## Revised Conceptual Core

`encoded`
: what the model internally represents, whether or not that content is cleanly available through direct prompting.

`recoverable`
: what can be reconstructed from the model's internal state under the right interface, probing method, retrieval path, or generation procedure.

`expressed`
: what the model actually emits through the default output channel under ordinary prompting and decoding.

`exact binding`
: recovery of the exact task-required form such as a date, quote, citation, document identifier, entity-role assignment, or other source-bound detail.

`serialization loss`
: degradation introduced when richer internal structure is forced through a narrower interface such as natural language tokens, coarse tokenization, or shallow summary channels.

`structural recoverability`
: the extent to which encoded information can be reliably recovered under specific conditions, given architectural constraints on binding, role consistency, and interface format.

`expression pressure`
: the systematic distortion introduced when encoded structure must pass through ordinary token-level inference and decoding.

## Locked Thesis Direction

Modern AI models are best understood not as systems that simply compress or store information, but as systems with three separable representational levels: what they encode, what their architecture allows them to structurally recover, and what they actually emit under standard inference. Their most revealing successes and failures occur at the gaps between those levels.

Why this is locked:

- It keeps the useful part of the earlier recoverability frame while adding the missing qualifier: not all recoverability is structural or stable.
- It survives the inversion and reversibility pressure better than a naive `lossy latent` story.
- It turns the essay from a descriptive mismatch story into an architectural claim with predictable failure modes.

Frames that are now demoted:

- `compression` as headline noun
- `latent meaning` as title-level center unless the essay earns it far more rigorously
- `language bottleneck` as master theory
- `models know more than they say` when used without the stronger structural qualifier

## Working Thesis Sentence

What large language models encode, what their architecture allows them to structurally recover, and what they actually emit under standard inference form three separable representational levels; the gaps between them are not random noise but systematic pressure points where binding limits and serialization constraints determine which knowledge reaches the interface.

## Research Findings That Matter

### Internal Knowledge Exceeds Default Expression

- Several lines of work suggest models often internally encode more truthful or structured information than they reveal through ordinary outputs.
- This does not prove reliability. It does prove that output failure is not always identical to representational absence.
- This bucket materially strengthens the move from generic compression-talk to the sharper triplet of encoded, recoverable, and expressed.

Key papers:
- `2406.19501` propositional probes
- `2410.02707` LLMs know more than they show
- `2312.01037` ELK
- `2312.03729` cognitive dissonance
- `2410.14405` fact recall vs heuristics vs guesswork

### Alternative Interfaces Can Outperform Natural Language

- Natural language is not always the most efficient or faithful medium for internal reasoning or inter-agent transfer.
- Continuous latent reasoning, structured non-natural-language formats, and direct cache or latent transfer often improve performance or efficiency.
- This bucket supports a strong subordinate argument about interface choice, but not a universal anti-language thesis.
- Three adjacent sub-branches remain worth tracking but not centering yet: physical action-space transfer in robotics, latent-space prompt optimization, and entropy-style measurements of hidden representational density.

Key papers:
- `2412.06769` Coconut
- `2402.18439` AutoForm
- `2511.09149` Interlat
- `2511.20639` LatentMAS
- `2510.03215` Cache-to-Cache
- `2510.27688` CALM
- `2505.16552` CoLaR

### Exact Binding And Attribution Are Distinct Bottlenecks

- Many failures are not global ignorance but failures to recover source-bound, role-bound, or citation-bound detail in exact form.
- This is the strongest bridge between the essay's conceptual core and public-facing reliability questions.
- Attribution and evidence extraction work help sharpen the difference between general semantic shape and exact bound recovery.

Key papers:
- `2512.10791` FACTS
- `2305.14251` FActScore
- `2411.04368` SimpleQA
- `2509.07968` SimpleQA Verified
- `2506.17585` Cite Pretrain
- `2502.09604` SelfCite
- `2601.00821` CogCanvas
- `2602.10881` structural failures in evidence extraction

### Tokenization And Representation Format Shape What Becomes Recoverable

- The bottleneck begins before reasoning if the input representation itself breaks meaningful structure into dead fragments.
- Tokenization, vocabulary design, and compact representation format influence what later becomes easy or hard to recover.
- This bucket adds depth to the interface argument and prevents the essay from treating the output channel as the only bottleneck.

Key papers:
- `2511.14365` tokenization bottleneck in chemistry
- `2501.16975` Over-Tokenized Transformer
- `2406.17378` text embeddings align with key tokens
- `2310.06816` Vec2Text
- `2506.15001` memory tokens

## Priority Papers

- `2504.01928` Reversal Curse line
  Why it matters: is now the paradigmatic worked example because it isolates structural binding failure in a minimal and reproducible way.

- `2410.02707` LLMs Know More Than They Show
  Why it matters: anchors the claim that output failure is not identical to representational absence.

- `2310.06816` Text Embeddings Reveal (Almost) As Much As Text
  Why it matters: blocks sloppy `lossy latent` rhetoric by showing how much surface form remains recoverable.

- `2402.18439` Beyond Natural Language
  Why it matters: proves that medium and format choice is a genuine system-design variable rather than neutral packaging.

- `2410.14405` Fact Recall, Heuristics or Pure Guesswork?
  Why it matters: shows that accuracy can be mechanistically heterogeneous and therefore cannot stand in for genuine factual encoding.

- `2602.10881` Diagnosing Structural Failures in LLM-Based Evidence Extraction for Meta-Analysis
  Why it matters: extends exact binding from toy examples into precision knowledge work where structural fidelity really matters.

- `2406.19501` Monitoring Latent World States in Language Models with Propositional Probes
  Why it matters: provides a bounded but useful case where faithful internal state survives unfaithful output.

- `2502.13063` Cramming 1568 Tokens into a Single Vector and Back Again
  Why it matters: serves as an upper-bound pressure test on how much can remain recoverable even when ordinary expression does not use that capacity.

## Branches To Keep / Reframe / Cut

### Keep

- structural recoverability as the essay's center
- exact binding as the key failure mode
- medium and format effects as the main supporting branch
- architecture under budget only insofar as it explains how systems improve or fail recoverability

### Reframe

- language bottleneck
  Reframe as interface loss or expression pressure, not as a universal declaration that text is inherently inferior in all settings.

- continuous latent reasoning
  Reframe as a task-sensitive advantage in search-heavy settings, not as a categorical successor to language reasoning.

- attribution training
  Reframe as a specific demonstration that provenance can be architected into training, not as a replacement for retrieval.

- probing and internal-state papers
  Reframe as evidence about recoverability under specific procedures, not as proof of hidden knowledge in an unqualified sense.

- physical modality gap, latent prompt optimization, and entropy-profile work
  Reframe as peripheral extensions until they materially improve the flagship argument.

### Cut Or Demote

- dark-matter and ID-vector speculation
- latent communication as an active solution branch
- `compression equals intelligence` as a standalone thesis
- broad claims that every hallucination is a compression artifact
- `models know more than they say` when that phrase is doing more work than the evidence supports
- any implication that embeddings are bijective or that internal attribution replaces RAG

## Argument Architecture

1. Open with the Reversal Curse as the diagnostic symptom: a minimal case where data sufficiency and structural failure cleanly separate.
2. Introduce the three-level distinction: encoded, recoverable, and expressed.
3. Establish the mechanism with exact binding failures:
   use `2504.01928` and, if needed, `2602.10881`.
4. Show that serialization format is a design variable:
   use `2402.18439` to prove that interface choice changes what can be cleanly expressed.
5. Clarify the evaluation confusion:
   use `2410.14405` to show that correct answers do not all come from the same causal pathway.
6. End with the operational implication:
   design and evaluate systems around structural recoverability rather than surface correctness alone.

## Skeptical Objections

- The probing critique is the main one:
  recoverability under probes is not automatically the same thing as genuine encoded knowledge.
- Reversible embeddings and inversion work complicate any naive claim that intermediate representations are simply lossy.
- Alternative-interface wins may be local, benchmark-specific, or dependent on very particular task structure.
- Many failures may come from retrieval paths, decoding procedures, prompt sensitivity, or interface mismatch rather than missing internal representation.

## Research Method Note

The assistant pass was completed with alphaXiv using browser-backed web login and the local `alphaxiv` skill workflow.

Method used:

- one controlled wide-sweep hub session
- selective paper-grounded branch chats after the hub ranked missing work
- one clean `login-web` refresh when assistant sessions began stalling
- one fresh synthesis session at the end to avoid hub-context slowdown

Known operational note:

- `2407.14662` repeatedly stalled under the full branch prompt and had to be reduced to a narrower keep/supporting/cut prompt. Treat its role as limited until a cleaner paper-specific pass is run.

## Open Research Queue

- Decide whether `2602.10881` stays in the flagship essay as the serious precision-knowledge-work example or is demoted to background.
- Add only one more paper if it materially sharpens the probing critique or exact binding in a public-facing way.
- Revisit only those peripheral latent-interface additions that materially strengthen medium or format effects without reintroducing frontier hype.
- If `2407.14662` still seems necessary later, rerun it with a tighter paper-specific question or replace it with one empirical relational-composition paper.

## Drafting Rules

- Do not draft essay prose inside this file.
- Every future section in the essay must earn its inclusion by explanatory leverage, not by novelty or citation density.
- One worked example is mandatory before broadening into architecture.
- Citations must support a claim, not merely decorate it.
- If a section cannot clearly distinguish encoded, recoverable, and expressed, it does not belong in the next revision.
