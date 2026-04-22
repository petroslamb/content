# Workflow YAML Schema

## Purpose

Phase 2 needs a primary machine contract for lifecycle execution.

`workflow.yaml` is that contract.
The adjacent `README.md` remains the human explanation surface.

This decision is closed for Phase 2 planning: `workflow.yaml` is authored directly beside the README and checked for drift. It is not generated from prose.

## Design Rules

1. keep the machine contract explicit and small
2. do not duplicate long natural-language guidance into YAML
3. make runtime permissions and verification visible
4. make approval gates and trace requirements explicit
5. preserve package-local validation and review artifacts

## Required Top-Level Fields

Every `workflow.yaml` should declare:

- `workflow_id`
- `version`
- `summary`
- `package_classes`
- `runner_mode`
- `required_context`
- `allowed_tools`
- `allowed_paths`
- `steps`
- `trace_requirements`

Suggested shape:

```yaml
workflow_id: essay_iteration
version: 1
summary: Iterate an essay through bounded candidates and review gates.
package_classes:
  - leaf
runner_mode: guided
required_context:
  - package_status
  - package_readme
  - governing_brief
allowed_tools:
  - stage_runner
  - packet_initializer
  - packet_checker
allowed_paths:
  - publications/{package}/
  - reviewable-runs/
trace_requirements:
  include:
    - context_paths
    - context_hashes
    - workflow_hash
    - parent_artifact_ids
    - validation_results
steps:
  - id: resolve_packet
    mode: scripted
    command: .venv/bin/python scripts/init_essay_iteration_packet.py --package {package}
    outputs:
      - packet_manifest
    verify_with:
      - packet_manifest_exists
  - id: write_bounded_candidate
    mode: human_review_gate
    consumes:
      - packet_manifest
      - governing_brief
      - claim_scorecard
    allowed_tools:
      - editor
      - packet_checker
    allowed_paths:
      - publications/{package}/
      - reviewable-runs/
    outputs:
      - candidate_markdown
      - run_log
    approval_gate: major_rewrite
    preview_paths:
      - publications/{package}/{package}-candidate-r1.md
    verify_with:
      - check_essay_iteration_packet
```

## Step Model

Each step should declare:

- `id`
- `mode`
- `command` or named executor
- consumed inputs
- produced outputs
- allowed tools
- allowed paths
- local verification
- approval gate, if any
- trace requirements when the step adds special needs

Suggested `mode` values:

- `scripted`
- `hybrid`
- `human_review_gate`
- `external_approval_gate`

## Required Semantics

The machine contract should make these things explicit:

- workflow identity
- compatible package classes
- required context
- what the runtime may touch
- what each step produces
- what verification must run
- what kind of approval is required
- what trace data the step must leave behind

Phase 2 should be able to deny undeclared tools, undeclared paths, and undeclared context based on this contract.

## Relationship To The README

The intended split is:

- README explains the workflow to humans
- `workflow.yaml` defines what the runtime may do
- checks keep them aligned

The README should not be asked to carry machine authority through prose alone.

## Non-Goals

`workflow.yaml` should not try to encode:

- package-local argument structure
- long operator explanations
- speculative import semantics
- full semantic provenance graphs
- repo-wide research-memory behavior

Those belong elsewhere.
