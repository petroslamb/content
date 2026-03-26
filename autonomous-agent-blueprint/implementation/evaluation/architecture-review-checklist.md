# Architecture Review Checklist

Use this file to review a proposed agent architecture before implementation or deployment. The checklist is designed to expose missing subsystems, weak boundaries, and overbuilt autonomy by asking whether the system can answer the review questions in [`../../core/reviewable-runs.md`](../../core/reviewable-runs.md).

Worked examples that show this checklist applied in context:

- [`../case-studies/enterprise-policy-memo/README.md`](../case-studies/enterprise-policy-memo/README.md)
- [`../case-studies/coding-bugfix-agent/README.md`](../case-studies/coding-bugfix-agent/README.md)
- [`../case-studies/web-form-agent/README.md`](../case-studies/web-form-agent/README.md)

The standard here is not literal file presence. The standard is whether the records are available or reconstructable enough to review a run credibly.

## Six Review Questions

- [ ] Can the system state the task boundary and stop conditions?
- [ ] Can the system reconstruct what happened across the control loop?
- [ ] Can the system show what evidence, provenance, or state supported the run?
- [ ] Can the system show how the result or action was verified?
- [ ] Can the system show who approved a high-impact action, or explain why no approval was required?
- [ ] Can the system produce or reconstruct a failure review after an incident, near miss, or deliberate exercise?

## Cross-Cutting Scorecard

Score each dimension from `1` to `5`.

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Task grounding | vague task model | bounded workflow with partial task records | explicit task model with stop conditions and reviewable task scope |
| Memory quality | prompt stuffing | layered memory with basic retrieval | layered memory with write policy, pruning, and retrieval discipline |
| Action reliability | free-form action language | mostly typed tools with partial checks | replayable tools or code paths with deterministic checks |
| Verification strength | no real checks | critique or spot checks | explicit verification path tied to risk and action type |
| Safety boundary clarity | trust is implicit | some boundary separation | clear trust zones, least privilege, and approval rules |
| Runtime reviewability | only final outputs visible | traces and logs exist but are incomplete | task, trace, evidence, and verification records are reviewable or reconstructable |
| Governance reviewability | no approval or failure context | ad hoc review with weak context | approval context and post-failure review are explicit when the risk level requires them |

## Core Checklist

- [ ] The architecture has one obvious control loop.
- [ ] The architecture defines where memory writes happen and why.
- [ ] The architecture defines which action surfaces are allowed.
- [ ] The architecture separates reads from writes where risk differs.
- [ ] The architecture can produce or reconstruct task, trace, evidence, and verification records.
- [ ] The architecture defines human approval points for high-impact actions and explains when approval is unnecessary.
- [ ] The architecture has explicit trust separation for external or retrieved content.
- [ ] The architecture can support failure review after incidents or deliberate postmortem exercises.

## Chapter-Linked Review Prompts

### Memory

- [ ] Is working memory distinct from durable memory?
- [ ] Is semantic retrieval separated from episodic run history?
- [ ] Is there a write policy for memory rather than automatic logging?
- [ ] Is there any pruning, decay, or consolidation policy?

### Reasoning And Planning

- [ ] Is the reasoning scaffold matched to the task difficulty?
- [ ] Is ReAct or an equivalent loop used when tools or environment state matter?
- [ ] Is search reserved for tasks that truly need branching exploration?
- [ ] Is verification stronger than a single first-pass answer?

### Action And Tool Use

- [ ] Are action surfaces typed and replayable where possible?
- [ ] Are tool descriptions and argument shapes explicit?
- [ ] Can failed actions be observed and recovered from?
- [ ] Are write actions more constrained than read actions?

### Optimization And Self-Improvement

- [ ] Does the team have a stable evaluation set?
- [ ] Are prompt and schema changes measured before larger topology changes?
- [ ] Are feedback loops tied to known recurring failures?
- [ ] Is workflow search avoided until the baseline is already stable?

### Multi-Agent Design

- [ ] Is more than one agent actually justified?
- [ ] Are roles separated by tools, permissions, or artifacts rather than just names?
- [ ] Are handoffs structured and inspectable?
- [ ] Does a human still exist as an explicit role where accountability matters?

### Safety

- [ ] Are instructions separated from data?
- [ ] Are retrieval and memory treated as attack surfaces?
- [ ] Are irreversible actions guarded by deterministic checks and human approval?
- [ ] Are inter-agent messages, files, and screenshots treated as untrusted unless proven otherwise?

## Governance Notes

- Approval records are required when actions are high impact, external, destructive, expensive to roll back, or policy sensitive.
- Failure reviews are required after real incidents and are strongly recommended after near misses or deliberate red-team exercises.
- A low-risk successful run does not need every governance record persisted forever, but the system should support reconstructing them when needed.

## Review Outcomes

### Accept

Use this when the architecture has a bounded control loop, explicit trust boundaries, and a credible evaluation plan.

### Revise

Use this when the architecture is directionally sound but missing one or two critical controls such as verification, memory policy, or approval gates.

### Reject

Use this when the architecture relies on vague autonomy, unclear action surfaces, no verification, or no meaningful safety boundary.
