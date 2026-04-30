# YouTube Reference Comments

Experimental backfill surface for curated YouTube references on channel videos.

This is intentionally separate from the active cinematic rollout and YouTube upload workflows. The goal is to test whether a lightweight references surface improves trust, saves repeat explanation work, or attracts more technically serious engagement before it is normalized into a broader workflow.

The experiment currently has two lanes:

- curated comments
- append-only description backfill

## Hypothesis

A pinned or early channel comment that lists the **3 to 6 most important references** behind a video, with **one sentence on why each mattered**, may help more than a raw bibliography dump.

The experiment should answer:

- does the comment feel useful rather than academic for normal viewers
- do technically serious viewers engage with it
- does it create a better trust signal than the current description-only pattern
- does it become repetitive enough across videos to look spammy

## Policy Posture

This experiment is low-risk if comments stay:

- on-topic for the video they are posted under
- non-repetitive across the channel
- authored as normal editorial context, not engagement bait
- limited to a small curated subset of references

Do **not** paste the full essay bibliography into comments. Do **not** mass-post near-identical comments across a large backfill wave without review. Do **not** rewrite whole YouTube descriptions for this experiment. Description edits should append a single curated paper line only.

Official YouTube policy risk is tied more to repetitive or spammy comments than to creators commenting on their own videos:

- YouTube spam policy says comments spam includes comments where the sole purpose is to drive viewers elsewhere or repeated identical comments.
- Repetitive comments can be removed.

Sources:

- [YouTube spam, deceptive practices, and scams policy](https://support.google.com/youtube/answer/2801973?hl=en)
- [YouTube Community Guidelines overview](https://support.google.com/youtube/answer/9288567?hl=en)

## Experiment Boundary

Keep comments in draft-and-review mode first.

- Draft comment text locally.
- Review a small cohort manually.
- Post only after the operator approves the wording and cadence.

Description appends are a separate lower-risk lane:

- preserve the full existing description text
- append one `Key paper:` line only
- use a curated manual map when source structures vary too much for blind extraction

If the pilot works, the stable parts can later move into `workflows/youtube-channel-ops/` or `workflows/youtube-cinematic-rollout/`.

## Files

- `pilot_manifest.yaml`: candidate videos and their source essays
- `drafts/`: generated or edited draft comments
- `notes.md`: quick pilot observations and decisions
- `description_append_manifest.yaml`: append-only backfill targets for description updates

## Suggested First Backfill Cohort

- the two most recent hardware-friction cinematic briefs
- one or two older cinematic briefs with clearer, shorter reference sections

This keeps the pilot small enough to evaluate tone and usefulness before it becomes operational default behavior.

## Draft Rule

Use this structure:

1. one lead sentence
2. 3 to 6 references
3. one sentence per reference on why it mattered to the video
4. full essay link for the complete references

Good:

- selective
- editorial
- narrative
- human-readable

Bad:

- complete bibliography dump
- raw citation formatting everywhere
- identical comment scaffold on every video
- more than one comment per video for the same purpose

## Fresh Session Handoff

The next session should:

1. review `pilot_manifest.yaml`
2. inspect the generated drafts under `drafts/`
3. treat comments as optional and description appends as the default follow-through lane
4. use `description_append_manifest.yaml` for the remaining backfill cohort
5. record outcomes in `notes.md`

Do not wire this into the main cinematic rollout yet.
