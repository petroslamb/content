---
workflow_id: evidence_authorization
workflow_group: evidence
runner_mode: guided
default_skill: null
launch_templates: []
required_context:
  - package README or leaf README
  - package paper index or source index
  - active blueprint, plan, draft, or review finding that created the evidence question
  - current claim set or section spine
expected_outputs:
  - package-local evidence authorization ledger
  - source burden map separating body, hinge, optional, and forbidden uses
  - synthesis boundary naming what the evidence proves and does not prove
done_when:
  - the rewrite or blueprint can distinguish source-backed claims from synthesis without reopening the whole paper library
approval_gate: none
---

# Evidence Authorization

Use this workflow when a package already has a paper or source index, but the next blueprint or rewrite needs a stricter layer between "these sources exist" and "this essay may claim this."

The output is an evidence authorization ledger. It is not a paper index, a literature review, or a second blueprint. Its job is to prevent adjacent evidence from becoming load-bearing evidence by accident.

## Where It Sits

Use the layers this way:

| Layer | Question | Typical Surface |
| :--- | :--- | :--- |
| source inventory | what sources do we have, and where are they? | `papers/index.md`, source index, manifest |
| evidence authorization | what claims may those sources license? | evidence authorization ledger |
| blueprint | what essay architecture follows from the authorized claims? | `blueprint.md`, plan, prewrite surface |
| draft | how does the argument read? | bounded candidate or live draft |

This workflow is usually triggered during blueprint hardening, after a serious review finds that the draft is overclaiming, blending evidence types, or using a large paper set without clear source burdens.

## When To Use It

Use it when:

- multiple sources support nearby but distinct claims
- a coined frame depends on synthesis rather than one decisive source
- a high-bar review says the draft is precise but lacks a dangerous or actionable target, and the next move would require evidence for a new argumentative bridge
- the package has many papers and the draft risks becoming a citation parade
- a review says the problem is evidence authority, evidence scope, actionability, or proof boundary
- you need to state what the essay cannot claim before rewriting

Do not use it when:

- the package has only one or two straightforward sources
- the paper index itself is missing or stale; use [`../paper-intake/README.md`](../paper-intake/README.md) first
- the thesis is still exploratory; use [`../alphaxiv-research/README.md`](../alphaxiv-research/README.md) first
- the real task is prose polish rather than evidence governance

## Canonical Output

Name the package-local file according to local convention. Good defaults:

```text
evidence-authorization-ledger.md
<package-name>-evidence-authorization-ledger.md
claims-evidence-ledger.md
```

Keep it beside the blueprint or active package root, not inside `papers/`. The paper index owns source paths. The ledger owns claim permission.

## Hinge Warrant Ledger

Sometimes the useful output is narrower than a full evidence authorization ledger. Use a package-local hinge warrant ledger when one proposed bridge claim is doing disproportionate work, especially after an external review says the essay needs a sharper target, more actionability, or a more provocative antagonist.

A warrant ledger answers one question:

> What is the strongest version of this bridge claim that the evidence safely licenses?

This is the pattern that proved useful in the confidence-debt work. The paper index named the deployment and evaluation sources. The evidence authorization ledger mapped the essay's broader claims. The narrower warrant ledger tested the dangerous bridge: responsible-looking AI deployment practice can itself become a trust-transfer surface. That ledger made the claim usable by separating the supported synthesis from forbidden overclaims such as "teams knowingly launder confidence" or "artifact-score-approval workflows are proven to cause downstream failures."

Use a warrant ledger when:

- the draft needs to attack a real practice, not just describe an abstract problem
- a single bridge claim would materially raise debate energy or actionability
- the evidence supports the components but not a direct causal proof
- a full new draft would be premature until the bridge claim is authorized

Do not use it as a substitute for intake or as a way to make weak evidence sound stronger. If the warrant ledger cannot state a safe bridge claim, the rewrite should not proceed from that bridge.

## Claim-State Authorization

Claim-State Authorization is an optional advanced mode of this same workflow. Keep `workflow_id: evidence_authorization`; do not create a new lifecycle stage, root command, or separate workflow.

Use this mode when a package already has researched claims and the hard question is no longer only "what claims does the evidence authorize?" The harder question is:

> What is each claim's current state across evidence, contradiction, validation, and draft readiness?

This mode is more complex than the normal evidence authorization ledger and lighter than the full Evidence Governance pattern in [`../../publications/evidence-governance/README.md`](../../publications/evidence-governance/README.md). It imports a narrow claim-state mechanism without asking every publication package to adopt a full governance protocol.

Use Claim-State Authorization when:

- papers, local proof, repo practice, and article framing create real tensions rather than generic objections
- the package already has a claim ledger or evidence authorization ledger
- a future draft needs to know not only whether a claim is supported, but whether it is contested, validated, parked, or article-ready
- local proof artifacts such as validators, reports, traces, or reviewable runs affect claim permission
- the team needs a curated contradiction surface before drafting

Do not use it when:

- the package still needs basic paper intake
- the current problem is ordinary citation placement
- there are no meaningful tensions between sources, proof, practice, and framing
- a lightweight hinge warrant ledger would answer the question

The outputs are:

| Output | Job |
| :--- | :--- |
| claim ledger | Evidence-state surface. It records researched claims, support levels, authorized wording, caveats, and parked claims. |
| contradiction register | Tension-state surface. It records high-value contradictions or frame tensions with an authority rule and draft instruction. |
| scoring rubric | Readiness-state rule. It defines how to score each claim across paper support, local proof, enforcement, contradiction handling, and article role. |
| claim scorecard | Draft-gate surface. It applies the rubric to current top claims and names the next action. |

