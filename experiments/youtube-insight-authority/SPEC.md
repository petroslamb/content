# Insight Authority YouTube Experiment

## Status

- Experiment id: `insight_authority_cinematic`
- State workspace: `experiments/youtube-insight-authority/`
- Analytics registry entry: `experiments/youtube-analytics/experiment_registry.yaml`
- Created: 2026-05-09
- Current posture: live YouTube apply completed; analytics baseline refreshed
- Live apply completed: `2026-05-09T11:43:52Z`
- Final readback completed: `2026-05-09T11:46:45Z`
- Analytics refresh completed: `2026-05-09T11:45:58Z`

## Source Of Truth

The experiment source of truth is this folder:

- `manifest.yaml`: experiment metadata, state pointers, mutation boundary, and dashboard registration intent
- `authority_packets.yaml`: apply-mode packet contract and applied packet record
- `cohort.yaml`: canonical initial cohort, inclusion rationale, YouTube ids, and local evidence paths
- `evaluation_rubric.yaml`: manual and analytics scoring rules
- `studio_verification.yaml`: Studio/API verification checklist, mutation readback expectations, and apply readback state
- `release_ledger.md`: experiment state changes and review notes
- `youtube_mutation_report.json`: bounded live YouTube mutation report
- `youtube_final_readback.json`: post-apply API readback for title, description, tags, thumbnail URL, and technical comments

The analytics registry is only the dashboard index. It should mirror the cohort video ids, but it does not own cohort rationale or operational state.

## Hypothesis

Cinematic briefs that state a concrete operating insight in the title, description, thumbnail, and first minute should outperform more general cinematic briefs on qualified attention:

- better average viewed percentage for the same format band
- stronger views per day after the first distribution pulse
- higher thumbnail click-through rate when impressions are sufficient
- more downstream movement into full research breakdowns, essays, or related videos
- higher subscriber conversion when the claim is practical rather than spectacle-oriented

Because the first cohort was already live before the experiment was created, the initial analytics read is observational. The May 9 live apply creates an intervention timestamp for future reads, not a clean pre-publication A/B assignment.

## Target Audience

The target audience is builders, technical operators, engineering leaders, and research-adjacent viewers who need compact operating rules for AI systems. The packaging should reward viewers looking for mechanisms, boundaries, source-of-truth surfaces, and deployment filters rather than broad AI news or generic topic summaries.

## Experiment Cohort

Initial cohort selection rules:

- include only already-published cinematic videos
- require a local cinematic upload report with a YouTube video id
- require a local caption SRT that can be used for content/rubric inspection
- prefer videos with Shorts candidate reports or Shorts upload reports for follow-through context
- favor `q3_gPM4E8yw` / "Why Most Multi-Agent AI Is a Workaround" as the anchor example
- exclude videos whose local evidence is only a legacy ledger unless they are explicitly promoted later

Initial cohort video ids:

- `q3_gPM4E8yw`
- `J9dz9_9YPQw`
- `abBHq8lwCEE`
- `bto9FNWlahY`
- `n99g7mLWQek`
- `xPLU4cISmxE`
- `Ju5UJvO4X5k`
- `slozjRp6CPg`

The generated MP4 files are not required to be present in the git worktree for this experiment. The required local evidence is the upload report, managed/recovered captions, and publication metadata.

## Packaging Rules

Each authority packet packages one already-published video around a practical claim:

- title must name the reusable operating insight without the old "Cinematic Research Brief" suffix
- description must include the claim, evidence, technical dilemma, author note, source URL, and research breakdown URL when one exists
- tags are rendered from packet tags plus `rootedlayers` and `research`
- `categoryId`, `defaultLanguage`, and `defaultAudioLanguage` are preserved from current YouTube state during snippet updates
- generated thumbnails live under `experiments/youtube-insight-authority/thumbnails/`
- top-level technical comments are posted when the packet provides `pinned_comment`
- pinning must be recorded as blocked unless a separately verified pinning surface exists

## Content Rules

The content promise is an inspectable authority claim, not a topic summary. Each packet should make one of these visible:

- mechanism: why the claim works
- boundary: what changes state, action, memory, permissions, or evaluation
- source of truth: which artifact controls intent or conflict resolution
- decision rule: what test the viewer can reuse
- evidence path: where the viewer can inspect the essay, breakdown, caption, or source artifact

## Thumbnail Rules

Thumbnails must be generated PNGs tied to the packet `thumbnail_text`. They should compress the authority claim into a short operational phrase and avoid broad hype language. The 2026-05-09 apply uploaded all eight generated thumbnails and final readback found maxres thumbnail URLs for all cohort videos.

## Cadence Governor

The local apply plan keeps the channel cadence governor recorded even though this live apply repaired already-published packaging rather than scheduling new releases:

