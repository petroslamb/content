# Topic Vocabulary Map

Run id: `phase-2-primary-topic-discovery-proof`
Workflow: `topic_discovery`
Package context: `literate-workflow-programming`
Discovery trigger: `primary proof for autonomous content-agent publication workflows and specification-surface governed runtime`
Target ambition: `north_star_flagship`

## Search Commands

| Query | Command | Useful Topics | Noisy Topics | Decision |
| :--- | :--- | :--- | :--- | :--- |
| `primary proof autonomous content agent publication workflow specification surface` | `.venv/bin/alphaxiv search topics 'primary proof autonomous content agent publication workflow specification surface'` | none returned | none returned | drop as too repo-local |
| `software engineering agents` | `.venv/bin/alphaxiv search topics 'software engineering agents'` | `agent-based-systems`, `cs.MA`, `cs.LG` | `reinforcement-learning` | keep only as broad agent backdrop |
| `coding agents` | `.venv/bin/alphaxiv search topics 'coding agents'` | `agent-based-systems`, `agents`, `multi-agent-learning` | `reinforcement-learning` | keep as broad recall surface |
| `autonomous agents software engineering workflow verification specification` | `.venv/bin/alphaxiv search papers 'autonomous agents software engineering workflow verification specification'` | specification-driven construction, agentic software engineering, event-sourced agent workflows, developer intent coverage | social/legal/ethical verification | keep |
| `AI agents software engineering benchmark repository workflow` | `.venv/bin/alphaxiv search papers 'AI agents software engineering benchmark repository workflow'` | repository-level coding agents, long-horizon benchmarks, DevOps-cycle evaluation | generic teammate framing | keep |
| `specification driven software engineering agents benchmark` | `.venv/bin/alphaxiv search papers 'specification driven software engineering agents benchmark'` | SWE-AGI, Spec Kit Agents, TDAD, project-development benchmarks | microservice generation side routes | keep |
| `repository level coding agents long horizon software engineering` | `.venv/bin/alphaxiv search papers 'repository level coding agents long horizon software engineering'` | NL2Repo-Bench, SWE-EVO, SWE-Bench Pro, SWE-CI | navigation-only papers | keep as evaluation vocabulary |

## Decision

Primary topic surfaces:

- specification-driven software construction
- context-grounded agentic workflows
- repository-level and long-horizon coding-agent benchmarks
- CI/evolution evaluation for maintainability rather than one-shot task success
- event-sourced or append-only execution traces for agent state and mutation boundaries
- repo-local governed runtime proof: declared workflow, admitted context, gate contract, resolved run, run record, and review gate

Broad recall surfaces:

- `agentic-frameworks`
- `agents`
- `cs.SE`
- `tool-use`
- `model-observability`
- `agent-based-systems`

Dropped surfaces:

- reinforcement-learning topic slugs
- generic "AI teammate" product framing
- benchmark-score-only framing
- pure event-sourcing architecture without editorial or publication governance

Why:

The topic is not "can agents code?" or "do benchmarks improve?" The publishable object is narrower: autonomy becomes operationally credible only when an agent run is constrained by declared specifications and leaves reviewable proof. The repo-local Phase 2 runtime is therefore not just an implementation detail; it is part of the evidence surface for a larger article object.
