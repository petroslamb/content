# Phase 1 / 1.5 Closure Checklist

Snapshot date: 2026-04-17

Status legend:

- `DONE`: implemented and verified enough to count toward phase closure
- `PARTIAL`: implemented in part, or true only with caveats
- `OPEN`: not yet implemented or not yet proven
- `INTENTIONAL`: not a gap; kept outside scope by design

## Snapshot

| Surface | Current State |
| :--- | :--- |
| Workflow docs | 16 canonical workflow/operations docs, plus the workflow and skills indexes |
| Skill bundles | 10 tracked repo-local skills under `workflows/skills/` |
| Root scripts | Root scripts contain no package-specific exceptions; package/series adapters live under owning packages or skills |
| Harness contract | `harness_contract.yaml` present |
| Harness policy | `harness_policy.yaml` present |
| Harness check | `npm run check:harness` passes as of the latest workflow refactor |
| Reviewable run log check | `npm run check:reviewable-runs` validates v2 lightweight lifecycle logs and launch packs |
| Repo-link check | `npm run check:repo-links` passes |
| Strategic read | Phase 1 is closed; Phase 1.5 is built but not proof-run cleared |

## Phase 1 - The Clean Machine

Goal from the strategy document:

> Zero orphan scripts. One interface. Any article can be run start-to-finish by an agent - no hand-holding.

### Summary Verdict

`DONE`, under clarified Phase 1 scope.

Phase 1 is closed as internal repo normalization. The repo has moved from scattered tools into a structured operating environment with package manifests, lifecycle scripts, workflow docs, root-script hygiene, package-orientation checks, and a harness-facing command surface.

The original strategy sentence "any article can be run start-to-finish by an agent" is now interpreted as the next autonomy proof layer. It is not a remaining Phase 1 blocker. It belongs to Phase 1.5 proof runs and, where operator-shell support is required, Phase 1.6.

### Gate Criteria

| Gate | Status | Evidence | Remaining Work |
| :--- | :---: | :--- | :--- |
| Describe the status of every publication in one command | `DONE` | `scripts/check_status.py`; `npm run status`; package `status.yaml` manifests | Keep manifests current as packages move or split |
| Let another agent or future operator pick up a half-finished package and know where it is | `DONE` | Package READMEs, `status.yaml`, workflow docs, `scripts/next_action.py`, harness contract, and `publication-package-orientation-audit-2026-04-17.md` | Keep package orientation green as older packages move or split |
| Zero scripts that mention a specific essay name | `DONE` | The hard package-specific root scripts were removed or moved out of root `scripts/`; remaining package names in root scripts are examples, migration checks, or generic package arguments | Keep this gate green when adding future automation |

### Milestones

| Milestone | Status | Evidence | Remaining Work |
| :--- | :---: | :--- | :--- |
| M1.1 Kill the root scripts | `DONE` | Root ad hoc scripts were moved, removed, or moved under their owning umbrella package; `scripts/README.md` now states that no package-specific root-script exceptions remain | Keep package-specific utilities package-local unless they are generalized |
| M1.2 Publication lifecycle manifest | `DONE` | `status.yaml` layer; `scripts/check_status.py`; `npm run status` | Keep manifests synchronized when package taxonomy changes |
| M1.3 Generic `run` interface | `DONE` | `scripts/run_stage.py`; `npm run stage:resolve`; `npm run stage:run` | Continue improving guided-stage launch packs rather than pretending all stages are fully automated |
| M1.4 Reviewable Runs integration | `DONE` | `run_stage.py` writes v2 lightweight logs; harness launch packs use v2 schema; `npm run check:reviewable-runs` validates the current log layer | Full proof packets remain selective retained artifacts, not automatic paperwork for every routine run |

### Phase 1 Closure Items

1. Classify or eliminate package-specific script exceptions. `DONE`.
   - `scripts/stitch_binding_gap_slides.py` was removed.
   - `scripts/sync_operating_agents_substack.py` was moved to `publications/autonomous-agents/scripts/`.
   - `scripts/update_initial_status.py` was removed.
   - Generic wrappers with package examples in help text remain acceptable if they take `--package`.

2. Run a publication package orientation audit. `DONE`; see `phased-strategy/publication-package-orientation-audit-2026-04-17.md`.
   - Confirm every active leaf package has a useful README, `status.yaml`, live draft pointer, artifact surface, and evidence surface where applicable.
   - Old umbrella packages were normalized with configured evidence paths and top-level artifact/archive orientation surfaces.

3. Decide the retained-proof boundary. `DONE`.
   - Routine stage logs belong in `reviewable-runs/logs/`.
   - Strong retained proof examples belong in `reviewable-runs/examples/proofs/`.
   - The original Phase 1 wording expected automatic proof pairs for every run; the accepted standard is now tighter v2 lightweight logs plus selective retained proof packets.

4. Resolve or classify repo-link check failures. `DONE`.
   - `npm run check:repo-links` now passes.
   - The stale relative links and absolute local paths were cleaned up during the Phase 1/1.5 closure pass.

## Phase 1.5 - Harness-Native Autonomy

Goal from the strategy document:

