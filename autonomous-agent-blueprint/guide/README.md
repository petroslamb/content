# Guide: Operating Agents

This folder contains the current near-public package for *Operating Agents*: one preface and six essays aimed at skeptical builders moving from prototype systems to deployable agent architecture.

## Reading Order

| File | Title | Topic |
|------|-------|-------|
| [00-series-preface.md](./00-series-preface.md) | Operating Agents: Series Preface | Why most agent writing starts in the wrong place and why this series is organized around control layers |
| [01-action-tool-use.md](./01-action-tool-use.md) | Operating Agents I: When the Model Starts Doing Things | Agency as controlled state change, action surfaces, tool-use seams, and observation contracts |
| [02-reasoning-planning.md](./02-reasoning-planning.md) | Operating Agents II: The Lightest Correct Scaffold | Why most reasoning failures are scaffold failures and what the conservative default stack should be |
| [03-memory.md](./03-memory.md) | Operating Agents III: The Agent That Forgets | Memory as governance over time, typed memory layers, and forgetting as hygiene |
| [04-multi-agent.md](./04-multi-agent.md) | Operating Agents IV: One Agent Is Not Enough | Multi-agent as workflow decomposition, not intelligence multiplication |
| [05-safety.md](./05-safety.md) | Operating Agents V: The Attack Surface You Built | Safety as interface architecture across trust boundaries, tools, memory, retrieval, and handoffs |
| [06-optimization.md](./06-optimization.md) | Operating Agents VI: The Workflow Is the Object | Measurement-led improvement, the correct optimization order, and bounded self-improvement |

## Relationship to Other Materials

The essays are the reader-facing narrative layer. The broader `autonomous-agent-blueprint` package remains the reference layer for source notes, blueprints, case studies, and evaluation materials. Internal drafting support for this series also lives in this folder as `analysis_and_brainstorm.md` and `implementation_plan.md`.

## Word Counts (approximate)

| Part | Words |
|------|-------|
| Preface | ~1,000 |
| Part 1: Action | ~2,100 |
| Part 2: Reasoning | ~2,000 |
| Part 3: Memory | ~1,800 |
| Part 4: Multi-Agent | ~1,400 |
| Part 5: Safety | ~1,600 |
| Part 6: Optimization | ~1,500 |
| **Total** | **~11,700** |
