# Reddit Experiment Ledger

## Package

- Package: `literate-workflow-programming/specification-surface-source-of-truth`
- Canonical post: `https://lambpetros.substack.com/p/the-specification-surface-is-the`
- Current Reddit mode: `thread_follow_through`
- Last updated: 2026-05-06

## Account Health

| Signal | Evidence | Decision |
| :--- | :--- | :--- |
| Recent removals or mod holds | Account has recent removals and one active `r/artificial` mod-approval hold. | Do not open another Reddit post for this package. Work the existing thread. |
| Recent native posts that stayed live | `r/aiengineering` native discussion stayed live and received views, comments, and shares. | `r/aiengineering` is the current best-fit thread. |
| Recent substantive comments in target communities | One reply in-thread was expanded to clarify the argument. | Continue comment follow-through rather than reposting. |
| Owned-link or owned-content pressure | OP has no Substack link. Held link comment remains unused. | Keep link held unless requested. |
| Current mode | Existing thread is live, but account health is fragile. | `thread_follow_through`; no new Reddit post for this package. |

## Experiments

| Date | Subreddit | Mode | Status | Title | Body Pattern | Link Placement | Metrics | Strongest Objection | Follow-Through | Next Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-05-05 | `r/aiengineering` | `post_now_native` | `live` | `Where should the source of truth live when AI agents write code?` | Native discussion question about agent intent, constraints, acceptance checks, specs, tests, and trace evidence as maintained authority surfaces. | No owned link in body. Optional Substack link held. | 2026-05-06 insight readback: 593 views, 0 upvotes, 50% upvote ratio, 3 comments, 2 shares, 0 crossposts. | A commenter dismissed the premise with `None of us are seeing this issue`. | Reply edited to expose the fake-consensus move and clarify the source-of-truth claim. OP body edited to add stronger research grounding from specification gap, professional-control, spec-driven development, harness, typed workflow, and constraint-checking work. | Watch for replies. Answer objections. Do not link unless asked. |

## Comment Work Queue

| Community | Target Behavior | Notes |
| :--- | :--- | :--- |
| `r/aiengineering` | Respond to concrete workflow objections and ask where teams keep authority surfaces. | Make the thread useful to quiet readers. |
| `r/LLM` / `r/LLMDevs` | Comment on related threads about agent workflows, reviewability, harnesses, and evaluation. | No reposting the same thesis until account health improves. |

## 2026-05-06 Live Comment Scan

Browser scan source: Reddit `/new/` feeds and selected thread pages while signed in.

| Rank | Community | Thread | Fit | Draft Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `r/LLMDevs` | [How do folks manage worktrees when working with multiple agents in parallel?](https://www.reddit.com/r/LLMDevs/comments/1t50mxb/how_do_folks_manage_worktrees_when_working_with/) | Very high | Ready | Direct fit for worktree isolation, shared contracts, authority surfaces, owned paths, and handoff state. |
| 2 | `r/artificial` | [AI is getting better at doing things, but still bad at deciding what to do?](https://www.reddit.com/r/artificial/comments/1t50i19/ai_is_getting_better_at_doing_things_but_still/) | High | Ready | Use the "continue must be earned" gate framing from the specification-surface argument. |
| Watch | `r/aiengineering` | [Where should the source of truth live when AI agents write code?](https://www.reddit.com/r/aiengineering/comments/1t3vagg/where_should_the_source_of_truth_live_when_ai/) | Existing thread | Hold | Feed is quiet; work this thread only if replies arrive. Do not repost. |
| Hold | `r/LLM` | `/r/LLM/new/` | Low | None | Feed appears semantically mixed and not a primary trust-repair surface right now. |

## Ready Native Replies

Use these as starting points only. Do not include an owned link unless someone asks for it.

### `r/LLMDevs`: Worktrees For Multiple Agents

```text
I would separate the mechanics from the authority layer.

Worktree per agent is the right isolation primitive. The harder part is giving each agent the same source of truth about what it is allowed to change, what "done" means, and what it needs to tell the next agent or reviewer.

The setup that has held up best for me:

- one worktree per task
- explicit owned paths before agents start
- a checked-in task/spec packet with acceptance checks
- an append-only notes or handoff file for assumptions, touched files, blockers, and verification
- no two agents writing the same files unless that dependency is intentional

Agents should not infer each other's state from git diff alone. Diffs show what changed; they do not preserve intent, constraints, or open questions.

For stacked PRs, I would only stack when the dependency is real. Most parallel agent work should partition by write set and merge frequently, otherwise the stack becomes a coordination substitute instead of a dependency model.
```

### `r/artificial`: Doing Vs Deciding

```text
The decision layer needs an authority surface, not just better prompts.

For every step in the workflow, the system should know:

- what context it is allowed to use
- what required fields must exist
- what ambiguity forces a pause
- what action needs approval
- what evidence has to exist before it can claim success

The failure you described is common because "continue" is the default path. On clean data that looks intelligent. On messy data it becomes silent over-execution.

I would design the workflow so "continue" has to be justified. If the model cannot name the evidence and the rule that permits the next step, the correct behavior is stop, ask, or route to review.
```

## Held Link Copy

Use only after a reader asks for the longer context or after explicit action-time confirmation.

```text
Longer write-up, if useful: https://lambpetros.substack.com/p/the-specification-surface-is-the
```
