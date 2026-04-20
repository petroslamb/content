# Spec-Diff Experiment

Date: 2026-04-20

Status: research design note, not an accepted workflow change

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

## Open Design Questions

- Should the manifest be generated from `run_stage.py`, a separate `spec_diff.py`, or a workflow-specific validator?
- Should expected state be stored as an artifact, regenerated on demand, or both?
- Should ignored files such as PDFs be first-class local evidence in the manifest?
- Should source clauses use markdown headings, line numbers, or stable semantic anchors?
- Should imports be modeled as file dependencies, context layers, or capability bindings?
