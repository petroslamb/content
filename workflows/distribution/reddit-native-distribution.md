# Reddit Native Distribution

Use this companion playbook when a publication has a plausible Reddit audience.

The operating rule is:

```text
Do not distribute essays on Reddit. Distribute community-native arguments, then let the essay absorb demand.
```

## Channel Modes

Every Reddit target must be placed in one of these modes before drafting:

| Mode | Use When | Action |
| :--- | :--- | :--- |
| `post_now_native` | Account is healthy, subreddit fit is strong, and the post is a standalone discussion. | Prepare and submit a native post after approval. |
| `draft_hold` | The argument is plausible but subreddit fit, timing, or moderation risk is unclear. | Keep a local draft; do not submit. |
| `trust_repair` | Recent posts are removed, stuck in mod approval, or the account looks self-promotional. | Stop posting owned-content threads; rebuild community participation. |
| `skip` | No community-native argument exists. | Do not force Reddit distribution for this essay. |

Do not create a new Reddit account to bypass removals, mod queues, bans, karma limits, or reputation problems.

## Account Health Gate

Before any Reddit post, record:

- recent removals or mod-approval holds
- target subreddit karma/account-age requirements if visible
- recent ratio of owned-link or owned-content posts to non-promotional comments
- last 5-10 comments in the target community, if any
- whether the account has recent substantive participation unrelated to the current essay

If recent posts are repeatedly removed or waiting for approval, default to `trust_repair`.

## Trust Repair Track

When in `trust_repair`, the workflow goal is not traffic. The goal is to make the account legible as a real community participant.

Minimum repair plan:

- no new posts linking to or promoting owned surfaces for at least 7 days
- 5-10 substantive comments in the target community or adjacent communities
- comments should answer questions, correct errors, add sources, or ask informed follow-ups
- no generic praise, no drive-by comments, no repeated mention of the publication
- after the repair window, post only one native discussion in one carefully selected subreddit

If the target subreddit is strict or ambiguous, prepare a concise modmail pre-clearance draft. Sending modmail is external communication and requires action-time confirmation.

## Native Argument Preflight

A Reddit post is eligible only when it has all of the following:

- a concrete technical or operational contradiction
- 2-3 evidence points that stand alone without the essay
- one arguable thesis that knowledgeable readers can disagree with
- one sincere question for the community
- a body that reads like a person opening a discussion, not a polished abstract
- no Substack URL in the post body by default

Bad Reddit seed:

```text
I wrote an essay about specification surfaces in AI-assisted software work.
```

Better Reddit seed:

```text
AI-generated PRs can pass tests while nobody can name the controlling spec. Where should the source of truth live?
```

## Link Placement

Default policy:

- no Substack link in the post body
- optional link comment only after the native post is live
- link comment requires separate confirmation
- if the post is gaining organic discussion, prefer answering comments first and linking only when someone asks for more context

If the subreddit explicitly bans self-promotion or external links, do not post the link comment.

## Follow-Through

For the first 24 hours, distribution means comment work:

- answer objections directly
- concede valid corrections
- add sources only when they help the thread
- avoid sounding like a prepared campaign
- turn strong objections into future essay or follow-up post candidates

Record comment URLs when they materially advance the discussion.

## Experiment Log

Every Reddit experiment should record:

- subreddit
- post mode
- title
- body pattern
- link placement
- approval/removal status
- mod response, if any
- comment count and strongest objections
- Substack traffic impact
- podcast/audio impact when available
- decision for the next Reddit attempt
