# Reviewable Runs

This doc is the conceptual source of truth for this package.

The framework is not trying to teach that a serious system emits six neat markdown files. It is trying to teach that a serious system makes a run reviewable.

## Why This Exists

The upstream blueprint package already requires most of the ingredients that make reviewable runs necessary:

- bounded control loops
- replayable and inspectable actions
- episodic traces and prior-failure memory
- explicit verification
- approval gates for meaningful side effects
- post-incident replay and review

What was missing was the run-level contract that ties those expectations together for one meaningful execution.

Reviewable runs fills that gap.

## Why This Matters

A trace alone is not enough. A trace can show that the system did something, but it does not by itself explain what the task was, what evidence supported the run, how the result was checked, whether a human approved the risky step, or how the same setup could fail. A deployable agent system should emit or be able to reconstruct enough records to answer those questions.

## Three Layers

### Agent Runtime Outputs

These are the direct outputs of the acting system:

- actions
- observations
- tool calls
- intermediate state
- optional plan text

These outputs matter, but they are not the full review surface.

### System Records

These are the records that make the run inspectable after the fact:

- task spec
- execution trace
- evidence, provenance, or state record
- verification report

These records may be emitted directly during the run or reconstructed from logs and stored state.

### Governance Records

These are the records that make high-impact or failed runs accountable:

- approval decision when the system crosses a meaningful side-effect boundary
- failure review when something fails or when a deliberate postmortem or red-team exercise is being run

These records are conditional in production. They are not required for every low-risk successful run, but the system should support them when the situation calls for them.

## Six Review Questions

Every serious system in this framework should be able to answer these six questions:

| Review question | Typical record | When it matters most |
| --- | --- | --- |
| What was the task? | task spec | every meaningful run |
| What happened? | execution trace | every meaningful run |
| What did it rely on? | evidence, provenance, or state record | any run grounded in retrieval, environment state, or tools |
| How was it checked? | verification report | any run that produces an output or proposes an action |
| Who approved impact? | approval decision | high-impact, external, destructive, or hard-to-roll-back actions |
| What failed or could fail? | failure review | incidents, near misses, red-team exercises, and teaching examples |

The question is not whether these exact filenames exist. The question is whether the system can answer the review question with emitted or reconstructable records.

## Trace Is Only One Record

The most common failure in agent demos is to confuse trace visibility with system reviewability. Seeing the action loop is useful, but it does not replace evidence provenance, verification scope, approval context, or post-failure analysis. This framework treats traces as necessary but incomplete.

## Risk Tiers

This framework is not saying that every low-value run must emit a heavy dossier.

### Low Risk

Use lightweight reconstruction. Runtime outputs and ordinary logs may be enough if the system can still recover task, action history, and basic verification on demand.

### Medium Risk

Use explicit task, trace, evidence, and verification records. Approval may be optional, but the run should still be easy to reconstruct after the fact.

### High Risk

Use the full surface. Task, trace, evidence, verification, approval, and failure review should all be available or reconstructable.

## How This Package Uses The Model

- `../autonomous-agent-blueprint/implementation/use-cases/` remains the upstream architecture source.
- `dossiers/` turns those default architectures into linear examples that answer the six review questions for one concrete scenario.
- `dossiers/*/runtime-records/` contains the core run records.
- `dossiers/*/governance-records/` contains the approval and failure-review records used when the scenario crosses a governance boundary.
- `evaluation/` explains how to judge both architecture readiness and run-level reviewability.
- `templates/` contains both direct record templates and adjacent support patterns.

## What Not To Infer

- A production system does not need to store literal markdown files.
- Approval and failure review are not universal per-step outputs.
- A readable dossier is for humans; the underlying system may store the same information in logs, database rows, UI events, or postmortem documents.
- The goal is reviewability, not document theater.
- This is not a model interpretability framework.
- This is not a claim that the six record names are universal or final.
