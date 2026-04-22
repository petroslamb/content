# Phase 2 Architecture

## Goal

Phase 2 adds a local execution platform on top of the repo contract.

The platform should:

- execute workflow contracts
- validate and constrain runtime behavior
- write traces and gate artifacts
- stop cleanly at review boundaries
- expose state in a thin local cockpit

It should do that without replacing the filesystem-backed repo surfaces as the source of truth.

## Core Decisions

These decisions are closed for Phase 2 planning:

- `workflow.yaml` is the **primary machine contract**
- `workflow.yaml` is authored directly beside each workflow README
- the workflow README remains the **human explanation surface**
- drift between README and YAML is controlled by checks, not by making prose the machine truth
- `content-agent` is **thin first** and wraps stable stage-resolution and run machinery
- pending review state lives in a central file-backed gate store under `reviewable-runs/gates/`
- the cockpit is a thin reader/approver over filesystem-backed truth, not a second system of record

## Source Of Truth

Phase 2 should keep truth file-backed:

- `status.yaml` for package lifecycle state
- package files for content and artifacts
- `workflow.yaml` for machine execution contracts
- workflow READMEs for human guidance
- `reviewable-runs/logs/` for run records
- `reviewable-runs/gates/` for pending and resolved review gates

Local indexes or caches are allowed only when they are rebuildable from those files.

## Layering

### Repo Contract Layer

Owns:

- manifests
- workflow READMEs
- `workflow.yaml`
- package structure
- validation scripts and run records

### Operator Shell Layer

Owns:

- named skills
- generated operator docs
- visible safety modes
- selective persistent browser support

### Phase 2 Platform Layer

Owns:

- contract loading
- execution planning
- validation and denial hooks
- trace writing
- gate creation and resumption
- the thin `content-agent` wrapper
- the local cockpit

Phase 2 should consume the lower layers, not re-encode them.

## Platform Objects

The platform should treat these as first-class objects:

- `package`
- `workflow_contract`
- `run_request`
- `run_record`
- `review_gate`
- `approval_decision`
- `promoted_output_state`

Each object should map back to a tracked or rebuildable file-backed artifact.

## Control Loop

1. operator or harness invokes `content-agent`
2. `content-agent` resolves package and next valid action from repo state
3. the runtime loads the stage `workflow.yaml`
4. the runtime verifies required context and denies undeclared context, tools, or paths where applicable
5. non-gated steps execute through repo-native tools
6. validation results and trace data are written to the run record
7. if a review boundary is reached, the runtime writes a gate artifact under `reviewable-runs/gates/` and stops
8. the cockpit or CLI exposes pending gates and decisions
9. approval or rejection resumes or redirects execution

## Minimum Platform Artifacts

### Run Trace Minimums

Every Phase 2 run path should be able to record:

- context file paths
- context content hashes
- workflow version or hash
- parent artifact ids
- validation results
- gate ids when applicable

These are the minimum trace primitives for source-linked debugging.

### Promoted-Output State Minimums

Phase 2 should also define a small state model for promoted outputs:

- `authority_order`
- `claim_state`
- `contradiction_state`
- `validation_state`
- `trace_state`

The exact storage surface remains open. It may live in run records, gate artifacts, or a separate small manifest, but the vocabulary should be stable across all three.

## Research Constraints

Phase 2 should preserve the strongest findings from `literate-workflow-programming`:

- manifest-first routing beats prose-first routing
- workflow specs become meaningful only when attached to runtime, validation, and policy
- validation is lifecycle infrastructure, not a trailing test pass
- traces are derivative debugging records, not source
- bounded drift detection is useful before broad conformance claims
- workflow-as-namespace is promotable as a routing concept
- skills need capability binding, routing, and verification

Phase 2 should not assume:

- import semantics are settled
- package-as-object semantics are ready for promotion
- full semantic provenance graphs are required before the platform can start
- current logs are already the source of truth

## Out Of Scope

Phase 2 is not:

- a multi-tenant SaaS
- a cloud execution layer
- a replacement for repo-native artifacts
- a repo-wide research-memory system
- a blanket promotion of every literate-workflow idea into the roadmap

## Main Risks

- making `content-agent` fat before the workflow contract stabilizes
- building the cockpit before trace and gate artifacts are stable
- duplicating contract truth across README prose and YAML fields
- letting validation collapse back into advisory prose
- treating logs as the authority surface instead of as debugging evidence
