# Important Multi-Agent Papers From The Last 3 Months

This note captures a full alphaXiv CLI research workflow run on 2026-03-16 for the question:

> Which papers from the last 3 months look most important for multi-agent systems?

Scope and constraints:

- Date window: roughly the prior 90 days
- Retrieval first, synthesis second
- Importance heuristic: feed prominence, engagement, GitHub traction, and substantive multi-agent contribution
- Durable raw outputs are stored under `artifacts/`

Workflow files:

- [01-topic-discovery.md](01-topic-discovery.md)
- [02-feed-candidates.md](02-feed-candidates.md)
- [03-paper-inspection.md](03-paper-inspection.md)
- [04-assistant-synthesis.md](04-assistant-synthesis.md)
- [05-final-shortlist.md](05-final-shortlist.md)

Raw artifacts:

- `artifacts/`

Final shortlist:

1. `2602.01848` ROMA: Recursive Open Meta-Agent Framework for Long-Horizon Multi-Agent Systems
2. `2601.04748` When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail
3. `2603.00349` EmCoop: A Framework and Benchmark for Embodied Cooperation Among LLM Agents
4. `2602.15382` The Vision Wormhole: Latent-Space Communication in Heterogeneous Multi-Agent Systems
5. `2602.11865` Intelligent AI Delegation

The shortlist and ranking were produced from deterministic CLI retrieval plus one final assistant comparison pass. The assistant did not replace the search process; it only refined the ordering at the end.
