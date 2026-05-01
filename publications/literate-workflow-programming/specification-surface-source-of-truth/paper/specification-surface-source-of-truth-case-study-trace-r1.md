---
kind: case_study_trace
package: "literate-workflow-programming/specification-surface-source-of-truth"
revision: 1
status: draft_trace_plan
created: "2026-04-30"
workflow: paper_development
source_blueprint: "specification-surface-source-of-truth-paper-blueprint.md"
case_type: illustrative_artifact_analysis
---

# Case Study Trace R1

## Purpose

This artifact turns the local workflow machinery into a concrete case-study plan for the paper. Its role is to keep the paper from becoming a pure position essay. The case study is illustrative: it shows how the taxonomy can classify a real file-backed workflow system, not that the system is generally effective.

## Unit Of Analysis

Package:

`publications/literate-workflow-programming/specification-surface-source-of-truth`

Workflow surface:

`paper_development`, with supporting evidence from the package's recently completed `essay_iteration` route.

Current package state as of 2026-04-30:

- `status.yaml` reports `kind: leaf`, `revision: 3`, and `essay_iteration.done: true`.
- The live draft is `specification-surface-source-of-truth.md`.
- The r3 packet now lives under `iterations/r3/`.
- The human approval surface records promotion of `iterations/r3/specification-surface-source-of-truth-candidate-r3-polished.md` into the live draft.
- `content-agent validate --workflow paper_development --package literate-workflow-programming/specification-surface-source-of-truth` passes with no findings.

## Research Questions For The Case

RQ-C1. Which package and workflow artifacts act as specification surfaces under the paper taxonomy?

RQ-C2. How does authority move from maintained source surfaces to runtime validation and retained evidence?

RQ-C3. Where does the case show repair or promotion pressure flowing back into a maintained surface rather than staying only in generated prose?

## Artifact Corpus

Primary corpus:

| Artifact | Path | Role In Case |
| :--- | :--- | :--- |
| Package status | `../status.yaml` | Lifecycle and context-admission authority. |
| Package README | `../README.md` | Human-facing package orientation and route boundary. |
| Claim boundary ledger | `../specification-surface-source-of-truth-claim-boundary-ledger.md` | Evidence and forbidden-claim surface. |
| R3 external review synthesis | `../iterations/r3/specification-surface-source-of-truth-external-review-synthesis-r3.md` | Review evidence and repair pressure. |
| R3 human approval | `../iterations/r3/specification-surface-source-of-truth-human-promotion-approval-r3.md` | Promotion authority surface. |
| Paper folder README | `README.md` | Local paper-work boundary. |
| Paper blueprint | `specification-surface-source-of-truth-paper-blueprint.md` | Paper-route source surface. |
| Paper publication route | `specification-surface-source-of-truth-publication-route-r1.md` | Venue and submission route surface. |

Root workflow and authority corpus:

| Artifact | Path | Role In Case |
| :--- | :--- | :--- |
| Authority map | `../../../../AUTHORITY.md` | Source-of-truth ordering. |
| Harness policy | `../../../../harness_policy.yaml` | Local write, approval, and enforcement policy. |
| Gate contracts | `../../../../gate_contracts.yaml` | Gate definitions and required artifacts. |
| Pipeline profiles | `../../../../pipeline_profiles.yaml` | Route sequencing and required gates. |
| Paper workflow contract | `../../../../workflows/paper-development/workflow.yaml` | Machine-readable paper-work contract. |
| Essay workflow contract | `../../../../workflows/essay-iteration/workflow.yaml` | Completed essay route contract. |
| Evidence authorization workflow | `../../../../workflows/evidence-authorization/workflow.yaml` | Claim-permission support route. |
| Content-agent runtime | `../../../../content-agent` and `../../../../scripts/content_agent.py` | Runtime surface that validates declared contracts. |
| Reviewable run logs | `../../../../reviewable-runs/logs/` | Evidence layer for prior runs and gate checks. |

## Observed Runtime Trace

Commands run for this case-study setup:

```bash
./content-agent status --package literate-workflow-programming/specification-surface-source-of-truth
./content-agent next --package literate-workflow-programming/specification-surface-source-of-truth
./content-agent validate --workflow paper_development --package literate-workflow-programming/specification-surface-source-of-truth
npm run check:repo-links
```

Observed summary:

| Command | Outcome | Paper-Relevant Interpretation |
| :--- | :--- | :--- |
| `content-agent status` | Passed; package is leaf revision 3; current lifecycle stage is `notebooklm_artifacts`; 12 workflow YAML surfaces are visible; no pending review gates. | The runtime reads package and root authority surfaces before reporting route state. |
| `content-agent next` | Next default publication stage is `notebooklm_artifacts`, but it is not directly executable without required NotebookLM context and approval. | The runtime distinguishes route readiness from allowed execution. Missing context blocks downstream automation. |
| `content-agent validate --workflow paper_development` | Passed with no findings. | The experimental paper workflow is a valid module even though it is not the package's default lifecycle stage. |
| `npm run check:repo-links` | Passed. | Local markdown references in paper artifacts resolve under repo-link validation. |

Representative prior evidence:

| Log | Summary |
| :--- | :--- |
| `reviewable-runs/logs/2026-04-30_01-44-42_literate-workflow-programming__specification-surface-source-of-truth_research_exit_gate-check.json` | Records `gate_id: research_exit` with `status: pass`. |
| `reviewable-runs/logs/2026-04-30_02-38-47_literate-workflow-programming__specification-surface-source-of-truth_essay_iteration_execute.json` | Records an `essay_iteration` lifecycle-stage run for the package. |

Boundary note: the retained logs are trace/evidence surfaces. They do not outrank `workflow.yaml`, root policy YAMLs, or package `status.yaml`.

## Artifact Classification

| Artifact | Surface Type | Lifecycle Stage | Operational Force | Failure Or Repair Implication |
| :--- | :--- | :--- | :--- | :--- |
| `AUTHORITY.md` | Authority/gate surface | specify | Defines which repo layer wins when surfaces disagree. | If logs or reports start acting as source authority, repair the authority map or the consuming workflow. |
| `status.yaml` | Authority/context surface | specify | Resolves package kind, revision, live draft path, evidence path, and stage state. | Stage decisions should be repaired here, not inferred from prose alone. |
| `workflows/paper-development/workflow.yaml` | Runtime and authority surface | specify, validate | Declares context dependencies, allowed read/write paths, outputs, checks, and trace requirements. | If paper artifacts drift into the leaf root or mutate the essay route, repair the workflow contract or package paper folder boundary. |
| `workflows/essay-iteration/workflow.yaml` | Runtime and gate surface | specify, generate, validate | Declares packet, candidate, review, scorecard, decision, and gate outputs. | Candidate promotion requires review and approval surfaces rather than direct overwrite. |
| `gate_contracts.yaml` | Gate surface | validate, repair | Defines movement, quality, promotion, and external-mutation gates. | Missing or bypassed approvals should stop promotion or external mutation. |
| `harness_policy.yaml` | Enforcement surface | specify, validate | Sets local-write, approval, mutation, and enforcement posture. | External mutation or promotion without explicit approval violates policy. |
| `pipeline_profiles.yaml` | Route surface | specify, repair | Declares ordered workflows, required gates, and fallback routes. | Route confusion should be fixed by profile or status updates, not by ad hoc run logs. |
| `content-agent` | Runtime surface | generate, validate, trace | Reads declared contracts and reports status, next action, validation findings, and gate state. | Runtime warnings identify context gaps that should repair package config or workflow inputs. |
| Claim boundary ledger | Evidence surface | specify, validate, repair | Names authorized, caveated, and forbidden claims. | If paper prose drifts into forbidden claims, repair the paper blueprint or mapping table. |
| External review synthesis | Evidence/repair surface | validate, repair | Aggregates external review findings and names required polish. | Review findings can repair candidate prose but do not by themselves authorize promotion. |
| Human promotion approval | Gate/authority surface | validate, repair | Records explicit user approval to promote polished r3 candidate into the live draft. | Promotion is authorized through this surface; without it, the live draft remains protected. |
| Paper blueprint | Source surface | specify | Defines paper claim, contribution, route, outline, taxonomy, mapping, and limits. | If the paper becomes a position essay, repair the blueprint before drafting. |
| Publication route note | Route surface | specify, repair | Records arXiv and peer-review route decisions, deadlines, and readiness criteria. | Do not post to arXiv until readiness criteria are met. |
| Reviewable run logs | Trace surface | trace | Retain prior run and gate-check evidence. | Logs diagnose what happened but are not source authority. |

