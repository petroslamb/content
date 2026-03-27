# Reviewer Governance Lens

## Thesis

Reviewable Runs is already strong at making approval timing, handoff quality, and post-run accountability visible. Its weakest governance area is not basic control, but ambiguous or distributed responsibility.

## What Worked

- `Q1:` The framework handles runs with real gates best: merge boundaries, handoffs, pre-submit browser holds, and publish-or-don't-publish cases. Evidence: [`../../examples/proofs/march-07-origin-refactor/README.md`](../../examples/proofs/march-07-origin-refactor/README.md), [`../../examples/proofs/coding-real-run/README.md`](../../examples/proofs/coding-real-run/README.md), [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md).
- `Q3:` It clearly adds value beyond raw traces by making approval status and failure posture explicit. The March 7 proof shows why handoff matters; the coding proof shows why merge approval matters; the synthetic lab shows why retroactive approval still fails. Evidence: [`../../examples/proofs/march-07-origin-refactor/comparison.md`](../../examples/proofs/march-07-origin-refactor/comparison.md), [`../../examples/proofs/coding-real-run/comparison.md`](../../examples/proofs/coding-real-run/comparison.md), [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md).
- `Q5:` The approval-decision and failure-review records are conceptually coherent. The framework is not merely logging actions; it is marking control boundaries and plausible failure classes in a way that supports after-the-fact judgment. Evidence: [`../../evaluation/run-review-checklist.md`](../../evaluation/run-review-checklist.md), [`../../examples/proofs/march-26-standalone-extraction/review-packet/approval-decision.md`](../../examples/proofs/march-26-standalone-extraction/review-packet/approval-decision.md).

## What Failed

- `Q2:` The framework struggles when responsibility is distributed or late. The synthetic retroactive-approval case and multi-agent handoff case show that the framework can expose the problem, but not yet rank or assign responsibility sharply enough. Evidence: [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md).
- `Q4:` Governance records remain highly hand-authored. The current framework does not yet specify how approval records or failure reviews should be captured from real systems rather than written after the fact.
- `Q6:` The docs are directionally right, but the hardest cases still need careful judgment. A commit boundary, a review handoff, a release gate, and an external action boundary are not identical, and the framework should keep that distinction crisp. Evidence: [`../../PLAYBOOK.md`](../../PLAYBOOK.md), [`../../examples/proofs/march-07-origin-refactor/review-packet/approval-decision.md`](../../examples/proofs/march-07-origin-refactor/review-packet/approval-decision.md).

## What Is Missing

- `Q8:` The framework needs a more explicit gate taxonomy: handoff, commit, merge, release, publish, submit, and external action. That would make governance records more operational.
- `Q9:` Real proof supports the claim that governance becomes clearer when the packet is explicit. It does not yet support stronger claims about repeated postmortem or approval use in production organizations. Evidence: [`../../examples/proofs/README.md`](../../examples/proofs/README.md), [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md).

## Tuning Needed

- `Q7:` Tune the governance surface around timing and control type, not just yes/no approval.
- `Q10:` Run the framework on a real browser pre-submit flow and a real publication-sensitive retrieval run. Those would stress approval timing and failure review more directly than the current proof set. Evidence: [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md), [`../../examples/proofs/real-run-index.md`](../../examples/proofs/real-run-index.md).

## Strongest Evidence

- [`../../validation-lab/RUN_RESULTS.md`](../../validation-lab/RUN_RESULTS.md)
- [`../../examples/proofs/march-07-origin-refactor/review-packet/approval-decision.md`](../../examples/proofs/march-07-origin-refactor/review-packet/approval-decision.md)
- [`../../examples/proofs/coding-real-run/review-packet/approval-decision.md`](../../examples/proofs/coding-real-run/review-packet/approval-decision.md)
- [`../../evaluation/run-review-checklist.md`](../../evaluation/run-review-checklist.md)

## Confidence

Overall confidence: `medium-high`

Reason: the governance strengths are visible in both real and synthetic evidence, but the missing distinctions around distributed and late responsibility are still more diagnostic than solved.
