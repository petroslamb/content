# 01. Topic Discovery

The goal of this step was to find the alphaXiv topic vocabulary that best maps to broad multi-agent work, rather than assuming the obvious natural-language term would directly map to the best feed filters.

## Query: multi-agent

Command
```bash
alphaxiv feed filters search "multi-agent"
```

Raw output
- `artifacts/topic-search-multi-agent.txt`

What mattered
- Returned topics: `multi-agent-learning`, `agent-based-systems`, `agents`, `cs.RO`
- Returned organizations were not especially useful for this task.
- `agents` looked broad but potentially high recall.

Decision
- Keep `multi-agent-learning` and `agent-based-systems` as exact topic candidates.
- Keep `agents` as the broad adjacent topic for discovery.
- Do not use the organizations as primary filters.

## Query: multi-agent systems

Command
```bash
alphaxiv feed filters search "multi-agent systems"
```

Raw output
- `artifacts/topic-search-multi-agent-systems.txt`

What mattered
- Returned topics: `agent-based-systems`, `multi-agent-learning`, `reinforcement-learning`, `cs.RO`
- The result reinforces that alphaXiv maps this area partly through generic RL and robotics tags.

Decision
- Keep `agent-based-systems` and `multi-agent-learning`.
- Drop `reinforcement-learning` for now because it is too broad for the research question.
- Keep `cs.RO` only as a possible fallback, not as a main discovery surface.

## Query: agent collaboration

Command
```bash
alphaxiv feed filters search "agent collaboration"
```

Raw output
- `artifacts/topic-search-agent-collaboration.txt`

What mattered
- Returned topics: `agent-based-systems`, `multi-agent-learning`, `human-ai-interaction`, `cs.RO`
- The query did not reveal a distinct collaboration-specific topic namespace.

Decision
- Do not add a new topic from this query.
- Treat `human-ai-interaction` as off-target for the core shortlist.

## Query: multi-agent systems topic suggestions

Command
```bash
alphaxiv search topics "multi-agent systems"
```

Raw output
- `artifacts/search-topics-multi-agent-systems.txt`

What mattered
- Suggested topics matched the feed filter search results: `agent-based-systems`, `multi-agent-learning`, `reinforcement-learning`, `cs.RO`
- This confirmed that the feed and search surfaces were pointing to the same taxonomy.

Decision
- Use `agent-based-systems`, `multi-agent-learning`, and broad `agents` in the feed step.

## Query: multi-agent systems paper search

Command
```bash
alphaxiv search papers "multi-agent systems"
```

Raw output
- `artifacts/search-papers-multi-agent-systems.txt`

What mattered
- The search immediately surfaced strong recent candidates: `2602.15382` and `2601.04748`.
- It also surfaced older or less clearly central results such as `2505.16997`, `2511.13288`, and `2511.21572`.
- This confirmed that exact keyword search alone was useful for seed papers but not enough for ranking importance.

Decision
- Carry forward these initial seeds:
  - `2602.15382`
  - `2601.04748`
- Move to feed ranking to determine which recent papers are actually prominent and worth deeper inspection.

## Step Output

Chosen topic/filter terms for feed exploration:

- `agent-based-systems`
- `multi-agent-learning`
- `agents`

Why these:

- `agent-based-systems` is the closest literal taxonomy match.
- `multi-agent-learning` captures directly relevant agentic work.
- `agents` is the broad discovery surface needed because recent multi-agent work is often tagged under general agentic categories rather than a narrow multi-agent namespace.
