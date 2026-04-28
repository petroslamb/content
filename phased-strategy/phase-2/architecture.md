# Phase 2 Architecture

## Goal

Phase 2 adds a local governed harness/runtime on top of the repo contract.

The runtime should:

- execute workflow contracts
- admit context as an explicit dependency
- validate and constrain runtime behavior
- write source-linked run records
- stop cleanly at file-backed review gates
- expose package state, gates, and recent runs in a thin local cockpit

It should do that without replacing filesystem-backed repo surfaces as the source of truth.

## Authority Position

Phase 2 planning now uses this authority chain:

1. [`idea-bank.md`](idea-bank.md) is the raw research inventory.
2. [`phase-2-distilled-findings.md`](phase-2-distilled-findings.md) is the compact decision-relevant distillation.
3. [`claim-ledger.md`](claim-ledger.md) and [`contradiction-register.md`](contradiction-register.md) decide what can be promoted and what authority rule constrains it.
4. This file, [`milestones.md`](milestones.md), [`workflow-yaml-schema.md`](workflow-yaml-schema.md), and the `2.1` / `2.2` / `2.3` specs are the operative plan.
5. [`open-questions.md`](open-questions.md) holds unresolved questions that can block, narrow, or defer promotion.

## Core Decisions

These decisions are closed for Phase 2 planning:

- Phase 2 is a governed harness/runtime layer around a thin model loop.
- `workflow.yaml` is the highest functional truth layer for workflow behavior.
- `workflow.yaml` is authored directly beside each workflow README.
- `workflow.yaml` carries workflow identity, version, stability, kind, and group metadata.
- the workflow README remains the human explanation surface.
- drift between README and YAML is controlled by checks, not by making prose the machine truth.
- `workflow.yaml` should carry a small behavioral envelope: preconditions, invariants, budgets, and recovery semantics.
- required context is admitted as a governed dependency, not loaded as passive prompt material.
- validation is a layered stack, not a trailing test pass.
- review gates are durable file-backed runtime objects.
- external mutation approval is distinct from content quality approval.
- `content-agent` is the single deterministic Phase 2 CLI/runtime entrypoint, implemented first as a local script or package.
- `content-agent` is thin first and consumes tracked contracts, package state, validation hooks, trace requirements, and gate artifacts.
- `content-agent` is not an LLM persona and does not require separate model credentials in the first architecture.
- Phase 2 should support both human-led exploratory work and governed continuous runs.
- governed, gated, resumable, or audit-required runs persist a durable `resolved_run`; exploratory previews may remain transient.
- promoted outputs are recorded first in run records and review gate artifacts, not in a standalone manifest.
- experimental workflows can run on demand, but they should not silently replace canonical lifecycle paths.
- workflow discovery starts with thin hand-authored, skill-like wrappers that point back to canonical workflow contracts.
- the cockpit is a thin reader/approver over filesystem-backed truth, not a second system of record.
- umbrella and leaf package semantics are consumed from current `status.yaml` manifests rather than redesigned inside Phase 2.

## Source Of Truth

Phase 2 keeps source authority and execution evidence file-backed:

- `workflow.yaml` for the highest functional workflow behavior contract
- workflow READMEs for human guidance
- `harness_policy.yaml` for repo-level autonomy and approval boundaries
- `pipeline_profiles.yaml` for cross-workflow route templates
- `gate_contracts.yaml` for reusable gate definitions
- `status.yaml` for package lifecycle state
- package files for content and artifacts
- `reviewable-runs/resolved-runs/` for durable resolved runs when resume, gates, or audit require them
- `reviewable-runs/logs/` for run records
- `reviewable-runs/gates/` for pending and resolved review gates

For workflow behavior, the highest editable truth layer is the tracked source contract set: per-workflow `workflow.yaml`, workflow README, root `harness_policy.yaml`, `gate_contracts.yaml`, `pipeline_profiles.yaml`, and package `status.yaml`. Generated or runtime surfaces must adapt to those files, not the other way around.

Within that set, authority is not flat: `workflow.yaml` owns machine behavior, the workflow README owns human explanation, `status.yaml` owns package lifecycle state, and root YAMLs own shared policy, gate, and routing constraints.

For package manifests specifically:

- `kind: leaf` means the package itself owns lifecycle progression.
- `kind: umbrella` means the runtime must resolve either an active leaf or an `umbrella_route` before assuming a normal stage path.
- settled umbrella roots may have no active lifecycle stage.

