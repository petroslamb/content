# Operating Agents Coverage Map V7

This note is the breadth layer behind the `v7` essay package. The public essays are intentionally sharper and narrower than both the distilled chapter guide and the full survey. This file shows what each `v7` post covers, what source terrain sits behind it, what it leaves out on purpose, and where an interested reader should go next.

**Reading order:** Launch Note, Action, Memory, Reasoning, Multi-Agent, Safety, then Optimization.

## How To Use This Layer

- Essays: the public doctrine layer built for strong thesis shape, public readability, and reuse by builders
- Companions: second-pass essays that reconnect each post to omitted terrain, fuller source interpretation, and broader chapter logic
- Blueprints: the operator layer for architecture choices, build order, and anti-patterns
- Paper notes: the source-note layer for named methods and individual literature artifacts

Only Parts I through VI have dedicated companions. The launch note routes to this map and the broader package.

## Series Map

| Piece | Current thesis | Distilled chapter-guide sections | Original survey sections | What the essay emphasizes | What it leaves out on purpose | Where to go next |
|---|---|---|---|---|---|---|
| [Launch Note](./launch-note/00-launch-note-v7.md) | Reliable agents come from explicit operating layers, not capability stacking | [Practical chapters guide](../reference/chapters-guide.md) reading order and [practical distillation](../reference/practical-distillation.md) | Chapters `2`, `3`, `8`, `9`, `11`, `14`, `17` to `19` as the practical stack | postmortem-first framing, doctrine stack, publication order versus architecture order, reviewability standard | chapter-specific nuance, source breadth, deeper sequencing argument | [Practical chapters guide](../reference/chapters-guide.md)<br>[Practical distillation](../reference/practical-distillation.md) |
| [Action](./action/01-action-tool-use-v7.md) | Language becomes agency only when it becomes accountable state change | Guide Chapter `8`, especially `8.3.1`, `8.3.2`, `8.3.3` | Survey Chapter `8`, especially `8.1`, `8.2`, `8.3.1`, `8.3.2`, `8.3.3`, `8.4` | seam-level action failure, observation contracts, surface escalation, uncertainty reduction | physical action, broader action-learning literature, GUI and computer-use frontier depth, structured data surface detail | [Action companion](./action/companion-v7.md)<br>[Action blueprint](../core/practical-chapter-blueprints/03-action-tool-use-blueprint.md) |
| [Memory](./memory/03-memory-v7.md) | Memory is governance over time, not storage | Guide Chapter `3`, especially `3.3.2`, `3.3.3`, `3.4`, `3.4.3`, `3.4.4`, `3.4.6` | Survey Chapter `3`, especially `3.2`, `3.3.2`, `3.3.3`, `3.4.1` to `3.4.6` | stale-state authority, typed memory layers, provenance, derivation, forgetting | human-memory analogy, richer lifecycle detail, graph-heavy retrieval frontier, procedural-promotion breadth | [Memory companion](./memory/companion-v7.md)<br>[Memory blueprint](../core/practical-chapter-blueprints/01-memory-blueprint.md) |
| [Reasoning](./reasoning/02-reasoning-planning-v7.md) | Most production reasoning failures are control failures before they are intelligence failures | Guide Chapter `2`, especially `2.2.2`, `2.2.2.2`, `2.2.3`, `2.2.4` | Survey Chapter `2`, especially `2.2.1`, `2.2.2`, `2.2.3`, `2.2.4` | scaffold diagnosis, decomposition, ReAct, verification, planner handoff, late search | broader reasoning taxonomy, self-refinement breadth, consensus methods, abstraction-reset methods, search family detail | [Reasoning companion](./reasoning/companion-v7.md)<br>[Reasoning blueprint](../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md) |
| [Multi-Agent](./multi-agent/04-multi-agent-v7.md) | Extra agents multiply ambiguity unless they create a real boundary | Guide Chapter `14`, especially `14.1.2`, `14.2.1`, `14.3.4`, `14.4`, `14.5`, `14.6.1`, `14.6.3` | Survey Chapters `13` to `16`, especially `13.1.2`, `14.2`, `14.5`, `14.6`, `15`, `16` | permission boundaries, critique overlays, typed artifact handoffs, collapse discipline | broader topology catalog, protocol layers, collective-intelligence framing, human-placement depth, evaluation breadth | [Multi-agent companion](./multi-agent/companion-v7.md)<br>[Multi-agent blueprint](../core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md) |
| [Safety](./safety/05-safety-v7.md) | Agent safety is trust-boundary design, not refusal theater | Guide safety chapters, especially `17.1.2`, `17.1.3`, `18.2.1`, `18.2.2`, `19.1`, `19.2`, `19.3` | Survey Chapters `17`, `18`, `19`, and adjacent Chapter `20` context | indirect injection, tool-scope segmentation, trust reset, channel policy, predeployment abuse rehearsal | broader hallucination framing, supply-chain detail, perception threats, attack taxonomies, safety-scaling context | [Safety companion](./safety/companion-v7.md)<br>[Safety blueprint](../core/practical-chapter-blueprints/06-safety-blueprint.md) |
| [Optimization Bonus](./optimization/06-optimization-v7.md) | The workflow is the object | Guide Chapters `9` and `11`, especially `9.2`, `9.2.3`, `9.3`, `9.4`, `9.4.3`, `11.1` | Survey Chapters `9`, `10`, `11`, especially `9.2`, `9.3`, `9.4`, `9.5`, `10.1` to `10.4`, `11.1` | objective stability, evaluation architecture, failure-class accounting, review burden, bounded self-improvement | wider optimization taxonomy, judge-systems depth, workflow-search breadth, frontier self-improvement detail | [Optimization companion](./optimization/companion-v7.md)<br>[Optimization blueprint](../core/practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md) |

## Reading Rule

Use the essay first, the companion second, the blueprint third, and the paper notes last.

That order matters. The essay gives you the argument. The companion gives you the fuller lay of the land, the omitted chapter logic, and the longer source explanations. The blueprint gives you the operator surface. The paper notes are where you go once you need named-method detail rather than a polished companion-level explanation.
