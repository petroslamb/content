# Topic Discovery Packet

Run id: `phase-2-primary-topic-discovery-proof`
Workflow: `topic_discovery`
Package context: `literate-workflow-programming`

## Trigger

- Seed question: Can the Phase 2 `content-agent` proof run itself become the next publishable object in the literate-workflow-programming line?
- Trigger type: `archive_gap`
- Target ambition: `north_star_flagship`
- Relevant prior essays or packages:
  - `publications/literate-workflow-programming/`
  - `publications/literate-workflow-programming/specification-surface-source-of-truth/`
  - `reviewable-runs/examples/proofs/specification-surface-lifecycle-proof/`

## 01. Topic Vocabulary

Record the exact search commands and what they revealed.

| Query | Command | Useful Topics | Noisy Topics | Decision |
| :--- | :--- | :--- | :--- | :--- |
| `primary proof autonomous content agent publication workflow specification surface` | `.venv/bin/alphaxiv search topics 'primary proof autonomous content agent publication workflow specification surface'` | none returned | none returned | drop as too repo-local |
| `software engineering agents` | `.venv/bin/alphaxiv search topics 'software engineering agents'` | `agent-based-systems`, `cs.MA`, `cs.LG` | `reinforcement-learning` | keep only as broad agent backdrop |
| `coding agents` | `.venv/bin/alphaxiv search topics 'coding agents'` | `agent-based-systems`, `agents`, `multi-agent-learning` | `reinforcement-learning` | keep as broad recall surface |
| `autonomous agents software engineering workflow verification specification` | `.venv/bin/alphaxiv search papers 'autonomous agents software engineering workflow verification specification'` | specification-driven construction, agentic software engineering, event-sourced agent workflows, developer-intent coverage | social/legal/ethical verification | keep |
| `AI agents software engineering benchmark repository workflow` | `.venv/bin/alphaxiv search papers 'AI agents software engineering benchmark repository workflow'` | repository-level coding agents, long-horizon benchmarks, DevOps-cycle evaluation | generic teammate framing | keep |
| `specification driven software engineering agents benchmark` | `.venv/bin/alphaxiv search papers 'specification driven software engineering agents benchmark'` | SWE-AGI, Spec Kit Agents, TDAD, project-development benchmarks | microservice generation side routes | keep |
| `repository level coding agents long horizon software engineering` | `.venv/bin/alphaxiv search papers 'repository level coding agents long horizon software engineering'` | NL2Repo-Bench, SWE-EVO, SWE-Bench Pro, SWE-CI | navigation-only papers | keep as evaluation vocabulary |

Decision:

- Primary topic surfaces:
  - specification-driven software construction
  - context-grounded agentic workflows
  - repository-level and long-horizon coding-agent benchmarks
  - CI/evolution evaluation
  - event-sourced or append-only execution traces
  - repo-local governed runtime proof
- Broad recall surfaces:
  - `agentic-frameworks`
  - `agents`
  - `cs.SE`
  - `tool-use`
  - `model-observability`
- Dropped surfaces:
  - benchmark-score-only framing
  - pure event-sourcing architecture
  - generic "AI teammate" framing
- Why:
  - The publishable object is not "agents can code." It is that governed proof runs become the trust surface between declared specifications and autonomous action.

## 02. Feed Candidates

Use multiple imperfect ranking surfaces instead of trusting one list.

| Surface | Command | Candidates That Recurred | Noise / Caveat |
| :--- | :--- | :--- | :--- |
| specification-driven agent construction | `.venv/bin/alphaxiv search papers 'specification driven software engineering agents benchmark'` | `2602.09447`, `2604.05278`, `2603.08806` | benchmark success alone does not prove governance |
| repository-level coding agents | `.venv/bin/alphaxiv search papers 'AI agents software engineering benchmark repository workflow'` | `2508.18993`, `2509.16941`, `2601.20882`, `2602.01465` | many papers measure agents, not proof surfaces |
| long-horizon engineering | `.venv/bin/alphaxiv search papers 'repository level coding agents long horizon software engineering'` | `2512.12730`, `2512.18470`, `2509.16941`, `2603.03823` | some are benchmark-only |
| prior package harness index | `rg -n 'Spec Kit|SWE-AGI|AgentSPEX|Natural-Language Agent Harnesses|ContextCov' publications/literate-workflow-programming/harness_papers/index.md publications/literate-workflow-programming/papers/index.md` | `2603.25723`, `2604.13346`, `2604.05278`, `2603.00822`, `2602.09447` | prior curation is strong but does not replace fresh discovery |

Primary inspection pool:

