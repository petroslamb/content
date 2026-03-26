# Contributing

Thank you for your interest in improving the Autonomous Agent Blueprint repository. This is a builder-first architecture manual designed to help teams choose, justify, and review agent system designs before implementation.

## Before Contributing

- Read `README.md` to understand the package structure and reading paths.
- Read `MAINTENANCE.md` for source intake rules, quality policy, confidence guidelines, and update requirements.

## How to Contribute

### Add a New Paper Note

The `reference/papers/` directory contains distilled notes on individual research papers that anchor the blueprints.

**Requirements:**
- The paper must be relevant to one of the six practical themes: Memory, Reasoning & Planning, Action, Optimization, Multi-Agent, or Safety.
- The paper should either be cited by an existing blueprint or represent a "Named Method" that builders should know.
- Follow the template and style of existing notes in `reference/papers/` (mimic an existing note if no dedicated template file is present).
- Include: clear summary, key claims, practical takeaways, limitations, and confidence assessment.

**Process:**
1. Add your note file to `reference/papers/` with a clear, lowercase filename (e.g., `new_paper.md`).
2. Update `reference/source-index.md` to include the new paper in the appropriate theme's table.
3. Update `reference/literature-quality.md` if the paper's quality assessment differs from defaults.
4. Update the relevant blueprint or use case only if the paper changes the package guidance.
5. Record the change in `CHANGELOG.md`.
6. Open a PR describing the paper, its relevance, and where it changed the package.

### Suggest Blueprint Changes

Blueprints are the stable core. Changes require strong evidence and consensus.

**Requirements:**
- Proposals must be backed by sources (papers, production case studies) or compelling gap analysis.
- Do not propose changes for stylistic preferences alone; defaults are intentional.
- If a blueprint is missing coverage, reference the specific section and explain the gap.

**Process:**
1. Open an issue with the prefix `[Blueprint Change]` in the title.
2. Include:
   - Current text and location
   - Proposed change
   - Supporting evidence (papers, case studies, benchmarks)
   - Impact on use cases and package defaults
3. Expect discussion; maintainers will evaluate based on source quality, practical relevance, and consistency with the repo's philosophy.
4. Changes to core documents may require updates to multiple locations (blueprint, companion note, source index).

### Add a Use Case

**Use Cases** (`implementation/use-cases/`) compose multiple blueprints into end-to-end reference architectures for common scenarios (enterprise, coding, web, and similar bounded workflows).

**Requirements:**
- Use cases must demonstrate composition of at least two blueprints with clear rationale.
- Follow the structure and depth of existing examples.

**Process:**
1. Add new use cases under `implementation/use-cases/`.
2. Ensure the document cross-links to relevant blueprints and source notes.
3. Update `CHANGELOG.md`.
4. Open a PR with a clear description of the scenario and what the use case illustrates.

### Report Gaps

Found something missing? The repository deliberately excludes some territories (see `DEPRIORITIZED_TERRITORIES.md` if it exists), but there may be genuine gaps within scope.

**Process:**
1. Open an issue with the prefix `[Gap]` in the title.
2. Include:
   - Clear description of what the blueprints or support materials do not cover
   - Why it matters for builders (impact and user personas)
   - Any known solutions or workarounds you can suggest
   - Which theme(s) are affected (memory, reasoning, action, etc.)
   - Priority assessment:
     - Critical: blocks production deployments
     - High: important but has workarounds
     - Medium: would improve guidance
     - Low: niche or speculative

## Review Process

- All contributions are reviewed by maintainers.
- Contributions to core guidance (blueprints) require consensus and strong source backing.
- Documentation improvements are welcome, but this package prefers fewer clearer docs over more navigation layers.
- Continuous integration may check formatting and link validity.
- See `MAINTENANCE.md` for detailed update rules and confidence policy.

## Community Guidelines

- Be precise and practical. This repository prioritizes actionable defaults over exhaustive coverage.
- Cite sources. Claims about what works should be backed by research papers or production evidence.
- Respect the scope: focus on digital, tool-using enterprise agents. Out-of-scope topics include robotics, pure perception systems, frontier alignment theory, and scientific discovery agents (see `DEPRIORITIZED_TERRITORIES.md` if present).
- Assume readers are experienced engineers who need decision rules, not academic surveys.

Thank you for helping make this resource better for the agent engineering community.
