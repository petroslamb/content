# Memory Chapter Slide-to-Transcript Map (OCR First, Visually Checked)

This draft uses:

- the transcript: `../transcript_The Four Layer AI Memory Blueprint_full.txt`
- the numbered transcript: `../transcript_The Four Layer AI Memory Blueprint_numbered.txt`
- the OCR text extracted from:
  `../slides/AI Memory Architecture/ocr/`

No timestamping is attempted here. The goal is only to identify the transcript lines where each slide should swap in.

## Proposed swaps

| Slide | Proposed transcript lines | Why this fit was chosen from transcript + OCR first, then visually checked |
| --- | --- | --- |
| `slide-001.png` | `0041-0057` | OCR gives the chapter title and subtitle. These lines are the clean intro framing for the memory blueprint. |
| `slide-002.png` | `0057-0149` | OCR says almost every serious agent breaks beyond a single prompt and names the two bad defaults. These lines are exactly the collapse-of-memory / prompt-packing framing. |
| `slide-003.png` | `0153-0201` | OCR says the architecture must answer four distinct questions. These lines enumerate those four questions directly. |
| `slide-004.png` | `0213-0233` | OCR shows the physical workspace analogy across all four layers. The best fit is where the transcript moves from the abstract four-layer split into the chef-workspace analogy. |
| `slide-005.png` | `0213-0357` | OCR says “Layer 1 & 2: Active State vs. Durable Knowledge.” These lines cover working memory first, then semantic memory as the next durable retrieval layer. |
| `slide-006.png` | `0361-0533` | OCR says “Layer 3 & 4: Traces and Reusable Know-How.” These lines cover episodic memory, procedural memory, and the recap of all four layers. |
| `slide-007.png` | `1061-1085` | OCR says the memory system is a continuously running governor and shows the lifecycle pipeline. These lines are the cleanest pure lifecycle introduction before the discussion turns toward retrieval intent and decay. |
| `slide-008.png` | `1101-1141` | OCR says forgetting is mandatory and shows the decay curve. The exact conceptual fit is the later “forgetting mandate” block, not the earlier research-paper introduction. |
| `slide-009.png` | `1081-1141` | OCR shows the unified memory schematic with pruning. Visually this is the synthesis slide for the policy-system section, so it fits the write-policy checks plus the forgetting mandate together. |
| `slide-010.png` | `1153-1277` | OCR says “Architectural trade-offs: The Memory Method Matrix.” These lines are the explicit “if your problem looks like X, choose Y” decision matrix. |
| `slide-011.png` | `0541-1053` | OCR says “The Research Foundation: Toolkits, not textbooks.” These lines are the seven-paper literature walk-through that grounds the architecture. |
| `slide-012.png` | `1485-1517` | OCR says “The Deployment Protocol: Recommended Build Order.” These lines are the explicit five-step build order. |
| `slide-013.png` | `1281-1389` | OCR says “Critical Failure Modes & Anti-Patterns.” These lines are the anti-pattern section: mixed channels, stale state, neural memory in weights, over-writing raw logs, and retrieval-as-verification. |
| `slide-014.png` | `1405-1481` | OCR says “The Memory Evaluation Stack.” These lines enumerate the measurement stack: retrieval relevance, stale-memory rate, token savings, correction recurrence, reuse, and write precision. |
| `slide-015.png` | `1521-1569` | OCR says “Memory is not longer context. It is governable state.” These lines are the chapter synthesis and closing argument. |

## Notes on uncertainty

- `slide-011.png` is broad by design. It is the research-foundation summary slide, so it naturally spans a much larger transcript region than the other slides.
- The deck order diverges from the transcript in section three. The deck places lifecycle, forgetting, and the unified schematic before the research-foundation summary slide, while the transcript explains the research literature first and only then arrives at the policy-system architecture.

## Visual consistency review

After writing the OCR-first map, I visually checked the actual slide deck.

- Strong matches:
  - `slide-002.png` to `0057-0149`
  - `slide-003.png` to `0153-0201`
  - `slide-005.png` to `0213-0357`
  - `slide-006.png` to `0361-0533`
  - `slide-007.png` to `1061-1097`
  - `slide-010.png` to `1153-1277`
  - `slide-012.png` to `1485-1517`
  - `slide-013.png` to `1281-1389`
  - `slide-014.png` to `1405-1481`
  - `slide-015.png` to `1521-1569`

- Corrected after visual review:
  - `slide-004.png` was moved to `0213-0233`. OCR alone makes it tempting to place it before the analogy begins, but the actual image is explicitly the workspace metaphor.
  - `slide-008.png` was moved from the earlier research-paper discussion to `1101-1141` because the slide itself is about mandatory forgetting as an architectural policy, not just the existence of decay research.
  - `slide-009.png` was tightened to `1081-1141` because the image fuses the policy checks and pruning logic into one full-system schematic.

- Still structurally awkward:
  - `slide-011.png` appears later in the deck than it does in the transcript. That is a real structural mismatch between the slide order and the spoken chapter.
