# Hardened Blueprint

Live draft: `publications/literate-workflow-programming/specification-surface-source-of-truth/specification-surface-source-of-truth.md`
Candidate target: `publications/literate-workflow-programming/specification-surface-source-of-truth/iterations/r2/specification-surface-source-of-truth-candidate-r2.md`
Packet manifest: `publications/literate-workflow-programming/specification-surface-source-of-truth/iterations/r2/specification-surface-source-of-truth-essay-iteration-packet-r2.json`

## Promise

The r2 candidate should argue that AI-assisted software work is exposing a source-of-truth inversion: the durable governing artifact is no longer always the generated implementation, but the maintained specification surface that constrains, validates, coordinates, or authorizes that implementation. The r2 bridge is now stronger than r1 because three locally intaken papers carry the public-world burden: `2602.00180` shows specifications becoming contracts and source artifacts in general software practice, `2603.24284` shows underspecification as a measurable coordination failure in code agents, and `2512.14012` shows experienced developers rejecting vibe practice in favor of planning, supervision, validation, version control, and expertise. The essay must still avoid the forbidden claim that natural language is code. The allowed thesis is narrower: controlled, maintained, typed, linted, validated, trace-linked, or runtime-interpreted specification surfaces can become source-of-truth artifacts when they enter the control loop.

## Spine

1. Opening pressure: start from a professional failure mode, not from terminology. A generated change arrives with passing tests, but the governing intent lives in chat, a vague ticket, or one user's private prompt. The review object is therefore wrong.
2. Definition: name `specification surface` as the maintained artifact where intent becomes public, reviewable, and operational. Exclude loose prose, stale design docs, ordinary README text, and one-off prompts unless they are connected to control, validation, typing, linting, runtime interpretation, or traceability.
3. General software bridge: use `2602.00180` to move outside the agent-harness niche. Spec-driven development supplies a spectrum from spec-first to spec-anchored to spec-as-source, with validation and human review as the discipline that keeps the spec authoritative rather than advisory.
4. Coordination proof: use `2603.24284` to show what happens when shared decisions are missing. Stripped specifications cause multi-agent integration failure; the full specification is the strongest recovery instrument; conflict reports diagnose but do not replace the missing specification.
5. Professional-control antagonist: use `2512.14012` to sharpen `vibe` into a source-of-truth error. Experienced developers use agents for acceleration while preserving design control, validation, version control, task decomposition, and supervision.
6. Source/runtime/validation stack: use `2603.17399`, `2603.25723`, `2604.13346`, `2603.00822`, `2603.08806`, `2512.18940`, `2603.23806`, `2603.29848`, and `2602.13855` to show the specification surface maturing from prose into harnesses, workflow languages, executable constraints, tests, trace checks, and claim-evidence ledgers.
7. Caveat layer: keep AGENTS.md and context-file claims metric-specific. Context files are evidence of machine-facing project artifacts, not proof that more repository prose automatically improves agent behavior.
8. Operator doctrine: close by distinguishing source surfaces from derived evidence. Generated code, tests, traces, logs, and reports still matter, but teams must decide which upstream surfaces carry authority and maintain those surfaces accordingly.

## Paragraph burden

The opening must make the reader feel the cost of reviewing only the generated diff when the real intent artifact is missing. The definition section must give a usable exclusion test: a surface earns authority only when it can change or check what the system does. The SDD bridge must prove that this is a software-engineering shift, not only an agent orchestration pattern. The specification-gap paragraph must make underspecification concrete as missing shared decisions, not generic prompt weakness. The professional-control paragraph must turn anti-vibe from a slogan into observed practice. The body stack must preserve r1's mechanism while compressing paper-by-paper exposition. The caveat section must protect the essay from context-file boosterism. The ending must leave an operator standard for what teams should maintain, review, lint, validate, trace, and dispute before code generation becomes the only record of intent.

## Evidence burden

Body evidence:

- `2602.00180` carries the broad software-practice bridge. Use its spectrum and workflow, especially spec-first, spec-anchored, spec-as-source, specify/plan/implement/validate, drift control, and the minimum-rigor caveat.
- `2603.24284` carries the negative coordination proof. Use the reported degradation from detailed specifications to bare signatures, the persistent multi-agent coordination gap, and the finding that full specifications recover performance more than post-hoc conflict reports.
- `2512.14012` carries the professional-control bridge. Use field observations and survey findings that experienced developers control design and implementation through planning, supervision, validation, version control, limited task slices, and expertise.
- `2603.17399`, `2603.25723`, and `2604.13346` carry the source/runtime evidence: specification-as-program, natural-language harnesses, and typed workflow specifications.
- `2603.00822`, `2603.08806`, `2512.18940`, `2603.23806`, `2603.29848`, and `2602.13855` carry enforcement, testing, trace validation, repair, and claim-level auditability.

Synthesis claims:

- `source of truth` is a synthesis across SDD, harness, validation, trace, and professional-control evidence. No single paper proves the whole public claim.
- `specification surface` is a package term. Papers support parts of it, but the essay must keep the component claims visible.
- `vibe` is useful only as the false proxy for ungoverned intent. It should not become a cultural complaint detached from source-of-truth authority.

Reference-only or caveated evidence:

- `2512.14805`, `2508.06942`, and `2603.15691` remain queue papers unless the r2 candidate needs more breadth.
- AGENTS.md and context-file papers belong in the caveat layer. Use them to show emergence and risk, not automatic benefit.

## Cut order

Cut local donor history first, then optional spec-diff discussion, then broad context architecture material, then repeated explanation of generated code as downstream. Preserve the opening scene, definition, three bridge paragraphs, one compressed source/runtime/validation stack, caveats, and operator doctrine. If length grows, use fewer papers with clearer argumentative jobs instead of widening the bibliography.

## Failure triggers

Return to blueprint hardening if the candidate says or implies that natural language is code, treats ordinary documentation as automatically governed, claims generated implementation no longer matters, claims richer specification automatically improves behavior, turns into generic vibe-coding commentary, loses the negative context-file caveat, or uses SDD to imply that every team should adopt spec-as-source. Stop and reconsider the object if r2 still cannot make the broader software-practice bridge visible after using the three locally intaken bridge papers.

## Opening Lab

The opening should use a concrete review failure:

A team accepts an agent-generated change because the diff is plausible and the tests pass. The reviewer can see the implementation, but not the durable statement of what the feature was supposed to preserve, what assumptions were settled, what validation mattered, or what the agent was not allowed to change. The source-of-truth problem begins there. The code is visible, but the controlling intent is not.

Avoid opening with an abstract claim about AI changing software. Avoid opening with a dictionary definition of `specification surface`. The first turn should make `vibe` look like a governance failure: intent is treated as atmosphere until generated code becomes the only artifact left for serious review.

## Object Decision

Keep the object as `specification surface`, not `contract layer`, `natural language as code`, or generic `AI coding best practices`. The r2 evidence supports the same object with a stronger bridge. `2602.00180` licenses a general software-practice axis, `2603.24284` supplies the failure mechanism, and `2512.14012` supplies the professional antagonist. The essay should therefore revise the same object rather than narrow to agent harnesses or reopen pivot search.

## Body / Support / Footnote Ledger

| Body claim | Required support | Use mode | Boundary |
| :--- | :--- | :--- | :--- |
| Specifications can become authoritative software artifacts. | `2602.00180`, `2603.17399`, `2604.13346` | Body | Do not universalize spec-as-source. Keep spec-first and spec-anchored visible. |
| Underspecification causes coordination failure. | `2603.24284` plus trace/validation papers | Body | Do not claim full specifications eliminate every coordination tax. |
| Professionals do not govern agents by vibe. | `2512.14012` | Body | Do not turn the article into a culture-war piece. Keep the control mechanisms concrete. |
| Specification surfaces need enforcement or evaluation. | `2603.00822`, `2603.08806`, `2512.18940`, `2603.23806`, `2603.29848` | Body | Do not say passive docs are enough. |
| Claim and trace evidence are downstream validation surfaces. | `2602.13855`, AgentPex, AgentFixer | Body/support | Do not promote logs into the source of truth. |
| Context files are emerging machine-facing artifacts. | `2602.11988`, `2511.12884`, `2510.21413` | Caveat/support | Keep the mixed-evidence caveat visible. |

## Second-Pass Bet

The second-pass bet is that r2 should feel less like an agent-systems survey and more like a software-work doctrine. The main revision move is to make the bridge evidence alter the reader's belief: code review without a maintained specification surface reviews the downstream artifact while leaving the controlling intent ungoverned.
