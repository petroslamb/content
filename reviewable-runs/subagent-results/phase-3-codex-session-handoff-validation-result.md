---
kind: subagent_result
schema_version: 1
request_id: phase-3-codex-session-handoff:validation
agent_type: worker
completed_at: '2026-05-07'
request_path: reviewable-runs/subagent-requests/phase-3-codex-session-handoff-validation-request.yaml
---
# Phase 3 Codex Session Handoff Validation Result

## Scope

This is a read-mostly critique and validation plan. I read the required governance surfaces: `AGENTS.md`, `AUTHORITY.md`, `gate_contracts.yaml`, `harness_policy.yaml`, `workflows/essay-iteration/workflow.yaml`, and the Phase 2 subagent result files. I also counted the repo-wide workflow surface to judge expansion risk from the current narrow prototype.

No implementation files were edited.

## Counts

| Surface | Count | Notes |
| :--- | ---: | :--- |
| Workflow YAML files | 16 | `workflows/*/workflow.yaml` |
| Gate contracts | 7 | `topic_viability`, `research_exit`, `essay_prewrite`, `replacement_north_star`, `pivot_research_grounding`, `pivot_north_star_viability`, `release_readiness` |
| Workflow gate declarations | 14 | Across 10 workflows; `release_readiness` is reused by 8 gate declarations |
| `codex_session` steps | 60 | Repo-wide across workflow YAML files |
| `codex_session` steps in `essay_iteration` | 3 | `harden_blueprint`, `write_bounded_candidate`, `run_cold_replacement_review` |
| `codex_session` steps producing gated outputs | 9 | These are the high-risk generic-expansion surface |
| `codex_session` steps with a step-level `gate` | 2 | `essay_iteration.write_bounded_candidate`, `youtube_production.record_video_handoff` |
| Explicit `agent_contract` handoffs | 1 | `essay_iteration.run_cold_replacement_review`, contract `essay_iteration.cold_replacement_review.v1` |

The 9 `codex_session` gated-output hotspots are:

- `article_polish.place_images` and `article_polish.final_editorial_pass`, producing `polished_live_draft` gated by `release_readiness`.
- `distribution.record_distribution_follow_through`, producing `distribution_follow_through_log` gated by `release_readiness`.
- `essay_iteration.harden_blueprint`, producing `plot_contract` gated by `essay_prewrite`.
- `essay_iteration.write_bounded_candidate`, producing `candidate_draft` gated by `essay_prewrite`.
- `essay_iteration.run_cold_replacement_review`, producing replacement-review artifacts gated by `replacement_north_star`; this is the only current explicit `agent_contract`.
- `post_ceiling_pivot.record_pivot_decision`, producing `pivot_decision` gated by `pivot_north_star_viability`.
- `release_gate.inspect_release_surfaces`, producing `release_gate_checklist` gated by `release_readiness`.
- `youtube_production.record_video_handoff`, producing `video_handoff_note` gated by `channel_mutation_boundary`.

## Cold Replacement Review Assessment

The Phase 2 prototype is correctly narrow. Its useful property is not that a `codex_session` became a subagent. Its useful property is that the gate-critical critic step has a declared request/result/integration shape, source hashes, required sections, allowed verdicts, and a blocking relationship to `replacement_north_star`.

The proof run also exposes the main constraint for generic expansion: the cold reviewer failed the known lost-plot candidate, but it also reported that `plot_contract` was missing from the allowed inputs. That is good fail-closed behavior for a gate-critical contract. Generic handoffs must not soften that rule into "best effort context" when the result is used to clear a gate.

## Validation Matrix

| Case | Minimum deterministic assertion | Expected outcome before broad use |
| :--- | :--- | :--- |
| Current explicit request emission | Running into `essay_iteration.run_cold_replacement_review` emits exactly one subagent request, records the request path in the run record, and defers before the step. | Pass required. No model execution inside `content-agent`. No gate approval implied. |
| Request schema and path bounds | Request has declared kind/schema/request/workflow/run/package identity, expected artifact paths, allowed input paths, and source hashes. Paths remain under declared workflow write surfaces. | Pass required. Any missing identity, out-of-bounds path, or artifact collision blocks. |
| Known bad candidate proof | The existing lost-plot proof candidate with scaffold residue and evidence drift receives `verdict: fail`. | Pass required. A generic handoff system that allows this to pass is not acceptable. |
| Missing required context | A gate-critical request with missing `plot_contract` or required source input cannot produce a gate-clearing pass. | Pass required. Missing declared context must be blocking for gate-critical contracts. |
| Stale source result | Change or simulate changed packet/live/candidate hashes after request/result generation. | Validator and gate reject as stale. |
| Bad verdict enum | Result uses an undeclared verdict or omits verdict. | Validator rejects. Gate remains blocked. |
| Missing result sections | Result omits required sections such as source hashes, line-grounded findings, scaffold residue check, drift check, or unresolved blockers. | Validator rejects for explicit contracts. |
| Integration mismatch | Integration decision references an unknown result, accepts a non-pass result, accepts and rejects the same result, or uses an undeclared decision. | Validator rejects. Gate remains blocked. |
| Gate blocking semantics | `replacement_north_star` blocks unless packet validation passes, cold-review result is current and `pass`, and integration decision accepts the pass. | Pass required. Positive prose alone cannot clear the gate. |
| Generic non-gate handoff | A `codex_session` with no gated output and no lifecycle/promotion/external mutation role can emit or accept a generic handoff artifact without changing gate status. | Pass required before generic expansion. Generic artifacts must be trace only unless explicitly bound. |
| Generic cannot satisfy gate | A generic `codex_session` result is present for a step that produces or feeds gated outputs but lacks explicit `agent_contract`. | Gate must ignore or reject it as gate evidence. It may inform the parent, but it cannot unblock. |
| Multiple handoffs in one run | Two generic handoffs and one explicit contract in the same run get unique request/result paths and trace entries. | Pass required. No overwrites, no request/result cross-link confusion. |
| Legacy artifact tolerance | Existing Phase 2 or older subagent result files that are not tied to a generated request remain non-blocking. | Pass required. Compatibility should not create hidden gate evidence. |
| Policy boundary | A generic handoff tries to authorize promotion, lifecycle movement, release, publish, or external mutation. | Must fail or be ignored. Only declared gates and explicit approvals can authorize those boundaries. |

