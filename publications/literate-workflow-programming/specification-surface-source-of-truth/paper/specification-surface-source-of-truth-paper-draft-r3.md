---
kind: paper_draft
package: "literate-workflow-programming/specification-surface-source-of-truth"
revision: 3
status: pre_submission_polish
created: "2026-05-05"
workflow: paper_development
source_blueprint: "specification-surface-source-of-truth-paper-blueprint.md"
source_audit: "specification-surface-source-of-truth-draftability-audit-r1.md"
source_approval_gate: "specification-surface-source-of-truth-paper-draft-approval-gate-r1.md"
source_readiness_review: "specification-surface-source-of-truth-submission-readiness-review-r2.md"
target_route: aiware_2026_arxiv_track_round_2
external_submission_allowed: false
bibliography: references.bib
link-citations: true
---

# Specification Surfaces as Source-of-Truth Artifacts in AI-Assisted Software Engineering

Petros Lambropoulos  
Rooted Layers  
petroslamb.dev@gmail.com

## Abstract

AI-assisted software review usually begins with the generated diff, even when the decision a model followed lives somewhere else: a prompt, chat transcript, stale note, workflow file, test, harness, approval record, or private design choice. That mismatch creates a source-of-truth problem. Reviewers can inspect the downstream artifact while the artifact that authorized, constrained, or evaluated the work may remain outside the governed system. I define a `specification surface` as a maintained artifact with operational standing in AI-assisted software work because people or tools use it to constrain, validate, trace, authorize, or repair generated behavior. The definition includes specifications, schemas, tests, workflow contracts, harnesses, trace records, claim ledgers, and approval gates when they are maintained and coupled to control or evaluation. It excludes passive documentation and one-off prompts. The contribution is an eight-role taxonomy, a lifecycle model of `specify -> generate -> validate -> trace -> repair`, a systematization of recent AI-assisted software-engineering literature, and an illustrative artifact analysis of a file-backed workflow packet. The case is not evidence that one workflow improves outcomes. It shows how the framework separates source authority from evidence, traces, and approval records, giving code review a way to ask which upstream artifacts governed the code it is asked to judge.

## Keywords

AI-assisted software engineering; specification; code review; agent workflows; traceability; software process; governance.

## 1. Introduction

Review starts at the diff because the diff is visible. In AI-assisted software work, that habit is increasingly incomplete. A model may have generated the patch from an instruction file, a task contract, a test scaffold, a harness, a workflow policy, or a conversation that never becomes part of the repository. The implementation can look ordinary while the decision surface that governed it is missing, stale, or unreviewed.

Generated code still deserves ordinary engineering scrutiny. It can be wrong, insecure, slow, brittle, or inconsistent with local design. The problem is that the diff may not reveal the artifact that made the change reasonable or unreasonable in the first place. A reviewer can ask whether the code compiles and whether the tests pass, yet still be unable to inspect the maintained statement of intended behavior, the constraints the agent was expected to preserve, the validation surface that checked those constraints, or the repair path that should update the upstream artifact after failure.

This is a source-of-truth problem rather than a claim about syntax. The question is not whether natural language is code. The question is which artifacts have enough operational standing to govern AI-assisted software work. A design note, prompt, README, workflow file, or test suite can all influence a model. Only some of them deserve to be treated as source-of-truth surfaces.

I use `specification surface` for that narrower class: maintained artifacts that become part of the source-of-truth boundary because people or tools use them to constrain, validate, trace, authorize, or repair generated behavior. A surface may be written in prose, YAML, a schema language, tests, a workflow DSL, a trace format, or a review checklist. File format is secondary. The defining property is operational coupling.

The contribution is fourfold:

1. a definition of `specification surface` for AI-assisted software engineering;
2. an eight-role taxonomy covering source, runtime, validation, trace, evidence, context, repair, and authority surfaces;
3. a lifecycle model, `specify -> generate -> validate -> trace -> repair`, that explains why failures should update upstream surfaces rather than only downstream code;
4. a literature mapping and an illustrative artifact analysis showing how the framework classifies existing systems and one file-backed workflow packet.

This framing fits the AIware setting because foundation-model software development is changing not only implementation speed, but also the artifacts through which teams express, check, and repair intent. The paper does not argue for maximal formalism. It argues for knowing which artifacts are actually governing the work.

## 2. Background And Motivation

### 2.1 Specification authority in software work

Spec-driven development treats specifications as active development artifacts rather than background requirements prose. Piskala describes a spectrum from spec-first work, to spec-anchored work, to spec-as-source generation, with stronger specification discipline justified when it removes consequential ambiguity and can be maintained [@piskala2026specdriven]. That spectrum gives the present paper a software-engineering baseline. Specification surfaces are not limited to agent harnesses or prompt files; they continue a longer concern that software becomes hard to govern when intended behavior is not itself maintained.