- `2602.09447`: SWE-AGI. Direct anchor for specification-driven autonomous construction.
- `2604.05278`: Spec Kit Agents. Direct anchor for context-grounded workflow phases and validation hooks.
- `2509.16941`: SWE-Bench Pro. Pressure anchor against benchmark-success overclaiming.
- `2510.23761`: TDFlow. Workflow-design support for constrained sub-agents, tests, and bounded context.
- `2603.03823`: SWE-CI. Lifecycle support for regression and maintainability proof over time.
- `2602.23193`: ESAA. Architecture analogy for append-only events, deterministic orchestration, and replay verification.
- `2508.18993`: GitTaskBench. Practical pressure around environment provisioning and repository execution.
- `2603.25723`, `2604.13346`, `2603.00822`: existing direct donors in the package evidence tree.

Near-misses:

- `2512.12730`: long-horizon generation benchmark; less direct than SWE-AGI.
- `2603.24755`: degradation benchmark; useful later as a failure-mode support.
- `2602.01465`: multi-agent team framing; off-center for proof-run governance.
- `2604.10599`: broad survey route; defer unless the package needs literature review breadth.

## 03. Paper Inspection

### `2602.09447` SWE-AGI

Commands:

```bash
.venv/bin/alphaxiv paper show 2602.09447
.venv/bin/alphaxiv paper abstract 2602.09447
.venv/bin/alphaxiv paper summary 2602.09447
.venv/bin/alphaxiv paper similar 2602.09447 --limit 5
```

What mattered:

- Specification-driven software construction is increasingly feasible, but production-scale reliability remains unresolved.
- The summary identifies code understanding, architectural consistency, and debugging as scaling bottlenecks.
- The similar-paper surface connected the topic to SWE-bench, CodeAgent, SWE-Dev, NL2Repo-Bench, and SWE-Perf.

Essay-object role:

- `direct_anchor`

Decision:

- `keep`

### `2604.05278` Spec Kit Agents

Commands:

```bash
.venv/bin/alphaxiv paper show 2604.05278
.venv/bin/alphaxiv paper abstract 2604.05278
.venv/bin/alphaxiv paper summary 2604.05278
```

What mattered:

- The summary endpoint had no overview, so the pass used `show` and `abstract`.
- The paper frames spec-driven development as useful but context blind without repository-grounding hooks.
- Read-only probing hooks and validation hooks map cleanly to Phase 2 context admission and validation surfaces.

Essay-object role:

- `direct_anchor`

Decision:

- `keep`

### `2509.16941` SWE-Bench Pro

Commands:

```bash
.venv/bin/alphaxiv paper summary 2509.16941
```

What mattered:

- Long-horizon industrial software tasks remain hard for current agents.
- Human augmentations such as requirements and interface specifications materially improve outcomes.
- Failure modes include context overflow, endless file reading, and tool-use errors.

Essay-object role:

- `pressure_anchor`

Decision:

- `keep`

### `2510.23761` TDFlow

Commands:

```bash
.venv/bin/alphaxiv paper summary 2510.23761
```

What mattered:

- Repository-scale repair improves when work is decomposed into specialized agents with constrained toolsets and precise context.
- Valid tests shift the bottleneck toward reproduction-test generation.
- This supports declared step boundaries, validation, and gate stops.

Essay-object role:

- `adjacent`

Decision:

- `keep`

### `2603.03823` SWE-CI

Commands:

```bash
.venv/bin/alphaxiv paper summary 2603.03823
```

What mattered:

- Snapshot-style correctness misses regression and maintainability risk.
- CI/evolution evaluation is a better analogy for proof runs than one-off completion.

Essay-object role:

- `adjacent`

Decision:

- `keep`

### `2602.23193` ESAA

Commands:

```bash
.venv/bin/alphaxiv paper summary 2602.23193
.venv/bin/alphaxiv paper abstract 2602.23193
```

What mattered:

- The summary endpoint had no overview, so the pass used `abstract`.
- The paper separates agent intention from deterministic state mutation through structured events, validation, append-only logs, and replay verification.
- Useful analogy, but not a direct publication workflow proof.

Essay-object role:

- `enabling`

Decision:

- `provisional`

## 04. Assistant Synthesis

Use assistant only after retrieval and inspection.

Prompt:

```text
Not used.
```

What changed:

- Nothing. Assistant comparison was skipped because the workflow budget declares `external_mutations: 0`, and deterministic retrieval was sufficient for the handoff decision.

What did not change:

- The lead object remains a proof-runtime essay, not a benchmark survey and not a repeat of the published specification-surface essay.

## 05. Essay-Object Slate

