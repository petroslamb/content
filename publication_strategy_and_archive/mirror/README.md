# Mirror

This folder contains the 11ty source for the public GitHub Pages mirror of Rooted Layers. Its homepage is the selective portfolio entrance; the archive routes remain the complete historical mirror.

The site is a mirror, not the canonical publication endpoint. Substack remains canonical. The curated entrance highlights no more than four flagship and four supporting essays, while the complete archive keeps navigation, repository links, research-folder context, and archive provenance on top of every downloaded public post snapshot.

## Inputs

The mirror is built from four upstream sources:

- [`../substack_archive/metadata.json`](../substack_archive/metadata.json): generated archive manifest
- [`../post_map.yaml`](../post_map.yaml): hand-edited curation layer
- [`../portfolio/portfolio_manifest.yaml`](../portfolio/portfolio_manifest.yaml): governed portfolio selections, order, annotations, disclosure, and professional-profile target
- [`../editorial_atlas/atlas_data.json`](../editorial_atlas/atlas_data.json): generated editorial atlas data for the public route
- `../editorial_atlas/rubric_assessments_*.yaml`: model-specific rubric-input sources for the atlas scores

In practice:

- the archive supplies post bodies, canonical Substack URLs, timestamps, and localized assets
- the post map supplies research-folder links, series grouping, tags, summaries, and featured status
- the portfolio manifest exclusively controls the flagship and supporting homepage slots; `homepage.annotation` takes precedence over an artifact rationale when present
- the editorial atlas supplies essay-level scores, section scores, move tags, and draft-pull objects for the public atlas route
- `atlas_data.json` is expected to round-trip from the complete model-specific rubric files; `npm run check:mirror` now fails when the generated atlas and the checked-in JSON diverge

The editorial atlas route is deliberately preserved for historical access, but it is not linked from the homepage or primary navigation.

## Layout

- [`lib/archive-data.js`](lib/archive-data.js): merges archive manifest and curated map into the data model used by the site
- [`src/_data/`](src/_data): 11ty global data entrypoints
- [`src/_includes/`](src/_includes): layouts and reusable partials
- [`src/index.njk`](src/index.njk): selective portfolio entrance
- [`src/archive/index.njk`](src/archive/index.njk): filterable archive page
- [`src/editorial-atlas/index.njk`](src/editorial-atlas/index.njk): public editorial atlas page
- [`src/posts/post.njk`](src/posts/post.njk): per-post template
- [`src/series/series.njk`](src/series/series.njk): series landing pages
- [`src/feed.xml.njk`](src/feed.xml.njk): mirror RSS
- [`src/sitemap.xml.njk`](src/sitemap.xml.njk): sitemap
- [`src/archive.json.njk`](src/archive.json.njk): machine-readable archive export
- [`src/static/`](src/static): CSS and small client-side archive filtering
- `_site/`: generated output, gitignored

## Routes

The mirror currently publishes:

- `/`
- `/archive/`
- `/editorial-atlas/`
- `/posts/<slug>/`
- `/series/<series_key>/`
- `/feed.xml`
- `/sitemap.xml`
- `/archive.json`

## Local Commands

Run from the repo root:

```bash
npm run build:mirror
npm run dev:mirror
npm run check:mirror
```

Use `check:mirror` before pushing. It validates:

- required manifest keys
- the portfolio manifest's four-plus-four cap, exact ordering, annotations, canonical Substack URLs, AI disclosure, and professional-profile CTA
- that no unmanifested essay appears in a curated homepage slot
- archive file existence
- complete public archive preservation and a Substack canonical URL on every mirrored essay page
- localized markdown asset references
- generated root README mapping content
- internal links in the built mirror
- HTTP smoke routes for the homepage, archive, a representative essay, feed, and the preserved atlas route at the configured root or Pages path prefix
- removal of archive statistics, recent additions, and editorial-atlas promotion from the entrance and primary navigation
- the responsive viewport, mobile breakpoint, skip link, and visible keyboard focus styles
- editorial atlas data shape and the still-built atlas route

## Environment Variables

The mirror uses three environment variables:

- `ELEVENTY_PATH_PREFIX`: base path for GitHub Pages project sites such as `/content/`
- `MIRROR_SITE_URL`: root site origin such as `https://petroslamb.github.io`
- `MIRROR_REPO_URL`: repository URL used for GitHub links in the UI

For local Pages-like verification:

```bash
ELEVENTY_PATH_PREFIX=/content/ MIRROR_SITE_URL=https://petroslamb.github.io npm run check:mirror
```

## Deployment

GitHub Pages deploys from [`deploy-mirror.yml`](../../.github/workflows/deploy-mirror.yml).

The workflow:

1. checks out the repo
2. installs Python and Node dependencies
3. builds and verifies the mirror
4. uploads `mirror/_site` as the Pages artifact
5. deploys via GitHub Actions

The public URL is [https://petroslamb.github.io/content/](https://petroslamb.github.io/content/).

## Sync Relationship

The mirror does not fetch Substack directly. The sync step happens first through [`scripts/sync_substack_archive.py`](../../scripts/sync_substack_archive.py), which refreshes the archive and manifest. The mirror then renders from the local archive.

That means:

- if a post is missing from the mirror, check the archive sync first
- if sync is blocked upstream, you can manually import the post into `../substack_archive/` and `metadata.json`, then rerun `npm run check:mirror`
- if a post renders without a research folder, add or update its entry in `post_map.yaml`
- if a post should not appear publicly, inspect `mirror_enabled` in `metadata.json`
- if a selected essay is missing or appears in the wrong order, correct the proposed portfolio manifest and regenerate its decision report before approval; do not hand-curate the template

## Current Assumptions

- only public posts are mirrored
- homepage selection counts are upper bounds, not quotas; zero selected essays is valid
- series are defined manually in `post_map.yaml`
- Substack canonical URLs remain the preferred canonical link target
- local markdown snapshots are the render source, not the raw HTML files
