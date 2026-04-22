---
kind: object_ceiling_report
package: "$package_key"
revision: $revision
live_draft_path: "$live_draft_path"
terminal_candidate_path: "$candidate_path"
terminal_replacement_review_path: "$replacement_review_path"
terminal_decision_path: "$decision_path"
dominant_blocker_slug: ""
ceiling_verdict: pending
effort_verdict: pending
next_route: pending
---
# Ceiling Report

Live draft: `$live_draft_path`
Terminal candidate: `$candidate_path`
Terminal replacement review: `$replacement_review_path`
Terminal decision: `$decision_path`
Packet manifest: `$packet_manifest_path`

## Verdict

State whether this flagship object has actually capped out and why.

## Iteration Chronology

Summarize the meaningful revision sequence, not every tiny edit.

## Blocker Timeline

State which blocker changed, which blocker persisted, and what the stop gate actually proved.

## Effort Audit

Say whether the iterations tried hard enough to justify a stop or whether a real move was skipped.

## What Survived

- 

## What Did Not Survive

- 

## Lessons Learned

- 

## Next Route

Choose one of: `post_ceiling_pivot`, `publish_non_flagship`, `shelve`, and justify it.
