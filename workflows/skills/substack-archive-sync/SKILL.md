---
name: substack-archive-sync
description: Use when Codex needs to refresh the tracked public Substack archive, validate the Eleventy mirror, troubleshoot sync or deploy failures, or follow the repo's documented manual-import fallback for publication_strategy_and_archive/.
---

# Substack Archive Sync

Use this skill for the canonical public Substack pipeline in `publication_strategy_and_archive/`. Prefer the repo scripts in `scripts/` over ad hoc scraping, manual metadata edits, or direct mirror edits.

## Working Rules

1. Run from the repo root with the repo-local environment: `.venv/bin/python ...` and `npm run ...`.
2. Treat `scripts/sync_substack_archive.py` as the canonical archive refresh entrypoint.
3. After any archive mutation, validate the mirror before concluding the task.
4. If `/feed` is blocked or CI is failing with a 403, switch to the manual-import fallback instead of repeatedly rerunning a broken sync.
5. Keep `publication_strategy_and_archive/substack_archive/metadata.json`, localized assets, and the README publication table in sync.

## Core Paths

### Refresh The Archive

Normal refresh:

```bash
npm run sync:substack
```

Or run the underlying script directly with a machine-readable summary:

```bash
.venv/bin/python scripts/sync_substack_archive.py \
  --summary-path /tmp/substack-sync-summary.json
```

### Validate The Mirror

Run the built-in validation path after syncs or manual imports:

```bash
npm run build:mirror
npm run check:mirror
```

Also check the GitHub Pages subpath mode when troubleshooting deployment issues:

```bash
ELEVENTY_PATH_PREFIX=/content/ MIRROR_SITE_URL=https://petroslamb.github.io npm run check:mirror
```

### Inspect Failures

Use the lower-level checks when you need to isolate the failure:

- `scripts/check_mirror.py`: validates metadata, asset references, README generation, and built-link integrity.
- `scripts/e2e_mirror_smoke.py`: serves `_site/` locally and confirms homepage, archive, post, and feed routes.

### Manual Fallback

Use the documented manual-import path when feed discovery or the GitHub workflow is blocked. The manual fallback should create canonical slug files that future sync runs can overwrite cleanly, not duplicate shadow entries.

## Reference Map

- `../../../workflows/substack-archive-sync/README.md`: tracked canonical archive refresh, validation, and manual-import workflow.
- `../../../publication_strategy_and_archive/README.md`: tracked archive-system orientation.
- `references/workflow.md`: command inventory, validation flow, and manual-import checklist.
- `references/rollout-lessons.md`: feed 403 behavior, prefix-safe mirror checks, workflow cadence, and environment constraints.
