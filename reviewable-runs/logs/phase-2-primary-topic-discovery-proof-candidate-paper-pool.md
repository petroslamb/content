# Ranked Candidate Paper Pool

Run id: `phase-2-primary-topic-discovery-proof`
Workflow: `topic_discovery`

## Feed Candidates

| Surface | Command | Candidates That Recurred | Noise / Caveat |
| :--- | :--- | :--- | :--- |
| specification-driven agent construction | `.venv/bin/alphaxiv search papers 'specification driven software engineering agents benchmark'` | `2602.09447`, `2604.05278`, `2603.08806` | includes benchmark papers that do not by themselves support a governance thesis |
| repository-level coding agents | `.venv/bin/alphaxiv search papers 'AI agents software engineering benchmark repository workflow'` | `2508.18993`, `2509.16941`, `2601.20882`, `2602.01465` | many papers evaluate code agents, not proof surfaces |
| long-horizon engineering | `.venv/bin/alphaxiv search papers 'repository level coding agents long horizon software engineering'` | `2512.12730`, `2512.18470`, `2509.16941`, `2603.03823` | some are benchmark-only and lack workflow-control detail |
| prior package harness index | `rg -n 'Spec Kit|SWE-AGI|AgentSPEX|Natural-Language Agent Harnesses|ContextCov' publications/literate-workflow-programming/harness_papers/index.md publications/literate-workflow-programming/papers/index.md` | `2603.25723`, `2604.13346`, `2604.05278`, `2603.00822`, `2602.09447` | prior curation is strong but must not replace fresh topic discovery |

## Primary Inspection Pool

- `2602.09447`, SWE-AGI: direct anchor for end-to-end, specification-driven autonomous construction. The abstract frames production-scale construction from authoritative standards as still open, and the summary identifies code understanding as the scaling bottleneck.
- `2604.05278`, Spec Kit Agents: direct anchor for context-grounded specification phases and validation hooks in agentic workflows. The abstract is almost exactly on the Phase 2 seam: read-only probing hooks plus validation hooks around Specify, Plan, Tasks, and Implement.
- `2509.16941`, SWE-Bench Pro: benchmark pressure. It says long-horizon industrial tasks remain hard, and human augmentations such as requirements and interface specifications materially affect outcomes.
- `2510.23761`, TDFlow: workflow pressure. It decomposes repository-scale repair into constrained sub-agents and shows that valid tests shift the bottleneck toward reproduction-test generation.
- `2603.03823`, SWE-CI: lifecycle pressure. It evaluates agents through CI/evolution rather than snapshot success and makes regression control a first-class concern.
- `2602.23193`, ESAA: architecture-adjacent support for append-only event logs, validated structured intentions, deterministic orchestrators, and replay verification.
- `2508.18993`, GitTaskBench: practical autonomy pressure, especially environment provisioning and execution failures in repository-centric tasks.
- `2603.25723`, Natural-Language Agent Harnesses: existing direct donor in this package for natural-language harness logic, contracts, roles, stage structure, and durable artifacts.
- `2604.13346`, AgentSPEX: existing direct donor for explicit workflow specification as governed source with runtime support.
- `2603.00822`, ContextCov: existing direct donor for deriving executable constraints from agent instruction files.

## Paper Inspection Notes

### `2602.09447` SWE-AGI

Commands:

```bash
.venv/bin/alphaxiv paper show 2602.09447
.venv/bin/alphaxiv paper abstract 2602.09447
.venv/bin/alphaxiv paper summary 2602.09447
.venv/bin/alphaxiv paper similar 2602.09447 --limit 5
```

What mattered:

- The task design is specification-first and cold-start: agents must implement systems from standards and fixed API scaffolds.
- The paper separates short benchmark success from production-scale reliability.
- The summary reports that code reading and understanding dominate logged actions as complexity rises.

Essay-object role:

- `direct_anchor` for the claim that specification surfaces are necessary but not sufficient; they must be paired with governed proof.

Decision:

- keep.

### `2604.05278` Spec Kit Agents

Commands:

```bash
.venv/bin/alphaxiv paper show 2604.05278
.venv/bin/alphaxiv paper abstract 2604.05278
.venv/bin/alphaxiv paper summary 2604.05278
```

What mattered:

- The summary endpoint had no overview, so the pass fell back to `show` and `abstract`.
- The abstract describes context-grounding hooks and validation hooks around phase-level agent workflow stages.
- It directly supports the repo's separation between declared workflow contracts, read-only context admission, and validation evidence.

Essay-object role:

- `direct_anchor` for Phase 2 workflow design.

Decision:

- keep.

### `2509.16941` SWE-Bench Pro

Command:

```bash
.venv/bin/alphaxiv paper summary 2509.16941
```

What mattered:

- Long-horizon task performance remains materially below autonomous reliability.
- Human-provided requirements and interface specifications materially improve outcomes.
- Failure modes include context overflow, endless file reading, and tool-use errors.

Essay-object role:

- `pressure_anchor` against overclaiming autonomy from one successful run.

Decision:

- keep.

### `2510.23761` TDFlow

Command:

```bash
.venv/bin/alphaxiv paper summary 2510.23761
```

What mattered:

- Specialized sub-agents with constrained toolsets and precise context improve repository-scale repair.
- The fully autonomous bottleneck moves to reproduction-test generation.
- The workflow frame supports declared step boundaries and validation before mutation.

Essay-object role:

- `adjacent` workflow-design support.

Decision:

- keep.

### `2603.03823` SWE-CI

Command:

```bash
.venv/bin/alphaxiv paper summary 2603.03823
```

What mattered:

- Snapshot correctness is inadequate for codebase maintenance.
- Regression control and long-term maintainability require CI/evolution evaluation.
- This strengthens the argument that a proof run must record more than final output.

Essay-object role:

- `adjacent` lifecycle-proof support.

Decision:

- keep.

### `2602.23193` ESAA

Commands:

```bash
.venv/bin/alphaxiv paper summary 2602.23193
.venv/bin/alphaxiv paper abstract 2602.23193
```

What mattered:

- The summary endpoint had no overview, so the pass fell back to `abstract`.
- The paper separates cognitive intention from deterministic state mutation through structured intentions, validation, append-only logs, and replay verification.
- This is conceptually close to resolved-run plus run-record evidence, but it is not itself an editorial publication workflow.

Essay-object role:

- `enabling` architecture analogy.

Decision:

- provisional.

### `2508.18993` GitTaskBench

Command:

```bash
.venv/bin/alphaxiv paper summary 2508.18993
```

What mattered:

- Repository-centric tasks expose environment provisioning and execution as major bottlenecks.
- This supports retaining sandbox, tool, and evidence boundaries rather than treating agent action as self-validating.

Essay-object role:

- `adjacent` practical autonomy pressure.

Decision:

- keep as support, not as lead.

## Near-Misses

- `2512.12730` NL2Repo-Bench: useful long-horizon generation benchmark, but less direct than SWE-AGI and SWE-Bench Pro for specification/proof framing.
- `2603.24755` SlopCodeBench: useful degradation frame, but currently more of a failure-taxonomy support paper.
- `2602.01465` Agyn: potentially useful multi-agent team paper, but the proof-run object is not primarily about multi-agent orchestration.
- `2604.10599` Rethinking Software Engineering for Agentic AI Systems: broad survey route; useful later, not needed for topic gate.
