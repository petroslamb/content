# Failure And Friction Review

## Summary

The publication finished. The proof trail is reconstructable. The runtime proof is not yet clean enough to claim fully autonomous Phase 2 lifecycle execution.

## Friction Table

| Problem | Class | Corrective Direction |
| :--- | :--- | :--- |
| Lifecycle evidence is spread across package files, lightweight logs, browser readbacks, and later Phase 2 records. | `source-trace confusion` | Use this proof packet as the retained bridge; future lifecycle proof should use one declared proof workflow or a linked chain of `content-agent` runs. |
| Some decisive work happened before the final `content-agent` migration. | `contract gap` | Do not retrofit false runtime evidence. Mark the proof as retrospective/hybrid. |
| `content-agent` defers before `codex_session` steps instead of launching constrained agents. | `runtime gap` | Phase 3 should add agent-handoff execution for non-scriptable steps, with declared context, allowed write paths, and output validation. |
| External publication/distribution effects are proven by logs and readbacks, not replayed. | `external mutation` | Keep external verification as readback evidence; do not rerun external mutation for proof aesthetics. |
| Distribution experiments introduced side paths and channel-specific state. | `context overload` | Keep the distribution log as the source for channel outcomes; separate later Reddit/engagement experiments from the core publication proof where possible. |

## What Worked

- Package state is explicit and complete.
- Release gate approval is tracked.
- Publish and archive logs are concrete.
- Distribution outcomes are channel-specific.
- Phase 2 validation can read the completed package.

## What Did Not Work As Strict Phase 2 Proof

- No single `content-agent` run owns the full lifecycle.
- No formal Phase 2 review gate exists for every external mutation.
- Non-scriptable drafting, polish, and distribution steps were guided by Codex/browser work rather than executed by the deterministic runtime.

## Required Hardening

For a stricter future proof, add one of:

1. a `content-agent` proof workflow that chains lifecycle segment records, or
2. a proof-campaign convention that links one resolved run per major lifecycle segment.

Either option should preserve this rule:

> source truth remains in package artifacts and workflow contracts; proof records reconstruct what happened without becoming the new source of truth.
