# Hardened Blueprint

Live draft: `publications/clean-interface-illusion/clean-interface-illusion.md`
Candidate target: `publications/clean-interface-illusion/clean-interface-illusion-candidate-r1.md`
Packet manifest: `publications/clean-interface-illusion/clean-interface-illusion-essay-iteration-packet-r1.json`

## Promise

This essay will argue that the field’s benchmark environments have improved faster than its benchmark interpretation. The paper set already defeats the lazy complaint that agent evaluations are still toy settings: recent benchmarks inject toolscale, privilege stress, policy complexity, recovery pressure, and realistic interface variance directly. The surviving claim is narrower and stronger. Point success rates remain badly calibrated to deployment trust because the most deployment-relevant properties are reliability properties: consistency across runs, recovery under perturbation, retrieval discipline at scale, and bounded failure under privilege-bearing tools.

## Spine

1. **Opening mismatch**
   The opening must show the difference between what a benchmark headline sounds like and what it actually licenses.
2. **Thesis lock**
   Stabilize the claim that the hard part is now calibration, not merely realism.
3. **The field already knows the easy critique**
   Use richer benchmark papers to show that serious builders already moved beyond toy tasks.
4. **Why success rates still mislead**
   Show that reliability and recovery properties remain unstable enough that pass rates overstate trust.
5. **Why toolscale and privilege raise the stakes**
   Show that the cost of overreading benchmark success increases as tools and permissions get more consequential.
6. **Counterpressure**
   Admit what the thesis does not claim and use challenge papers to prevent drift into a generic anti-benchmark essay.
7. **Doctrine ending**
   Land on a rule for what benchmark scores should and should not license.

## Paragraph burden

- **Opening mismatch**: earn the dispute before naming benchmark taxonomies.
- **Thesis lock**: state the exact claim in one portable sentence and distinguish it from "benchmarks are too clean."
- **The field already knows the easy critique**: prove that richer benchmark design already exists.
- **Why success rates still mislead**: connect benchmark realism to reliability gaps, not just lower absolute scores.
- **Why toolscale and privilege raise the stakes**: show why miscalibration becomes operationally dangerous.
- **Counterpressure**: keep the frame honest with explicit non-claims and objections.
- **Doctrine ending**: translate the argument into a reusable evaluation rule.

## Evidence burden

**Body work**

- `WebSuite`: failure attribution and action-level diagnosis
- `TheAgentCompany`: consequential-task completion limits
- `LiveMCPBench`: retrieval failures in large toolspaces
- `From Task Solving to Robust Real-World Adaptation in LLM Agents`: the clean-interface critique in explicit form
- `Towards a Science of AI Agent Reliability`: consistency, robustness, predictability, safety as reliability dimensions
- `WebForge`: benchmark realism has already advanced materially

**Supporting work**

- `WorkArena`
- `MCP-Bench`
- `MCPAgentBench`
- `ToolMisuseBench`
- `MCPTox`
- `GrantBox`
- `Establishing Best Practices for Building Rigorous Agentic Benchmarks`
- `EDDOps`

**Counterpressure / reference-only work**

- `tau-bench`
- `REAL`

**Synthesis claims rather than source-owned claims**

- The field improved benchmark design faster than benchmark interpretation.
- Reliability properties remain more deployment-relevant than single pass rates.
- Benchmark success should license only the operational confidence the benchmark explicitly measured.

## Cut order

1. EDDOps process detail
2. benchmark-checklist detail
3. extra side-by-side MCP benchmark comparison
4. browser environment construction detail

Do not cut the opening mismatch, thesis lock, reliability section, or final doctrine.

## Failure triggers

- The draft reduces to "benchmarks are unrealistic."
- The draft becomes a benchmark survey without a stable interpretive claim.
- The opening takes too long to produce a public dispute.
- The reliability argument lacks a clear rule connecting benchmark scores to operational trust.
- The counterpressure section is too weak to survive the `tau-bench` and `REAL` objections.

## Opening Lab

- `tau-bench` repeated-run collapse: the best model reaches 61% in retail and 35% in airline, while pass-to-the-eighth in retail falls below 25%. Best option for exposing the gap between "can do the task" and "can be trusted repeatedly."
- `Towards a Science of AI Agent Reliability`: accuracy rises while reliability trails. Best option for a doctrine-first opening, weaker as a public scene.
- `REAL`: deterministic replicas of real sites still top out at 41.07%. Best option for rebutting the old "toy benchmark" complaint, weaker for the calibration claim.

Current bet: start from `tau-bench` or do not claim flagship ignition.

## Object Decision

This remains one flagship thesis essay with an operator-doctrine ending. Do not split it yet. Split only if the second pass still cannot make the calibration claim feel primary over the benchmark-survey material.

## Body / Support / Footnote Ledger

- Hero exhibit: `tau-bench` or the reliability figure. Choose one.
- Body: `Towards a Science of AI Agent Reliability`, `WebSuite`, `LiveMCPBench`, `WebForge`.
- Support: `TheAgentCompany`, `From Task Solving to Robust Real-World Adaptation in LLM Agents`, `REAL`.
- Conditional support: one of `MCPTox` or `GrantBox` only if the privilege section survives.
- Footnote or reference-only: `WorkArena`, `MCP-Bench`, `MCPAgentBench`, `ToolMisuseBench`, `Establishing Best Practices for Building Rigorous Agentic Benchmarks`, `EDDOps`.

## Second-Pass Bet

The next pass should win by compression. If one vivid opening anomaly plus a narrowed body makes the doctrine feel inevitable, the essay remains on a north-star path. If that compression cannot be achieved without weakening the thesis, the object should be narrowed or split instead of rewritten again.
