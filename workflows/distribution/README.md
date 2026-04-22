---
workflow_id: distribution
workflow_kind: stage
stage_binding: distribution
stability: canonical
workflow_group: distribution
runner_mode: guided
default_skill: null
launch_templates: []
required_context:
  - published canonical post URL
  - package or publication distribution plan when present
  - any required platform-specific copy or media assets
expected_outputs:
  - finalized distribution copy or posting plan for the target channels
  - recorded follow-through on the channels that matter for the package
done_when:
  - the planned post-publication distribution work is complete or explicitly deferred with notes
approval_gate: required_before_external_posting
---

# Distribution

This is the canonical tracked workflow for post-publication distribution work after the Substack post is live.

Use it when the publication is ready to be adapted for downstream channels such as Notes, Reddit, LinkedIn, Hacker News, or package-specific socials.

## Purpose

This workflow exists so distribution stays attached to the package rather than drifting into one-off external posting with no local record.

The goal is not to post everywhere. The goal is to ship the channels that matter for the essay and preserve the plan locally.

## Evidence-Backed Defaults

- Start from the live published post, not from an obsolete draft.
- Use the package’s existing distribution or socials surfaces when they already exist instead of creating another parallel notes file.
- Keep channel-specific copy short, platform-aware, and traceable back to the canonical essay.
- If distribution is deliberately skipped, record that explicitly rather than leaving the stage ambiguous.

## Canonical Flow

1. confirm the published Substack post or live canonical URL
2. open the package distribution plan, socials folder, or local notes surface if one exists
3. choose only the channels that fit the piece and audience
4. adapt the framing for each channel without changing the underlying thesis
5. publish or queue the downstream copy
6. record what shipped and what was intentionally skipped

## Typical Outputs

- subreddit post drafts
- Substack Notes copy
- LinkedIn or X copy
- Hacker News title and blurb
- package-local distribution log or checklist

## Related Docs

- [`../substack-publishing/README.md`](../substack-publishing/README.md)
- package-local `distribution/` or `socials/` surfaces when present
