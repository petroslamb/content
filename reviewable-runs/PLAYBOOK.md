# Playbook

This is the canonical operator guide for using Reviewable Runs.

Use it as a field manual for turning a real trace or real run into a credible review surface.

## What This Is For

Use Reviewable Runs when a run matters enough that you do not want to trust it just because it looked smart.

Good triggers:

- a coding run before merge or release
- a browser or platform run before submit or publish
- a retrieval-heavy or policy-sensitive output
- a run that crosses a real control boundary
- an incident, near miss, or postmortem

Do not use the heavy version for trivial low-risk work.

## The Core Rule

One run = one objective + one stop boundary.

Do not apply the framework to a whole conversation by default. Slice the session until you can point to one objective and one meaningful stop condition.

## The Workflow

1. Preserve the raw trace or raw artifacts.
2. Define or slice one bounded run.
3. Identify the real boundary type.
4. Classify the run by risk.
5. Collect the minimum raw evidence set.
6. Reconstruct only the review surface the run actually needs.
7. Verify the correct final state.
8. Answer the six review questions.
9. Approve, reject, revise, or escalate.
10. If the run is worth retaining, classify it as flagship proof, secondary candidate, or private/internal only.

The default process starts from trace preservation, not immediate packet writing.

Important: `framework fit` and `proof promotion` are not the same thing. A run can be a strong use of the framework and still stay a secondary candidate because it adds little new public proof value.

## Boundary Types

Accepted stop-boundary types:

- `handoff`: the run stops at a reviewer or owner handoff
- `commit`: the run stops at a committed internal code state
- `merge`: the run stops at an integrated repository state
- `release`: the run stops at a tagged or shipped software release
- `submit`: the run stops when an external system receives the action
- `publish`: the run stops when public-facing state is live
- `explicit non-approval reason`: the run stays internal and the reason approval was not needed is visible

External-action runs often use `submit` or `publish`, not `commit`.

Bounded internal runs can still be strong when the boundary is `explicit non-approval reason`, as long as the reason is visible and the verification is strong.

If the real boundary is unclear, the run is not ready for review.

## Verification Rules

Internal code runs can often verify with tests, checks, and changed surface evidence.

External-action runs require live platform-state verification. Local success signals, scripts, or screenshots are supporting evidence only when the controlled system is external.

Use the strongest final-state check available:

- tests and validators for internal code
- final UI or API state for third-party platforms
- deployed public state for publish-style runs

Limit-finding runs are valid if the learned boundary is explicit, evidence-backed, and useful for later review. A run does not have to end in conventional success to be strong.

## Minimum Surface By Risk

### Low Risk

Use lightweight reconstruction.

Minimum:

- reconstructable task boundary
- reconstructable action or event history
- basic verification or completion signal
- explicit reason approval was not required

Do not persist a full six-record packet by default.

### Medium Risk

Make the runtime surface explicit.

Minimum:

- task spec
- execution trace
- evidence record
- verification report

Approval may be unnecessary, but the reason should be visible.

### High Risk

Use the full review surface.

Minimum:

- task spec
- execution trace
- evidence record
- verification report
- approval decision
- failure-review capability

External, destructive, hard-to-reverse, or policy-sensitive runs should default here.

## How To Slice Real Sessions

Split a session into separate runs when:

- the objective changes
- the approval or stop boundary changes
- the evidence surface changes materially
- the session shifts from diagnosis to fallback execution
- the session shifts from implementation to release or publish

Do not packetize a mega-session as one run.

The March 26 framework-building work and the March 27 publication-ops work only became strong proof after being split into bounded sub-runs.

## What To Keep

The lightest useful retention set is:

- raw trace
- source manifest
- session excerpt
- changed-files summary
- verification summary
- boundary record

Add the six review records only when the run needs a real review packet or proof artifact.

## When To Escalate To A Full Packet

Lightweight reconstruction is enough when:

- the run is low risk
- the boundary is clear
- the evidence surface is small
- verification is straightforward

Escalate to a full packet when:

- the run crosses a real approval boundary
- verification is contested or non-obvious
- the action affects an external system
- the run may need later defense, rejection, or postmortem
- the run is being promoted as retained proof

Default to selective promotion. Do not archive every run as a flagship proof.

A full packet is about review need, not prestige. Some strong runs should still remain lightweight or secondary.

## Common Anti-Patterns

- treating a whole session as one run
- using a fake commit boundary for an external-action run
- treating raw trace as the final review surface
- treating local success as decisive verification for an external system
- treating limit-finding runs as automatic failures
- treating flagship proof status as the same thing as framework strength
- treating opinion-only review threads as runs
- producing full packets for trivial work

The right question is always:

What is the lightest record surface that makes this run credibly reviewable?

## Examples

Use these proofs as the main operator references:

- code/package run: `examples/proofs/march-12-alphaxiv-auth-refactor/README.md`
- external-action run: `examples/proofs/march-27-youtube-playlist-order-fix/README.md`
- publish/deploy run: `examples/proofs/march-27-manual-mirror-import/README.md`
- broader calibration set: `examples/proofs/real-run-index.md`

After this guide, use `evaluation/run-review-checklist.md` to inspect a specific run.

The rules in this playbook are grounded in the current real-run analysis layer at `analysis/`.