> Given an idea and a package target, a general-purpose agent harness such as Codex can discover the repo contract, choose the next valid action, execute bounded work, and leave an inspectable record with minimal human glue.

### Summary Verdict

`PARTIAL`.

The repo now has the main Phase 1.5 machinery: a machine-readable contract, policy boundaries, package initialization, next-action resolution, guided launch packs, harness adapters, and workflow frontmatter. The missing piece is evidence. Phase 1.5 should not be called closed until proof runs show that the system works for real tasks without a long bespoke explanation from the user.

### Gate Criteria

| Gate | Status | Evidence | Remaining Work |
| :--- | :---: | :--- | :--- |
| Harness can determine the next valid action for a package without repo explanation | `PARTIAL` | `harness_contract.yaml`; `scripts/next_action.py`; `npm run stage:next`; workflow frontmatter | Works best for packages with good `status.yaml`; pre-package topic work still depends on workflow judgment |
| Harness can start from an idea or package target and produce bounded outputs with correct logs and approval behavior | `PARTIAL` | `scripts/init_package.py`; `npm run package:init`; `scripts/run_stage.py`; `harness_policy.yaml` | Need measured proof runs across research, editorial, media/release, and sandbox/auth boundaries |
| At least 3 real runs succeeded with minimal prompt glue and no repo-specific hand-holding beyond the tracked contract | `OPEN` | Recent rollouts informed workflow hardening, but they were not captured as formal Phase 1.5 proof runs | Run and score three proof runs using the same evaluation template |

### Milestones

| Milestone | Status | Evidence | Remaining Work |
| :--- | :---: | :--- | :--- |
| M1.5.1 Harness contract surface | `DONE` | `harness_contract.yaml`; `npm run check:harness` | Keep contract synchronized with workflow frontmatter and package scripts |
| M1.5.2 Idea-to-package intake | `DONE` | `scripts/init_package.py`; `npm run package:init` | Test in a real idea-to-research proof run |
| M1.5.3 Next-action resolution | `DONE` | `scripts/next_action.py`; `npm run stage:next -- --package <package>` | Improve package metadata where next action is ambiguous |
| M1.5.4 Guided stage launch packs | `PARTIAL` | `scripts/harness.py`; `run_stage.py` launch-pack behavior; guided workflow frontmatter | Launch packs exist, but the quality of guided execution still depends on the workflow docs and model discipline |
| M1.5.5 Harness adapters | `DONE` | `npm run stage:resolve`; `npm run stage:run`; `npm run stage:next`; `npm run package:init` | Keep adapters as the preferred command surface |
| M1.5.6 Autonomy boundaries and approval rules | `DONE` | `harness_policy.yaml`; sandbox/permission guidance in workflow docs | Continue hardening browser/auth and external side-effect handoffs |
| M1.5.7 Harness proof runs | `OPEN` | No formal three-run closure set yet | Run, score, and retain the proof-run evidence |

### Phase 1.5 Open Items

1. Run three measured proof runs.
   - Research-heavy: `topic-discovery` to `package:init` to alphaXiv research to paper-intake decision.
   - Polish/publish continuation: article polish to release gate to Substack publishing decision without accidental external mutation.
   - Media/distribution: NotebookLM or YouTube production with explicit auth/sandbox handoff handling.

2. Create a proof-run evaluation template. `DONE` as of `reviewable-runs/templates/harness-proof-run-template.md`.
   - Track prompt glue, manual interventions, repo-discovery failures, approval-boundary behavior, command-surface usage, and final outcome.
   - Store routine logs under `reviewable-runs/logs/` and only promote strong examples to `reviewable-runs/examples/proofs/`.

3. Measure guided-stage quality.
   - Confirm weaker models can follow launch packs without inventing artifacts after sandbox failures.
   - Confirm they ask for narrow permission or user-executed commands when blocked.

4. Decide whether topic discovery and release gate become harness stages later.
   - Current status: both are documented decision layers.
   - They should not become status stages unless repeated proof runs show that doing so reduces confusion.

5. Keep Phase 1.6 separate.
   - Persistent browser/session support, generated skill docs, named operator commands, and proof-run evaluation harness belong in Phase 1.6.
   - Do not use Phase 1.6 work to avoid closing the Phase 1.5 proof-run gap.

## Recommended Next Actions

1. Keep Phase 1 closed.
   - New package-specific utilities should live inside the owning package or be generalized before entering root `scripts/`.
   - Series adapters should live under the owning umbrella package or skill bundle.

2. Use the proof-run template under `reviewable-runs/templates/harness-proof-run-template.md`.
   - This is now the missing measurement step between "the harness exists" and "Phase 1.5 is proven."

3. Run the three Phase 1.5 proof runs.
   - Do not score Phase 1.5 as closed until these are done.

4. Keep `npm run check:repo-links` green as package moves continue.
   - The current failure set is closed; future package migrations should run the check before commit.

5. After proof runs, decide whether Phase 1.6 starts.
   - If the main failure is prompt glue, generate skill docs and named operator commands.
   - If the main failure is browser/auth friction, prioritize selective persistent browser support.
   - If the main failure is weak-model compliance, harden launch packs and stop conditions before adding new features.
