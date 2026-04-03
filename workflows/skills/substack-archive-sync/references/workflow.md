# Substack Archive Sync Workflow

Use this file for the concrete command path behind the archive and mirror workflow.

## Canonical Commands

Refresh the archive and write a JSON summary:

```bash
.venv/bin/python scripts/sync_substack_archive.py \
  --summary-path /tmp/substack-sync-summary.json
```

Build and validate the mirror:

```bash
npm run build:mirror
npm run check:mirror
```

Validate the GitHub Pages subpath mode explicitly:

```bash
ELEVENTY_PATH_PREFIX=/content/ MIRROR_SITE_URL=https://petroslamb.github.io npm run check:mirror
```

## Script Map

- `scripts/sync_substack_archive.py`: discovers posts, fetches `/api/v1/posts/<slug>`, localizes assets, writes markdown and HTML snapshots, updates `metadata.json`, and rewrites the generated README publication map.
- `scripts/archive_utils.py`: shared paths plus `post_map.yaml` and README-table helpers.
- `scripts/check_mirror.py`: validates metadata keys, archive-file presence, localized asset references, README generation, and built-site internal links.
- `scripts/e2e_mirror_smoke.py`: serves the built mirror locally and checks `/`, `/archive/`, `/posts/<slug>/`, and `/feed.xml`.

## Manual Import Fallback

Use the manual path when sync is blocked by feed or workflow failures.

Required archive artifacts per post:

1. `publication_strategy_and_archive/substack_archive/YYYY-MM-DD_<slug>.md`
2. `publication_strategy_and_archive/substack_archive/YYYY-MM-DD_<slug>.html`
3. any referenced files under `publication_strategy_and_archive/substack_archive/assets/`
4. a `metadata.json` entry with:
   `slug`, `title`, `url`, `post_date`, `audience`, `fetched_at`, `content_hash`, `md_path`, `html_path`, `hero_image`, `mirror_enabled`

Manual imports should use the canonical slug and filename pattern so future sync runs replace them cleanly.

After manual import:

```bash
npm run build:mirror
npm run check:mirror
```

## Expected Outcome

- `publication_strategy_and_archive/substack_archive/metadata.json` stays internally consistent
- the README publication table remains generated from `post_map.yaml`
- the built mirror works at both root and `/content/`
