# Runtime Record: Task Spec

## Task

Correct the `Operating Agents` YouTube course playlist order, verify whether the TL;DR playlist has the same problem, and leave both playlists in the intended chapter order.

## Objective

- inspect the live order of both playlists
- correct the course playlist if it is reversed
- avoid unnecessary changes to the TL;DR playlist if it is already correct
- use the minimum control path required to reach the intended live state
- stop only after the live playlist state is verified

## Inputs

- the user's report that the course order looked upside down
- the current YouTube playlist state
- the local YouTube API playbook and OAuth setup

## Constraints

- the run acts on a live third-party platform
- the approval/control boundary is operational, not code-based
- final verification must rely on live playlist state
- the run should prefer API control, but may use Studio if the API alone is insufficient

## Stop Condition

The course playlist is in the intended chapter order, the TL;DR playlist is confirmed correct, and the final live state is verified directly from YouTube.
