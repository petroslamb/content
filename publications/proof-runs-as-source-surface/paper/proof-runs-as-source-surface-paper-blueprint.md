---
kind: paper_blueprint
package: proof-runs-as-source-surface
workflow: paper_development
status: active_experiment
run_id: phase-2-8-proof-paper-development-proof-runs
draft_manuscript: false
promotion_claim: false
---

# Paper Blueprint: Proof Runs as Source Surfaces

## Proposed Title

Proof Runs as Source Surfaces: Making Autonomous Content Work Reviewable,
Resumable, and Governed

## Abstract Draft

Autonomous content agents increasingly initialize packages, transform drafts,
coordinate evidence, and prepare publication artifacts. Existing evaluation
frames often emphasize task completion, benchmark scores, or generated output
quality, but those signals are insufficient for deciding whether a human should
trust an agent to mutate or publish a content package. This paper proposes
`proof runs as source surfaces`: retained governed run records that bind a
declared workflow, admitted context, bounded tools, review gates, subagent
handoffs, validation commands, and non-promotion evidence into an inspectable
artifact. The paper develops a lifecycle model for governed content-agent work,
maps related evidence from specification-driven agents and schema-gated
workflows, and outlines an artifact analysis of retained Reviewable Runs records.
The intended contribution is not a benchmark, publication autopilot, or claim of
agent autonomy. It is a framework for deciding what evidence must exist before
human operators should trust autonomous content mutation, resumption, or
publication preparation.

## Contribution Statement

The paper contributes a framework and systematization for treating governed
proof runs as source surfaces: durable artifacts that make agentic content work
reviewable before downstream trust, resumption, or publication decisions.

This is more than the essay claim because it names a model, an evidence taxonomy,
a reviewability standard, and an artifact-analysis plan.

## Paper Type

Framework and systematization short paper with illustrative artifact analysis.

## Route

Primary route: software-engineering workshop or ICSE NIER-style short paper
after the method is hardened. AIware may be used for fast feedback if the audit
approves it. arXiv is only a later distribution route after manuscript,
references, method, artifact statement, and checklist exist.

## Core Model

The framework has five layers:

1. **Declared intent**: workflow id, package, run id, runtime inputs, and explicit
   non-goals.
2. **Admitted context**: package status, README, evidence surfaces, workflow
   contract, and source hashes.
3. **Bounded execution**: allowed tools, allowed paths, no external mutation,
   and no lifecycle movement without gates.
4. **Reviewable handoffs**: subagent requests and results with verification
   commands, findings, and source-hash awareness.
5. **Retained evidence**: resolved run, run record, gates, logs, and local output
   artifacts that preserve what happened without promoting the output.

## Evidence Map

| Source | Paper role | Section burden |
| :--- | :--- | :--- |
| SWE-AGI (`2602.09447`) | Shows the appeal and gap of end-to-end specification-driven autonomous software construction. | Motivation and limits of capability-first trust. |
| Spec Kit Agents (`2604.05278`) | Anchors context-grounded agent workflows and phase-level hooks. | Related work on specification-grounded execution. |
| SWE-Bench Pro (`2509.16941`) | Pressures benchmark-score-only autonomy claims. | Non-claim boundary and evaluation contrast. |
| Productivity-Reliability Paradox (`2605.01160`) | Supports governance as the dependability constraint. | Governance framing. |
| Talk Freely, Execute Strictly (`2603.06394`) | Supports separating flexible interaction from schema-gated execution. | Runtime contract and schema-gating analogy. |
| Specification-Anchored Auditing (`2604.26495`) | Anchors traceable audit pipelines and phase-attributed false positives. | Artifact-analysis and auditability framing. |

## Case-Study Plan

Unit of analysis: one governed proof-campaign run for `paper_development` on
`proof-runs-as-source-surface`.

Initial corpus:

- resolved run artifact
- run record artifact
- subagent request/result artifacts
- validation logs
- package-local paper outputs
- any review gate reached by the run

Coding categories:

- declared workflow identity
- context admission and source hashes
- allowed write/read boundaries
- external mutation and lifecycle movement outcomes
- handoff/result verification shape
- output-to-evidence traceability
- explicit blocker or gate status
- promotion/non-promotion language

## Full Outline

1. Introduction: why output quality is not enough for autonomous content trust.
2. Problem: hidden mutation, missing context, and unverifiable resumption.
3. Framework: proof runs as source surfaces.
4. Evidence taxonomy: what must be retained before trust decisions.
5. Related work: specification-driven agents, benchmarks, governance, and
   schema-gated workflows.
6. Artifact analysis method: unit, corpus, coding scheme, and non-claims.
7. Illustrative findings from the proof-campaign record.
8. Limitations: local repo, content workflow, no external validity claim.
9. Implications for governed agent workflows.

## Risks And Limitations

- The package currently has a compact source essay, so the method must carry the
  paper burden.
- The evidence index is enough for planning but not yet citation-grade drafting.
- The artifact-analysis corpus is local and illustrative, not a general
  benchmark.
- The paper must avoid claiming that retained proof evidence proves autonomous
  safety or workflow promotion.

## Forbidden Framing

- Do not claim agents can publish themselves safely.
- Do not treat benchmark scores as sufficient trust evidence.
- Do not treat arXiv as peer review.
- Do not claim this proof run promotes `paper_development`.
- Do not change package status from this paper route.
