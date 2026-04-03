# Multi-Agent Chapter Slide-to-Transcript Map (OCR First, Visually Checked)

This draft uses:

- the transcript: `../transcript_The escalation path for multi agent AI_full.txt`
- the numbered transcript: `../transcript_The escalation path for multi agent AI_numbered.txt`
- the OCR text extracted from:
  `../slides/Multi-Agent Design Blueprint/ocr/`

No timestamping is attempted here. The goal is only to identify the transcript lines where each slide should swap in.

## Proposed swaps

| Slide | Proposed transcript lines | Why this fit was chosen from transcript + OCR first, then visually checked |
| --- | --- | --- |
| `slide-001.png` | `0053-0105` | OCR gives the chapter title and the workflow-decomposition thesis. These lines are the clean chapter framing. |
| `slide-002.png` | `0097-0221` | OCR says multi-agent solves workflow problems, not missing intelligence. These lines are the “agent theater” critique and workflow-decomposition argument. |
| `slide-003.png` | `0225-0245` | OCR says architecture begins with four practical workflow questions. These lines enumerate those four questions directly. |
| `slide-004.png` | `0893-0905` | OCR says multi-agent design is an escalation path, not the baseline. These lines make that exact claim at the start of the matrix section. |
| `slide-005.png` | `0345-0393` | OCR says bounded delegation is justified when roles need distinct tools or permissions. These lines are the cleanest role-splitting explanation. |
| `slide-006.png` | `0457-0581` | OCR says role-based pipelines for staged workflows. These lines cover MetaGPT and ChatDev as structured staged pipelines. |
| `slide-007.png` | `1053-1069` | OCR says add a critic overlay only for high-value outputs. These lines are the level-four critic/reviewer escalation. |
| `slide-008.png` | `0729-0805` | OCR says reserve debate and consensus for hard judgment tasks. These lines cover MAD and Reconcile. |
| `slide-009.png` | `1153-1197` | OCR says prefer typed artifact handoffs over free-form conversation. These lines are the explicit artifact-contract argument. |
| `slide-010.png` | `1201-1221` | OCR says keep humans as explicit, first-class nodes. These lines are the human-as-routing-node section. |
| `slide-011.png` | `0901-1093` | OCR says this is the diagnostic matrix for escalating complexity. These lines are the five-level escalation matrix. |
| `slide-012.png` | `0817-0857` | OCR says match topology to workflow shape. These lines are the synthesis across role separation, critique, and artifact-based decomposition. |
| `slide-013.png` | `1285-1361` | OCR says a valid topology must beat a strong single-agent baseline. These lines are the evaluation block around end-task quality, overhead, cost, and failure localization. |
| `slide-014.png` | `1365-1389` | OCR says multi-agent design is workflow decomposition, not magic emergence. These lines are the final synthesis and close. |

## Notes on uncertainty

- `slide-004.png` appears much later in the transcript than the surrounding early conceptual slides. The deck uses the escalation idea as an early principle, but the transcript restates it most explicitly in the matrix section.
- `slide-012.png` is a synthesis slide. It visually condenses a pattern the transcript develops across several sections, especially the literature synthesis and the matrix.
- `slide-009.png` and `slide-010.png` are part of the later practical build-order block, not the earlier literature discussion, so the deck becomes more operational than the transcript at that point.

## Visual consistency review

After writing the OCR-first map, I visually checked the actual slide deck.

- Strong matches:
  - `slide-002.png` to `0097-0221`
  - `slide-003.png` to `0225-0245`
  - `slide-005.png` to `0345-0393`
  - `slide-006.png` to `0457-0581`
  - `slide-007.png` to `1053-1069`
  - `slide-008.png` to `0729-0805`
  - `slide-009.png` to `1153-1197`
  - `slide-010.png` to `1201-1221`
  - `slide-011.png` to `0901-1093`
  - `slide-013.png` to `1285-1361`
  - `slide-014.png` to `1365-1389`

- Corrected after visual review:
  - `slide-004.png` was aligned to `0893-0905`, not the earlier thesis section, because the image is explicitly the “escalation path” staircase rather than the general anti-agent-theater argument.
  - `slide-012.png` was kept on the synthesis block around `0817-0857` because the image is conceptual rather than matrix-shaped.

- Still structurally awkward:
  - `slide-012.png` conceptually sits next to `slide-011.png`, but the transcript reaches the cleanest “match topology to problem shape” phrasing slightly earlier than the full escalation matrix.
