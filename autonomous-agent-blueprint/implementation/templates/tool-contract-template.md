# Template: Tool Contract

Use this template when defining a tool the agent may call. It is intentionally structural and framework-agnostic.

Linked chapters:

- `core/practical-chapter-blueprints/03-action-tool-use-blueprint.md`
- `core/practical-chapter-blueprints/06-safety-blueprint.md`

```yaml
tool_name: ""
purpose: ""
risk_level: low | medium | high
allowed_modes:
  - read
  - write
inputs:
  - name: ""
    type: ""
    required: true
    validation: ""
outputs:
  - name: ""
    type: ""
side_effects: ""
failure_modes:
  - ""
preconditions:
  - ""
postconditions:
  - ""
approval_required: true | false
logging_requirements:
  - arguments
  - result
  - error
```
