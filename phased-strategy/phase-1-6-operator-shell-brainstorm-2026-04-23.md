# Phase 1.6 Operator Shell Brainstorm And Convergence Plan

Snapshot date: 2026-04-23

## Purpose

This note is the working plan for Phase 1.6.

It is intentionally two-step:

1. brainstorm the operator-shell design space without prematurely freezing implementation
2. converge on the thinnest concrete solution that reduces prompt glue in real runs

The source phase definition remains [`strategic_plan.md`](strategic_plan.md). This note is the execution-planning layer for that phase, not a replacement strategy.

## What Phase 1.6 Must Actually Fix

Phase 1.5 already gave the repo a stable machine-facing contract:

- [`harness_contract.yaml`](../harness_contract.yaml)
- [`harness_policy.yaml`](../harness_policy.yaml)
- `package:init`
- `stage:next`
- `stage:resolve`
- `stage:run`
- launch-pack generation

What it did **not** fully solve:

- prompt glue still shows up in ambiguous or research-heavy runs
- guided-stage launch quality still varies by package and stage
- safety is encoded, but not yet surfaced as named operator controls
- the tracked skill layer is useful, but it is still a collection of tool/stage skills rather than a small operator shell
- browser/auth persistence exists in fragments rather than as one visible operating pattern

Phase 1.6 should therefore be judged by one question:

> Does it make the existing harness surface materially easier and safer to use without creating a second hidden system?

## Current Assets To Reuse

| Surface | Already Exists | Phase 1.6 Implication |
| :--- | :--- | :--- |
| Machine contract | [`../harness_contract.yaml`](../harness_contract.yaml) | Operator commands should compose this, not bypass it. |
| Policy layer | [`../harness_policy.yaml`](../harness_policy.yaml) | Safety modes should be views over policy, not a parallel rulebook. |
| Workflow contract | workflow frontmatter in [`../workflows/`](../workflows/README.md) | Generated operator docs should pull from workflow metadata directly. |
| Stage routing | `npm run stage:next`, `stage:resolve`, `stage:run`, `package:init` | The operator shell should be a thin wrapper around these entrypoints. |
| Existing skills | [`../workflows/skills/README.md`](../workflows/skills/README.md) | Keep specialized skills as lower-level execution helpers. |
| Safety backstop | [`../scripts/codex_hooks/stop_lifecycle_check.py`](../scripts/codex_hooks/stop_lifecycle_check.py) | Visible safety controls should complement the hook, not replace it. |
| Proof evidence | [`../reviewable-runs/logs/README.md`](../reviewable-runs/logs/README.md), [`../reviewable-runs/evaluation/README.md`](../reviewable-runs/evaluation/README.md) | Phase 1.6 should upgrade evaluation quality using the same retained-run discipline. |
| Browser footholds | alphaXiv persistent profile guidance; Substack CDP attach flow | Build a narrow browser-session pattern instead of a general browser platform. |

## New Fixture Baseline After Package Migration

The operator shell now has real package classes to test against. Treat these as the minimum fixture set for Phase 1.6 proof runs:

- active umbrella with active flagship leaf: [`../publications/evidence-governance/`](../publications/evidence-governance/README.md)
- umbrella with stopped successor-search overlay: [`../publications/literate-workflow-programming/`](../publications/literate-workflow-programming/README.md)
- settled published umbrellas: [`../publications/autonomous-agents/`](../publications/autonomous-agents/README.md), [`../publications/hardware-friction/`](../publications/hardware-friction/README.md), [`../publications/orchestration-paradigm/`](../publications/orchestration-paradigm/README.md), and [`../publications/neural-architectures/`](../publications/neural-architectures/README.md)

This matters because Phase 1.6 is no longer testing only whether the shell can route a single-publication package. It must also:

- avoid pretending that settled umbrella roots are still marching through downstream stages
- correctly hand off from umbrella roots to active leaf packages when a leaf owns the lifecycle
- surface umbrella-level routes such as `post_ceiling_pivot` when there is no active successor leaf

## Brainstorm Frame

Before building, answer these five questions:

1. Should the operator shell route by lifecycle stage or by user intent?
2. Should the Phase 1.6 skill docs be fully generated, fully hand-authored, or mixed?
3. Where should `careful`, `freeze`, and `guard` actually live?
4. How much persistent browser support is enough for this phase?
5. What proof would show that the shell improved real Codex use rather than just producing nicer docs?

## Brainstorm Options

### 1. Routing Surface

**Option A: stage-first shell**

- expose `paper-intake`, `research`, `essay-iteration`, `publish`, and so on directly
- strongest alignment with the current workflow vocabulary
- weak point: this mostly mirrors the lifecycle and does not reduce prompt glue for ambiguous user asks

**Option B: intent-first shell**

- expose a small set of named entrypoints such as `/content-next`, `/content-research`, and `/content-proof-run`
- route from user intent to the existing stage surface
- strongest fit for the actual Phase 1.6 milestone text

