# Validation Results

This file records the first pass of the existing `reviewable-runs` framework against the 12 synthetic validation-lab cases.

Method:

- run-level judgment used `../evaluation/run-review-checklist.md`
- architecture-level judgment used `../evaluation/architecture-readiness-checklist.md`
- unanswered-question counts refer to the six review questions, not the longer architecture checklist

These results are synthetic. They are useful for checking whether the framework behaves coherently across clean, weak, and edge cases. They are not substitute proof.

## Summary

The framework behaved as intended on the first pass.

- all 4 validate cases landed `Strong` and `Accept`
- all 4 invalidate cases landed `Weak`; 3 required `Revise` and 1 required `Reject`
- all 4 stress-test cases landed `Partial`; 3 required `Revise` and 1 required `Reject`
- the clearest passes came from bounded runs with explicit evidence, verification, and governance timing
- the clearest failures came from missing evidence provenance, missing state verification, and ambiguous or absent approval context
- the most contested area was partial reconstruction over long or split runs

## Case Results

| Case ID | Run-review result | Architecture-readiness result | Unanswered review questions | Result vs expected | Notes |
| --- | --- | --- | --- | --- | --- |
| `coding_bugfix_complete_review` | Strong | Accept | 0 | matched | clean bounded coding run with full six-question coverage |
| `enterprise_policy_memo_with_freshness_controls` | Strong | Accept | 0 | matched | strongest high-risk case because freshness and approval are both explicit |
| `web_form_pre_submit_review` | Strong | Accept | 1 | matched | browser state evidence is strong enough because submission is held before impact |
| `support_triage_with_clear_nonapproval_reason` | Strong | Accept | 1 | matched | framework handles explicit "approval not required" cleanly when risk stays internal |
| `coding_trace_only_no_evidence_record` | Weak | Revise | 2 | matched | visible trace cannot replace a preserved evidence basis |
| `enterprise_publish_without_approval_context` | Weak | Reject | 3 | matched | strongest negative case; high-impact publish path without clear approval fails outright |
| `web_success_message_without_state_verification` | Weak | Revise | 2 | matched | success UI without persisted-state proof is not enough |
| `memory_heavy_run_without_provenance` | Weak | Revise | 3 | matched | provenance and freshness gaps dominate the whole run |
| `multi_agent_handoff_contamination` | Partial | Revise | 2 | matched | framework exposes contamination well, but does not yet rank upstream vs downstream blame sharply |
| `long_horizon_partial_reconstruction` | Partial | Revise | 3 | matched at upper bound | framework tolerates partial reconstruction, but confidence drops quickly once early trace loss compounds |
| `conflicting_evidence_and_verification_split` | Partial | Revise | 1 | matched | one of the best stress tests; framework can represent disagreement without collapsing into confusion |
| `retroactive_approval_ambiguity` | Partial | Reject | 2 | matched | run is reconstructable, but governance timing still fails the architecture standard |

## What The Framework Catches Reliably

The framework is already good at three kinds of failure.

First, it catches missing evidence support. The coding trace-only case and the memory-heavy provenance case both fail for the right reason: visible activity is not enough when the run cannot show what actually mattered.

Second, it catches verification theater. The weak web case has a clean UI success moment and still fails, because the verification question is not "did the interface smile back" but "was the intended state actually checked."

Third, it catches governance ambiguity. The enterprise publish case and the retroactive approval case both show that approval timing matters, not just approval language. The framework does not treat a late or implied signoff as equivalent to a clean gate.

## Where The Framework Is Directionally Right But Still Loose

The long-horizon partial-reconstruction case shows the main current softness. The framework can say "Partial" and "Revise," which is correct, but it is less crisp about how much reconstruction loss is still acceptable before the run should be treated as effectively weak.

The multi-agent handoff case shows a second softness. The framework can surface contaminated handoffs, but it still needs a stronger way to talk about attribution across agents. Right now it explains the problem better than it prioritizes the fix.

The conflicting-evidence case is a better outcome. There the framework behaves well because both evidence and verification are visible, so the disagreement itself becomes reviewable instead of mysterious.

## Practical Reading Of The Results

The validation lab suggests the current framework is strong enough for three real uses:

- rejecting runs that only have traces, success signals, or output polish
- defending approval gates for high-impact actions
- escalating ambiguous but reconstructable runs instead of forcing false certainty

The lab also suggests the current framework still needs sharper policy for:

- partial reconstruction thresholds
- multi-agent attribution and handoff responsibility
- how to score "reviewable but contested" runs more precisely than `Partial`

## Bottom Line

The first synthetic pass supports the framework's core claim.

The six-question model reliably separates clean runs from weak runs, and it handles edge cases without collapsing into raw intuition. The current limitation is not basic coherence. The limitation is calibration: the framework still needs crisper thresholds for degraded traces, contested evidence, and split responsibility.
