---
kind: essay_iteration_prewrite_gate
package: "literate-workflow-programming"
revision: 1
judgment_policy: "draft_only"
live_draft_path: "publications/literate-workflow-programming/literate-workflow-programming.md"
candidate_path: "publications/literate-workflow-programming/literate-workflow-programming-candidate-r1.md"
writability_verdict: writable
candidate_authorized: true
dominant_blocker_slug: ""
supporting_artifact_paths:
  - publications/literate-workflow-programming/claim-ledger.md
  - publications/literate-workflow-programming/contradiction-register.md
  - publications/literate-workflow-programming/claim-scorecard.md
---
# Essay Prewrite Gate

Live draft: `publications/literate-workflow-programming/literate-workflow-programming.md`
Candidate target: `publications/literate-workflow-programming/literate-workflow-programming-candidate-r1.md`
Packet manifest: `publications/literate-workflow-programming/literate-workflow-programming-essay-iteration-packet-r1.json`

## Promise

Authorize a bounded essay that argues workflow specifications become meaningful source artifacts for agent systems only when they are coupled to validation gates, policy enforcement, and semantic debugging traces. The candidate may use "literate workflow programming" as the synthesis label, but it must immediately narrow that frame to the source/validation/trace stack and keep claim-level provenance as the next missing layer rather than a current repo capability.

## Spine

1. Opening problem: narrow the overbroad "markdown as code" framing into a stricter workflow-specification claim.
2. Specification surface: show how workflow specs, harnesses, and declarative agent languages make the source layer inspectable.
3. Validation hinge: explain that validators, policy checks, and enforcement gates are what connect those specs to reality.
4. Trace stack: separate execution traces and reviewable runs from the source of truth while showing why they still matter.
5. Provenance boundary: state that contradiction transparency and claim-level provenance are the next layer, not a solved repo property.
6. Skills boundary: keep skills as a bounded supporting layer with portability caveats visible.
7. Conclusion: restate the usable synthesis without promoting parked claims such as import semantics, package-as-object semantics, or repo-wide validator promotion.

## Paragraph burden

- The opening must reject passive-markdown maximalism and establish the narrowed claim.
- The specification section must anchor the essay in workflow specs and harness contracts, not generic context engineering.
- The validation section must make validation load-bearing, not a trailing implementation detail.
- The trace section must keep the spec/trace hierarchy explicit: traces debug source-linked drift but do not replace source.
- The provenance section must name the missing layer honestly and keep contradiction transparency visible.
- The skills section must remain one bounded support section, not become the center of the article.
- The conclusion must restate the synthesis and its limits in a way that does not smuggle in parked claims.

## Evidence burden

Body-work sources:
- `2603.25723`, `2604.13346`, `2603.17399`, `2603.00822` for workflow specs, externalized harnesses, specification primacy, and executable constraints.
- `2603.29848`, `2603.23806`, `2602.13855` for validation as lifecycle infrastructure, trace evaluation, and claim-level provenance.
- `2510.04173`, `2512.19769`, `2512.18940`, `2603.20380`, `2504.11703` for portability, declarative workflow surfaces, conformance limits, and policy enforcement.

Package-local support surfaces:
- `claim-ledger.md` for claim state and boundaries.
- `contradiction-register.md` for authority rules and caveats.
- `claim-scorecard.md` for article-ready claim selection.
- `literate-workflow-programming-blueprint-r1.md` for the narrowed promise and section burden.

Reference-only or bounded supporting material:
- skills portability papers and the workflow-as-namespace bridge.
- local `spec-diff` proof as a bounded source/evidence drift example, not as broad conformance proof.

Synthesis-only claims:
- "literate workflow programming" as the essay label.
- the stack mapping from source, validator, trace, and provenance layers onto the repo.

## Cut order

1. Cut broad framing about literate programming history before cutting the source/validation/trace stack.
2. Compress the skills section into one bounded paragraph before cutting the main proof path.
3. Compress context-file caveats into one sentence when they start to dominate the lead.
4. Cut extended namespace discussion before cutting the validation hinge or provenance boundary.
5. Keep the claim-level provenance boundary visible, but cut detail before turning it into a side essay.

## Failure triggers

- The candidate starts claiming markdown alone is executable or sufficient as source.
- The source/trace hierarchy collapses and run logs are treated as primary artifacts.
- `spec-diff` is used as proof of broad behavioral conformance instead of bounded drift detection.
- The draft implies current repo skills are already portable production substrate.
- The article drifts into package-as-object semantics, markdown import semantics, or repo-wide validator promotion.
- Claim-level provenance is described as already implemented rather than as the next missing layer.

## Claim-State Gate

The prewrite verdict is justified by tracked claim-state surfaces, not by ad hoc notes:

- [`claim-ledger.md`](claim-ledger.md) narrows the public claim to workflow specifications plus validation, policy, and traces, and keeps stronger metaphors parked or caveated.
- [`contradiction-register.md`](contradiction-register.md) resolves the load-bearing tensions around literate-programming framing, markdown enforcement, spec-vs-trace hierarchy, and provenance scope.
- [`claim-scorecard.md`](claim-scorecard.md) marks CSA-C1, CSA-C2, CSA-C3, CSA-C5, CSA-C6, and CSA-C7 as article-ready, with CSA-C4 admitted only with explicit caveat.

These tracked surfaces are strong enough to authorize a bounded candidate as long as the draft stays inside the article-ready claim set and keeps the registered caveats visible.

## Writability Verdict

The essay is writable at the current target bar. `candidate_authorized: true` is justified because the package now has:

- a hardened blueprint with a narrowed promise and section spine
- a tracked claim ledger that distinguishes article-ready claims from parked ones
- a tracked contradiction register that resolves the main framing tensions
- a tracked claim scorecard that authorizes the lead, validation hinge, trace hierarchy, drift-proof example, and provenance-boundary claims

The candidate is authorized only as a bounded draft carrying the article-ready claim set. Skills remain caveated support, and parked claims stay out of the body.

## Required Follow-Through

1. Draft the bounded candidate using CSA-C1, CSA-C2, CSA-C3, CSA-C5, CSA-C6, and CSA-C7 as the load-bearing claims.
2. Keep CSA-C4 as a bounded support claim with portability and selection caveats visible.
3. Keep imports, package-as-object semantics, and repo-wide validator promotion out of the draft body.
4. Run the replacement review, scorecard, and decision surfaces after the candidate is written.
5. Use `npm run check:essay-iteration -- --package literate-workflow-programming` once the remaining packet artifacts are filled.
