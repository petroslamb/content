---
kind: paper_draft
package: "literate-workflow-programming/specification-surface-source-of-truth"
revision: 2
status: draft_for_submission_readiness_review
created: "2026-04-30"
workflow: paper_development
source_blueprint: "specification-surface-source-of-truth-paper-blueprint.md"
source_audit: "specification-surface-source-of-truth-draftability-audit-r1.md"
source_approval_gate: "specification-surface-source-of-truth-paper-draft-approval-gate-r1.md"
source_readiness_review: "specification-surface-source-of-truth-submission-readiness-review-r1.md"
target_route: aiware_fast_feedback_then_nier_or_workshop
external_submission_allowed: false
---

# Specification Surfaces as Source-of-Truth Artifacts in AI-Assisted Software Engineering

## Abstract

AI-assisted software workflows make generated code increasingly easy to produce and review, but they often leave the intent that governed generation outside maintained artifacts. This creates a review asymmetry: the downstream diff is visible, while the upstream source of authority may exist only in a prompt, chat transcript, stale document, or private design decision. This paper introduces `specification surfaces`: maintained artifacts that acquire operational force because they constrain, validate, trace, authorize, or repair AI-assisted software work through typing, linting, validation, trace links, runtime interpretation, generated tests, or review gates. The concept excludes passive documentation and one-off prompts unless they are connected to a control, evaluation, or maintenance loop. We propose a taxonomy of specification-surface types, a lifecycle model of `specify -> generate -> validate -> trace -> repair`, and a mapping of recent AI-assisted software-engineering literature into the model. We then present an illustrative artifact analysis of a file-backed workflow system whose package manifests, workflow contracts, gate definitions, validation commands, review packets, and run records separate source authority from evidence. The goal is a framework for reasoning about where source-of-truth authority lives in AI-assisted software work and how code review can inspect upstream intent without dismissing the continued importance of generated code.

## Keywords

AI-assisted software engineering; specification; code review; agent workflows; traceability; software process; governance.

## 1. Introduction

AI-assisted coding changes the economics of implementation. Agents can produce plausible diffs, tests, summaries, and repair attempts faster than teams can reconstruct why a change was supposed to be correct. Conventional code review still matters: generated code carries bugs, security exposure, performance costs, and maintenance obligations. But reviewing only the generated diff is incomplete when the governing intent remains informal.

The failure mode is not simply misplaced trust in a model. It is a source-of-truth problem. A reviewer may be able to see the code but not the maintained statement of intended behavior, the constraints the agent was expected to preserve, the validation surface that checked those constraints, or the repair loop that should update the governing artifact after failure. In this setting, the question is not whether natural language is code. The question is where reviewable authority lives.

This paper introduces `specification surfaces`: maintained artifacts that become part of the source-of-truth boundary for AI-assisted software work because humans or tools use them to constrain, validate, trace, authorize, or repair generated behavior. A specification surface may be a structured specification, schema, test suite, workflow contract, agent harness, policy file, trace, claim ledger, or context file. Syntax is not the defining property. Operational coupling is.

The distinction matters because AI-assisted workflows often blur prompts, documentation, generated code, tests, logs, and review comments into one conversational stream. That stream can be useful during work, but it is weak as a governance surface unless the controlling intent is maintained, checked, and repaired. We therefore need a vocabulary for artifacts that sit upstream of generated code and still have enough operational force to be inspected.

This paper makes four contributions:

1. It defines `specification surface` as a governed, operationally coupled artifact in AI-assisted software engineering.
2. It proposes a taxonomy of surface roles: source, runtime, validation, trace, evidence, context, repair, and authority/gate surfaces.
3. It proposes a lifecycle model in which failures flow back into the governing surface: `specify -> generate -> validate -> trace -> repair`.
4. It maps recent literature and a local file-backed workflow case into the taxonomy to show how the concept organizes existing work.

## 2. Background And Motivation

