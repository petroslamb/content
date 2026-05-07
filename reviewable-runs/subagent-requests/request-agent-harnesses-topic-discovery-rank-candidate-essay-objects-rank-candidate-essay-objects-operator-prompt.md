# Subagent Prompt

Read only this request artifact and the allowed input declared inside it:

- `reviewable-runs/subagent-requests/request-agent-harnesses-topic-discovery-rank-candidate-essay-objects-rank-candidate-essay-objects.yaml`

Do not use parent conversation context. Do not inspect undeclared files. Do not perform workflow steps beyond `rank_candidate_essay_objects`.

Use the admitted ranked paper pool and runtime input `target_publication_ambition: north_star_flagship`. The request shows `assistant_discussion_notes` as a missing output target; do not fabricate assistant notes and do not run assistant/authenticated/mutating commands.

Write the declared workflow output exactly to:

- `reviewable-runs/logs/agent-harnesses-topic-discovery-rank-candidate-essay-objects-candidate-essay-slate.md`

Write the requested subagent result artifact exactly to:

- `reviewable-runs/subagent-results/result-agent-harnesses-topic-discovery-rank-candidate-essay-objects-rank-candidate-essay-objects.md`

The result must satisfy the request's `result_requirements`, including YAML frontmatter with matching request metadata, repeated source hashes, an allowed verdict, and line-grounded findings using `path` or `file` plus `line`.
