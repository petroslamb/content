# Governance Record: Failure Review

## Plausible Failure

The package could claim to be API-key-first while still leaving browser-coupled behavior, docs, or dependency assumptions in the steady-state path, creating a misleading public interface.

## Failure Class

Auth model drift and packaging inconsistency.

## Control Gap

The refactor touched runtime code, CLI behavior, docs, metadata, tests, and publishability surfaces at once. Without an explicit review surface, it would be easy to verify only the code path or only the docs and miss the mismatch between them.

## Corrective Direction

- keep auth semantics and docs under the same review packet when this surface changes
- preserve local verification outputs alongside the commit boundary
- treat later auth or CLI changes as separate bounded runs instead of extending this packet indefinitely
