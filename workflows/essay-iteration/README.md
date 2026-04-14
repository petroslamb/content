---
workflow_id: essay_iteration
runner_mode: hybrid
launch_mode: scaffold_only
default_skill: null
launch_templates:
  - ".venv/bin/python scripts/init_essay_iteration_packet.py --package {package_key}"
packet_templates:
  - "workflows/essay-iteration/templates/hardened_blueprint_template.md"
  - "workflows/essay-iteration/templates/candidate_template.md"
  - "workflows/essay-iteration/templates/cold_replacement_review_template.md"
  - "workflows/essay-iteration/templates/atlas_live_draft_scorecard_template.md"
  - "workflows/essay-iteration/templates/promotion_decision_template.md"
validator_commands:
  - "npm run check:essay-iteration -- --package {package_key}"
required_context:
  - canonical live draft
  - leaf package README
  - parent umbrella README when present
  - companion when present
  - nearest blueprint when present
  - nearest review artifacts when present
  - target evidence surface or source index
expected_outputs:
  - essay-iteration packet manifest beside the live draft
  - bounded rewrite candidate and structured review artifacts within the packet
done_when:
  - a validated packet exists beside the live draft and the current direction is explicit enough for human review or the next lifecycle handoff
approval_gate: required_for_major_rewrite
judgment_policy: draft_only
prohibited_moves:
  - Do not overwrite the current live draft before a replacement verdict exists.
  - Do not archive adjacent leaves before the promotion decision is explicit.
  - Do not mark the stage done from a weak-model run without human review.
  - Do not claim Publication Power 9 or above under the draft-only policy.
---

# Essay Iteration

This is the canonical tracked workflow for taking an essay from live draft to review, rewrite, and archive.

## Core Model

The repo standard is:

- one stable **live draft** path
- supporting review artifacts beside it when useful
- older versions and superseded support files moved into local `archive/`

The default is not “versioned files forever” and not “rewrite in place with no history.”

## Scaffolded Hybrid Flow

`essay_iteration` is now a scaffolded hybrid stage rather than a prose-only guided stage.

The intended sequence is:

1. set the leaf package `status.yaml` so `essay_iteration` is the next stage
2. run `npm run stage:run -- --package <leaf> --stage essay_iteration`
3. let the scaffold script create a package-local packet beside the live draft
4. point the model at the leaf package plus that packet manifest
5. fill the packet, run the validator, and leave promotion to a stronger reviewer or human approver

The scaffold step is allowed without promotion approval because it only creates or refreshes the working packet. It does not authorize replacement of the live draft and it does not mark the stage done automatically.

## Packet Manifest

The package-local essay-iteration packet is the canonical machine-readable contract for weaker models. It should be sufficient, together with the leaf package itself, for a weaker model to work without a custom rescue prompt.

The packet manifest must name:

- the live draft
- the leaf README
- the parent umbrella README when present
- the nearest companion, blueprint, and review artifacts
- the evidence surface or source index
- the generated packet file targets
- the validator command
- the judgment policy
- the prohibited moves

Treat the packet manifest as the primary execution surface. The workflow prose remains the policy layer, but the packet is the object a weaker model should actually follow.

## Weak-Model Judgment Limit

Under the default `draft_only` judgment policy, a weaker model may:

- harden the blueprint
- write a bounded candidate
- fill a replacement review
- fill an atlas-style scorecard
- recommend whether to revise again or keep the live draft

It may not:

- promote the candidate into the live path on its own
- mark the stage done on its own
- claim `Publication Power` `9` or above as a settled outcome
- treat package cleanup as proof that the essay has cleared the publication bar

## Recommended Supporting Files

Use these only when they help:

- `companion.md`
- blueprint or plan file
- claims ledger
- review file
- scoring or rubric file

These are working surfaces, not mandatory ceremony.

## Review Inputs

Before a serious review pass, pull the package context that actually defines the bar:

- package `README.md`
- root [`voice_consistency_guide.md`](../../voice_consistency_guide.md) when the package targets publication prose
- blueprint or plan file if one exists
- companion if the package uses one
- prior live drafts or comparison baselines when the task is version-to-version review
- package evidence surface when the rewrite is evidence-sensitive and the blueprint makes source-backed claims

For a **cold replacement review** on a bounded candidate, the default minimum context is narrower:

- the candidate draft
- the current live draft
- the root [`voice_consistency_guide.md`](../../voice_consistency_guide.md)

Use the blueprint only after the main cold read if blueprint alignment needs comment. Do not let the blueprint pre-justify the draft.

