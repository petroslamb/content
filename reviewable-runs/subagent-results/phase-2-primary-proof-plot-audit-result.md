---
kind: subagent_result
schema_version: 1
request_id: phase-2-primary-proof-plot-audit
agent_id: 019dff3c-00c5-7a60-a858-5d4451f6375e
agent_nickname: Einstein
agent_type: default
fork_context: false
reasoning_effort: high
completed_at: '2026-05-07T00:00:00+03:00'
request_path: reviewable-runs/subagent-requests/phase-2-primary-proof-plot-audit-request.yaml
---
# Phase 2 Primary Proof Plot Audit

## Verdict

The root cause was **drafting**, not topic discovery or package-init. Topic discovery preserved a clear editorial object: proof runs as the trust surface, bounded against "agents can publish themselves" and benchmark-score claims.

Evidence:

- [topic-discovery handoff, line 51](../logs/phase-2-primary-topic-discovery-proof-topic-discovery-handoff.md): the topic is framed as governed proof runs becoming the trust surface between declared specifications and autonomous action.
- [topic-discovery handoff, line 274](../logs/phase-2-primary-topic-discovery-proof-topic-discovery-handoff.md): the handoff says the claim must remain bounded to a governed local runtime path to gate, not autonomous external publication reliability.
- [candidate slate, line 38](../logs/phase-2-primary-topic-discovery-proof-candidate-essay-slate.md): "Agents can now autonomously publish" is explicitly blocked as an overclaim.

## Where The Draft Broke

The draft initially follows that plot, but loses editorial control by turning into a system-defense memo and then leaving visible scaffold residue. The clearest hard failure is the duplicate/template tail: after a complete `Limits` and `References` section, the candidate repeats `## Limits`, `## References`, and instruction text meant for drafting, not publication.

Evidence:

- [candidate, line 63](../../publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md): the real `## Limits` section starts.
- [candidate, line 97](../../publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md): a duplicate `## Limits` scaffold section remains after the references.

That is where the editorial plot visibly breaks.

There is also a subtler drafting drift: the handoff's evidence frame centered the Phase 2 proof run and a specific shortlist. The candidate's research section swaps in a different support set and reads more like runtime-governance justification than a reader-facing essay argument.

Evidence:

- [topic-discovery handoff, line 278](../logs/phase-2-primary-topic-discovery-proof-topic-discovery-handoff.md): proposed slug and package idea are carried forward.
- [topic-discovery handoff, line 280](../logs/phase-2-primary-topic-discovery-proof-topic-discovery-handoff.md): initial paper shortlist is specified.
- [candidate, line 31](../../publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md): the research section starts.
- [candidate, line 85](../../publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md): the references section includes the substituted support set.

## Later Missed Checks

Review is the major downstream failure. It declares no `P0`, calls the candidate structurally coherent, and says promotion is blocked by policy rather than content, despite the template residue and evidence drift.

Evidence:

- [replacement review, line 22](../../publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-replacement-review-r1.md): the review says the candidate clears the live-draft replacement comparison.
- [replacement review, line 28](../../publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-replacement-review-r1.md): the review says `P0`: none.
- [replacement review, line 40](../../publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-replacement-review-r1.md): the review gives high structural coherence.

Gate semantics then compounded the miss by treating the issue as `draft_only` policy, not failed editorial readiness.

Evidence:

- [decision, line 18](../../publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-decision-r1.md): the decision says promotion is blocked by policy.
- [decision, line 22](../../publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-decision-r1.md): the required follow-through routes to gate checks rather than editorial correction.
