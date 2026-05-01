---
kind: paper_blueprint
package: "literate-workflow-programming/specification-surface-source-of-truth"
status: experimental
created: "2026-04-30"
source_candidate: "../iterations/r3/specification-surface-source-of-truth-candidate-r3.md"
source_claim_ledger: "../specification-surface-source-of-truth-claim-boundary-ledger.md"
paper_route: "framework_systematization_case_study"
workflow: "paper_development"
---

# Specification Surfaces as Source-of-Truth Artifacts in AI-Assisted Software Engineering

## Purpose

This blueprint turns the r3 essay argument into the easiest viable paper route. It is not a Substack rewrite and should not be promoted into the live essay. Its job is to define a research-paper contribution that can stand on more than essay strength.

The paper should be written as a `cs.SE` framework and systematization paper with a small illustrative artifact analysis. It should not be submitted as an opinion essay, pure position paper, pure literature review, or broad commentary on vibe coding.

## One-Sentence Paper Claim

AI-assisted software work becomes more governable when the artifacts that express intent are maintained as specification surfaces: operationally coupled artifacts that constrain, validate, trace, authorize, or repair generated software behavior.

## Proposed Title

Primary title:

`Specification Surfaces as Source-of-Truth Artifacts in AI-Assisted Software Engineering`

Backup titles:

- `Specification Surfaces for Governed AI-Assisted Software Engineering`
- `From Generated Diffs to Governed Intent: Specification Surfaces in AI-Assisted Software Workflows`
- `Reviewing the Surface Before the Diff: Source-of-Truth Artifacts for AI-Assisted Development`

## Abstract Draft

AI-assisted software workflows expose a review asymmetry: generated code is visible in diffs, while the intent that governed generation often remains outside maintained artifacts. This paper introduces `specification surfaces`: maintained artifacts that acquire operational force because they constrain, validate, trace, authorize, or repair AI-assisted software work through typing, linting, validation, trace links, runtime interpretation, or versioned review. The concept excludes passive documentation and one-off prompts unless they are connected to a control, evaluation, or maintenance loop. We present a taxonomy of specification-surface types, a lifecycle model of `specify -> generate -> validate -> trace -> repair`, and a literature mapping across spec-driven development, multi-agent specification gaps, agent harnesses, context enforcement, trace compliance, validation frameworks, and claim-level auditability. We then analyze a file-backed editorial/software workflow system as an illustrative case study, focusing on workflow contracts, gate definitions, status manifests, runtime validation, and retained run evidence. The contribution is a framework for identifying where source-of-truth authority resides in AI-assisted software engineering and how review can include upstream intent without dismissing the continued importance of generated code. The paper argues that governability improves when intent can be inspected before execution, checked during execution, and repaired after failure.

## Paper Type

Framework + systematization + illustrative artifact analysis.

This is not a benchmark paper. It can become one later, but the minimum viable paper should avoid pretending to measure general effectiveness. Its research contribution is a disciplined concept, taxonomy, lifecycle, literature map, and concrete case analysis.

## Contribution Statement

The paper should make five explicit contributions:

1. A crisp definition of `specification surface` as a governed, operationally coupled source-of-truth artifact in AI-assisted software work.
2. A taxonomy of specification-surface types, separating source, runtime, validation, trace, evidence, context, repair, and authority/gate surfaces.
3. A lifecycle model showing how surfaces govern the sequence `specify -> generate -> validate -> trace -> repair`.
4. A systematization table mapping existing literature into the taxonomy and lifecycle model.
5. An illustrative artifact analysis of this repo's `content-agent` / workflow-gate machinery as a file-backed example of governed specification surfaces.

## Definition

A specification surface is a maintained artifact that becomes part of the source-of-truth boundary for AI-assisted software work because humans or tools use it to constrain, validate, trace, authorize, or repair generated behavior.

The artifact may be natural language, YAML, schema, tests, contracts, policy files, traces, or claim ledgers. Syntax is not the defining property. Operational coupling is.

### Inclusion Criteria

An artifact can be treated as a specification surface when at least one of these is true:

