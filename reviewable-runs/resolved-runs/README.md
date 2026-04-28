# Resolved Runs

This store holds durable Phase 2 `resolved_run` YAML artifacts.

Persist a resolved run only when a run is governed, gated, resumable, continuous, or audit-relevant. The artifact records one workflow contract resolved against one package/run request. It is derivative execution evidence, not a new workflow contract and not package source authority.

Minimum v1 artifacts are validated by:

```bash
./content-agent validate
npm run check:workflow-model
```

Retained examples may set `retained_example: true`; active runtime code should not treat those examples as resumable pending work.
