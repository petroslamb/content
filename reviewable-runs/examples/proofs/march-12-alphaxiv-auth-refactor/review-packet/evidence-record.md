# Runtime Record: Evidence Record

## Key Evidence

- the user explicitly requested a fix to the auth path and asked whether a headless browser was actually required
- assistant commentary states the intended target design before code changes: API-key-first runtime auth with explicit optional browser login
- commit `24bdff1` touched the core auth, client, CLI, docs, packaging, and test surfaces together
- the trace shows a full verification loop with initial failures, corrections, and a final clean state before commit
- the trace ends with a visible push to `origin/main`, not only a local edit

## What Actually Mattered

The run was justified by five visible facts:

- steady-state runtime auth stopped depending on browser-token refresh
- browser support was isolated behind an optional `browser` extra
- the CLI exposed an explicit API-key save path while retaining explicit browser login
- docs and metadata now matched the runtime auth story
- the final refactor passed verification strongly enough to justify a pushed commit

## What Was Omitted

The March 12 session contains later `alphaxiv-py` sub-runs about status labels, paper commands, and eventually release work. Those were omitted so this packet represents only the API-key-first auth refactor ending at `24bdff1`.