- It constrains allowed behavior before execution.
- It is parsed, typed, linted, interpreted, compiled, or validated by tooling.
- It drives generation or orchestration.
- It defines tests, checks, gates, policies, or completion criteria.
- It links outputs to governing intent or supporting evidence.
- It records traceable execution state that can be inspected or replayed.
- It becomes a repair target when a failure exposes ambiguity, drift, or missing intent.

### Exclusion Criteria

An artifact is not automatically a specification surface merely because it is written down.

Exclude:

- passive docs that no process maintains or validates;
- ordinary README files that only orient humans;
- one-off prompts or chat transcripts that do not become durable, reviewable artifacts;
- context files that are not evaluated, enforced, or kept current;
- generated code outputs when they are only downstream products rather than governing intent;
- broad claims that natural language itself is code.

## Research Questions

RQ1. What artifact classes currently act as specification surfaces in AI-assisted software engineering?

RQ2. How do these surfaces distribute authority across the lifecycle from specification to repair?

RQ3. How can an artifact analysis identify whether a workflow treats intent as governed source of truth rather than as informal prompt context?

## Category And Route Recommendation

Recommended arXiv category if a preprint is used:

- Primary: `cs.SE`
- Cross-list: `cs.AI` only if the final paper foregrounds agent systems, not merely AI-assisted coding as context.

Do not default to `cs.PL` unless the final paper formalizes a specification language or semantics. Do not default to `cs.SY` / `eess.SY` unless the paper seriously uses control-system modeling. `cs.HC`, `cs.MA`, or `cs.CY` can be mentioned as adjacent readerships, but they should not be the default category for this version.

Recommended venue route:

1. Workshop or venue submission first, preferably in a software-engineering or agentic-software-engineering track. OpenReview may be the submission/review infrastructure if the chosen venue uses it, but OpenReview itself is not acceptance.
2. If accepted, post the accepted or camera-ready version to arXiv with the venue reference if the venue allows it.
3. If posting before venue acceptance, submit only after the draft is clearly an original research/framework article with a concrete case analysis. Do not submit a lightly academicized essay.

Reasoning:

- arXiv is a moderated distribution service, not peer review. Its moderation process checks fit, scholarly standards, and category appropriateness; it does not provide peer-review feedback.
- arXiv's Computer Science category has tightened practice around review/survey articles and position papers. A paper that looks like a position paper or annotated bibliography is at elevated risk unless it has already completed peer review.
- A framework article with a taxonomy, lifecycle model, literature map, and artifact analysis has a better route than a pure position paper.

Official route references:

- arXiv category taxonomy: https://arxiv.org/category_taxonomy
- arXiv moderation policy: https://info.arxiv.org/help/moderation/index.html
- arXiv content types: https://info.arxiv.org/help/policies/content-types.html
- arXiv CS review/position update: https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/
- OpenReview about page: https://openreview.net/about

## Full Outline

### 1. Introduction

Opening problem:

- AI-assisted code review can inspect generated diffs while missing the upstream artifact that governed generation.
- The problem is not that code review stops mattering. The problem is that code review is incomplete when controlling intent remains informal.

Core move:

- Introduce specification surfaces as governed source-of-truth artifacts for AI-assisted work.
- State that the paper studies where authority resides, not whether natural language is code.

Contributions:

- definition;
- taxonomy;
- lifecycle model;
- literature mapping;
- illustrative artifact analysis.

Expected figure:

- Figure 1: `specify -> generate -> validate -> trace -> repair`, with surface types attached to each stage.

### 2. Background And Motivation

2.1 Spec-driven development:

- Use `2602.00180` to place the work in the spec-first, spec-anchored, spec-as-source spectrum.
- Carry the minimum-rigor principle: use enough specification to remove consequential ambiguity, not maximum ceremony.

2.2 Specification gaps in code agents:

- Use `2603.24284` as the hinge evidence that underspecification can produce integration failure under multi-agent generation.
- The key lesson is asymmetric: diagnostics explain failures, but restored specification is the recovery mechanism in the studied setting.

2.3 Professional control:

