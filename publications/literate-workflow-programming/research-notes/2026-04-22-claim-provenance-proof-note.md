# Claim-Provenance Proof Note

Date: 2026-04-22

Status: package-local provenance-layer proof note, not a draft or strategy update

## Purpose

This note executes the next bounded action identified in the 2026-04-22 proof gate:

> Create a package-local claim-provenance proof note that maps the article-ready claims to evidence state, contradiction state, validation state, and trace state using the existing ledger, contradiction register, scorecard, and retained `spec-diff` proof artifacts.

The target is narrow. This is not a new article frame, a candidate draft, or a repo-wide validator proposal. It is a local proof that the package can represent claim state more richly than "paper exists" or "run passed."

## Inputs Used

- [`../claim-ledger.md`](../claim-ledger.md)
- [`../claim-scorecard.md`](../claim-scorecard.md)
- [`../contradiction-register.md`](../contradiction-register.md)
- [`../literate-workflow-programming.md`](../literate-workflow-programming.md)
- [`2026-04-21-p2a-local-intake-trace-provenance.md`](2026-04-21-p2a-local-intake-trace-provenance.md)
- [`2026-04-21-confidence-debt-contradiction-ledger-transfer.md`](2026-04-21-confidence-debt-contradiction-ledger-transfer.md)
- [`../../../reviewable-runs/logs/2026-04-21_literate-workflow-programming_p1-intake-spec-diff-proof-candidate.md`](../../../reviewable-runs/logs/2026-04-21_literate-workflow-programming_p1-intake-spec-diff-proof-candidate.md)
- [`../../../reviewable-runs/logs/2026-04-21_illusion-of-swarm_spec-diff-proof-candidate.md`](../../../reviewable-runs/logs/2026-04-21_illusion-of-swarm_spec-diff-proof-candidate.md)

## State Vocabulary

This note uses the narrower mechanism transferred from the Confidence Debt cross-read:

```text
claim -> evidence state + contradiction state + validation state + trace state
```

The meanings here are package-local:

- `evidence state`: whether the claim has sufficient local paper-backed and package-backed support to appear in the article
- `contradiction state`: whether the main tension has been resolved, remains open with visible caveat, or is still blocking
- `validation state`: whether the package has a real local validation or enforcement surface for the claim, not just paper support
- `trace state`: whether there is a retained local run/proof artifact showing the claim on live package state rather than only in prose

This is still weaker than full claim-level provenance graphs. The note maps claims to current state; it does not implement semantic provenance queries or automatic contradiction resolution.

## Claim-State Map

| Claim ID | Short Claim | Evidence State | Contradiction State | Validation State | Trace State | Current Use |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CSA-C1 | Workflow specs become meaningful source only when coupled to validation gates, policy enforcement, and semantic debugging traces. | strong local paper support plus local package synthesis | resolved through `CSA-001`, `CSA-002`, `CSA-003` | partial local validation: `spec-diff` proves bounded source/evidence drift only | indirect trace support through the two `spec-diff` proof candidates | safe as lead frame with the bounded `spec-diff` caveat visible |
| CSA-C2 | Reviewable-run logs should be traces and semantic debugging surfaces, not the source of truth. | strong local paper support plus local proof notes | resolved through `CSA-003` | partial local validation: Reviewable Runs plus `spec-diff` show trace/debug value without source inversion | direct trace support from the P1 intake and `illusion-of-swarm` proof candidates | safe in the proof section if the source/trace hierarchy stays explicit |
| CSA-C3 | Markdown workflow files become programming substrate only when paired with runtime binding, validation, policy enforcement, and provenance. | strong local paper support | open but bounded through `CSA-007`; task-risk caveat remains mandatory | partial local validation: package has validators and policy language, but not full provenance | indirect trace support through `spec-diff` and packet validators | safe as narrowed metaphor, not as a claim that markdown alone is executable |
| CSA-C5 | Local `spec-diff` experiments are repo-native proof candidates for source-linked drift detection. | strong local package support and two retained proof records | parked through `CSA-005`; repo-wide promotion remains out of scope | strong local validation for the bounded claim only | direct trace support from both retained proof candidates | safe as the package's local proof example for drift detection only |
| CSA-C6 | Claim-level provenance and contradiction state should be part of the semantic-debugging surface for promoted workflow claims. | strong local paper support after P2a plus explicit package need | resolved on scope through `CSA-006`; implementation gap remains explicit | weak-to-partial local validation: contradiction register exists, but no claim-evidence graph or queryable provenance | indirect trace support only; current logs show drift and gap classification, not full provenance | safe as the next-layer requirement, not as a statement of completed local capability |
| CSA-C7 | Validation should be treated as lifecycle infrastructure, not as a one-time gate. | strong local paper support | open but bounded through `CSA-008`; formality is diagnostic, not monotonic proof | partial-to-strong local validation: `spec-diff`, packet validation, and package checks model continuous checking in a limited way | direct trace support from the P1 intake proof candidate and current packet-validator state | safe as the hinge claim if the draft avoids fully autonomous-validation overreach |

