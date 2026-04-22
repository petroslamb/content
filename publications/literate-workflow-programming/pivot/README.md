# Pivot Workspace

This folder holds successor-search artifacts after the flagship stop gate fires.

## Layout

- `active/`
  The single live pivot-search workspace.
- `archive/<pivot-id>/`
  Reserved for older pivot attempts once the active search is superseded.

## Rule

Only one pivot workspace should be active at a time.

If the package changes pivot direction materially:

1. move the old `active/` contents into `archive/<pivot-id>/`
2. start a fresh `active/` workspace
3. keep the donor `ceiling report` at package root

This keeps the bounded flagship packet visible while preventing pivot artifacts from mixing with `candidate-r*`, `replacement-review-r*`, and other root-level essay-iteration surfaces.
