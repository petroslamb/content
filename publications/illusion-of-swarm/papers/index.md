# The Illusion Of The Swarm Paper Index

This index tracks the evidence surface for *The Illusion of the Swarm*.

`status.yaml` marks `paper_intake.done: true`, so this file should orient reviewers to the local evidence that already exists and to the paper gaps that remain unresolved. This pass does not change the published essay, download new papers, or mark any lifecycle stage done.

## Evidence Surface Notes

This package predates the current canonical `papers/markdown/` split. It uses mixed local evidence:

- source PDFs where available
- root-level `.txt` alphaXiv full-text captures
- root-level `.md` converted markdown for a small subset
- alphaXiv artifact records under `../artifacts/`

The `papers/markdown/` directory currently contains only its README. Do not treat that as missing conversion by itself; this package stored the older root-level captures and converted markdown beside the source PDFs.

## Locally Represented Papers

| arXiv ID | Paper | Local Evidence | Artifact Support | Role In Draft |
| :--- | :--- | :--- | :--- | :--- |
| `2601.04748` | When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail | `When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail.pdf`; `When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail.md`; `When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail.txt` | `../artifacts/paper-abstract-2601.04748.txt`; `../artifacts/paper-show-2601.04748.txt`; `../artifacts/paper-summary-2601.04748.txt` | Anchor for the single-agent-with-skills collapse and semantic-confusability limit. |
| `2602.01848` | ROMA: Recursive Open Meta-Agent Framework for Long-Horizon Multi-Agent Systems | `ROMA: Recursive Open Meta-Agent Framework for Long-Horizon Multi-Agent Systems.pdf`; `ROMA: Recursive Open Meta-Agent Framework for Long-Horizon Multi-Agent Systems.md`; `ROMA: Recursive Open Meta-Agent Framework for Long-Horizon Multi-Agent Systems.txt` | `../artifacts/paper-abstract-2602.01848.txt`; `../artifacts/paper-show-2602.01848.txt`; `../artifacts/paper-summary-2602.01848.txt` | Recursive decomposition and aggregation counterpoint to flat multi-agent committees. |
| `2601.14192` | Toward Efficient Agents: Memory, Tool learning, and Planning | `Toward Efficient Agents: Memory, Tool learning, and Planning.txt` | `../artifacts/paper-abstract-2601.14192.txt`; `../artifacts/paper-show-2601.14192.txt`; `../artifacts/paper-summary-2601.14192.txt` | Efficiency pressure for context, planning, memory, and tool use. |
| `2601.01885` | Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents | `Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents.txt` | `../artifacts/paper-abstract-2601.01885.txt`; `../artifacts/paper-show-2601.01885.txt`; `../artifacts/paper-summary-2601.01885.txt` | Unified memory policy and context-efficiency evidence. |
| `2602.11865` | Intelligent AI Delegation | `Intelligent AI Delegation.txt` | `../artifacts/paper-abstract-2602.11865.txt`; `../artifacts/paper-show-2602.11865.txt`; `../artifacts/paper-summary-2602.11865.txt` | Governance and delegation-boundary frame. |
| `2602.15382` | The Vision Wormhole: Latent-Space Communication in Heterogeneous Multi-Agent Systems | `The Vision Wormhole: Latent-Space Communication in Heterogeneous Multi-Agent Systems.txt` | `../artifacts/paper-abstract-2602.15382.txt`; `../artifacts/paper-show-2602.15382.txt`; `../artifacts/paper-summary-2602.15382.txt` | Higher-bandwidth heterogeneous-agent communication case. |
| `2602.23008` | Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization | `Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization.txt` | `../artifacts/paper-abstract-2602.23008.txt`; `../artifacts/paper-show-2602.23008.txt`; `../artifacts/paper-summary-2602.23008.txt` | Exploration scaffolding and memory-tip internalization analogy. |
| `2603.00349` | EmCoop: A Framework and Benchmark for Embodied Cooperation Among LLM Agents | `EmCoop: A Framework and Benchmark for Embodied Cooperation Among LLM Agents.txt` | `../artifacts/paper-abstract-2603.00349.txt`; `../artifacts/paper-show-2603.00349.txt`; `../artifacts/paper-summary-2603.00349.txt` | Embodied cooperation and process-level coordination measurement. |

## Cited In Draft But Not Yet Local Evidence

These arXiv IDs appear in the canonical draft but do not currently have local paper files or alphaXiv artifact records in this package. They are classified here as evidence gaps rather than silently treated as missing markdown. Do not expand this pass into new paper intake.

| arXiv ID | Paper | Current Status |
| :--- | :--- | :--- |
| `2512.08296` | Towards a Science of Scaling Agent Systems | Cited in the draft; no local paper file or alphaXiv artifact record found in this package. |
| `2602.19672` | SkillOrchestra: Learning to Route Agents via Skill Transfer | Cited in the draft; no local paper file or alphaXiv artifact record found in this package. |
| `2503.01935` | MultiAgentBench: Evaluating the Collaboration and Competition of LLM Agents | Cited in the draft; no local paper file or alphaXiv artifact record found in this package. |
| `2511.20639` | Latent Collaboration in Multi-Agent Systems | Cited in the draft; no local paper file or alphaXiv artifact record found in this package. |
| `2602.03955` | AgentArk: Distilling Multi-Agent Intelligence into a Single LLM Agent | Cited in the draft; no local paper file or alphaXiv artifact record found in this package. |

## Review Notes

The local evidence surface is sufficient to orient the article's core claims, but it is not a complete local mirror of every external citation. The unresolved entries above should remain gaps until a future paper-intake pass deliberately downloads, converts, or captures them.
