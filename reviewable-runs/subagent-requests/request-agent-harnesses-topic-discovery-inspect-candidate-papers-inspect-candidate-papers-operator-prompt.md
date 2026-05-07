# Subagent Prompt

Read only this request artifact and the allowed input declared inside it:

- `reviewable-runs/subagent-requests/request-agent-harnesses-topic-discovery-inspect-candidate-papers-inspect-candidate-papers.yaml`

Do not use parent conversation context. Do not inspect undeclared files. Do not perform workflow steps beyond `inspect_candidate_papers`.

Use the admitted topic vocabulary map and deterministic public alphaXiv paper inspection commands as needed. Do not use assistant/authenticated/mutating commands.

Write the declared workflow output exactly to:

- `reviewable-runs/logs/agent-harnesses-topic-discovery-inspect-candidate-papers-candidate-paper-pool.md`

Write the requested subagent result artifact exactly to:

- `reviewable-runs/subagent-results/result-agent-harnesses-topic-discovery-inspect-candidate-papers-inspect-candidate-papers.md`

The result must satisfy the request's `result_requirements`, including YAML frontmatter with matching request metadata, repeated source hashes, an allowed verdict, and line-grounded findings using `path` or `file` plus `line`.
