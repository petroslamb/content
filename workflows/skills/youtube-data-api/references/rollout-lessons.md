# Rollout Lessons

Use this file when the repo's YouTube scripts behave oddly or when an agent needs the reasoning behind the current workflow shape.

## End-Screen Limitation

- The YouTube Data API does not expose the modern Studio end-screen editor.
- Do not spend time trying to automate “suggested next video” tiles through the API.
- The supported fallback in this repo is description-based cross-link blocks plus playlist order maintenance.

## Manual Sort Requirement

- Playlist reordering can fail with `manualSortRequired`.
- When that happens, switch the playlist to manual sorting in YouTube Studio, then rerun the reorder script.
- Treat this as a Studio precondition, not a bug in `playlistItems.update`.

## Quota Exhaustion

- Writes can fail with `quotaExceeded`.
- Local caption verification, OCR review, cue-sheet generation, and render steps can continue without API quota.
- Prefer `yt-dlp` subtitle recovery during quota exhaustion, then resume the write steps after the quota window resets.

## Why The Skill Owns The Workflow Docs

- A prior repo cleanup moved the Operating Agents video workflow out of the essay folders and into the YouTube playbook because it was generic tooling, not essay-specific narrative content.
- Keep cross-series YouTube operational knowledge under the YouTube skill instead of scattering it across article or chapter folders.