The framework here is narrower than a general recommendation to formalize everything. A surface earns authority when it participates in control, validation, traceability, or repair. A highly formal artifact that nobody maintains can be weaker than a short acceptance contract that drives generation and tests.

### 2.2 Specification gaps in agentic generation

The issue becomes sharper when agents coordinate under partial knowledge. Sartori studies multi-agent class generation while reducing specification detail and introducing opposing representation biases [@sartori2026specgap]. The useful lesson is not that every task needs maximal detail. It is that underspecified shared intent can become an integration failure, and that restoring specification can be more useful than post-hoc conflict information in the studied setting.

That result anchors the review problem. When a generated implementation diverges, the missing object may sit upstream of the diff: the shared decision that agents needed but did not receive. A review process that only inspects output can miss the ungoverned decision surface that caused the output to look plausible and still be wrong.

### 2.3 Professional control around agents

Huang et al. report that experienced developers use coding agents through planning, supervision, validation, version control, and domain expertise [@huang2025professional]. That practice matters because it locates AI assistance inside professional control rather than outside it. The human task is not merely to accept or reject a model output. It is to preserve the artifacts that make design intent inspectable and failure repairable.

The phrase "vibe coding" is useful only as a warning label for the opposite pattern: treating intent as informal prompt material while generated code becomes the only serious artifact. The paper does not depend on that term. The technical point is that some artifacts need to carry authority, some only provide context, and some should be repaired when failure exposes missing intent.

## 3. Definition: Specification Surface

A specification surface is a maintained artifact that becomes part of the source-of-truth boundary for AI-assisted software work because people or tools use it to constrain, validate, trace, authorize, or repair generated behavior.

An artifact qualifies when at least one of the following is true:

- it constrains allowed behavior before execution;
- tooling parses, types, lints, interprets, compiles, or validates it;
- it drives generation, orchestration, decomposition, or tool access;
- it defines tests, checks, gates, policies, or completion criteria;
- it links outputs to governing intent or supporting evidence;
- it records execution state that can be inspected, replayed, or compared;
- failure turns the artifact itself into a repair target.

This definition excludes passive documentation. A README does not become a specification surface merely because an agent can read it. A prompt does not become source of truth because it came before generated code. A context file becomes a candidate surface only when it is maintained and connected to evaluation, enforcement, runtime interpretation, traceability, or review.

The boundary also protects four claims that often get blurred in AI-assisted software discussions. Natural language can participate in a governed surface, but natural language is not automatically code. Documentation can inform work, but documentation is not automatically authority. Generated code remains consequential because it is the artifact users and systems execute. More formal specification can help when it removes consequential ambiguity and can be checked, but formality is not a monotonic improvement in model behavior.

## 4. Taxonomy Of Specification Surfaces

Table 1 treats surface types as roles rather than mutually exclusive file formats. A single artifact can occupy several roles when it is both human-reviewable and machine-interpreted.

**Table 1. Specification-surface taxonomy**

| Surface type | Working definition | Operational force | Examples | Main risks |
| :--- | :--- | :--- | :--- | :--- |
| Source surfaces | Artifacts that state desired behavior, constraints, interfaces, or acceptance criteria before implementation. | Guide generation, constrain implementation, establish review target. | Product specs, API contracts, schemas, BDD scenarios, task contracts. | Drift, ambiguity, over-specification, false confidence when the spec is wrong. |
| Runtime surfaces | Artifacts interpreted by a runtime to orchestrate agent or workflow behavior. | Execute control flow, roles, state transitions, tool access, and decomposition. | Agent harnesses, workflow YAML, agent configs, DSLs, skill definitions. | Hidden runtime semantics, weak replayability, model-dependent interpretation. |
| Validation surfaces | Artifacts that check whether behavior conforms to stated intent. | Turn expectations into tests, validators, linters, or contract checks. | Test suites, generated checks, static validators, mutation tests. | Test gaming, incomplete coverage, validator drift. |
| Trace surfaces | Artifacts that retain execution evidence for audit, replay, debugging, or comparison. | Preserve what ran, which inputs were admitted, and which constraints applied. | Run logs, agent traces, checkpoint logs, replay records. | Treating logs as authority rather than evidence. |
| Evidence surfaces | Artifacts that link claims, outputs, or decisions to support and contradictions. | Make claims auditable and contradictions visible. | Claim ledgers, source maps, evidence tables, provenance notes. | Paper-thin support, citation laundering, stale evidence. |
| Context surfaces | Project guidance that becomes operational only when maintained and evaluated. | Shape generation or review when coupled to checks or process. | Repository instructions and coding guidelines. | Passive context mistaken for enforcement. |
| Repair surfaces | Artifacts that convert failure diagnosis into upstream revision. | Feed validation or trace failures back into specs, policies, tests, or prompts. | Repair tickets, revised specs, updated tests, policy patches. | Fixing only generated output while leaving controlling ambiguity intact. |
| Authority and gate surfaces | Artifacts that decide what may run, move, publish, or be promoted. | Govern lifecycle movement, permissions, promotion, or external mutation. | Gate contracts, approval records, release checklists, policy manifests. | Bypassed approvals; unclear authority order. |

