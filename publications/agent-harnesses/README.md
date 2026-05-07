# Agent Harnesses

This is a minimal governed topic-discovery scaffold for the seed topic `agent harnesses`.

It exists because the current `content-agent run --workflow topic_discovery` surface requires a package argument and `status.yaml`, even for greenfield discovery. The topic has not cleared `topic_viability`, has not been initialized as a publication package, and should not move into research or essay iteration until a governed topic-discovery handoff says so.

## Current Surfaces

- status: `status.yaml`
- discovery evidence: `reviewable-runs/` artifacts from the active `topic_discovery` run

## Operator Boundary

- Treat this package as a pre-viability placeholder.
- Do not infer paper intake, research completion, or essay writability from this scaffold.
- Use `./content-agent run --workflow topic_discovery --package agent-harnesses` with explicit runtime inputs to decide whether the topic should become a real package, narrow research delta, pivot, parked idea, or blocked idea.