- timezone: `Europe/Athens`
- long-form slot times: `09:00`, `13:00`
- long-form weekdays: Tuesday, Thursday
- snapshot/Short weekdays: Monday, Wednesday, Friday, Saturday, Sunday
- max per day: 1
- minimum hours between releases: 3

This experiment does not authorize new uploads or schedules.

## Approval Grant And Mutation Boundary

Standing approval covers only bounded YouTube Data API updates for already-published videos named by validated authority packets when the CLI is invoked with both `--apply` and `--apply-youtube`.

Allowed live mutations:

- update video title, description, and tags from rendered metadata
- preserve `categoryId`, `defaultLanguage`, and `defaultAudioLanguage`
- upload the generated PNG thumbnail
- post the top-level technical provocation comment
- read back video state and write `youtube_mutation_report.json`
- write final post-apply verification to `youtube_final_readback.json`

Explicitly out of scope:

- new uploads or scheduled releases
- playlist, card, end-screen, or related-video mutation
- Shorts extraction or upload
- Studio-only mutation
- claiming a pinned comment

The YouTube Data API does not expose a first-class pin-comment endpoint for this workflow. The 2026-05-09 apply posted comments but records every requested pin as `blocked_no_youtube_data_api_pin_endpoint`.

## Implementation Tickets/Subagents

Completed implementation work:

- Create central experiment source-of-truth artifacts.
- Register the cohort in `experiments/youtube-analytics/experiment_registry.yaml`.
- Add authority packet queue for eight already-published videos.
- Render local metadata and generated thumbnail assets.
- Run live bounded YouTube apply for title, description, tags, thumbnails, and top-level technical comments.
- Run final post-apply readback for all eight videos.
- Refresh analytics ledger, weekly report, dashboard source JSON, and snapshot.

Open implementation work:

- Add any future manual Studio evidence for playlist, cards, end screens, and related-video settings.
- Re-run the analytics dashboard after enough post-apply watch time accumulates.
- Decide whether Shorts follow-through should become a separate sub-cohort or stay as supporting context.

## PR Status

- Branch: `codex/insight-authority-youtube-experiment`
- Commit: `2b93703` / `Launch Insight Authority YouTube experiment`
- PR: https://github.com/petroslamb/content/pull/10
- Status: open after local validation and live YouTube apply; ready for automated merge under the standing approval grant after checks are confirmed.

## Publishing Ledger

The eight videos were already public before the experiment state was created. The live apply completed at `2026-05-09T11:43:52Z` and changed only bounded packaging fields for the existing videos.

| Published At UTC | Video ID | Applied Title | Live Apply Status |
| :--- | :--- | :--- | :--- |
| 2026-04-24T08:09:54Z | `q3_gPM4E8yw` | When Teams Split Work Too Early | applied |
| 2026-04-26T07:03:05Z | `J9dz9_9YPQw` | Memory Needs an Owner | applied |
| 2026-04-27T14:56:16Z | `abBHq8lwCEE` | The Second Worker Needs a Boundary | applied |
| 2026-04-27T14:56:16Z | `bto9FNWlahY` | Fix the Support Before the Model | applied |
| 2026-04-28T08:46:57Z | `n99g7mLWQek` | The Work Process Is the Product | applied |
| 2026-04-30T12:33:52Z | `xPLU4cISmxE` | Hardware Decides What Ships | applied |
| 2026-04-30T13:19:29Z | `Ju5UJvO4X5k` | Hardware Filters Progress | applied |
| 2026-05-04T07:52:16Z | `slozjRp6CPg` | Specs Need a Surface | applied |

## Video IDs

Canonical long-form cohort IDs:

- `q3_gPM4E8yw`: When Teams Split Work Too Early
- `J9dz9_9YPQw`: Memory Needs an Owner
- `abBHq8lwCEE`: The Second Worker Needs a Boundary
- `bto9FNWlahY`: Fix the Support Before the Model
- `n99g7mLWQek`: The Work Process Is the Product
- `xPLU4cISmxE`: Hardware Decides What Ships
- `Ju5UJvO4X5k`: Hardware Filters Progress
- `slozjRp6CPg`: Specs Need a Surface

## Shorts IDs

Derivative Shorts are supporting context, not the primary intervention cohort. Local evidence paths for Shorts candidate manifests and upload reports are tracked in `cohort.yaml`. No Shorts uploads or related-video settings were mutated by the 2026-05-09 Insight Authority apply.

Known analytics refresh Shorts references relevant to adjacent follow-through include:

- `pE_BwIGiXXk`: AI Agents Drift Into the Ditch #shorts
- `ZzMk5kv7YpI`: A Second Agent Needs a Boundary #shorts
- `_GOUwFLcERM`: The Coordination Tax Kills Agent Handoffs #shorts
- `B3mZ51x1dPk`: Hardware Kills Elegant AI Architectures #shorts
- `XTWLFL1Ha60`: FlashAttention Passed the Silicon Filter #shorts
- `FSaE54r8rPo`: FlashAttention Pays a Two-Year Ecosystem Tax #shorts
- `sakzDga10nQ`: Hardware Friction Becomes a Startup Tax #shorts

