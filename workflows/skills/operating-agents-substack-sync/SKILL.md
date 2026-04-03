---
name: operating-agents-substack-sync
description: Use when Codex needs to republish the Operating Agents preface or essay markdown to live Substack, preserve embedded video blocks, keep published links Substack-first, and refresh the local archive after publication.
---

# Operating Agents Substack Sync

Use this skill only when the user wants live Substack posts changed. This is the repo-specific publishing path for the Operating Agents preface plus the six essay posts under `autonomous-agent-blueprint/essays/`.

## Working Rules

1. Run from the repo root with `.venv/bin/python`.
2. Require `/tmp/substack_cookie_string.txt` before attempting a live sync.
3. Treat `scripts/sync_operating_agents_substack.py` as a mutating whole-series sync. It currently republishes every post in `POST_SPECS`.
4. Preserve the existing `Video TL;DR` embed block. The sync script is designed to keep that node when republishing.
5. After a live sync, rerun `npm run sync:substack` so the tracked archive snapshots match the live posts.
6. Prefer Substack URLs for already-published essays, not GitHub blob links.

## Core Path

Run the live republish from the repo root:

```bash
PYTHONUNBUFFERED=1 .venv/bin/python scripts/sync_operating_agents_substack.py
```

Then refresh the tracked public archive:

```bash
npm run sync:substack
```

## What The Script Already Handles

- rewrites repo-relative links for published Operating Agents markdown into live Substack URLs
- preserves the existing embedded video node when the markdown still includes the `#### Video TL;DR` anchor
- retries rate-limited Substack API calls with exponential backoff
- republishes the full preface-to-optimization set from the repo sources

## Reference Map

- `../../../workflows/substack-publishing/README.md`: tracked publishing defaults for article structure, `Video TL;DR`, and reference sections.
- `references/workflow.md`: prerequisites, post list, command sequence, and follow-up archive refresh.
- `references/rollout-lessons.md`: 429 handling, Substack-first link rewrites, and CI/archive coordination notes.
