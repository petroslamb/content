---
workflow_id: expert_feedback_outreach
workflow_kind: module
stability: experimental
workflow_group: distribution
runner_mode: guided
default_skill: null
launch_templates: []
packet_templates:
  - "workflows/expert-feedback-outreach/templates/outreach_tracker_template.md"
required_context:
  - package status
  - package README
  - published canonical post URL
  - source essay candidate or live draft
  - package evidence surface or papers index
  - existing distribution or outreach tracker when present
expected_outputs:
  - package-local expert feedback outreach tracker
  - paper author target map
  - paper-specific message pack
  - outcome retrospective after the success window
done_when:
  - the package has a bounded paper-author outreach experiment with exact drafts, manual-send boundary, and outcome tracking
approval_gate: none
---

# Expert Feedback Outreach

This is an experimental workflow for targeted paper-author outreach after publication.

It is not a traffic workflow. Treat outreach as an expert-feedback loop: the useful outcomes are replies, objections, corrections, weak ties, later collaboration, or a clearer sense that the essay frame is not landing with the people whose work it cites. Clicks are incidental.

## Trigger

Use this workflow after a Substack essay is published and the essay has cited papers, source papers, or explicit boundary-case papers whose authors could usefully pressure-test the argument.

Do not use it for broad audience growth, generic influencer lists, cold sales, or bulk distribution. If the target is a channel rather than a cited-paper author, use [`../distribution/README.md`](../distribution/README.md) instead.

## Core Rule

V1 targets paper authors only.

Eligible targets are:

- authors of cited papers that carry real argumentative weight
- authors of papers used as explicit boundary cases, stress tests, or negative examples
- authors whose paper is named in the essay/source surface even if it is not the central load-bearing citation

Do not add people only because they are famous, adjacent, or likely to amplify the post.

## Operating Boundaries

- Cap each essay batch at 5-10 targets.
- Do not scrape contacts, automate sending, mass-DM people, bypass platform limits, or use replacement accounts.
- External sends are outside this workflow. The workflow prepares and records copy; the user sends manually or gives explicit action-time approval with the exact destination and copy.
- Connection requests should not carry the essay link by default. A connection request can introduce the shared area, but the essay belongs in a post-acceptance message.
- Post-acceptance messages must name the recipient's paper, state exactly how the essay used it, and ask for one objection or correction.
- Put the essay link after the ask, not as the opening payload.
- Record outcomes even when nothing happens. Silence is experimental data.
- For LinkedIn batches, inspect and record the visible action state before sending anything: `connect`, `follow`, `message`, `2nd`, `3rd+`, and mutual connections when visible. If the account has recent outreach risk or uncertain limits, send at most 5 initial invites or messages per day unless the user explicitly approves a different pace.
- After any approved LinkedIn action, record the action evidence separately from the attempt: `invite_sent_without_note`, `invite_sent_with_note`, `message_sent`, `blocked_at_confirmation`, `premium_or_inmail_block`, `pending_visible`, or `connect_still_visible`. Do not mark a target as invited only because the invite modal opened.

## Canonical Flow

1. Resolve the package status, package README, published canonical URL, essay/source draft, and evidence surface.
2. Open any existing package-local distribution or outreach tracker. Preserve it and adapt in place rather than duplicating historical records.
3. Define the experiment hypothesis, message variant, target batch, success window, and decision after the window.
4. Build a 5-10 person target map from cited or boundary-case paper authors.
5. Record each paper's role in the essay and why that author is a good feedback target.
6. Draft the message pack with exact text for each target or variant.
7. Stop before external sending. If the user sends manually or gives explicit action-time approval, update the tracker afterward with dates, exact action evidence, and outcomes.
8. Review the batch after the default 14-day success window and decide whether to continue, revise the message, pause, or retire that target type.

## Standard Tracker

Use this package-local path:

```text
publications/<package>/distribution/expert-feedback-outreach.md
```

If a package already has a tracker, preserve the historical records and adapt the existing file in place when it is clearly the same experiment. If the existing tracker is platform-specific, keep it as history and link it from the standard tracker.

Every tracker must record:

- hypothesis: what the outreach is testing
- target batch: 5-10 paper authors
- message variant: `generic`, `paper_specific`, or `reply_follow_up`
- success window: default 14 days after message send
- decision after window: `continue`, `revise_message`, `pause`, or `retire_target_type`

## Message Rule

Default post-acceptance message shape:

```text
Hi <name> - I write Rooted Layers, a publication about how AI systems, software practice, and research ideas turn into operational constraints.

I used your paper, "<paper title>", in a recent essay as <exact paper role in the essay>.

The essay argues <one-sentence thesis>. I would value one objection or correction, especially if you think I used the paper too broadly or missed an important limitation.

<canonical essay URL>
```

This is a pattern, not a script. The live message should be short, specific, and honest about what the essay borrowed from the paper.

## Outcome Meanings

Useful outcomes include:

- `accepted`: the connection request was accepted
- `message_sent`: the paper-specific message was sent manually or with explicit approval
- `reply`: the target replied
- `objection`: the target identified a disagreement or limitation
- `correction`: the target corrected a source use, framing, or claim
- `weak_tie`: the contact is now reachable for a later related piece
- `collaboration`: the exchange produced a follow-up call, quote, review, or project
- `no_reply`: the success window elapsed without a reply

Do not score the experiment by traffic unless a later distribution workflow explicitly studies traffic.

## Stop And Retirement Rules

Pause or retire a target type when:

- the batch gets no replies across the success window and the message does not contain a clear paper-specific ask
- the outreach starts to resemble promotion instead of expert feedback
- platform limits or account health make further messages risky
- the essay's use of the paper is too thin to justify contacting the author
- a correction shows the essay or local source surface needs repair before further outreach

If a reply raises a material correction, route the essay or archive repair through the appropriate editorial, publishing, or archive-sync workflow before continuing the batch.

## Command Surface

Validate the workflow with:

```bash
./content-agent validate --workflow expert_feedback_outreach --package <package>
```

Run a guided pass with:

```bash
./content-agent run --workflow expert_feedback_outreach --package <package>
```

This workflow has an external mutation budget of zero. A guided run validates context and then hands off to a Codex session for tracker creation, target selection, message drafting, and retrospective notes. It can prepare and record outreach, but it must not send LinkedIn messages, emails, comments, or DMs by itself.

## Related Docs

- [`../distribution/README.md`](../distribution/README.md)
- [`../release-gate/README.md`](../release-gate/README.md)
- package-local `distribution/` trackers when present
