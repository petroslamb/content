# Paper Index

## Admitted Body Papers

### WebSuite: Systematically Evaluating Why Web Agents Fail

- arXiv: `2406.01623`
- PDF: [`2406.01623_websuite.pdf`](2406.01623_websuite.pdf)
- Markdown: [`markdown/2406.01623_websuite.md`](markdown/2406.01623_websuite.md)
- Relevance: Failure-attribution anchor. This is the cleanest source for showing that benchmark value increases when failures become diagnosable rather than merely countable.

### TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks

- arXiv: `2412.14161`
- PDF: [`2412.14161_theagentcompany.pdf`](2412.14161_theagentcompany.pdf)
- Markdown: [`markdown/2412.14161_theagentcompany.md`](markdown/2412.14161_theagentcompany.md)
- Relevance: Consequential-task anchor. This is the core source for showing how low autonomous completion remains once the workflow becomes long-horizon and professionally consequential.

### LiveMCPBench: Can Agents Navigate an Ocean of MCP Tools?

- arXiv: `2508.01780`
- PDF: [`2508.01780_livemcpbench.pdf`](2508.01780_livemcpbench.pdf)
- Markdown: [`markdown/2508.01780_livemcpbench.md`](markdown/2508.01780_livemcpbench.md)
- Relevance: Toolscale and retrieval anchor. This is the clearest body source for the claim that large toolspaces expose retrieval and composition bottlenecks directly.

### From Task Solving to Robust Real-World Adaptation in LLM Agents

- arXiv: `2602.02760`
- PDF: [`2602.02760_robust_real_world_adaptation.pdf`](2602.02760_robust_real_world_adaptation.pdf)
- Markdown: [`markdown/2602.02760_robust_real_world_adaptation.md`](markdown/2602.02760_robust_real_world_adaptation.md)
- Relevance: Clean-interface critique anchor. This paper most directly states the gap between nominal task solving and deployment-like robustness.

### Towards a Science of AI Agent Reliability

- arXiv: `2602.16666`
- PDF: [`2602.16666_agent_reliability_science.pdf`](2602.16666_agent_reliability_science.pdf)
- Markdown: [`markdown/2602.16666_agent_reliability_science.md`](markdown/2602.16666_agent_reliability_science.md)
- Relevance: Reliability-measurement anchor. This is the core source for consistency, robustness, predictability, and safety as dimensions that outrun single success metrics.
- Conversion note: The markdown conversion is usable but noisy around tables and figure-heavy sections. Verify quotations against the PDF.

### WebForge: Breaking the Realism-Reproducibility-Scalability Trilemma in Browser Agent Benchmark

- arXiv: `2604.10988`
- PDF: [`2604.10988_webforge.pdf`](2604.10988_webforge.pdf)
- Markdown: [`markdown/2604.10988_webforge.md`](markdown/2604.10988_webforge.md)
- Relevance: Counterpressure anchor. This paper prevents the essay from collapsing into the easy complaint that benchmark builders are still stuck in toy environments.

## Intake Priority

The next paper-intake pass should prioritize the supporting set:

1. `WorkArena`
2. `MCP-Bench`
3. `MCPAgentBench`
4. `ToolMisuseBench`
5. `MCPTox`
6. `GrantBox`
7. `Establishing Best Practices for Building Rigorous Agentic Benchmarks`
8. `EDDOps`

## Supporting Queue

Admit these after the body set if they materially tighten the live claim or the counterpressure section:

- `WorkArena`
- `MCP-Bench`
- `MCPAgentBench`
- `ToolMisuseBench`
- `MCPTox`
- `GrantBox`
- `Establishing Best Practices for Building Rigorous Agentic Benchmarks`
- `EDDOps`

## Counterpressure Queue

These papers matter mainly to keep the essay honest and to stop the frame from drifting back into the easy critique:

- `tau-bench`
- `REAL`

## Working Rule

Do not treat alphaXiv summaries as the permanent evidence surface. Once a paper is selected for body work, promote it into `papers/` and `papers/markdown/` through the tracked paper-intake workflow.
