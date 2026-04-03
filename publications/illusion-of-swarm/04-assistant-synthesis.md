# 04. Assistant Synthesis

The assistant was used only after the deterministic retrieval and inspection steps were complete. The goal here was to pressure-test the ranking, not to discover papers from scratch.

## Cross-Paper Comparison

Command
```bash
alphaxiv assistant start "Compare these recent multi-agent papers: 2602.01848, 2601.04748, 2602.15382, 2603.00349, 2602.11865. Rank them by importance and explain the ranking in terms of novelty, practical impact, and likely lasting relevance."
```

Raw output
- `artifacts/assistant-shortlist.txt`

What mattered
- The assistant ranked the five papers as:
  1. `2602.01848` ROMA
  2. `2601.04748` When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail
  3. `2603.00349` EmCoop
  4. `2602.15382` The Vision Wormhole
  5. `2602.11865` Intelligent AI Delegation
- The assistant put ROMA first because it looks like the most reusable, empirically grounded architecture contribution.
- It put the single-agent-versus-multi-agent paper second because its conceptual impact could be very large even if it is less likely to become the default production architecture.
- It viewed EmCoop as durable evaluation infrastructure, Vision Wormhole as high-novelty but more speculative, and Intelligent AI Delegation as useful but less technically decisive.

Decision
- Accept the assistant ranking as the final order.
- Keep the same five papers; the assistant changed the ordering slightly rather than changing the shortlist itself.

## What Changed

Before the assistant step, the shortlist was already stable, but the ordering between ROMA and the single-agent-with-skills paper was still debatable.

What the assistant clarified:

- `2602.01848` should rank first if the definition of importance emphasizes a reusable architecture with strong evidence and likely practitioner uptake.
- `2601.04748` should rank first only under a more contrarian or theory-heavy interpretation of importance, where challenging the field's assumptions counts more than providing the most adoptable system.

Decision
- Use the pragmatic ranking with ROMA first.
- Preserve the caveat that `2601.04748` may age especially well as a foundational critique of the field.