## Evidence-Backed Defaults

- Brutal reviews in this repo are expected to be explicit, scored, and rubric-driven. Casual “looks good” feedback is not enough when a draft is near publication.
- If the user asks for version comparison, keep the rubric stable across versions so the comparison stays apples-to-apples.
- When the package is clearly aiming at public publication, include importance, distinctiveness, or virality as separate axes instead of collapsing everything into one prose-quality score.
- When a bounded candidate is being considered for promotion into the live path, run a cold replacement review before promotion if the package does not already have a stronger established editorial gate.
- When an umbrella package is being collapsed from multiple live leaves into one flagship essay, treat that as a bounded candidate and replacement decision, not as a cleanup pass. Keep the prior live leaves readable until one candidate actually clears promotion.
- After a brutal review or cold replacement review that does not clear promotion, the next step is a high-bar blueprint hardening gate. Either produce a blueprint strong enough to govern a rewrite aimed at the outstanding-essay bar, or conclude explicitly that the current frame cannot reach that bar from the available evidence.
- When a draft is already close, prefer surgical fixes that clear the remaining blockers over a broad rewrite that destabilizes the whole piece.
- The stable-live-draft-plus-archive model is the default. The main exception is when a package explicitly manages parallel bundle baselines, in which case versioned siblings can temporarily stay live until one becomes canonical.
- For refinement passes on an existing essay, harden the blueprint before a major rewrite when the blueprint is derived from the draft and still contains fuzzy claims, unresolved citation drift, or under-specified revision goals.
- When a major rewrite is needed, prefer a clearly named bounded candidate such as `-v2.md` or `-revision-2.md` before promoting it into the stable live path. Do not overwrite the live draft first and decide later what changed.
- If the blueprint already exists, use it as the preparation surface instead of creating a separate memo by default. Add a new memo only when the blueprint cannot absorb the needed evidence validation cleanly.
- For evidence-sensitive rewrites, do not draft against alphaXiv-only context if the missing papers are already known. Intake first, then harden the blueprint, then draft the article.
- When a hardened blueprint is aiming at the outstanding bar, an external AI review of the blueprint can be useful before the essay prewrite gate, but that review is advisory. The writer remains responsible for adjudicating which findings matter, which are misreads, and which proposed fixes would actually improve the governing surface.
- Before writing a high-bar bounded draft, run an essay prewrite gate. Either produce an essay-governing prewrite surface strong enough to support an outstanding draft, or conclude explicitly that the essay is not yet writable at that bar.
- Do not let package cleanliness, folder normalization, or archive work stand in for proof that the new essay is stronger. A cleaner package can still contain a thinner publication object.

## Blueprint Hardening

Use blueprint hardening when the package already has a blueprint or plan, but that surface still behaves like an author memo, a section outline, or a thesis dump rather than a rewrite-governing research artifact.

When blueprint hardening is triggered by a blocking brutal review or cold replacement review, it becomes the next mandatory step rather than an optional preparation pass.

The recurring strong pattern is:

1. convert the blueprint from essay-outline or process language into a standalone research surface
2. replace vague principles with source-backed findings or explicitly labeled synthesis
3. add explicit guardrails for non-claims, historical overreach, and evidence mismatch
4. add a claim-to-evidence ledger when the rewrite is evidence-sensitive and multiple papers are doing different argumentative jobs
5. add conditional evidence triggers when extra papers should only be intaken if a claim survives pressure-testing
6. use alphaXiv in narrow validation mode and paper intake only when the claim set actually changes

For evidence-sensitive article work, the preparation order is:

1. intake missing papers into the canonical evidence surface
2. harden the blueprint against that evidence surface
3. write the bounded article candidate

Do not invert that order unless the package already has every load-bearing paper locally.

For post-review hardening, the gate is binary:

1. produce an outstanding-governing blueprint that sets the next rewrite direction at the top bar
2. or issue an explicit impossibility finding that names the frame or evidence gap blocking that bar

Do not proceed from a merely cleaner outline, a softer memo, or a partially tightened thesis dump.

The acceptance bar is higher than “better notes.” A hardened blueprint should:

- contain no memo-language about the essay-writing process
- avoid imposed synthesis that the evidence has not earned
- avoid ornamental citations that do not change what the blueprint is allowed to claim
- separate source-backed findings from higher-level synthesis
- be strong enough to govern a bounded rewrite without reopening the whole argument from scratch
- either set a top-bar rewrite direction or state explicitly why that bar is not reachable from the current frame and evidence base

