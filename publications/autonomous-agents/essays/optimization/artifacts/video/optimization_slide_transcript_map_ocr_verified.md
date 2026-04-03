# Optimization Chapter Slide-to-Transcript Map (OCR First, Visually Checked)

This draft uses:

- the transcript: `../transcript_Optimizing AI Agent Workflows for Production_full.txt`
- the numbered transcript: `../transcript_Optimizing AI Agent Workflows for Production_numbered.txt`
- the OCR text extracted from:
  `../slides/Agentic Optimization Blueprint/ocr/`

No timestamping is attempted here. The goal is only to identify the transcript lines where each slide should swap in.

## Proposed swaps

| Slide | Proposed transcript lines | Why this fit was chosen from transcript + OCR first, then visually checked |
| --- | --- | --- |
| `slide-001.png` | `0097-0145` | OCR gives the title card and the workflow-self-improvement framing. These lines are the chapter setup. |
| `slide-002.png` | `0101-0177` | OCR says “The Target Has Shifted.” These lines argue that optimization moves away from a single prompt and onto the full workflow. |
| `slide-003.png` | `0261-0285` | OCR says “Where to Apply Optimization Pressure.” These lines enumerate the four levers: prompts, topology, tools, and feedback loops. |
| `slide-004.png` | `0333-0817` | OCR says “The Research Landscape.” These lines are the literature tour from OPRO through textual gradients, self-improvement loops, and topology search. |
| `slide-005.png` | `1097-1233` | OCR says “Method Comparison Matrix.” These lines are the practical comparison block where the blueprint stages cheap fixes, feedback loops, judging, and workflow search. |
| `slide-006.png` | `1189-1233` | OCR says “Architectural Escalation Triggers.” These lines are the clearest explicit escalation block from local fixes to feedback loops to workflow search. |
| `slide-007.png` | `1009-1261` | OCR says “Recommended Build Order.” These lines are the explicit six-step optimization blueprint from locked evals through topology search. |
| `slide-008.png` | `0953-1097` | OCR says “Instrumentation Over Intuition.” These lines are the regression-check / locked-eval / metrics section that frames optimization as measurement first. |
| `slide-009.png` | `1533-1597` | OCR says “The Pragmatic Standard.” These lines are the final synthesis and closing warning about keeping humans in control of what success means. |

## Notes on uncertainty

- `slide-005.png`, `slide-006.png`, and `slide-007.png` all summarize the same blueprint section in different ways, so overlap is unavoidable.
- `slide-008.png` includes anti-pattern callouts directly on the slide, but the strongest transcript fit is still the earlier instrumentation-and-measurement block because that is the dominant visual message.
- `slide-004.png` is intentionally broad. It is a research-landscape slide, so it spans several distinct transcript subsections.

## Visual consistency review

After writing the OCR-first map, I visually checked the actual slide deck.

- Strong matches:
  - `slide-002.png` to `0101-0177`
  - `slide-003.png` to `0261-0285`
  - `slide-004.png` to `0333-0817`
  - `slide-005.png` to `1097-1233`
  - `slide-006.png` to `1189-1233`
  - `slide-007.png` to `1009-1261`
  - `slide-008.png` to `0953-1097`
  - `slide-009.png` to `1533-1597`

- Corrected after visual review:
  - `slide-004.png` was narrowed to start at `0333`, where the transcript actually begins the named research-paper tour.
  - `slide-006.png` was tightened to the late blueprint block where the escalation logic is stated most explicitly rather than the entire build-order section.
  - `slide-007.png` was widened to include the full six-step sequence through the point where the architecture becomes “as good as it can be” before search.
  - `slide-008.png` was widened to `0953-1097` because the slide mixes instrumentation, regression control, and dashboard metrics, all of which live in that combined transcript block.

- Still structurally awkward:
  - `slide-005.png` through `slide-008.png` are all summary-heavy slides. The transcript is more sequential than the deck, so the images naturally overlap in the same operational block.