### 2.1 Specifications as software authority

Spec-driven development reframes specifications as stronger development artifacts rather than passive requirements documents. Piskala describes a spectrum from spec-first work, to spec-anchored work, to spec-as-source generation, with stronger specification discipline justified when it removes consequential ambiguity and can be maintained [@piskala2026specdriven]. This is an important baseline because the specification-surface argument is not limited to agent harnesses. It extends an older software-engineering concern: code becomes difficult to govern when the intended behavior is not itself a maintained object.

The specification-surface frame is narrower than a universal call for formal specification. It does not say that every team should move to spec-as-source development. It says that, when AI systems generate or modify software, the upstream artifact that governed generation may need to become reviewable in its own right.

### 2.2 Specification gaps in agentic code generation

The problem becomes sharper when code agents divide work under partial knowledge. Sartori studies coordination failure in multi-agent class generation by progressively stripping specification detail and introducing opposing internal representation biases [@sartori2026specgap]. The central lesson for this paper is not that every code task needs maximal specification. It is that underspecified shared intent can become an integration failure, and that restored specification can be more useful than post-hoc conflict information in the studied recovery setting.

That result gives the specification-surface frame a concrete software-engineering hinge: when agents must coordinate, the missing source of truth may be upstream of the diff. A code review that sees only the generated implementation may miss the ungoverned decision that caused the implementation to diverge.

### 2.3 Professional control rather than vibe delegation

Professional developers do not simply hand all software judgment to agents. Huang et al. report that experienced developers use agents through planning, supervision, validation, version control, and domain expertise [@huang2025professional]. That practice aligns with the claim here: the professional-control problem is not only whether a model can write code, but whether the surrounding workflow preserves human-readable and tool-checkable control surfaces.

This paper uses `vibe` as a failure label for treating intent as informal prompt material while generated code remains the only serious artifact. The response is not to make every document formal. It is to identify which artifacts must carry authority, which artifacts only provide context, and which artifacts must be repaired when failures expose missing intent.

## 3. Definition: Specification Surface

A specification surface is a maintained artifact that becomes part of the source-of-truth boundary for AI-assisted software work because humans or tools use it to constrain, validate, trace, authorize, or repair generated behavior.

An artifact can be treated as a specification surface when at least one of these conditions holds:

- It constrains allowed behavior before execution.
- It is parsed, typed, linted, interpreted, compiled, or validated by tooling.
- It drives generation or orchestration.
- It defines tests, checks, gates, policies, or completion criteria.
- It links outputs to governing intent or supporting evidence.
- It records traceable execution state that can be inspected or replayed.
- It becomes a repair target when a failure exposes ambiguity, drift, or missing intent.

This definition deliberately excludes passive documentation. A README does not become a specification surface merely because an agent can read it. A prompt does not become source of truth merely because it came before generated code. A context file becomes a candidate surface only when it is maintained and connected to evaluation, enforcement, runtime interpretation, traceability, or review.

The definition also rejects four tempting overclaims:

- It does not claim that natural language is code.
- It does not claim that all documentation becomes authoritative.
- It does not claim that generated code stops mattering.
- It does not claim that richer or more formal specification always improves model behavior.

The boundary is operational coupling, not file format.

## 4. Taxonomy Of Specification Surfaces

Table 1 treats surface types as roles rather than mutually exclusive file formats. A single artifact can occupy several roles if it is both human-reviewable and machine-interpreted.

**Table 1. Specification-surface taxonomy**