Phase 2 reads those distinctions from tracked manifests rather than inferring them from README prose or rebuilding them in a hidden index.

Local indexes or caches are allowed only when they are rebuildable from file-backed truth.

YAML is the default persisted structured format for Phase 2 contracts and runtime artifacts. JSON may be used only for rebuildable caches, API responses, or external tool interoperability.

## Root YAML Surfaces

The repo already has root-level YAML surfaces that Phase 2 should consume rather than ignore.

| File | Phase 2 Role | Authority Rule |
| :--- | :--- | :--- |
| `harness_policy.yaml` | Global local-first autonomy, write, approval, and external-mutation policy. | Acts as a policy floor. Per-workflow contracts may narrow it but should not silently override it. |
| `gate_contracts.yaml` | Catalog of reusable gate types, required artifacts, recommended validators, and proof modes. | Defines gate classes. Individual gate artifacts instantiate these contracts under `reviewable-runs/gates/`. |
| `pipeline_profiles.yaml` | Cross-workflow route templates: ordered workflows, required gates, allowed entry workflows, and fallback routes. | Helps `content-agent` choose the next workflow from package state. It does not replace per-workflow `workflow.yaml`. |
| `harness_contract.yaml` | Generated aggregate compatibility/index surface for the current harness and scripts. | Should be derived from primary sources. It should not compete with `workflow.yaml` as the authored workflow contract. |

Phase 2 should migrate authored workflow authority from workflow README frontmatter into per-workflow `workflow.yaml` files. During the transition, `harness_contract.yaml` may remain as a tracked generated roll-up for existing checks and scripts, but new implementation decisions should read the primary surfaces directly when possible.

## Execution State Placement

Package directories hold package lifecycle and content artifacts.

`reviewable-runs/` holds generated execution state:

- `reviewable-runs/resolved-runs/` for durable resolved runs when resume, gates, governed continuity, or audit require them
- `reviewable-runs/logs/` for source-linked run records
- `reviewable-runs/gates/` for pending and resolved YAML-backed review gates

Phase 2 runtime artifacts should point back to package-local drafts, previews, source files, and evidence rather than moving those content artifacts into `reviewable-runs/`.

Generated execution-state artifacts are maintained by `content-agent`. Humans inspect them and make decisions through the CLI or cockpit rather than hand-authoring run records, resolved runs, or gate files.

Exploratory workflow previews may stay transient. Once a run becomes governed, gated, resumable, or audit-relevant, the runtime should persist enough resolved state to continue from files.

Promoted-output state lives first in run records and review gate artifacts. Phase 2 should not add a standalone promoted-output manifest until repeated promoted outputs need independent tracking across runs or gates.

## Authority Surfaces

Phase 2 should keep these surfaces distinct:

| Surface | Role | Authority Rule |
| :--- | :--- | :--- |
| Workflow README | Human explanation and operator orientation. | Never carries machine permissions, gates, or allowed paths alone. |
| `workflow.yaml` | Machine contract for execution planning. | Wins for runtime authority. |
| Runtime adapter/control plane | Resolves package state, admits context, mediates tools, runs checks, writes records, and stops at gates. | Executes declared contracts; it does not invent workflow semantics. |
| Resolved run | Runtime view of one workflow contract applied to one package/run request. | Durable only when needed for governed continuity, gates, resume, or audit. |
| Run record | Source-linked account of what happened. | Derivative debugging and audit support, not source of truth. |
| Review gate | Durable stop/resume object. | Explains why execution stopped and how it can resume. |
| Approval decision | Human decision over a gate. | Can approve, reject, or defer; external mutation approval must be explicit. |
| Promoted-output state | Minimal contradiction/provenance state for trust-sensitive outputs. | Recorded in run records and gates first; full semantic graphs stay out of scope. |
| Discovery wrapper | Skill-like routing hint for Codex/operator discovery. | Points back to `workflow.yaml`; does not own process rules. |
| Cockpit | Local reader/approver over files. | May index for convenience, but filesystem truth remains authoritative. |

## Authority Planes

The Phase 2 "layers" are authority planes, not implementation tiers. They explain which surface wins when downstream artifacts disagree.

