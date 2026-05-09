---
workflow_id: youtube_insight_authority
workflow_kind: module
stability: experimental
workflow_group: operations
runner_mode: guided
default_skill: youtube-data-api
launch_templates: []
required_context:
  - source-of-truth insight authority spec for the target package
  - package-local authority packet with video promise, evidence, claims, and release intent
  - verified local video, captions, thumbnail, packaging, and engagement assets
  - authenticated YouTube channel access and analytics readback surfaces
expected_outputs:
  - approved authority packet and packaging packet
  - verified upload or scheduling plan with cadence governor decision
  - pinned comment and engagement plan
  - analytics tracking row and readback cadence
  - standing approval grant record or blocked-state note
done_when:
  - the target video is locally prepared, channel mutation is either completed under the standing approval grant or held at an explicit stop condition, and analytics tracking is queued
approval_gate: standing_approval_with_release_readiness_and_channel_mutation_stop_conditions
---

# YouTube Insight Authority

This is an experimental end-to-end YouTube workflow for turning a package insight into a channel-ready upload with explicit authority, packaging, cadence, engagement, and analytics governance.

Use it when the task is not just rendering a video or running a narrow channel operation, but carrying a YouTube asset from source specification through upload/scheduling, pinned comment, and performance tracking.

This workflow acknowledges the user's standing approval for bounded YouTube channel execution. That approval is an operating grant, not permission to ignore failed preconditions. Stop before mutation when credentials, quota, required assets, dry-run verification, API/Studio tools, or analytics tracking cannot be verified.

## Phase 2.8 Lifecycle State

State: `contracted`. This workflow has a governed `workflow.yaml` with `stability: experimental`, so it can be invoked explicitly through `content-agent`; it is not a canonical/default route and has no promotion proof from this note.

## Source-Of-Truth Order

The source-of-truth hierarchy for this workflow is:

1. the package-local Insight Authority spec
2. the authority packet generated from that spec
3. the packaging packet generated from the authority packet
4. the upload, engagement, and analytics records generated from those packets

Do not let a title, thumbnail idea, short-term analytics hunch, or upload script default overrule the source spec. If the spec and packet disagree, stop and repair the packet before continuing.

## Authority Packet

Each run needs an authority packet before packaging or upload. It records:

- insight promise: what the viewer should understand after watching
- source spine: package draft, evidence surface, caption source, slide/video master, and references used
- claim permissions: what the video may claim, must caveat, and must not imply
- audience and format: longform, cinematic, TL;DR, Short, or remaster
- release intent: why this asset should exist now
- approval state: approved, revise, or blocked

The authority packet is the handoff between editorial evidence and YouTube packaging. A polished video with an unapproved authority packet remains blocked.

## Packaging Rules

Packaging must be derived from the authority packet:

- title states the viewer problem or concrete insight, not the internal essay frame alone
- first two description lines carry the promise and primary destination link
- chapters exist for longform unless the format makes chapters meaningless
- playlists, tags, category, language, and visibility are named before upload
- Shorts descriptions name the related longform or canonical essay path when available
- dry-run output must match the packet before any `--apply` or Studio write

Never patch packaging directly in YouTube Studio and leave the local packet stale. If the channel is changed manually, record the readback into the packet or handoff note.

## Thumbnail Rules

The thumbnail is packaging evidence, not decoration. It must:

- match the exact video promise and not introduce a stronger claim than the authority packet allows
- be readable at small sizes with one dominant visual idea
- avoid generic stock imagery, unreadable text walls, and bait-and-switch framing
- use a stable package-local source path and export path
- pass the current YouTube Studio/API constraints before upload
- be logged with the title as one tested packaging pair

If no suitable thumbnail asset exists, stop. Do not upload a weak default thumbnail under the standing approval grant unless the packet explicitly chooses that as the test.

## Cadence Governor

The cadence governor decides whether the channel should mutate now, schedule later, or hold:

- respect already scheduled uploads and Shorts from the cinematic, Operating Agents, and package workflows
- avoid more than one longform-style release per channel day unless the packet explicitly approves a burst
- avoid more than one Short from the same source video per day
- preserve enough spacing for analytics attribution before retitles, thumbnail swaps, or remasters
- record the publish slot, timezone, related queued assets, and reason for the decision

If cadence cannot be determined from local records and YouTube readback, stop before upload or scheduling.

## Engagement And Pinned Comment

Every upload plan needs an engagement packet:

- pinned or first channel comment text, unless the packet records why no comment should be posted
- 3 to 6 curated references or companion links when the video is evidence-heavy
- one sentence per reference explaining why it matters to the video
- no full bibliography dump, repetitive cross-video comment scaffold, or engagement bait
- reply policy for substantive questions, corrections, or objections
- Studio/API readback proving the comment was posted and pinned when that action is in scope

If the tool can upload the video but cannot safely create or verify the pinned comment, record the video state and stop the engagement step. Do not invent readback.

## Analytics Tracking

Before considering the run complete, create or update the analytics tracking record with:

- package path, video format, title, thumbnail path, playlist, publish time, and video ID
- authority packet hash and packaging packet hash
- cadence governor decision
- pinned-comment state and engagement notes
- checkpoints for `+24h`, `+72h`, `+7d`, and `+30d`
- fields needed by the YouTube analytics decision loop, including retention, CTR, traffic source, subscriber, related-video, card, end-screen, and manual Studio observations when available

Analytics refreshes are readback and report work. They must not retitle, swap thumbnails, unlist, upload, pin comments, or mutate playlists by themselves.

## Approval Grant

The user has given standing approval for this workflow to perform bounded YouTube channel execution when all of the following are true:

- the authority packet is approved
- the packaging packet is approved
- the cadence governor permits the slot
- dry-run output matches the approved packet
- credentials and quota are healthy
- all required assets exist and pass verification
- the tool can write and read back the channel state
- analytics tracking can be recorded locally

Standing approval covers the ordinary upload, scheduling, playlist placement, related-video metadata, and pinned-comment steps described by the approved packets. It does not cover improvising missing assets, bypassing failed tools, ignoring quota, changing unrelated channel state, or mutating a different video than the packet names.

## Stop Conditions

Stop and record a blocked-state note when any of these occur:

- YouTube OAuth credentials are missing, expired, or cannot be verified
- API quota blocks a required write or readback
- the verified MP4, caption file, thumbnail, title, description, chapters, or comment text is missing
- a local file is zero bytes, stale, or outside the packet's declared path
- the upload, playlist, comment, pin, scheduling, related-video, or analytics tool fails
- Studio/API readback disagrees with the intended state
- cadence conflicts with existing scheduled releases
- the package authority packet or packaging packet is unapproved
- local validation fails

The fallback is a precise handoff note with the command that failed, the target video/package, the expected state, and the next safe verification step.

## Related Surfaces

- [`../youtube-production/README.md`](../youtube-production/README.md): local MP4 production and verification.
- [`../youtube-channel-ops/README.md`](../youtube-channel-ops/README.md): YouTube auth, upload, captions, playlist, comments, and analytics operations.
- [`../youtube-cinematic-rollout/README.md`](../youtube-cinematic-rollout/README.md): cinematic backlog and Shorts cadence constraints.
- [`../youtube-series-operating-agents/README.md`](../youtube-series-operating-agents/README.md): Operating Agents series-specific channel work.
- [`../../experiments/youtube-analytics/README.md`](../../experiments/youtube-analytics/README.md): analytics dashboard and decision loop.
