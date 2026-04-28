# Workflow YAML Schema

## Purpose

`workflow.yaml` is the authored machine contract for Phase 2 workflow behavior.

It sits beside the workflow README. The README explains the workflow to humans. `workflow.yaml` defines what `content-agent` can load, validate, resolve, execute, stop, and record.

This file reflects [`2.1-executable-workflow-contract.md`](2.1-executable-workflow-contract.md). It names the practical v1 vocabulary only. Enforcement behavior is governed by [`2.2-enforcement-and-validation-layer.md`](2.2-enforcement-and-validation-layer.md), and durable evidence is governed by [`2.3-trace-and-provenance-minimums.md`](2.3-trace-and-provenance-minimums.md).

## Authority Rules

- `workflow.yaml` is authored directly and checked for drift.
- `workflow.yaml` is YAML-first. JSON is only for rebuildable caches, API responses, or external tool interoperability.
- README prose and skill guidance do not carry runtime permission, path, gate, routing, or completion semantics alone.
- Root `harness_policy.yaml`, `gate_contracts.yaml`, and `pipeline_profiles.yaml` constrain workflow contracts but do not replace per-workflow `workflow.yaml`.
- Package `status.yaml` supplies package lifecycle state; `workflow.yaml` supplies workflow behavior.
- `harness_contract.yaml` may remain a generated compatibility/index surface, not authored workflow authority.
- `resolved_run`, `run_record`, `review_gate`, and promoted-output state are derivative execution evidence. Workflow YAML may declare trace requirements for them, but the artifacts themselves are not hand-authored workflow truth.

## Design Rules

1. keep the authored contract explicit and checkable
2. avoid long natural-language operator guidance in YAML
3. make context, tools, capabilities, paths, outputs, gates, and validation visible
4. declare preconditions, invariants, budgets, and recovery only when they produce checkable runtime signal
5. declare deny/detect/record posture for enforcement surfaces without pretending Phase 2 has total sandboxing
6. keep trace requirements source-linked and minimal

## Top-Level Fields

Every platform-targeted `workflow.yaml` should declare:

- `workflow_id`
- `version`
- `stability`
- `workflow_kind`
- `workflow_group`
- `summary`
- `package_classes`
- `inputs`
- `context_dependencies`
- `capabilities`
- `allowed_paths`
- `outputs`
- `behavior`
- `enforcement`
- `validation`
- `gates`
- `trace`
- `steps`

Recommended enum values:

- `stability`: `canonical`, `experimental`
- `workflow_kind`: `stage`, `module`, `overlay`
- `steps[].mode`: `scriptable`, `codex_session`, `review_gated`, `external_mutation_gated`
- enforcement posture values: `deny`, `detect`, `record`

## Suggested Shape

```yaml
workflow_id: essay_iteration
version: 1
stability: canonical
workflow_kind: stage
workflow_group: essay_lifecycle
summary: Iterate an essay through bounded candidates and review gates.

package_classes:
  - leaf

inputs:
  package:
    required: true
  paths:
    - id: package_root
      pattern: publications/{package}/
    - id: reviewable_runs
      pattern: reviewable-runs/

context_dependencies:
  - id: package_status
    path: publications/{package}/status.yaml
    required: true
    purpose: Read package lifecycle state before resolving the next action.
    record_hash: true
  - id: package_readme
    path: publications/{package}/README.md
    required: true
    purpose: Load human package orientation.
    record_hash: true
  - id: governing_brief
    path: publications/{package}/brief.md
    required: false
    purpose: Load the accepted package brief when present.
    record_hash: true

capabilities:
  tools:
    - id: packet_initializer
      command: .venv/bin/python scripts/init_essay_iteration_packet.py
    - id: packet_checker
      command: .venv/bin/python scripts/check_essay_iteration_packet.py
  skills: []

allowed_paths:
  read:
    - publications/{package}/
    - reviewable-runs/
  write:
    - publications/{package}/
    - reviewable-runs/resolved-runs/
    - reviewable-runs/logs/
    - reviewable-runs/gates/

outputs:
  - id: packet_manifest
    path: publications/{package}/review/essay_iteration_packet.yaml
    required: true
  - id: candidate_markdown
    path: publications/{package}/{package}-candidate-r1.md
    required: false
    promotable: true

behavior:
  preconditions:
    - id: package_status_exists
      check: path_exists
      target: publications/{package}/status.yaml
      on_fail: stop
  invariants:
    - id: no_publish_without_gate
      check: external_mutation_requires_gate
  budgets:
    max_steps: 8
    max_retries: 1
    external_mutations: 0
  recovery:
    on_validation_failure: stop
    on_gate_reject: defer
    resume_from: resolved_run

enforcement:
  context_admission: deny
  tool_use: deny
  path_access: deny
  external_mutation: deny
  lifecycle_movement: deny
  trace_completeness: detect

validation:
  static_checks:
    - workflow_contract_loads
    - readme_yaml_drift
  hooks:
    - id: packet_manifest_exists
      command: .venv/bin/python scripts/check_essay_iteration_packet.py --package {package}
  drift_checks:
    - id: candidate_matches_governing_brief
      pattern: spec-diff
      required: false

gates:
  - id: major_rewrite_review
    type: content_quality
    contract: major_rewrite
    decisions:
      - approve
      - reject
      - defer
  - id: publish_boundary
    type: external_mutation
    contract: publication_approval
    decisions:
      - approve
      - reject
      - defer

trace:
  include:
    - context_paths
    - context_hashes
    - workflow_id
    - workflow_version
    - workflow_hash
    - parent_artifact_ids
    - validation_results
    - enforcement_outcomes
    - gate_ids
  run_record: required
  resolved_run:
    persist_when:
      - governed
      - gated
      - resumable
      - audit_relevant

steps:
  - id: resolve_packet
    title: Resolve iteration packet
    mode: scriptable
    executor:
      command: .venv/bin/python scripts/init_essay_iteration_packet.py --package {package}
    consumes:
      - package_status
      - package_readme
    produces:
      - packet_manifest
    validation:
      hooks:
        - packet_manifest_exists
    trace:
      required: true

  - id: write_bounded_candidate
    title: Write bounded candidate
    mode: codex_session
    consumes:
      - packet_manifest
      - governing_brief
    produces:
      - candidate_markdown
    validation:
      drift_checks:
        - candidate_matches_governing_brief
    gate:
      id: major_rewrite_review
    trace:
      required: true
```

