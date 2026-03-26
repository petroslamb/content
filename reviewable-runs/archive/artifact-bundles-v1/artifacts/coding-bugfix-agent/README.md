# Artifact Guide: Coding Bugfix Agent

Read these files in order:

1. `input-brief.md`
   The reported bug, task scope, and engineering constraints.
2. `planner-trace.md`
   The inspect -> patch -> test -> review loop.
3. `state-or-evidence-record.md`
   The files inspected, the evidence found, and the working hypothesis.
4. `verification-report.md`
   The concrete checks and test results that justify the patch.
5. `approval-record.md`
   The point where merge stays human-governed.
6. `failure-review.md`
   The plausible miss even after the target test passes.

This bundle is meant to show why coding-agent correctness comes from environment feedback and verification scope, not from confident prose.

Treat these files as examples of the records a serious coding agent should emit or be able to reconstruct, not as extra commentary around the case.
