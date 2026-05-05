# Fresh Session Handoff

## Goal

Pilot YouTube references surfaces without embedding the behavior into the main cinematic or long-form workflows yet.

## What Already Exists

- experiment README:
  [`README.md`](README.md)
- pilot manifest:
  [`pilot_manifest.yaml`](pilot_manifest.yaml)
- draft builder:
  [`../../scripts/build_youtube_reference_comment_draft.py`](../../scripts/build_youtube_reference_comment_draft.py)
- description appender:
  [`../../scripts/append_key_paper_to_youtube_descriptions.py`](../../scripts/append_key_paper_to_youtube_descriptions.py)
- description append manifest:
  [`description_append_manifest.yaml`](description_append_manifest.yaml)
- first sample drafts:
  [`drafts/hardware_friction_map_comment.md`](drafts/hardware_friction_map_comment.md)
  [`drafts/what_actually_works_hardware_comment.md`](drafts/what_actually_works_hardware_comment.md)
  [`drafts/illusion_of_swarm_comment.md`](drafts/illusion_of_swarm_comment.md)

## Current Assessment

- `what_actually_works_hardware` draft is close to usable.
- `hardware_friction_map` needed manual wording because its source essay only has a compact selected-references appendix.
- `illusion_of_swarm` now has manually drafted cinematic and long-form variants and is one of the cleanest pilots.
- `moltbook_phenomenon` now has manually drafted cinematic and long-form variants and is the best test of a reporting-driven version of this idea.
- The first four public comment pilots were posted, but operator feedback was negative enough that the default backfill direction should now shift toward append-only description edits instead of more comments.

## Recommended Next Steps

1. Treat comments as paused unless the operator explicitly wants another pilot.
2. Use the description append manifest for the remaining backfill cohort, preserving all existing description text and appending only one curated `Key paper:` line.
3. Compare whether description appends feel better than comments before normalizing anything into the main rollout.
4. Record results in:
   [`notes.md`](notes.md)

## Policy Posture

Do not treat creator comments as risky by default. The risk is repetitive or spammy behavior, not commenting on your own videos once with relevant context.

Use this practical rule:

- safe: one tailored, on-topic references comment per video
- risky: near-identical comments pasted across many videos in a short burst

Official references:

- [YouTube spam, deceptive practices, and scams policy](https://support.google.com/youtube/answer/2801973?hl=en)
- [YouTube Community Guidelines overview](https://support.google.com/youtube/answer/9288567?hl=en)
