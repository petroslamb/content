# Use It

This is the day-to-day operator guide for Reviewable Runs.

The framework should feel like an operating discipline, not a second framework you need to stand up first.

## When To Use It

Use Reviewable Runs when a run matters enough that you do not want to trust it just because it looked smart.

Good triggers:

- a coding run before merge or release
- a browser run before submit
- a retrieval-heavy memo or recommendation
- a run that crosses a real approval boundary
- an incident, near miss, or postmortem

Do not use the heavy version for trivial low-risk work.

## Choose The Run Unit First

Reviewable Runs applies to one bounded run, not one whole conversation by default.

Choose the run unit before you choose the risk tier.

Accepted stop-boundary types:

- handoff
- commit
- merge
- release
- submit
- publish
- explicit non-approval reason

Default anti-pattern:

- do not treat whole conversations or mega-sessions as one run unless the task, evidence, and stop condition are genuinely singular

## Daily Workflow

1. Define or slice the run.
2. Classify the run by risk.
3. Decide the minimum record surface required.
4. Capture or reconstruct the needed records.
5. Review the run against the six questions.
6. Approve, reject, revise, or escalate.

That is the whole operating method.

## Boundary Rules

- one run = one objective + one stop boundary
- if goals split, split the run
- if approvals split, split the run
- if the stop boundary is unclear, the run is not ready for review

## Minimum Record Surface By Risk

### Low Risk

Use lightweight reconstruction.

Minimum:

- reconstructable task boundary
- reconstructable action or event history
- basic verification or completion signal
- explicit reason approval was not required

What this means in practice:

- ordinary logs are acceptable if a reviewer can recover the run without guesswork
- no persisted six-record packet is required
- failure review is optional for a clean low-risk run

Typical cases:

- internal drafts
- non-destructive repo inspection
- low-impact retrieval

### Medium Risk

Make the runtime surface explicit.

Minimum:

- task spec
- execution trace
- evidence record
- verification report

What this means in practice:

- the run should be easy to inspect after the fact
- approval may be unnecessary, but the reason should be visible
- failure review is recommended after near misses and required after incidents

Typical cases:

- bounded coding fixes held before merge
- governed internal artifacts
- browser actions held before final submit

### High Risk

Use the full review surface.

Minimum:

- task spec
- execution trace
- evidence record
- verification report
- approval decision
- failure-review capability

What this means in practice:

- approval should be explicit rather than inferred
- governance records are required when actions are external, destructive, hard to roll back, or policy sensitive
- failure review is mandatory after incidents and strongly recommended after near misses

Typical cases:

- code merge or release approval
- financial, legal, or policy-sensitive output
- external account or system changes

## The Six Questions In Practice

For each meaningful run, make sure a reviewer can answer:

1. What was the task?
2. What happened?
3. What did it rely on?
4. How was it checked?
5. Who approved impact, or why was approval not required?
6. What failed or could fail?

If those answers are weak, the run is weak no matter how polished the output looks.

## Emitted Versus Reconstructed

The framework does not require everything to be generated live as prose.

Some records can be emitted directly:

- task spec from a job manifest or user instruction
- execution trace from a tool or event log
- approval decision from a gate UI or workflow

Some records are often reconstructed:

- evidence record from retrieved sources, files touched, or state snapshots
- verification report from tests, validators, or reviewer checks
- failure review from an incident note or postmortem

The requirement is not "write six documents."
The requirement is "make the run reconstructable enough for credible review."

## Good Enough First Implementation

For a first deployment:

- keep the run-review checklist as the operator standard
- use the six direct templates only when a run actually needs a packet
- prefer logs plus reconstruction for low-risk work
- prefer explicit runtime records for medium risk
- add governance records only where the action boundary justifies them

This is enough to make the framework useful without turning it into bureaucracy.

## When Not To Use One Packet

Large sessions should be sliced into sub-runs before packet assembly.

The March 26 framework-building session is the model here: it only became reviewable once it was separated into bounded sub-runs with distinct commit or handoff boundaries.

## What Not To Overdo

- do not produce a full packet for every trivial run
- do not treat a trace as automatically sufficient
- do not treat an LLM critique as a substitute for records
- do not let the framework become heavier than the work

The right question is always:

What is the lightest record surface that makes this run credibly reviewable?

## Where To Go Next

- use `evaluation/run-review-checklist.md` to inspect a single run
- use `evaluation/architecture-readiness-checklist.md` to judge whether a system can support reviewable runs at all
- use `templates/README.md` if you need a packet shape
- use `examples/proofs/coding-real-run/README.md` if you want the clearest current proof
