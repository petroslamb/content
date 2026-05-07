# Subagent Repair Prompt

Validation failed for:

- `reviewable-runs/subagent-results/result-run-2026-05-07T15-06-34Z-agent-harnesses-topic-discovery-state-discovery-trigger.md`

The validator reported that each `findings[]` item must be line-grounded with `path` or `file` plus `line`. The current artifact uses `source`.

Read only the original request, the current result artifact, and declared allowed inputs. Repair only the result artifact at the same path by replacing each finding's `source` key with an accepted `path` key, preserving the line numbers and meaning. Do not expand the scope or inspect undeclared files.
