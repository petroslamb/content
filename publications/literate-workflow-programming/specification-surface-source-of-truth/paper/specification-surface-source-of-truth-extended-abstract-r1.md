---
kind: extended_abstract
package: "literate-workflow-programming/specification-surface-source-of-truth"
revision: 1
status: draft
created: "2026-04-30"
workflow: paper_development
source_blueprint: "specification-surface-source-of-truth-paper-blueprint.md"
source_literature_map: "specification-surface-source-of-truth-literature-mapping-r1.md"
source_case_trace: "specification-surface-source-of-truth-case-study-trace-r1.md"
target_shape: "AIware short paper or ICSE NIER seed"
---

# Specification Surfaces as Source-of-Truth Artifacts in AI-Assisted Software Engineering

## Abstract

AI-assisted software workflows make generated code increasingly easy to produce and review, but they often leave the intent that governed generation outside maintained artifacts. This creates a review asymmetry: the downstream diff is visible, while the upstream source of authority may exist only in a prompt, chat transcript, stale document, or private design decision. This extended abstract introduces `specification surfaces`: maintained artifacts that acquire operational force because they constrain, validate, trace, authorize, or repair AI-assisted software work through typing, linting, validation, trace links, runtime interpretation, generated tests, or review gates. The concept excludes passive documentation and one-off prompts unless they are connected to a control, evaluation, or maintenance loop. We propose a taxonomy of specification-surface types, a lifecycle model of `specify -> generate -> validate -> trace -> repair`, and a mapping of recent AI-assisted software-engineering literature into the model. We then outline an illustrative artifact analysis of a file-backed workflow system whose package manifests, workflow contracts, gate definitions, validation commands, review packets, and run records separate source authority from evidence. The goal is a framework for reasoning about where source-of-truth authority lives in AI-assisted software work and how code review can inspect upstream intent without dismissing the continued importance of generated code.

## Keywords

AI-assisted software engineering; specification; code review; agent workflows; traceability; software process; governance.

## Problem

AI-assisted coding changes the speed and shape of implementation. Agents can produce plausible diffs, tests, summaries, and repair attempts faster than teams can reconstruct why a change was supposed to be correct. Code review still matters: generated code carries bugs, security exposure, performance costs, and maintenance obligations. But reviewing only the generated diff is incomplete when the governing intent remains informal.

The failure mode is not simply misplaced trust in a model. It is a source-of-truth problem. A reviewer may be able to see the code but not the maintained statement of intended behavior, the constraints the agent was expected to preserve, the validation surface that checked those constraints, or the repair loop that should update the governing artifact after failure. In this setting, teams need vocabulary for the artifacts that make intent reviewable and operational.

## Definition

A specification surface is a maintained artifact that becomes part of the source-of-truth boundary for AI-assisted software work because humans or tools use it to constrain, validate, trace, authorize, or repair generated behavior.

The artifact may be natural language, YAML, schema, tests, contracts, workflow definitions, policy files, traces, or claim ledgers. Syntax is not the defining property. Operational coupling is.

This definition deliberately excludes passive documentation. A README does not become a specification surface merely because an agent can read it. A prompt does not become source of truth merely because it came before generated code. A context file becomes a candidate surface only when it is maintained and connected to evaluation, enforcement, runtime interpretation, traceability, or review.

## Contributions

This paper will make four contributions:

1. It defines `specification surface` as a governed, operationally coupled artifact in AI-assisted software engineering.
2. It proposes a taxonomy of surface roles: source, runtime, validation, trace, evidence, context, repair, and authority/gate surfaces.
3. It proposes a lifecycle model in which failures flow back into the governing surface: `specify -> generate -> validate -> trace -> repair`.
4. It maps recent literature and a local file-backed workflow case into the taxonomy to show how the concept organizes existing work.

## Taxonomy

The taxonomy treats surface types as roles rather than mutually exclusive file formats. A single artifact can occupy several roles if it is both human-reviewable and machine-interpreted.

| Surface Type | Role |
| :--- | :--- |
| Source surfaces | State desired behavior, constraints, interfaces, or acceptance criteria before implementation. |
| Runtime surfaces | Are interpreted by a runtime to orchestrate agents, tools, state, control flow, or workflow decomposition. |
| Validation surfaces | Check whether generated behavior conforms to stated intent. |
| Trace surfaces | Retain execution evidence for audit, replay, debugging, or comparison. |
| Evidence surfaces | Link claims, outputs, or decisions to support and contradictions. |
| Context surfaces | Supply project guidance when maintained and evaluated rather than merely present. |
| Repair surfaces | Convert detected failures into upstream revisions of prompts, specs, tests, policies, or workflow artifacts. |
| Authority/gate surfaces | Decide what may run, move, publish, or be promoted. |

