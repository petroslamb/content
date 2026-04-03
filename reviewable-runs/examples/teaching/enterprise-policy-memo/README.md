# Reviewable Run Dossier: Enterprise Policy Memo

**Status:** `synthetic teaching dossier`

This dossier applies the enterprise reference architecture to one policy-sensitive drafting task. Read it linearly first. Inspect the supporting records only if you want to audit how the run is grounded or governed.

## Scenario and operating constraints

The system is asked to draft an internal memo titled `Policy Guidance for AI-Generated Customer Support Summaries`. It must synthesize current policy and workflow material, avoid superseded revisions, and stop before publication until compliance approves the result. The risk is not random verbosity. The risk is a polished memo that looks authoritative while carrying stale or operationally unsafe guidance.

## Why this default architecture was selected

This dossier instantiates [`../../../../publications/autonomous-agents/implementation/use-cases/enterprise-agent.md`](../../../../publications/autonomous-agents/implementation/use-cases/enterprise-agent.md). The enterprise default wins because the task is evidence-grounded drafting under approval, not open browsing and not repository mutation. The main chapter basis is [`../../../../publications/autonomous-agents/core/practical-chapter-blueprints/01-memory-blueprint.md`](../../../../publications/autonomous-agents/core/practical-chapter-blueprints/01-memory-blueprint.md), [`../../../../publications/autonomous-agents/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md`](../../../../publications/autonomous-agents/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md), [`../../../../publications/autonomous-agents/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md`](../../../../publications/autonomous-agents/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md), and [`../../../../publications/autonomous-agents/core/practical-chapter-blueprints/06-safety-blueprint.md`](../../../../publications/autonomous-agents/core/practical-chapter-blueprints/06-safety-blueprint.md).

The main source basis is [`../../../../publications/autonomous-agents/reference/papers/memgpt.md`](../../../../publications/autonomous-agents/reference/papers/memgpt.md), [`../../../../publications/autonomous-agents/reference/papers/react.md`](../../../../publications/autonomous-agents/reference/papers/react.md), [`../../../../publications/autonomous-agents/reference/papers/chain_of_verification.md`](../../../../publications/autonomous-agents/reference/papers/chain_of_verification.md), [`../../../../publications/autonomous-agents/reference/papers/gorilla.md`](../../../../publications/autonomous-agents/reference/papers/gorilla.md), and [`../../../../publications/autonomous-agents/reference/papers/greshake_indirect_prompt_injection.md`](../../../../publications/autonomous-agents/reference/papers/greshake_indirect_prompt_injection.md). The design stays conservative because typed memo production, evidence discipline, and publication approval matter more here than visible autonomy.

## Runtime loop in plain language

1. Bound the task to drafting, not policy editing or publication.
2. Retrieve the current policy and workflow sources with revision awareness.
3. Draft a memo that keeps claims aligned to specific evidence rows.
4. Verify freshness, source coverage, and policy-action separation.
5. Stop at the publication gate and wait for human approval.

## What the system must surface for this run

This dossier follows the model in [`../../README.md`](../../README.md). The system should be able to answer the six review questions through these records:

- What was the task? [`runtime-records/task-spec.md`](runtime-records/task-spec.md)
- What happened? [`runtime-records/execution-trace.md`](runtime-records/execution-trace.md)
- What did it rely on? [`runtime-records/evidence-record.md`](runtime-records/evidence-record.md)
- How was it checked? [`runtime-records/verification-report.md`](runtime-records/verification-report.md)
- Who approved impact? [`governance-records/approval-decision.md`](governance-records/approval-decision.md)
- What failed or could fail? [`governance-records/failure-review.md`](governance-records/failure-review.md)

In production, the approval and failure records are conditional. They are included here because publication is policy-sensitive and this dossier is also a teaching example.

## Review and governance boundaries

Retrieved policy text is evidence, not privileged instruction. The trust boundary sits between drafting policy and retrieved content, and between read-only retrieval and publication. Approval is required because the output changes the guidance other teams may follow. Run review should use [`../../../evaluation/run-review-checklist.md`](../../../evaluation/run-review-checklist.md). If the run exposes a broader design gap, escalate to [`../../../evaluation/architecture-readiness-checklist.md`](../../../evaluation/architecture-readiness-checklist.md). The likely misses should be pressure-tested against [`../../../evaluation/failure-mode-catalog.md`](../../../evaluation/failure-mode-catalog.md).

## Failure or near-miss analysis

The most plausible miss is a stale but convincing policy clause. A superseded retention paragraph can still retrieve well, slip into the draft, and survive until verification if freshness checks are weak. That is why the failure review for this dossier focuses on freshness metadata, supersession checks, and retrieval hygiene rather than on more elaborate reasoning loops. See [`governance-records/failure-review.md`](governance-records/failure-review.md).

## What to copy from this example

- Keep retrieval freshness explicit instead of assuming the top result is current.
- Make every memo claim traceable to an evidence row.
- Separate drafting from publication with a hard approval boundary.
- Keep the verification report focused on evidence coverage, freshness, and policy-action separation.

## What not to generalize from this example

- Not every enterprise task needs a memo-shaped deliverable; the important part is reviewable evidence, not the memo form itself.
- Not every enterprise run needs publication approval; approval is tied to impact, not to mere existence of text.
- Do not generalize this into “more retrieval is always better”; stale retrieval can be the central failure mode.
