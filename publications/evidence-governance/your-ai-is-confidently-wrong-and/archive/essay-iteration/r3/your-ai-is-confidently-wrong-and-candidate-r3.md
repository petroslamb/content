# Your AI Is Confidently Wrong: The Human Discipline of Evidence Governance

**Generation is cheap; trust is expensive. The expense isn't compute: it's the willingness to be proven wrong.**

---

## The Moment of Contradiction

The summary in the compliance report was definitive: *"All obligations properly mapped to specification and implementation code."*

The underlying data, however, told a different story. The mapping fields pointed to an ABI wrapper, a test file, and an RPC helper. None of these contained the protocol logic the summary claimed was verified. Both documents were AI-generated. Both were formatted with institutional confidence. They flatly contradicted each other.

And we had no rule for which one to trust.

In most organizations, the polished narrative wins because narratives are easy to read and data is difficult to audit. But this was more than a model failure; it was a governance failure. We had built a system that could generate claims but lacked the protocol to adjudicate them when they collided. This is the reality of the current AI cycle: we are shipping "certainty" without infrastructure for "truth."

---

## The Auditability Gap

Building **eip-verify**, a tool for Ethereum protocol verification, revealed a counterintuitive truth about model progression. Over five iterations of development, the system did not get dramatically "better" at being right. Even the strongest models peaked at an 80% validity rate for complex obligation mapping.

However, the system became dramatically better at being **findably wrong**.

By instrumenting the model with claim-level auditability, we shifted the human burden from "blind verification" to "targeted adjudication." We found that while correctness is hard to scale, **inspectability** is an engineering choice. Findable wrongness is a manageable operational risk. Confident wrongness is a catastrophic liability.

Most teams are optimizing for the wrong variable. They treat AI as an oracle and try to move the accuracy bar from 80% to 90%. They should instead treat AI as a fallible clerk and build the scaffolding that makes the 20% failure rate visible.

---

## The CHOKE Phenomenon

The danger of "Oracle-style" AI is now technically documented. Research into **CHOKE** (Certain Hallucinations Overriding Known Evidence) proves that models frequently hallucinate with high certainty even when they possess the correct underlying knowledge (Simhi et al., 2025). 

A model can consistently answer a question correctly in one context, but a subtle change in the prompt, or the mere act of generating a summary, can cause it to produce a confident error that overrides its own data. This is why "human-in-the-loop" review often fails: if the human is reviewing the *tone* of the summary rather than the *receipts* of the data, they are simply being charmed by a hallucination.

Verification is not a test of the model’s intelligence. It is a test of the human’s protocol for handling disagreement.

---

## The Historical Precedent

In the 1990s, clinical medicine faced a similar crisis. Expert opinions sounded authoritative, but randomized controlled trials (RCTs) frequently contradicted years of "established" practice. The solution was not to train "better" experts or wait for smarter professors.

The solution was **Evidence-Based Medicine (EBM)**: a mechanical rule that removed judgment from the conflict-resolution step. This created an **Evidence Hierarchy**: Systematic reviews beat RCTs. RCTs beat cohort studies. Cohort studies beat expert narratives. No exceptions. No appeals to authority.

This shifted the "expense" of medicine from the brilliance of the doctor to the discipline of the evidence. We must now apply this same mechanical discipline to the outputs of large language models.

---

## The Evidence Governance Protocol

To move from "fluent AI" to "verifiable AI," we implemented a five-component protocol. These are not product features; they are constraints on the human workflow.

1. **The Evidence Hierarchy**: Raw artifacts (CSVs, transcripts, code snippets) overrule narrative summaries. When a summary says "verified" but the data says "null," the data wins. Narratives are treated as "candidate claims" until the hierarchy supports them.
2. **Atomic Claim-Level Verification**: Systems must decompose long-form answers into atomic, verifiable statements (Ji et al., 2026). Whole-answer scoring is a mask for isolated but safety-critical errors.
3. **The Contradiction Register**: Disagreements between artifacts are upgraded to first-class workflow objects. They are not "resolved" by the model; they are flagged for human adjudication. Surfacing the "8 contradictions" in our pilot was the difference between a compliant report and a lie.
4. **The Claim Ledger**: Every external claim must be linked to a supporting artifact, a confidence tag, and known counter-evidence. A claim without a ledger entry is discarded, regardless of how "confident" the prose sounds.
5. **The Governance Loop**: Run → Generate Claims → Audit Receipts → Register Contradictions → Re-score. The goal is to maximize the speed at which contradictions are found, not the speed at which the final report is written.

---

## The Uncomfortable Truth

There was a final irony in the `eip-verify` project. Much of the evidence governance infrastructure (the rubrics, the registers, the ledgers) was itself built with AI assistance.

The AI is mediocre at verifying complex protocol logic. It is, however, excellent at building the scaffolding that exposes its own mediocrity. That is the actual product.

The cost of AI isn't the GPUs or the token price. It is the human discipline required to use the scaffolding instead of cherry-picking the results that sound best. It is the willingness to downgrade a high-confidence claim when the evidence hierarchy says it's unsupported.

If you ship AI-generated analysis and do not yet have a contradiction register, start one today. If you have one, gate your next report on it. The protocol price is human: the cost of being honest about what your models don't know.

---

## The Monday Morning Operator

In the `eip-verify` pilot, our audit infrastructure processed 47 adjudication rows, resulting in an aggregate follow-up rate of **38.3%** (the percentage of rows requiring manual audit). This sounds expensive until the governance system reveals the skew: **72.2%** of that total burden was concentrated in output from the cheapest model tier (Haiku). Excluding Haiku rows, follow-up burden was **15.6%**. 

This insight transformed an undifferentiated cost problem into an actionable routing decision. More importantly, the system surfaced 8 high-confidence contradictions that would have otherwise been missed. These led to the manual downgrading of 3 critical claims that models had initially tagged as "verified." In a high-integrity environment, those three rows are the difference between a compliant system and a silent failure.

---

## Limits
- **Not a Solution for Ignorance**: This protocol assumes the model has access to the correct evidence in its context or retrieval layer. It cannot fix a model that is "missing" the truth.
- **Human Discipline Required**: The protocol is only as strong as the human's willingness to enforce it. If reviewers "approve" contradicted claims anyway, the system collapses.
- **Proof Boundary**: This framework represents an original synthesis supported by a single high-fidelity pilot project (`eip-verify`) and converging theoretical literature. It should be treated as a robust governance pattern for emerging AI workflows, but it has not yet been established as a cross-domain validated standard.

## References
- **Simhi, A., et al. (2025)**. *Trust Me, I’m Wrong: LLMs Hallucinate with Certainty Despite Knowing the Answer*. arXiv:2502.12964. (The CHOKE Phenomenon).
- **Ji, Y., et al. (2026)**. *MedRAGChecker: Claim-Level Verification for Biomedical Retrieval-Augmented Generation*. arXiv:2601.15601. (Atomic Claim-Level Verification).
- **Guyatt, G. H., et al. (2008)**. *GRADE: an emerging consensus on rating quality of evidence and strength of recommendations*. BMJ, 336(7650). (The Evidence Hierarchy).
- **Petros Lamb (2025)**. *eip-verify Technical Companion*. Evidence Governance Project.