| Surface type | Working definition | Operational force | Examples | Main risks |
| :--- | :--- | :--- | :--- | :--- |
| Source surfaces | Artifacts that state desired behavior, constraints, interfaces, or acceptance criteria before implementation. | Guide generation, constrain implementation, establish review target. | Product specs, API contracts, schemas, BDD scenarios, task contracts. | Drift, ambiguity, over-specification, false confidence when the spec is wrong. |
| Runtime surfaces | Artifacts interpreted by a runtime to orchestrate agent or workflow behavior. | Execute control flow, roles, state transitions, tool access, and decomposition. | Agent harnesses, workflow YAML, agent configs, DSLs, skill definitions. | Hidden runtime semantics, weak replayability, model-dependent interpretation. |
| Validation surfaces | Artifacts that check whether behavior conforms to stated intent. | Turn expectations into tests, validators, linters, or contract checks. | Test suites, generated checks, static validators, mutation tests. | Test gaming, incomplete coverage, validator drift. |
| Trace surfaces | Artifacts that retain execution evidence for audit, replay, debugging, or comparison. | Preserve what ran, which inputs were admitted, and which constraints applied. | Run logs, agent traces, checkpoint logs, replay records. | Treating logs as authority rather than evidence. |
| Evidence surfaces | Artifacts that link claims, outputs, or decisions to support and contradictions. | Make claims auditable and contradictions visible. | Claim ledgers, source maps, evidence tables, provenance notes. | Paper-thin support, citation laundering, stale evidence. |
| Context surfaces | Project guidance that becomes operational only when maintained and evaluated. | Shape generation or review when coupled to checks or process. | AGENTS.md, repo instructions, coding guidelines, memory files. | Passive context treated as enforcement; bloat; conflicting instructions. |
| Repair surfaces | Artifacts that convert failure diagnosis into upstream revision. | Feed validation or trace failures back into specs, policies, tests, or prompts. | Repair tickets, revised specs, updated tests, policy patches. | Fixing only generated output while leaving controlling ambiguity intact. |
| Authority/gate surfaces | Artifacts that decide what may run, move, publish, or be promoted. | Govern lifecycle movement, permissions, promotion, or external mutation. | Gate contracts, approval records, release checklists, policy manifests. | Bypassed approvals; unclear source-of-truth order. |

The taxonomy is intentionally plural. Source authority may live in a schema, a workflow contract, a test-generated prompt, or a human approval record. The paper's claim is not that one surface should replace all others. It is that review needs to know which surfaces govern which decisions.

## 5. Lifecycle Model

Specification surfaces matter because they participate in a lifecycle rather than remaining static documents.

```text
specify -> generate -> validate -> trace -> repair
   ^                                      |
   |______________________________________|
```

In the first stage, a surface states intent, constraints, or authority. In the generation stage, an agent, tool, or workflow produces code or another downstream artifact. Validation checks conformance. Trace records what happened and which inputs or surfaces were admitted. Repair updates the governing surface when failures expose ambiguity, drift, stale assumptions, missing constraints, or weak evidence.

This loop separates governed specification surfaces from ordinary documents. The surface must be reviewable before execution, useful during execution, and repairable after failure.

Several recent systems occupy different parts of this loop. Bootstrapping Coding Agents treats the specification as the stable artifact of record in a narrow agent-bootstrap setting [@monperrus2026bootstrapping]. Natural-Language Agent Harnesses and AgentSPEX make harness or workflow logic executable through runtimes with contracts, state, checkpointing, tracing, replay, or verification [@pan2026nlah; @wang2026agentspex]. ContextCov converts passive agent instruction files into executable constraints, directly illustrating the transition from context surface to validation surface [@sharma2026contextcov]. Test-Driven AI Agent Definition compiles behavioral specifications into tests and prompt artifacts [@rehan2026tdad]. FASTRIC treats prompt-protocol formality as a design parameter for verifiable interactions [@jin2025fastric]. Trace and repair work such as AgentPex, AgentFixer, and claim-level auditability show why outcome-only review is too weak for long-running agent behavior [@barke2026willful; @mulian2026agentfixer; @rasheed2026fluent].

The lifecycle model also explains why generated code remains important. Generated code is the executable artifact that users and systems encounter. But when it fails, the repair target is often not only the code. It is also the governing surface that allowed the failure to happen.

