# alphaXiv Discussion: Claim-State Gap Pass

Date: 2026-04-21

Session ids:

- `019db0b1-df12-7587-99f6-0028445d2771`
- `019db0b3-9566-7bfa-ba44-70b24294cd10`
- `019db0b4-cc0b-73f4-aa80-31a1f5ae3d5e`
- `019db0b4-c894-773f-8b98-ce937258004f`
- `019db0be-04e2-7b72-a37a-bf517f73ef41`

Titles:

- `Pressure Test Workflow Claims`
- `AGENTS.md claim analysis`
- `Agent Observability CSA`
- `CSA-C4 Skills Analysis`
- `Audit Workflow Delta`

Full histories:

```bash
.venv/bin/alphaxiv assistant history 019db0b1-df12-7587-99f6-0028445d2771
.venv/bin/alphaxiv assistant history 019db0b3-9566-7bfa-ba44-70b24294cd10
.venv/bin/alphaxiv assistant history 019db0b4-cc0b-73f4-aa80-31a1f5ae3d5e
.venv/bin/alphaxiv assistant history 019db0b4-c894-773f-8b98-ce937258004f
.venv/bin/alphaxiv assistant history 019db0be-04e2-7b72-a37a-bf517f73ef41
```

## Question Asked

Pressure-test the current Claim-State Authorization claims for `literate-workflow-programming` against the P2 gap papers and nearby alphaXiv search candidates.

The target claims were:

- CSA-C1: workflow specs become meaningful source only with validation gates, policy enforcement, and semantic debugging traces.
- CSA-C2: reviewable-run logs should be traces, not the source of truth.
- CSA-C3: markdown workflow files become programming substrate only with runtime binding, validation, policy enforcement, and provenance.
- CSA-C4: skills are code-like, but raw markdown skills are not portable production substrate.
- CSA-C5: local `spec-diff` experiments are proof candidates for source-linked drift detection.
- CSA-C6: contradiction state should be part of semantic debugging.

## Papers Or Claims In Scope

Existing P2 queue:

- `2603.05344` / Building Effective AI Coding Agents for the Terminal
- `2512.05470` / Everything is Context
- `2602.20478` / Codified Context
- `2604.08224` / Externalization in LLM Agents
- `2604.05278` / Spec Kit Agents
- `2505.20127` / Agentic AI Process Observability
- `2508.02736` / AgentSight
- `2602.11988` / Evaluating AGENTS.md
- `2601.20404` / On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents
- `2511.12884` / Agent READMEs
- `2508.11126` / AI Agentic Programming

Search-sweep candidates:

- `2603.23806` / Willful Disobedience: Automatically Detecting Failures in Agentic Traces
- `2603.29848` / AgentFixer
- `2603.08993` / Arbiter
- `2604.13108` / Formal Architecture Descriptors
- `2602.12670` / SkillsBench
- `2604.01687` / CoEvoSkills
- `2411.13768` / Evaluation-Driven Development and Operations of LLM Agents
- `2602.13855` / Claim-Level Auditability

## Extracted Takeaways

- Context-file evidence splits by metric and task risk. AGENTS.md-style files can improve efficiency while still hurting correctness or cost under other conditions.
- The source/runtime/debugging lead survived. P2 papers mostly add caveats and stronger mechanisms rather than a new lead frame.
- FASTRIC adds an important warning: more formal specifications do not monotonically improve conformance. The article should avoid implying that stricter specs always make agents behave better.
- Observability papers strengthen the trace/debugging claim, but current Reviewable Runs are not yet full semantic source maps.
- Skills are useful, but usefulness is not the same as portable production substrate. Skills need capability binding, selection control, and verification.
- Claim-level auditability looks like the cleanest next candidate for the contradiction-state / semantic-provenance claim.
- A final fresh audit session was attempted after these notes were drafted. The first retry only fetched abstracts before failing with `Missing Authorization`, and a non-mutating API-key-only retry was rejected for assistant writes.
- After browser auth was refreshed, the fresh audit did return, but it introduced claims not grounded in the retrieved summaries, including an `attention-sink` reading of `2601.20404`, a `semantic source maps` reading of `2602.11988`, and a `namespace control is solved` reading of `2604.03088`. I treated that final audit as useful adversarial pressure rather than as adopted synthesis.

## Adopted

- Added a metric/task-risk contradiction for context files.
- Added a specification-formality contradiction for `spec-diff` and conformance claims.
- Added a skill usefulness vs portability/selection contradiction.
- Added search-sweep papers to the intake queue.
- Preserved the lead frame while narrowing the next research pass to P2a.

## Rejected Or Parked

- Do not reopen the whole lead frame.
- Do not treat the assistant as evidence; use paper intake before body citations.
- Do not claim current Reviewable Runs already provide full semantic provenance.
- Do not claim raw markdown skills fail categorically. The stronger point is that skill value depends on curation, verification, capability binding, and routing.
- Do not turn `spec-diff` into a broad conformance proof.

## Where It Entered The Package

- [`../2026-04-21-claim-state-gap-contradiction-pass.md`](../2026-04-21-claim-state-gap-contradiction-pass.md)
- [`../../claim-ledger.md`](../../claims/claim-ledger.md)
- [`../../contradiction-register.md`](../../claims/contradiction-register.md)
- [`../../claim-scorecard.md`](../../claims/claim-scorecard.md)
- [`../../papers/index.md`](../../papers/index.md)

## Current Status

Distilled.