**Option C: black-box meta-agent**

- ask for any request and let a hidden router decide the rest
- lowest visible complexity
- wrong fit for this repo because it hides dispatch logic and creates a second orchestration layer

**Recommendation**

Choose **Option B**.

Phase 1.6 is supposed to be an operator shell, not a new hidden planner. The shell should make routing more legible, not less.

### 2. Skill Doc Generation

**Option A: fully hand-maintained skill docs**

- fastest to start
- highest drift risk

**Option B: fully generated skill docs**

- lowest drift
- likely too rigid for good operator guidance and examples

**Option C: generated contract blocks plus small hand-authored intent blocks**

- keep the machine-derived parts generated
- keep only the intent framing, examples, and escalation notes hand-authored

**Recommendation**

Choose **Option C**.

The repo should not hand-maintain stage ids, approval boundaries, or command examples twice. But fully generated operator docs will likely be too stiff to help with real routing.

### 3. Safety Controls

**Option A: doc-only named modes**

- easiest to write
- does not actually change operating behavior

**Option B: wrapper flags only**

- real behavior change
- easy to hide in command syntax and easy to forget

**Option C: policy-backed operator profiles surfaced in output, launch packs, and skill docs**

- safety state becomes visible
- the underlying policy remains authoritative
- can be reused by both humans and the harness

**Recommendation**

Choose **Option C**.

The shell should surface at least these modes:

- `careful`: prefer inspect/resolve/launch-pack behavior and avoid unattended external mutation
- `freeze`: keep edits bounded to declared package or file scope
- `guard`: combine both

### 4. Persistent Browser Support

**Option A: universal persistent browser layer**

- conceptually neat
- overbuilds the problem and drifts toward a platform project

**Option B: per-target session adapters with one shared operating convention**

- one narrow pattern for Substack, NotebookLM, and YouTube
- keeps the session state local-only
- matches the actual pain points already seen in the repo

**Option C: defer browser support entirely**

- smallest immediate scope
- leaves a known Phase 1.6 requirement unresolved

**Recommendation**

Choose **Option B**.

The tracked layer should define adapters and readiness checks only. Auth state, cookies, and browser profiles should remain local-only.

### 5. Proof-Run Evaluation

**Option A: markdown retrospectives only**

- human-readable
- hard to compare across runs

**Option B: JSON metrics only**

- comparable
- poor review surface on its own

**Option C: markdown review plus structured JSON sidecar**

- human-readable retained record
- machine-comparable metrics for prompt glue, routing, and safety behavior

**Recommendation**

Choose **Option C**.

## Converged Concrete Solution

The thinnest viable Phase 1.6 architecture is:

1. add one small tracked **operator route map**
2. add one thin **operator router script**
3. generate six **intent-level operator skills** from the route map plus the existing contract/policy/workflow metadata
4. surface three **visible safety modes**
5. standardize three **browser session adapters**
6. add a **proof-run eval sidecar** for operator-shell runs

### Recommended New Surfaces

| Surface | Role | Rule |
| :--- | :--- | :--- |
| `operator_shell.yaml` or similarly named tracked map | maps user intents to existing stage surfaces, defaults, and safety posture | must reference existing stage ids and skills rather than duplicate workflow logic |
| `scripts/content_shell.py` | thin router over `package:init`, `stage:next`, `stage:resolve`, `stage:run`, and launch-pack generation | should emit concise operator payloads, not invent a new lifecycle engine |
| `workflows/skills/content-*/SKILL.md` | named operator shell entrypoints | generated from tracked sources except for small intent preambles/examples |
| browser target registry | declares how Substack, NotebookLM, and YouTube sessions are detected or attached | keep actual auth state out of git |
| eval schema for operator runs | captures prompt glue and routing quality | reuse Reviewable Runs rather than invent a separate evidence system |

## Proposed Operator Surface

| Operator skill | Primary job | Underlying surface |
| :--- | :--- | :--- |
| `/content-office-hours` | turn a broad idea or messy package state into a concrete next move | topic-discovery guidance plus `package:init` when ready |
| `/content-next` | continue a known package with the right next stage and bounded command surface | `stage:next` then `stage:resolve` |
| `/content-research` | route ambiguous paper/research/validation asks into the right research lane | `stage:resolve` for `research` or `paper_intake` plus existing research skills |
| `/content-polish` | prepare a package for release-quality editorial cleanup | `stage:resolve` for `notebooklm_artifacts` or `article_polish` |
| `/content-publish-check` | stop before mutation and show release/publish readiness | release-gate workflow plus publish-stage boundary metadata |
| `/content-proof-run` | frame a bounded proof target, emit the right launch pack, and attach evaluation expectations | launch-pack generation plus Reviewable Runs evaluation surfaces |

## Why This Is The Right Thin Slice

