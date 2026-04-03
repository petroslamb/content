# 03. Paper Inspection

This step inspected the candidate pool one paper at a time using the deterministic paper surfaces. The question at this stage was not just whether a paper was strong, but whether it was genuinely important for multi-agent systems specifically.

## Candidate: `2601.04748`

Commands
```bash
alphaxiv paper show 2601.04748
alphaxiv paper abstract 2601.04748
alphaxiv paper summary 2601.04748
alphaxiv paper resources 2601.04748
alphaxiv paper similar 2601.04748 --limit 5
```

Raw output
- `artifacts/paper-show-2601.04748.txt`
- `artifacts/paper-abstract-2601.04748.txt`
- `artifacts/paper-summary-2601.04748.txt`
- `artifacts/paper-resources-2601.04748.txt`
- `artifacts/paper-similar-2601.04748.txt`

What mattered
- The paper directly asks when multi-agent systems should be replaced by a single agent with skills.
- The summary points to large efficiency gains while exposing a real scaling limit for skill-based replacement.
- This is both a systems paper and a conceptual correction to the field.

Decision
- Keep. This became one of the strongest shortlist candidates because it directly tests whether multi-agent structure is necessary at all.

## Candidate: `2602.01848`

Commands
```bash
alphaxiv paper show 2602.01848
alphaxiv paper abstract 2602.01848
alphaxiv paper summary 2602.01848
alphaxiv paper resources 2602.01848
alphaxiv paper similar 2602.01848 --limit 5
```

Raw output
- `artifacts/paper-show-2602.01848.txt`
- `artifacts/paper-abstract-2602.01848.txt`
- `artifacts/paper-summary-2602.01848.txt`
- `artifacts/paper-resources-2602.01848.txt`
- `artifacts/paper-similar-2602.01848.txt`

What mattered
- The abstract presents ROMA as a reusable recursive framework for long-horizon multi-agent systems.
- The GitHub traction is unusually strong for such a recent paper.
- The summary endpoint did not have an overview yet, but the paper still looked like the strongest direct architecture contribution.

Decision
- Keep. ROMA stayed in the top tier even without an overview because the architecture, benchmarks, and traction all looked strong.

## Candidate: `2603.00349`

Commands
```bash
alphaxiv paper show 2603.00349
alphaxiv paper abstract 2603.00349
alphaxiv paper summary 2603.00349
alphaxiv paper resources 2603.00349
alphaxiv paper similar 2603.00349 --limit 5
```

Raw output
- `artifacts/paper-show-2603.00349.txt`
- `artifacts/paper-abstract-2603.00349.txt`
- `artifacts/paper-summary-2603.00349.txt`
- `artifacts/paper-resources-2603.00349.txt`
- `artifacts/paper-similar-2603.00349.txt`

What mattered
- EmCoop is a framework and benchmark for embodied cooperation among LLM agents.
- The summary endpoint had no overview yet, but the abstract made the benchmark contribution clear.
- This is less about orchestration mechanics and more about evaluation infrastructure for cooperative agents.

Decision
- Keep. It looked like the strongest benchmarking and evaluation candidate in the pool.

## Candidate: `2602.15382`

Commands
```bash
alphaxiv paper show 2602.15382
alphaxiv paper abstract 2602.15382
alphaxiv paper summary 2602.15382
alphaxiv paper resources 2602.15382
alphaxiv paper similar 2602.15382 --limit 5
```

Raw output
- `artifacts/paper-show-2602.15382.txt`
- `artifacts/paper-abstract-2602.15382.txt`
- `artifacts/paper-summary-2602.15382.txt`
- `artifacts/paper-resources-2602.15382.txt`
- `artifacts/paper-similar-2602.15382.txt`

What mattered
- The paper proposes a latent-space communication mechanism for heterogeneous multi-agent systems.
- The summary claims reduced communication overhead and a more favorable scaling pattern.
- The GitHub traction is low so far, but the mechanism is novel enough to warrant inclusion.

Decision
- Keep. This became the most interesting communication-mechanism candidate, with higher novelty than many better-known adjacent papers.

