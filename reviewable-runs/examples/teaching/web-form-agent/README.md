# Reviewable Run Dossier: Web Form Agent

**Status:** `synthetic teaching dossier`

This dossier applies the web reference architecture to one high-friction browser task. Read it linearly first. Use the supporting records only when you want to inspect how the browser run was grounded, gated, and reviewed.

## Scenario and operating constraints

The system is asked to prepare a travel reimbursement request through a vendor portal with a multi-step form, dynamic help text, and attachment uploads. It must gather evidence from booking pages, keep track of changing page state, and stop before final submission until a human approves the prepared claim. The main risk is acting on unstable or hostile page content with high confidence.

## Why this default architecture was selected

This dossier instantiates [`../../../../publications/autonomous-agents/implementation/use-cases/web-agent.md`](../../../../publications/autonomous-agents/implementation/use-cases/web-agent.md). The web default wins because live page state is the dominant uncertainty here. The main chapter basis is [`../../../../publications/autonomous-agents/core/practical-chapter-blueprints/01-memory-blueprint.md`](../../../../publications/autonomous-agents/core/practical-chapter-blueprints/01-memory-blueprint.md), [`../../../../publications/autonomous-agents/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md`](../../../../publications/autonomous-agents/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md), [`../../../../publications/autonomous-agents/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md`](../../../../publications/autonomous-agents/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md), and [`../../../../publications/autonomous-agents/core/practical-chapter-blueprints/06-safety-blueprint.md`](../../../../publications/autonomous-agents/core/practical-chapter-blueprints/06-safety-blueprint.md).

The main source basis is [`../../../../publications/autonomous-agents/reference/papers/react.md`](../../../../publications/autonomous-agents/reference/papers/react.md), [`../../../../publications/autonomous-agents/reference/papers/webagent.md`](../../../../publications/autonomous-agents/reference/papers/webagent.md), [`../../../../publications/autonomous-agents/reference/papers/mind2web.md`](../../../../publications/autonomous-agents/reference/papers/mind2web.md), [`../../../../publications/autonomous-agents/reference/papers/chain_of_verification.md`](../../../../publications/autonomous-agents/reference/papers/chain_of_verification.md), and [`../../../../publications/autonomous-agents/reference/papers/greshake_indirect_prompt_injection.md`](../../../../publications/autonomous-agents/reference/papers/greshake_indirect_prompt_injection.md). This is a conservative observe-summarize-act-verify loop because browser success depends on state discipline more than on free-form exploration.

## Runtime loop in plain language

1. Observe the current portal state and confirm the intended flow.
2. Gather evidence from booking pages and receipts.
3. Fill the draft claim through bounded browser actions.
4. Re-check the live page state after every risky transition.
5. Stop at the submission gate and wait for approval.

## What the system must surface for this run

This dossier follows the model in [`../../README.md`](../../README.md). The system should be able to answer the six review questions through these records:

- What was the task? [`runtime-records/task-spec.md`](runtime-records/task-spec.md)
- What happened? [`runtime-records/execution-trace.md`](runtime-records/execution-trace.md)
- What did it rely on? [`runtime-records/evidence-record.md`](runtime-records/evidence-record.md)
- How was it checked? [`runtime-records/verification-report.md`](runtime-records/verification-report.md)
- Who approved impact? [`governance-records/approval-decision.md`](governance-records/approval-decision.md)
- What failed or could fail? [`governance-records/failure-review.md`](governance-records/failure-review.md)

In production, approval and failure review are conditional. They are included here because final submission is high impact and the dossier is also a teaching example.

## Review and governance boundaries

The trust boundary is between page content and control policy. Help text, recommendations, and dynamic labels can be useful observations, but they are not privileged instructions. Approval is required because submission changes an external system. Run review should use [`../../../evaluation/run-review-checklist.md`](../../../evaluation/run-review-checklist.md). If the run reveals a deeper browser-system weakness, escalate to [`../../../evaluation/architecture-readiness-checklist.md`](../../../evaluation/architecture-readiness-checklist.md). Web-specific misses should be checked against [`../../../evaluation/failure-mode-catalog.md`](../../../evaluation/failure-mode-catalog.md).

## Failure or near-miss analysis

The most plausible miss is a page-state reset that looks like success. The agent can extract the correct amount, prepare the right attachments, and still end up on the wrong claim type after a refresh-sensitive widget re-renders. That is why the failure review for this dossier focuses on final-state verification and approval-packet clarity rather than on deeper search. See [`governance-records/failure-review.md`](governance-records/failure-review.md).

## What to copy from this example

- Separate observation summaries from action policy.
- Re-verify live page state after every meaningful state transition.
- Keep the approval packet focused on the exact visible pre-submit state.
- Prefer DOM-aware control and treat GUI-like control as a fallback.

## What not to generalize from this example

- Not every browser task needs human approval; the gate is tied to impact and irreversibility.
- Not every web run needs durable memory; stale web state is often more dangerous than forgotten state.
- Do not generalize this into “the page said it was fine”; the lesson is that visible success and safe state are not always the same thing.
