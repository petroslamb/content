# Cross-Read: Confidence Debt And Contradiction Ledgers

Date: 2026-04-21

Status: adjacent-package transfer note, not a new article frame

## Question

`publications/confidence-debt/` is adjacent to this package, but it is not trying to answer the same question.

Confidence Debt asks how trust moves farther than evidence. Literate Workflow Programming asks when workflow specs become meaningful source for agent systems. The overlap is not the public thesis. The overlap is the mechanism: a workflow-source system needs a way to preserve evidence state, contradiction state, validation state, and trace state around the claims it promotes.

## Surfaces Read

Within this repo:

- `../../confidence-debt/README.md`
- `../../confidence-debt/blueprint.md`
- `../../confidence-debt/confidence-debt-evidence-authorization-ledger.md`
- `../../confidence-debt/confidence-debt-shipping-practice-warrant-ledger.md`
- `../../confidence-debt/confidence-debt.md`

Outside this repo:

- `/Users/petros/Projects/eth-llm/poc5/docs/evaluations/contradictions.csv`
- `/Users/petros/Projects/eth-llm/poc5/docs/evaluations/evidence_ledger.md`
- `/Users/petros/Projects/eth-llm/poc5/docs/evaluations/claim_audit.md`
- `/Users/petros/Projects/eth-llm/governance-core/PILOT_PROTOCOL.md`
- `/Users/petros/Projects/eth-llm/governance-core/PHASE_GATES.md`

## Transferable Mechanism

The most important import is not the term "confidence debt." It is the artifact discipline around contradiction.

Confidence Debt's artifact gate says that a promoted claim needs visible evidence state, contradiction state, and expiry condition. The `eth-llm` governance-core protocol operationalizes the same instinct more concretely: claims are not settled by narrative summaries, CSV rows, or model-generated outputs. Evidence is consumed in an authority order, contradictions are tracked as first-class records, and unresolved contradictions block final governance.

That matters for this package because `spec-diff` is currently checking package evidence consistency, not claim conflict. It can tell whether a paper index represents local evidence. It does not yet tell whether two package artifacts make incompatible claims, whether a higher-authority source overrules a lower-authority trace, or whether a promoted claim has unresolved contradiction state.

The transferable pattern is:

```text
claim -> evidence state + contradiction state + validation state + trace state
```

In a workflow-source system, this is the difference between a run log and a semantic debugging surface. A log says what happened. A contradiction register says which claims conflict, what evidence tier resolves the conflict, and whether the conflict is still open.

## Boundary

Do not import the full Confidence Debt thesis into this article. That essay is about trust propagation across artifacts, evaluations, and human oversight. This package is about the engineering conditions under which workflow specs become source.

Do import these narrower lessons:

- A claim ledger answers what a source is allowed to license.
- A contradiction register answers where two artifacts disagree and which source has authority.
- An evidence hierarchy prevents polished summaries and generated traces from outranking lower-level evidence.
- A validation gate is incomplete if it can detect missing artifacts but cannot represent unresolved contradiction state.

Do not import these broader claims:

- the three-gate deployment doctrine as the governing structure of this essay,
- confidence debt as the public frame,
- a universal requirement that every publication package must maintain a contradiction register,
- the claim that contradiction-ledger machinery has been validated as a complete workflow system.

## Implication For `spec-diff`

The current `spec-diff` prototype should stay evidence-surface focused. Its next conceptual extension is not a larger root command. It is a richer manifest vocabulary:

- `authority_order`: which artifacts are allowed to overrule which other artifacts,
- `claim_state`: supported, contested, inference, parked, or blocked,
- `contradiction_state`: none, classified, unresolved, resolved, or blocking,
- `validation_state`: pass, warning, fail, skipped, or out of scope,
- `trace_state`: which run or report produced the observed state.

The `illusion-of-swarm` proof candidate already points in this direction. Five draft-cited arXiv IDs lacked local evidence or alphaXiv artifact records. The repair did not pretend they were present. It classified them as gaps. That is a primitive contradiction-state move: preserve the mismatch rather than smoothing it away.

## Article Use

Use this as a short supporting move in the semantic-debugging section:

> A source-linked trace is useful only if it can preserve conflict. The interesting artifact is not just "the run succeeded" or "the file exists." It is the claim's current state: what evidence supports it, what evidence contradicts it, which source has authority, and whether the conflict is still open.

That sentence belongs near `spec-diff` and Reviewable Runs. It should not move the essay into confidence-debt territory.
