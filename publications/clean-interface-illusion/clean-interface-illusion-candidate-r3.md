# The Clean Interface Illusion

A model that solves retail support tasks 61 percent of the time sounds close to useful. In `tau-bench`, that same result changes character once you ask what happens over repeated runs. The best model reaches 61 percent in retail and 35 percent in airline, then the retail pass-to-the-eighth falls below 25 percent. The model did not lose the task between the first try and the eighth. What changed was the interpretation. The topline score sounded like capability. The repeated-run result starts to sound like operations.

That is enough to retire the lazy version of the benchmark debate. Modern agent evaluation is not stuck in toy worlds. The stronger recent benchmarks already rebuild real sites, localize failures, inject noise, and force agents to search large toolspaces. The live mistake happens later, when that thicker evaluation surface gets flattened back into one readiness signal.

The adaptation literature is useful here because it names what gets buried by that flattening: underspecified rules, shifting environments, implicit objectives, and unreliable signals. The reliability literature explains why those variables matter. `Towards a Science of AI Agent Reliability` separates consistency, robustness, predictability, and safety because capability alone does not tell you whether behavior stays within useful bounds. Its central pattern is the one the field keeps trying to look past: accuracy rises while reliability trails behind. Better benchmark scores can therefore coexist with weak operational trust.

That gap changes how average performance should be read. An agent that fails on a stable subset of tasks is difficult in one way. An agent that alternates between competence and collapse across repeated runs or small perturbations is difficult in another. The topline score may look similar. The downstream decision should not. One case invites routing and scope control. The other contaminates planning because the boundary of failure does not stay put.

The clearest move in the recent benchmark literature appears when `WebSuite` and `WebForge` are read together instead of separately. `WebSuite` raises the engineering value of evaluation by making failures localizable. A flat web score tells you less than learning that the agent breaks on complex forms or ambiguous link selection. `WebForge` raises the realism of evaluation through richer environments, noise injection, and multidimensional difficulty control precisely because aggregate numbers hide capability profiles. Read together, these papers are not making leaderboards more impressive. They are making topline scores less sufficient.

`LiveMCPBench` pushes the same lesson into tool use. Inside a large MCP ecosystem, the hard part is not merely calling a known function. It is finding the right tool inside a noisy surface and composing several steps without losing the thread. That is closer to real delegation than the early function-calling demos, but it still does not settle the trust question. The score tells you something about retrieval and sequencing under that benchmark's conditions. It does not yet tell you how confidently to delegate the surrounding workflow.

The broader picture stays narrow even when the environment gets more realistic. `TheAgentCompany` reports 30.3 percent autonomous completion on consequential office tasks and 39.3 percent on a partial-credit metric. `REAL`, even on deterministic simulations of real sites, still tops out around 41.07 percent. Those results establish bounded usefulness. They do not justify broader delegation language. The field is getting better at measuring nontrivial work. That does not mean it has already measured trust.

The rule that follows is simple enough to use in practice. A benchmark score should license only the confidence its design actually measured. If the benchmark measures repeated-run stability, it supports claims about consistency. If it measures failure localization, it supports diagnosis. If it measures tool retrieval at scale, it supports claims about tool discovery and sequencing in a large toolspace. If it measures bounded task completion, it supports bounded task completion. Everything beyond that is narrative inflation.

This matters because deployment review is exactly where that inflation becomes expensive. A readiness discussion should ask which parts of the workflow can be delegated, which require routing or fallback, and which still need human checkpoints because reliability evidence is too thin. A leaderboard result cannot answer those questions by itself. The clean interface illusion survives when the field mistakes a measurement for a delegation policy.

## Limits

- This essay does not claim that modern agent benchmarks are still trapped in toy settings.
- This essay does not claim that aggregate scores are useless. It claims they are routinely overread.
- This essay does not claim that current agents lack bounded practical value.
- This essay does not attempt to deliver a full certification framework for deployment or procurement.

## References

- `2406.01623` WebSuite: Systematically Evaluating Why Web Agents Fail
- `2412.14161` TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks
- `2504.11543` REAL: Benchmarking Autonomous Agents on Deterministic Simulations of Real Websites
- `2508.01780` LiveMCPBench: Can Agents Navigate an Ocean of MCP Tools?
- `2602.02760` From Task Solving to Robust Real-World Adaptation in LLM Agents
- `2602.16666` Towards a Science of AI Agent Reliability
- `2604.10988` WebForge: Breaking the Realism-Reproducibility-Scalability Trilemma in Browser Agent Benchmark
- `2406.12045` τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains
