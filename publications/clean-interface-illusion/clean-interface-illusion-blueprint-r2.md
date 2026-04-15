# Hardened Blueprint

Live draft: `publications/clean-interface-illusion/clean-interface-illusion.md`
Candidate target: `publications/clean-interface-illusion/clean-interface-illusion-candidate-r2.md`
Packet manifest: `publications/clean-interface-illusion/clean-interface-illusion-essay-iteration-packet-r2.json`

## Promise

This pass will argue that benchmark realism has improved enough that the remaining public error is interpretive. Recent benchmarks already expose toolscale, policy pressure, realistic interfaces, and noisy interaction. The surviving claim is that point success rates still carry too much deployment-trust weight because reliability, failure localization, and repeated-run behavior remain more operationally important than the topline score alone.

## Spine

1. **Opening anomaly**
   Start with `tau-bench` repeated-run collapse so the calibration problem is visible before any benchmark taxonomy appears.
2. **Thesis lock**
   State that realism improved faster than interpretation.
3. **Reliability object**
   Use `Towards a Science of AI Agent Reliability` to define why capability scores leave operational meaning unresolved.
4. **Benchmark-to-benchmark turn**
   Read `WebSuite` and `WebForge` together to show that richer evaluation surfaces make flat scores less sufficient, not more authoritative.
5. **Toolscale and bounded usefulness**
   Use `LiveMCPBench`, with `REAL` and `TheAgentCompany` as support, to show how realism can improve while trust still stays narrow.
6. **Doctrine ending**
   Land on what a benchmark score is allowed to license.

## Paragraph burden

- **Opening anomaly**: make the first paragraph public and memorable enough that the essay does not begin as a survey.
- **Thesis lock**: name the exact interpretive error without collapsing back into "benchmarks are too clean."
- **Reliability object**: explain why average scores underdetermine deployment decisions.
- **Benchmark-to-benchmark turn**: produce one decisive comparison that changes how the middle is read.
- **Toolscale and bounded usefulness**: keep the essay honest about real progress without broadening the trust claim.
- **Doctrine ending**: give the reader a portable evaluation rule.

## Evidence burden

**Hero exhibit**

- `tau-bench`

**Body work**

- `Towards a Science of AI Agent Reliability`
- `WebSuite`
- `WebForge`
- `LiveMCPBench`

**Support**

- `REAL`
- `TheAgentCompany`
- `From Task Solving to Robust Real-World Adaptation in LLM Agents`

**References only**

- `WorkArena`
- `MCP-Bench`
- `MCPAgentBench`
- `ToolMisuseBench`
- `Establishing Best Practices for Building Rigorous Agentic Benchmarks`
- `EDDOps`

## Cut order

1. `TheAgentCompany` support detail
2. `REAL` support detail
3. adaptation-paper framing
4. any sentence that restates the thesis after the benchmark-to-benchmark turn

Do not cut the opening anomaly, the reliability paragraph, the `WebSuite`/`WebForge` comparison, or the doctrine ending.

## Failure triggers

- The draft still opens abstractly instead of through the `tau-bench` anomaly.
- `WebSuite` and `WebForge` appear as separate summaries rather than one comparative turn.
- `LiveMCPBench` turns into generic tool-use exposition.
- The ending states a doctrine without changing what downstream decisions the doctrine should govern.
- The draft still feels like a benchmark survey with a strong conclusion attached.
