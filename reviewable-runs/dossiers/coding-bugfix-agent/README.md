# Reviewable Run Dossier: Coding Bugfix Agent

This dossier applies the coding reference architecture to one repository-scoped bugfix. Read it linearly first. Use the supporting records only when you want to inspect how the run, approval boundary, or near miss is documented.

## Scenario and operating constraints

The system is assigned a regression where invoices with a `0%` discount serialize incorrectly. The run is bounded to one repository, must begin with inspection rather than editing, and must end with tests plus a reviewable diff before any merge. The main risk is a patch that makes the target test pass while leaving neighboring behavior insufficiently checked.

## Why this default architecture was selected

This dossier instantiates [`../../../autonomous-agent-blueprint/implementation/use-cases/coding-agent.md`](../../../autonomous-agent-blueprint/implementation/use-cases/coding-agent.md). The coding default wins because repository state and executable feedback are the strongest source of truth here. The main chapter basis is [`../../../autonomous-agent-blueprint/core/practical-chapter-blueprints/01-memory-blueprint.md`](../../../autonomous-agent-blueprint/core/practical-chapter-blueprints/01-memory-blueprint.md), [`../../../autonomous-agent-blueprint/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md`](../../../autonomous-agent-blueprint/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md), [`../../../autonomous-agent-blueprint/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md`](../../../autonomous-agent-blueprint/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md), and [`../../../autonomous-agent-blueprint/core/practical-chapter-blueprints/06-safety-blueprint.md`](../../../autonomous-agent-blueprint/core/practical-chapter-blueprints/06-safety-blueprint.md).

The main source basis is [`../../../autonomous-agent-blueprint/reference/papers/swe_agent.md`](../../../autonomous-agent-blueprint/reference/papers/swe_agent.md), [`../../../autonomous-agent-blueprint/reference/papers/react.md`](../../../autonomous-agent-blueprint/reference/papers/react.md), [`../../../autonomous-agent-blueprint/reference/papers/self_refine.md`](../../../autonomous-agent-blueprint/reference/papers/self_refine.md), [`../../../autonomous-agent-blueprint/reference/papers/chain_of_verification.md`](../../../autonomous-agent-blueprint/reference/papers/chain_of_verification.md), and [`../../../autonomous-agent-blueprint/reference/papers/toolemu.md`](../../../autonomous-agent-blueprint/reference/papers/toolemu.md). This is a conservative inspect-patch-test-review loop because environment feedback is better than conversational confidence for bounded engineering work.

## Runtime loop in plain language

1. Reproduce the failure and inspect the relevant code path.
2. Form a narrow hypothesis from files, logs, and failing tests.
3. Patch the smallest sensible surface.
4. Re-run the target and nearby regression checks.
5. Summarize the diff and stop at the merge gate.

## What the system must surface for this run

This dossier follows the model in [`../../reviewable-runs.md`](../../reviewable-runs.md). The system should be able to answer the six review questions through these records:

- What was the task? [`runtime-records/task-spec.md`](runtime-records/task-spec.md)
- What happened? [`runtime-records/execution-trace.md`](runtime-records/execution-trace.md)
- What did it rely on? [`runtime-records/evidence-record.md`](runtime-records/evidence-record.md)
- How was it checked? [`runtime-records/verification-report.md`](runtime-records/verification-report.md)
- Who approved impact? [`governance-records/approval-decision.md`](governance-records/approval-decision.md)
- What failed or could fail? [`governance-records/failure-review.md`](governance-records/failure-review.md)

In production, approval and failure review are conditional. They are included here because merge is a meaningful control boundary and the dossier is also a teaching example.

## Review and governance boundaries

The trust boundary is between repository evidence and generated patch text. Failing tests, inspected files, and command outputs count as evidence; the patch does not become trusted until the verification scope is strong enough. Merge remains human-governed. Run review should use [`../../evaluation/run-review-checklist.md`](../../evaluation/run-review-checklist.md). If the run suggests a design weakness, escalate to [`../../evaluation/architecture-readiness-checklist.md`](../../evaluation/architecture-readiness-checklist.md). The near-miss analysis should be checked against [`../../evaluation/failure-mode-catalog.md`](../../evaluation/failure-mode-catalog.md).

## Failure or near-miss analysis

The plausible miss is a false sense of safety: the patch fixes the target test but verification remains too narrow for the changed surface. That is why the failure review for this dossier focuses on regression coverage, diff-risk labeling, and explicit merge conditions rather than on a more complex planning topology. See [`governance-records/failure-review.md`](governance-records/failure-review.md).

## What to copy from this example

- Start with inspection and reproduction before editing.
- Keep the patch scope narrow and explain it with repository evidence.
- Treat the verification contract as more than one target test.
- Stop at review and merge approval rather than auto-merging by default.

## What not to generalize from this example

- Not every coding task needs the same regression breadth; verification should scale with the touched surface.
- Not every engineering run needs durable memory writes; keep memory selective and repo-scoped.
- Do not generalize this into “a passing test is enough”; the main lesson is verification scope, not target-test success.