## Lifecycle Model

The lifecycle begins with specification, but it does not end with generation.

```text
specify -> generate -> validate -> trace -> repair
   ^                                      |
   |______________________________________|
```

In the first stage, a surface states intent, constraints, or authority. In the generation stage, an agent, tool, or workflow produces code or another downstream artifact. Validation checks conformance. Trace records what happened and which inputs or surfaces were admitted. Repair updates the governing surface when failures expose ambiguity, drift, stale assumptions, missing constraints, or weak evidence.

This loop is what separates governed specification surfaces from ordinary documents. The surface must be reviewable before execution, useful during execution, and repairable after failure.

## Literature Mapping

The evidence base is organized by surface role rather than by a conventional survey narrative.

Spec-driven development provides the general software-engineering baseline: specification authority can range from spec-first work, to spec-anchored work, to spec-as-source generation, with stronger rigor justified only when it removes real ambiguity and can be maintained. The Specification Gap supplies the central coordination mechanism: when multiple code agents work under partial knowledge, stripped specifications can produce integration failures, and in the studied recovery setting restoring the full specification is more useful than providing conflict reports alone. Professional-control work grounds the human practice side: experienced developers use agents through planning, supervision, validation, version control, and domain judgment rather than unconstrained delegation.

Agent and harness papers populate the runtime, validation, trace, and repair rows. Bootstrapping Coding Agents shows a narrow but strong form of specification-as-source. Natural-Language Agent Harnesses and AgentSPEX show workflow logic becoming executable through runtimes with contracts, state, checkpointing, tracing, replay, and verification. ContextCov shows how passive agent instructions can be transformed into executable guardrails. Test-Driven AI Agent Definition shows behavioral specifications generating tests and prompt artifacts. FASTRIC shows prompt-protocol formality as a design parameter rather than a monotonic good. AgentPex, AgentFixer, and claim-level auditability work show trace evaluation, validation-driven repair, and evidence surfaces for checking long-running agent outputs.

The literature map supports a bounded synthesis: source-of-truth authority can move upstream into maintained specification surfaces, but only when artifacts are connected to control, validation, traceability, or repair.

## Illustrative Case Study

The case study analyzes a file-backed editorial/software workflow system in this repository. The unit of analysis is the `specification-surface-source-of-truth` package and its surrounding workflow machinery.

The package has a `status.yaml` manifest that resolves its kind, revision, live draft, evidence path, and lifecycle stage. Root authority surfaces define which layer wins when artifacts disagree: workflow contracts, policy YAMLs, gate contracts, pipeline profiles, and package status outrank logs and views. The experimental `paper_development` workflow admits package status, package README, the live draft or candidate, claim boundary ledger, evidence surface, and paper folder. Its allowed write path is the package-local `paper/` folder, keeping paper work separate from the public essay route.

The completed r3 essay route supplies a concrete repair and promotion example. External reviews identified non-blocking polish requirements and judged the candidate to clear the north-star bar, but the external review synthesis did not authorize live draft replacement. A separate human promotion approval surface authorized copying the polished candidate into the live draft. Retained run logs record prior run and gate-check evidence, but the authority map prevents those logs from becoming source authority.

This case is useful because it separates several roles that are often collapsed: source surfaces declare intent, runtime surfaces execute declared contracts, validation surfaces report readiness, evidence surfaces record review findings, trace surfaces retain operational facts, and authority surfaces decide promotion.

## Expected Paper Form

The first complete manuscript should be a framework/systematization/case-study paper, not a benchmark paper.

The strongest short-paper version is suitable for AIware-style discussion or ICSE NIER-style early research if it keeps the case study modest and concrete. A full research-track version would need a stricter empirical method, a broader corpus of systems or workflows, or independent coding of specification-surface roles.

## Limitations

The concept is not a claim that natural language is code. Some specification surfaces may be written in ordinary language, but the defining property is operational coupling, not syntax.

The framework does not claim that all documentation becomes authoritative, that generated code stops mattering, or that richer specification always improves model behavior. Generated code remains consequential and reviewable. Documentation remains documentation unless it enters a maintenance, validation, runtime, trace, or review loop. Formality can help when it makes consequential ambiguity checkable, but it can also add friction or over-constrain behavior.

The literature map is preprint-heavy and fast-moving. The case study is single-case, local, and illustrative. It demonstrates how the taxonomy can classify a file-backed workflow system; it does not prove that the workflow improves quality, speed, or safety.

## Submission Implication

This extended abstract is enough to start a short-paper draft, but it is not yet enough for arXiv submission as a standalone research article. The next manuscript step is to expand the case-study trace into a concise method and artifact-analysis section, then decide whether the paper is strong enough for the AIware 2026 ArXiv Track or should instead mature toward ICSE 2027 NIER.
