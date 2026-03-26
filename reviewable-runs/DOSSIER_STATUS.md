# Dossier Status

This package distinguishes dossier status explicitly so readers do not confuse teaching artifacts with proof artifacts.

## Status Labels

### `synthetic teaching dossier`

Use this for examples designed to teach the framework shape.

These dossiers are realistic, but they are authored examples rather than reconstructed captures of one literal run.

### `real reconstructed run`

Use this for a dossier or proof packet built from an actual captured run.

The runtime happened first. The packet was reconstructed from the run artifacts afterward.

### `hybrid`

Use this when a dossier is anchored in a real run but includes synthetic additions, simplifications, or normalized records for teaching clarity.

## Why This Matters

The framework makes a strong claim about operational usefulness. That claim gets weaker when synthetic examples and real proof artifacts are mixed together without labels.

Status labels solve that problem by making the evidence class explicit.

## Current Default

The three canonical dossiers under `dossiers/` are currently labeled `synthetic teaching dossier`.

The first real proof artifact now lives under `proofs/coding-real-run/`.
