# Phase 2 Milestones

Phase 2 is ordered around stable file-backed authority before runtime convenience.

The sequence is:

1. source workflow contracts
2. bounded enforcement and validation
3. execution evidence and review gates
4. deterministic `content-agent` runtime
5. thin local cockpit
6. bounded editorial automation
7. disciplined clean-context subagent handoffs

That order is deliberate. Phase 2 should not start with a dashboard, fat runtime, or autonomous agent wrapper over unstable workflow semantics.

## Baseline Assumptions

Phase 2 consumes the current repo model rather than redesigning package shape:

- umbrella roots use `status.yaml` with `kind: umbrella`
- leaf publication objects use `status.yaml` with `kind: leaf`
- settled umbrella roots may have no active stage
- active umbrella roots may route through `umbrella_route` or through an active default leaf
- package content artifacts remain in package directories
- generated execution evidence lives under `reviewable-runs/`

Use current publication packages as fixtures. Do not invent synthetic package classes to prove Phase 2.

## Spec Stack

The current operative stack is:

- [`architecture.md`](architecture.md): authority planes, runtime boundary, object boundaries, and run modes
- [`2.1-executable-workflow-contract.md`](2.1-executable-workflow-contract.md): authored workflow source contract
- [`2.2-enforcement-and-validation-layer.md`](2.2-enforcement-and-validation-layer.md): deny/detect/record posture and validation stack
- [`2.3-trace-and-provenance-minimums.md`](2.3-trace-and-provenance-minimums.md): resolved runs, run records, review gates, and promoted-output state
- [`2.4-gate-runtime-and-content-agent.md`](2.4-gate-runtime-and-content-agent.md): deterministic CLI/runtime implementation plan
- [`2.5-local-cockpit.md`](2.5-local-cockpit.md): cockpit dependency boundary and v0 scope
- [`2.6-editorial-automation.md`](2.6-editorial-automation.md): bounded editorial automation plan
- [`2.7-agent-handoff-discipline.md`](2.7-agent-handoff-discipline.md): post-baseline parent/subagent handoff discipline
- [`workflow-yaml-schema.md`](workflow-yaml-schema.md): schema companion to 2.1, not a competing authority

## Subphase Read

| Subphase | Job | Depends On | Done When |
| :--- | :--- | :--- | :--- |
| **2.1 Executable Workflow Contract** | Author per-workflow `workflow.yaml` as the highest functional truth layer for workflow behavior. | Architecture decisions, current workflow READMEs, root YAML surfaces, package `status.yaml`. | Implemented. Target workflows have authored YAML contracts with identity, version, stability, kind, group, context dependencies, capabilities, paths, steps, outputs, validation, gates, trace requirements, and a small behavioral envelope. |
| **2.2 Enforcement and Validation Layer** | Attach contracts to bounded runtime checks. | Stable 2.1 contract vocabulary. | Implemented. Each enforcement surface declares `deny`, `detect`, or `record`; `content-agent validate` reports contract, context, path/tool, gate, and trace-readiness findings without promotion. |
| **2.3 Trace and Provenance Minimums** | Define derivative execution evidence for debugging, resume, gates, and promotion. | Stable 2.1 and 2.2 semantics. | Implemented. Governed or proof-relevant runs persist `resolved_run`, write source-linked `run_record`, stop at YAML-backed `review_gate`, and record promoted-output state in run/gate artifacts. |
| **2.4 Gate Runtime and `content-agent`** | Implement the deterministic CLI/runtime over stable contracts and evidence. | 2.1, 2.2, 2.3, `gate_contracts.yaml`, `pipeline_profiles.yaml`, `harness_policy.yaml`. | Implemented. `content-agent init`, `status`, `next`, `run`, `resume`, `review`, and `validate` work over file-backed truth without becoming an LLM persona or second orchestration language. |
| **2.5 Local Cockpit** | Add a thin browser reader/approver over package state, gates, and recent runs. | Stable gate store, run records, and CLI commands. | Implemented. The cockpit exposes package state, pending gates, recent runs, validation health, gate decisions, and report-only editorial checks while leaving filesystem-backed YAML and package files authoritative. |
| **2.6 Editorial Automation** | Add structured editorial/style/compliance reporting. | Stable governed run path and article-polish boundaries. | Implemented. Automation produces reports, violations, and source-improvement suggestions without autonomous rewrite, promotion, publication, or lifecycle authority. |
| **2.7 Agent Handoff Discipline** | Formalize clean-context subagent handoffs after the deterministic runtime baseline. | 2.4 runtime boundary, 2.6 editorial automation closeout, `codex_session_handoff` policy, and Reviewable Runs handoff stores. | Strategy subphase documented. Parent sessions orchestrate, worker subagents do model-mediated work with `fork_context=false`, `content-agent` emits and validates deterministic artifacts without spawning models, and hook/skill additions remain later implementation work. |