## Pinned Comments

Top-level technical comments were posted for all eight cohort videos during the live apply. Pinning is blocked because the YouTube Data API does not expose a pin-comment endpoint for this workflow.

| Video ID | Comment ID | Pin Status |
| :--- | :--- | :--- |
| `q3_gPM4E8yw` | `UgyCieAJxHovLeEB_7V4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `J9dz9_9YPQw` | `UgzRIfDLSWMTheE0Q9d4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `abBHq8lwCEE` | `UgzCuwH7gDZ9XSwl6DF4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `bto9FNWlahY` | `UgxjlNg9bPbfHma68614AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `n99g7mLWQek` | `UgxRZrrM9UCccD70W9l4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `xPLU4cISmxE` | `Ugy9zLj-FHTpxCKGEgx4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `Ju5UJvO4X5k` | `Ugzx3wKjIr7z6zLxxxx4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `slozjRp6CPg` | `UgyNDcCu0v2sGzTnyiR4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |

## Studio Verification

API verification artifacts:

- `youtube_mutation_report.json` reports `applied: true`, `youtube_mutations: true`, eight applied items, eight uploaded thumbnails, and eight posted comments.
- `youtube_final_readback.json` passed title, description, tag, and technical comment checks for all eight videos.
- Final readback found each video public and processed.
- Final readback found maxres thumbnail URLs for all eight videos.
- Comment pinning remains blocked by the YouTube Data API limitation.

Manual Studio verification remains pending for Studio-only surfaces such as playlist placement, cards, end screens, and related-video settings.

## Analytics Baseline

Analytics refresh completed after the live apply:

- metrics ledger: `experiments/youtube-analytics/metrics_ledger.json`
- metrics ledger created: `2026-05-09T11:45:30Z`
- analytics end date: `2026-05-08`
- metrics ledger records: 252 videos
- reporting API sync: 87 reports merged, 232 videos updated
- weekly report JSON: `experiments/youtube-analytics/weekly_reports/2026-05-09.json`
- weekly report Markdown: `experiments/youtube-analytics/weekly_reports/2026-05-09.md`
- dashboard snapshot: `experiments/youtube-analytics/snapshots/2026-05-09T11-45-59Z.json`
- summary counts: `scale` 0, `funnel_winner` 0, `clip_more` 0, `retitle` 22, `hook_problem` 3, `remaster` 3, `ignore` 226

Initial recommendations still include some newly applied cohort videos in `retitle` or `hook_problem` buckets because the analytics window ends on 2026-05-08, before the 2026-05-09 apply could influence behavior.

## Evaluation Rubric

Manual rubric dimensions:

- claim specificity
- mechanism clarity
- authority surface
- evidence traceability
- practical decision rule
- title/transcript promise fit
- funnel intent

Primary dashboard metric:

- `averageViewPercentage`

Secondary metrics:

- `views_per_day`
- `videoThumbnailImpressionsClickRate`, only when thumbnail impressions are sufficient
- `related_video_traffic_views`
- known downstream clicks from cards, related-video clicks, or end screens when available
- `subscribersGained`
- Shorts follow-through where a cinematic has derivative Shorts

Decision rules:

- Scale when at least six cohort videos are found in the analytics ledger and the cohort or a coherent subgroup beats the current cinematic median on average viewed percentage, with at least one downstream funnel or subscriber signal.
- Repair when retention is healthy but CTR, title specificity, or funnel state is weak.
- Pause when cohort coverage is missing, target metrics are unavailable, or the manual rubric shows the cohort is too mixed.

## Weekly Checkpoints

- 2026-05-09: created experiment state, registered dashboard cohort, ran live YouTube apply, completed final readback, refreshed analytics baseline.
- Next weekly checkpoint: re-run analytics after a full post-apply window and compare cohort videos against cinematic median and their own pre-apply recommendations.
- Manual checkpoint: add Studio-only verification if playlist, card, end-screen, or related-video surfaces are checked outside the Data API workflow.

## Blockers/Resolutions

- Blocker: comment pinning requested by packet language.
  Resolution: posted top-level comments and recorded `blocked_no_youtube_data_api_pin_endpoint`; do not claim pins.
- Blocker: first analytics window ends before the apply timestamp.
  Resolution: treat 2026-05-09 analytics as baseline/readiness, not post-intervention effect.
- Blocker: Studio-only surfaces are outside the allowed mutation boundary.
  Resolution: leave playlist/card/end-screen/related-video verification pending manual Studio review.
- Blocker: initial cohort was already live before experiment creation.
  Resolution: label the first read observational and use the 2026-05-09 apply timestamp for future intervention analysis.