| Plane | Owns | Rule |
| :--- | :--- | :--- |
| Planning authority | Distilled findings, claim ledger, contradiction register, open questions. | Decides what architecture may promote. |
| Source authority | Per-workflow `workflow.yaml`, workflow README, root policy/profile/gate YAMLs, package `status.yaml`. | Highest editable truth for workflow behavior and package routing. |
| Package authority | Package content files, artifacts, drafts, previews, and lifecycle manifests. | Owns publication state and evidence. |
| Execution evidence | Resolved runs, run records, review gates, traces, validation results. | Derivative proof and resumability; does not redefine source contracts. |
| Views | Local cockpit, indexes, discovery wrappers, generated compatibility docs. | Convenience only; rebuildable or traceable to source authority. |

Phase 2 consumes these planes. It should not re-encode package taxonomy, workflow prose, or skill guidance into a second hidden system.

## Platform Objects

The platform should treat these as first-class objects:

- `package`
- `workflow_contract`
- `context_admission`
- `run_request`
- `resolved_run`
- `run_record`
- `review_gate`
- `approval_decision`
- `promoted_output_state`

Object boundaries:

- `workflow_contract` is the loaded runtime view of `workflow.yaml`, not a second authored contract file.
- `resolved_run` is the runtime's resolved view of one run, persisted as YAML only when governed continuity, gates, resume, or audit require it.
- `run_record` records execution against a contract, normally persisted as YAML or Markdown with YAML frontmatter, not authority.
- `review_gate` records why execution stopped and how it can resume, normally persisted as YAML.
- `promoted_output_state` supports promotion decisions, recorded first inside run records and review gates; it is not a full provenance graph.

Each object should map back to a tracked or rebuildable file-backed artifact.

## Execution Host Boundary

`content-agent` is a deterministic local CLI/runtime facade, not the sole thinking entity, not a Codex persona, and not a separate LLM-backed agent.

Initial Phase 2 execution is Codex-session-hosted. Codex, or another active operator harness, performs model-mediated work while `content-agent` supplies the local contract/runtime boundary.

`content-agent` should not require separate model credentials until a later executor adapter is explicitly promoted.

It may be invoked by:

- a human operator using the CLI
- a cockpit action
- an existing agent harness such as Codex
- a local script or automation

Model-backed work beyond the active Codex/operator harness should sit behind an executor adapter selected by the workflow contract and runtime configuration.

This keeps three things separate:

- `content-agent` owns contract resolution, context admission, validation, traces, gates, and resumability.
- the current operator or agent harness can perform model-mediated work under those constraints.
- a future model-provider adapter can run selected steps non-interactively if Phase 2 later proves that need.

Subagent-hosted execution is a compatible later executor mode, not the Phase 2 baseline. In that mode, an isolated Codex subagent may invoke the `content-agent` CLI and perform model-mediated workflow steps with bounded context. The subagent does not replace `content-agent` as the authority: contract resolution, validation, run records, gates, and lifecycle movement still come from file-backed state plus `content-agent` transitions.

## Content-Agent Command Surface

The v1 CLI vocabulary should be small and stable:

- `content-agent init`: initialize or check workflow/package runtime setup without advancing lifecycle state
- `content-agent status`: show package state, selected route, active gates, recent runs, and validation health
- `content-agent next`: resolve the next eligible workflow or action from package state, profiles, gates, and policy
- `content-agent run`: start a governed or exploratory run from a workflow contract and package target
- `content-agent resume`: continue from a durable `resolved_run` or review gate after validation
- `content-agent review`: list, inspect, approve, reject, or defer file-backed review gates
- `content-agent validate`: run static, contract, context, path/tool, gate, and trace checks without promotion

These names are the v1 user-facing contract. Flags and subcommands can evolve, but new implementation should avoid replacing this vocabulary with older `stage:*` or `workflow:*` command families.

## Run Modes

Phase 2 needs two explicit run modes.

### Exploratory Mode

Use when the human is working with Codex to inspect, improve, create, or test workflows.

Behavior:

- `content-agent` may initialize or validate a workflow run, but it does not claim continuous control.
- hooks should warn or annotate rather than block unrelated human-directed actions by default.
- experimental workflow edits may happen without being treated as completed platform execution.
- promotion, publication, lifecycle movement, and gate resolution still require explicit `content-agent` validation.

### Governed Continuous Mode