- Use `2512.14012` to frame professional agent use as planning, supervision, validation, version control, and domain judgment.
- Use this as practice context, not as a claim that every experienced developer already uses specification surfaces.

### 3. Definition: Specification Surface

Define the term and distinguish it from adjacent terms:

- specification;
- documentation;
- prompt;
- context;
- test;
- trace;
- generated implementation.

Required boundary paragraph:

The paper does not claim that natural language is code, that all docs become governed specs, that generated implementation stops mattering, or that stricter specification always improves behavior.

### 4. Taxonomy Of Specification Surfaces

Use Table 1 below as the paper's taxonomy table.

The section should emphasize that the rows are roles, not mutually exclusive file types. One artifact can occupy multiple roles when it is both human-reviewable and machine-interpreted.

### 5. Lifecycle Model

Define the lifecycle:

1. Specify: establish intent, constraints, accepted behavior, and authority.
2. Generate: produce implementation, workflow action, prompt artifact, or intermediate output from a surface.
3. Validate: check conformance through tests, validators, linters, contract checks, or gate evaluations.
4. Trace: retain evidence of what ran, which inputs were admitted, and which constraints applied.
5. Repair: update the governing surface, not only the downstream output, when failures expose missing or stale intent.

Expected figure:

- Figure 2: feedback loop from validation/trace failure back into specification-surface repair.

### 6. Literature Mapping

Use Table 2 below as the main systematization table.

The section should be written as a structured mapping, not as a broad literature review. Each paper should be used for the surface role it demonstrates.

### 7. Case Study: File-Backed Workflow Governance

Use this repo's `content-agent` / workflow-gate machinery as an illustrative case study.

Case-study claim:

The repository demonstrates how source-of-truth authority can be distributed across maintained workflow contracts, package manifests, gate definitions, runtime validators, and retained run evidence.

Do not claim:

- that this repo proves general effectiveness;
- that the workflow is a universal best practice;
- that logs are the source of truth;
- that the system has complete semantic provenance.

Expected table:

- Table 3: repo artifact -> taxonomy role -> lifecycle stage -> validation/trace hook -> failure/repair implication.

### 8. Discussion

Topics:

- Why the frame changes code review: review must inspect the governing surface as well as the generated diff.
- Why generated code still matters: it remains the executable artifact carrying bugs, latency, security exposure, and maintenance cost.
- Why context files are risky: they become surfaces only when maintained and evaluated.
- Why formality is not monotonic: specification detail is useful when it removes consequential ambiguity and can be checked.
- How specification surfaces can fail: rot, over-specification, stale authority, validator mismatch, false confidence, and unreviewed generated checks.

### 9. Limitations

Required limitations:

- The taxonomy is conceptual and will need validation against more systems.
- The case study is single-case and illustrative.
- The literature map uses mostly recent preprints and should be treated as a fast-moving evidence surface.
- The paper does not include a controlled empirical benchmark.
- The framework does not prove that natural language is code or that generated code is disposable in ordinary software projects.
- Stronger specification may add friction or harm behavior when mismatched to model, domain, or tool maturity.

### 10. Conclusion

Closing claim:

AI-assisted software work becomes governable when intent can be read before execution, checked during execution, traced after execution, and repaired when failures expose missing decisions.

## Table 1: Taxonomy Of Specification Surfaces