This design stays on the correct side of the boundary:

- it does **not** replace the lifecycle
- it does **not** create a universal browser platform
- it does **not** create a second workflow instruction universe
- it does **not** hide dispatch behind a black-box meta-agent

It only makes the existing contract more routable and more operable.

## Delivery Sequence

### Step 1: Freeze The Operator Boundary

Write the route map first.

It should answer:

- which user intents map to which named shell commands
- which stage ids or workflow groups each command may route into
- which existing skills can be delegated to
- which safety mode each route defaults to
- whether the route can execute or should only resolve/emit a launch pack by default

**Exit criterion**: the route map is small, explicit, and contains no duplicated workflow prose.

### Step 2: Build The Thin Router

Implement the operator router as a wrapper over existing harness commands.

Minimum behavior:

- resolve package target or idea target
- call `package:init`, `stage:next`, `stage:resolve`, `stage:run`, and `--emit-launch-pack` as needed
- print a short operator-facing payload with next move, boundaries, and context requirements

**Exit criterion**: `/content-next` and `/content-proof-run` can run end-to-end without bypassing the Phase 1.5 harness.

### Step 3: Generate The Skill Docs

Generate the operator-skill docs from:

- [`../harness_contract.yaml`](../harness_contract.yaml)
- [`../harness_policy.yaml`](../harness_policy.yaml)
- workflow frontmatter
- the operator route map

Hand-authored material should be limited to:

- the skill description
- the mental-model summary
- one or two examples
- escalation notes

**Exit criterion**: changing a workflow stage, approval gate, or entrypoint updates the generated operator docs automatically.

### Step 4: Add Visible Safety Profiles

Expose `careful`, `freeze`, and `guard` as first-class operator states.

They should appear in:

- the router output
- launch packs
- generated skill docs
- proof-run evaluation

**Exit criterion**: a user or harness can tell which safety profile is active without reopening YAML by hand.

### Step 5: Standardize Browser Session Adapters

Create a narrow shared pattern for:

- Substack
- NotebookLM
- YouTube

Likely shape:

- readiness check
- attach command or expected local profile
- clear failure message when the session is absent

**Exit criterion**: auth-heavy routes stop requiring rediscovery of the same browser/session instructions.

### Step 6: Add Operator-Shell Evaluation

For proof runs through the new shell, capture:

- task prompt
- operator command used
- package target
- follow-up prompts required before the objective stabilized
- routing correctness
- launch-pack quality
- approval-boundary behavior
- repo-discovery failures
- whether the shell reduced prompt glue compared with the old path

**Exit criterion**: at least two retained comparisons show that the shell improved a real run.

Those comparisons should include at least one active umbrella-with-leaf case and one umbrella-overlay stop-path case so the proof set covers the new baseline package classes rather than only leaf-style runs.

## Recommended First Implementation Cut

Do **not** start by building all six skills at once.

Start with:

1. `/content-next`
2. `/content-proof-run`

Why these first:

- they attack the exact residual Phase 1.5 pain around routing gap and prompt glue
- they reuse the strongest existing harness surfaces
- they let the repo test evaluation, safety visibility, and doc generation without needing browser work first

After that, add:

3. `/content-research`
4. `/content-publish-check`
5. `/content-polish`
6. `/content-office-hours`

That order keeps the shell close to current operational pain rather than beginning with the vaguest route.

## Proof Targets For The First Slice

Use one clean leaf and one ambiguous research-heavy package.

Recommended targets:

- a clean package continuation case such as the retained `publish-adjacent` proof lane
- [`../publications/literate-workflow-programming/`](../publications/literate-workflow-programming/README.md) as the ambiguity stress case for `/content-proof-run`

The first proof should answer:

- did the route pick the correct operating mode faster
- did the shell make the approval boundary more obvious
- did the launch pack become more actionable

## Success Criteria

Phase 1.6 is on the right track if all of these become true:

1. a user can ask for normal repo work through a small named operator surface instead of remembering raw entrypoints
2. operator docs stay aligned with the tracked contract and workflow metadata
3. the active safety state is visible during a run
4. browser-heavy routes have one stable attach/check story where it matters
5. retained proof runs show less prompt glue or fewer routing errors than the Phase 1.5 baseline

## Non-Goals

This phase should **not** attempt:

- a universal browser automation platform
- a hidden meta-agent that silently dispatches everything
- a second hand-maintained workflow universe
- forcing non-publication surfaces such as `phased-strategy/` into publication `status.yaml`
- replacing the specialized lower-level skill bundles that already work

## Decision

The recommended concrete solution is:

- **intent-routed operator shell**
- **generated contract-aligned skill docs**
- **policy-backed visible safety modes**
- **narrow browser session adapters**
- **proof-run eval with markdown plus structured metrics**

That is the smallest Phase 1.6 build that directly addresses the current evidence-backed pain points.
