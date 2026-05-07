# Subagent Prompt

Read only this request artifact and the allowed inputs declared inside it:

- `reviewable-runs/subagent-requests/request-run-2026-05-07T15-06-34Z-agent-harnesses-topic-discovery-state-discovery-trigger.yaml`

Do not use parent conversation context. Do not inspect undeclared files. Do not perform workflow steps beyond the request scope.

Write the requested subagent result artifact exactly to:

- `reviewable-runs/subagent-results/result-run-2026-05-07T15-06-34Z-agent-harnesses-topic-discovery-state-discovery-trigger.md`

The result must satisfy the request's `result_requirements`: include YAML frontmatter with `kind: subagent_result`, `schema_version: 1`, matching `request_id`, `package`, `workflow`, `run`, an allowed `verdict`, repeated `source_hashes`, and line-grounded `findings`. Keep the body concise and limited to the requested step.