| Surface Type | Working Definition | Operational Force | Examples | Main Risks |
| :--- | :--- | :--- | :--- | :--- |
| Source surfaces | Artifacts that state desired behavior, constraints, interfaces, or acceptance criteria before implementation. | Guide generation, constrain implementation, establish review target. | Product specs, BDD scenarios, API contracts, schemas, interface descriptions, task contracts. | Drift, ambiguity, over-specification, false confidence when the spec is wrong. |
| Runtime surfaces | Artifacts interpreted by a runtime to orchestrate agent or workflow behavior. | Execute control flow, roles, state transitions, tool access, and decomposition. | Agent harnesses, workflow YAML, agent configs, skill/workflow definitions. | Hidden runtime semantics, weak replayability, model-dependent interpretation. |
| Validation surfaces | Artifacts or generated checks that test whether output conforms to stated intent. | Fail builds, block commands, score behavior, detect policy or contract violations. | Unit tests, hidden tests, lint rules, AST checks, shell shims, architectural validators, gate checks. | Validator mismatch, brittle checks, overfitting, Goodharting visible tests. |
| Trace surfaces | Retained execution evidence showing what ran, what state existed, and which decisions occurred. | Support audit, debugging, replay, and comparison across runs. | Agent traces, checkpoint logs, replay records, run records, trajectory logs. | Treating logs as authority, excessive noise, missing semantic links. |
| Evidence surfaces | Artifacts linking claims, outputs, or decisions to supporting evidence. | Make review and audit possible at claim or decision granularity. | Claim ledgers, source-burden maps, provenance graphs, contradiction logs, review packets. | Incomplete provenance, weak evidence semantics, stale claim maps. |
| Context surfaces | Maintained project instructions or context artifacts used by humans or agents. | Shape allowed behavior only when admitted, maintained, and evaluated. | AGENTS.md, repository instructions, coding guidelines, skill docs. | Passive-document trap, bloat, contradiction, stale guidance, unevaluated context. |
| Repair surfaces | Artifacts that convert failure detection into revisions of prompts, specs, policies, or workflow code. | Close the loop by changing the upstream governing surface after failure. | Failure taxonomies, root-cause reports, validation recommendations, review decisions. | Local symptom fixing without upstream repair, unreviewed automated suggestions. |
| Authority/gate surfaces | Artifacts that decide what may run, move, publish, or be promoted. | Authorize lifecycle movement, external mutation, promotion, or package state changes. | `status.yaml`, `workflow.yaml`, gate contracts, pipeline profiles, approval records. | Authority confusion, bypassed gates, logs outranking source contracts. |

## Table 2: Evidence Mapping

| Evidence | Surface Role | Lifecycle Stages | Use In Paper | Boundary |
| :--- | :--- | :--- | :--- | :--- |
| `2602.00180` Spec-Driven Development | Source surfaces; spectrum from spec-first to spec-anchored to spec-as-source. | specify, generate, validate, repair | Establishes SE grounding and the minimum-rigor principle. | Do not use to claim all projects should become spec-as-source. |
| `2603.24284` The Specification Gap | Source surfaces as coordination contracts; diagnostics as secondary. | specify, generate, validate, repair | Hinge evidence that underspecification can cause multi-agent integration failure and that restored specification can recover performance in the studied setting. | Do not generalize effect sizes beyond the experiment. |
| `2512.14012` Professional Developers Don't Vibe | Professional control practices: planning, supervision, validation, version control, domain expertise. | specify, validate, repair | Grounds anti-vibe argument in observed developer practice. | Do not claim every professional workflow already has governed surfaces. |
| `2603.17399` Bootstrapping Coding Agents | Specification-as-source artifact; implementation as downstream generated product in a narrow experiment. | specify, generate, validate | Shows a strong form of specification authority. | Do not claim generated code never matters or that all codebases can be regenerated safely. |
| `2603.25723` Natural-Language Agent Harnesses | Runtime surfaces externalized as portable executable artifacts with contracts and durable artifacts. | specify, generate, trace | Supports harness logic as reviewable runtime surface. | Do not reduce the claim to natural language alone; runtime coupling matters. |
| `2604.13346` AgentSPEX | Typed workflow/runtime surface with explicit control flow, state, checkpointing, tracing, replay, and verification. | specify, generate, validate, trace | Strong anchor for structured runtime surfaces. | Do not imply every workflow must be formalized as a DSL. |
| `2603.00822` ContextCov | Context files transformed into executable guardrails. | specify, validate, repair | Key evidence for the passive-docs-to-active-invariants distinction. | Do not claim ordinary AGENTS.md files are automatically governed surfaces. |
| `2603.08806` Test-Driven AI Agent Definition | Behavioral specs compiled into visible/hidden tests and prompt artifacts. | specify, generate, validate, repair | Supports validation surfaces and regression discipline. | Do not ignore specification-gaming and hidden-test caveats. |
| `2512.18940` FASTRIC | Prompt interaction protocols as explicit FSM-like specs with trace conformance. | specify, validate, trace | Supports the point that formality is a design parameter, not a universal good. | Do not claim more formal specification always improves behavior. |
| `2603.23806` AgentPex / Willful Disobedience | Trace surfaces evaluated against extracted behavioral rules. | validate, trace | Supports procedure-level trace checking beyond outcome-only scoring. | Keep prompts/specifications primary; traces diagnose conformance. |
| `2603.29848` AgentFixer | Validation and root-cause modules that turn failures into repair recommendations. | validate, trace, repair | Supports repair lifecycle and validation-driven refinement. | Do not claim automated repair replaces human review. |
| `2602.13855` From Fluent to Verifiable | Claim-level auditability and semantic provenance for research agents. | trace, validate, repair | Supports evidence surfaces and claim-evidence maps. | Do not claim this repo already implements full semantic provenance graphs. |
| Local `content-agent` / workflow-gate machinery | Authority, runtime, validation, trace, and evidence surfaces in a file-backed workflow. | specify, generate, validate, trace, repair | Illustrative case study. | Single-case artifact analysis only, not proof of general effectiveness. |