Use these templates when starting the variant:

- [`templates/claim_state_authorization_template.md`](templates/claim_state_authorization_template.md)
- [`templates/contradiction_register_template.md`](templates/contradiction_register_template.md)
- [`templates/claim_scoring_rubric_template.md`](templates/claim_scoring_rubric_template.md)
- [`templates/claim_scorecard_template.md`](templates/claim_scorecard_template.md)

The variant works best with a small contradiction register. Curate tensions that would change the article, proof plan, or claim permission. Do not let the register become a dumping ground for every possible objection.

For this mode, draft admission requires three states beside the claim:

1. Ledger status: what evidence authorizes the claim and what caveat travels with it.
2. Contradiction status: whether known tensions are resolved, open, parked, or blocking.
3. Rubric status: whether the claim is article-ready, usable with caveat, parked, or blocked.

## Required Sections

A useful ledger has these sections:

1. **Purpose**: state that the ledger sits between the source index and blueprint.
2. **Support Levels**: define labels such as `Direct`, `Hinge`, `Analogical`, `Synthesis`, and `Speculative`.
3. **Claim Map**: map claim IDs to source sets, support level, authorized wording, caveat, and draft role.
4. **Source Burden**: state each source's job: body, hinge, optional, reference-only, or cut.
5. **Synthesis Boundary**: separate what the sources prove from what the essay is synthesizing.
6. **Forbidden Claims**: list claims the draft must not make from the current evidence.
7. **Blueprint Instructions**: translate authorization into rewrite-governing instructions.
8. **Open Evidence Gaps**: name missing proof, field studies, or source types.

Use [`templates/evidence_authorization_ledger_template.md`](templates/evidence_authorization_ledger_template.md) as the starting shape.

A useful hinge warrant ledger can be shorter, but it must still include:

1. **Hinge Claim**: the contested bridge in one sentence.
2. **Why It Matters**: what the claim would unlock in the blueprint or draft.
3. **Source Warrants**: which sources support which component parts.
4. **Safe Wording**: the strongest body-ready sentence the evidence permits.
5. **Forbidden Wording**: the tempting claims the evidence does not permit.
6. **Blueprint Instruction**: where the bridge may enter the essay, or why it must stay out.

## Working Flow

1. Read the package README, source index, active blueprint or draft, and the review that triggered the ledger.
2. Extract the live claim set. Claims should be sentence-level or paragraph-level, not vague themes.
3. Assign each claim to sources that directly support it, sources that only provide a bridge, and sources that are merely adjacent.
4. Write authorized wording for each claim. This should be the strongest sentence the evidence safely licenses.
5. Write the caveat beside the claim, not in a separate memo. The caveat is part of the authorization.
6. Build the source burden map. Every source must have a job or be marked optional/reference-only.
7. Write the synthesis boundary. This is where high-level frames are allowed to exist, but only with their epistemic status labeled.
8. Add forbidden claims before drafting. The ledger should stop the next writer from overclaiming.
9. Feed the ledger back into the blueprint or prewrite gate before opening a new candidate.

For a hinge warrant ledger, keep the flow tighter:

1. Write the proposed bridge claim before rereading sources.
2. Reopen only the exact anchor papers or artifacts that would have to support it.
3. Split the claim into component findings, synthesis, and speculation.
4. Write the safe sentence and the forbidden stronger sentence side by side.
5. Update the blueprint only if the safe sentence changes the essay's target or actionability.
6. Do not open a new candidate merely because the ledger is cleaner; open one only if the authorized bridge materially changes the draft.

## Evidence Labels

Use these default labels unless the package already has stronger local terms:

- `Direct`: the source directly supports the claim.
- `Hinge`: the source supports a necessary bridge in the argument.
- `Analogical`: the source is suggestive but does not prove the claim.
- `Synthesis`: the claim integrates several supported claims but is not directly proven by one source.
- `Speculative`: useful idea, not safe as an asserted claim.

Do not let `Synthesis` become a loophole. A synthesis claim still needs a visible chain of supported component claims.

## Acceptance Criteria

The ledger is strong enough when:

- a future writer can tell which sources must appear in the body and which should stay in references
- every major claim has authorized wording and a caveat
- synthesis claims are labeled as synthesis rather than smuggled in as findings
- forbidden claims are concrete enough to prevent predictable overreach
- the blueprint can be hardened from the ledger without rereading the whole paper set

The ledger is too weak when:

- it repeats the paper index with longer notes
- it only lists sources under themes without claim-level permission
- every source appears mandatory
- synthesis boundaries are missing or apologetic
- the draft could still claim the same unsupported thing after reading the ledger

A hinge warrant ledger is too weak when:

- it proves only that sources are thematically nearby
- it cannot name the exact bridge sentence the draft may use
- it avoids forbidden wording because the limits are uncomfortable
- it would not change the blueprint, section burden, or cut order

## Related Workflows

- Use [`../paper-intake/README.md`](../paper-intake/README.md) before this workflow when sources are not yet local.
- Use [`../alphaxiv-research/README.md`](../alphaxiv-research/README.md) before this workflow when the right papers are not yet known.
- Use [`../essay-iteration/README.md`](../essay-iteration/README.md) after this workflow to harden the blueprint and write bounded candidates.
