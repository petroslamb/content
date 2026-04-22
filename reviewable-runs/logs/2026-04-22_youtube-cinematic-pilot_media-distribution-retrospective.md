# Harness Proof Run: YouTube Cinematic Pilot Media/Distribution Retrospective

Note: this remains valid secondary media/distribution evidence, but the current primary Phase 1.5 media/distribution lane record is [`2026-04-22_confidence-debt_media-distribution-retrospective.md`](./2026-04-22_confidence-debt_media-distribution-retrospective.md).

This retrospective proof record reconstructs session `019db567-5fb0-7933-8487-ec24ea0ac512` as Phase 1.5 media/distribution evidence.

It is not a clean cold-start proof. It began as an experiment discussion in Plan Mode, expanded into tracked workflow and script work, then crossed into real NotebookLM and YouTube channel mutations. The source trace is strong enough to document what happened and why it matters, but not strong enough to treat the run as a minimal-glue retained proof.

## Run Identity

| Field | Value |
| :--- | :--- |
| Run id | `2026-04-22_youtube-cinematic-pilot_media-distribution-retrospective` |
| Package or idea | Idea-driven experiment across `neural-architectures/neural-architecture-design-as-a-compositional-32e`, `autonomy-tax`, and `illusion-of-swarm` |
| Operator / harness | Codex desktop thread |
| Model or runtime | Codex |
| Source thread or trace | Session `019db567-5fb0-7933-8487-ec24ea0ac512` |
| Start boundary | User asked to evaluate and help run a new YouTube cinematic experiment because longform, slide, and TL;DR lanes were underperforming |
| Stop boundary | Experiment workflow and scripts were implemented, two cinematic videos and four Shorts were uploaded/scheduled, and the remaining `illusion-of-swarm` cinematic was blocked by NotebookLM quota |
| Boundary type | `publish` |
| Phase 1.5 proof class | `media-distribution` |

## Starting Prompt

```text
ok i have a long running process for you. i need to try a new experiment on youtube to see if i get more tracktion and i need your help. but first i want to discuss this. my longform videos, the one we enrich we slides, as well as the normal tl;dr videos we create with the appropriate text prompt have little tracktion. i created shorts from the long form videos with slides, but the tracktion is also slow. Cinematic videos, the ones we created as one offs in a couple of publications only and that
```

## Task Boundary

- Objective: evaluate and then run a cinematic-video experiment lane for YouTube that could improve acquisition relative to the current longform/TL;DR stack
- Explicit non-goals: do not treat cinematic as proven by default, do not roll it out blindly across the whole repo, do not mutate unrelated publication workflows
- Stop condition: a reusable experiment lane exists, live channel scheduling is coherent, package-local upload reports exist, and unresolved blockers are explicit
- External side effects allowed: NotebookLM artifact creation, YouTube uploads, playlist mutation, scheduling changes, package-local upload reports, tracked experiment/workflow/script changes
- External side effects forbidden: unrelated publication mutations, silent queue collisions, unsupported claims that cinematic is already the winning format
- Required approval before mutation: yes for channel mutation; the session repeatedly narrowed choices before uploads and schedule changes

## Manual Glue Score

| Measure | Count / Rating | Notes |
| :--- | :---: | :--- |
| User prompts after start | High | The session contains `31` user messages and multiple strategic corrections. |
| Repo explanations from user | Low | The repo surface was mostly discoverable from tracked docs and scripts. |
| Manual command executions by user | Some | NotebookLM UI interaction and experiment steering occurred alongside repo automation. |
| Permission or sandbox handoffs | Low | No sandbox approval issues, but NotebookLM and YouTube auth/readiness checks mattered. |
| Repo-discovery failures | Low | The harness found the relevant YouTube and NotebookLM surfaces. |
| Invented artifacts or unsupported claims | Low | The run kept grounding itself in channel state, package artifacts, and upload reports. |
| Approval-boundary mistakes | Low | The run asked for strategic choices before stepping on an existing Shorts queue. |

Suggested closure rating: `PARTIAL`.

## Execution Summary

1. The harness inspected the tracked YouTube, NotebookLM, and Shorts workflows plus the existing channel/tooling surface.
2. It pulled read-only channel state, playlist inventory, upload history, and existing Shorts queue data using repo-local YouTube API scripts.
3. It concluded the repo could operationalize a cinematic pilot, but the experiment was analytically under-instrumented.
4. It designed and implemented a reusable experiment lane:
   - `workflows/youtube-cinematic-pilot/README.md`
   - `experiments/youtube-cinematic-pilot/`
   - `scripts/upload_publication_cinematic.py`
   - extensions to `scripts/upload_publication_shorts.py`
