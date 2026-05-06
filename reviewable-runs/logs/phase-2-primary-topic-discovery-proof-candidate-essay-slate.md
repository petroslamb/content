# Candidate Essay Slate

Run id: `phase-2-primary-topic-discovery-proof`
Workflow: `topic_discovery`
Target ambition: `north_star_flagship`

## Candidate Objects

| Candidate | One-Sentence Promise | Public Enemy / False Proxy | Evidence Already Present | Evidence Delta | Kill Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Proof Runs Are the Source Surface | For autonomous content work, the trustworthy artifact is the governed proof run: declared workflow, admitted context, bounded tools, gates, and evidence that make progress reviewable and resumable. | "The agent finished, therefore it worked." | Phase 2 `content-agent` runtime, `workflow.yaml`, `status.yaml`, `harness_policy.yaml`, `gate_contracts.yaml`, `pipeline_profiles.yaml`, reviewable-run stores, SWE-AGI, Spec Kit Agents, SWE-Bench Pro, ESAA | Finish topic-discovery proof to `topic_viability`, then package-init only after approval | Kill if the runtime cannot materialize a durable gate from declared workflow contracts and proof artifacts |
| Specification Surfaces Need Runtime Teeth | Specification files become source only when they bind context admission, allowed tools, validation, and review gates. | "Better instructions are enough." | Existing Specification Surface essay, AgentSPEX, Natural-Language Agent Harnesses, ContextCov, Spec Kit Agents | Needs a sharper second object; risks repeating the published successor | Kill if it only restates the already published specification-surface thesis |
| Benchmarks Are Not Publication Proof | Coding-agent benchmark scores do not answer whether an autonomous publication run is governed, replayable, or safe to resume. | "Benchmark pass rate equals editorial reliability." | SWE-AGI, SWE-Bench Pro, SWE-CI, GitTaskBench | Needs stronger bridge from code benchmarks to content workflow proof | Kill if it becomes a benchmark survey instead of a proof-runtime essay |
| Event Logs Are the Agent Memory That Matters | Durable event logs are the control surface that turns probabilistic agent actions into replayable state. | "Longer context is memory." | ESAA, SWE-CI, local run records and gates | Needs more direct editorial and content-production anchors | Kill if it becomes architecture-only and loses publication relevance |

## Scores

| Candidate | Debate Gain | Aperture Gain | Doctrine Utility | Opening Power | Synthesis Headroom | Evidence Maturity | Read |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| Proof Runs Are the Source Surface | 5 | 5 | 5 | 4 | 5 | 4 | lead |
| Specification Surfaces Need Runtime Teeth | 3 | 3 | 5 | 3 | 3 | 5 | provisional |
| Benchmarks Are Not Publication Proof | 4 | 3 | 3 | 4 | 4 | 3 | provisional |
| Event Logs Are the Agent Memory That Matters | 3 | 4 | 4 | 3 | 4 | 2 | park |

## Decision

Lead object: `Proof Runs Are the Source Surface`.

Reason:

- It is not a repeat of the already published `Specification Surface Is the New Source of Truth` leaf.
- It is a stronger next article object because it moves from "what is source truth?" to "what proves governed runtime action happened?"
- The repo can produce unusually direct local evidence: a live Phase 2 run that starts at topic discovery, admits context, writes declared outputs, and stops at a first-class lifecycle gate.
- The paper pool supports the stakes without forcing the article to become a benchmark survey.

Blocked framings:

- "Agents can now autonomously publish." This overclaims; the proof is governed local runtime to gate, not external publication reliability.
- "Workflow YAML is the whole system." This collapses package state, policy, gates, profiles, and evidence into one file.
- "A successful run proves full autonomy." The proof run only supports the governed-runtime baseline and must preserve human approval gates.