## 6. Literature Mapping

Table 2 maps the core literature by surface role and lifecycle stage. This is not a broad survey. It is a systematization of which artifact roles appear in recent AI-assisted software-engineering work.

**Table 2. Literature mapped to specification-surface roles**

| Source | Surface roles | Lifecycle stages | Use in this paper | Boundary |
| :--- | :--- | :--- | :--- | :--- |
| Spec-Driven Development [@piskala2026specdriven] | source, validation, repair | specify, generate, validate, repair | General SE baseline for spec-first, spec-anchored, and spec-as-source modes. | Do not claim maximum specification is always best. |
| Specification Gap [@sartori2026specgap] | source, validation, repair | specify, generate, validate, repair | Hinge evidence that underspecification can cause coordination failure. | Specific tasks and models; do not overgeneralize. |
| Professional Developers Don't Vibe [@huang2025professional] | source, validation, repair, authority | specify, validate, repair | Practice baseline for professional control. | Does not prove universal use of specification surfaces. |
| Bootstrapping Coding Agents [@monperrus2026bootstrapping] | source, validation | specify, generate, validate | Narrow strong example of specification-as-record. | Does not make all implementation safely regenerable. |
| Natural-Language Agent Harnesses [@pan2026nlah] | runtime, source, trace | specify, generate, trace | Harness behavior as external executable artifact. | Runtime coupling matters. |
| AgentSPEX [@wang2026agentspex] | runtime, validation, trace, source | specify, generate, validate, trace | Typed workflow specification and execution language. | Not every team needs a DSL. |
| ContextCov [@sharma2026contextcov] | context, validation, repair | specify, validate, repair | Passive instructions transformed into executable guardrails. | Ordinary context files are not automatically governed. |
| Test-Driven AI Agent Definition [@rehan2026tdad] | source, validation, repair | specify, generate, validate, repair | Behavioral specs compiled into tests and prompt artifacts. | Tests do not prove all behavior. |
| FASTRIC [@jin2025fastric] | source, validation, trace | specify, validate, trace | Prompt-protocol specification and procedural conformance. | Formality is not monotonic improvement. |
| Willful Disobedience / AgentPex [@barke2026willful] | trace, validation | validate, trace | Procedural trace checking beyond outcome success. | Traces diagnose; they do not replace source authority. |
| AgentFixer [@mulian2026agentfixer] | validation, trace, repair | validate, trace, repair | Failure detection, root cause, and repair recommendations. | Automated repair does not replace human review. |
| From Fluent to Verifiable [@rasheed2026fluent] | evidence, trace, validation, repair | trace, validate, repair | Claim-level auditability and contradiction transparency. | This case does not implement full provenance graphs. |

The mapping supports a bounded synthesis: source-of-truth authority can move upstream into maintained specification surfaces, but only when artifacts are connected to control, validation, traceability, or repair.

## 7. Illustrative Artifact Analysis

### 7.1 Method

This section presents an illustrative artifact analysis, not a controlled empirical evaluation. The unit of analysis is the `specification-surface-source-of-truth` package in a file-backed editorial/software workflow repository and the surrounding `paper_development` and `essay_iteration` workflow machinery.

The artifact corpus includes package status, package README, claim-boundary ledger, paper blueprint, publication route note, workflow contracts, gate contracts, policy manifests, retained run logs, external review synthesis, and human promotion approval records. I coded each artifact against the surface roles in Table 1 and the lifecycle stages in Section 5. The coding protocol asked three questions for each artifact:

1. Which decision does the artifact govern, if any?
2. Which tool, reviewer, or workflow step reads or validates it?
3. When a failure occurs, is the artifact evidence, authority, or a repair target?

