---
workflow_id: archive_sync
runner_mode: scripted
default_skill: substack-archive-sync
launch_templates:
  - ".venv/bin/python scripts/sync_substack_archive.py"
  - "npm run check:mirror"
required_context:
  - repo root environment with archive scripts available
  - up-to-date publication metadata or recently published post
expected_outputs:
  - refreshed tracked public archive
  - updated archive metadata and README publication map
done_when:
  - the archive refresh completes successfully and the mirror validation pass is clean
approval_gate: none
---

# Substack Archive Sync

This is the tracked canonical workflow for refreshing the public Substack archive, validating the Eleventy mirror, and handling the manual-import fallback when sync is blocked.

Use this workflow before dropping into the repo scripts or the `substack-archive-sync` skill bundle.

## Evidence-Backed Defaults

- Treat `npm run sync:substack` and `scripts/sync_substack_archive.py` as the canonical refresh path.
- After any archive mutation, validate both the normal mirror and the `/content/` prefixed GitHub Pages mode.
- If feed discovery or CI is blocked by a `403`, use the manual-import fallback instead of creating duplicate shadow entries.
- Manual imports must keep the canonical slug-based filename pattern so later sync runs overwrite them cleanly.
- The repo converged on monthly scheduled sync plus manual dispatch, not aggressive automatic polling.

## Canonical Flow

### 1. Refresh The Archive

Normal entrypoint:

```bash
npm run sync:substack
```

Lower-level script with a machine-readable summary:

```bash
.venv/bin/python scripts/sync_substack_archive.py \
  --summary-path /tmp/substack-sync-summary.json
```

### 2. Validate The Mirror

Build and validate the normal mirror:

```bash
npm run build:mirror
npm run check:mirror
```

Validate the GitHub Pages subpath mode explicitly:

```bash
ELEVENTY_PATH_PREFIX=/content/ MIRROR_SITE_URL=https://petroslamb.github.io npm run check:mirror
```

### 3. Use Manual Import Only When Sync Is Blocked

Use manual import when the feed or workflow path is blocked and a tracked archive entry still needs to be added or repaired.

Required artifacts per post:

1. `publication_strategy_and_archive/substack_archive/YYYY-MM-DD_<slug>.md`
2. `publication_strategy_and_archive/substack_archive/YYYY-MM-DD_<slug>.html`
3. localized assets under `publication_strategy_and_archive/substack_archive/assets/`
4. a `metadata.json` entry with:
   `slug`, `title`, `url`, `post_date`, `audience`, `fetched_at`, `content_hash`, `md_path`, `html_path`, `hero_image`, `mirror_enabled`

After a manual import, rerun the mirror validation path.

## Troubleshooting Defaults

- If CI behavior looks wrong before jobs even start, inspect workflow YAML syntax before debugging archive code.
- Treat `scripts/check_mirror.py` and `scripts/e2e_mirror_smoke.py` as required validation, not optional extras.
- Do not spend routine archive time untangling unrelated environment dependency conflicts if the working repo environment already runs the canonical scripts.

## Related Surfaces

- [`../../publication_strategy_and_archive/README.md`](../../publication_strategy_and_archive/README.md): archive system orientation and public mirror context.
- [`../../scripts/README.md`](../../scripts/README.md): tracked script map for refresh, validation, and smoke tests.
- [`../skills/substack-archive-sync/`](../skills/substack-archive-sync/): execution-focused skill bundle.
