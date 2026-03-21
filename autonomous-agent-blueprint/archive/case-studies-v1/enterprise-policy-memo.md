# Worked Case Study: Enterprise Policy Memo

> Historical note: This v1 packet-oriented case study was superseded by [`../../reviewable-runs.md`](../../reviewable-runs.md) and [`../../case-studies/enterprise-policy-memo/README.md`](../../case-studies/enterprise-policy-memo/README.md).

This case applies the enterprise reference architecture to a concrete internal-governance task: drafting a policy memo that will be reviewed by compliance and then posted to an internal knowledge base.

## How To Read This Case

Read this file in four passes:

1. read `Problem and operating constraints` to understand why this is an enterprise task rather than a browser or coding task
2. read `Default architecture selected` plus `Why this architecture wins here` to see which abstract defaults were instantiated
3. open the artifact bundle in [`artifacts/enterprise-policy-memo/`](artifacts/enterprise-policy-memo/) to see the good path
4. finish with `Failure review` and [`../../evaluation/architecture-review-checklist.md`](../../evaluation/architecture-review-checklist.md) to see how the same design is pressure-tested

## Problem and operating constraints

The agent is asked to draft a memo explaining the company's document retention and vendor-sharing policy for AI-generated customer support summaries. It must synthesize three internal policy documents, cite evidence cleanly, avoid using superseded policy text, and stop before any external circulation. The workflow is approval-gated, policy-sensitive, and expensive to get wrong because a plausible but stale memo could create operational and legal mistakes.

## Default architecture selected

This case instantiates the abstract enterprise architecture in [`../../use-cases/enterprise-agent.md`](../../use-cases/enterprise-agent.md). It adopts the memory, reasoning, action, and safety defaults from [`../../practical-chapter-blueprints/01-memory-blueprint.md`](../../practical-chapter-blueprints/01-memory-blueprint.md), [`../../practical-chapter-blueprints/02-reasoning-planning-blueprint.md`](../../practical-chapter-blueprints/02-reasoning-planning-blueprint.md), [`../../practical-chapter-blueprints/03-action-tool-use-blueprint.md`](../../practical-chapter-blueprints/03-action-tool-use-blueprint.md), and [`../../practical-chapter-blueprints/06-safety-blueprint.md`](../../practical-chapter-blueprints/06-safety-blueprint.md).

The design is anchored by named sources: [`../../papers/memgpt.md`](../../papers/memgpt.md), [`../../papers/react.md`](../../papers/react.md), [`../../papers/chain_of_verification.md`](../../papers/chain_of_verification.md), [`../../papers/gorilla.md`](../../papers/gorilla.md), and [`../../papers/greshake_indirect_prompt_injection.md`](../../papers/greshake_indirect_prompt_injection.md).

The matching artifact bundle lives in [`artifacts/enterprise-policy-memo/`](artifacts/enterprise-policy-memo/).

## Why this architecture wins here

The task is fundamentally an evidence-grounded drafting workflow, not an open-ended browser or coding task. The enterprise architecture wins because it treats retrieval as a governed memory layer, uses a bounded ReAct-style planning loop to gather policy evidence, and then forces the memo through explicit verification and approval before publication.

Typed artifact production matters here more than autonomy theater. The memo has to be reviewable, source-backed, and easy for a human approver to audit. That makes the enterprise default stronger than either a conversational multi-agent design or a browser-first agent, both of which would widen the trust boundary without improving the output contract.

## Alternatives rejected

- Browser-first policy gathering was rejected because the documents already exist in an indexed internal knowledge store, and adding browsing would expand the untrusted-content surface without improving retrieval quality; basis: [`../../use-cases/enterprise-agent.md`](../../use-cases/enterprise-agent.md), [`../../papers/gorilla.md`](../../papers/gorilla.md), [`../../papers/webagent.md`](../../papers/webagent.md).
- Free-form multi-agent drafting was rejected because the main requirement is evidence discipline, not role-played debate, and typed memo sections are easier to verify than conversational handoffs; basis: [`../../practical-chapter-blueprints/05-multi-agent-design-blueprint.md`](../../practical-chapter-blueprints/05-multi-agent-design-blueprint.md), [`../../papers/autogen.md`](../../papers/autogen.md), [`../../papers/metagpt.md`](../../papers/metagpt.md).
- Automatic memory logging of every retrieval result was rejected because stale or superseded policy text is itself a risk surface, so memory writes must stay curated and provenance-aware; basis: [`../../practical-chapter-blueprints/01-memory-blueprint.md`](../../practical-chapter-blueprints/01-memory-blueprint.md), [`../../papers/memgpt.md`](../../papers/memgpt.md), [`../../papers/agentpoison.md`](../../papers/agentpoison.md).

## Trust boundaries and approval gates

The key trust boundary is between system instructions and retrieved policy text. Retrieved policy snippets can support the memo, but they cannot override the drafting policy or the approval rules. The design also separates read-only retrieval from any write action to the knowledge base.

Human approval happens after verification and before publication to the internal policy hub. The approver sees the memo, the evidence table, the verification report, and the explicit note that no external circulation is permitted until approval is granted. This maps directly to the controls in [`../../evaluation/architecture-review-checklist.md`](../../evaluation/architecture-review-checklist.md).

## Evaluation plan

The architecture is reviewed with [`../../evaluation/architecture-review-checklist.md`](../../evaluation/architecture-review-checklist.md) and pressure-tested against the enterprise-relevant entries in [`../../evaluation/failure-mode-catalog.md`](../../evaluation/failure-mode-catalog.md). The main acceptance criteria are:

- the memo cites current policy text rather than stale or superseded guidance
- every claim in the memo has a matching evidence row
- the artifact is typed and reviewable rather than conversationally vague
- publication remains blocked until approval is recorded

The good-path artifact bundle for this case is:

- [`artifacts/enterprise-policy-memo/input-brief.md`](artifacts/enterprise-policy-memo/input-brief.md)
- [`artifacts/enterprise-policy-memo/planner-trace.md`](artifacts/enterprise-policy-memo/planner-trace.md)
- [`artifacts/enterprise-policy-memo/state-or-evidence-record.md`](artifacts/enterprise-policy-memo/state-or-evidence-record.md)
- [`artifacts/enterprise-policy-memo/verification-report.md`](artifacts/enterprise-policy-memo/verification-report.md)
- [`artifacts/enterprise-policy-memo/approval-record.md`](artifacts/enterprise-policy-memo/approval-record.md)

## Failure review

The plausible failure for this default is not a random hallucination. It is a governed failure: retrieval returns a superseded retention-policy paragraph that still looks legitimate, the memo absorbs it, and the first draft becomes directionally polished but wrong on retention duration. This maps directly to `Stale memory reuse` and `Retrieval poisoning` in [`../../evaluation/failure-mode-catalog.md`](../../evaluation/failure-mode-catalog.md), even though the issue may come from benign staleness rather than a malicious corpus attack.

The failure review artifact for this case lives at [`artifacts/enterprise-policy-memo/failure-review.md`](artifacts/enterprise-policy-memo/failure-review.md). The review shows that stronger freshness metadata and a mandatory supersession check in the verification layer would likely have caught the error before approval.

## Bottom line

Start from the enterprise architecture when the output is a policy-sensitive artifact that must be evidence-backed, typed, and approval-gated. This case shows what that looks like when the repo's abstractions are applied to a concrete drafting task rather than left at the taxonomy level.
