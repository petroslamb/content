# Content Repository

## Description

This repository contains research and publication packages on enterprise agents, agent architectures, and neural architecture adoption. The current root-level structure is anchored around three documented packages with their own maintained `README.md` files.

## Current Packages

### [`ai_agents_enterprise_state/`](./ai_agents_enterprise_state/)

Research and writing package for **The Autonomy Tax**, a three-piece publication series on why enterprise agents fail on control rather than intelligence.

- Implemented publication package: `v8A`, `v8B`, `v8C`
- Evidence layer: `sources/`, including a source manifest and derived casebook
- Scoring assets: `assets/` with scorecard templates and rubric material

Start with: `ai_agents_enterprise_state/README.md`

### [`autonomous-agent-blueprint/`](./autonomous-agent-blueprint/)

Local research corpus on foundation agents organized into a practical architecture guide and chapter-specific blueprints.

- Main synthesis: `agentic-architectures-blueprint.md`
- Chapter mapping: `foundation-agents-practical-chapters-guide.md`
- Supporting material: `practical-chapter-blueprints/` and `papers/`

Start with: `autonomous-agent-blueprint/README.md`

### [`hardware_compatibility_architecture_2023_2025/`](./hardware_compatibility_architecture_2023_2025/)

Published research project: **What Actually Works: The Hardware Compatibility Filter in Neural Architecture (2023-2025)**. This package studies why GPU-friendly architectures dominate production and includes the associated hardware friction methodology and dataset.

- Canonical article and publication drafts
- Quantitative scorecard and research artifacts
- Supporting evidence on MoE adoption, FlashAttention, and SSM limits
- Links to the public hardware friction scorecard dataset repository

Start with: `hardware_compatibility_architecture_2023_2025/README.md`

## Other Top-Level Directories

These directories exist at the repository root but do not currently expose a package-level `README.md`:

- `agent_revolution/`
- `neural_architectures/`
- `paper_reviews/`
- `reference/`
- `rooted layers/`
- `security_research/`

Treat them as supporting or legacy material unless they are documented separately.

## Notes

- This root README summarizes the packages that currently define their own root-level documentation.
- For current status, entry points, and working rules, use each package README as the source of truth.