The taxonomy is intentionally plural. Source authority may live in a schema, a workflow contract, a test-generated prompt, or a human approval record. No single surface should replace all others. Review needs to know which surfaces govern which decisions.

## 5. Lifecycle Model

Specification surfaces matter because they participate in a lifecycle rather than remaining static documents.

```text
specify -> generate -> validate -> trace -> repair
   ^                                      |
   |______________________________________|
```

In the first stage, a surface states intent, constraints, or authority. In the generation stage, an agent, tool, or workflow produces code or another downstream artifact. Validation checks conformance. Trace records what happened and which inputs or surfaces were admitted. Repair updates the governing surface when failures expose ambiguity, drift, stale assumptions, missing constraints, or weak evidence.

This loop separates governed specification surfaces from ordinary documents. A surface should be reviewable before execution, useful during execution, and repairable after failure.

Recent systems occupy different parts of this loop. Bootstrapping Coding Agents treats the specification as the stable artifact of record in a narrow agent-bootstrap setting [@monperrus2026bootstrapping]. Natural-Language Agent Harnesses and AgentSPEX make harness or workflow logic executable through runtimes with contracts, state, checkpointing, tracing, replay, or verification [@pan2026nlah; @wang2026agentspex]. ContextCov converts passive agent instruction files into executable constraints, illustrating the transition from context surface to validation surface [@sharma2026contextcov]. Test-Driven AI Agent Definition compiles behavioral specifications into tests and prompt artifacts [@rehan2026tdad]. FASTRIC treats prompt-protocol formality as a design parameter for verifiable interactions [@jin2025fastric]. Trace and repair work such as AgentPex, AgentFixer, and claim-level auditability shows why outcome-only review remains weak for long-running agent behavior [@barke2026willful; @mulian2026agentfixer; @rasheed2026fluent].

The lifecycle model also explains why generated code remains important. Generated code is the executable artifact that users and systems encounter. But when it fails, the repair target is often not only the code. It is also the governing surface that allowed the failure to happen.

## 6. Literature Mapping

Table 2 maps the core literature by surface role and lifecycle stage. The table is a systematization of artifact roles in recent AI-assisted software-engineering work, not a broad survey of the area.

**Table 2. Literature mapped to specification-surface roles**

| Source | Surface roles | Lifecycle stages | Use in this paper | Boundary |
| :--- | :--- | :--- | :--- | :--- |
| Spec-driven development [@piskala2026specdriven] | source, validation, repair | specify, generate, validate, repair | SE baseline for spec-first, spec-anchored, and spec-as-source modes. | Do not claim maximum specification is always best. |
| Specification gap [@sartori2026specgap] | source, validation, repair | specify, generate, validate, repair | Hinge evidence that underspecification can cause coordination failure. | Specific tasks and models; do not overgeneralize. |
| Professional control [@huang2025professional] | source, validation, repair, authority | specify, validate, repair | Practice baseline for expert supervision and validation. | Does not prove universal use of specification surfaces. |
| Bootstrap specs [@monperrus2026bootstrapping] | source, validation | specify, generate, validate | Narrow example of specification as record. | Does not make all implementation safely regenerable. |
| NL agent harnesses [@pan2026nlah] | runtime, source, trace | specify, generate, trace | Harness behavior as external executable artifact. | Runtime coupling matters. |
| AgentSPEX [@wang2026agentspex] | runtime, validation, trace, source | specify, generate, validate, trace | Typed workflow specification and execution language. | Not every team needs a DSL. |
| ContextCov [@sharma2026contextcov] | context, validation, repair | specify, validate, repair | Passive instructions transformed into executable guardrails. | Ordinary context files are not automatically governed. |
| Test-driven agent definition [@rehan2026tdad] | source, validation, repair | specify, generate, validate, repair | Behavioral specs compiled into tests and prompt artifacts. | Tests do not prove all behavior. |
| FASTRIC [@jin2025fastric] | source, validation, trace | specify, validate, trace | Prompt-protocol specification and procedural conformance. | Formality is not monotonic improvement. |
| AgentPex traces [@barke2026willful] | trace, validation | validate, trace | Procedural trace checking beyond outcome success. | Traces diagnose; they do not replace source authority. |
| AgentFixer [@mulian2026agentfixer] | validation, trace, repair | validate, trace, repair | Failure detection, root cause, and repair recommendations. | Automated repair does not replace human review. |
| Claim auditability [@rasheed2026fluent] | evidence, trace, validation, repair | trace, validate, repair | Claim-level auditability and contradiction transparency. | This case does not implement full provenance graphs. |

