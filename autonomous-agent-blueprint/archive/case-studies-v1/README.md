# Worked Case Studies

> Historical note: This is the archived v1 packet-oriented worked-example layer. The default path is now [`../../reviewable-runs.md`](../../reviewable-runs.md) and the rebuilt [`../../case-studies/README.md`](../../case-studies/README.md).

This folder is the repo's applied proof layer. The `use-cases/` docs tell you the abstract default architecture; the files here show what those defaults look like when a real task, a realistic artifact trail, and a concrete failure review are all placed side by side.

The key idea is that the artifacts are not decorative documentation. They are markdown-shaped stand-ins for the records a real deployable system should emit or be able to reconstruct. A trace is only one of those records. Serious systems also need a task definition, evidence or state record, verification result, approval record when actions matter, and an incident-style failure review when something goes wrong.

## What A Case Study Does

Each case study in this folder:

- instantiates one existing reference architecture
- names the chapter blueprints and paper notes that justify the design
- shows one realistic good-path artifact bundle
- shows one plausible failure and how the repo's review stack would analyze it

This is the fastest path when you already believe the repo's abstractions and now need to see what a bounded agent workflow looks like in practice.

## Canonical Examples

- [`enterprise-policy-memo.md`](enterprise-policy-memo.md)
  Approval-gated enterprise knowledge agent that drafts a policy memo from internal documents and retrieved evidence.
- [`coding-bugfix-agent.md`](coding-bugfix-agent.md)
  Repository-scoped coding agent that diagnoses a failing test, patches code, reruns checks, and produces a reviewable diff.
- [`web-form-agent.md`](web-form-agent.md)
  Browser-based agent that gathers evidence across pages and completes a high-friction form flow with approval before submission.

## Shared Structure

Every case study uses the same structure:

1. Problem and operating constraints
2. Default architecture selected
3. Why this architecture wins here
4. Alternatives rejected
5. Trust boundaries and approval gates
6. Evaluation plan
7. Failure review
8. Bottom line

## Artifact Contract

Each case study has a sibling artifact bundle under `artifacts/` with exactly these files:

- `input-brief.md`
- `planner-trace.md`
- `state-or-evidence-record.md`
- `verification-report.md`
- `approval-record.md`
- `failure-review.md`

The artifacts are synthetic but realistic. They are not placeholders, and they are intentionally shaped to match the underlying architecture rather than a generic agent story.

In production, these would not necessarily be markdown files. They might be job specs, run traces, retrieval provenance records, validation reports, approval events in a UI, or postmortems. The point of this folder is to make those system responsibilities concrete and inspectable.

## How To Use This Folder

Read in this order:

1. the matching abstract use case in `../../use-cases/`
2. the worked case study in this folder
3. the artifact bundle under `artifacts/`
4. `../../evaluation/architecture-review-checklist.md`
5. `../../evaluation/failure-mode-catalog.md`

Use the matching chapter blueprints when you need to understand why a design choice was selected rather than merely observe its output.

## Cross-Case Comparison

If the question is "which archetype should I start from," read [`comparison-matrix.md`](comparison-matrix.md) before reading any single case in depth.
