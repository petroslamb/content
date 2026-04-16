---
workflow_id: evidence_authorization
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

## Related Workflows

- Use [`../paper-intake/README.md`](../paper-intake/README.md) before this workflow when sources are not yet local.
- Use [`../alphaxiv-research/README.md`](../alphaxiv-research/README.md) before this workflow when the right papers are not yet known.
- Use [`../essay-iteration/README.md`](../essay-iteration/README.md) after this workflow to harden the blueprint and write bounded candidates.
