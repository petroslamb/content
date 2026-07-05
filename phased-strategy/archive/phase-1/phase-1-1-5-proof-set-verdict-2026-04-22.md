# Phase 1.5 Proof-Set Verdict

Snapshot date: 2026-04-22

Archive note, 2026-05-06: this verdict is retained as historical evidence for the Phase 1.5 closure bar. It may mention retired compatibility commands because those were the live surfaces at the time. Current governed work uses `./content-agent`; see [`../../../AUTHORITY.md`](../../../AUTHORITY.md).

## Summary Verdict

`DONE`, under the pragmatic bar.

It is now honest to close Phase 1.5 pragmatically.

That does not mean the proof set is perfectly symmetric. It means the repo now has enough retained evidence across the three required lanes to justify moving on without pretending every lane was proven by the same quality of cold-start run.

What is now true:

- the repo has stronger manifest-first routing, lifecycle checks, governing-brief resolution, and a local Stop-hook backstop
- the `research-heavy` proof lane now includes both a gate-verification pass and an approved bounded `essay_iteration` candidate step
- a strong `publish-adjacent` bounded proof exists on a clean leaf package
- the `media/distribution` lane now has package-scoped retained evidence from `confidence-debt`, including real YouTube upload reports, Shorts upload reports, and workflow hardening committed from the same session

What is not yet true:

- the proof set does not contain three equally clean, proof-minimal runs
- the `publish-adjacent` proof is still `archive_sync`-adjacent rather than the ideal pre-publish/publish-decision continuation
- the `media/distribution` proof is package-scoped and sequential rather than a single-purpose proof prompt
- the `research-heavy` lane is now good enough to retain, but it reached closure through a gate-check plus an approved bounded candidate step rather than a single pristine cold-start run

## Evidence By Lane

| Lane | Best Current Evidence | Read | Verdict |
| :--- | :--- | :--- | :--- |
| `research-heavy` | [`reviewable-runs/logs/2026-04-22_literate-workflow-programming_manifest-first-proof-run.md`](../../../reviewable-runs/logs/2026-04-22_literate-workflow-programming_manifest-first-proof-run.md), [`reviewable-runs/logs/2026-04-22_literate-workflow-programming_claim-provenance-step.md`](../../../reviewable-runs/logs/2026-04-22_literate-workflow-programming_claim-provenance-step.md), [`reviewable-runs/logs/2026-04-22_literate-workflow-programming_major-rewrite-gate-check.md`](../../../reviewable-runs/logs/2026-04-22_literate-workflow-programming_major-rewrite-gate-check.md), [`reviewable-runs/logs/2026-04-22_literate-workflow-programming_bounded-candidate-step.md`](../../../reviewable-runs/logs/2026-04-22_literate-workflow-programming_bounded-candidate-step.md) | The lane now proves the full post-research transition: stage resolution, gate respect, and one approved bounded `essay_iteration` packet step. | `PASS`, but not proof-minimal |
| `publish-adjacent` | [`reviewable-runs/logs/2026-04-22_17-50-08_neural-architectures__neural-architecture-design-as-a-compositional-32e_archive_sync_launch-pack.json`](../../../reviewable-runs/logs/2026-04-22_17-50-08_neural-architectures__neural-architecture-design-as-a-compositional-32e_archive_sync_launch-pack.json), [`reviewable-runs/logs/2026-04-22_17-54-42_neural-architectures__neural-architecture-design-as-a-compositional-32e_archive_sync_local-mirror-validation.json`](../../../reviewable-runs/logs/2026-04-22_17-54-42_neural-architectures__neural-architecture-design-as-a-compositional-32e_archive_sync_local-mirror-validation.json) | Clean cold-start package targeting, correct next-stage resolution, correct bounded local validator step, no external mutation. | `PASS`, but narrower than the ideal checklist lane |
| `media/distribution` | Private operational YouTube reports moved to the private overlay. | Strong package-scoped operational evidence existed for rebuilt longform, TL;DR upload, scheduled Shorts readback, downloaded portrait Shorts upload, and workflow hardening from the same session. | `PASS`, but not proof-minimal |

## What This Session Actually Bought

The initial goal was to use `publications/literate-workflow-programming` as a proving ground for repo-wide workflow improvement rather than merely to advance one publication. That goal was met.

This session produced four durable outcomes:

1. **Research-to-repo synthesis**
   - The strongest defensible direction is now clearer: manifest-first routing, validation as the hinge, and traces as derivative debugging surfaces.
   - More speculative directions such as repo-wide `spec-diff` promotion, import semantics, or package-as-object claims stayed parked.

2. **Tracked workflow hardening**
   - manifest-first lifecycle guardrails
   - explicit `config.blueprint_path`
   - lifecycle checker
   - repo-documented local Stop hook
   - better umbrella/leaf routing

3. **Proof-run instrumentation hardening**
   - the proof-run template now measures routing, context friction, source/trace discipline, and checker/hook correction
   - the repo can now distinguish a real bounded proof from a vague successful workflow anecdote

4. **Concrete package repairs that matter to the harness**
   - `publications/neural-architectures` now has a real umbrella governing brief
   - the umbrella now delegates its active media-stage surface coherently to the default leaf
   - `scripts/harness.py` now prefers timed captions over untimed transcript files for `youtube_production`

## Residual Strict-Bar Caveats

The repo is operable enough to close the phase pragmatically. The remaining caveats matter, but they no longer need to block the phase:

- the **research-heavy** lane reached retained-proof quality through two bounded passes rather than one pristine proof-minimal run
- the **publish-adjacent** lane is still `archive_sync`-adjacent rather than a cleaner release-gate continuation
- the **media/distribution** lane is operationally strong, but its retained proof remains package-scoped and sequential

Those are the reasons a stricter bar could still say `PARTIAL`. They are not strong enough reasons to keep the repo artificially stuck in Phase 1.5.

## Pragmatic Gate Read

Against [`phase-1-1-5-closure-checklist.md`](phase-1-1-5-closure-checklist.md):

| Gate | Current Answer | Notes |
| :--- | :---: | :--- |
| Harness can determine next valid action without repo explanation | `yes` | The retained runs now cover research-heavy, publish-adjacent, and media/distribution routing decisions with tracked-state evidence. |
| Harness can produce bounded outputs with correct logs and approval behavior | `yes` | Proven repeatedly for local bounded steps. |
| At least 3 real runs succeeded with minimal prompt glue and no repo-specific hand-holding beyond the tracked contract | `yes`, pragmatically | The three lanes now have retained evidence. They are not equally clean, but they are good enough to clear the phase on a pragmatic standard. |

## Recommended Next Move

Open **Phase 1.6** and treat any stricter reruns as hardening work, not as a Phase 1.5 blocker.

Recommended follow-through:

1. Keep the retained proof set as the closure basis for Phase 1.5.
2. Preserve the strict-bar caveats so later work does not overclaim what was proven.
3. Use Phase 1.6 to reduce prompt glue, improve auth/browser ergonomics, and tighten proof-run quality further.

The correct strategic label is now: **Phase 1.5 closed under the pragmatic bar.**