The analysis reports observations only where the artifact's role is visible from maintained files or retained run records. Interpretive claims are limited to what the taxonomy can classify: source authority, runtime interpretation, validation, trace, evidence, repair, context, or gate behavior. This case is useful because it separates roles that are often collapsed in AI-assisted work. It is also limited: it is a single local system, analyzed by the author, and does not prove general effectiveness.

### 7.2 Case summary

Observation 1: the package has a `status.yaml` manifest that resolves its kind, revision, live draft, evidence path, and lifecycle stage. This makes package state a maintained surface rather than an inference from prose.

Observation 2: root authority surfaces define which layer wins when artifacts disagree. Workflow contracts, policy YAMLs, gate contracts, pipeline profiles, and package status outrank logs and views. This keeps trace evidence from silently becoming source authority.

Observation 3: the experimental `paper_development` workflow admits package status, package README, the live draft or candidate, claim boundary ledger, evidence surface, and paper folder. Its allowed write path is the package-local `paper/` folder, keeping paper work separate from the public essay route.

Observation 4: the completed r3 essay route supplies a repair and promotion example. External reviews identified non-blocking polish requirements and judged the candidate to clear the north-star bar, but the external review synthesis did not authorize live draft replacement. A separate human promotion approval surface authorized copying the polished candidate into the live draft.

Interpretation: these observations support the limited claim that the taxonomy can classify source authority, runtime contracts, evidence, trace, and approval as distinct surfaces in a real workflow. They do not support a claim that this repository's workflow improves quality, speed, safety, or adoption compared with another process.

### 7.3 Artifact classification

**Table 3. Local artifact roles**

| Artifact | Surface type | Lifecycle stage | Operational force | Failure or repair implication |
| :--- | :--- | :--- | :--- | :--- |
| `AUTHORITY.md` | authority/gate | specify | Defines source-of-truth order. | If logs act as source authority, repair the authority map or consuming workflow. |
| `status.yaml` | authority/context | specify | Resolves package kind, revision, live draft, evidence path, and stage state. | Stage decisions should be repaired here, not inferred from prose alone. |
| `workflows/paper-development/workflow.yaml` | runtime/authority/validation | specify, validate, trace | Declares context dependencies, allowed paths, outputs, and checks. | Paper artifacts cannot silently mutate the essay route. |
| `workflows/essay-iteration/workflow.yaml` | runtime/validation/authority | specify, generate, validate, trace | Declares candidate, review, scorecard, decision, and gate outputs. | Promotion requires review and approval surfaces. |
| `gate_contracts.yaml` | authority/validation | validate, repair | Defines movement, quality, promotion, and external-mutation gates. | Missing approvals should block movement or mutation. |
| Claim boundary ledger | evidence/repair | specify, validate, repair | Names authorized, caveated, and forbidden claims. | Paper prose that drifts into forbidden claims repairs the blueprint or draft. |
| External review synthesis | evidence/repair | validate, repair | Aggregates review findings and required polish. | Review can repair a candidate without authorizing promotion. |
| Human promotion approval | authority/gate | validate, repair | Records explicit approval to promote the polished candidate. | Promotion is authorized through this surface, not through file existence. |
| Reviewable run logs | trace | trace | Retain operational evidence. | Logs diagnose what happened but are not source authority. |

### 7.4 Case lesson

The local case demonstrates how a workflow can keep source authority, runtime interpretation, evidence, trace, and approval distinct. The case does not show that this repository's process is generally better than alternatives. It shows how the specification-surface taxonomy can classify a real file-backed workflow and identify which artifacts govern intent before, during, and after AI-assisted work.

## 8. Discussion

### 8.1 Code review moves upstream, but code remains consequential

The central review implication is not that generated code stops mattering. It is that generated code may not be the first artifact reviewers should ask about. When generated output is downstream of maintained specification surfaces, reviewers need to inspect both the diff and the surface that governed the diff. A clean diff can still be wrong if the controlling surface is stale, ambiguous, or unauthorized.

### 8.2 Context files become surfaces only under control

