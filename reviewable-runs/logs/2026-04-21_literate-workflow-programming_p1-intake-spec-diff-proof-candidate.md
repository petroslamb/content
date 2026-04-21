# Harness Proof Run Candidate: P1 Intake With Spec-Diff

This lightweight Reviewable Runs record captures the fresh P1 paper-intake run for `publications/literate-workflow-programming` and evaluates whether `spec-diff` added review value during the run.

It is a stronger candidate than the earlier wrapper because `spec-diff` ran before the paper index was repaired, caught real intake drift, and then verified the repaired final state.

## Run Identity

| Field | Value |
| :--- | :--- |
| Run id | `2026-04-21_literate-workflow-programming_p1-intake-spec-diff-proof-candidate` |
| Package or idea | `publications/literate-workflow-programming` |
| Operator / harness | Codex desktop thread |
| Model or runtime | Codex |
| Source thread or trace | Current local thread; raw transcript not exported into the repo |
| Start boundary | User asked Codex to do the next moves after the first wrapper showed only limited proof value |
| Stop boundary | P1 papers intaken, pre-index drift captured, final `spec-diff` passed, proof candidate recorded |
| Boundary type | `explicit non-approval reason` |
| Phase 1.5 proof class | `research-heavy` |

## Starting Prompt

```text
ok do the next moves
```

## Allowed Context

- `AGENTS.md` / local operator instructions: user-provided thread context for `/Users/petros/Projects/content`
- Package README / `status.yaml`: `publications/literate-workflow-programming/README.md`, `publications/literate-workflow-programming/status.yaml`
- Workflow docs: `workflows/paper-intake/README.md`, `workflows/alphaxiv-research/README.md`
- Skills: `markitdown-paper-intake`, `alphaxiv`
- Scripts / npm entrypoints: `.venv/bin/alphaxiv`, `.venv/bin/markitdown`, package-local `scripts/spec_diff_paper_intake.py`, `npm run check`
- Reviewable Runs guidance: `reviewable-runs/PLAYBOOK.md`, `reviewable-runs/templates/harness-proof-run-template.md`

## Task Boundary

- Objective: Use the queued P1 paper intake as a fresh test of whether package-local `spec-diff` finds reviewable state drift during real package work.
- Explicit non-goals: Do not publish, push, stage, commit, or promote `spec-diff` to a repo-wide validator.
- Stop condition: P1 papers are stored locally, converted, indexed, and verified by `spec-diff`; the proof candidate states whether the wrapper added value.
- External side effects allowed: public alphaXiv/PDF retrieval only.
- External side effects forbidden: Substack, YouTube, GitHub mutation, package publication, strategy gate mutation.
- Required approval before mutation: not required for local package paper-intake edits and local validation artifacts.

## Command Surface Used

```bash
.venv/bin/alphaxiv paper show --json <paper-id>
.venv/bin/alphaxiv paper pdf download <paper-id> <target-pdf>
.venv/bin/markitdown <target-pdf> -o <target-md>
.venv/bin/python publications/literate-workflow-programming/scripts/spec_diff_paper_intake.py --format json --write-report publications/literate-workflow-programming/artifacts/spec-diff/paper-intake-p1-preindex.json
.venv/bin/python publications/literate-workflow-programming/scripts/spec_diff_paper_intake.py --format json --write-report publications/literate-workflow-programming/artifacts/spec-diff/paper-intake-latest.json
npm run check
git diff --check
```

## Manual Glue Score

| Measure | Count / Rating | Notes |
| :--- | :---: | :--- |
| User prompts after start | 0 | The run proceeded from the quoted prompt. |
| Repo explanations from user | 0 | The required package/workflow context was discoverable from tracked files and prior thread context. |
| Manual command executions by user | 0 | Codex ran the local commands directly. |
| Permission or sandbox handoffs | 0 | PDF retrieval and local conversion did not require handoff. |
| Repo-discovery failures | 0 | The package queue, paper-intake workflow, alphaXiv skill, and `spec-diff` artifacts were found. |
| Invented artifacts or unsupported claims | 0 | The proof candidate is scoped to observed files and command results. |
| Approval-boundary mistakes | 0 | The run stayed inside local package evidence and validation surfaces. |

Suggested closure rating: `PASS` as a package-local proof candidate; `PARTIAL` for Phase 1.5 closure because it covers one guided research/paper-intake slice, not three proof classes.

## Execution Summary

