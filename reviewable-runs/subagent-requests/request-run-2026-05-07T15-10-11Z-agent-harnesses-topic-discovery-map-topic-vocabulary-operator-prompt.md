# Subagent Prompt

Read only this request artifact and the allowed inputs declared inside it:

- `reviewable-runs/subagent-requests/request-run-2026-05-07T15-10-11Z-agent-harnesses-topic-discovery-map-topic-vocabulary.yaml`

Do not use parent conversation context. Do not inspect undeclared files. Do not perform workflow steps beyond `map_topic_vocabulary`.

Use the request runtime input `discovery_trigger: agent harnesses` and the allowed alphaXiv skill guidance. Run only deterministic alphaXiv retrieval needed to map topic and paper-search vocabulary.

Write the declared workflow output exactly to:

- `reviewable-runs/logs/run-2026-05-07T15-10-11Z-agent-harnesses-topic-discovery-topic-vocabulary-map.md`

Write the requested subagent result artifact exactly to:

- `reviewable-runs/subagent-results/result-run-2026-05-07T15-10-11Z-agent-harnesses-topic-discovery-map-topic-vocabulary.md`

The result must satisfy the request's `result_requirements`, including YAML frontmatter with matching request metadata, repeated source hashes, an allowed verdict, and line-grounded findings using `path` or `file` plus `line`.