5. It then ran real channel-side work:
   - uploaded `Neural Architecture` cinematic
   - uploaded `The Autonomy Tax` cinematic
   - recovered or checked captions
   - uploaded/scheduled related Shorts
   - repaired a transient playlist issue
   - accelerated part of the rollout on April 22, 2026
6. `Illusion of the Swarm` remained blocked by NotebookLM’s daily cinematic quota, and that blocker was explicitly recorded rather than hand-waved.

## Evidence And State Used

| Evidence | Why It Mattered | Freshness / Provenance |
| :--- | :--- | :--- |
| [`workflows/youtube-cinematic-pilot/README.md`](../../workflows/youtube-cinematic-pilot/README.md) | Canonical tracked workflow created by the run. | Tracked workflow surface from this rollout. |
| [`experiments/youtube-cinematic-pilot/pilot_manifest.yaml`](../../experiments/youtube-cinematic-pilot/pilot_manifest.yaml) | Experiment contract across publications. | Tracked experiment coordination surface. |
| [`experiments/youtube-cinematic-pilot/release_calendar.yaml`](../../experiments/youtube-cinematic-pilot/release_calendar.yaml) | Chronological rollout and scheduling state. | Tracked experiment coordination surface. |
| [`experiments/youtube-cinematic-pilot/metrics/pilot-run-2026-04-22.md`](../../experiments/youtube-cinematic-pilot/metrics/pilot-run-2026-04-22.md) | Consolidated live run ledger and blockers. | Tracked experiment metric/report artifact. |
| [`publications/neural-architectures/neural-architecture-design-as-a-compositional-32e/artifacts/video/neural_architecture_design_cinematic_upload_report.json`](../../publications/neural-architectures/neural-architecture-design-as-a-compositional-32e/artifacts/video/neural_architecture_design_cinematic_upload_report.json) | Confirms real cinematic upload state and readback. | Package-local upload report. |
| [`publications/neural-architectures/neural-architecture-design-as-a-compositional-32e/artifacts/video/shorts/cinematic_shorts_upload_report.json`](../../publications/neural-architectures/neural-architecture-design-as-a-compositional-32e/artifacts/video/shorts/cinematic_shorts_upload_report.json) | Confirms real Shorts upload/schedule/readback state. | Package-local upload report. |
| [`publications/autonomy-tax/artifacts/video/autonomy_tax_cinematic_upload_report.json`](../../publications/autonomy-tax/artifacts/video/autonomy_tax_cinematic_upload_report.json) | Confirms real cinematic upload state for the second publication. | Package-local upload report. |
| Session trace `019db567-5fb0-7933-8487-ec24ea0ac512` | Provides the actual prompt glue, API reads, choices, and mutation sequence. | Source trace outside repo, reconstructable. |

## Failure Or Friction Review

| Problem | Class | Corrective Direction |
| :--- | :--- | :--- |
| The run started as broad experiment discussion rather than a bounded proof prompt. | `context overload` | Future media/distribution proofs should start from one bounded prompt and one explicit package/experiment target. |
| The run required many user interactions and five `request_user_input` decision points. | `model discipline` | Keep Phase 1.5 proofs narrower than strategic pilot design sessions. |
| The experiment mixed tracked workflows, new experiment surfaces, and live channel operations. | `workflow-doc gap` | Add a shorter proof-oriented variant or checklist for media/distribution runs. |
| NotebookLM daily cinematic quota blocked one lane. | `sandbox/auth` | Treat quota and external platform ceilings as first-class proof annotations. |

## Phase 1.5 Gate Answers

| Gate | Answer | Evidence |
| :--- | :---: | :--- |
| Could the harness determine the next valid action without repo explanation? | `partial` | It discovered the repo surfaces well, but the experiment shape was co-designed with the user. |
| Could it start from an idea or package target and produce bounded outputs with correct logs and approval behavior? | `yes` | It started from an experiment idea and produced tracked workflow, experiment artifacts, upload reports, and real scheduled uploads. |
| Did it succeed with minimal prompt glue and no repo-specific hand-holding beyond the tracked contract? | `no` | The run was operationally successful but highly interactive and not proof-minimal. |

## Final Decision

- Closure rating: `PARTIAL`
- Promote to retained proof? `no`
- If not promoted, where does the routine record live? This retrospective log plus the tracked experiment artifacts and package-local upload reports.
- Required workflow/script/skill hardening: add a current proof-template wrapper for media/distribution runs; keep experiment design separate from proof measurement; preserve channel-state readback in a lighter reusable form.
- Next proof run to attempt: one bounded media/distribution continuation that starts from an explicit target and performs only one approved channel-side step.
