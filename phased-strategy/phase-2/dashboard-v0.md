# Local Cockpit v0

## Goal

The cockpit is the first browser surface for the Phase 2 platform.

It should expose package state, pending gates, and recent runs without turning the browser into a new source of truth.

## Dependency Rule

The cockpit comes after stable gate artifacts and stable trace minimums.

It should consume:

- package manifests
- lifecycle checker output
- `reviewable-runs/logs/`
- `reviewable-runs/gates/`

It should not lead the design of those artifacts.

## Required Views

### Fleet Status

Show:

- package name
- current stage
- next valid stage
- last updated timestamps
- active lifecycle warnings

Data source:

- package `status.yaml`
- lifecycle checker output

### Pending Review Gates

Show:

- package
- workflow and step
- gate class
- preview link
- created time
- current status

Data source:

- `reviewable-runs/gates/`

### Recent Runs

Show:

- recent run records
- outcome
- package
- workflow or stage
- timestamp

Data source:

- `reviewable-runs/logs/`

## Minimum Actions

The cockpit only needs enough actions to support the gate model:

- open package
- open preview artifact
- open evidence artifact
- approve gate
- reject gate
- re-run safe validation

Anything more ambitious should wait until the underlying gate and trace contracts prove stable.

## Constraints

- local-first
- file-backed data sources
- no cloud dependency
- no hidden second system of record

The cockpit may use a local API or index for performance, but filesystem truth remains authoritative.

## Non-Goals

Cockpit v0 should not include:

- user accounts
- workspace sharing
- cloud job orchestration
- full content editing
- analytics as a primary function
- a general control plane for launching arbitrary work

## Success Read

Cockpit v0 is good enough when:

1. pending gates are visible without reading terminal logs
2. recent runs are inspectable from one place
3. approval decisions can be made against the gate artifacts cleanly
4. the cockpit never becomes the only place where truth exists