| Candidate | One-Sentence Promise | Public Enemy / False Proxy | Evidence Already Present | Evidence Delta | Kill Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Proof Runs Are the Source Surface | For autonomous content work, the trustworthy artifact is the governed proof run: declared workflow, admitted context, bounded tools, gates, and evidence that make progress reviewable and resumable. | "The agent finished, therefore it worked." | Phase 2 `content-agent` runtime, root policy/profile/gate YAMLs, reviewable-run stores, SWE-AGI, Spec Kit Agents, SWE-Bench Pro, ESAA | Finish topic-discovery proof to `topic_viability`, then initialize only after approval | Kill if the runtime cannot materialize a durable gate from declared workflow contracts and proof artifacts |
| Specification Surfaces Need Runtime Teeth | Specification files become source only when they bind context admission, allowed tools, validation, and review gates. | "Better instructions are enough." | Existing Specification Surface essay, AgentSPEX, Natural-Language Agent Harnesses, ContextCov, Spec Kit Agents | Needs a sharper second object; risks repeating the published successor | Kill if it only restates the already published specification-surface thesis |
| Benchmarks Are Not Publication Proof | Coding-agent benchmark scores do not answer whether an autonomous publication run is governed, replayable, or safe to resume. | "Benchmark pass rate equals editorial reliability." | SWE-AGI, SWE-Bench Pro, SWE-CI, GitTaskBench | Needs stronger bridge from code benchmarks to content workflow proof | Kill if it becomes a benchmark survey instead of a proof-runtime essay |
| Event Logs Are the Agent Memory That Matters | Durable event logs are the control surface that turns probabilistic agent actions into replayable state. | "Longer context is memory." | ESAA, SWE-CI, local run records and gates | Needs more direct editorial and content-production anchors | Kill if it becomes architecture-only and loses publication relevance |

Scores are advisory.

| Candidate | Debate Gain | Aperture Gain | Doctrine Utility | Opening Power | Synthesis Headroom | Evidence Maturity | Read |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| Proof Runs Are the Source Surface | 5 | 5 | 5 | 4 | 5 | 4 | lead |
| Specification Surfaces Need Runtime Teeth | 3 | 3 | 5 | 3 | 3 | 5 | provisional |
| Benchmarks Are Not Publication Proof | 4 | 3 | 3 | 4 | 4 | 3 | provisional |
| Event Logs Are the Agent Memory That Matters | 3 | 4 | 4 | 3 | 4 | 2 | park |

## 06. Handoff Decision

Choose exactly one:

- `package_init_ready`
- `research_delta_needed`
- `post_ceiling_pivot`
- `intake_ready`
- `parked`
- `blocked`

Decision:

package_init_ready

Rationale:

The topic clears the package-init threshold because it is distinct from the published specification-surface leaf, has a live repo-local proof surface, has paper support across specification-driven construction and agent workflow validation, and has a concrete first gate: initialize only after `topic_viability` approval. The claim must remain bounded: this proves a governed local runtime path to gate, not autonomous external publication reliability.

Carry-forward package idea if ready:

- Proposed slug: proof-runs-as-source-surface
- One-sentence promise: For autonomous content work, the trustworthy artifact is the governed proof run: declared workflow, admitted context, bounded tools, gates, and evidence that make progress reviewable and resumable.
- Initial paper shortlist:
  - `2602.09447` SWE-AGI
  - `2604.05278` Spec Kit Agents
  - `2509.16941` SWE-Bench Pro
  - `2510.23761` TDFlow
  - `2603.03823` SWE-CI
  - `2602.23193` ESAA
  - `2603.25723` Natural-Language Agent Harnesses
  - `2604.13346` AgentSPEX
  - `2603.00822` ContextCov
- Near-misses and blocked framings:
  - benchmark-score-only autonomy claims
  - "agents can publish themselves" claims
  - event-sourcing-only architecture essay
  - repeat of `The Specification Surface Is the New Source of Truth`
First research question: What evidence must a governed local runtime emit before a human should trust an agent to initialize, mutate, resume, or publish a content package?
Expected evidence surface: `workflow.yaml`, package `status.yaml`, `harness_policy.yaml`, `gate_contracts.yaml`, `pipeline_profiles.yaml`, resolved-run YAML, run-record YAML, review-gate YAML, gate-check log, paper shortlist, and an explicit contradiction boundary against full autonomous publication claims.

## Negative Evidence

Record failed searches and demotions.

- Topic search for the repo-local trigger returned no useful topic slugs.
- `2604.05278` and `2602.23193` did not have alphaXiv overview summaries available; deterministic inspection fell back to `show` and `abstract`.
- Benchmark papers alone were demoted because benchmark performance does not prove reviewable publication governance.
- Multi-agent teamwork papers were demoted because the current proof object is about governed runtime evidence, not orchestration breadth.

## Next Action

One concrete next action:

- Stop at the `topic_viability` lifecycle gate. If approved, initialize `publications/proof-runs-as-source-surface/` from this packet and keep the first proof claim bounded to governed local runtime evidence, not external publication reliability.
