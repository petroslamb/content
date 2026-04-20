# alphaXiv Discussion Cluster: ICM Workflow Design

Date: 2026-04-20

Session ids:

- `019dabcb-1fff-7d63-b509-f3ecf087b2ac` / `Robust autonomy workflow design`
- `019dabc9-1e0e-72e1-8d5f-9c19b676fd14` / `ICM Folder vs Framework`
- `019dabc8-7190-7403-9a1e-22e00ca2e2e3` / `ICM vs. Prod Agent Repo`
- `019dabc6-5b80-7537-bb7b-ce33954cc023` / `Agent harness design test`

Full histories:

```bash
.venv/bin/alphaxiv assistant history 019dabcb-1fff-7d63-b509-f3ecf087b2ac
.venv/bin/alphaxiv assistant history 019dabc9-1e0e-72e1-8d5f-9c19b676fd14
.venv/bin/alphaxiv assistant history 019dabc8-7190-7403-9a1e-22e00ca2e2e3
.venv/bin/alphaxiv assistant history 019dabc6-5b80-7537-bb7b-ce33954cc023
```

## Question Asked

These sessions were early follow-ups around ICM and whether folder-structured markdown workflows are sufficient for robust autonomy, production agent repos, and harness design.

## Papers Or Claims In Scope

- `2603.16021` Interpretable Context Methodology
- local `phased-strategy/` workflow-system implications before the new package existed
- local Reviewable Runs direction
- local workflow docs, skills, and package-state architecture

## Extracted Takeaways

The sessions pushed four tensions into the package:

- passive markdown contracts are useful but insufficient without enforcement
- ICM-style folder scoping needs least-privilege and runtime validation when autonomy increases
- context files can help or hurt depending on minimality, scope, and enforceability
- reviewable logs should evolve toward semantic debugging rather than plain execution receipts

## Adopted

- The new package treats ICM as an anchor, not a finished architecture.
- `reviewable logs as semantic debugging/source maps` entered the claim ledger.
- `spec-diff` became the first implementation experiment because it tests declared workflow contracts against actual package state.
- The package keeps workflow-system research outside `phased-strategy/` until it changes proof-run requirements.

## Rejected Or Parked

- Do not assume folder structure alone supplies robust workflow governance.
- Do not treat every context file as beneficial.
- Do not promote semantic debugging into Reviewable Runs before a small validator proves it can stay lightweight.

## Where It Entered The Package

- [`../2026-04-20-icm-and-markdown-workflows.md`](../2026-04-20-icm-and-markdown-workflows.md)
- [`../2026-04-20-p0-intake-synthesis.md`](../2026-04-20-p0-intake-synthesis.md)
- [`../2026-04-20-spec-diff-experiment.md`](../2026-04-20-spec-diff-experiment.md)
- [`../../claim-ledger.md`](../../claim-ledger.md)

## Current Status

Distilled as a bounded cluster. This note backfills only sessions already named in the package's ICM research note.
