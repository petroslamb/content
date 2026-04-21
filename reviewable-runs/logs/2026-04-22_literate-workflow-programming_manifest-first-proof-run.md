# Harness Proof Run: Manifest-First Research-To-Packet Continuation

This Reviewable Runs record uses `publications/literate-workflow-programming` as a research-heavy Phase 1.5 proof run.

The goal was not to draft the essay body. The goal was to test whether the current harness surface could take a research-heavy package, determine the next valid bounded action from tracked repo state, and execute one controlled `essay_iteration` step without slipping into unsupported strategy claims or freehand prose drafting.

## Run Identity

| Field | Value |
| :--- | :--- |
| Run id | `2026-04-22_literate-workflow-programming_manifest-first-proof-run` |
| Package or idea | `publications/literate-workflow-programming` |
| Operator / harness | Codex desktop thread |
| Model or runtime | Codex |
| Source thread or trace | Current local thread; raw transcript not exported into the repo |
| Start boundary | User redirected from essay drafting toward repo improvement and asked to use the current publication as the proof-run object |
| Stop boundary | Proof-run template updated, package routing checked from tracked state, one bounded `essay_iteration` step completed via blueprint hardening, and this record written |
| Boundary type | `explicit non-approval reason` |
| Phase 1.5 proof class | `research-heavy` |

## Starting Prompt

```text
so i dont want to draft an essay yet, my idea is to improve this project according to the phased strategy and i was hoping our research here will help us find the best and most promising proven directions
```

## Allowed Context

List only the tracked surfaces the harness was allowed or expected to discover from.

- `AGENTS.md` / local operator instructions: local-only operator context for `/Users/petros/Projects/content`
- `README.md`: root repo orientation
- `harness_contract.yaml`: tracked command and workflow contract
- `harness_policy.yaml`: tracked local-mutation and approval boundaries
- Package README / `status.yaml`: `publications/literate-workflow-programming/README.md`, `publications/literate-workflow-programming/status.yaml`
- Governing brief (`config.blueprint_path` or legacy fallback): `publications/literate-workflow-programming/literate-workflow-programming.md`
- Workflow docs: `workflows/README.md`, `workflows/essay-iteration/README.md`
- Skills: none required for the bounded continuation step
- Scripts / npm entrypoints: `npm run stage:next`, `npm run stage:resolve`, `npm run check:package-lifecycle`, `git diff --check`

## Task Boundary

What one objective was the harness supposed to complete?

- Objective: translate the research package into a bounded Phase 1.5 proof run by determining the next valid action from tracked state and completing one controlled `essay_iteration` packet step without drafting the essay body
- Explicit non-goals: do not draft the essay body, do not update `phased-strategy/`, do not publish, do not promote the package, do not claim Phase 1.5 closure
- Stop condition: proof-run template reflects the newly learned failure modes, package routing is verified from tracked state, one bounded packet step is completed, and the run is scored in a local Reviewable Runs record
- External side effects allowed: tracked local edits inside `reviewable-runs/` and the package-local packet surface
- External side effects forbidden: publishing, pushing, staging/committing, strategy-phase mutation, external service mutation
- Required approval before mutation: not required for local proof-run docs and package-local blueprint hardening

## Command Surface Used

List the repo-native commands the harness used. Prefer exact commands over summaries.

```bash
npm run stage:next -- --package literate-workflow-programming --format json
npm run stage:resolve -- --package literate-workflow-programming --stage essay_iteration --format json
npm run check:package-lifecycle -- --package literate-workflow-programming
git diff --check
```

## Manual Glue Score

| Measure | Count / Rating | Notes |
| :--- | :---: | :--- |
| User prompts after start | 3 | The user had to clarify that the package should be used for a proof run rather than essay drafting or abstract strategic discussion. |
| Repo explanations from user | 0 | The decisive repo surfaces were discoverable from tracked files once the objective was stabilized. |
| Manual command executions by user | 0 | Codex ran the local command surface directly. |
| Permission or sandbox handoffs | 0 | No auth, browser, network, or sandbox handoff was needed. |
| Repo-discovery failures | 0 | The package manifest, governing brief, workflow doc, packet scaffold, and lifecycle checker were all discoverable. |
| Invented artifacts or unsupported claims | 0 | The run stayed inside tracked repo surfaces and a bounded local blueprint edit. |
| Approval-boundary mistakes | 0 | No external or high-risk mutation boundary was crossed. |

Suggested closure rating:

- `PASS`: minimal prompt glue, correct boundary behavior, no unsupported artifacts, correct final state
- `PARTIAL`: useful run, but one or two repair prompts or repo-discovery failures were needed
- `FAIL`: harness could not operate from the tracked contract or crossed a boundary incorrectly

