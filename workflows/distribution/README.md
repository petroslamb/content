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
- Do not equate authentication with distribution value. Assess current account reach and likely audience before treating a channel as `post_now`; low-reach accounts need an explicit purpose, such as a referenceable anchor post plus targeted replies into existing conversations.
- When a channel rewards native media and the package already has suitable assets, prefer the native surface over a link-only post. For LinkedIn, explicitly consider PDF document carousels from slide decks before falling back to a URL preview.
- If a native-media upload requires a browser or operating-system file picker that cannot be verified through the automation surface, record the channel as `manual_upload_required` with the exact asset path, document title, copy, and fallback policy. Do not silently downgrade to a weaker link post.
- For LinkedIn document carousels, keep the canonical essay URL out of the main post body by default. Use a first comment for the URL when the goal is native carousel distribution, and verify an existing comment before adding another one.
- For LinkedIn evidence, prefer the activity URL form `https://www.linkedin.com/feed/update/urn:li:activity:<id>/` when the activity id is visible from analytics or profile activity. Record the document title and first-comment state as evidence.
- If distribution is deliberately skipped or deferred, record that explicitly rather than leaving the stage ambiguous.
- Do not treat `deferred` as a final answer when a second-wave push is requested. Reassess fit, auth state, moderation risk, and exact copy before deciding whether the channel is now `post_now`, `draft_hold`, or `skip`.
- For communities with moderation or self-promotion risk, prepare the copy locally and hold it unless the channel-specific risk has been accepted.
- For Reddit and similar forum communities, prefer native discussion posts over external-link announcements. Do not put Substack links in the post body by default; if a link is useful, prepare it as an optional comment-only follow-up that requires separate confirmation.
- Before submitting an external post, verify the visible composer contains the intended copy. If exact composer verification fails, do not post; record the channel as prepared but held with the blocker.

## Canonical Flow

1. confirm the published Substack post or live canonical URL
2. open the package distribution plan, socials folder, or local notes surface if one exists
3. choose only the channels that fit the piece and audience
4. adapt the framing for each channel without changing the underlying thesis
5. record channel fit, auth/account state, audience reach, moderation or self-promotion risk, media strategy, link-placement strategy, and the exact copy to use
6. classify each channel as `post_now`, `draft_hold`, `manual_upload_required`, or `skip`
7. publish or queue the downstream copy only after action-time approval for external posting and exact composer verification
8. for native-media posts that need a manual upload, hand off the exact asset path and resume from the profile/activity feed after the user posts
9. verify any planned first comment does not already exist before adding it
10. record what shipped, what was held as a draft, and what was intentionally skipped

## Typical Outputs

- subreddit post drafts
- Substack Notes copy
- LinkedIn or X copy
- LinkedIn document carousel PDF selection when a slide deck exists
- native-media manual upload handoff when the browser surface cannot verify the upload
- LinkedIn first-comment link copy and verification state
- Hacker News title and blurb
- channel-fit and moderation-risk table
- held Reddit or Hacker News drafts when posting risk is high
- package-local distribution log or checklist

## Related Docs

- [`../substack-publishing/README.md`](../substack-publishing/README.md)
- package-local `distribution/` or `socials/` surfaces when present