For weaker models or loosely supervised runs, require this exact minimum output contract for a hardened blueprint:

- one paragraph on the active thesis and why this frame survives pressure
- one section-level argument spine with the burden of each section
- one explicit source-backed claim ledger naming which sources do body work
- one borders list naming what the essay will not claim
- one failure-trigger list naming what would void the rewrite

If hardening collapses the original frame, narrow or replace the frame before starting the rewrite. Do not carry a broken synthesis forward just because it sounded good in the previous draft.

## External Blueprint Review

Use this optional step after blueprint hardening when the package is aiming at the outstanding bar and the author wants one more cold pass on the governing surface before the essay prewrite gate.

The external review is advisory, not binding:

1. gather the review against the blueprint itself, not the draft or the general idea of the essay
2. adjudicate each finding as the writer: accept, reject, downgrade, or defer
3. integrate only the fixes that materially strengthen the blueprint's governance
4. do not let an external review reopen a settled frame unless it exposes a real evidence gap, conceptual contradiction, or governance failure

The goal is not consensus. The goal is to improve the blueprint without surrendering authorship of the argument.

Strong uses of this step:

- catching fuzzy seams between adjacent concepts that the blueprint names but does not operationalize
- finding places where the blueprint bans failure modes without positively specifying the governing correction
- pressure-testing whether the evidence ledger and section contract actually agree

Weak uses of this step:

- treating every external suggestion as mandatory
- letting a reviewer push the essay back toward a broader or safer frame the blueprint has already rejected
- outsourcing title, opening, or structural judgment when the writer already has a stronger evidence-backed view

If the review surfaces only minor or clearly mistaken points, note that and move on. Do not perform ceremonial re-hardening.

## Essay Prewrite Gate

Use this gate after blueprint hardening, and after any optional external blueprint review, before drafting when the package is aiming at a high publication bar rather than a routine incremental revision.

The essay prewrite gate is also binary:

1. produce an essay-governing prewrite surface strong enough to support an outstanding draft
2. or conclude explicitly that the essay is not yet writable at that bar from the current frame, evidence, or voice constraints

The prewrite surface should not be a rough outline. It should set:

- the active working title or title family if that matters
- the exact essay promise
- the required structural spine
- the paragraph-level burden or equivalent section-level burden
- which papers must do body work versus reference-only work
- cut order if the draft becomes bloated
- explicit failure triggers that void the pass

For weaker models or autonomous runs, require this exact minimum output contract for the prewrite gate:

- `Promise`: one sentence on what the essay will prove
- `Spine`: ordered section list with the argumentative job of each section
- `Paragraph burden`: one sentence on what each section must accomplish before moving on
- `Evidence burden`: which papers or artifacts must appear in the body versus references only
- `Cut order`: what gets cut first if the draft bloats
- `Failure triggers`: the signs that mean the draft should not be promoted

If that surface cannot be produced cleanly, do not draft. Return to blueprint hardening, evidence intake, or an impossibility finding.

## Umbrella Consolidation

Use this mode when several related leaves inside one umbrella package are being collapsed into one flagship publication object.

The default sequence is:

1. identify the current live leaves and the specific reason consolidation is needed
2. run a scored brutal review or cold comparison across the candidate leaves
3. produce one hardened blueprint for the proposed flagship object
4. run the essay prewrite gate for that flagship object
5. write one bounded flagship candidate beside the existing surfaces when feasible
6. run a cold replacement review against the strongest prior leaf, not just against the author's intent
7. promote only after the candidate wins on publication power rather than cleanliness alone
8. archive the superseded leaves only after the promotion decision is explicit

Strong warning:

- do not overwrite the only surviving live leaf first and decide later whether the consolidation worked
- do not archive adjacent leaves before the replacement verdict is explicit unless the package is already in a transitional non-public state and that exception is stated directly

## Citation And Reference Defaults

When the package is writing an evidence-sensitive public article rather than a private memo, use these defaults unless the package already has a stronger established convention:

- Use inline author-style citations in the body, for example `(He et al., 2015)` rather than raw URLs, bare paper titles, or numeric bracket citations.
- Keep inline citations attached to argumentative claims, not every sentence. A citation should mark where the evidence is doing work.
- End the article with a real reference section. Do not stop at a bare link dump when the references are part of the reading experience.
- When the cited papers are doing substantive argumentative work, give each reference at least a short paragraph explaining why it matters to the essay. The reference section can therefore be annotated, not just bibliographic.
- Keep the article reference section distinct from `papers/index.md`. The article references explain argumentative importance; the paper index tracks the local source library.