Use when the operator wants the session to keep progressing until a review gate, terminal failure, budget limit, or workflow completion.

Behavior:

- `content-agent` creates or loads a durable `resolved_run` whenever the run must survive response boundaries, gates, resume, or audit.
- scriptable steps run directly.
- Codex-session-hosted model work follows the active `resolved_run` and returns control to `content-agent` for validation and continuation.
- the run should not stop merely because the agent reached an ordinary response boundary.
- hooks may nudge or auto-resume safe validation-only checkpoints when expected outputs exist.
- hooks should block only actions that would falsely advance, publish, approve, or mutate lifecycle state outside the governed path.
- external mutation and human review gates always stop for explicit approval.
- later executor modes may host the governed run inside an isolated Codex subagent, but only with `content-agent` and YAML state remaining authoritative.

Governed continuous mode is stronger than advisory handoff, but it is still not total sandboxing. Work outside the governed path may happen, but it does not count as valid platform progress until `content-agent` validates and records it.

Continuous unattended operation is handled by `content-agent` plus durable YAML state and file-backed gates. Codex hooks may support warnings, nudges, or false-advancement checks, but hooks are not the primary mechanism for forcing arbitrary session behavior.

## Workflow Evolution

Workflows need explicit evolution metadata.

Each `workflow.yaml` should declare:

- `workflow_id`: stable identity used by package state, profiles, run records, and gates
- `version`: contract version recorded in `resolved_run` and `run_record`
- `stability`: `canonical` or `experimental`
- `workflow_kind`: `stage`, `module`, or `overlay`
- `workflow_group`: discovery and organization metadata, not execution authority by itself

Canonical workflow updates should be tested in exploratory mode or proof runs before changing default routing. Experimental workflows may exist in the repo, but they should enter execution only through an explicit operator request, a package route/status decision, or a pipeline profile.

Git branches are useful for developing and testing workflow changes, but runtime selection should not depend on branch names. The runtime authority is the tracked `workflow.yaml`, package state, and `pipeline_profiles.yaml`.

## Workflow And Skill Boundary

Workflows and skills are different layers:

- workflows define process authority: context, allowed surfaces, steps, gates, validation, and completion
- skills provide execution guidance, references, helper scripts, or capability-specific instructions

A skill should not decide lifecycle routing, approval gates, package state, or promotion. A workflow may bind a skill as an allowed capability, but the workflow contract remains the authority.

For Codex discovery, Phase 2 starts with short, hand-authored workflow discovery wrappers that behave like skills. These wrappers should:

- use a concise skill-style description for when to enter the workflow
- point to the canonical `workflow.yaml` and workflow README
- name related execution skills
- avoid repeating process rules that belong in the workflow contract

Do not generate discovery wrappers in v1. Start with a flat discovery surface across workflows and skills. Preserve hierarchy through metadata such as `workflow_group`, `workflow_kind`, and `stability`. Add group-level discovery wrappers only if flat discovery becomes too noisy in real use.

## Workflow Contract Shape

The first `workflow.yaml` vocabulary should stay small but should be stronger than an ordered step list.

It should cover:

- workflow identity, version, stability, kind, and group
- compatible package classes
- context dependencies
- tool and capability requirements
- allowed paths
- package and path inputs
- ordered steps
- outputs
- validation hooks and checks
- review gates
- trace and run-record requirements
- preconditions
- invariants
- budgets
- recovery semantics

This is a behavioral envelope, not a proof of correctness. Fields should be added only where they can produce checkable runtime signal on real workflows.

## Context Policy

Phase 2 promotes context admission now:

- required context is declared by the workflow contract
- loaded context paths are recorded
- loaded context hashes are recorded
- undeclared context is denied, detected, or recorded as a violation according to the enforcement surface
- context violations appear in run records

Context lifecycle governance remains open:

- decay
- pruning
- contradiction handling
- privacy policy
- versioned reuse

Do not turn Phase 2 into a repo-wide memory system. Add lifecycle policy only where real runs expose stale-authority, privacy, or resumption failures.

## Validation Stack

Validation is lifecycle infrastructure.

The Phase 2 stack is:

1. static contract checks
2. context admission checks
3. allowed tool and path enforcement
4. workflow validation hooks
5. bounded source-linked drift checks
6. trace and run-record checks
7. review gate evidence and approval

