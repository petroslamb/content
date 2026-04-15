# Blueprint

## Active Thesis

Current agent benchmarks do not fail mainly because they are too clean. They fail when point success rates, even on increasingly realistic benchmarks, are treated as proxies for deployment trust despite high variance, brittle recovery, and weak reliability under perturbation.

## Why This Frame Survives

The paper set already resists the laziest version of the argument. `REAL`, `tau-bench`, `LiveMCPBench`, `MCPAgentBench`, `ToolMisuseBench`, `MCPTox`, and `GrantBox` all inject realism, noise, toolscale, or security stress directly. The surviving claim is therefore not that benchmarks are naive. It is that benchmark interpretation is still naive: single pass-rate readings are routinely over-read as readiness signals even when the benchmark itself reveals instability, recovery weakness, or reliability drift.

## Essay Promise

Show that the frontier moved from clean synthetic tasks to richer benchmark design, but the public reading of benchmark scores did not move with it. The piece should leave the reader with a stricter doctrine: benchmark success licenses only the specific operational confidence the benchmark actually measured, not a general claim of deployment readiness.

## Dominant Essay Mode

- Primary mode: flagship contrarian thesis essay
- Secondary mode: operator doctrine

## Pull Sheet

### Pull 1

- Essay: `The Transformer Attractor`
- Pull strength: high
- What to borrow: conflict-forward opening, thesis compression, hard landing
- What not to borrow: overconfident compression that outruns the evidence base

### Pull 2

- Essay: `The Binding Gap`
- Pull strength: high
- What to borrow: border-setting, exact definitions, disciplined non-claims
- What not to borrow: taxonomy-heavy pacing that drains public energy

### Pull 3

- Essay: `The Illusion of the Swarm`
- Pull strength: high
- What to borrow: middle-architecture synthesis, builder-first consequences, counterpressure handling
- What not to borrow: too much caveat density in the opening movement

### Resist 1

- Essay: `What Actually Works`
- Why resist: front matter and long survey scale would soften the ignition

### Resist 2

- Essay: `Operating Agents Bonus: Workflow Optimization and Evaluation`
- Why resist: too much operator explanation would narrow the public object

## Title Family

- The Clean Interface Illusion
- What Agent Leaderboards Still Don’t Measure
- Why Agent Success Rates Misprice Deployment Readiness

## Section Spine

### Opening

Open on the mismatch between what a benchmark headline sounds like and what it actually licenses. The opening needs one vivid example of a pass rate or capability claim that sounds like readiness until reliability and perturbation are introduced.

### Thesis Lock

Stabilize the claim early: the problem is no longer that agent benchmarks are unreal. The problem is that benchmark success is still being interpreted as a broader trust signal than the benchmark warrants.

### Development I: The Field Already Knows The Easy Critique

Use `WebForge`, `REAL`, `tau-bench`, `LiveMCPBench`, and `ToolMisuseBench` to show that the benchmark builders themselves already moved beyond toy settings. This section exists to disarm the obvious objection that the essay is just complaining about synthetic tasks.

### Development II: Why Better Benchmarks Still Leave A Reliability Gap

Use `WebSuite`, `TheAgentCompany`, `Robust Real-World Adaptation`, and `Towards a Science of AI Agent Reliability` to show the deeper issue: consistency, recovery, robustness, and predictability remain weak enough that point success rates compress away the most deployment-relevant behavior.

### Development III: Toolscale And Privilege Make Misreading More Dangerous

Use `MCP-Bench`, `MCPAgentBench`, `LiveMCPBench`, `MCPTox`, and `GrantBox` to show that large toolspaces and privilege-bearing tools raise the cost of over-reading benchmark success. Here the argument shifts from methodological sloppiness to operational consequence.

### Borders / Counterpressure

Admit three things clearly:

- the best benchmark builders already understand many of these problems
- aggregate scores still have value inside a fuller measurement stack
- this essay is about calibration and interpretation, not a blanket dismissal of benchmark work

Use `Establishing Best Practices for Building Rigorous Agentic Benchmarks` and `EDDOps` here.

### Ending

Land on a doctrine, not a slogan. A benchmark score should only license the operational confidence its design actually measures. Everything beyond that is narrative inflation.

## Evidence Ledger

### Body Papers

- `2406.01623` `WebSuite`
  Why it matters: failure attribution and action-level diagnosis
- `2412.14161` `TheAgentCompany`
  Why it matters: consequential task performance remains low enough to resist hype
- `2508.01780` `LiveMCPBench`
  Why it matters: retrieval-scale and multi-tool composition failures under large toolspaces
- `2602.02760` `From Task Solving to Robust Real-World Adaptation in LLM Agents`
  Why it matters: the clean-interface assumption is named and challenged directly
- `2602.16666` `Towards a Science of AI Agent Reliability`
  Why it matters: reliability dimensions outrun single success metrics
- `2604.10988` `WebForge`
  Why it matters: the field already knows how to build richer evaluation environments

### Supporting Papers

- `2403.07718` `WorkArena`
- `2508.20453` `MCP-Bench`
- `2512.24565` `MCPAgentBench`
- `2508.14925` `MCPTox`
- `2603.28166` `GrantBox`
- `2604.01508` `ToolMisuseBench`
- `2507.02825` `Establishing Best Practices for Building Rigorous Agentic Benchmarks`
- `2411.13768` `EDDOps`

### Counterpressure / Footnote Papers

- `2406.12045` `tau-bench`
- `2504.11543` `REAL`

## Non-Claims

- The essay does not claim that modern benchmark builders are still trapped in toy settings.
- The essay does not claim that higher capability scores tell us nothing useful.
- The essay does not claim that deployment failure comes only from noisy interfaces or adversarial conditions.

## Cut Order

If the draft bloats, cut in this order:

1. EDDOps process detail
2. best-practices checklist detail
3. extra MCP benchmark comparison detail
4. long exposition on browser-environment construction

Do not cut the opening mismatch, the thesis lock, the reliability section, or the landing doctrine.

## Failure Triggers

- If the draft slides back into "benchmarks are unrealistic" as the main claim, the frame failed.
- If the draft becomes a survey of benchmark papers without a stable interpretive argument, the frame failed.
- If the draft cannot explain what operational trust means more precisely than "better deployment," the frame failed.
- If the opening requires too much benchmark taxonomy before the dispute becomes legible, the frame failed.