## Table 3: Case Study Artifact Map

| Local Artifact | Taxonomy Role | Lifecycle Stage | What To Analyze |
| :--- | :--- | :--- | :--- |
| `AUTHORITY.md` | Authority surface | specify | Declares source-of-truth ordering and prevents logs/views from outranking source contracts. |
| `workflows/*/workflow.yaml` | Runtime and authority surface | specify, generate, validate | Declares context dependencies, allowed paths, required tools, validation hooks, outputs, gates, and trace requirements. |
| `publications/**/status.yaml` | Authority and context-admission surface | specify | Resolves package kind, revision, live draft, evidence path, blueprint path, and lifecycle state. |
| `harness_policy.yaml` | Authority and enforcement surface | specify, validate | Sets local write boundaries, approval requirements, and enforcement posture. |
| `gate_contracts.yaml` | Gate and validation surface | validate, repair | Defines movement, quality, promotion, and external-mutation gates with required artifacts and validators. |
| `pipeline_profiles.yaml` | Route surface | specify, repair | Defines ordered workflows, required gates, and fallback routes. |
| `./content-agent` and `scripts/content_agent.py` | Runtime surface | generate, validate, trace | Executes declared contracts, resolves context, reports validation and next actions. |
| `reviewable-runs/logs/` and `reviewable-runs/gates/` | Trace and evidence surfaces | trace, repair | Retain run and gate evidence without becoming the source of truth for workflow behavior. |
| Package claim ledgers and review packets | Evidence and repair surfaces | validate, repair | Record what claims are allowed, blocked, revised, or promoted. |

## Case Study Plan

Case study type:

Illustrative artifact analysis of a file-backed workflow system.

Unit of analysis:

The `literate-workflow-programming/specification-surface-source-of-truth` package moving through governed essay-iteration machinery, with broader reference to root workflow contracts.

Artifact set:

- `AUTHORITY.md`
- `harness_policy.yaml`
- `gate_contracts.yaml`
- `pipeline_profiles.yaml`
- `workflows/essay-iteration/workflow.yaml`
- `workflows/evidence-authorization/workflow.yaml`
- package `status.yaml`
- package `README.md`
- package claim ledger
- `./content-agent status`, `next`, and `validate` outputs
- relevant run logs and gate-check records in `reviewable-runs/logs/`

Analysis steps:

1. Inventory surfaces and classify each artifact using Table 1.
2. Trace one lifecycle path from package status and workflow contract through runtime validation and retained evidence.
3. Identify which artifacts are source authority and which are evidence records.
4. Record where gates require human approval, validation, or promotion decisions.
5. Identify at least one repair loop: a validation or review outcome that changes a governing surface rather than only changing prose or generated output.
6. Present the case as an existence example of the taxonomy, not as evidence that the taxonomy improves productivity or quality.