## Per-Claim Notes

### CSA-C1

This is the strongest top-level package claim, but its local proof remains composite rather than singular. The package has paper-backed specification, validation, policy, and trace arguments, and it has one bounded validator family that checks declared package state against evidence state. That is enough for article use. It is not enough to imply broad behavioral conformance or a generalized repo compiler.

### CSA-C2

This is the cleanest local source/trace claim. The package has both the paper support and the retained run artifacts to show the distinction in practice:

- the governing brief and package surfaces stay primary
- `spec-diff` reports are derivative checks
- Reviewable Runs logs preserve what happened without becoming the authority surface

The remaining gap is not conceptual. It is provenance depth.

### CSA-C3

This claim is article-safe only with the task-risk caveat. The open contradiction does not block the claim, but it prevents any flattening into "context files are good" or "markdown is code." The right local reading is stricter:

- workflow/source surfaces matter
- runtime binding and policy enforcement matter
- provenance still matters

Without that bundle, the package only has editable documentation, not a trustworthy programming substrate.

### CSA-C5

This is the best locally demonstrated claim because it has real before/after proof records:

- the P1 intake run caught ordinary intake drift before the index was repaired
- the `illusion-of-swarm` run caught orientation drift in a second package with mixed evidence conventions

That is enough to call `spec-diff` a proof candidate for source-linked drift detection. It is not enough to justify a root validator, phase change, or shared lifecycle requirement.

### CSA-C6

This is the claim this note is meant to clarify.

Local package state now supports three distinct statements:

1. contradiction state belongs in the semantic-debugging story
2. claim-level provenance is the correct next layer
3. the repo does not yet implement that layer fully

The package already has the minimal ingredients for a provenance-shaped claim surface:

- evidence state in the claim ledger
- contradiction state in the contradiction register
- article-readiness state in the scorecard
- retained trace artifacts in the proof-candidate logs

What it does not yet have:

- claim-evidence graphs
- provenance coverage or soundness metrics
- queryable contradiction transparency across claims
- automated authority resolution

So CSA-C6 is now a justified requirement claim, not a completed implementation claim.

### CSA-C7

This claim is stronger after the P2a intake and still honest locally. The package does not just have one terminal check. It has multiple bounded validation surfaces:

- package audit
- packet validation
- `spec-diff`
- contradiction classification

That is enough to support "validation as lifecycle infrastructure" in a package-local sense. It is not enough to claim the repo already has a full autonomous validation stack.

## What This Note Proves

- The package can represent article-ready claims in a richer state model than "supported / unsupported."
- The package already has separate surfaces for evidence, contradiction, validation, and trace.
- The strongest missing local layer is claim-level provenance integration, not more loose source discovery.
- A local claim-provenance experiment is warranted as package work.

## What This Note Does Not Prove

- that the repo already has semantic provenance graphs
- that current Reviewable Runs are full source maps
- that `spec-diff` proves broad behavioral conformance
- that repo-wide validator promotion is now justified
- that the package is ready for essay-body drafting without a real candidate/review loop

## Consequence For The Package

This note closes the specific open decision named in the live brief:

- a local claim-provenance experiment was warranted
- the bounded experiment can be satisfied by mapping the current article-ready claims onto evidence, contradiction, validation, and trace state
- the result strengthens CSA-C6 as a package-local requirement claim without changing `phased-strategy/`

## Contract Check

As of the tracked package state on 2026-04-22:

- [`../status.yaml`](../status.yaml) keeps the package in `essay_iteration`
- [`../literate-workflow-programming-prewrite-gate-r1.md`](../literate-workflow-programming-prewrite-gate-r1.md) sets `writability_verdict: writable`
- [`../literate-workflow-programming-prewrite-gate-r1.md`](../literate-workflow-programming-prewrite-gate-r1.md) sets `candidate_authorized: true`

So the packet-level contract does authorize a bounded candidate draft. This proof note does not change that authorization. It only adds a stronger local record for CSA-C6 and the claim-state machinery behind it.

For this proof pass, the bounded action stops here because the task constraint is explicit: do not draft the essay body.

The next honest non-drafting move would be either:

1. fold this state map into a stronger packet-level review artifact once a real candidate exists, or
2. design a smaller package-local provenance manifest for claims without promoting it to a repo-wide interface
