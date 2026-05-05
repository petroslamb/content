# Repository Authority Map

This file is the source-of-truth map for operating `/Users/petros/Projects/content` after the Phase 2 migration.

It does not replace package READMEs, workflow READMEs, or strategy docs. It defines which layer wins when those surfaces disagree.

## Authority Order

| Layer | Owns | Canonical Surfaces | Rule |
| :--- | :--- | :--- | :--- |
| Strategy intent | roadmap, architecture, open questions, phase boundaries | `phased-strategy/`, especially `phased-strategy/phase-2/` | Guides changes, but runtime should not infer permissions from strategy prose. |
| Source authority | workflow behavior, global policy, gate classes, routes, package lifecycle state | `workflows/*/workflow.yaml`, `harness_policy.yaml`, `gate_contracts.yaml`, `pipeline_profiles.yaml`, `publications/**/status.yaml` | Highest editable machine truth for governed work. |
| Package authority | drafts, blueprints, evidence, media, archive, package-local artifacts | `publications/**` package files | Owns publication content and package-local evidence. |
| Runtime surface | resolution, context admission, validation, run/gate creation, review decisions, resume | `./content-agent`, `scripts/content_agent.py` | Executes declared contracts. It must not invent workflow semantics. |
| Evidence layer | resolved runs, run records, review gates, validation outcomes, promotion state | `reviewable-runs/resolved-runs/`, `reviewable-runs/logs/`, `reviewable-runs/gates/` | Records what happened. It does not outrank source authority. |
| View layer | local inspection, approval UI, generated reports | `./content-cockpit`, `scripts/generate_editorial_report.py` | Convenience only. Views must be rebuildable from file-backed truth or traceable to it. |

## Operating Surface

Use `content-agent` for governed work:

```bash
./content-agent status --package <package>
./content-agent next --package <package>
./content-agent validate --workflow <workflow_id> --package <package>
./content-agent run --workflow <workflow_id> --package <package>
./content-agent gate check --gate <gate_id> --package <package>
./content-agent review list
./content-agent review inspect --gate <gate_id>
./content-agent review approve --gate <gate_id> --reason "<reason>"
./content-agent review reject --gate <gate_id> --reason "<reason>"
./content-agent review defer --gate <gate_id> --reason "<reason>"
./content-agent resume --gate <gate_id>
```

Equivalent npm aliases exist for common entrypoints, for example `npm run content-agent -- status`, `npm run agent:status -- --package <package>`, and `npm run agent:validate -- --workflow <workflow_id> --package <package>`.

Use the cockpit when a local browser surface is more useful than terminal output:

```bash
./content-cockpit --package <package>
npm run cockpit -- --package <package>
```

Use the editorial report generator as report-only automation:

```bash
npm run editorial:report -- --package <package>
```

The report may create findings and suggestions. It must not rewrite drafts, approve gates, move lifecycle state, publish, or promote outputs.

## Retired Compatibility Surfaces

The older npm runner commands and generated compatibility index have been retired from the active operator surface:

- `harness_contract.yaml`
- `npm run run`
- `npm run stage:next`
- `npm run stage:resolve`
- `npm run stage:run`
- `npm run workflow:resolve`
- `npm run workflow:run`
- `npm run gate:check`

Use `./content-agent` for status, next-action resolution, validation, workflow runs, gate checks, review decisions, and resume records. Historical strategy notes and old run records may still mention the retired names when describing earlier work.

## Adding Or Changing A Workflow

1. Update the human explanation in `workflows/<workflow>/README.md`.
2. Update or add the machine contract in `workflows/<workflow>/workflow.yaml`.
3. If the workflow introduces a gate class, update `gate_contracts.yaml`.
4. If the workflow changes route sequencing, update `pipeline_profiles.yaml`.
5. If the workflow changes package lifecycle expectations, update affected package `status.yaml` files or package READMEs.
6. Run:

```bash
npm run check:workflow-yaml
npm run check:workflow-model
./content-agent validate --workflow <workflow_id>
```

7. For canonical or policy-sensitive workflows, create a retained real-package proof through `./content-agent run` before claiming the change is operationally proven.

## Context Control

Context control lives in `workflow.yaml`.

Each governed workflow should declare:

- context dependencies
- allowed read paths
- allowed write paths
- required tools and capabilities
- validation hooks
- gate requirements
- trace requirements

`content-agent validate` and governed runs can then surface missing, undeclared, or out-of-bounds context. This is not total sandboxing and not a repo-wide memory system. It is file-backed admission control for governed workflow execution.

## Evidence Rules

Use `reviewable-runs/` for execution evidence:

- `resolved-runs/` stores durable resolved runtime state when a run is governed, gated, resumable, continuous, or audit-relevant.
- `logs/` stores run records and legacy operational logs.
- `gates/` stores file-backed review gates.

Do not make logs or gates the source of truth for workflow behavior. They record outcomes against source authority.

## Clean Migration Boundary

The Phase 2 migration is a source-of-truth consolidation, not a package reshuffle.

Do not move publication packages just to satisfy this map. Do not force all historical logs into the new YAML format. Do not remove compatibility commands while active docs and scripts still reference them.

New governed work should route through the authority layer above. Existing historical notes may still mention older runner surfaces when they are describing older work.
