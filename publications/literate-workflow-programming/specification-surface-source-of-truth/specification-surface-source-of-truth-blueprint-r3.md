# Hardened Blueprint

Live draft: `publications/literate-workflow-programming/specification-surface-source-of-truth/specification-surface-source-of-truth.md`
Candidate target: `publications/literate-workflow-programming/specification-surface-source-of-truth/specification-surface-source-of-truth-candidate-r3.md`
Packet manifest: `publications/literate-workflow-programming/specification-surface-source-of-truth/specification-surface-source-of-truth-essay-iteration-packet-r3.json`

## Promise

The r3 candidate should turn the r2 synthesis into a sharper public essay without reopening the object. The live claim remains narrow: AI-assisted software work becomes governable when the controlling intent lives in maintained specification surfaces that teams can review, validate, type, lint, trace, or execute against. R2 already resolved the bridge-evidence gap by using spec-driven development, the specification-gap paper, and professional-control evidence. R3 should therefore treat `publication-sharpness-gap` as a prose-execution blocker, not a research blocker. The guiding sentence is: code review without a maintained specification surface reviews the downstream artifact while leaving controlling intent ungoverned.

## Spine

1. Opening review failure: begin inside a pull request where the generated diff, tests, and agent summary are visible, but the durable statement of intended behavior is missing.
2. Source-of-truth error: name `vibe` as the failure to keep intent in a governed artifact, not as a personality insult or generic complaint about AI coding.
3. Definition: define `specification surface` as a written surface that gains authority only through maintenance, control, validation, typing, linting, trace linkage, runtime interpretation, or review.
4. Software-practice bridge: use `2602.00180` to keep spec-first, spec-anchored, and spec-as-source distinct. The essay should argue for enough specification and enforcement to expose drift, not universal spec-as-source adoption.
5. Hinge paragraph: make `2603.24284` the central proof that missing shared decisions are not a style problem. They create integration failure under partial knowledge, and restored specification detail is the strongest recovery surface in the studied setting.
6. Professional-control antagonist: use `2512.14012` to make anti-vibe concrete: experienced developers plan, supervise, validate, version, slice tasks, and apply expertise while using agents for speed.
7. Operational stack: compress the source/runtime/validation papers into one maturing pattern: specification-as-program, natural-language harnesses, typed workflows, executable constraints, prompt and protocol tests, trace checks, repair loops, and claim-level audit.
8. Caveat layer: keep context files and AGENTS.md-style instruction files metric-specific. They can become part of a specification surface when tied to control or evaluation, but passive documentation remains documentation.
9. Operator doctrine: return to the opening pull request and state what a serious review must now ask before it treats the generated diff as enough evidence.

## Paragraph burden

The opening must make the reader feel the wrong object being reviewed: the code is inspectable, but the authority that should govern the code is missing. The definition must be strict enough to exclude loose prose while broad enough to include markdown, YAML, tests, schemas, workflows, policies, traces, and claim ledgers when they actually enter a control loop. The SDD bridge must show that this is a software-work problem, not only an agent-harness problem. The specification-gap hinge must be the essay's turning point, because it converts the source-of-truth claim into a coordination failure that cannot be fixed by more confident inspection after the fact. The ending must cash out the opening scene by giving reviewers an operator standard: what governed the agent, what evidence shows conformance, and which surface changes after failure.

## Evidence burden

Body evidence:

- `2602.00180` supports the software-practice bridge and the spectrum from spec-first to spec-anchored to spec-as-source. Use it to prevent a careless all-prose or all-generation claim.
- `2603.24284` supports the central hinge: underspecification removes shared decisions, multi-agent integration suffers, conflict reports diagnose mismatches, and restored specification detail repairs the coordination surface in the studied recovery setting.
- `2512.14012` supports the professional-control contrast. It should turn `vibe` into an observed control failure rather than a cultural label.
- `2603.17399`, `2603.25723`, and `2604.13346` support specification-as-program, natural-language harnesses, and typed workflow specifications as operational forms of the surface.
- `2603.00822`, `2603.08806`, `2512.18940`, `2603.23806`, `2603.29848`, and `2602.13855` support enforcement, testing, trace validation, repair, and claim-level auditability.

