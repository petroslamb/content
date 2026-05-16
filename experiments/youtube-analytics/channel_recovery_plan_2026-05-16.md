# YouTube Channel Recovery Plan - 2026-05-16

## Current Read

- Source report: `experiments/youtube-analytics/weekly_reports/2026-05-16.json`
- Analytics end date: `2026-05-15`
- Channel readback during repair sprint: `Rooted Layers | AI Systems Grounded in Research`, 67 subscribers, 231 videos
- Immediate live repair completed under the Insight Authority boundary for five cohort videos; see `experiments/youtube-insight-authority/release_ledger.md`

## What Changed Live

The first action was not to keep diagnosing. The five Insight Authority cohort videos already classified as `retitle` and backed by authority packets were repaired through the YouTube Data API:

| Video ID | Previous Title | Repair Title |
| :--- | :--- | :--- |
| `q3_gPM4E8yw` | When Teams Split Work Too Early | Boundary First, Then More Workers |
| `J9dz9_9YPQw` | Memory Needs an Owner | When Memory Has No Owner |
| `n99g7mLWQek` | The Work Process Is the Product | Stop Tuning Instructions; Test the Process |
| `xPLU4cISmxE` | Hardware Decides What Ships | Hardware Friction Decides What Ships |
| `Ju5UJvO4X5k` | Hardware Filters Progress | Hardware Fit Filters Progress |

All five also received regenerated 1280x720 authority thumbnails. The full 8-video packet apply/readback passed title, description, tag, thumbnail, and technical-comment checks.

## Next Repair Queue

These videos have enough impression evidence to justify packaging review, but they are not safe to retitle directly until an authority packet or the owning cinematic rollout source is updated. Several still carry the older `A Cinematic Research Brief` suffix, which may be part of the rollout naming convention rather than accidental metadata.

Draft packets for the first five candidates live at `experiments/youtube-insight-authority/draft_repair_packets_2026-05-16.yaml`. They validate through `scripts/insight_authority_experiment.py` but are marked draft-only and must be promoted before any live apply.

| Priority | Video ID | Current Title | Package | Views | Impressions | CTR | Avg View % | Recommended Move |
| :--- | :--- | :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| 1 | `gcsTDFRynyw` | The AI Autonomy Tax \| A Cinematic Research Brief | `autonomy-tax` | 30 | 2361 | 0.59 | 40.05 | Create authority packet; test a practical-tax title without the wrapper suffix if rollout owner agrees |
| 2 | `vCpW8dYfeEY` | The AI Attack Surface Is the Agent's Architecture \| A Cinematic Research Brief | `autonomous-agents/essays/safety` | 28 | 2411 | 0.46 | 22.09 | Create safety authority packet; preserve card/end-screen context already recorded in rollout ledger |
| 3 | `NIJ92a65SxM` | Why Reliable Agents Start with Action Boundaries \| A Cinematic Research Brief | `autonomous-agents/essays/action` | 7 | 2143 | 0.28 | 18.75 | Review action-boundary thumbnail/title before removing suffix; low retention makes this riskier |
| 4 | `Vx7HwtBwo_c` | The Scaffold Failed First \| A Cinematic Research Brief | `autonomous-agents/essays/reasoning` | 4 | 1176 | 0.00 | 53.54 | Treat as high-retention/low-CTR candidate; verify sample before live mutation |
| 5 | `chr4R-fSZUY` | When LLMs Need a REPL for Their Own Thoughts \| A Cinematic Research Brief | `programmable-thinking` | 11 | 1606 | 0.37 | 15.72 | Rewrite away from jargon only after checking source packet and related-video chain |
| 6 | `bhoiLFJadAA` | The Model Kept the Facts. It Dropped the Wiring \| A Cinematic Research Brief | `binding-gap` | 30 | 1058 | 1.70 | 23.37 | Lower priority: CTR is weak but not as broken as the first five |
| 7 | `9C-N9gaJjN4` | Why Meta Bought a Broken AI Social Network \| A Cinematic Research Brief | `moltbook-phenomenon` | 18 | 549 | 1.64 | 10.85 | Do not repair first; retention is weak |

## Operating Rule

- Mutate only videos with a current local authority packet or owning workflow manifest update.
- Do not remove the cinematic suffix from rollout-owned videos until the rollout naming convention is explicitly changed.
- Prioritize title/thumbnail repairs where impressions are above 1000 and CTR is below 1 percent.
- Treat retention above 30 percent as salvageable; treat low-retention videos as concept or hook problems before title changes.
- Re-run the dashboard after YouTube Analytics includes at least three post-repair days for the 2026-05-16 batch.
