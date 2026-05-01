---
kind: literature_mapping
package: "literate-workflow-programming/specification-surface-source-of-truth"
revision: 1
status: appendix_ready_draft
created: "2026-04-30"
workflow: paper_development
source_blueprint: "specification-surface-source-of-truth-paper-blueprint.md"
evidence_surface: "../../papers/index.md"
---

# Literature Mapping R1

## Purpose

This mapping promotes the blueprint evidence table into an appendix-ready source map for the paper. It is a systematization scaffold, not a broad literature review. Each source is included because it demonstrates one or more roles in the `specification surface` taxonomy.

## Coding Scheme

Surface roles:

- `source`: states behavior, constraints, interfaces, or acceptance criteria.
- `runtime`: interpreted by a runtime to orchestrate work.
- `validation`: checks conformance to intent.
- `trace`: retains execution evidence or supports replay/audit.
- `evidence`: links claims, outputs, or decisions to support.
- `context`: supplies project or task context when maintained and evaluated.
- `repair`: turns failure diagnosis into a change to upstream surfaces.
- `authority`: governs promotion, lifecycle movement, permissions, or source-of-truth order.

Lifecycle stages:

- `specify`
- `generate`
- `validate`
- `trace`
- `repair`

Claim strength:

- `anchor`: necessary for the main argument.
- `support`: strengthens a taxonomy row or lifecycle stage.
- `caveat`: constrains overclaiming.
- `optional`: useful only if a section expands.

## Core Source Map

| ID | Title | Surface Roles | Lifecycle Stages | Claim Strength | Paper Use | Boundary |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `2602.00180` | Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants | source, validation, repair | specify, generate, validate, repair | anchor | Establishes SE grounding for spec-first, spec-anchored, and spec-as-source modes. Use to show that specification authority is not only an agent-harness niche. | Do not claim all projects should become spec-as-source. Use the minimum-rigor principle. |
| `2603.24284` | The Specification Gap: Coordination Failure Under Partial Knowledge in Code Agents | source, validation, repair | specify, generate, validate, repair | anchor | Main empirical hinge: underspecification can create multi-agent integration failure, and restored specification can dominate post-hoc conflict reports in the studied recovery setup. | Do not generalize effect sizes beyond Python class-generation tasks and the studied models/design. |
| `2512.14012` | Professional Software Developers Don't Vibe, They Control | source, validation, repair, authority | specify, validate, repair | anchor | Grounds the anti-vibe frame in professional practice: planning, supervision, validation, version control, and expertise. | Do not claim all experienced developers already use governed specification surfaces. |
| `2603.17399` | Bootstrapping Coding Agents: The Specification Is the Program | source, validation | specify, generate, validate | support | Strongest example of specification-as-source in a narrow coding-agent bootstrap experiment. | Do not claim generated code stops mattering or that all systems are safely regenerable. |
| `2603.25723` | Natural-Language Agent Harnesses | runtime, source, trace | specify, generate, trace | support | Shows harness logic externalized into an executable artifact with explicit contracts and durable artifacts. | Runtime coupling matters; do not reduce the claim to natural language by itself. |
| `2604.13346` | AgentSPEX: An Agent Specification and Execution Language | runtime, validation, trace, source | specify, generate, validate, trace | support | Strong anchor for typed workflow surfaces: explicit control flow, state, checkpointing, tracing, replay, and verification. | Do not imply every team needs a DSL. |
| `2603.00822` | ContextCov: Deriving and Enforcing Executable Constraints from Agent Instruction Files | context, validation, repair | specify, validate, repair | anchor for context caveat | Demonstrates the transition from passive instructions to executable guardrails. | Do not treat ordinary AGENTS.md files as automatically governed surfaces. |
| `2603.08806` | Test-Driven AI Agent Definition | source, validation, repair | specify, generate, validate, repair | support | Shows behavioral specs compiled into tests and prompt artifacts with hidden-test and mutation safeguards. | Preserve anti-gaming caveats and avoid claiming tests prove full behavior. |
| `2512.18940` | FASTRIC: Prompt Specification Language for Verifiable LLM Interactions | source, validation, trace | specify, validate, trace | caveat/support | Supports protocol-level specification and procedural conformance; useful for the formality-as-design-parameter caveat. | Do not claim more formal specification always improves behavior. |
| `2603.23806` | Willful Disobedience / AgentPex | trace, validation | validate, trace | support | Shows trace evaluation against behavioral rules and why outcome-only scoring misses procedural failures. | Keep traces diagnostic; do not make them source authority. |
| `2603.29848` | AgentFixer | validation, trace, repair | validate, trace, repair | support | Anchors repair lifecycle: validation, root-cause analysis, and improvement recommendations. | Do not claim automated repair replaces human review. |
| `2602.13855` | From Fluent to Verifiable | evidence, trace, validation, repair | trace, validate, repair | support | Supports evidence surfaces and claim-level auditability. | Do not claim this repo implements full semantic provenance graphs. |

## Local Case Map

