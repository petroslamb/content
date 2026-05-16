# Insight Authority Release Ledger

This ledger tracks experiment state changes, apply-mode readiness, and verification notes. It is not a replacement for the YouTube channel mutation report; any channel mutation performed by this experiment must be explicit, bounded to already-published videos, and recorded through the `--apply --apply-youtube` report.

## State Changes

| Date | Event | Scope | Evidence | Result |
| :--- | :--- | :--- | :--- | :--- |
| 2026-05-09 | Created central experiment state | `insight_authority_cinematic` | `SPEC.md`, `manifest.yaml`, `cohort.yaml`, `evaluation_rubric.yaml`, `studio_verification.yaml` | Initial read-only cohort created; no channel mutations |
| 2026-05-09 | Registered analytics dashboard cohort | 8 completed cinematic videos | `experiments/youtube-analytics/experiment_registry.yaml` | Dashboard can track cohort once analytics ledger is refreshed |
| 2026-05-09 | Enabled explicit YouTube apply posture | Already-published videos with validated authority packets | `scripts/insight_authority_experiment.py`, `authority_packets.yaml`, `SPEC.md`, `manifest.yaml`, `studio_verification.yaml` | CLI can update title, description, tags, generated thumbnail, and top-level technical comment under `--apply --apply-youtube`; no real channel mutation was run in this change |
| 2026-05-09 | Live YouTube apply completed | 8 Insight Authority cohort videos | `youtube_mutation_report.json` created at `2026-05-09T11:43:52Z` | Applied titles, descriptions, tags, thumbnails, and top-level technical comments; pinning recorded as blocked by no YouTube Data API pin endpoint |
| 2026-05-09 | Final post-apply readback passed | 8 Insight Authority cohort videos | `youtube_final_readback.json` created at `2026-05-09T11:46:45Z` | All title, description, tag, and technical comment checks passed; all videos public/processed with maxres thumbnail URLs |
| 2026-05-09 | Analytics baseline refreshed | YouTube analytics dashboard and ledger | `metrics_ledger.json`, `weekly_reports/2026-05-09.md`, `weekly_reports/2026-05-09.json`, `snapshots/2026-05-09T11-45-59Z.json` | Metrics ledger has 252 video records; reporting API sync merged 87 reports and updated 232 videos; weekly report/dashboard/snapshot written |
| 2026-05-16 | Live packaging repair applied | 5 `retitle` cohort videos, with full 8-video packet readback | `authority_packets.yaml`, `youtube_mutation_report.json`, `youtube_final_readback.json`, `SPEC.md`, `weekly_reports/2026-05-16.json` | Repaired titles, description leads, and thumbnail text for `q3_gPM4E8yw`, `J9dz9_9YPQw`, `n99g7mLWQek`, `xPLU4cISmxE`, `Ju5UJvO4X5k`; Data API apply and final readback passed for 8/8 packeted videos |
| 2026-05-16 | Expanded repair batch applied | 5 additional high-impression cinematic videos | `draft_repair_packets_2026-05-16.yaml`, `draft_repair_2026-05-16/youtube_mutation_report.json`, `draft_repair_2026-05-16/youtube_final_readback.json`, `channel_recovery_plan_2026-05-16.md` | Removed weak wrapper-style titles and uploaded regenerated thumbnails for `gcsTDFRynyw`, `vCpW8dYfeEY`, `NIJ92a65SxM`, `Vx7HwtBwo_c`, `chr4R-fSZUY`; final API readback passed for 5/5 |

## Initial Cohort Release Record

These videos were already published before the experiment state was created. The experiment begins as an observational tracking layer.

| Published At UTC | Video ID | Title | Local Evidence |
| :--- | :--- | :--- | :--- |
| 2026-04-24T08:09:54Z | `q3_gPM4E8yw` | Why Most Multi-Agent AI Is a Workaround | `publications/illusion-of-swarm/artifacts/video/illusion_of_swarm_cinematic_upload_report.json` |
| 2026-04-26T07:03:05Z | `J9dz9_9YPQw` | Why Agent Memory Needs Authority | `publications/autonomous-agents/essays/memory/artifacts/video/operating_agents_memory_cinematic_upload_report.json` |
| 2026-04-27T14:56:16Z | `abBHq8lwCEE` | When the Second Agent Actually Buys a Boundary | `publications/autonomous-agents/essays/multi-agent/artifacts/video/operating_agents_multi_agent_cinematic_upload_report.json` |
| 2026-04-27T14:56:16Z | `bto9FNWlahY` | Diagnose the Scaffold Before You Shop the Model | `publications/autonomous-agents/essays/reasoning/artifacts/video/operating_agents_reasoning_cinematic_upload_report.json` |
| 2026-04-28T08:46:57Z | `n99g7mLWQek` | When the Workflow Becomes the Object | `publications/autonomous-agents/essays/optimization/artifacts/video/operating_agents_optimization_cinematic_upload_report.json` |
| 2026-04-30T12:33:52Z | `xPLU4cISmxE` | Why Hardware Friction Decides What Ships in AI | `publications/hardware-friction/artifacts/video/hardware_friction_map_cinematic_upload_report.json` |
| 2026-04-30T13:19:29Z | `Ju5UJvO4X5k` | Why AI Architecture Progress Is Filtered by Hardware | `publications/hardware-friction/what-actually-works-the-hardware/artifacts/video/what_actually_works_hardware_cinematic_upload_report.json` |
| 2026-05-04T07:52:16Z | `slozjRp6CPg` | Why AI Coding Needs a Specification Surface | `publications/literate-workflow-programming/specification-surface-source-of-truth/artifacts/video/specification_surface_cinematic_upload_report.json` |

## Apply Readback Record

| Video ID | Applied Title | Comment ID | Pin Status |
| :--- | :--- | :--- | :--- |
| `q3_gPM4E8yw` | When Teams Split Work Too Early | `UgyCieAJxHovLeEB_7V4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `J9dz9_9YPQw` | Memory Needs an Owner | `UgzRIfDLSWMTheE0Q9d4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `abBHq8lwCEE` | The Second Worker Needs a Boundary | `UgzCuwH7gDZ9XSwl6DF4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `bto9FNWlahY` | Fix the Support Before the Model | `UgxjlNg9bPbfHma68614AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `n99g7mLWQek` | The Work Process Is the Product | `UgxRZrrM9UCccD70W9l4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `xPLU4cISmxE` | Hardware Decides What Ships | `Ugy9zLj-FHTpxCKGEgx4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `Ju5UJvO4X5k` | Hardware Filters Progress | `Ugzx3wKjIr7z6zLxxxx4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |
| `slozjRp6CPg` | Specs Need a Surface | `UgyNDcCu0v2sGzTnyiR4AaABAg` | `blocked_no_youtube_data_api_pin_endpoint` |

## Repair Readback Record

The 2026-05-16 repair kept the same top-level technical comments and blocked pin status. Material title changes:

| Video ID | Previous Title | Repair Title |
| :--- | :--- | :--- |
| `q3_gPM4E8yw` | When Teams Split Work Too Early | Boundary First, Then More Workers |
| `J9dz9_9YPQw` | Memory Needs an Owner | When Memory Has No Owner |
| `n99g7mLWQek` | The Work Process Is the Product | Stop Tuning Instructions; Test the Process |
| `xPLU4cISmxE` | Hardware Decides What Ships | Hardware Friction Decides What Ships |
| `Ju5UJvO4X5k` | Hardware Filters Progress | Hardware Fit Filters Progress |

## Expanded Repair Readback Record

The expanded repair promoted the first five channel-recovery candidates after user authorization to take channel-improvement actions.

| Video ID | Previous Title | Repair Title |
| :--- | :--- | :--- |
| `gcsTDFRynyw` | The AI Autonomy Tax \| A Cinematic Research Brief | Autonomy Breaks at the Control Layer |
| `vCpW8dYfeEY` | The AI Attack Surface Is the Agent's Architecture \| A Cinematic Research Brief | The Attack Surface Is the Architecture |
| `NIJ92a65SxM` | Why Reliable Agents Start with Action Boundaries \| A Cinematic Research Brief | Action Needs a Contract |
| `Vx7HwtBwo_c` | The Scaffold Failed First \| A Cinematic Research Brief | The Support Failed Before the Model |
| `chr4R-fSZUY` | When LLMs Need a REPL for Their Own Thoughts \| A Cinematic Research Brief | Models Need a REPL for Thought |

## Analytics Baseline Record

- Metrics ledger created: `2026-05-09T11:45:30Z`
- Analytics end date: `2026-05-08`
- Metrics ledger records: 252
- Reporting API sync: 87 reports, 232 videos updated, merged at `2026-05-09T11:45:52Z`
- Weekly report Markdown: `experiments/youtube-analytics/weekly_reports/2026-05-09.md`
- Weekly report JSON: `experiments/youtube-analytics/weekly_reports/2026-05-09.json`
- Dashboard snapshot: `experiments/youtube-analytics/snapshots/2026-05-09T11-45-59Z.json`
- Decision counts: `scale` 0, `funnel_winner` 0, `clip_more` 0, `retitle` 22, `hook_problem` 3, `remaster` 3, `ignore` 226

## Next Read

- Refresh the YouTube analytics dashboard after a full post-apply window.
- Compare the eight applied titles and thumbnails against the 2026-05-09 baseline, not against the pre-apply cohort creation state.
- Confirm `cohort_found` for `insight_authority_cinematic` is at least 6.
- Apply `evaluation_rubric.yaml` after each dashboard refresh that changes recommendation status for a cohort video.
- Keep manual Studio verification pending for playlist, card, end-screen, and related-video surfaces unless a separate authorized check is run.
