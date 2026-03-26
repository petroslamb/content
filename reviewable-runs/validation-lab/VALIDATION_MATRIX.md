# Validation Matrix

Use this file to see the full first synthetic wave in one place.

| Case ID | Synthetic agent | Class | Risk tier | Primary claim tested | Expected run-review result | Expected architecture-readiness result | Expected unanswered questions band |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `coding_bugfix_complete_review` | `coding_bugfix_agent` | validate | medium | complete six-question coverage improves review | Strong | Accept | `0-1` |
| `enterprise_policy_memo_with_freshness_controls` | `enterprise_policy_agent` | validate | high | evidence freshness and approval context matter | Strong | Accept | `0-1` |
| `web_form_pre_submit_review` | `web_form_agent` | validate | high | state evidence and pre-submit approval can be made reviewable | Strong | Accept | `0-1` |
| `support_triage_with_clear_nonapproval_reason` | `support_triage_agent` | validate | medium | medium-risk runs can be explicit without heavy governance | Strong | Accept | `0-1` |
| `coding_trace_only_no_evidence_record` | `coding_bugfix_agent` | invalidate | medium | traces alone are not enough | Weak | Revise | `2-3` |
| `enterprise_publish_without_approval_context` | `enterprise_policy_agent` | invalidate | high | high-impact output without approval context should fail review | Weak | Reject | `2-4` |
| `web_success_message_without_state_verification` | `web_form_agent` | invalidate | high | visible success without state verification is not enough | Weak | Revise | `2-3` |
| `memory_heavy_run_without_provenance` | `support_triage_agent` | invalidate | medium | evidence freshness and provenance are mandatory when retrieval dominates | Weak | Revise | `2-4` |
| `multi_agent_handoff_contamination` | `multi_agent_research_pipeline` | stress-test | high | structured-looking handoffs can still be unsafe | Partial | Revise | `1-3` |
| `long_horizon_partial_reconstruction` | `release_gate_agent` | stress-test | medium | reconstruction limits become visible on long uneven traces | Partial | Revise | `1-3` |
| `conflicting_evidence_and_verification_split` | `release_gate_agent` | stress-test | high | reviewer judgment matters when evidence and checks disagree | Partial | Revise | `1-2` |
| `retroactive_approval_ambiguity` | `release_gate_agent` | stress-test | high | late or retroactive approval should not count as clean governance | Partial | Reject | `1-3` |
