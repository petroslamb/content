# Template: Run Trace

Use this template when capturing one agent run for debugging, evaluation, or review.

Linked chapters:

- `practical-chapter-blueprints/02-reasoning-planning-blueprint.md`
- `practical-chapter-blueprints/03-action-tool-use-blueprint.md`
- `evaluation/architecture-review-checklist.md`

```yaml
run_id: ""
task: ""
goal_state: ""
start_time: ""
end_time: ""
steps:
  - step_id: ""
    intent: ""
    observation: ""
    action_taken: ""
    tool_used: ""
    output_artifact: ""
    verification_result: ""
    error_or_retry: ""
final_result: ""
human_gate_triggered: true | false
failure_label: ""
follow_up_memory_write: ""
```