## Generic Versus Explicit Handoff Classification

| Handoff type | Safe as generic execution? | Contract requirement |
| :--- | :--- | :--- |
| Exploration, framing, vocabulary mapping, local synthesis, candidate slates, package-local notes | Yes | Generic is acceptable when outputs are not gate-clearing and not external/lifecycle/promotion authority. |
| Deterministic tool orchestration or inspection notes | Yes, but prefer scriptable where possible | Generic result is trace evidence only; deterministic validators remain authoritative. |
| Continuity-heavy drafting or local artifact preparation | Yes for execution, no for acceptance | The draft/artifact may be produced generically, but readiness must be judged by validators or explicit gate-critical review. |
| Independent critic, auditor, or reviewer whose result blocks or clears a gate | No | Requires explicit `agent_contract`, fresh source hashes, required sections, allowed verdicts, and integration decision. |
| Lifecycle movement: topic viability, research exit, pivot grounding, pivot north-star viability | No | Requires explicit gate-critical contract or existing review-gated artifact. Generic handoff must not initialize packages, advance stages, or open successor leaves. |
| Promotion or replacement decisions | No | Requires explicit gate-bound result plus integration decision, as proven by cold replacement review. |
| Release, publish, channel mutation, distribution posting, live publish | No | Requires explicit release/external-mutation gate handling. Generic handoff cannot authorize remote mutation. |
| Missing-input or stale-input gate evidence | No | Gate-critical contracts must fail closed on missing or stale declared inputs. |

## Expansion Risks

- Genericizing all 60 `codex_session` steps would erase the difference between ordinary execution trace and gate evidence. That would recreate the Phase 2 failure mode: a plausible review artifact masking content blockers.
- `release_readiness` is reused by 8 workflow gate declarations. A weak generic release handoff would have a larger blast radius than the current `replacement_north_star` prototype.
- The current prototype depends on integration decisions. If generic results are consumed directly by gates, rubber-stamped model output can bypass parent accountability.
- Clean-context independence can become false advertising if generic handoffs inherit the parent conversation while claiming to be independent.
- Missing context must stay visible. The cold proof's missing `plot_contract` finding is a useful fail-closed signal, not a nuisance to hide.
- Stale source hashes are the easiest deterministic regression to miss when broadening path templates and request/result naming.
- Generic handoff artifacts can create path sprawl and collisions unless request/result paths include run id, step id, and contract id, and existing files fail rather than overwrite.
- External mutation workflows have a different risk profile from editorial workflows. Publishing, playlist changes, live posting, and channel mutation should remain outside generic execution.
- YAML must not become a hidden prompt language. Contracts should declare admissible inputs, success/failure criteria, result shape, and gate binding, not unreviewable model instructions.

## Recommended Next Gate-Critical Contract

After the cold replacement review, the next gate-critical contract should be a release-readiness audit on `release_gate.inspect_release_surfaces`, tentatively:

`release_gate.release_readiness_audit.v1`

Rationale: `release_readiness` is the most reused and highest-blast-radius gate. It protects publication, sync, archive, distribution, and channel-mutation boundaries. Adding one explicit audit contract at the central `release_gate` module is more valuable than converting another drafting step, because it hardens the boundary immediately before external mutation without pretending that the model approves publication.

Minimum contract shape:

- `task_type: auditor`
- clean declared-file context: package status, package README, canonical live draft, latest promotion/publication approval note, artifact/media surface, references/links/Substack target, release-gate README/templates, `harness_policy.yaml`, and `gate_contracts.yaml`
- result verdicts: `pass`, `fail`, `defer`, `stale`
- required result sections: target identity, approval provenance, reference/link check, media-path check, publication-target check, external-mutation boundary check, line-grounded blockers, source hashes checked, unresolved blockers
- integration decisions: `accept_pass`, `accept_fail`, `reject_stale`, `reject_out_of_scope`, `defer_for_fixes`
- gate binding: a `pass` result plus accepted integration decision may be required input to `release_readiness`, but it must not itself approve publication or remote mutation

I would not make `essay_iteration.write_bounded_candidate` the next gate-critical contract. Drafting benefits from continuity, and the safer architecture is to let drafting remain generic execution while explicit critics and release auditors decide whether outputs can move through gates.
