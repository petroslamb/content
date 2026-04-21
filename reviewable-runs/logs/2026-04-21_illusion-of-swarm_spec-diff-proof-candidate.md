# Harness Proof Run Candidate: Illusion Of Swarm Spec-Diff

This lightweight Reviewable Runs record captures the first `spec-diff`-style run outside `publications/literate-workflow-programming`.

The run caught real evidence-orientation drift in `publications/illusion-of-swarm`, exposed one validator assumption during development, repaired only the package paper index, and left the published essay and lifecycle status unchanged.

## Run Identity

| Field | Value |
| :--- | :--- |
| Run id | `2026-04-21_illusion-of-swarm_spec-diff-proof-candidate` |
| Package or idea | `publications/illusion-of-swarm` |
| Operator / harness | Codex desktop thread |
| Model or runtime | Codex |
| Source thread or trace | Current local thread; raw transcript not exported into the repo |
| Start boundary | User asked to implement the next-step plan: synthesis first, then one external `spec-diff` proof |
| Stop boundary | Package-local validator created, pre/post reports retained, index orientation repaired, proof candidate recorded |
| Boundary type | `explicit non-approval reason` |
| Proof class | `package-local evidence-surface validation` |

## Starting Prompt

```text
PLEASE IMPLEMENT THIS PLAN:
# Next Steps Plan: Synthesis First, Then One External Spec-Diff Proof
```

## Allowed Context

- `AGENTS.md` / local operator instructions for `/Users/petros/Projects/content`
- Package status and draft: `publications/illusion-of-swarm/status.yaml`, `publications/illusion-of-swarm/the-illusion-of-the-swarm.md`
- Package evidence surface: `publications/illusion-of-swarm/papers/`, `publications/illusion-of-swarm/artifacts/`
- Prior prototype shape: `publications/literate-workflow-programming/scripts/spec_diff_paper_intake.py`
- Reviewable Runs guidance implied by the existing package-local proof-candidate records

## Task Boundary

- Objective: Test whether a `spec-diff`-style validator finds useful drift in a second publication package with different evidence conventions.
- Explicit non-goals: Do not edit the published essay, download missing papers, mark lifecycle stages done, create a root validator, or update `phased-strategy/`.
- Allowed repair: Improve `publications/illusion-of-swarm/papers/index.md` so existing local evidence and known gaps are visible.
- Stop condition: Retain pre/post reports and state whether the second-package threshold is met.
- External side effects allowed: none.
- External side effects forbidden: publishing, platform mutation, paper download, Git mutation, lifecycle mutation.

## Command Surface Used

```bash
.venv/bin/python publications/illusion-of-swarm/scripts/spec_diff_paper_intake.py --write-report publications/illusion-of-swarm/artifacts/spec-diff/paper-intake-preindex.json
.venv/bin/python publications/illusion-of-swarm/scripts/spec_diff_paper_intake.py --write-report publications/illusion-of-swarm/artifacts/spec-diff/paper-intake-latest.json
```

The final verification pass for the full implementation also ran the requested package audits and repo checks.

## Manual Glue Score

| Measure | Count / Rating | Notes |
| :--- | :---: | :--- |
| User prompts after start | 0 | The run proceeded from the plan prompt. |
| Repo explanations from user | 0 | The needed package and proof boundary were in the plan and tracked files. |
| Manual command executions by user | 0 | Codex ran the local commands directly. |
| Permission or sandbox handoffs | 0 | No external mutation or approval boundary was crossed. |
| Repo-discovery failures | 0 | The package draft, status, evidence surface, and prior validator shape were discoverable. |
| Invented artifacts or unsupported claims | 0 | Findings are based on local files and retained JSON reports. |
| Approval-boundary mistakes | 0 | No paper downloads, publication edits, lifecycle marks, staging, commits, or pushes occurred. |

Suggested closure rating: `PASS` as a second-package proof candidate; `NO PROMOTION` as a repo-wide validator requirement.

## Execution Summary

