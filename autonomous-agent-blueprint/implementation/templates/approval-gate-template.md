# Template: Approval Gate

Use this template when a workflow requires human approval before side effects.

Linked chapters:

- `core/practical-chapter-blueprints/06-safety-blueprint.md`
- `implementation/use-cases/enterprise-agent.md`
- `implementation/use-cases/web-agent.md`

```yaml
gate_name: ""
trigger_condition: ""
action_class: ""
required_evidence:
  - ""
required_checks:
  - ""
approver_role: ""
approval_question: ""
rollback_notes: ""
log_fields:
  - proposed_action
  - evidence
  - approver_decision
  - timestamp
```
