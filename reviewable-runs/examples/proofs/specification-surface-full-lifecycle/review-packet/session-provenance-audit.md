# Session Provenance Audit

## Purpose

This audit checks whether the local Codex session and memory history can elevate this proof from a retrospective full-lifecycle proof candidate to a primary autonomous `content-agent` proof.

The audit inspected local-only provenance under `~/.codex/sessions`, `~/.codex/archived_sessions`, and `~/.codex/memories`. Raw session dumps are not imported into this tracked proof packet.

## Primary-Proof Criteria

| Criterion | Finding | Classification effect |
| --- | --- | --- |
| Governed runtime initiated the full lifecycle | `content-agent` was used for status, next-action, validation, and later expert-feedback runs, but the publication lifecycle was not initiated as one `content-agent run` campaign. | Blocks primary proof. |
| Workflow contracts governed the work | The sessions repeatedly checked package state, workflow contracts, release gates, archive sync, and distribution validation. | Supports secondary proof. |
| Clean bounded agent launch drove the package | The decisive closeout was driven by ordinary Codex interaction, browser work, helper scripts, and direct user prompts. | Blocks primary proof. |
| Outputs were validated | Release readiness, Substack public readback, archive sync, mirror validation, distribution validation, and `content-agent validate` records exist. | Supports secondary proof. |
| Approval gates and external mutations were recorded | The release gate and distribution records exist, but one decisive live-publication approval came from direct user instruction during the session. | Supports governed retrospective proof, not autonomous proof. |
| Tracked repo evidence reconstructs the outcome | The completed package can be reconstructed from tracked state, logs, archive snapshots, reports, and distribution records. | Supports retaining the proof. |

## Relevant Local Provenance

The strongest local provenance is the May 4 publication-closeout session. It shows:

- `content-agent status`, `next`, and `validate` were used to orient and check the package.
- The package was found incomplete at `substack_publishing`, `archive_sync`, and `distribution`.
- The release gate initially blocked on missing approval evidence.
- The user explicitly authorized continuation before live Substack mutation.
- Codex then executed the Substack sync, public readback, archive sync, mirror validation, distribution closeout, and status updates.

Earlier April 30 sessions show research, essay iteration, paper-route experimentation, and workflow validation, but they are also ordinary guided Codex sessions rather than a single governed runtime proof.

Later May 5 and May 6 expert-feedback outreach records show that the completed package can be admitted into the Phase 2 YAML evidence model with `resolved_run` and `run_record` artifacts. Those records are post-publication follow-on runs, not proof that the article lifecycle itself was autonomously executed.

## Verdict

Do not elevate this packet to primary proof.

Best classification remains `secondary candidate`: the lifecycle outcome is real, complete, validated, and reconstructable, but the execution mode was hybrid and human-prompted. A primary proof would require a fresh or separately captured lifecycle campaign where `content-agent run` launches bounded clean-agent work, records admitted context, writes run records and gates during execution, stops at approvals, resumes from gates, and validates outputs before lifecycle movement.
