# Phase 1.5 Proof-Set Verdict

Snapshot date: 2026-04-22

## Summary Verdict

`PARTIAL`.

Phase 1.5 is materially closer to closure than it was at the start of this session, but it is not yet honest to call it closed.

What is now true:

- the repo has stronger manifest-first routing, lifecycle checks, governing-brief resolution, and a local Stop-hook backstop
- the `research-heavy` proof lane has been exercised with real package-local work
- a strong `publish-adjacent` bounded proof exists on a clean leaf package
- the `media/distribution` lane now has package-scoped retained evidence from `confidence-debt`, including real YouTube upload reports, Shorts upload reports, and workflow hardening committed from the same session

What is not yet true:

- the proof set does not yet contain three equally strong, current-style measured Phase 1.5 proofs
- the research-heavy proof still needed clarifying prompt glue
- the publish-adjacent proof is good evidence, but it is `archive_sync`-adjacent rather than the stricter `article_polish` to release-gate to publish-decision lane named in the checklist
- the research-heavy lane remains the weakest current proof and is now the main reason the phase is still not honest to close

## Evidence By Lane

| Lane | Best Current Evidence | Read | Verdict |
| :--- | :--- | :--- | :--- |
| `research-heavy` | [`reviewable-runs/logs/2026-04-22_literate-workflow-programming_manifest-first-proof-run.md`](../reviewable-runs/logs/2026-04-22_literate-workflow-programming_manifest-first-proof-run.md), [`reviewable-runs/logs/2026-04-22_literate-workflow-programming_claim-provenance-step.md`](../reviewable-runs/logs/2026-04-22_literate-workflow-programming_claim-provenance-step.md) | Real package-local bounded work happened, and the run improved the proof template itself. | `PARTIAL` |
| `publish-adjacent` | [`reviewable-runs/logs/2026-04-22_17-50-08_neural-architectures__neural-architecture-design-as-a-compositional-32e_archive_sync_launch-pack.json`](../reviewable-runs/logs/2026-04-22_17-50-08_neural-architectures__neural-architecture-design-as-a-compositional-32e_archive_sync_launch-pack.json), [`reviewable-runs/logs/2026-04-22_17-54-42_neural-architectures__neural-architecture-design-as-a-compositional-32e_archive_sync_local-mirror-validation.json`](../reviewable-runs/logs/2026-04-22_17-54-42_neural-architectures__neural-architecture-design-as-a-compositional-32e_archive_sync_local-mirror-validation.json) | Clean cold-start package targeting, correct next-stage resolution, correct bounded local validator step, no external mutation. | `PASS`, but narrower than the ideal checklist lane |
| `media/distribution` | [`reviewable-runs/logs/2026-04-22_confidence-debt_media-distribution-retrospective.md`](../reviewable-runs/logs/2026-04-22_confidence-debt_media-distribution-retrospective.md), [`publications/confidence-debt/artifacts/video/shorts/shorts_upload_report.json`](../publications/confidence-debt/artifacts/video/shorts/shorts_upload_report.json), [`publications/confidence-debt/artifacts/latest/tldr_upload_report.json`](../publications/confidence-debt/artifacts/latest/tldr_upload_report.json), [`publications/confidence-debt/artifacts/video/downloaded-shorts/downloaded_shorts_upload_report.json`](../publications/confidence-debt/artifacts/video/downloaded-shorts/downloaded_shorts_upload_report.json) | Strong package-scoped operational evidence: rebuilt longform, TL;DR upload, `16` scheduled Shorts with readback, `4` downloaded portrait Shorts uploaded immediately, and workflow hardening committed from the same session. | `PASS`, but not proof-minimal |

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

## Why Phase 1.5 Is Still Not Closed

The open gap is no longer “the repo is not operable.” The open gap is narrower:

- the **research-heavy** lane is useful but still prompt-fragile
- the **publish-adjacent** lane is strong, but it is still an `archive_sync` proof rather than the checklist’s ideal pre-publish/publish-decision continuation
- the **media/distribution** lane is now covered well enough by `confidence-debt` that it is no longer the main blocker

That means the repo has crossed from “the system might work” into “the system mostly works, but the proof set is not yet strong enough to certify the phase.”

## Honest Gate Read

Against [`phase-1-1-5-closure-checklist.md`](phase-1-1-5-closure-checklist.md):

| Gate | Current Answer | Notes |
| :--- | :---: | :--- |
| Harness can determine next valid action without repo explanation | `partial` | Good on clean packages; still some ambiguity in research-heavy framing and umbrella packages before recent fixes. |
| Harness can produce bounded outputs with correct logs and approval behavior | `yes` | Proven repeatedly for local bounded steps. |
| At least 3 real runs succeeded with minimal prompt glue and no repo-specific hand-holding beyond the tracked contract | `partial` | Three lanes now have retained evidence, but the research-heavy lane still does not clear the same bar as the other two. |

## Recommended Next Move

Run **one stricter research-heavy rerun**.

Preferred standard:

- one bounded prompt
- one package target
- current proof template or equivalent fields
- explicit boundary behavior
- explicit glue score
- explicit stop condition

The media/distribution reconstruction now exists and the publish-adjacent lane is already strong, so the remaining ask is narrower:

1. **Fresh cleaner research-heavy proof run**
   - Best if we want a clean closure argument.
   - Use one explicit `research-heavy` package target and one bounded next-step continuation.

2. **Or write the final strict closure note**
   - The remaining weakness is concentrated rather than diffuse.
   - If we accept lane asymmetry, the note should say that explicitly instead of pretending all three lanes are equally clean.

Until that stricter research-heavy proof or explicit closure exception exists, the correct phase label remains `PARTIAL`.
