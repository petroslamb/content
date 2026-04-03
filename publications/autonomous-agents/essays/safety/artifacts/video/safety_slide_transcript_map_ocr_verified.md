# Safety Chapter Slide-to-Transcript Map (OCR First, Visually Checked)

This draft uses:

- the transcript: `../transcript_The Architecture of AI Agent Safety_full.txt`
- the numbered transcript: `../transcript_The Architecture of AI Agent Safety_numbered.txt`
- the OCR text extracted from:
  `../slides/Agent Safety Architecture/ocr/`

No timestamping is attempted here. The goal is only to identify the transcript lines where each slide should swap in.

## Proposed swaps

| Slide | Proposed transcript lines | Why this fit was chosen from transcript + OCR first, then visually checked |
| --- | --- | --- |
| `slide-001.png` | `0017-0045` | OCR is weak, but the image is clearly the title card. These lines are the chapter framing on agent safety as system architecture. |
| `slide-002.png` | `0081-0117` | OCR asks where attackers or failure chains take control. These lines state that exact practical question and list the major vulnerability classes. |
| `slide-003.png` | `0093-0125` | OCR says “The Practical Attack Surface Map.” These lines are the clean high-level attack-surface framing before the transcript zooms into individual mechanisms. |
| `slide-004.png` | `0125-0169` | OCR says “The Poisoned Context Window.” These lines are the direct explanation of indirect prompt injection via mixed instructions and data. |
| `slide-005.png` | `0173-0293` | OCR says “From Text to Side Effects.” These lines move from prompt injection into tool-integrated agents, sandboxing, least privilege, and approval gates. |
| `slide-006.png` | `0297-0385` | OCR says “The Memory Liability.” These lines are the durable-memory poisoning and jamming discussion. |
| `slide-007.png` | `0449-0473` | OCR says “Inter-Agent Contamination Flow.” These lines are the zero-trust treatment of inter-agent files and messages. |
| `slide-008.png` | `0525-0529` | OCR says safety failures happen at interfaces. These lines are the exact thesis statement that safety is interface architecture, not a suffix classifier. |
| `slide-009.png` | `0529-0581` | OCR says “The Default Safety Blueprint.” Visually it is the main system schematic, so it belongs to the architecture-and-matrix synthesis block that follows the thesis sentence. |
| `slide-010.png` | `0533-0541` | OCR says “Boundary 1: Trust Separation.” These lines are the trust-separation row of the Aura matrix walkthrough. |
| `slide-011.png` | `0545-0557` | OCR says “Boundaries 2 & 3: Containment and Approval.” These lines are tool containment and approval gates in the Aura scenario. |
| `slide-012.png` | `0561-0565` | OCR says “Boundary 4: Memory Hygiene.” These lines are the memory-hygiene row of the matrix. |
| `slide-013.png` | `0565-0573` | OCR says “Boundaries 5 & 6: Skepticism and Verification.” These lines cover inter-agent skepticism and verification in the Aura walkthrough. |
| `slide-014.png` | `0529-0577` | OCR is the control matrix. These lines are the full Aura matrix walk-through from trust separation through verification. |
| `slide-015.png` | `0589-0605` | OCR says “Evaluating the Architecture.” These lines are the testing suite: injection resistance, red-team tools, poisoning simulations, contamination drills, approval bypass, and incident replay. |
| `slide-016.png` | `0609-0621` | OCR says “Recommended Build Order.” These lines are the explicit six-step deployment order. |
| `slide-017.png` | `0625-0665` | OCR says “Architectural Anti-Patterns.” These lines are the anti-pattern section: mixed prompts, suffix prompts, self-poisoning memory, debate-as-safety, and post-hoc monitoring. |
| `slide-018.png` | `0669-0685` | OCR says “Agent Safety Is Architecture.” These lines are the chapter close and final synthesis. |

## Notes on uncertainty

- `slide-009.png` and `slide-014.png` still overlap on purpose because one is the blueprint diagram and the other is the full control matrix for the same architectural block.
- `slide-010.png` through `slide-013.png` are best treated as zoomed-in rows of the matrix rather than fully separate narrative sections.
- The transcript is denser than the deck in the early attack-surface section, so `slide-003.png`, `slide-004.png`, and `slide-005.png` form a quick visual progression over a broad continuous discussion.

## Visual consistency review

After writing the OCR-first map, I visually checked the actual slide deck.

- Strong matches:
  - `slide-002.png` to `0081-0117`
  - `slide-003.png` to `0093-0125`
  - `slide-004.png` to `0125-0169`
  - `slide-005.png` to `0173-0293`
  - `slide-006.png` to `0297-0385`
  - `slide-007.png` to `0449-0473`
  - `slide-008.png` to `0525-0529`
  - `slide-010.png` to `0533-0541`
  - `slide-011.png` to `0545-0557`
  - `slide-012.png` to `0561-0565`
  - `slide-013.png` to `0565-0573`
  - `slide-015.png` to `0589-0605`
  - `slide-016.png` to `0609-0621`
  - `slide-017.png` to `0625-0665`
  - `slide-018.png` to `0669-0685`

- Corrected after visual review:
  - `slide-003.png` was narrowed to `0093-0125` because the image is a map of the attack surface, not the full later tool-containment sequence.
  - `slide-008.png` was tightened to the thesis line itself. The image is effectively a bumper slide for the “interfaces” claim.
  - `slide-009.png` was separated from `slide-008.png` and tied to the blueprint-and-matrix walkthrough that follows.
  - `slide-014.png` was widened to cover the entire Aura walkthrough because it is visually the matrix slide, not one individual row.

- Still structurally awkward:
  - `slide-003.png`, `slide-004.png`, and `slide-005.png` compress a long attack-surface sequence into three fast visuals. The transcript does not pause cleanly between them.
