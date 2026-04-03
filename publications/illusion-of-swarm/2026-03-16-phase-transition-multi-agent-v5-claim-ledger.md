# Claim Ledger for `2026-03-16-phase-transition-multi-agent-v5`

This ledger records the core claims used in the rewrite, the paper support behind them, and whether each claim was kept, softened, or cut.

| Claim | Scope | Anchor source | Corroborating source(s) | Caveat | Decision |
| --- | --- | --- | --- | --- | --- |
| Many same-model production multi-agent systems are workarounds for routing, state, and coordination limits rather than default architectural necessities. | Synthesis for same-model, tool-using systems | `2601.04748` | `2601.14192`, `2512.08296` | Not universal; benchmark and systems evidence only | Keep |
| The tested models in `2601.04748` show a collapse zone around 80-90 skills rather than graceful degradation. | Limited to the evaluated model/task setups | `2601.04748` | none | Do not universalize as a fixed law for all models | Keep, scoped |
| "An agent is a namespace" is the right practical interpretation for many orchestration boundaries. | Author synthesis | `2601.04748` | `2602.01848`, `2602.19672` | Interpretation, not a direct paper claim | Keep as interpretation |
| Recursive decomposition is a better answer than flat persona committees once routing overload appears. | Long-horizon orchestration on tested benchmarks | `2602.01848` | `2601.04748`, `2602.19672` | Not a universal best architecture claim | Keep |
| Multi-agent structure is genuinely load-bearing for heterogeneity, trust boundaries, embodied coordination, and some search/exploration workflows. | Conditional design cases | `2512.08296` | `2602.11865`, `2603.00349`, `2602.15382`, `2602.23008` | Mixed evidence types; partly empirical, partly conceptual | Keep |
| Text is increasingly the bottleneck in some multi-agent settings. | Communication design on selected benchmarks/setups | `2602.15382` | `2511.20639`, `2603.00349` | Stronger than "text is costly," weaker than "text is obsolete" | Keep, softened |
| English is about to die as the inter-agent protocol. | Universal future claim | none | `2602.15382`, `2511.20639` | Current evidence does not support this level of certainty | Cut |
| Evaluation and measurement are becoming their own layer in multi-agent research. | Benchmark and observability trend | `2603.00349` | `2503.01935` | Evaluation infrastructure is not deployment validation | Keep |
| External scaffolding can sometimes be internalized into policy or weights. | Training/adaptation pattern | `2602.23008` | `2601.01885`, `2602.03955` | Emerging pattern only; not universal | Keep, softened |
| A swarm can be a training rig rather than the final deployed architecture. | Engineering workflow pattern | `2602.23008` | `2602.03955`, `2601.01885` | Keep conditional on whether boundaries remain load-bearing | Keep |
| Multi-agent intelligence can be fully transferred into one model without major loss. | Universal transfer claim | none | `2602.03955`, `2602.23008` | Evidence is promising but too narrow for full-transfer language | Cut/soften |
| `Intelligent AI Delegation` empirically proves better agent networks. | Performance claim | none | `2602.11865` | Paper is better treated as conceptual framing than decisive empirical support | Cut as empirical support |
