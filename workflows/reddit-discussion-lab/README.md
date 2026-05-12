---
workflow_id: reddit_discussion_lab
workflow_kind: module
stability: experimental
workflow_group: distribution
runner_mode: guided
default_skill: null
launch_templates: []
packet_templates:
  - "workflows/reddit-discussion-lab/templates/reddit-discussion-lab-template.md"
required_context:
  - package status
  - package README
  - live draft, published post, or candidate essay
  - existing package-local distribution or Reddit ledger when present
  - observed Reddit examples and current account-health state
expected_outputs:
  - package-local Reddit discussion lab tracker
  - post idea inventory
  - tone and engagement-mechanics analysis
  - scored native post drafts
  - approval and posting plan
  - outcome readback after posting or comment follow-through
done_when:
  - the package has at least three scored Reddit-native discussion seeds and a clear post, hold, or comment-first decision
approval_gate: required_before_external_posting
---

# Reddit Discussion Lab

This is an experimental distribution workflow for turning Rooted Layers essays into Reddit-native discussion prompts.

The purpose is not to summarize the essay. The purpose is to find the live problem inside the essay that a subreddit already knows how to discuss.

Use this workflow when a package has a strong argument but the Reddit version is landing as a thesis announcement, a coined-frame pitch, or a lightly disguised external post.

## Phase 2.8 Lifecycle State

- State: `active_experiment`
- Governed contract: `present` - adjacent `workflow.yaml` has `stability: experimental` and is explicitly invokable through `content-agent`.
- Proof runs: `deferred_only` - `phase-2-8-proof-reddit-discussion-confidently-wrong`, `phase-2-8a-stress-reddit-discussion-confidently-wrong-2026-05-11`, and `phase-2-8a-stress-reddit-discussion-confidently-wrong-2026-05-11-start-at-tracker` ran on `publications/evidence-governance/your-ai-is-confidently-wrong-and` and retained evidence, but terminal status was `deferred`.
- Promotion status: `not_candidate` - not canonical, not default-routed, and not promotion-ready.
- Promotion blockers: needs two clean real-package governed proof run ids plus explicit human approval text; deferred proof-campaign evidence does not count as clean promotion proof.

## Core Finding

The successful 2026-05-06 Reddit comment pass worked because the target threads were already shaped as live community problems. They invited experience, disagreement, and debugging detail before asking anyone to accept a concept.

The reusable shape is:

```text
live problem -> concrete distinction -> open question
```

Do not lead with the coined frame. Lead with the failure scene or operator problem that makes the frame necessary.

## Interest Mechanics

A Reddit post is more likely to get comments when readers can participate without reading the essay.

Strong posts usually have:

- an immediate failure scene, operator pain, or weird behavior
- a title that asks about something readers have seen
- low activation energy: a reader can answer from experience
- one concrete distinction that makes the thread smarter
- enough tension for disagreement without sounding like bait
- no owned link in the body
- no demand that readers accept a new term before the problem is clear

Weak essay-derived Reddit posts usually fail because they lead with:

- the publication frame
- an abstract noun
- a conclusion
- a polished title that sounds like an article headline
- too many claims before the question
- evidence before the reader has a reason to care

## Reddit Voice

Use the companion Reddit-native voice rule from [`../distribution/reddit-native-distribution.md`](../distribution/reddit-native-distribution.md).

For this lab, the practical style is:

- short, mostly lowercase when natural, and conversational
- concrete before conceptual
- one useful distinction per post
- no article cadence
- no title-case thesis title
- no generic hype or outrage
- no deliberate fake typos, fake roughness, or deceptive humanizing

The goal is native and useful, not artificially sloppy.

## Canonical Flow

1. Resolve the package, live draft or published post, and current Reddit/account-health state.
2. Open [`examples.md`](examples.md) and identify 3-5 relevant working examples.
3. Extract the engagement mechanics from those examples: title pattern, problem type, participation invitation, and tone.
4. Mine the essay for failure scenes, operator questions, surprising distinctions, and places where readers can answer from experience.
5. Convert the essay frame into at least five problem-first title candidates.
6. Draft at least three native post bodies using the shape `observed problem -> one distinction -> open question`.
7. Score each seed with the discussion-spark rubric.
8. Decide `post_now_native`, `comment_first`, `draft_hold`, or `skip`.
9. Stop before external posting. External posting requires action-time approval and exact composer verification.
10. After posting or commenting, record the outcome: upvotes, comments, strongest objections, replies worth answering, and next action.

## Discussion-Spark Rubric

Score each seed from 0-3 on each axis.

| Axis | 0 | 3 |
| :--- | :--- | :--- |
| Problem concreteness | abstract thesis | recognizable incident or workflow pain |
| Answerability | requires accepting the essay | readers can answer from their own experience |
| Subreddit fit | generic AI discourse | matches live community behavior |
| Tension | flat agreement prompt | arguable but not hostile |
| Distinction value | repeats common take | adds one useful technical frame |
| Native voice | article headline or promo | casual, short, thread-native |
| Link risk | needs the essay to make sense | stands alone without owned links |

Default threshold:

- 18+ points: candidate for `post_now_native`
- 14-17 points: revise or use as a comment
- below 14 points: hold

## Package Tracker

Use this package-local path:

```text
publications/<package>/distribution/reddit-discussion-lab.md
```

If the package already has a Reddit experiment ledger, keep the ledger as the event record and use the discussion lab tracker for pre-drafting, scoring, and retrospective notes.

Use [`templates/reddit-discussion-lab-template.md`](templates/reddit-discussion-lab-template.md) when starting a new tracker.

## Output Standard

Every run should leave behind:

- examples consulted
- lessons borrowed from those examples
- essay source frame
- failure scenes or operator problems mined from the essay
- title candidates
- three scored native post drafts
- posting decision and approval boundary
- outcome readback when a post or comment goes live

## Stop Rules

Stop or hold when:

- the only available title is the essay title
- the body needs an owned link to make sense
- the post asks for agreement rather than experience
- the target subreddit has active moderation or self-promotion risk and the account is already fragile
- the draft depends on fake casualness, outrage, or using another commenter as the topic
- the post would duplicate a recent thread where a comment would be better

## Related Docs

- [`examples.md`](examples.md)
- [`seed-bank.md`](seed-bank.md)
- [`../distribution/README.md`](../distribution/README.md)
- [`../distribution/reddit-native-distribution.md`](../distribution/reddit-native-distribution.md)