The mapping supports a bounded synthesis: source-of-truth authority can sit upstream of generated code, but only when artifacts are connected to control, validation, traceability, or repair.

## 7. Illustrative Artifact Analysis

### 7.1 Method

This section presents an illustrative artifact analysis, not a controlled empirical evaluation. The unit of analysis is a single specification-surface package in a file-backed editorial and software-workflow repository, together with the paper-development and essay-iteration workflow machinery around it.

The artifact corpus includes package status, package README, claim-boundary ledger, paper blueprint, publication route note, workflow contracts, gate contracts, policy manifests, retained run logs, external review synthesis, and human promotion approval records. Each artifact was coded against the surface roles in Table 1 and the lifecycle stages in Section 5. The coding protocol asked three questions:

1. Which decision does the artifact govern, if any?
2. Which tool, reviewer, or workflow step reads or validates it?
3. When a failure occurs, is the artifact evidence, authority, or a repair target?

The analysis reports observations only where the artifact role is visible from maintained files or retained run records. Interpretive claims are limited to what the taxonomy can classify: source authority, runtime interpretation, validation, trace, evidence, repair, context, or gate behavior. The case is useful because it separates roles that often collapse into a single conversational stream during AI-assisted work. It is also limited: it is a single local system, analyzed by the author, and does not prove general effectiveness.

### 7.2 Case summary

Observation 1: the package has a `status.yaml` manifest that resolves its kind, revision, live draft, evidence path, and lifecycle stage. Package state is therefore a maintained surface rather than an inference from prose.

Observation 2: root authority surfaces define which layer wins when artifacts disagree. Workflow contracts, policy YAMLs, gate contracts, pipeline profiles, and package status outrank logs and views. This keeps trace evidence from silently becoming source authority.

Observation 3: the experimental `paper_development` workflow admits package status, package README, the live draft or candidate, claim boundary ledger, evidence surface, and paper folder. Its allowed write path is the package-local `paper/` folder, keeping paper work separate from the public essay route.

Observation 4: the completed public-essay route supplies a repair and promotion example. External reviews identified non-blocking polish requirements and judged the candidate to clear the north-star bar, but the external review synthesis did not authorize live draft replacement. A separate human promotion approval surface authorized copying the polished candidate into the live draft.

These observations support a limited claim: the taxonomy can classify source authority, runtime contracts, evidence, trace, and approval as distinct surfaces in a real workflow. They do not support a claim that this repository's workflow improves quality, speed, safety, or adoption compared with another process.

### 7.3 Artifact classification

Table 3 uses role labels rather than full repository paths so the manuscript remains readable in narrow columns. The exact file names are retained in the local case-study trace and workflow packet.

**Table 3. Local artifact roles**

| Artifact | Surface type | Lifecycle stage | Operational force | Failure or repair implication |
| :--- | :--- | :--- | :--- | :--- |
| Authority map | authority, gate | specify | Defines source-of-truth order. | If logs act as source authority, repair the authority map or consuming workflow. |
| Package status manifest | authority, context | specify | Resolves package kind, revision, live draft, evidence path, and stage state. | Stage decisions should be repaired here, not inferred from prose alone. |
| Paper workflow contract | runtime, authority, validation | specify, validate, trace | Declares context dependencies, allowed paths, outputs, and checks. | Paper artifacts cannot silently mutate the essay route. |
| Essay workflow contract | runtime, validation, authority | specify, generate, validate, trace | Declares candidate, review, scorecard, decision, and gate outputs. | Promotion requires review and approval surfaces. |
| Gate contract manifest | authority, validation | validate, repair | Defines movement, quality, promotion, and external-mutation gates. | Missing approvals should block movement or mutation. |
| Claim boundary ledger | evidence, repair | specify, validate, repair | Names authorized, caveated, and forbidden claims. | Paper prose that drifts into forbidden claims repairs the blueprint or draft. |
| External review synthesis | evidence, repair | validate, repair | Aggregates review findings and required polish. | Review can repair a candidate without authorizing promotion. |
| Human promotion approval | authority, gate | validate, repair | Records explicit approval to promote the polished candidate. | Promotion is authorized through this surface, not through file existence. |
| Reviewable run logs | trace | trace | Retain operational evidence. | Logs diagnose what happened but are not source authority. |