## Cold Replacement Review

Use this review mode when a bounded candidate might replace the live draft and the decision should be made against a high publication bar rather than against local momentum.

The default posture is:

- prefer a fresh thread or new context window so the read is actually cold
- compare the candidate against the live draft on substance, argumentative force, and replacement-readiness, not surface polish alone
- also score the candidate against the north star of an outstanding essay, not just against the current package baseline
- prefer false negatives over false positives when the replacement decision is genuinely unclear

The review should default to this output shape:

1. findings first, ordered by severity
2. prioritized issue list using `P0` through `P3`
3. strict scorecard with category scores and a weighted overall score
4. explicit replacement verdict
5. explicit north-star verdict
6. one short paragraph on the main blocker to replacement and the main blocker to outstanding quality

Expected scoring categories for this mode:

- thesis strength
- argumentative force
- historical honesty
- evidence discipline
- conceptual precision
- structural coherence
- intellectual necessity of prose
- voice quality
- replacement readiness
- outstanding-essay proximity

Priority meanings:

- `P0`: fatal replacement blocker
- `P1`: major weakness that materially limits the essay
- `P2`: real but non-fatal weakness
- `P3`: polish-level issue

Cold replacement reviews should explicitly call out:

- where the draft only works if the reader already shares the author's framing
- where the history feels imposed, over-smoothed, or too neat
- where citations are present but not actually doing argumentative work
- where the prose sounds high-level without doing necessary intellectual work
- where the title, subtitle, or framing outruns what the body really proves

If the live draft is still stronger in any important way, say so directly. If the candidate is cleaner but thinner, that should count against promotion rather than for it.

## Post-Review Blueprint Gate

Use this gate immediately after a brutal review or cold replacement review when the review does not clear promotion and the next direction is still materially unsettled.

This gate is binary:

1. produce a rewrite-governing blueprint strong enough to aim at the outstanding-essay bar
2. or issue an explicit impossibility finding naming the frame mismatch, evidence gap, or title-level overreach that blocks that bar

No middleground is allowed here. Do not launch another broad rewrite from a cleaner outline, a softened memo, or a partially improved blueprint.

## Canonical Iteration Loop

1. maintain one stable live draft path
2. run a brutal review with explicit scoring or rubric criteria when the draft is mature enough
3. if the review does not clearly support promotion or bounded fixes, run the post-review blueprint gate as the next step
4. either produce an outstanding-governing blueprint or state explicitly why that bar is not reachable from the current frame and evidence
5. if the blueprint passes, optionally run an external blueprint review and adjudicate it as the writer
6. run the essay prewrite gate before drafting
7. either produce an essay-governing prewrite surface or conclude explicitly that the essay is not yet writable at the target bar
8. use that result to decide whether another rewrite is viable at all
9. get user approval before a major rewrite pass when the next direction materially changes the essay
10. if the draft is close, apply bounded fixes first; otherwise produce a clearly bounded candidate
11. run a cold replacement review before promotion when the candidate is a serious replacement contender
12. compare, choose, and only then promote or archive
13. archive superseded versions, local review files, and retired companions once they are no longer the active surface

## Refinement Defaults

For a published or older essay under refinement, the recurring strong pattern is:

1. keep the current live draft intact
2. intake missing load-bearing papers into the package evidence surface if the claim set still depends on temporary research context
3. harden the blueprint until it becomes a standalone research artifact rather than a memo or loose outline
4. optionally run an external blueprint review and integrate only the adjudicated fixes that materially improve governance
5. run the essay prewrite gate before drafting any high-bar bounded candidate
6. run targeted validation against the package evidence surface when principle-level claims need pressure-testing
7. write a bounded candidate beside the live draft
8. run a cold replacement review against both the live draft and the outstanding-essay bar
9. if the review blocks promotion, return immediately to the post-review blueprint gate instead of launching another freehand rewrite
10. compare, choose, and only then promote one draft back into the canonical live path

This is the default refinement loop unless the package has a stronger established editorial process.

## Archive Discipline

What should usually move into local `archive/`:

- older versioned drafts
- superseded companions
- retired local README files
- prior review matrices or scoring passes that no longer define the active direction

Keep the live surface readable. Archive depth should preserve history without overwhelming the default reading path.

## Package Expectations

For single-publication packages, the live surface should usually make it obvious where to find:

- the live essay
- optional companion
- papers
- artifacts
- archive

For umbrella packages, preserve the stronger established package structure. The archive discipline still applies inside the local topic or essay folder.