1. Loaded the paper-intake and alphaXiv workflow guidance.
2. Retrieved metadata and PDFs for the six queued P1 papers.
3. Converted the six PDFs with the repo-local `markitdown` binary.
4. Ran `spec-diff` before updating `papers/index.md`; it produced 24 warnings.
5. Fixed a prototype version-normalization bug that had initially missed `2510.04173v4` as a queued-paper conflict.
6. Updated `papers/index.md` and `status.yaml`.
7. Reran `spec-diff`; the latest report passed with zero findings.
8. Recorded the proof-candidate result and reran repo checks.

## Evidence And State Used

| Evidence | Why It Mattered | Freshness / Provenance |
| :--- | :--- | :--- |
| `publications/literate-workflow-programming/papers/index.md` | The authoritative package paper inventory and queue. | Updated during this run. |
| `publications/literate-workflow-programming/artifacts/spec-diff/paper-intake-p1-preindex.json` | Captures drift after files landed but before index repair. | Generated on 2026-04-21. |
| `publications/literate-workflow-programming/artifacts/spec-diff/paper-intake-latest.json` | Captures final consistent state after repair. | Regenerated on 2026-04-21. |
| `publications/literate-workflow-programming/scripts/spec_diff_paper_intake.py` | Validator under test; also received the version-normalization fix. | Package-local prototype. |
| `publications/literate-workflow-programming/status.yaml` | Lifecycle state and `paper_intake.last_updated`. | Updated to 2026-04-21. |
| Six new metadata files under `papers/metadata/` | Deterministic alphaXiv metadata for P1 entries. | Retrieved during this run. |
| Six new markdown files under `papers/markdown/` | Converted local reading surface for P1 entries. | Generated during this run. |

## Verification

| Check | Result | Notes |
| :--- | :---: | :--- |
| Pre-index `spec-diff` | `PASS_WITH_WARNINGS` | 24 warnings: unindexed PDFs, markdown, metadata, and queued/local overlap. |
| Final `spec-diff` | `PASS` | 13 indexed papers, 13 local PDFs, 13 markdown files, 12 metadata files, 11 queued papers, 0 findings. |
| `npm run check` | `PASS` | Harness, reviewable-runs, repo-links, and alphaXiv discussion checks passed. |
| `git diff --check` | `PASS` | No whitespace errors. |

## Approval And Boundary Behavior

- Was approval required? No.
- Was approval obtained before the controlled action? The user asked to proceed with the next moves.
- If approval was not required, why not? The run performed local evidence intake and validation only. It did not publish, submit, push, stage, commit, or mutate an external account.
- Did the harness stop at the correct boundary? Yes. The run stopped after local intake, validation, and proof-candidate documentation.
- If blocked by sandbox/auth/network, did it ask for narrow permission or provide exact user-exec commands? Not applicable.

## Failure Or Friction Review

| Problem | Class | Corrective Direction |
| :--- | :--- | :--- |
| The first pre-index run exposed a missed queue conflict for `2510.04173v4`. | `script gap` | Fixed by normalizing arbitrary numeric arXiv version suffixes. |
| Guided paper intake still depends on Codex choosing the intermediate `spec-diff` checkpoint. | `workflow-doc gap` | Consider adding package-local validator hooks to launch packs only after another run confirms repeat value. |
| P1 PDF conversions have extraction noise. | `package-local gap` | Keep conversion notes in `papers/index.md`; use PDFs as source of truth when exact wording matters. |

## Phase 1.5 Gate Answers

| Gate | Answer | Evidence |
| :--- | :---: | :--- |
| Could the harness determine the next valid action without repo explanation? | `yes` | The package queue and prior `stage:next` state pointed to continued research/paper intake. |
| Could it start from a package target and produce bounded outputs with correct logs and approval behavior? | `yes` | P1 papers were intaken, drift was captured and repaired, and no external mutation boundary was crossed. |
| Did it succeed with minimal prompt glue and no repo-specific hand-holding beyond the tracked contract? | `partial` | The run needed no extra prompts, but the intermediate `spec-diff` checkpoint is still operator judgment rather than a declared workflow hook. |

## Final Decision

- Closure rating: `PASS` as a fresh package-local proof candidate.
- Promote to retained proof? `no`, not yet. Keep it as a strong secondary candidate unless a later run shows the same pattern outside this package.
- If not promoted, where does the routine record live? `reviewable-runs/logs/2026-04-21_literate-workflow-programming_p1-intake-spec-diff-proof-candidate.md`
- Required workflow/script/skill hardening: consider a validator-hook field in guided stage launch packs after one more fresh run.
- Next proof run to attempt: apply `spec-diff` or a similar expected-state validator to a different publication package with known evidence drift.
