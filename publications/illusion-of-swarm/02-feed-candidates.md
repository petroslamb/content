# 02. Feed Candidates

This step used the 90-day feed to convert topic candidates into a ranked candidate pool. The goal was not to take the feed at face value, but to see which papers repeatedly surfaced across multiple importance proxies.

## Query Set: `agent-based-systems`

Commands
```bash
alphaxiv feed list --interval 90-days --topic agent-based-systems --sort hot --limit 10
alphaxiv feed list --interval 90-days --topic agent-based-systems --sort likes --limit 10
alphaxiv feed list --interval 90-days --source github --topic agent-based-systems --sort most-stars --limit 10
```

Raw output
- `artifacts/feed-hot-agent-based-systems.txt`
- `artifacts/feed-likes-agent-based-systems.txt`
- `artifacts/feed-most-stars-agent-based-systems.txt`

What mattered
- The exact `agent-based-systems` topic was noisier than expected.
- Some returned items were clearly relevant, but the overall signal was weaker than the broader `agents` surface.
- The GitHub-ranked output looked especially messy and duplicate-prone.

Decision
- Do not rely on `agent-based-systems` as the primary ranking surface.
- Keep it only as a supporting cross-check for explicitly multi-agent phrasing.

## Query Set: `multi-agent-learning`

Commands
```bash
alphaxiv feed list --interval 90-days --topic multi-agent-learning --sort hot --limit 10
alphaxiv feed list --interval 90-days --topic multi-agent-learning --sort likes --limit 10
alphaxiv feed list --interval 90-days --source github --topic multi-agent-learning --sort most-stars --limit 10
```

Raw output
- `artifacts/feed-hot-multi-agent-learning.txt`
- `artifacts/feed-likes-multi-agent-learning.txt`
- `artifacts/feed-most-stars-multi-agent-learning.txt`

What mattered
- `multi-agent-learning` surfaced directly relevant recent items, but still mixed together general agentic work and broader RL-flavored papers.
- Strong visible candidates included:
  - `2602.11865` Intelligent AI Delegation
  - `2602.19672` SkillOrchestra
  - `2601.12538` Agentic Reasoning for Large Language Models
  - `2601.07055` Dr. Zero
- This surface was useful, but not sufficient by itself to isolate the strongest multi-agent systems papers.

Decision
- Keep `2602.11865` as a direct candidate.
- Treat `2602.19672`, `2601.12538`, and `2601.07055` as adjacent or enabling papers rather than automatic finalists.

## Query Set: `agents`

Commands
```bash
alphaxiv feed list --interval 90-days --topic agents --sort hot --limit 10
alphaxiv feed list --interval 90-days --topic agents --sort likes --limit 10
alphaxiv feed list --interval 90-days --source github --topic agents --sort most-stars --limit 10
```

Raw output
- `artifacts/feed-hot-agents.txt`
- `artifacts/feed-likes-agents.txt`
- `artifacts/feed-most-stars-agents.txt`

What mattered
- `agents` was the strongest discovery surface overall.
- The GitHub-ranked agent feed surfaced the most compelling recent systems candidates:
  - `2602.01848` ROMA
  - `2603.00349` EmCoop
  - `2601.01885` Agentic Memory
  - `2602.23008` Exploratory Memory-Augmented LLM Agent
- The likes-ranked agent feed also surfaced high-engagement adjacent papers:
  - `2602.08234` SkillRL
  - `2601.14192` Toward Efficient Agents
  - `2601.12538` Agentic Reasoning for Large Language Models

Decision
- Treat `agents` as the main ranking surface for the rest of the workflow.
- Pull the following into the inspection pool:
  - `2602.01848`
  - `2603.00349`
  - `2601.01885`
  - `2602.23008`
  - `2601.14192`

## Broad Baselines

Commands
```bash
alphaxiv feed list --interval 90-days --sort hot --limit 20
alphaxiv feed list --interval 90-days --sort likes --limit 20
alphaxiv feed list --interval 90-days --source github --sort most-stars --limit 20
```

Raw output
- `artifacts/feed-hot-baseline.txt`
- `artifacts/feed-likes-baseline.txt`
- `artifacts/feed-most-stars-baseline.txt`

What mattered
- The baseline confirmed that exact multi-agent tagging alone would miss some of the most prominent recent agentic work.
- The broad feed also confirmed that some highly ranked papers were off-target for this question and needed manual inspection.
- Broad rankings reinforced the visibility of:
  - `2601.14192`
  - `2601.01885`
  - `2601.12538`
  - `2602.08234`

Decision
- Use the broad baseline only as a guardrail against missing important papers.
- Continue with manual inspection rather than blindly trusting any one feed sort.

## Candidate Pool After Feed Stage

Primary inspection pool:

- `2602.01848` ROMA
- `2603.00349` EmCoop
- `2601.04748` When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail
- `2602.15382` The Vision Wormhole
- `2602.11865` Intelligent AI Delegation
- `2601.01885` Agentic Memory
- `2602.23008` Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization
- `2601.14192` Toward Efficient Agents: Memory, Tool learning, and Planning

Secondary near-misses from feed prominence:

- `2602.08234` SkillRL
- `2601.12538` Agentic Reasoning for Large Language Models
- `2601.07055` Dr. Zero
- `2602.19672` SkillOrchestra

Why this pool:

- It combines exact multi-agent search hits with recent feed prominence and GitHub traction.
- It intentionally includes a few adjacent agentic papers to test whether they should displace direct multi-agent work in the final list.