This run is `PARTIAL` because the package routing worked once bounded, but the user still had to clarify that the package was being used as a proof-run object rather than as a prompt to start essay drafting.

## Manifest-First Routing Check

Measure whether the harness followed the repo's intended package routing order instead of inferring state from prose or memory.

| Check | Result | Notes |
| :--- | :---: | :--- |
| Read `status.yaml` before making stage claims | `yes` | `stage:next` and `stage:resolve` both routed from the manifest and returned `essay_iteration`. |
| Used package README as local map rather than source of truth | `yes` | README matched the manifest and served as orientation rather than stage authority. |
| Resolved governing brief correctly | `yes` | `config.blueprint_path` resolved to `literate-workflow-programming.md`. |
| Used the matching workflow doc for the claimed next step | `yes` | `essay_iteration` was resolved against `workflows/essay-iteration/README.md`. |
| Treated packet/review artifacts as stage-specific surfaces rather than generic always-load context | `yes` | Packet and review artifacts were used only after the next stage was resolved. |

## Context And Routing Friction

Record whether the run stayed inside stage-scoped context or drifted into prompt bloat and namespace confusion.

| Signal | Result | Notes |
| :--- | :---: | :--- |
| Unnecessary context loaded | `partial` | The run initially lived in a broader strategy discussion before collapsing to the bounded proof-run task. |
| Wrong package or stage inferred | `no` | Once package continuation was the objective, the harness resolved `essay_iteration` correctly. |
| Workflow namespace confusion | `partial` | The package can plausibly be treated as research lab, essay object, or strategy input; that role needed explicit narrowing. |
| Prompt glue needed because tracked routing surfaces were unclear | `yes` | The tracked surfaces resolved stage correctly, but they do not yet explain how to repurpose a research package as a proof-run object. |
| Hook or checker caught a routing mistake | `no` | No lifecycle correction was required after the task was bounded. |

## Execution Summary

1. User redirected the thread from essay drafting toward repo improvement under `phased-strategy`.
2. The harness reviewed `phased-strategy/` and concluded the current strategic gap is still Phase 1.5 proof-run evidence rather than more editorial output.
3. The harness updated `reviewable-runs/templates/harness-proof-run-template.md` so proof runs now score manifest-first routing, governing-brief resolution, context friction, source/trace discipline, and checker/hook corrections.
4. The harness treated `publications/literate-workflow-programming` as the research-heavy proving-ground package and ran `stage:next`, `stage:resolve`, and `check:package-lifecycle`.
5. The package resolved cleanly to `essay_iteration`, with `config.blueprint_path` pointing at the live research brief and the packet scaffold already present.
6. The harness completed one bounded `essay_iteration` step by hardening `literate-workflow-programming-blueprint-r1.md` instead of drafting the essay body.
7. The run stopped without editing `phased-strategy/`, without promoting the package, and without crossing any external boundary.

## Evidence And State Used

List the source files, package state, workflow docs, external outputs, or platform state that actually mattered.

| Evidence | Why It Mattered | Freshness / Provenance |
| :--- | :--- | :--- |
| `phased-strategy/strategic_plan.md` | Defined the actual gap: proof-run evidence before any Phase 1.6 or Phase 2 move. | Tracked strategy source. |
| `phased-strategy/phase-1-1-5-closure-checklist.md` | Named the three proof-run classes and the current open items. | Tracked phase checklist. |
| `publications/literate-workflow-programming/status.yaml` | Resolved the current stage and governing brief path. | Current package manifest. |
| `publications/literate-workflow-programming/README.md` | Provided package-local orientation and confirmed the current stage read. | Current package README. |
| `publications/literate-workflow-programming/literate-workflow-programming.md` | Served as the governing brief named by `config.blueprint_path`. | Current package live research brief. |
| `publications/literate-workflow-programming/literate-workflow-programming-essay-iteration-packet-r1.json` | Confirmed packet scaffold existence and bounded packet outputs. | Current package packet manifest. |
| `publications/literate-workflow-programming/claim-ledger.md` and `claim-scorecard.md` | Supplied the article-ready claims and claim boundaries used to harden the blueprint. | Current package claim-state surfaces. |
| `reviewable-runs/templates/harness-proof-run-template.md` | Was upgraded during this run to capture the newly surfaced failure modes. | Edited in this run. |
| `publications/literate-workflow-programming/literate-workflow-programming-blueprint-r1.md` | Received the bounded `essay_iteration` mutation. | Edited in this run. |

## Source / Trace Discipline

Use this section when the run touches validators, logs, or reviewable traces.

