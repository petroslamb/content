# Harness Proof Run Candidate: Literate Workflow Programming Spec-Diff

This is a lightweight Reviewable Runs record for testing whether the package-local `spec-diff` prototype adds evidence useful to Phase 1.5 proof-run evaluation.

It is not a retained proof artifact. The underlying `spec-diff` prototype was created before this wrapper run, so this record evaluates review value and boundary clarity rather than claiming a fresh autonomous implementation proof.

## Run Identity

| Field | Value |
| :--- | :--- |
| Run id | `2026-04-21_literate-workflow-programming_spec-diff-proof-candidate` |
| Package or idea | `publications/literate-workflow-programming` |
| Operator / harness | Codex desktop thread |
| Model or runtime | Codex |
| Source thread or trace | Current local thread; raw transcript not exported into the repo |
| Start boundary | User asked to run the proof-run wrapper around the existing `spec-diff` work |
| Stop boundary | This candidate record written under `reviewable-runs/logs/` and repo checks rerun |
| Boundary type | `explicit non-approval reason` |
| Phase 1.5 proof class | `other`: proof-run evaluation of a package-local validator experiment |

## Starting Prompt

```text
ok sure run it. however the previous use of spec-diff was directly when it was created. lets see however if reviewable runs finds something of value
```

## Allowed Context

- `AGENTS.md` / local operator instructions: user-provided thread context for `/Users/petros/Projects/content`
- `README.md`: repo orientation implied by local instructions; not reread during this wrapper run
- `harness_contract.yaml`: used indirectly through `stage:next` and existing harness checks
- `harness_policy.yaml`: used indirectly through harness checks and stage boundary metadata
- Package README / `status.yaml`: `publications/literate-workflow-programming/README.md`, `publications/literate-workflow-programming/status.yaml`
- Workflow docs: `workflows/paper-intake/README.md`, `workflows/alphaxiv-research/README.md`
- Skills: no new skill execution; prior package work references `markitdown-paper-intake` and `alphaxiv`
- Scripts / npm entrypoints: `scripts/audit_package.py`, `scripts/next_action.py`, `scripts/check_reviewable_run_logs.py`, `scripts/check_harness.py`, `scripts/check_repo_links.py`, package-local `scripts/spec_diff_paper_intake.py`

## Task Boundary

- Objective: Evaluate whether wrapping the existing package-local `spec-diff` experiment in a Reviewable Runs proof-run record exposes useful Phase 1.5 evidence.
- Explicit non-goals: Do not promote `spec-diff` to a repo-wide validator. Do not update `phased-strategy/`. Do not claim a fresh end-to-end autonomous implementation proof.
- Stop condition: Fresh `spec-diff` report, next-action read, package audit, and validation checks are recorded with an honest proof-candidate decision.
- External side effects allowed: none.
- External side effects forbidden: publishing, platform mutation, package status mutation, strategy gate mutation.
- Required approval before mutation: not required for local documentation and validation artifacts in this bounded package/review surface.

## Command Surface Used

```bash
.venv/bin/python publications/literate-workflow-programming/scripts/spec_diff_paper_intake.py --format json --write-report publications/literate-workflow-programming/artifacts/spec-diff/paper-intake-latest.json
npm run --silent stage:next -- --package literate-workflow-programming --format json
.venv/bin/python scripts/audit_package.py --package literate-workflow-programming
npm run check:repo-links
npm run check:harness
npm run check:reviewable-runs
git diff --check
```

## Manual Glue Score

| Measure | Count / Rating | Notes |
| :--- | :---: | :--- |
| User prompts after start | 0 | The wrapper run proceeded after the quoted prompt. |
| Repo explanations from user | 1 | The user supplied the important caveat that prior `spec-diff` use happened when it was created. |
| Manual command executions by user | 0 | Codex ran local commands directly. |
| Permission or sandbox handoffs | 0 | No network, browser, or external-service permission was needed. |
| Repo-discovery failures | 0 | The package, Reviewable Runs guidance, and validation entrypoints were discoverable. |
| Invented artifacts or unsupported claims | 0 | The record explicitly limits what the run proves. |
| Approval-boundary mistakes | 0 | No external or destructive boundary was crossed. |

Suggested closure rating: `PARTIAL`.

The run is review-useful, but it is not a Phase 1.5 autonomy proof because the main implementation happened before this wrapper run.

## Execution Summary

1. Read the Reviewable Runs front door, logs guidance, proof-promotion guidance, playbook, real-run index, and run-review checklist.
2. Reran the package-local `spec-diff` prototype and refreshed the latest JSON artifact.
3. Queried the package next action through the harness command surface.
4. Ran the package structural audit and repo validation checks.
5. Wrote this proof-run candidate as a lightweight log, with an explicit decision not to promote it yet.

## Evidence And State Used

| Evidence | Why It Mattered | Freshness / Provenance |
| :--- | :--- | :--- |
| `publications/literate-workflow-programming/research-notes/2026-04-20-spec-diff-experiment.md` | Defines the experiment, success criteria, and non-goals. | Package research note, updated before this wrapper run. |
| `publications/literate-workflow-programming/scripts/spec_diff_paper_intake.py` | Implements the drift checks under evaluation. | Package-local untracked prototype. |
| `publications/literate-workflow-programming/artifacts/spec-diff/paper-intake-latest.json` | Fresh result of the prototype: pass, 0 findings. | Regenerated on 2026-04-21 at 17:25 EEST. |
| `publications/literate-workflow-programming/papers/index.md` | Contains the ignored-PDF note that fixed the first semantic drift. | Uncommitted package edit. |
| `reviewable-runs/logs/2026-04-20_22-57-15_literate-workflow-programming_paper_intake_launch-pack.json` | Shows the paper-intake launch-pack boundary. | Existing v2 lightweight run log. |
| `reviewable-runs/logs/2026-04-20_23-10-05_literate-workflow-programming_paper_intake_mark-done.json` | Shows the lifecycle mark-done boundary for paper intake. | Existing v2 lightweight run log. |
| `reviewable-runs/templates/harness-proof-run-template.md` | Supplies the Phase 1.5 proof-run evaluation shape. | Tracked template. |

## Verification

| Check | Result | Notes |
| :--- | :---: | :--- |
| `spec-diff` prototype | `PASS` | 7 indexed papers, 7 local PDFs, 7 markdown files, 6 metadata files, 0 blocking findings, 0 warnings. |
| `npm run --silent stage:next -- --package literate-workflow-programming --format json` | `PARTIAL` | Correctly identifies `research` as next stage, but reports guided `launch_mode: none` as not directly executable in Phase 1.5. |
| `.venv/bin/python scripts/audit_package.py --package literate-workflow-programming` | `PASS` | README, evidence path, artifacts, archive, and live draft link all pass. |
| `npm run check:repo-links` | `PASS` | Repo links OK. |
| `npm run check:harness` | `PASS` | Harness validation passed. |
| `npm run check:reviewable-runs` | `PASS` | Current JSON logs validate; this markdown candidate is a lightweight note outside that JSON schema. |
| `git diff --check` | `PASS` | No whitespace errors. |

## Approval And Boundary Behavior

- Was approval required? No.
- Was approval obtained before the controlled action? The user explicitly asked to run the proof-run wrapper.
- If approval was not required, why not? The run only touched local review documentation and refreshed a package-local report artifact. It did not publish, submit, push, stage, commit, mark a lifecycle stage done, or mutate an external service.
- Did the harness stop at the correct boundary? Yes: it stopped at a local proof-candidate record and validation summary.
- If blocked by sandbox/auth/network, did it ask for narrow permission or provide exact user-exec commands? Not applicable.

## Failure Or Friction Review

| Problem | Class | Corrective Direction |
| :--- | :--- | :--- |
| The valuable `spec-diff` finding happened during prototype creation, before this proof wrapper. | `proof-slice gap` | Treat this as a secondary candidate only. Use a future fresh intake or another package to test whether `spec-diff` catches drift during an independently bounded run. |
| `stage:next` can identify the next stage, but guided `launch_mode: none` remains not directly executable. | `workflow-doc gap` | Add better launch modes or validator hooks only after repeated runs show this reduces prompt glue. |
| The current `spec-diff` script is package-local and hard-coded. | `script gap` | Keep it package-local until another package or stage needs the same shape. Then consider a generalized validator surface. |

## Phase 1.5 Gate Answers

| Gate | Answer | Evidence |
| :--- | :---: | :--- |
| Could the harness determine the next valid action without repo explanation? | `partial` | `stage:next` correctly returned `research`, but also reported guided `launch_mode: none` as not directly executable. |
| Could it start from an idea or package target and produce bounded outputs with correct logs and approval behavior? | `partial` | It produced this bounded wrapper and refreshed the `spec-diff` report, but it did not perform the original implementation or a fresh paper-intake stage. |
| Did it succeed with minimal prompt glue and no repo-specific hand-holding beyond the tracked contract? | `partial` | The tracked docs supplied most context, but the user's caveat about prior `spec-diff` timing materially changed the proof interpretation. |

## Final Decision

- Closure rating: `PARTIAL`
- Promote to retained proof? `no`
- If not promoted, where does the routine record live? `reviewable-runs/logs/2026-04-21_literate-workflow-programming_spec-diff-proof-candidate.md`
- Required workflow/script/skill hardening: none immediately. The useful hardening candidate is a future validator hook that lets package-local `spec-diff` reports appear in guided-stage launch packs or proof-run verification.
- Next proof run to attempt: run `spec-diff` during a fresh P1 intake or on a different publication package with known evidence drift, then compare whether the Reviewable Runs wrapper catches anything beyond the validator output.