## Lifecycle Trace

```text
specify
  status.yaml
  workflow.yaml
  claim-boundary ledger
  paper blueprint
    |
    v
generate
  essay candidates
  paper artifacts
  route notes
    |
    v
validate
  content-agent validate
  gate checks
  external review synthesis
  repo link checks
    |
    v
trace
  reviewable-runs/logs
  human promotion approval
  package README/status updates
    |
    v
repair
  polished candidate
  promoted live draft
  paper folder boundary
  paper blueprint and route artifacts
```

## Case Narrative

The package illustrates a separation between source authority, runtime interpretation, evidence, and promotion. The package `status.yaml` names the live draft, evidence path, and current lifecycle state. The root authority map assigns machine authority to workflow YAML, policy YAML, gate contracts, pipeline profiles, and package status, while explicitly subordinating logs and views to source authority.

The `paper_development` workflow makes the paper route explicit without mutating the public essay route. It admits the package status, package README, live draft or candidate, claim boundary ledger, evidence surface, and paper folder. Its allowed write path is the package-local `paper/` folder plus reviewable-run stores. That write boundary is the case's simplest concrete example of a specification surface: the paper route can produce paper artifacts, but it cannot silently promote essay prose or publish externally.

The completed r3 essay route supplies a second trace. External reviewers judged the candidate to clear the north-star bar and recommended bounded polish, but the external review synthesis explicitly did not authorize live draft replacement. The separate human promotion approval surface did. This separation is useful for the paper because it shows that evidence, review, and authority are different roles even when they concern the same object.

The retained run logs then record bounded operational facts, such as the research-exit gate passing and essay-iteration runs occurring. They are useful for audit and reconstruction, but the authority map prevents them from becoming the source of workflow behavior. In the paper's terms, logs are trace surfaces, not source surfaces.

## Repair Loop To Use In The Paper

The strongest repair loop in the case is:

1. r3 candidate is produced under essay-iteration surfaces.
2. external review synthesis identifies non-blocking polish requirements and confirms claim-boundary safety.
3. polished candidate is created as a separate artifact.
4. human promotion approval authorizes copying the polished candidate to the live draft.
5. package `status.yaml` marks `essay_iteration.done: true`, while downstream publication stages remain incomplete.

This loop is modest but paper-usable. It shows that review findings repair a maintained artifact, and promotion happens through an explicit approval surface rather than through the mere existence of a better generated file.

## Case-Study Claims Allowed

Allowed:

- The local repo is an illustrative example of file-backed specification surfaces.
- It demonstrates separable source, runtime, validation, trace, evidence, repair, and gate roles.
- It shows how a workflow can keep paper-route artifacts separate from public essay promotion.
- It shows that retained logs can support audit without becoming source authority.

Forbidden:

- Do not claim this repo proves general effectiveness.
- Do not claim this workflow is a universal best practice.
- Do not claim the repo has complete semantic provenance.
- Do not claim logs are the source of truth.
- Do not claim all documentation in the repo is a specification surface.

## Evidence Gaps Before Full Paper Draft

- The case needs a compact diagram in the manuscript, likely one figure showing authority layering and one figure showing the lifecycle loop.
- The case should include a short method paragraph explaining why this is an illustrative artifact analysis rather than empirical evaluation.
- If the paper targets ICSE NIER, the case section should be compressed to one artifact table plus one lifecycle trace.
- If the paper targets a longer workshop format, include one short command-output table.

## Case Study Readiness

Status: usable for an extended abstract.

Not yet enough for a full research-track paper. A research-track version would need a stricter case-study protocol, more than one system or workflow, independent coding, or an empirical question beyond taxonomy demonstration.