Minimal case-study output:

- One artifact map table.
- One lifecycle trace diagram.
- One short narrative showing how `content-agent validate --workflow essay_iteration --package literate-workflow-programming/specification-surface-source-of-truth` resolves declared context and evidence requirements.
- One limitation paragraph stating that the analysis is endogenous and illustrative.

## Method Section Blueprint

The paper should use a lightweight qualitative method:

1. Define inclusion criteria for specification surfaces.
2. Select papers from the local evidence surface because they each instantiate one or more roles in the taxonomy.
3. Code each paper by surface type and lifecycle stage.
4. Select the local workflow system as a convenience case because its specification, validation, gate, and evidence artifacts are file-backed and inspectable.
5. Analyze artifacts by tracing declared authority, runtime interpretation, validation hooks, and retained evidence.

Threats to validity:

- Selection bias in the literature map.
- Single-system case-study bias.
- Author/operator involvement in the local case.
- Rapidly changing AI-agent tooling.
- Preprint-heavy evidence base.

Mitigation:

- Keep the claims conceptual and illustrative.
- Make the coding table explicit.
- Keep forbidden claims visible.
- Avoid effectiveness claims without measurement.

## Figures And Tables To Build

Required:

- Figure 1: Specification-surface lifecycle.
- Table 1: Taxonomy of specification surfaces.
- Table 2: Evidence mapping.
- Table 3: Case-study artifact map.

Optional:

- Figure 2: Authority layering in the local workflow system.
- Table 4: Failure modes and repair targets.
- Appendix table: inclusion/exclusion decisions for context files and passive docs.

## Paper MVP Checklist

The paper is viable when it has:

- one definition;
- one taxonomy;
- one lifecycle model;
- one literature mapping table;
- one concrete artifact analysis;
- careful limitations;
- `cs.SE` framing;
- no dependence on essay strength alone.

The paper is not viable if it remains:

- a strong essay;
- a position statement;
- a broad literature review;
- an arXiv submission without a concrete contribution.

## Risks And Limitations

| Risk | Why It Matters | Mitigation |
| :--- | :--- | :--- |
| Looks like a position paper | arXiv CS treatment of position papers is stricter, and venues may reject unfalsifiable claims. | Keep the framework, tables, and case analysis central. |
| Looks like a survey | A broad literature map without a new model is weak. | Use literature only to populate the taxonomy and lifecycle. |
| Overclaims natural language | The essay's public energy could tempt a "natural language is code" frame. | Repeat that syntax is secondary and operational coupling is decisive. |
| Overclaims context files | AGENTS.md-style files are mixed evidence and can become stale or contradictory. | Treat them as context surfaces only when maintained and evaluated. |
| Overclaims formality | Some evidence shows formality has model- and task-specific optima. | Frame formality as a design parameter and validation aid. |
| Treats logs as authority | Trace evidence can be mistaken for source of truth. | Keep logs and gates as evidence surfaces subordinate to source authority. |
| Local case is self-referential | A repo-authored workflow system can look anecdotal. | Present it as an illustrative artifact analysis, not effectiveness proof. |
| Generated code gets dismissed | The argument can sound like code review no longer matters. | State repeatedly that generated code remains reviewable and consequential. |

## Forbidden Framing

Do not write:

- `natural language is code`;
- passive docs are specification surfaces;
- prompts are source of truth because they came first;
- generated code no longer matters;
- richer specs always improve model behavior;
- all teams should adopt spec-as-source;
- the local repo proves general effectiveness;
- arXiv acceptance would equal peer review.

## Next Work Items

1. Convert this blueprint into a 2-3 page extended abstract with the definition, taxonomy, lifecycle figure, and case-study plan.
2. Build the literature mapping table as a separate CSV or appendix-ready markdown table.
3. Collect the case-study artifact trace from `content-agent status`, `next`, and `validate`, plus one representative gate-check log.
4. Draft the case-study section before drafting the full introduction; the case determines whether the paper is a research/framework article or slides back into a position essay.
5. Only after the case-study section exists, decide between workshop-first submission and a `cs.SE` preprint.
