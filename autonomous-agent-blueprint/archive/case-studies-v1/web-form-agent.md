# Worked Case Study: Web Form Agent

> Historical note: This v1 packet-oriented case study was superseded by [`../../core/reviewable-runs.md`](../../core/reviewable-runs.md) and [`../../implementation/case-studies/web-form-agent/README.md`](../../implementation/case-studies/web-form-agent/README.md).

This case applies the web reference architecture to a concrete browser task: gather evidence across several pages, fill a high-friction reimbursement form, and require approval before final submission.

## How To Read This Case

Read this file in four passes:

1. read `Problem and operating constraints` to see why live page state is the dominant source of uncertainty
2. read `Default architecture selected` plus `Why this architecture wins here` to understand why the web archetype wins over enterprise or coding defaults
3. open the artifact bundle in [`artifacts/web-form-agent/`](artifacts/web-form-agent/) to see observe -> summarize -> act -> verify -> approve in sequence
4. finish with `Failure review` and [`../../implementation/evaluation/architecture-review-checklist.md`](../../implementation/evaluation/architecture-review-checklist.md) to see how page-state mistakes are reviewed before submission

## Problem and operating constraints

The agent is asked to submit a travel reimbursement request through a vendor portal that has a multi-step form, dynamic help text, and attachment upload requirements. The agent must collect evidence from prior booking pages, keep track of page state as it changes, and stop before the final submit step until a human approves the draft. The main risk is acting on unstable or hostile page content and submitting the wrong thing with high confidence.

## Default architecture selected

This case instantiates the abstract web architecture in [`../../implementation/use-cases/web-agent.md`](../../implementation/use-cases/web-agent.md). It adopts the defaults from [`../../core/practical-chapter-blueprints/01-memory-blueprint.md`](../../core/practical-chapter-blueprints/01-memory-blueprint.md), [`../../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md`](../../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md), [`../../core/practical-chapter-blueprints/03-action-tool-use-blueprint.md`](../../core/practical-chapter-blueprints/03-action-tool-use-blueprint.md), and [`../../core/practical-chapter-blueprints/06-safety-blueprint.md`](../../core/practical-chapter-blueprints/06-safety-blueprint.md).

The source basis is [`../../reference/papers/react.md`](../../reference/papers/react.md), [`../../reference/papers/webagent.md`](../../reference/papers/webagent.md), [`../../reference/papers/mind2web.md`](../../reference/papers/mind2web.md), [`../../reference/papers/chain_of_verification.md`](../../reference/papers/chain_of_verification.md), and [`../../reference/papers/greshake_indirect_prompt_injection.md`](../../reference/papers/greshake_indirect_prompt_injection.md).

The matching artifact bundle lives in [`artifacts/web-form-agent/`](artifacts/web-form-agent/).

## Why this architecture wins here

This task depends on live page state, not static enterprise retrieval or repository execution. The web architecture wins because it treats observation and action as separate steps, uses ReAct-style planning to move through the flow incrementally, and forces verification before each high-impact state transition.

The approval gate is essential here because the form submission is the irreversible step. The system is allowed to navigate, gather evidence, and prepare the draft, but the final transition from prepared form to submitted request is explicitly governed.

## Alternatives rejected

- GUI-first action was rejected because the portal exposes stable DOM structure for the key fields, making DOM-aware control safer and more observable than screenshot-only interaction; basis: [`../../implementation/use-cases/web-agent.md`](../../implementation/use-cases/web-agent.md), [`../../reference/papers/webagent.md`](../../reference/papers/webagent.md), [`../../reference/papers/mind2web.md`](../../reference/papers/mind2web.md).
- Retrieval-only browsing without state verification was rejected because snippets from earlier pages are not enough evidence for a safe submission once the current page state changes; basis: [`../../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md`](../../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md), [`../../reference/papers/webagent.md`](../../reference/papers/webagent.md), [`../../reference/papers/chain_of_verification.md`](../../reference/papers/chain_of_verification.md).
- No approval gate before submission was rejected because purchases, reimbursements, and external commitments are exactly the class of browser action that should not rely on page-local confidence alone; basis: [`../../core/practical-chapter-blueprints/06-safety-blueprint.md`](../../core/practical-chapter-blueprints/06-safety-blueprint.md), [`../../reference/papers/toolemu.md`](../../reference/papers/toolemu.md), [`../../reference/papers/greshake_indirect_prompt_injection.md`](../../reference/papers/greshake_indirect_prompt_injection.md).

## Trust boundaries and approval gates

The core trust boundary is between page content and control policy. Help text, tooltips, and inline instructions on the site can be useful evidence, but they are not privileged instructions. The agent keeps observation summaries separate from action policy and verifies page state before it advances.

Approval occurs when the form is fully populated, attachments are staged, and the verification report confirms that the current page matches the intended submission target. The human approver sees the selected fields, extracted evidence, final amount, and the exact action waiting for approval. This is aligned with [`../../implementation/evaluation/architecture-review-checklist.md`](../../implementation/evaluation/architecture-review-checklist.md).

## Evaluation plan

The architecture is reviewed with [`../../implementation/evaluation/architecture-review-checklist.md`](../../implementation/evaluation/architecture-review-checklist.md) and the web-relevant entries in [`../../implementation/evaluation/failure-mode-catalog.md`](../../implementation/evaluation/failure-mode-catalog.md). The main acceptance criteria are:

- the agent always re-summarizes page state before acting
- the extracted reimbursement amount matches visible evidence
- the prepared submission is correct before the approval gate opens
- the final submit action is blocked until approval is recorded
- the agent can recover from one navigation mismatch without losing state discipline

The good-path artifact bundle for this case is:

- [`artifacts/web-form-agent/input-brief.md`](artifacts/web-form-agent/input-brief.md)
- [`artifacts/web-form-agent/planner-trace.md`](artifacts/web-form-agent/planner-trace.md)
- [`artifacts/web-form-agent/state-or-evidence-record.md`](artifacts/web-form-agent/state-or-evidence-record.md)
- [`artifacts/web-form-agent/verification-report.md`](artifacts/web-form-agent/verification-report.md)
- [`artifacts/web-form-agent/approval-record.md`](artifacts/web-form-agent/approval-record.md)

## Failure review

The plausible failure for this default is a page-state mistake that looks like success: the agent extracts the correct amount from a booking page, but a dynamic reimbursement form resets the selected expense category after an auto-refresh, leaving the form prepared for the wrong claim type. This maps to `Observation-action confusion` and `Indirect prompt injection` in [`../../implementation/evaluation/failure-mode-catalog.md`](../../implementation/evaluation/failure-mode-catalog.md), because the page itself becomes a source of misleading control state.

The failure review artifact for this case lives at [`artifacts/web-form-agent/failure-review.md`](artifacts/web-form-agent/failure-review.md). The review shows that a stricter final-state verification check and clearer approval evidence would have caught the reset before submission.

## Bottom line

Start from the web architecture when the environment itself is the main source of uncertainty. This case shows what disciplined web agency looks like: observe, summarize, act, verify, approve.
