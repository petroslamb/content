# Hardened Blueprint: Your AI Is Confidently Wrong

Live draft: `publications/evidence-governance/your-ai-is-confidently-wrong-and/your-ai-is-confidently-wrong-and.md`
Candidate target: `publications/evidence-governance/your-ai-is-confidently-wrong-and/your-ai-is-confidently-wrong-and-candidate-r3.md`
Packet manifest: `publications/evidence-governance/your-ai-is-confidently-wrong-and/your-ai-is-confidently-wrong-and-essay-iteration-packet-r3.json`

## Goal
The goal is to elevate the essay from a conceptual "summary object" draft to a high-fidelity, evidence-backed flagship publication that proposes a concrete "Evidence Governance" operational doctrine.

## Promise

Generation is cheap; trust is expensive. This essay proves that "trusting" an AI model is a category error. Instead, we must implement **Evidence Governance**—a human discipline inspired by Evidence-Based Medicine—that ignores model certainty and gates claims on a mechanical hierarchy of proof.

## Spine

1. **The Moment of Contradiction**: The opening hook where a model contradicts its own data. This is not a "failure" but the default state of un-governed AI.
2. **The Auditability Gap**: Correctness vs. Inspectability. The hard finding that models don't get much more "right," but they do get much more "findably wrong" when instrumented.
3. **The CHOKE Phenomenon**: (Simhi et al., 2025) The technical proof that models hallucinate with high certainty even when they "know" the truth. This kills the "certainty-as-proxy" excuse.
4. **The Historical Protocol**: The Evidence-Based Medicine (EBM) anchor. Medicine didn't solve its knowledge crisis by "tuning better experts," but by building an evidence hierarchy that removed expert judgment from conflict resolution.
5. **The Evidence Governance Protocol**: The 5-component doctrine (Hierarchy, Scoring, Register, Ledger, Loop) reframed as an operational mandate.
6. **The Monday Morning Operator**: Quantitative proof from the `eip-verify` pilot showing a 38.3% burden reduction and the surafcing of critical contradictions.
7. **The Honesty Expense**: The conclusion. The cost of AI isn't tokens or compute—it's the willingness to downgrade a polished narrative when the receipts fail to arrive.

## Paragraph burden

- **Intro**: Establish that the polished narrative wins by default unless a protocol intervenes.
- **Auditability**: Prove that "findable wrongness" is the only actionable metric for enterprise AI.
- **CHOKE**: Use the Simhi/Ji findings to invalidate "human review" that relies on the AI's tone.
- **EBM**: Use the Oxford Levels anchor to justify the mechanical downgrading of "expert" (narrative) claims.
- **Protocol**: Define the 5 steps not as features, but as constraints on human behavior.
- **Operator**: Quantify the impact with `eip-verify` metrics (47 rows, 8 contradictions).
- **Conclusion**: Land on the "discipline of honesty" as the differentiator.

## Evidence burden

- **Body Work**:
    - `trust_me_im_wrong.md` (Simhi et al., 2025): Support the CHOKE section.
    - `oxford_levels_of_evidence.md`: Support the Hierarchy section.
    - `medragchecker.md` (Ji et al., 2026): Support the "Claim Ledger" and "Atomic Verification" section.
- **References only**:
    - `from_fluent_to_verifiable.md`: Supporting the correctness vs. inspectability point.
- **Synthesis**: The 5-component "Evidence Governance" pattern is the original synthesis.

## Cut order

1. Detailed model metrics (move to companion).
2. The specific history of `eip-verify` (keep lean, move detailed trace to companion).

## Limits
- **Not a Solution for Ignorance**: The protocol assumes the model has access to the correct evidence.
- **Proof Boundary**: This framework is an original synthesis supported by the `eip-verify` pilot and converging theoretical literature; it is not yet a cross-domain validated standard.
- **Human Discipline Required**: The protocol is only as strong as the human's willingness to enforce it.

## Failure triggers

- The essay feels like a product pitch for `eip-verify` rather than a protocol for human behavior.
- The EBM analogy takes up more than 15% of the word count.
- The "Trust Gap" section lacks the "Auditability vs Correctness" data point.
