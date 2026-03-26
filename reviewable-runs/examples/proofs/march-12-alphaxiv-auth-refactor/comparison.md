# Raw Trace Vs Review Packet

Use this file to compare the March 12 `alphaxiv-py` auth refactor in two modes:

1. curated raw session artifacts
2. reconstructed review packet

## Raw Trace Only

The raw trace shows the user request, the coding work, the verification loop, and the final commit and push. That is enough to recover the broad story, but three things still take extra reviewer effort:

- separating the auth refactor from the neighboring `alphaxiv-py` sub-runs in the same long session
- understanding which parts of the broad diff were core to the run versus productization support work
- seeing that the run ended at a pushed commit rather than only a local code change

## Review Packet

The packet makes these things explicit:

- the bounded task: API-key-first runtime auth with browser login demoted to an explicit optional path
- the evidence that the runtime path, docs, metadata, tests, and publish surfaces all moved together
- the actual verification sequence, including failed intermediate checks and the final green state
- the approval boundary: commit `24bdff1` pushed to `origin/main`
- the most plausible failure: auth semantics and docs drifting apart again in later changes

## Practical Difference

| Question | Raw trace only | Review packet |
| --- | --- | --- |
| What was the task? | mixed with adjacent productization discussion | explicit API-key-first auth refactor |
| What happened? | reconstructable with effort | explicit coding and verification sequence |
| What did it rely on? | spread across status, diff, and source reads | explicit evidence record |
| How was it checked? | visible, but spread across several tool outputs | explicit test/lint/type-check summary |
| Who approved impact? | commit and push are visible, but implicit | explicit pushed-commit boundary |
| What failed or could fail? | mostly implied | explicit auth-drift control gap |

## Bottom Line

For this run, the packet earns its cost by separating one real engineering sub-run from the larger March 12 session and by making the verification and approval boundary substantially easier to review.