1. Created `publications/illusion-of-swarm/scripts/spec_diff_paper_intake.py` with the same CLI shape as the literate-workflow prototype.
2. Ran the validator before repair and retained `paper-intake-preindex.json`.
3. The pre-repair report found 19 warnings: a thin index, mixed storage conventions not called out, 12 local evidence files not indexed, and 5 cited arXiv IDs with no local evidence or artifact record.
4. During the first dry check, the validator over-counted arXiv IDs from reference lists in local paper text. The identity scan was narrowed to the file name/header area before retaining the pre/post reports.
5. Repaired only `papers/index.md`, enumerating local PDFs, root markdown, root text captures, artifact support, and unresolved draft-citation gaps.
6. Reran the validator and retained `paper-intake-latest.json`; it passed with zero findings.

## Evidence And State Used

| Evidence | Why It Mattered | Freshness / Provenance |
| :--- | :--- | :--- |
| `publications/illusion-of-swarm/status.yaml` | Confirms `paper_intake.done: true` and names the canonical draft. | Existing package state. |
| `publications/illusion-of-swarm/papers/index.md` | The repaired orientation surface for local paper evidence and gaps. | Updated during this run. |
| `publications/illusion-of-swarm/papers/` | Local evidence files: PDFs, root markdown, and root text captures. | Existing local evidence. |
| `publications/illusion-of-swarm/artifacts/` | alphaXiv artifact records for eight draft-cited arXiv IDs. | Existing package artifacts. |
| `publications/illusion-of-swarm/artifacts/spec-diff/paper-intake-preindex.json` | Retained pre-repair report. | Generated on 2026-04-21. |
| `publications/illusion-of-swarm/artifacts/spec-diff/paper-intake-latest.json` | Retained post-repair report. | Generated on 2026-04-21. |

## Verification

| Check | Result | Notes |
| :--- | :---: | :--- |
| Pre-repair `spec-diff` | `PASS_WITH_WARNINGS` | 0 blocking, 19 warnings. |
| Post-repair `spec-diff` | `PASS` | 12 local evidence files, 13 cited arXiv IDs, 8 artifact-supported IDs, 5 classified gaps, 0 findings. |
| Published essay untouched | `PASS` | The canonical draft was read for citation IDs only. |
| Lifecycle status untouched | `PASS` | `status.yaml` was not modified in this pass. |
| Paper intake expansion avoided | `PASS` | Missing citations were classified as gaps, not downloaded. |

## Approval And Boundary Behavior

- Was approval required? No.
- Was approval obtained before the controlled action? The user explicitly requested the plan implementation.
- If approval was not required, why not? The run created local validation artifacts and repaired a package index only.
- Did the harness stop at the correct boundary? Yes. It stopped after the second-package proof candidate and did not promote to `phased-strategy/`.
- If blocked by sandbox/auth/network, did it ask for narrow permission or provide exact user-exec commands? Not applicable.

## Failure Or Friction Review

| Problem | Class | Corrective Direction |
| :--- | :--- | :--- |
| The first validator draft treated reference-list arXiv IDs inside local papers as local evidence for cited draft IDs. | `validator assumption` | Identity detection now scans the file name/header area instead of broad paper text. |
| The package had mixed local evidence conventions with only a generic index. | `orientation drift` | The index now names root text captures, root markdown, PDFs, artifacts, and gaps explicitly. |
| Five cited papers still lack local files or alphaXiv artifacts in this package. | `evidence gap` | Leave them classified until a future paper-intake pass deliberately captures them. |

## Final Decision

- Closure rating: `PASS` as the requested second-package `spec-diff` proof candidate.
- Did the validator catch drift? `yes`.
- Did it merely confirm consistency? `no`; it found real orientation drift before repair.
- Did it expose a bad validator assumption? `yes`; broad arXiv-ID scanning was tightened before retaining reports.
- Does this meet the second-package threshold? `yes`, as a candidate.
- Promote to retained proof or root validator? `no`, not in this pass.
- Update `phased-strategy/`? `no`; the result supports a future promotion decision but does not require changing phase or proof requirements today.
