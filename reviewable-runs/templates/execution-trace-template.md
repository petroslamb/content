# Template: Execution Trace

Use this template when capturing what happened across one meaningful run.

Linked chapters:

- `../autonomous-agent-blueprint/core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md`
- `../autonomous-agent-blueprint/core/practical-chapter-blueprints/03-action-tool-use-blueprint.md`
- `../evaluation/run-review-checklist.md`

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
