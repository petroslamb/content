# Confidence Debt Slide-to-Transcript Map

Manual visual/SRT review for the rebuilt longform render. The OCR-first draft was used only as a warning signal: it collapsed most slides into the ending captions and was not used for final ordering.

## Rebuild Principles

- Use the latest deck as the primary argument spine.
- Use the previous deck as supporting visual variation at matching argument points.
- Preserve every `latest` slide and every `previous` slide at least once.
- Anchor slide changes to the timestamped SRT after reading the transcript flow, not to keyword or OCR matches.
- Use the project-root Rooted Layers mark as the opening and the inverted mark as the closing, wrapped to 16:9 bookend images for clean video framing.

## Cue Map

| Start | Slide | Narrative anchor |
| :--- | :--- | :--- |
| `00:00:00.000` | `bookends/rooted_layers_open_16x9.png` | Opening Rooted Layers mark. |
| `00:00:16.000` | `latest/slide-001.png` | Scenario setup under the confidence-debt title. |
| `00:00:59.520` | `latest/slide-002.png` | “An absolute thing of beauty” / the polished 4:45 p.m. AI report. |
| `00:02:49.840` | `previous/slide-001.png` | Borrowed trust after forwarding without checking evidence. |
| `00:04:28.720` | `latest/slide-004.png` | “Confidence debt describes…” formal definition. |
| `00:06:07.680` | `latest/slide-003.png` | EIP-verify incident begins. |
| `00:07:56.720` | `previous/slide-002.png` | Two generated artifacts: polished summary versus row-level evidence. |
| `00:09:56.880` | `previous/slide-005.png` | ABI helpers, test fixtures, and RPC glue mistaken for core logic. |
| `00:11:43.600` | `latest/slide-003.png` | 13-of-15 follow-up failures and contradiction statistics. |
| `00:13:15.040` | `latest/slide-005.png` | The usable false artifact travels while raw evidence is ignored. |
| `00:14:23.600` | `previous/slide-003.png` | Technical debt, epistemic debt, and confidence debt contrast. |
| `00:15:01.600` | `latest/slide-004.png` | “Confidence debt is the act of borrowing trust.” |
| `00:16:00.639` | `latest/slide-007.png` | Gate 1: claim auditability at the artifact layer. |
| `00:17:20.880` | `previous/slide-006.png` | Contradiction register and blocked approval workflow. |
| `00:18:56.000` | `latest/slide-007.png` | Provenance coverage, soundness, contradiction transparency, audit effort. |
| `00:20:38.240` | `previous/slide-012.png` | Paper Trail and passive transparency. |
| `00:22:14.880` | `latest/slide-006.png` | Nutrition-label analogy / transparency without behavioral blockage. |
| `00:23:56.159` | `latest/slide-007.png` | Dead approve button, forced adjudication, temporal validity. |
| `00:25:27.360` | `previous/slide-004.png` | Compression as the argument moves from claims to dashboards. |
| `00:26:13.679` | `latest/slide-008.png` | Gate 2: reliability release and the single-number dashboard trap. |
| `00:27:27.520` | `previous/slide-007.png` | Pass@1 versus Pass@8 collapse. |
| `00:29:50.320` | `latest/slide-010.png` | ReliabilityBench envelope replaces flat percentages. |
| `00:30:54.960` | `previous/slide-008.png` | Measured deployment envelope: k, epsilon, lambda. |
| `00:32:36.399` | `latest/slide-009.png` | Car-alignment analogy for long-horizon drift. |
| `00:34:00.000` | `previous/slide-009.png` | Trajectory drift and bounded autonomy. |
| `00:36:01.119` | `latest/slide-011.png` | Gate 3: frictionless automation hollows human correction capacity. |
| `00:36:57.920` | `previous/slide-010.png` | Engaged friction versus passive review. |
| `00:38:39.280` | `latest/slide-011.png` | Contractor-style AI use and later debugging collapse. |
| `00:39:44.640` | `latest/slide-012.png` | Competence shadow and keyhole effect. |
| `00:40:27.440` | `previous/slide-011.png` | Keyhole/tiger visual for hidden hazards. |
| `00:42:40.640` | `latest/slide-013.png` | Co-audit as the human-layer fix. |
| `00:43:02.079` | `previous/slide-013.png` | Forced adjudication UI and cognitive forcing functions. |
| `00:44:13.440` | `latest/slide-013.png` | Hypothesis-driven interfaces and counter-evidence. |
| `00:45:02.640` | `latest/slide-015.png` | The failures finance each other. |
| `00:45:25.119` | `previous/slide-014.png` | Fintech cascade setup and step one. |
| `00:46:46.800` | `latest/slide-015.png` | Step three: human reviewer, system crash, regulatory impact. |
| `00:47:56.720` | `latest/slide-014.png` | Appropriate reliance critique. |
| `00:49:32.079` | `previous/slide-015.png` | Micro decision calibration versus macro workflow failure. |
| `00:51:20.000` | `latest/slide-016.png` | Three gates synthesis. |
| `00:52:25.599` | `previous/slide-016.png` | Three rules for surviving generative workflows. |
| `00:53:02.079` | `latest/slide-017.png` | Doctrine of friction. |
| `00:53:40.000` | `previous/slide-017.png` | Friction as a reliability feature. |
| `00:54:08.880` | `bookends/rooted_layers_close_16x9.png` | Closing inverted Rooted Layers mark on “Stop the cascade before it starts.” |

## Workflow Notes

- The OCR-first caption aligner produced unusable late-video matches for this deck because the slide text is conceptual and repeated across sections.
- Manual SRT review should be the default for multi-deck interleaving when slide order already follows the narration.
- The renderer needed an explicit audio-duration cap. Relying on `-shortest` still allowed the video stream to overrun by about 18 seconds because the concat demuxer repeats the final still.