## Field Semantics

### Identity And Scope

- `workflow_id` is the stable identity used by package state, profiles, run records, and gates.
- `version` is recorded in `resolved_run` and `run_record`.
- `stability` decides whether the workflow can be routed by default.
- `workflow_kind` distinguishes lifecycle stages, reusable modules, and overlays.
- `workflow_group` is discovery and organization metadata, not execution authority by itself.
- `package_classes` limits compatible package kinds such as `leaf` or `umbrella`.

### Context And Capabilities

- `context_dependencies` declares context as a governed dependency.
- Each context item should say whether it is required, why it is needed, and whether the runtime records its hash.
- `capabilities.tools` declares repo-native tools or named commands.
- `capabilities.skills` binds operator guidance or helper capabilities; a skill does not own routing, gates, package state, or promotion.
- `allowed_paths` declares read/write surfaces. Policy may narrow these paths.

### Behavioral Envelope

- `preconditions` must hold before execution starts.
- `invariants` must remain true while the workflow runs.
- `budgets` define bounded limits such as steps, retries, time, files, or external operations.
- `recovery` declares stop, resume, retry, defer, rollback, or fail-closed behavior.

The envelope should stay small. Do not add fields that cannot be checked by `content-agent validate`, a declared hook, or a later proof run.

### Enforcement And Validation

- `enforcement` declares the workflow-level deny/detect/record posture.
- Root `harness_policy.yaml` is the policy floor. Workflow posture can narrow it, not silently weaken it.
- `validation.static_checks` covers contract shape, references, and README/YAML drift.
- `validation.hooks` names local commands or checks.
- `validation.drift_checks` supports bounded source-linked checks where they add signal.

### Gates And Trace

- `gates` names gate instances and references gate classes in `gate_contracts.yaml`.
- Quality approval and external mutation approval should remain distinguishable.
- `trace.include` names the evidence the run record must preserve.
- `trace.resolved_run.persist_when` declares when `content-agent` must write durable resolved state.

## Step Model

Each `steps[]` item should declare:

- `id`
- `title`
- `mode`
- executor command or declared manual/model-mediated action
- consumed context or artifacts
- produced outputs
- validation hooks or drift checks
- gate reference, if gated
- trace requirement

Step-level fields may narrow top-level capabilities, paths, validation, gates, or trace requirements. They should not widen top-level policy without an explicit root-policy allowance.

## Relationship To Discovery Wrappers

Workflow discovery wrappers are not part of this schema. They are thin skill-like routing hints for Codex/operator discovery.

In v1, wrappers are hand-authored only where useful, and they must point back to the canonical `workflow.yaml` and README. They should not duplicate process rules that belong in this schema.

## Non-Goals

`workflow.yaml` should not encode:

- long operator explanations
- package-local article argument structure
- generated `resolved_run`, `run_record`, or `review_gate` artifacts
- standalone promoted-output manifests
- context lifecycle governance beyond admission requirements
- speculative import semantics
- host-independent verifiable traces
- full semantic provenance graphs
- repo-wide research-memory behavior
- default subagent-hosted execution
