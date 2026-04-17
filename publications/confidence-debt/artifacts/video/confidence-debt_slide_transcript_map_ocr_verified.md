# Confidence Debt Slide-to-Transcript Map (Precision Verified)

This map aligns the 17 `latest` slides to the exact anchors in `confidence-debt_auto_captions.srt`.

## Precision Anchors

| Slide | Target Narration Anchor Phrase | Logic / Context |
| :--- | :--- | :--- |
| `slide-001.png` | (Start) | Title card. |
| `slide-002.png` | "flawless... It looks finished." | The "Thing of Beauty" discussion. |
| `slide-003.png` | "The EIP Verify incident" | Narrative shift to the specific failure case. |
| `slide-004.png` | "Confidence debt is the act of borrowing..." | Formal definition block. |
| `slide-005.png` | (Compression Funnel intro) | Visual diagram showing the funnel steps. |
| `slide-006.png` | "...nutritional label on a highly [processed...]" | Shift to the failure of passive transparency. |
| `slide-008.png` | "...misunderstood because a single dashboard..." | Explanation of the single-number trap. |
| `slide-009.png` | "...long horizon decay and trajectory..." | The car alignment analogy. |
| `slide-012.png` | "...competence shadow and forces it right..." | The keyhole effect explanation. |
| `slide-007.png` | "...confidence debt is born at gate one." | Transition to the First Gate: Claim Auditability. |
| `slide-010.png` | "The debt balloons at gate two." | Transition to the Second Gate: Reliability Release. |
| `slide-014.png` | "Appropriate reliance is a..." | Technical comparison with existing literature. |
| `slide-016.png` | "...into the absolute core doctrine." | Synthesis section. |
| `slide-013.png` | (Gate 3 / Co-Audit discussion) | Transition to the Third Gate. |
| `slide-015.png` | "...confidence debt requires us to [restructure...]" | The downstream cascade diagram. |
| `slide-017.png` | "Stop the cascade before it..." | Final doctrine slide. |

## Visual Variety Plan (Interleaving)

Per User Strategy: For each segment defined above, the video will swap to the `previous/` deck variant at the **arithmetic midpoint** of the segment's duration in the narration.

1.  Calculate duration between precision anchors.
2.  Place `latest/slide-XXX.png` at the Anchor Timestamp.
3.  Place `previous/slide-XXX.png` at `Anchor Timestamp + (Duration / 2)`.
