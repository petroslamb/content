# Gates

This store holds concrete Phase 2 `review_gate` YAML artifacts.

A gate artifact is a durable stop/resume object. It must link to the run record, the resolved run when one exists, package evidence, validation results, enforcement outcomes, and the exact approval dimensions being requested.

Quality approval, external mutation approval, lifecycle movement approval, and promotion approval are separate booleans. A content-quality approval does not imply external mutation approval.

Minimum v1 artifacts are validated by:

```bash
./content-agent validate
npm run check:workflow-model
```

Retained examples may set `retained_example: true`; active runtime code should not treat those examples as pending operator decisions.
