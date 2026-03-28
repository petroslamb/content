# Reasoning Chapter Slide-to-Transcript Map (OCR First, Visually Checked)

This draft uses:

- the transcript: `/Users/petros/Projects/content/autonomous-agent-blueprint/essays/reasoning/artifacts/transcript_Reasoning scaffolds for reliable AI agents_full.txt`
- the numbered transcript: `/Users/petros/Projects/content/autonomous-agent-blueprint/essays/reasoning/artifacts/transcript_Reasoning scaffolds for reliable AI agents_numbered.txt`
- the OCR text extracted from:
  `/Users/petros/Projects/content/autonomous-agent-blueprint/essays/reasoning/artifacts/slides/Reasoning Architectures/ocr/`

No timestamping is attempted here. The goal is only to identify the transcript lines where each slide should swap in.

## Proposed swaps

| Slide | Proposed transcript lines | Why this fit was chosen from transcript + OCR first, then visually checked |
| --- | --- | --- |
| `slide-001.png` | `0017-0029` | OCR gives the title card for the reasoning chapter. These lines are the chapter framing. |
| `slide-002.png` | `0053-0105` | OCR says “The Model is Not Always the Problem.” These lines make that exact argument and blame the missing scaffold rather than model capability. |
| `slide-003.png` | `0125-0205` | OCR says “The Escalation Thesis.” These lines define the split between lightweight defaults, overlays, and expensive escalations, while separating reasoning from planning. |
| `slide-004.png` | `0301-0413` | OCR says “The Default Reasoning Blueprint.” These lines introduce the baseline pattern: decomposition followed by the React loop. |
| `slide-005.png` | `0309-0389` | OCR says “Least-to-Most & Step-Back Prompting.” These lines are the structural-decomposition section. |
| `slide-006.png` | `0393-0521` | OCR says “ReAct.” These lines are the full thought-action-observation loop and its operational role. |
| `slide-007.png` | `0541-0645` | OCR says “Self-Refine & Reflexion.” These lines compare localized critique to persistent episodic learning. |
| `slide-008.png` | `0653-0801` | OCR says “Chain-of-Verification (CoVe).” These lines are the isolated factual-auditing mechanism and why it must be mechanically separated. |
| `slide-009.png` | `0809-0953` | OCR says “Self-Consistency.” These lines cover parallel sampling, majority voting, and the latency/cost trade-off. |
| `slide-010.png` | `0953-1069` | OCR says “Tree of Thoughts & LATS.” These lines cover tree search, LATS, and LLM+P as the heavy escalations. |
| `slide-011.png` | `1089-1105` | OCR says “Reasoning is an Architectural Menu, Not a Prompt Bag.” These lines are the pivot from primitives into operational synthesis. |
| `slide-012.png` | `1105-1201` | OCR says “The Reasoning Method Matrix.” These lines are the integrated build-order and method-selection summary. |
| `slide-013.png` | `1193-1201` | OCR says “Diagnostic Routing: If X, Choose Y.” These lines are the clearest literal routing summary: decomposition for deterministic multi-step work, React for live state, CoVe for factual accuracy, search for branching tasks. |
| `slide-014.png` | `1109-1181` | OCR says “Recommended Build Order.” These lines walk through the five-step staged deployment order. |
| `slide-015.png` | `1281-1309` | OCR says “Evaluating the Reasoning Stack.” These lines define evaluation by post-verification success, tool-grounded coherence, and cost per solved task. |
| `slide-016.png` | `1205-1277` | OCR says “Architectural Anti-Patterns.” These lines cover overusing chain-of-thought without grounding and confusing verbal fluency with validated reasoning. |
| `slide-017.png` | `1337-1369` | OCR gives the conclusion slide. These lines are the restraint-focused close and final listener prompt. |

## Notes on uncertainty

- `slide-012.png`, `slide-013.png`, and `slide-014.png` all summarize the same operational synthesis block, so some overlap is unavoidable.
- `slide-015.png` and `slide-016.png` are structurally reversed relative to the transcript. The deck puts evaluation before anti-patterns, while the transcript introduces anti-patterns first and then moves into the evaluation criteria.
- `slide-011.png` is a short bridge slide. It works best exactly at the transition into the synthesis section rather than as a long section anchor.

## Visual consistency review

After writing the OCR-first map, I visually checked the actual slide deck.

- Strong matches:
  - `slide-002.png` to `0053-0105`
  - `slide-005.png` to `0309-0389`
  - `slide-006.png` to `0393-0521`
  - `slide-007.png` to `0541-0645`
  - `slide-008.png` to `0653-0801`
  - `slide-009.png` to `0809-0953`
  - `slide-010.png` to `0953-1069`
  - `slide-014.png` to `1109-1181`
  - `slide-015.png` to `1281-1309`
  - `slide-017.png` to `1337-1369`

- Corrected after visual review:
  - `slide-004.png` was expanded to `0301-0413` because the slide is not just decomposition; it visually frames the full default baseline that includes decomposition feeding the loop.
  - `slide-016.png` was moved earlier than the deck order would imply because the anti-pattern content is clearly in `1205-1277`, not after the evaluation block.

- Still structurally awkward:
  - `slide-012.png` and `slide-013.png` compress the same operational synthesis into two different summary visuals. The transcript is more verbal and sequential than the deck.
