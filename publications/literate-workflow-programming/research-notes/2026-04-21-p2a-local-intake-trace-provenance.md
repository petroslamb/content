# P2a Local Intake: Trace, Validation, And Claim-Level Provenance

Date: 2026-04-21

Status: local paper intake and claim-state rescore.

## Purpose

The earlier claim-state gap pass identified a focused P2a queue:

- `2603.23806` AgentPex
- `2603.29848` AgentFixer
- `2602.13855` Claim-Level Auditability

This note records what changed once those papers were stored locally, converted to markdown, and read against the package claim surfaces.

The target was not a new lead. The target was to decide whether the trace/provenance claims were still assistant-backed hunches or had become local paper-backed package claims.

## Intaken Papers

| Paper | Why It Was Queued | What It Now Adds |
| :--- | :--- | :--- |
| `2603.23806` Willful Disobedience / AgentPex | Trace compliance beyond outcome-only scoring | Prompt-derived rule extraction, normalized trace artifacts, procedural violation detection, and a clean source/trace hierarchy |
| `2603.29848` AgentFixer | Failure localization and validation-driven repair | Validation as a continuous engineering loop spanning prompt analysis, cross-stage checks, trace comparison, diagnosis, and refinement |
| `2602.13855` From Fluent to Verifiable | Claim-level provenance and contradiction transparency | A paper-backed model for provenance coverage, provenance soundness, contradiction transparency, audit effort, and protocolized validation during synthesis |

## Findings

### 1. AgentPex Strengthens The Trace Layer Without Collapsing Source Into Logs

AgentPex normalizes each run into a self-contained artifact made of:

- the system prompt
- the tool schema
- the sequential message log

It then applies explicit-only rule extraction and evaluates compliance against those prompt-derived rules.

That matters for this package because it gives the trace claim a stronger local formulation:

Reviewable traces are not just receipts. They are evaluatable behavioral records that can be checked against declared source-side constraints.

The boundary is just as important:

- AgentPex does not make logs the source of truth.
- AgentPex does not provide repair.
- AgentPex is strongest on prompt-derived procedural constraints directly observable in the trace.

So the package can say "trace checking" with more confidence, but it still cannot call logs full provenance or source code.

### 2. AgentFixer Makes Validation Look Like Lifecycle Infrastructure

AgentFixer is the strongest local paper for the article's hinge claim about validation.

It spans:

- prompt analysis
- input validation
- output validation
- cross-stage consistency checks
- root-cause analysis
- trace comparison
- validation-driven refinement

The strongest local result for this package is not any single tool. It is the paper's operating model:

Validation is a continuous engineering loop connecting incident detection, diagnosis, and design refinement.

The useful details are concrete enough to matter:

- the framework contains fifteen detection tools and two RCA tools
- trace comparison beat failed-trace-only analysis in 12 of 26 paired cases and was never worse
- the discussion section explicitly argues that validation is a continuous engineering process rather than an afterthought

The boundary stays visible:

- the system still uses interactive analysis and human prioritization
- some checks are architecture- or language-specific in practice
- the paper does not justify fully autonomous validation as a black-box infrastructure

### 3. Claim-Level Auditability Turns Contradiction State Into A Provenance Requirement

`2602.13855` is the paper that upgrades contradiction state from workflow transfer idea to paper-backed design requirement.

Its useful move is architectural:

- claims need provenance paths, not only action logs
- contradictions should be surfaced explicitly, not averaged away
- validation should run during synthesis, not only after publication

The AAR frame gives the package a precise vocabulary:

- provenance coverage
- provenance soundness
- contradiction transparency
- audit effort

This is the first local paper that directly supports the package's claim that promoted claims should carry contradiction state as part of the debugging/provenance surface.

The boundary is again essential:

- the paper does not justify automatic contradiction resolution
- the paper does not prove the current repo already has claim-level provenance
- it strengthens the next-layer claim, not the claim that the layer already exists locally

### 4. The Trace Stack Is Now Cleaner

After the P2a local intake, the safe stack is:

1. trace checking: did the run comply with declared rules?
2. failure localization: where did the trajectory drift or break?
3. claim-level provenance: which evidence supports which promoted claim, and where does it conflict?

The package now has local evidence for all three layers as concepts.

The package does not yet have local implementation for all three layers.

Current local state:

- `spec-diff` and Reviewable Runs reach trace checking
- local contradiction and claim-state surfaces reach part of the provenance framing
- full claim-level provenance graphs are still future work

## Assistant Pressure Test

I ran one narrow alphaXiv assistant audit after deterministic retrieval and local intake. The extraction note is [`alphaxiv-discussions/019db0f6-p2a-claim-audit.md`](alphaxiv-discussions/019db0f6-p2a-claim-audit.md).

The assistant was useful for one thing only: it confirmed the strongest defensible wording for the three claims and helped expose what the papers do not justify.

I did not adopt its invented overlay labels such as:

- `compliance-execution paradox`
- `refinement overhead`
- `cognitive load gap`

Those were not stable package terms and were not clearly paper-backed.

## Claim-State Consequences

- CSA-C2 stays article-ready and gains a cleaner boundary: logs are execution records and trace-evaluation surfaces, not the artifact of record.
- CSA-C6 upgrades from `use with caveat` to `article-ready` as a design requirement, because contradiction transparency and claim-level provenance are now local paper-backed. The caveat remains that the repo does not yet implement full provenance graphs.
- CSA-C7 stays article-ready and becomes harder to flatten into a single final test gate.

## Draft Consequence

The article can now cleanly separate:

1. specification as visible source surface
2. validation as lifecycle infrastructure
3. traces as evaluatable runtime records
4. claim-level provenance as the next debugging and audit layer
