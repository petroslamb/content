---
kind: claim_boundary_surface
package: "proof-runs-as-source-surface"
revision: 1
evidence_surface_path: "publications/proof-runs-as-source-surface/papers/index.md"
auxiliary_evidence_paths:
  - "publications/proof-runs-as-source-surface/research-notes/alphaxiv-shortlist-r1.md"
  - "publications/proof-runs-as-source-surface/research-notes/paper-intake-queue-r1.md"
  - "publications/proof-runs-as-source-surface/proof-runs-as-source-surface-research-exit-gate-r1.md"
  - "reviewable-runs/logs/phase-2-primary-topic-discovery-proof-topic-discovery-handoff.md"
gate_role: essay_iteration_prewrite_claim_boundary
---
# Proof Runs As Source Surface Claim Boundary Ledger

## Purpose

This ledger states which claims the first bounded candidate may carry out of the approved research exit and into essay iteration. It is narrower than a publication fact check. Its job is to prevent the proof-run essay from turning a successful local Phase 2 pass into a claim about complete autonomous publication reliability.

## Source Surfaces

Primary package evidence:

- [`papers/index.md`](papers/index.md)
- [`research-notes/alphaxiv-shortlist-r1.md`](research-notes/alphaxiv-shortlist-r1.md)
- [`research-notes/paper-intake-queue-r1.md`](research-notes/paper-intake-queue-r1.md)
- [`proof-runs-as-source-surface-research-exit-gate-r1.md`](proof-runs-as-source-surface-research-exit-gate-r1.md)

Primary repo proof evidence:

- [`../../reviewable-runs/logs/phase-2-primary-topic-discovery-proof-topic-discovery-handoff.md`](../../reviewable-runs/logs/phase-2-primary-topic-discovery-proof-topic-discovery-handoff.md)
- [`../../reviewable-runs/resolved-runs/phase-2-primary-topic-discovery-proof.yaml`](../../reviewable-runs/resolved-runs/phase-2-primary-topic-discovery-proof.yaml)
- [`../../reviewable-runs/gates/gate-phase-2-primary-topic-discovery-proof-topic-viability.yaml`](../../reviewable-runs/gates/gate-phase-2-primary-topic-discovery-proof-topic-viability.yaml)

## Claim Map

| Claim ID | Authorized Claim | Evidence Status | Draft Permission | Boundary |
| :--- | :--- | :--- | :--- | :--- |
| PR-C1 | A governed proof run is a stronger source surface for agent work than an unstructured transcript because it records declared workflow, admitted context, bounded tools, validation, gate state, and resume evidence. | Supported by the repo proof artifacts and by schema-gated, specification-driven, and audit-oriented papers in the package evidence index. | Main body claim. | Do not claim proof runs are self-authenticating or sufficient without human review. |
| PR-C2 | The separation between `workflow.yaml`, `status.yaml`, policy, gate contracts, pipeline profiles, runtime execution, and evidence is the trust mechanism. | Directly supported by the current repo architecture and the Phase 2 proof artifacts. | Body definition and architecture explanation. | Do not collapse the architecture into a single status manifest or a hidden workflow language inside `content-agent`. |
| PR-C3 | The relevant research backdrop is a move toward specification discipline, context grounding, schema-gated execution, and auditable workflow evidence. | Supported by SWE-AGI, Spec Kit Agents, SWE-Bench Pro, the Productivity-Reliability Paradox, Talk Freely, Execute Strictly, and SPECA. | Body synthesis claim with cited papers doing visible work. | Do not present the synthesis as a single paper finding. |
| PR-C4 | Gate stops are the boundary between probabilistic work and authorized lifecycle movement. | Supported by the local topic-discovery and research-exit gates, plus the schema-gated execution papers. | Body claim and closing claim. | Do not say gates prove quality by themselves. They prove that movement was stopped, inspected, and explicitly resumed. |
| PR-C5 | Phase 2 has shown a local governed path through topic discovery, package initialization, research exit, paper intake, and essay-iteration prewrite proof. | Supported only after the current proof packet and validation records are retained. | Local proof claim. | Do not extend this to publication, external mutation, or distribution reliability. |
| PR-C6 | Publication reliability remains unproven until later stages emit release, publication, archive, and distribution evidence under their own gates. | Supported by the gate model and the stated Phase 2 boundaries. | Required caveat near any strong reliability language. | Do not let the essay close as if a local proof pass equals a publication system. |

## Source Burden

The body may use the local Phase 2 artifacts to explain the proof-run anatomy. Those artifacts carry the repo-specific claim.

The papers carry the broader pattern. SWE-AGI and Spec Kit Agents carry the specification-driven workflow pressure. SWE-Bench Pro and the Productivity-Reliability Paradox carry the reliability caveat. Talk Freely, Execute Strictly and SPECA carry the schema-gate and auditability frame.

## Forbidden Claims

- Do not claim full autonomous publication reliability.
- Do not claim external mutation safety.
- Do not claim benchmark progress is enough to trust agent work.
- Do not claim `content-agent` can invent behavior outside declared workflow contracts.
- Do not claim a gate approval is the same thing as publication approval.

## Drafting Instructions

Use `proof run` as the central object. Treat `source surface` as the role that object plays for human review. Keep the local proof claim bounded to governed local runtime behavior and lifecycle gates. Use the papers to explain why this architecture belongs to the broader research direction, not to inflate the local proof beyond what it has emitted.

## Follow-On Research Triggers

If the candidate starts making claims about release readiness, external mutation safety, or distribution reliability, stop and require stage-specific proof artifacts. If the paper discussion needs quote-level close reading, inspect the local markdown conversions against the PDFs before promotion review.
