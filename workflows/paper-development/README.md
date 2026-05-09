---
workflow_id: paper_development
workflow_kind: module
stability: experimental
workflow_group: scholarship
runner_mode: guided
default_skill: null
launch_templates: []
packet_templates:
  - "workflows/paper-development/templates/paper_north_star_rubric_template.md"
  - "workflows/paper-development/templates/draftability_audit_template.md"
  - "workflows/paper-development/templates/paper_draft_approval_gate_template.md"
required_context:
  - package status
  - package README
  - source essay candidate or live draft
  - claim_boundary_ledger when present
  - package evidence surface
  - package paper folder
expected_outputs:
  - package-local paper folder README
  - package-local paper roadmap/status surface
  - paper north-star rubric before draftability audit
  - paper blueprint
  - literature mapping table when the route needs a separate appendix surface
  - case study trace plan when the route needs artifact analysis
  - draftability audit before full manuscript drafting
  - docs-only two-reviewer approval gate before manuscript drafting
  - draft manuscript when the audit allows drafting
  - references and venue checklist surfaces before submission or posting
done_when:
  - the package has a paper folder with a roadmap strong enough to decide whether to draft, harden the method, submit, post, park, or stop
approval_gate: none
---

# Paper Development

This is an experimental workflow for turning an essay argument into a viable academic-paper route.

It is not a publishing workflow. It does not submit to arXiv, OpenReview, a workshop, or a journal. It creates local paper-facing artifacts that make a paper draft possible without confusing the paper route with the public essay route.

It is also not a runner-code workflow. `content-agent` already discovers `workflows/*/workflow.yaml`; this experiment should remain YAML/docs-driven unless a later generic validator is justified across multiple paper routes.

The north-star bar is a fast-feedback ladder with a peer-review quality floor. AIware can be used for fast feedback only if the draftability gate clears it. ICSE NIER or an appropriate workshop remains the main peer-review route. arXiv waits until a complete manuscript exists and venue policy allows posting.

## Phase 2.8 Lifecycle State

State: `active_experiment`. This workflow has a governed `workflow.yaml` with `stability: experimental`, and the 2026-05-09 proof campaign invoked it on `publications/proof-runs-as-source-surface` with run id `phase-2-8-proof-paper-development-proof-runs`. That run produced retained evidence, but its terminal status was `deferred`, so it is not a clean promotion proof and this workflow is not a canonical/default route.

## Trigger

Use this workflow when a package has a strong essay candidate or live draft, but the next goal is an academic paper rather than Substack publication.

The workflow is appropriate when the paper needs:

- a proposed title and abstract
- a contribution statement
- paper type and venue route
- a taxonomy or model
- evidence mapping
- a concrete case-study or artifact-analysis plan
- limitations and forbidden framing

If the task is only to improve the essay, stay in [`../essay-iteration/README.md`](../essay-iteration/README.md).

## Core Rule

The paper route must add a concrete scholarly contribution.

An essay can supply the motivating argument, but it is not enough. The workflow should force the paper to name at least one of:

- a definition
- a taxonomy
- a lifecycle or process model
- a systematization table
- a case study or artifact analysis
- a benchmark or empirical method

For the current `specification surface` paper, the intended minimum is framework + systematization + illustrative artifact analysis.

## Filesystem Shape

Paper artifacts live in a package-local folder:

```text
publications/<package>/paper/
```

Use that folder for:

- `README.md`
- paper roadmap/status surface
- paper north-star rubric
- paper blueprint
- publication route notes
- literature mapping appendix
- case-study trace notes
- draftability audit
- docs-only two-reviewer approval gate
- extended abstract
- draft manuscript
- references and venue checklists

Do not add more paper-route files to the leaf root unless the package README needs a pointer.

## Experimental Phases

Use these phases to organize what is done and what remains:

1. **Route setup**: create the paper folder, roadmap, blueprint, publication route, evidence map, case-study trace, and extended abstract when justified.
2. **Rubric setup**: create or update the paper north-star rubric before the audit runs.
3. **Draftability audit**: decide whether the route is strong enough to draft, should harden the method, should aim for a later venue, or should stop.
4. **Approval gate**: require two independent reviewer verdicts before manuscript drafting starts.
5. **Method hardening**: convert the case-study trace into a real method surface with unit of analysis, artifact corpus, coding scheme, observations, and non-claims.
6. **Manuscript draft**: write a Markdown draft before TeX conversion or venue formatting.
7. **Venue packet**: prepare references, artifact availability language, figures or tables, and the target checklist.
8. **Submission decision**: decide whether to submit, post to arXiv, hold, or park.

## Working Sequence

1. Resolve package context from `status.yaml`, package `README.md`, and the active essay candidate or live draft.
2. Load the evidence surface and claim-boundary artifacts.
3. Create or update the package-local `paper/` folder.
4. Create or update the package-local roadmap before adding new paper artifacts.
5. Create or update the paper north-star rubric.
6. Draft a paper blueprint before drafting prose.
7. Record the publication or review route when arXiv, OpenReview, workshops, or journals are under consideration.
8. Build an evidence mapping table that ties sources to paper roles rather than broad literature-review commentary.
9. Define the case-study or artifact-analysis plan.
10. Draft an extended abstract only after the blueprint has a concrete contribution and case-study or method path.
11. Run a draftability audit against the rubric before full manuscript drafting.
12. Run the docs-only two-reviewer approval gate.
13. Harden the method if the audit or approval gate finds the case-study trace too thin.
14. Draft the manuscript and venue packet only after both reviewers approve the same drafting route.

## Output Standard

A viable paper blueprint must include:

- proposed title
- abstract draft
- contribution statement
- paper type
- venue or preprint route
- category recommendation when arXiv is under consideration
- full outline
- taxonomy or model, when relevant
- evidence mapping table
- case-study, artifact-analysis, benchmark, or method plan
- risks and limitations

A viable draftability audit must decide one of:

- `approve_aiware_sprint`
- `approve_peer_review_short_paper`
- `hold_for_method_hardening`
- `park_paper_route`

## North-Star Rubric And Approval Gate

Use a 0-2 rubric across six dimensions:

- scholarly contribution
- evidence and literature fit
- case-study/method spine
- claim discipline and forbidden-frame avoidance
- venue/feedback readiness
- reviewability and artifact traceability

Hard caps:

- any forbidden framing violation blocks approval
- no case-study unit or corpus caps the score at 7
- no literature or evidence map caps the score at 7
- treating arXiv as peer review blocks approval
- arXiv route approval is blocked without manuscript, references, method, artifact statement, and checklist

Gate decisions:

- `approve_aiware_sprint`: score is at least 9; scholarly contribution is 2; claim discipline is 2; case-study/method spine is at least 1; both reviewers approve the same route.
- `approve_peer_review_short_paper`: score is at least 10; scholarly contribution, evidence, method, and claim discipline are all 2; both reviewers approve the same route.
- `hold_for_method_hardening`: route is promising but method or evidence is not strong enough for drafting.
- `park_paper_route`: contribution remains essay-shaped, the paper violates hard caps, or the route no longer justifies continued work.

Two-reviewer approval:

- Reviewer A owns scholarship, evidence, and method.
- Reviewer B owns venue fit, paper shape, and reviewability.
- Both reviewers must independently approve the same route before manuscript drafting starts.
- A split verdict blocks drafting; revise the audit or method and rerun the approval gate.

A viable submission packet must include:

- manuscript draft
- references
- method section
- artifact availability language
- venue-specific checklist

## Rejection And Parking

Default rejection policy: park it.

If this workflow is rejected:

- keep package-local `paper/` artifacts as useful notes;
- mark the package-local roadmap or workflow README as parked;
- remove the workflow from the active workflow map if it should no longer be advertised;
- do not delete the blueprint, route research, literature map, case trace, or extended abstract unless a later artifact supersedes them;
- do not patch `content-agent` for the rejected experiment.

If this workflow succeeds across more than one paper package, consider promoting it from `experimental` to a stable scholarship workflow.

## Boundaries

Do not use this workflow to claim:

- arXiv is peer review
- OpenReview is acceptance
- a strong essay is already a research contribution
- a pure position paper is the default route
- a pure literature review is enough for a preprint

For paper routes derived from essays, keep the public-essay path and academic-paper path visibly separate.
