# Worked Case Study: Coding Bugfix Agent

> Historical note: This v1 packet-oriented case study was superseded by [`../../README.md`](../../README.md) and [`../../examples/teaching/coding-bugfix-agent/README.md`](../../examples/teaching/coding-bugfix-agent/README.md).

This case applies the coding reference architecture to a concrete repository task: diagnosing a failing test, patching the implementation, rerunning checks, and presenting a reviewable diff for approval.

## How To Read This Case

Read this file in four passes:

1. read `Problem and operating constraints` to see the scoped engineering task and why inspection comes first
2. read `Default architecture selected` plus `Why this architecture wins here` to map the case back to the coding blueprint
3. open the artifact bundle in [`artifacts/coding-bugfix-agent/`](artifacts/coding-bugfix-agent/) to follow inspect -> patch -> test -> approval
4. finish with `Failure review` and [`../../evaluation/failure-mode-catalog.md`](../../evaluation/failure-mode-catalog.md) to see how a seemingly good patch can still fail review

## Problem and operating constraints

The agent is assigned a bug where invoices with a `0%` discount are serialized incorrectly and fail a regression test. The task is bounded to one repository, must begin with inspection rather than editing, and must end with tests and a diff review before anything is merged. The main risk is not elegant prose; it is making a narrow patch that appears to work while creating a hidden regression.

## Default architecture selected

This case instantiates the abstract coding architecture in [`../../../publications/autonomous-agents/implementation/use-cases/coding-agent.md`](../../../publications/autonomous-agents/implementation/use-cases/coding-agent.md). It adopts the default choices from [`../../../publications/autonomous-agents/core/practical-chapter-blueprints/01-memory-blueprint.md`](../../../publications/autonomous-agents/core/practical-chapter-blueprints/01-memory-blueprint.md), [`../../../publications/autonomous-agents/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md`](../../../publications/autonomous-agents/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md), [`../../../publications/autonomous-agents/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md`](../../../publications/autonomous-agents/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md), and [`../../../publications/autonomous-agents/core/practical-chapter-blueprints/06-safety-blueprint.md`](../../../publications/autonomous-agents/core/practical-chapter-blueprints/06-safety-blueprint.md).

The source basis is [`../../../publications/autonomous-agents/reference/papers/swe_agent.md`](../../../publications/autonomous-agents/reference/papers/swe_agent.md), [`../../../publications/autonomous-agents/reference/papers/react.md`](../../../publications/autonomous-agents/reference/papers/react.md), [`../../../publications/autonomous-agents/reference/papers/self_refine.md`](../../../publications/autonomous-agents/reference/papers/self_refine.md), [`../../../publications/autonomous-agents/reference/papers/chain_of_verification.md`](../../../publications/autonomous-agents/reference/papers/chain_of_verification.md), and [`../../../publications/autonomous-agents/reference/papers/toolemu.md`](../../../publications/autonomous-agents/reference/papers/toolemu.md).

The matching artifact bundle lives in [`artifacts/coding-bugfix-agent/`](artifacts/coding-bugfix-agent/).

## Why this architecture wins here

This task is governed by executable feedback. The coding architecture wins because it treats shell access, file inspection, patching, and tests as one loop rather than splitting them into separate assistant behaviors. That makes verification cheap, explicit, and tied to the environment.

The design is intentionally conservative: inspect first, patch second, test third, and only then summarize the diff. That sequence is stronger than a browser-first or conversation-first approach because the core evidence for correctness comes from repository state and test results, not from argument quality alone.

## Alternatives rejected

