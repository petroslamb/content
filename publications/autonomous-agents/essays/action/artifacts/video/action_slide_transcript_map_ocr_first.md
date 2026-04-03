# Action Chapter Slide-to-Transcript Map (OCR First)

This draft uses only:

- the transcript: `../transcript_Action Systems and Tool Use_full.txt`
- the OCR text extracted from the slide images in:
  `../slides/Engineering Reliable Action/ocr/`

No timestamping is attempted here. The goal is only to identify the transcript lines where each slide should swap in.

## Proposed swaps

| Slide | Proposed transcript lines | Why this fit was chosen from transcript + OCR only |
| --- | --- | --- |
| `slide-001.png` | `0061-0109` | OCR says “Architecting Reliable Action Systems” and “Moving from language generation to explicit software execution.” These lines are where the chapter is introduced and framed as the move from theoretical intelligence to practical utility. |
| `slide-002.png` | `0069-0133` | OCR says “Reasoning Does Not Make an Agent” and contrasts “Describing Work” vs “Performing Work.” These lines explicitly state “Reasoning is not agency” and give the file-renaming example. |
| `slide-003.png` | `0273-0557` | OCR says “Deconstructing the Action Monolith” and lays out detection, selection, filling, execution, integration, with explicit Gorilla and HuggingGPT references. These lines span the five-subproblem breakdown and the follow-on discussion of Toolformer, Gorilla, and HuggingGPT. |
| `slide-004.png` | `0217-0249` | OCR points to the action representation ladder and the rule to “move upward on the ladder.” These lines define typed tool invocations and explicitly say designers should move upward on the ladder whenever possible. |
| `slide-005.png` | `0781-0877` | OCR says “Navigating the Five Action Surfaces” with a comparison matrix. These lines are where the transcript walks surface-by-surface through API, code, SQL, browser, and GUI. |
| `slide-006.png` | `0561-0605` | OCR says “Designing for Absolute Reproducibility,” contrasts APIs with code, and explicitly cites `SWE-agent` and `OpenHands`. These lines are the software-engineering section where the transcript introduces those exact references and frames code as the required surface for reproducible work. |
| `slide-007.png` | `0625-0681` | OCR says “Operating on Enterprise Reality” and stresses structured-data agents and Database/SQL action. These lines are the Bird/Spider 2.0 pivot into SQL-native agent work. |
| `slide-008.png` | `0689-0769` | OCR says “Interacting with Closed and Visual Systems” and names browser and GUI/mobile action. These lines cover WebAgent, Mind2Web, mobile agents, and the visual-interface fallback. |
| `slide-009.png` | `0885-0941` | OCR says “The Closed-Loop Action Architecture” with reasoning, execution, observation, recovery, and tool specialization. These lines transition from tool specialization into the engine-room architecture. |
| `slide-010.png` | `0913-0961` | OCR says “Enforcing Least-Privilege Execution” and mentions sandboxed execution, input validation, and output normalization. These lines are the execution-layer and observation-layer explanation. |
| `slide-011.png` | `0969-0985` | OCR says “Handling Failure with State, Not Apologies.” These lines make that exact argument and show why errors must create machine-readable state. |
| `slide-012.png` | `1013-1037` | OCR says “The Escalation Path: A Build Strategy.” These lines are the explicit step-by-step build order from APIs to code to SQL/browser to GUI. |
| `slide-013.png` | `0985-1013` | OCR says “Measuring Action Reality vs. Vibes.” These lines are the evaluation section beginning with the rejection of “end-task vibes” and listing the key metrics. |
| `slide-014.png` | `1037-1057` | OCR says “Critical Structural Anti-Patterns” and lists God-Agent, unnormalized output, plain-text plans, and defaulting to computer use. These lines are the anti-pattern section. |
| `slide-015.png` | `1061-1097` | OCR says “Action Must Be Bounded and Measurable.” These lines are the chapter close and final synthesis around bounded, measurable, replayable action. |

## Notes on uncertainty

- `slide-003.png` and `slide-004.png` appear reversed relative to the transcript flow. The transcript introduces the representation ladder before the five-subproblem “action monolith” breakdown, while the slide filenames place the monolith slide first.
- `slide-005.png` is a matrix summary slide, so it naturally overlaps with several later slides (`006`, `007`, `008`) that unpack specific surfaces in more detail.
- `slide-009.png` combines two transcript regions into one visual frame: tool specialization and the closed-loop execution/observation/recovery architecture.
- `slide-013.png` and `slide-012.png` are close neighbors conceptually. The transcript does evaluation first and then the step-by-step build order; the proposed mapping follows that sequence.

## Visual consistency review

After writing the OCR-first map, I visually checked the actual slide images.

- Strong matches:
  - `slide-005.png` to `0781-0877`
  - `slide-007.png` to `0625-0681`
  - `slide-008.png` to `0689-0769`
  - `slide-010.png` to `0913-0961`
  - `slide-011.png` to `0969-0985`
  - `slide-012.png` to `1013-1037`
  - `slide-013.png` to `0985-1013`
  - `slide-014.png` to `1037-1057`
  - `slide-015.png` to `1061-1097`

- Corrected after visual review:
  - `slide-006.png` was initially mapped too late into the generic action-surface matrix. The actual slide explicitly foregrounds `SWE-agent` and `OpenHands`, so the better fit is `0561-0605`.

- Still structurally awkward:
  - `slide-003.png` vs `slide-004.png`. The slide deck places the action-monolith frame before the representation-ladder frame, while the transcript explains the ladder first and the monolith second.
  - `slide-009.png`. The image itself fuses two ideas the transcript treats separately: specialized tools and the execution-observation-recovery loop.
