# Spec-Diff Experiment

Date: 2026-04-20

Status: research design note, not an accepted workflow change

Prototype:

- Script: [`../scripts/spec_diff_paper_intake.py`](../scripts/spec_diff_paper_intake.py)
- Latest artifact: [`../artifacts/spec-diff/paper-intake-latest.json`](../artifacts/spec-diff/paper-intake-latest.json)

## Purpose

Test whether this repo's workflow docs, package status, paper indexes, validators, and reviewable-run logs can behave like a source-and-trace system rather than loose operational prose.

The experiment asks:

> Can a workflow stage contract compile into an expected-state manifest, and can a reviewable run report semantic drift between that expected state and the actual package state?

## Literature Pressure

The P0 batch makes this the highest-value experiment:

- ICM says folder structure and markdown contracts can organize sequential agent workflows.
- Natural-Language Agent Harnesses says harness logic can be externalized and executed through contracts and durable artifacts.
- AgentSPEX says workflow specifications can include explicit state, context, logging, checkpointing, replay, and validation.
- Bootstrapping Coding Agents says the specification is the stable artifact of record.
- TDAD says behavioral specs should generate tests and regression checks.
- ContextCov says instruction files should compile into enforceable constraints.
- SkVM says markdown skills need capability binding or compilation to become portable runtime substrate.

The experiment should therefore make the source/trace hierarchy explicit:

- source: workflow doc, package README, status config, evidence index
- compiled expectation: expected-state manifest
- trace: reviewable-run log
- debug output: drift findings linked back to source clauses

## Candidate First Target

Use `paper_intake` for `publications/literate-workflow-programming/`.

Reasons:

- It has a clear workflow contract in `workflows/paper-intake/README.md`.
- It has a package-local evidence surface: `papers/`.
- It has expected outputs: source PDFs, converted markdown, updated index.
- It already produced a launch pack and mark-done lifecycle log.
- It includes a real edge case: PDFs are intentionally gitignored while markdown/index/metadata are tracked.

## Minimal Manifest

The first version should produce a JSON manifest, not execute new work.

```json
{
  "package": "literate-workflow-programming",
  "stage": "paper_intake",
  "workflow_doc": "workflows/paper-intake/README.md",
  "default_skill": "markitdown-paper-intake",
  "source_context": [
    "publications/literate-workflow-programming/README.md",
    "publications/literate-workflow-programming/status.yaml",
    "publications/literate-workflow-programming/papers/index.md"
  ],
  "evidence_surface": "publications/literate-workflow-programming/papers",
  "expected_outputs": [
    "source PDFs under papers/",
    "converted markdown under papers/markdown/",
    "paper index entry for each intaken source"
  ],
  "done_when": [
    "selected papers are stored locally and the package evidence index is current"
  ]
}
```

## Minimal Drift Checks

Start with deterministic checks:

- every local markdown link in `papers/index.md` exists
- every local metadata link in `papers/index.md` exists
- every local PDF link in `papers/index.md` exists locally, even if ignored by git
- every PDF in the P0 intake has a corresponding markdown file
- every markdown file in `papers/markdown/` has an index entry
- status marks `paper_intake` done only after at least one local source and index entry exist
- lifecycle logs exist for launch and mark-done when the stage is marked done

Then add semantic checks:

- index entries distinguish locally intaken papers from queued papers
- conversion notes identify noisy markdown where needed
- ignored PDFs are called out explicitly so reviewers do not confuse git status with local evidence state
- the next lifecycle stage is `research`, not `essay_iteration`

## Source-Map Shape

A useful drift finding should point to both sides:

- the source clause that created the expectation
- the observed file, status field, or log record

Example:

```json
{
  "finding": "indexed_markdown_missing",
  "source_clause": "papers/index.md: Local markdown",
  "expected_path": "publications/literate-workflow-programming/papers/markdown/2604.13346.md",
  "observed": "missing",
  "severity": "blocking"
}
```

The current reviewable-run logs mostly answer whether a lifecycle command ran. `spec-diff` would answer whether the resulting package state matches the declared workflow contract.

## Non-Goals

- Do not build a general compiler yet.
- Do not invent markdown imports yet.
- Do not change all workflows at once.
- Do not make routine lifecycle logs heavier.
- Do not move this into `phased-strategy/` until it changes proof-run requirements.

## Success Criteria

This experiment is worth extracting back into the workflow system if it can:

1. catch a real inconsistency in package paper intake or stage status,
2. explain the inconsistency using source-linked findings,
3. stay lightweight enough to run as a validation command,
4. produce a reviewable-run trace that is more useful than an execution receipt.

## First Prototype Result

The first run produced a useful warning that the standard `npm run check` bundle did not catch: local PDFs were intentionally present but gitignored, while `papers/index.md` did not explicitly tell reviewers that the `Local PDF` links refer to ignored local evidence rather than tracked files.

That drift was fixed by adding a conversion note to `papers/index.md`:

> Local PDFs are intentionally gitignored third-party evidence. Treat the `Local PDF` links above as local evidence pointers, not as expected tracked files.

After the fix, the prototype report passes:

- 7 indexed local papers
- 7 local PDFs
- 7 converted markdown files
- 6 metadata files
- 0 blocking findings
- 0 warnings

This is a small but real result: `spec-diff` caught a reviewer-facing semantic mismatch, not a missing file or broken link.

## Reviewable Runs Wrapper Result

