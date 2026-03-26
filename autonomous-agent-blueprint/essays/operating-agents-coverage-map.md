# Operating Agents Coverage Map

This note is the breadth layer behind the `v5` essay package. The public essays are intentionally sharper and narrower than both the distilled chapter guide and the full survey. This file shows what each post covers, what source terrain sits behind it, what it leaves out on purpose, and where an interested reader should go next.

**Reading order:** Launch Note, Action, Memory, Reasoning, Multi-Agent, Safety, then Optimization.

## How To Use This Layer

- Essays: the public narrative layer built for Substack readability and strong thesis shape.
- Companions: substantial breadth essays that reconnect each post to the distilled guide and the original survey, explain what the public essay compressed, and teach the surrounding terrain rather than just pointing at references.
- Blueprints: the operator layer for architecture choices, build order, and anti-patterns.
- Paper notes: the source-note layer for named methods and individual literature artifacts.

Only Parts I through VI have dedicated companions. The launch note routes to this map only.

## Series Map

| Piece | Current thesis | Distilled chapter-guide sections | Original survey sections | What the essay emphasizes | What it leaves out on purpose | Where to go next |
|---|---|---|---|---|---|---|
| [Launch Note](./launch-note/00-launch-note-v5.md) | Start from operating layers, not model shopping | [Practical chapters guide](../reference/chapters-guide.md) reading order and [practical distillation](../reference/practical-distillation.md) | Chapters `2`, `3`, `8`, `9`, `11`, `14`, `17` to `19` as the practical stack | Build order, target reader, series logic | chapter-specific nuance, source breadth, alternate chapter ordering | [Practical chapters guide](../reference/chapters-guide.md)<br>[Practical distillation](../reference/practical-distillation.md) |
| [Action](./action/01-action-tool-use-v5.md) | Agency begins when language becomes accountable state change | Guide Chapter `8`, especially `8.3.1`, `8.3.2`, `8.3.3` | Survey Chapter `8`, especially `8.1`, `8.2`, `8.3.1`, `8.3.2`, `8.3.3`, `8.4` | digital action surfaces, observation contracts, action as uncertainty reduction | physical action, broader action learning, perception-action coupling | [Action companion](./action/companion.md)<br>[Action blueprint](../core/practical-chapter-blueprints/03-action-tool-use-blueprint.md) |
| [Memory](./memory/03-memory-v5.md) | Memory is governance over time, not storage | Guide Chapter `3`, especially `3.3.2`, `3.3.3`, `3.4`, `3.4.3`, `3.4.4`, `3.4.6` | Survey Chapter `3`, especially `3.2`, `3.3.2`, `3.3.3`, `3.4.1` to `3.4.6` | working, semantic, episodic, procedural split, lifecycle, forgetting | human-memory analogy, neural memory networks, broader biological framing | [Memory companion](./memory/companion.md)<br>[Memory blueprint](../core/practical-chapter-blueprints/01-memory-blueprint.md) |
| [Reasoning](./reasoning/02-reasoning-planning-v5.md) | Most production reasoning failures are scaffold failures | Guide Chapter `2`, especially `2.2.2`, `2.2.2.2`, `2.2.3`, `2.2.4` | Survey Chapter `2`, especially `2.2.1`, `2.2.2`, `2.2.3`, `2.2.4` | decomposition, ReAct, verification, late search | broader reasoning taxonomy, self-refinement breadth, formal planning handoff | [Reasoning companion](./reasoning/companion.md)<br>[Reasoning blueprint](../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md) |
| [Multi-Agent](./multi-agent/04-multi-agent-v5.md) | Multi-agent systems solve three different problems | Guide Chapter `14`, especially `14.1.2`, `14.2.1`, `14.3.4`, `14.4`, `14.5`, `14.6.1`, `14.6.3` | Survey Chapters `13` to `16`, especially `13.1.2`, `14.2`, `14.5`, `14.6`, `15`, `16` | role separation, critique, artifact handoffs, human review | broader topology catalog, protocol layers, collective-intelligence framing, evaluation breadth | [Multi-agent companion](./multi-agent/companion.md)<br>[Multi-agent blueprint](../core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md) |
| [Safety](./safety/05-safety-v5.md) | Safety is interface architecture | Guide safety chapters, especially `17.1.2`, `17.1.3`, `18.2.1`, `18.2.2`, `19.1`, `19.2`, `19.3` | Survey Chapters `17`, `18`, `19`, and adjacent Chapter `20` context | indirect injection, retrieval poisoning, tool scope, handoff contamination, approval | broader hallucination framing, perception threats, safety-scaling context, wider non-brain-module material | [Safety companion](./safety/companion.md)<br>[Safety blueprint](../core/practical-chapter-blueprints/06-safety-blueprint.md) |
| [Optimization Bonus](./optimization/06-optimization-v5.md) | Most agent optimization is fake without measurement | Guide Chapters `9` and `11`, especially `9.2`, `9.2.3`, `9.3`, `9.4`, `9.4.3`, `11.1` | Survey Chapters `9`, `10`, `11`, especially `9.2`, `9.3`, `9.4`, `9.5`, `10.1` to `10.4`, `11.1` | evaluation first, contracts before cleverness, bounded self-improvement | wider optimization taxonomy, Chapter `10` iteration layer, more neutral treatment of prompt, tool, and workflow levers | [Optimization companion](./optimization/companion.md)<br>[Optimization blueprint](../core/practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md) |

## Reading Rule

Use the essay first, the companion second, the blueprint third, and the paper notes last.

That order matters. The essay gives you the argument. The companion gives you the fuller lay of the land, the omitted chapter logic, and the longer source explanations. The blueprint gives you the operator surface. The paper notes are where you go once you need named-method detail rather than a polished companion-level explanation.