| Check | Result | Notes |
| :--- | :---: | :--- |
| Source artifact stayed primary | `yes` | `status.yaml`, workflow docs, and the governing brief drove the run. |
| Logs/traces treated as derivative debugging surfaces | `yes` | The proof-run record is documenting the run, not replacing the governing package surfaces. |
| Validator findings were linked back to source state or stage contract | `yes` | `check:package-lifecycle` and `stage:resolve` both reported directly on manifest and workflow state. |
| Run avoided claiming broad conformance from a bounded drift check | `yes` | No broad behavioral claim was made from the package-local checks. |
| Provenance gap was identified honestly when present | `yes` | The run treated claim-level provenance as future work rather than current repo capability. |

## Verification

Name the checks run and their results.

| Check | Result | Notes |
| :--- | :---: | :--- |
| `npm run stage:next -- --package literate-workflow-programming --format json` | `PASS` | Returned `essay_iteration` with resolved governing-brief and package evidence context. |
| `npm run stage:resolve -- --package literate-workflow-programming --stage essay_iteration --format json` | `PASS` | Returned clean `essay_iteration` resolution with no blocking issues and no lifecycle warnings. |
| `npm run check:package-lifecycle -- --package literate-workflow-programming` | `PASS` | No lifecycle warnings. |
| `git diff --check` | `PASS` | No whitespace errors. |
| Final `git status --short` | `PASS` | Dirty state is intentional and limited to the proof-run template, the hardened blueprint, this proof-run log, and local-only `AGENTS.md`. |

## Approval And Boundary Behavior

- Was approval required? No.
- Was approval obtained before the controlled action? The user explicitly asked to proceed with the proof-run use of the current package.
- If approval was not required, why not? The run was limited to local proof-run documentation and package-local blueprint hardening.
- Did the harness stop at the correct boundary? Yes. It stopped after one bounded packet step and did not draft the essay body or mutate `phased-strategy/`.
- If blocked by sandbox/auth/network, did it ask for narrow permission or provide exact user-exec commands? Not applicable.
- If lifecycle state was ambiguous or wrong, did a checker or hook force a correction before finalizing? No correction was needed once the task was bounded.

## Failure Or Friction Review

Classify every material problem.

| Problem | Class | Corrective Direction |
| :--- | :--- | :--- |
| The package could plausibly be treated as an essay object, a research lab, or a proof-run input, so the user had to narrow the operating mode explicitly. | `routing gap` | Add a tracked note or future skill surface for how research-heavy packages map onto proof-run classes. |
| The prior proof-run template did not ask about manifest-first routing, governing-brief resolution, source/trace discipline, or checker/hook correction. | `validation gap` | Fixed in this run by extending the template. |
| Several follow-up prompts were needed before the proof-run objective stabilized. | `model discipline` | Keep proving the repo with narrower bounded runs and consider a future `/content-proof-run` operator shell surface in Phase 1.6. |

Recommended problem classes for the current phase:

- `routing gap`: wrong stage, wrong package, wrong governing brief, or wrong workflow doc chosen
- `source-trace confusion`: logs, traces, or validator outputs treated as primary source artifacts
- `context overload`: too much passive context loaded or unclear namespace boundaries
- `validation gap`: validator/checker/hook missing or too weak to catch a material mistake

## Phase 1.5 Gate Answers

| Gate | Answer | Evidence |
| :--- | :---: | :--- |
| Could the harness determine the next valid action without repo explanation? | `partial` | `stage:next` and `stage:resolve` correctly selected `essay_iteration`, but the user still had to clarify that the package should be used as a proof-run object instead of an essay-drafting prompt. |
| Could it start from an idea or package target and produce bounded outputs with correct logs and approval behavior? | `yes` | It continued from the package target, stayed local, hardened one packet artifact, and wrote this inspectable record. |
| Did it succeed with minimal prompt glue and no repo-specific hand-holding beyond the tracked contract? | `partial` | The run stayed within tracked surfaces once bounded, but it took multiple clarifying prompts to settle the objective. |

## Final Decision

- Closure rating: `PARTIAL`
- Promote to retained proof? `no`
- If not promoted, where does the routine record live? `reviewable-runs/logs/2026-04-22_literate-workflow-programming_manifest-first-proof-run.md`
- Required workflow/script/skill hardening: keep the strengthened proof-run template; consider a future proof-run routing surface once more runs confirm the same confusion pattern
- Next proof run to attempt: a cleaner cold-start `polish-publish` or `media-distribution` proof run that begins with only a package target and one bounded objective

## Best-Fit Use Cases

Use this template especially for:

- research-to-intake or research-to-essay-iteration handoffs
- stage-resolution tests where the package has multiple plausible next moves
- runs that exercise lifecycle checkers, packet scaffolds, or Stop-hook corrections
- bounded validator experiments where source/trace hierarchy must remain explicit