On 2026-04-21, this experiment was wrapped in a lightweight Phase 1.5 proof-run candidate: [`../../../reviewable-runs/logs/2026-04-21_literate-workflow-programming_spec-diff-proof-candidate.md`](../../../reviewable-runs/logs/2026-04-21_literate-workflow-programming_spec-diff-proof-candidate.md).

The wrapper added value, but mainly by limiting the claim:

- it made the prompt-glue and approval boundary explicit,
- it confirmed that the package next-action resolver correctly points to `research`,
- it exposed that guided stages with `launch_mode: none` are still not directly executable proof runs,
- it showed that this run should not be promoted as retained proof because the useful `spec-diff` finding happened during prototype creation, before the wrapper.

The next useful test is not another wrapper over the same artifact. It is a fresh `spec-diff` run during P1 intake or against a different package with known evidence drift.

## P1 Intake Result

The 2026-04-21 P1 intake gave the experiment a real second test. Six queued P1 papers were downloaded, converted, and stored locally before the index was updated:

- Open Agent Specification
- A Declarative Language for Building And Orchestrating LLM-Powered Agent Workflows
- FASTRIC
- ALARA for Agents
- Progent
- When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail

The pre-index `spec-diff` report found 24 warnings: six local PDFs were not indexed, six markdown files were not indexed, six metadata files were not indexed, and the six papers still appeared in the intake queue. The report is retained at [`../artifacts/spec-diff/paper-intake-p1-preindex.json`](../artifacts/spec-diff/paper-intake-p1-preindex.json).

That run also found a prototype bug: version normalization only handled `v1` through `v3`, so `2510.04173v4` initially avoided the queued-paper check. The prototype now strips arbitrary numeric version suffixes.

After the index and `status.yaml` were updated, the latest report passed:

- 13 indexed local papers
- 13 local PDFs
- 13 converted markdown files
- 12 metadata files
- 11 queued papers
- 0 blocking findings
- 0 warnings

This is a stronger result than the first wrapper. `spec-diff` caught ordinary intake drift while work was in progress, then verified that the package returned to a consistent declared state.

## Second-Package Result

On 2026-04-21, the experiment was tested outside this package with `publications/illusion-of-swarm/`.

That package was a useful second target because its paper evidence predates the current `papers/markdown/` convention. It had a published essay, a `paper_intake.done: true` lifecycle state, root-level text captures, a few PDFs and root markdown files, alphaXiv artifacts, and a thin generic `papers/index.md`.

The first retained `illusion-of-swarm` report found 19 warnings:

- the paper index was too thin for a done evidence surface,
- mixed local evidence conventions were not called out,
- 12 local paper evidence files were not represented in the index,
- 5 draft-cited arXiv IDs had no local paper file or alphaXiv artifact record.

The run also exposed a validator assumption before the retained report was finalized: scanning too much paper text made reference-list arXiv IDs look like local evidence. The second-package validator now treats only file names and header-area IDs as local paper identity, while alphaXiv artifact support comes from artifact filenames.

The repair stayed inside the planned boundary. Only `publications/illusion-of-swarm/papers/index.md` changed. It now enumerates the existing local evidence, names the mixed storage convention, and classifies the five unresolved draft-citation gaps without downloading papers or changing the published essay.

The latest `illusion-of-swarm` report passes:

- 12 local evidence files
- 13 cited arXiv IDs in the canonical draft
- 8 artifact-supported arXiv IDs
- 5 classified gaps
- 0 blocking findings
- 0 warnings

The Reviewable Runs record is [`../../../reviewable-runs/logs/2026-04-21_illusion-of-swarm_spec-diff-proof-candidate.md`](../../../reviewable-runs/logs/2026-04-21_illusion-of-swarm_spec-diff-proof-candidate.md).

This meets the requested second-package threshold as a proof candidate. It should not be promoted to a root validator or retained proof yet. The evidence says the pattern is worth a promotion decision, not that the repo-wide interface is ready.

## Adjacent Governance Transfer

The Confidence Debt package and the external `eth-llm` contradiction-ledger artifacts add one useful future direction without changing the current prototype scope. Confidence Debt's artifact gate asks promoted claims to carry evidence state, contradiction state, and expiry condition. The `eth-llm` governance-core protocol turns that into operating artifacts: authority order, claim ledgers, contradiction registers, evidence maps, scores, and final contradiction rollups.

For this experiment, the important transfer is narrow: `spec-diff` should eventually be able to report contradiction state, not only evidence-surface drift. The current validators already have a primitive version of this in `illusion-of-swarm`: cited papers with no local evidence were classified as gaps instead of silently treated as missing markdown. A richer manifest could make this explicit:

```json
{
  "authority_order": ["workflow_doc", "status_yaml", "paper_index", "run_trace"],
  "claim_state": "supported | contested | inference | parked | blocked",
  "contradiction_state": "none | classified | unresolved | resolved | blocking",
  "validation_state": "pass | warning | fail | skipped | out_of_scope",
  "trace_state": "reviewable-run or report id"
}
```

Do not implement this in the package-local validator yet. Keep it as a design pressure for the promotion memo.

## Open Design Questions

- Should the manifest be generated from `run_stage.py`, a separate `spec_diff.py`, or a workflow-specific validator?
- Should expected state be stored as an artifact, regenerated on demand, or both?
- Should ignored files such as PDFs be first-class local evidence in the manifest?
- Should source clauses use markdown headings, line numbers, or stable semantic anchors?
- Should imports be modeled as file dependencies, context layers, or capability bindings?
- Should future reports model `authority_order` and `contradiction_state`, or should those live in a separate claim-audit artifact?