Synthesis claims:

- `source of truth` is a synthesis across the bridge, harness, validation, trace, and professional-control evidence. No single paper proves the public claim by itself.
- `specification surface` is the package term. The candidate must keep its component properties visible: controlled, maintained, validated, typed, linted, trace-linked, or runtime-interpreted.
- `vibe` is useful only as the false source-of-truth regime where intent stays private or ephemeral while code becomes the only serious record.

Reference-only or caveated evidence:

- Context-file papers belong in the caveat layer, not as proof that more repository prose is automatically better.
- `2512.14805`, `2508.06942`, and `2603.15691` remain follow-on triggers only. R3 should not open new claims that require them.

## Cut order

Cut paper-by-paper exposition before cutting the opening scene, the definition, the SDD bridge, the specification-gap hinge, the professional-control paragraph, the context-file caveat, or the final operator doctrine. If the draft bloats, compress the agent-specific stack into fewer paragraphs rather than widening the bibliography. Do not cut the generated-code caveat; the essay needs it to avoid claiming that implementation no longer matters.

## Failure triggers

Void the draft pass if it says or implies that natural language is code, treats ordinary documentation or passive context files as automatically governed source-of-truth artifacts, claims generated implementation stops mattering, universalizes spec-as-source, presents richer specifications as guaranteed behavioral improvement, reuses `bridge-evidence-thinness` as the blocker without a new claim, or turns `vibe` into a generic culture-war antagonist detached from governed intent.

## Opening Lab

The opening should stay inside one scene long enough to make the failure concrete. A reviewer opens an agent-generated pull request. The diff is plausible, the tests pass, and the summary sounds orderly. The missing artifact is the maintained statement of what the change had to preserve, what the agent was allowed to change, what was out of scope, and what failure would force the specification to be revised. That is the review failure: the downstream artifact is public, while the controlling intent remains atmospheric.

Do not open with a broad claim about AI changing software. Do not open by defining `specification surface`. Do not make the first paragraph a literature review. The first reader-facing pressure is review discipline: a team cannot review authority it never made durable.

## Object Decision

Keep the object as `specification surface`. Do not rename it `contract layer`, `natural language as code`, `prompt governance`, or generic `AI coding best practices`. R3 has no warrant for a new object. The evidence already supports a disciplined source-of-truth claim when the surface is controlled, maintained, validated, typed, linted, trace-linked, or interpreted by a runtime.

## Body / Support / Footnote Ledger

| Body claim | Required support | Use mode | Boundary |
| :--- | :--- | :--- | :--- |
| Code review fails when controlling intent remains outside a governed artifact. | R2 candidate, claim-boundary ledger, `2512.14012`, `2603.24284` | Opening and thesis pressure | Do not claim code review becomes obsolete. |
| Specifications can become authoritative software artifacts. | `2602.00180`, `2603.17399`, `2604.13346` | Body | Keep spec-first, spec-anchored, and spec-as-source distinct. |
| Underspecification creates coordination failure under partial knowledge. | `2603.24284` | Hinge | Do not claim full specifications remove every coordination cost. |
| Professional agent use is control practice, not vibe delegation. | `2512.14012` | Body | Keep mechanisms concrete: planning, supervision, validation, version control, expertise, task slicing. |
| A specification surface needs enforcement or evaluation to become operational. | ContextCov, TDAD, FASTRIC, AgentPex, AgentFixer | Body | Do not treat passive docs as enough. |
| Traces, logs, tests, and claims are downstream evidence surfaces. | AgentPex, AgentFixer, `2602.13855` | Body/support | Do not make traces the upstream source of truth. |
| Context files are emerging machine-facing artifacts. | `2602.11988`, `2511.12884`, `2510.21413` | Caveat/support | Keep the mixed evidence caveat visible. |

## Second-Pass Bet

R3 should not become a broader essay. The bet is that three surgical moves can clear the publication-sharpness gap: a more concrete pull-request opening, a specification-gap hinge that names missing shared decisions as the failure mechanism, and a closing return to review practice. If those moves do not make the piece feel publishable, the next decision should be human editorial judgment, not another blind evidence pass.
