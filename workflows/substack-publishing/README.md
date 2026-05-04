---
workflow_id: substack_publishing
workflow_kind: stage
stage_binding: substack_publishing
stability: canonical
workflow_group: release
runner_mode: hybrid
launch_mode: external_mutation
default_skill: null
launch_templates:
  - ".venv/bin/python scripts/sync_markdown_post_to_substack.py --publication-url {substack_url} --post-id {substack_post_id} --markdown {markdown_path}"
required_context:
  - config.markdown_path
  - config.substack_url
  - config.substack_post_id
  - release gate verdict or explicit publication approval
  - existing Substack draft or publish target
expected_outputs:
  - synced Substack draft or published post
  - publication-ready markdown rendered in the target Substack post
done_when:
  - the synced post has been reviewed and explicitly approved as complete
approval_gate: required_before_live_publish
---

# Substack Publishing

This is the canonical tracked workflow for taking a finished essay package to Substack.

## Purpose

Use this when an article is ready enough to become a public post and the package already contains:

- the canonical live essay
- final or near-final references
- any relevant media placements with stable filenames and deliberate insertion points
- completed polish work from [`../article-polish/README.md`](../article-polish/README.md)
- a release-ready verdict from [`../release-gate/README.md`](../release-gate/README.md), or explicit user approval to proceed despite a known blocker

## Canonical Publishing Expectations

When appropriate, the published essay should include:

- a `#### Video TL;DR` heading near the top if a relevant video artifact exists
- inline author-year citations in the body where sources carry claims
- a precise reference section at the end
- cited paper entries formatted as linked h4 headings to the arXiv paper or canonical source
- source-contribution paragraphs for references doing argumentative work
- short orientation text for references when useful
- appendices when they genuinely help
- links back to the upstream repo for companions, datasets, or supporting material that do not fit inside the main essay

If a draft still reads like repo documentation rather than a public essay, simplify the publication surface before publishing. In practice that often means trimming documentation furniture, overly mechanical endings, or reference machinery that belongs in the repo more than in email or Substack.

## Evidence-Backed Defaults

- Keep already-published links Substack-first when republishing or cross-linking a live series.
- If the post belongs in the tracked public archive, the publishing task is not done until the archive refresh and mirror validation pass.
- If archive sync is blocked and a manual import is required, use the canonical slug and replacement path so the future sync can overwrite cleanly instead of creating duplicate pages.

## Standard Flow

1. confirm the live draft is the canonical publish target
2. confirm article polish is complete, including:
   - final image naming
   - intentional image placement
   - any transcript-driven rehumanization pass
   - body author-year citations for cited claims
   - linked h4 reference headings with source-contribution paragraphs
3. run or inspect the release gate verdict before any external mutation
4. insert the `Video TL;DR` block if a video artifact exists and the post format supports it
5. publish with `python-substack` or a package-specific publishing helper
6. refresh the tracked public archive if the post is part of the Substack archive system

## Existing-Draft API Sync

When a post already exists as a Substack draft and the goal is to replace its body from the repo's canonical markdown, use the generic single-post sync script instead of editing in the browser.

Recommended path:

```bash
.venv/bin/python scripts/sync_markdown_post_to_substack.py \
  --publication-url https://lambpetros.substack.com \
  --post-id <DRAFT_ID> \
  --markdown publications/<package>/<live-draft>.md \
  --chrome-debug-url http://127.0.0.1:9222
```

This path:

- reuses an already logged-in Chrome session over CDP to extract the Substack cookie string without browser interaction
- uploads standalone markdown images to Substack
- preserves an existing `video` node or injects one from `draft_video_upload_id`
- recognizes a `#### Video TL;DR` heading in the markdown and places the uploaded draft video directly under it
- leaves the post as a draft unless you explicitly pass `--publish`

For the video block, keep this pattern in the canonical markdown:

```md
#### Video TL;DR

[Descriptive video label](artifacts/video/example.mp4)
```

The local `.mp4` link is a placement marker for the sync script. The script does not upload the video file itself. It expects the target Substack draft already to have an uploaded video asset, exposed as `draft_video_upload_id`, and then builds the correct embedded `video` node in the draft body.

## Package-Specific Exceptions

- Some series or packages have specialized publishing helpers, such as the Operating Agents Substack sync path.
- Use those only when the task is explicitly about that series. Do not generalize series-specific automation into the generic publishing path.

## Archive Follow-Through

If the published post belongs in the repo’s tracked public archive:

1. refresh the archive
2. validate the mirror
3. confirm the publication maps back to the correct package or umbrella package
4. if repo links changed because the package moved, use the migration manifest in [`../../publication_strategy_and_archive/link_migration_manifest.yaml`](../../publication_strategy_and_archive/link_migration_manifest.yaml) to plan the later live Substack patch pass

## Related Docs

- [`../essay-iteration/README.md`](../essay-iteration/README.md)
- [`../notebooklm-artifacts/README.md`](../notebooklm-artifacts/README.md)
- [`../article-polish/README.md`](../article-polish/README.md)
- [`../release-gate/README.md`](../release-gate/README.md)
- [`../../publication_strategy_and_archive/README.md`](../../publication_strategy_and_archive/README.md)