- Editing before inspection was rejected because the task requires file scope, reproduction, and hypothesis formation before any code changes are justified; basis: [`../../../publications/autonomous-agents/implementation/use-cases/coding-agent.md`](../../../publications/autonomous-agents/implementation/use-cases/coding-agent.md), [`../../../publications/autonomous-agents/reference/papers/swe_agent.md`](../../../publications/autonomous-agents/reference/papers/swe_agent.md).
- Browser-first repo interaction was rejected because the issue lives in executable code and tests, so web navigation would add surface area without improving observability or verification; basis: [`../../../publications/autonomous-agents/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md`](../../../publications/autonomous-agents/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md), [`../../../publications/autonomous-agents/reference/papers/swe_agent.md`](../../../publications/autonomous-agents/reference/papers/swe_agent.md), [`../../../publications/autonomous-agents/reference/papers/webagent.md`](../../../publications/autonomous-agents/reference/papers/webagent.md).
- Unrestricted optimization or auto-merge was rejected because the agent already has mutating power inside the repo, so merge and self-improvement boundaries must remain human-governed; basis: [`../../../publications/autonomous-agents/core/practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md`](../../../publications/autonomous-agents/core/practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md), [`../../../publications/autonomous-agents/core/practical-chapter-blueprints/06-safety-blueprint.md`](../../../publications/autonomous-agents/core/practical-chapter-blueprints/06-safety-blueprint.md), [`../../../publications/autonomous-agents/reference/papers/toolemu.md`](../../../publications/autonomous-agents/reference/papers/toolemu.md).

## Trust boundaries and approval gates

The main trust boundary here is between repository evidence and speculation. Logs, failing tests, and inspected files are evidence; generated patch text is not trusted until tests and review pass. Inspection commands are separated from mutating commands, and merge remains outside the agent's permissions.

Approval happens after the test run and diff summary are complete. The reviewer sees the failing symptom, the patch rationale, the commands that were run, and the exact tests that passed. This is a direct application of the review logic in [`../../evaluation/architecture-readiness-checklist.md`](../../evaluation/architecture-readiness-checklist.md).

## Evaluation plan

The architecture is checked against [`../../evaluation/architecture-readiness-checklist.md`](../../evaluation/architecture-readiness-checklist.md) and the relevant failure modes in [`../../evaluation/failure-mode-catalog.md`](../../evaluation/failure-mode-catalog.md). The main acceptance criteria are:

- the agent starts with inspection, not editing
- the patch stays within the scoped files
- the target regression test passes
- the broader selected test set and diff review do not expose a hidden regression
- the change stops at review rather than auto-merge

The good-path artifact bundle for this case is:

- [`artifacts/coding-bugfix-agent/input-brief.md`](artifacts/coding-bugfix-agent/input-brief.md)
- [`artifacts/coding-bugfix-agent/planner-trace.md`](artifacts/coding-bugfix-agent/planner-trace.md)
- [`artifacts/coding-bugfix-agent/state-or-evidence-record.md`](artifacts/coding-bugfix-agent/state-or-evidence-record.md)
- [`artifacts/coding-bugfix-agent/verification-report.md`](artifacts/coding-bugfix-agent/verification-report.md)
- [`artifacts/coding-bugfix-agent/approval-record.md`](artifacts/coding-bugfix-agent/approval-record.md)

## Failure review

The plausible failure for this default is a false sense of safety: the agent diagnoses the bug correctly, patches it, and passes the targeted regression test, but it skips a broader invoice-serialization test and introduces a rounding regression in a nearby path. This maps to `Irreversible action without enough evidence` and `Prompt churn without measurement` in [`../../evaluation/failure-mode-catalog.md`](../../evaluation/failure-mode-catalog.md) by way of insufficient verification scope rather than bad reasoning alone.

The failure review artifact for this case lives at [`artifacts/coding-bugfix-agent/failure-review.md`](artifacts/coding-bugfix-agent/failure-review.md). The review shows that a stronger verification contract, especially a broader regression suite and explicit diff risk labeling, would have reduced the miss.

## Bottom line

Start from the coding architecture when repository state and executable checks are the real source of truth. This case shows how the repo's doctrine becomes concrete: inspect, patch, test, review, approve.