| Local Source | Surface Roles | Lifecycle Stages | Paper Use | Boundary |
| :--- | :--- | :--- | :--- | :--- |
| `AUTHORITY.md` | authority | specify, repair | Defines source-of-truth order: workflow/status/policy surfaces outrank logs and views. | Do not treat this as a universal authority model. |
| `status.yaml` | authority, context | specify | Resolves package kind, revision, live draft, evidence path, and current stage. | Do not infer stage from prose when status exists. |
| `workflows/paper-development/workflow.yaml` | runtime, authority, validation | specify, validate, trace | Demonstrates local paper-route isolation and allowed write paths. | Experimental module, not a canonical stage. |
| `workflows/essay-iteration/workflow.yaml` | runtime, validation, authority | specify, generate, validate, trace | Demonstrates packet/candidate/review/gate structure used before paper route began. | Essay route is separate from paper route. |
| `gate_contracts.yaml` | authority, validation | validate, repair | Defines gates and required artifacts. | Gate definitions do not themselves approve a decision. |
| `reviewable-runs/logs/` | trace | trace | Provides retained operational evidence. | Logs are evidence, not source authority. |
| `specification-surface-source-of-truth-claim-boundary-ledger.md` | evidence, repair | specify, validate, repair | Carries allowed, caveated, and forbidden claims into the paper route. | Claim permission is scoped to the successor object and local evidence. |
| `iterations/r3/*external-review-synthesis*` | evidence, repair | validate, repair | Records independent review findings and required polish. | Review synthesis did not itself authorize promotion. |
| `iterations/r3/*human-promotion-approval*` | authority, gate | validate, repair | Records explicit promotion approval. | Human approval is route-specific, not a general paper-submission approval. |

## Section Placement

| Paper Section | Required Sources | Optional Sources | Notes |
| :--- | :--- | :--- | :--- |
| Introduction | `2602.00180`, `2603.24284`, `2512.14012` | local case | Introduce the review asymmetry and source-of-truth problem. |
| Background | `2602.00180`, `2512.14012` | `2603.17399` | Keep the SE/practice frame primary. |
| Definition | claim boundary ledger, `2603.00822`, `2604.13346` | `2603.25723`, `2512.18940` | Define operational coupling as the decisive property. |
| Taxonomy | all core sources | local case | Use sources to populate rows, not as a survey narrative. |
| Lifecycle Model | `2603.08806`, `2603.23806`, `2603.29848`, `2602.13855` | `2604.13346` | Show validation, trace, and repair as a feedback loop. |
| Case Study | local authority/workflow/status/gate/log artifacts | `2603.16021` if filesystem/context architecture expands | Keep as illustrative artifact analysis. |
| Discussion | `2603.24284`, `2512.14012`, `2512.18940`, `2603.00822` | context-file queue papers | Discuss failures, context-file caveats, and non-monotonic formality. |
| Limitations | all caveat sources | route note | Name preprint-heavy evidence and single-case limits. |

## Optional Expansion Sources

These are useful if the paper grows beyond the MVP, but not required for the first extended abstract.

| ID | Title | Potential Use | Trigger |
| :--- | :--- | :--- | :--- |
| `2603.16021` | Interpretable Context Methodology | Filesystem structure and markdown stage contracts as agentic architecture. | Use if the case-study section expands into folder/workspace architecture. |
| `2510.04173` | Open Agent Specification | Portability and standardization of agent definitions. | Use if taxonomy adds standardization/portability row. |
| `2512.19769` | Declarative Language for LLM Agent Workflows | Workflow DSLs and runtime portability. | Use if runtime surfaces need more breadth beyond AgentSPEX/NLAH. |
| `2603.20380` | ALARA for Agents | Least-privilege context and tool scoping. | Use if authority/gate surfaces expand into security/control. |
| `2504.11703` | Progent | Programmable privilege control. | Use if the paper foregrounds permission/control policy. |
| `2604.03088` | SkVM | Skills as code and runtime portability. | Use if skill files become a main example. |
| `2601.04748` | When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail | Skill routing and semantic overload limits. | Use if the paper discusses skills/context surface failure. |

## Known Caveat Sources Not Yet Locally Central

These sources are indexed in the package queue and should be intaken or directly inspected before heavy use:

| ID | Title | Caveat Role |
| :--- | :--- | :--- |
| `2602.11988` | Evaluating AGENTS.md | Prevents booster claims about repository context files. |
| `2601.20404` | Impact of AGENTS.md Files | Balances negative context-file claims with task-specific benefits. |
| `2511.12884` | Agent READMEs | Supports context files as evolving machine-facing configuration artifacts, with caveats. |
| `2508.06942` | CNL-P | Could support controlled-language and linting claims. |
| `2603.15691` | VibeContract | Could support task contracts and QA in vibe-coding contexts. |
| `2512.14805` | Sharing State Between Prompts and Programs | Could support prompt/program state interfaces. |

## Claim Boundary Table

| Paper Claim | Licensed By | Required Caveat |
| :--- | :--- | :--- |
| Specification surfaces are governed artifacts, not passive prose. | Claim ledger, `2603.00822`, `2604.13346`, `2603.25723` | Operational coupling is required. |
| Code review needs upstream intent review. | r3 essay, `2602.00180`, `2603.24284`, `2512.14012` | Generated code still matters. |
| Underspecification can cause coordination failure. | `2603.24284` | Evidence is from a specific multi-agent code-generation setup. |
| Professional agent use favors control, planning, and validation. | `2512.14012` | Observational/survey evidence, not universal practice. |
| Context files can become specification surfaces. | `2603.00822`, optional context-file papers | Only when maintained, evaluated, enforced, or otherwise coupled to control. |
| Trace and audit surfaces support validation and repair. | `2603.23806`, `2603.29848`, `2602.13855` | Traces diagnose and audit; they do not replace the governing specification. |
| Stronger formality is not automatically better. | `2512.18940`, claim ledger | Formality is a design parameter whose value depends on model, task, and enforcement. |

## Readiness For Extended Abstract

Status: ready.

The map is sufficient for a 2-3 page extended abstract and an AIware go/no-go draft. It is not yet enough for a full research-track submission unless the case-study protocol is strengthened or additional systems are coded.