Agent instruction files and repository context files are important because they are increasingly machine-facing. But a context file is not automatically a governed specification surface. It becomes one when it is maintained, evaluated, enforced, interpreted by a runtime, or tied to review. ContextCov is a useful example because it turns passive instructions into executable guardrails [@sharma2026contextcov]. The broader lesson is that presence in the context window is weaker than operational coupling.

### 8.3 Formality is a design parameter

The taxonomy should not be read as a call for maximal formalism. A more formal surface can help when it removes consequential ambiguity and can be checked. It can also add friction, encode the wrong behavior, or over-constrain work when the domain is still exploratory. FASTRIC is useful here because it treats prompt-protocol formality as a variable design choice rather than a moral victory [@jin2025fastric].

### 8.4 Failure modes

Specification surfaces can fail in familiar ways:

- they drift from implementation or practice;
- they become too broad to review;
- they encode stale authority;
- validators check the wrong thing;
- generated tests create false confidence;
- traces are mistaken for source truth;
- approval gates become ceremony rather than decision points.

These failures do not invalidate the concept. They show why the surface must be maintained, validated, traced, and repaired.

## 9. Limitations And Threats To Validity

This paper is a framework and systematization paper with an illustrative artifact analysis. It is not a benchmark paper and does not measure general effectiveness.

The taxonomy is conceptual and should be tested against additional systems, teams, and workflow architectures. The case study is single-case, local, and author-coded. It demonstrates how the taxonomy can classify a file-backed workflow system; it does not prove that the workflow improves quality, speed, safety, or adoption.

The literature map is preprint-heavy and fast-moving. That is appropriate for a fast-feedback AI-assisted software-engineering venue, but it increases the risk that terminology, systems, and empirical results will change quickly.

The paper does not claim that natural language is code. Some specification surfaces may be written in ordinary language, but the defining property is operational coupling, not syntax. The paper also does not claim that all documentation becomes authoritative, that generated code is disposable, or that richer specification always improves model behavior.

## 10. Artifact Availability

This manuscript analyzes repository-local artifacts from the author's content workflow. The reviewable artifact packet consists of the paper roadmap, north-star rubric, draftability audit, approval gate, case-study trace, literature map, manuscript drafts, route checklists, and retained workflow records. A non-anonymous fast-feedback submission can cite these artifacts directly if the repository snapshot is made available. A double-anonymous submission should instead use an anonymized artifact appendix and remove repository-identifying paths according to venue policy.

The artifact packet is intended to support inspection of the classification method and workflow evidence. It is not presented as a benchmark dataset.

## 11. AI/Tool Use Disclosure

This manuscript was prepared with AI-assisted writing and repository-analysis tooling under a file-backed workflow. AI assistance was used to organize local evidence, draft and revise manuscript prose, and check workflow artifacts against the paper-development rubric. The author remains responsible for claims, citations, artifact selection, revision decisions, and any external submission.

## 12. Conclusion

AI-assisted software work becomes governable when intent can be read before execution, checked during execution, traced after execution, and repaired when failures expose missing decisions. Code review remains necessary, but it is incomplete when the upstream source of authority is informal. Specification surfaces name the artifacts that make intent reviewable: source surfaces, runtime surfaces, validation surfaces, trace surfaces, evidence surfaces, context surfaces, repair surfaces, and authority gates. The practical question for AI-assisted software engineering is therefore not whether prompts are code. It is whether the artifacts that control generated work are maintained enough to be governed.

## References

References are tracked in [`references.bib`](references.bib). Citation keys used in this draft:

- `piskala2026specdriven`
- `sartori2026specgap`
- `huang2025professional`
- `monperrus2026bootstrapping`
- `pan2026nlah`
- `wang2026agentspex`
- `sharma2026contextcov`
- `rehan2026tdad`
- `jin2025fastric`
- `barke2026willful`
- `mulian2026agentfixer`
- `rasheed2026fluent`
