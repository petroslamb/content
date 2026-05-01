# Hardened Blueprint

Live draft: `publications/literate-workflow-programming/literate-workflow-programming-flagship/literate-workflow-programming.md`
Candidate target: `publications/literate-workflow-programming/literate-workflow-programming-flagship/iterations/r1/literate-workflow-programming-candidate-r1.md`
Packet manifest: `publications/literate-workflow-programming/literate-workflow-programming-flagship/iterations/r1/literate-workflow-programming-essay-iteration-packet-r1.json`

## Promise

This essay argues that workflow specifications become meaningful source artifacts for agent systems only when they are coupled to validation gates, policy enforcement, and semantic debugging traces. That narrower frame survives pressure because it does not depend on the grander claim that markdown itself is executable or that "literate programming for agents" is already a settled category. The package evidence now supports a stricter stack: workflow specs as the visible source surface, validation as lifecycle infrastructure, traces as debugging records rather than source of truth, `spec-diff` as a bounded local proof of source-linked drift detection, and claim-level provenance as the next missing layer. The essay should therefore make the architecture legible without overstating portability, conformance, or repo-wide maturity.

## Spine

1. Opening problem: the repo is drifting toward a programming model, but the original "markdown as code" framing is too loose.
2. Specification surface: workflow specs, harness contracts, and natural-language workflow languages make the source-like layer inspectable.
3. Validation hinge: validation, policy enforcement, and contradiction checks are what attach those specs to reality.
4. Trace stack: reviewable runs, AgentPex/AgentFixer-style evaluation, and `spec-diff` show how traces debug source-linked drift without replacing source.
5. Provenance boundary: claim-level provenance is the next layer, and the current repo only partially reaches it.
6. Skills and namespace boundary: skills belong as a bounded support layer, not as the main proof of the article.
7. Conclusion: literate workflow programming is a synthesis label for the source/validation/trace stack, not a license for passive markdown sprawl.

## Paragraph burden

- Opening problem: separate the useful architecture claim from the overbroad metaphor. The opening must establish why "context engineering" is too broad and why passive markdown is not enough.
- Specification surface: show that the repo and the literature both have inspectable workflow surfaces, then narrow the claim to specifications that a runtime can interpret.
- Validation hinge: explain that validation is not a terminal test pass. It spans policy checks, drift checks, contradiction checks, and lifecycle gating.
- Trace stack: establish the source/trace hierarchy clearly. The reader should leave this section knowing why logs are useful and why they are still derivative artifacts.
- Provenance boundary: explain what the current stack still lacks, using contradiction transparency and claim-level provenance as the explicit missing capability.
- Skills and namespace boundary: keep the bridge to `illusion-of-swarm`, but prevent the article from turning into a generalized skills essay.
- Conclusion: restate the usable synthesis and the repo-level consequence without promoting parked claims like import semantics or repo-wide validator policy.

## Evidence burden

Body-work sources:
- `2603.16021` for folder-structured staged context and the future-work pressure toward semantic debugging and source integrity.
- `2603.25723`, `2604.13346`, `2603.17399`, `2603.00822` for the source/runtime split, harness externalization, and specification primacy.
- `2510.04173`, `2512.19769`, `2512.18940`, `2603.20380`, `2504.11703`, `2601.04748` for specification languages, conformance, policy enforcement, and the bounded skills bridge.
- `2603.23806`, `2603.29848`, `2602.13855` for trace evaluation, validation-as-lifecycle, and claim-level provenance.

Local proof sources:
- the two `spec-diff` runs, especially the second-package `illusion-of-swarm` result, for bounded source/evidence drift detection.
- the claim ledger, contradiction register, and scorecard as package-local evidence-state machinery.

Reference-only or supporting sources:
- context-file mixed-evidence papers when making the task-risk caveat.
- skills portability papers when bounding the skills section.

Synthesis-only claims:
- "literate workflow programming" as the article label.
- "a workflow is a namespace" as navigational synthesis.
- the mapping from source, validator, trace, and provenance layers onto the repo.

Explicit boundaries:
- do not claim passive markdown is executable by itself.
- do not claim stricter formalization monotonically improves behavior.
- do not claim current Reviewable Runs already provide full claim-level provenance.
- do not claim package-as-object semantics, import semantics, or repo-wide validator promotion.

## Cut order

1. Cut broad scene-setting about the repo or the history of literate programming before cutting the core source/validation/trace stack.
2. Compress the skills section into one bounded supporting paragraph if it starts to dominate the article.
3. Compress the context-file mixed-evidence caveat into one sentence if the draft starts turning into an AGENTS.md essay.
4. Cut extended treatment of workflow-as-namespace before cutting the `spec-diff` proof section.
5. Keep claim-level provenance as a forward boundary, but cut detail before cutting the main source/trace distinction.

## Failure triggers

- The essay starts claiming that markdown alone is a programming language or execution substrate.
- The source/trace hierarchy blurs and reviewable runs are treated as primary artifacts.
- The draft uses `spec-diff` as evidence of broad behavioral conformance instead of bounded source/evidence drift detection.
- The skills section outruns the evidence and implies raw markdown skills are already portable production substrate.
- The article collapses context engineering, workflow specs, harnesses, prompt specs, and skills into one undifferentiated term family.
- Claim-level provenance is described as current repo capability rather than as the next missing layer.
- The draft starts importing parked claims such as package-as-object semantics, imports as compiler features, or repo-wide validator promotion.

## Opening Lab

Open from a concrete operator problem, not from taxonomy repair. The best candidate opening is a bounded local workflow moment: a human edits the specification layer, a validator catches drift, and the system reveals that the human-readable workflow surface is already acting like source. Do not open with "markdown as code" as a slogan dispute. Use the dispute only after the concrete pressure point is visible.

## Object Decision

No object change. Keep the essay about workflow specifications becoming source-like artifacts under validation, policy, traces, and provenance pressure. Do not widen into a general context-engineering essay and do not pivot into a skills essay.

## Body / Support / Footnote Ledger

Body:

- `2603.16021`
- `2603.25723`
- `2604.13346`
- `2603.17399`
- `2603.08806`
- `2603.23806`
- `2603.29848`
- `2602.13855`
- local `spec-diff` proof notes and retained run logs

Support:

- `2603.00822`
- `2603.20380`
- `2504.11703`
- `2601.04748`

Footnote:

- `2512.19769`
- `2512.18940`

## Second-Pass Bet

The next pass works only if the essay stops sounding like a governed literature survey and starts sounding like one defended publication object. The bet is that a concrete opening plus a more compressed middle can supply that force without reopening research. If the same blocker survives `r2`, the stop gate should fire.