The first target is bounded denial and bounded checking, not perfect confinement. Every enforcement surface should say whether the first implementation denies, detects, or records for review.

## Governed Run Control Loop

1. a human operator, cockpit action, existing agent harness, or local automation invokes `content-agent` as the single Phase 2 runtime entrypoint
2. `content-agent` resolves package kind, route, and next valid action from repo state
3. the runtime loads the stage `workflow.yaml`
4. the runtime builds a `resolved_run` from the contract and package state, persisting it when the run is governed, gated, resumable, or audit-relevant
5. required context is admitted, hashed, and recorded
6. preconditions, invariants, budgets, and allowed surfaces are checked where supported
7. non-gated scriptable steps execute through declared repo-native tools
8. Codex-session-hosted steps run under the active `resolved_run` and return to `content-agent` for validation
9. validation results and trace data are written to the run record
10. the loop continues through eligible non-gated steps until a gate, terminal failure, budget limit, or workflow completion
11. if a review boundary is reached, the runtime writes a gate artifact under `reviewable-runs/gates/` and stops
12. the cockpit or CLI exposes pending gates and decisions
13. approval, rejection, or deferral resumes, redirects, or preserves execution state

## Minimum Platform Artifacts

### Run Trace Minimums

Every Phase 2 run path should be able to record:

- context file paths
- context content hashes
- workflow version or hash
- parent artifact ids
- validation results
- gate ids when applicable
- deny/detect/record outcomes for enforcement surfaces

These are the minimum trace primitives for source-linked debugging.

### Promoted-Output State Minimums

Phase 2 should use a small state model for promoted outputs:

- `authority_order`
- `claim_state`
- `contradiction_state`
- `validation_state`
- `trace_state`

V1 records this state in run records and review gate artifacts. Do not add a separate promoted-output manifest until outputs need independent tracking across multiple runs or gates.

## Research Constraints

Phase 2 should preserve the strongest promoted findings:

- manifest-first routing beats prose-first routing
- workflow specs become meaningful only when attached to runtime, validation, and policy
- workflow evolution needs explicit version and stability metadata
- workflow contracts need a small behavioral envelope
- context admission is governed dependency management
- validation is layered lifecycle infrastructure
- traces are derivative debugging records, not source
- gates are durable runtime objects
- skills need capability binding, routing, and verification before they become executable platform capabilities
- workflow discovery wrappers can improve Codex routing, but they are not workflow authority
- real package-path proof runs beat synthetic demos for closure

Phase 2 should not assume:

- context lifecycle governance is settled
- experimental workflows may silently replace canonical workflows
- import semantics are settled
- package-as-object semantics are ready for promotion
- full semantic provenance graphs are required before the platform can start
- event-sourced replay is required for the minimum trace layer
- multi-agent orchestration is the default runtime model
- current logs are already the source of truth

## Out Of Scope

Phase 2 is not:

- a multi-tenant SaaS
- a cloud execution layer
- a replacement for repo-native artifacts
- a repo-wide research-memory system
- a full semantic provenance platform
- an autonomous self-improvement loop
- a generic natural-language programming language
- a blanket promotion of every literate-workflow idea into the roadmap

## Verification Strategy

Phase 2 should be verified in layers:

1. static contract checks for `workflow.yaml`, root YAML surfaces, drift, and references
2. resolution tests that produce `resolved_run` from `status.yaml`, `workflow.yaml`, package state, policy, gates, and profiles
3. execution-state placement tests for resolved runs, run records, and gate artifacts under `reviewable-runs/`
4. enforcement tests for deny/detect/record behavior across context, paths, tools, validators, and gates
5. gate/resume tests for approve, reject, defer, and pending-gate visibility
6. run-mode tests for exploratory mode and governed continuous mode
7. real package-path proof runs

Passing static checks is not enough. Phase 2 closure requires retained proof runs on real packages that show the platform can run, stop, resume, validate, and record without replacing repo source-of-truth surfaces.

## Main Risks

- making `content-agent` fat before the workflow contract stabilizes
- expanding behavioral-envelope fields beyond what real workflows can validate
- treating context lifecycle governance as settled just because context admission is settled
- building the cockpit before trace and gate artifacts are stable
- duplicating contract truth across README prose and YAML fields
- letting validation collapse back into advisory prose
- treating logs or traces as authority instead of debugging evidence
- treating markdown skill guidance as executable capability without binding and verification