## Implementation Closeout

The Phase 2.1-2.6 local platform baseline is implemented.

Retained proof:

- run id: `phase-2-6-editorial-report-proof`
- package: `neural-architectures/neural-architecture-design-as-a-compositional-32e`
- resolved run: `reviewable-runs/resolved-runs/phase-2-6-editorial-report-proof.yaml`
- run record: `reviewable-runs/logs/phase-2-6-editorial-report-proof.yaml`
- review gate: `reviewable-runs/gates/gate-phase-2-6-editorial-report-proof-release-readiness.yaml`
- package report: `publications/neural-architectures/neural-architecture-design-as-a-compositional-32e/artifacts/editorial-report-r4.json`

That proof demonstrates the current platform path on a real package: `article_polish` produced a structured editorial report, recorded the report as a declared workflow output, stopped at a file-backed release-readiness gate, and linked the live draft plus report into gate preview and evidence paths.

Do not read this as a claim that Phase 2 now performs autonomous end-to-end publication. External mutation, lifecycle movement, and promotion remain gate-controlled and human-approved.

Phase 2.7 is a post-baseline discipline layer rather than a new autonomy claim. It records how parent sessions should supervise clean-context workers, how workers should exit, and which request/result fields, skills, and hooks should be implemented later.

## First Workflow Set

2.1 should start with the workflows that define the essay lifecycle and external publication path:

- `paper-intake`
- `alphaxiv-research`
- `essay-iteration`
- `article-polish`
- `substack-publishing`
- `substack-archive-sync`

Do not convert every workflow in the repo first. Add another workflow only when a real package-path run needs it.

## Execution Order

### 1. Source Contract Pass

Complete the `workflow.yaml` contract layer for the first workflow set.

This pass should produce:

- authored YAML contracts beside workflow READMEs
- practical v1 schema conformance
- README/YAML drift checks
- context dependencies as governed dependencies
- tool/capability and path declarations
- preconditions, invariants, budgets, and recovery semantics where checkable
- gate and trace references without implementing the full gate runtime
- optional thin hand-authored discovery wrappers that point back to canonical `workflow.yaml`

### 2. Enforcement And Validation Pass

Add the bounded runtime checks that make workflow contracts honest.

This pass should produce:

- static contract checks
- package and route resolution checks
- context admission checks
- allowed tool, capability, and path checks
- precondition, invariant, budget, and recovery checks where supported
- workflow validation hooks
- bounded source-linked drift checks for at least one high-value stage family
- explicit `deny`, `detect`, or `record` posture for each enforcement surface

Do not claim perfect confinement. Work outside the governed path may happen, but it does not count as valid platform progress until validated and recorded.

### 3. Execution Evidence Pass

Build the minimum evidence layer under `reviewable-runs/`.

This pass should produce:

- durable `resolved_run` files for governed, gated, resumable, continuous, or audit-relevant runs
- source-linked run records under `reviewable-runs/logs/`
- YAML-backed review gate artifacts under `reviewable-runs/gates/`
- context paths and hashes in run records
- workflow id, version, and hash in run records
- validation results and enforcement outcomes in run records
- gate ids and approval decisions in run/gate evidence
- promoted-output state recorded in run records and gates

Do not introduce standalone promoted-output manifests, full semantic provenance graphs, event-sourced replay, host-independent trace formats, or agent registries in this pass.

### 4. Gate Runtime And `content-agent` Pass

Implement `content-agent` as deterministic infrastructure.

The v1 command surface is:

- `content-agent init`
- `content-agent status`
- `content-agent next`
- `content-agent run`
- `content-agent resume`
- `content-agent review`
- `content-agent validate`

The runtime should:

- load `workflow.yaml`, package `status.yaml`, root policy/profile/gate YAMLs, and package artifacts
- resolve next valid workflow/action from package state
- admit context as a declared dependency
- validate contracts and enforcement posture
- write source-linked run records
- persist `resolved_run` only when governance, gates, resume, continuity, or audit require it
- stop at file-backed review or external mutation gates
- resume from gates only through explicit approval, rejection, or deferral

`content-agent` is not a separate LLM persona and does not require separate model credentials in the first architecture.

### 5. Cockpit Pass

Add a thin local reader/approver after the file-backed runtime objects stabilize.

The cockpit should expose:

- package lifecycle state
- selected route or next action
- active/pending gates
- recent run records
- validation health

It may index for convenience, but it must remain rebuildable or traceable to filesystem-backed truth.

### 6. Editorial Automation Pass

Add editorial automation after governed runs and approval boundaries are stable.

The starting point is:

- voice/style reports
- structured violations
- source-improvement suggestions based on repeated correction patterns
- article-polish checks that run under workflow contracts

This pass must not create autonomous rewrite, promotion, publication, or lifecycle authority.

### 7. Agent Handoff Discipline Pass

Formalize clean-context subagent handoffs after the deterministic runtime baseline exists.

This pass should produce:

- a Phase 2.7 strategy doc after 2.6
- a hard worker exit protocol
- request-artifact additions for recommended skills, exit protocol, and verification requirements
- result-artifact additions for deterministic verification commands
- a skill plan beginning with `content-agent-handoff`
- a design-only hook plan for later Stop-hook enforcement

This pass must not enable hooks by default, edit runtime code, change workflow YAML, spawn models from `content-agent`, clear gates automatically, or claim autonomous publication.

## Phase 2 Gate Read

The implemented Phase 2 baseline now shows:

1. stable `workflow.yaml` contracts for the target lifecycle workflows
2. schema and drift checks that make README/YAML authority boundaries visible
3. validation that can deny, detect, or record undeclared context, tools, paths, gates, budgets, and trace gaps
4. durable review gates visible outside terminal logs
5. source-linked run records with context hashes, workflow version/hash, parent artifacts, validation results, enforcement outcomes, gate ids, and promoted-output state
6. `content-agent` commands operating over file-backed truth without replacing repo source surfaces
7. retained proof runs on real package paths, not synthetic demos
8. documented handoff discipline that keeps model-mediated work in clean-context subagents while preserving deterministic evidence

The stronger claim that the platform is reliable across multiple fresh idea-to-publication lifecycles remains outside this implementation closeout. That is a later proof campaign, not a prerequisite for the Phase 2.1-2.6 local baseline.

## Explicit Deferrals

The following remain out of the Phase 2 milestone baseline:

- repo-wide research memory
- context lifecycle governance beyond admission checks
- package-as-object semantics
- markdown import semantics
- standalone promoted-output manifests
- full semantic provenance graphs
- event-sourced replay as a minimum requirement
- hidden multi-agent orchestration, autonomous model spawning, or external scheduler-driven subagent routing as the default runtime model
- default-enabled hook enforcement for subagent exits
- host-independent verifiable traces
- autonomous self-improvement or harness synthesis