## Candidate: `2602.11865`

Commands
```bash
alphaxiv paper show 2602.11865
alphaxiv paper abstract 2602.11865
alphaxiv paper summary 2602.11865
alphaxiv paper resources 2602.11865
alphaxiv paper similar 2602.11865 --limit 5
```

Raw output
- `artifacts/paper-show-2602.11865.txt`
- `artifacts/paper-abstract-2602.11865.txt`
- `artifacts/paper-summary-2602.11865.txt`
- `artifacts/paper-resources-2602.11865.txt`
- `artifacts/paper-similar-2602.11865.txt`

What mattered
- The paper is about delegation among increasingly capable AI agents.
- It feels more conceptual and protocol-oriented than the strongest systems papers, but it addresses a real coordination problem for agent networks.
- It also had meaningful visibility in the feed stage.

Decision
- Keep provisionally. It made the shortlist as a broader delegation/governance-flavored multi-agent paper, but remained the weakest of the final five.

## Near-Miss: `2601.01885`

Commands
```bash
alphaxiv paper show 2601.01885
alphaxiv paper abstract 2601.01885
alphaxiv paper summary 2601.01885
alphaxiv paper resources 2601.01885
alphaxiv paper similar 2601.01885 --limit 5
```

Raw output
- `artifacts/paper-show-2601.01885.txt`
- `artifacts/paper-abstract-2601.01885.txt`
- `artifacts/paper-summary-2601.01885.txt`
- `artifacts/paper-resources-2601.01885.txt`
- `artifacts/paper-similar-2601.01885.txt`

What mattered
- This was one of the most visible recent agentic papers, especially on the GitHub-ranked feed.
- The paper is clearly important for long-horizon agents, but it is not explicitly multi-agent.
- The resource metadata also looked suspicious enough to avoid over-weighting the GitHub score.

Decision
- Drop from the final five. Strong enabling infrastructure, but not direct enough for a specifically multi-agent shortlist.

## Near-Miss: `2602.23008`

Commands
```bash
alphaxiv paper show 2602.23008
alphaxiv paper abstract 2602.23008
alphaxiv paper summary 2602.23008
alphaxiv paper resources 2602.23008
alphaxiv paper similar 2602.23008 --limit 5
```

Raw output
- `artifacts/paper-show-2602.23008.txt`
- `artifacts/paper-abstract-2602.23008.txt`
- `artifacts/paper-summary-2602.23008.txt`
- `artifacts/paper-resources-2602.23008.txt`
- `artifacts/paper-similar-2602.23008.txt`

What mattered
- This looked like a strong RL-plus-memory agent paper with high GitHub visibility.
- It is important for agent training, but still not a direct multi-agent systems paper.

Decision
- Drop from the final five. Valuable adjacent work, but not specific enough to displace a direct multi-agent candidate.

## Near-Miss: `2601.14192`

Commands
```bash
alphaxiv paper show 2601.14192
alphaxiv paper abstract 2601.14192
alphaxiv paper summary 2601.14192
alphaxiv paper resources 2601.14192
alphaxiv paper similar 2601.14192 --limit 5
```

Raw output
- `artifacts/paper-show-2601.14192.txt`
- `artifacts/paper-abstract-2601.14192.txt`
- `artifacts/paper-summary-2601.14192.txt`
- `artifacts/paper-resources-2601.14192.txt`
- `artifacts/paper-similar-2601.14192.txt`

What mattered
- This is a useful survey on efficient agents rather than a central new multi-agent contribution.
- The summary confirmed it was broad and synthetic rather than a direct research advance in multi-agent systems.

Decision
- Drop from the final five. Useful background reading, but not a shortlist anchor.

## Inspection Outcome

Shortlist entering the assistant synthesis step:

- `2602.01848` ROMA
- `2601.04748` When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail
- `2603.00349` EmCoop
- `2602.15382` The Vision Wormhole
- `2602.11865` Intelligent AI Delegation

Why these five:

- one strong architecture paper
- one strong field-reframing paper
- one benchmark/infrastructure paper
- one novel communication-mechanism paper
- one delegation/coordination framing paper