### 7.4 Case lesson

The local case shows how a workflow can keep source authority, runtime interpretation, evidence, trace, and approval distinct. It does not show that this repository's process is generally better than alternatives. The value of the case is narrower: the taxonomy can classify a real file-backed workflow and identify which artifacts govern intent before, during, and after AI-assisted work.

## 8. Discussion

### 8.1 Code review moves upstream, but code remains consequential

Generated code does not stop mattering. It may simply be the second artifact reviewers should ask about. When generated output is downstream of maintained specification surfaces, reviewers need to inspect both the diff and the surface that governed the diff. A clean diff can still be wrong if the controlling surface is stale, ambiguous, or unauthorized.

### 8.2 Context files become surfaces only under control

Agent instruction files and repository context files deserve attention because they are machine-facing project artifacts. A context file becomes a governed specification surface only when it is maintained, evaluated, enforced, interpreted by a runtime, or tied to review. ContextCov is useful here because it turns passive instructions into executable guardrails [@sharma2026contextcov]. Presence in the context window is weaker than operational coupling.

### 8.3 Formality is a design parameter

The taxonomy should not be read as a call for maximal formalism. A more formal surface can help when it removes consequential ambiguity and can be checked. It can also add friction, encode the wrong behavior, or over-constrain work when the domain is still exploratory. FASTRIC is useful here because it treats prompt-protocol formality as a design variable rather than a moral victory [@jin2025fastric].

### 8.4 Failure modes

Specification surfaces can fail in familiar ways:

- they drift from implementation or practice;
- they become too broad to review;
- they encode stale authority;
- validators check the wrong thing;
- generated tests create false confidence;
- traces are mistaken for source truth;
- approval gates become ceremony rather than decision points.

These failures do not invalidate the concept. They explain why the surface must be maintained, validated, traced, and repaired.

## 9. Limitations And Threats To Validity

This is a framework and systematization paper with an illustrative artifact analysis. It is not a benchmark paper and does not measure general effectiveness.

The taxonomy is conceptual and should be tested against additional systems, teams, and workflow architectures. The case study is single-case, local, and author-coded. It demonstrates how the taxonomy can classify a file-backed workflow system; it does not prove that the workflow improves quality, speed, safety, or adoption.

The literature map is preprint-heavy and fast-moving. That is appropriate for a fast-feedback AI-assisted software-engineering venue, but it increases the risk that terminology, systems, and empirical results will change quickly.

The argument does not claim that natural language is code. Some specification surfaces may be written in ordinary language, but the defining property is operational coupling, not syntax. The paper also does not claim that all documentation becomes authoritative, that generated code is disposable, or that richer specification always improves model behavior.

## 10. Artifact Availability

This manuscript analyzes repository-local artifacts from the author's content workflow. The artifact packet consists of the paper roadmap, north-star rubric, draftability audit, approval gate, case-study trace, literature map, manuscript drafts, route checklists, and retained workflow records. The current fast-feedback submission does not include a separate public supplemental bundle. The case analysis is therefore presented as illustrative and author-audited rather than as an externally reusable dataset.

If the work moves to a peer-reviewed or arXiv-facing version, the next artifact step is a public or anonymized snapshot that lets reviewers inspect the classification method and workflow evidence directly. The packet is not presented as a benchmark dataset.

## 11. AI/Tool Use Disclosure

This manuscript was prepared with AI-assisted writing and repository-analysis tooling under a file-backed workflow. AI assistance was used to organize local evidence, draft and revise manuscript prose, and check workflow artifacts against the paper-development rubric. The author remains responsible for claims, citations, artifact selection, revision decisions, and external submission.

## 12. Conclusion

AI-assisted software work becomes easier to govern when intent can be read before execution, checked during execution, traced after execution, and repaired when failures expose missing decisions. Code review remains necessary, but it is incomplete when the upstream source of authority is informal. Specification surfaces name the artifacts that make intent reviewable: source surfaces, runtime surfaces, validation surfaces, trace surfaces, evidence surfaces, context surfaces, repair surfaces, and authority gates. The practical question for AI-assisted software engineering is not whether prompts are code. It is whether the artifacts that control generated work are maintained enough to be governed.

## References

::: {#refs}
:::
