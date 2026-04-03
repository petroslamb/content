# Rollout Lessons

These constraints came from the actual Substack mirror rollouts for this repo.

## Feed And CI Behavior

- `/feed` can return `403` inside GitHub runners even when local requests succeed.
- The sync path should tolerate that by falling back to `/api/v1/archive` instead of failing the whole run.
- When the workflow is blocked, use the documented manual-import fallback rather than creating duplicate archive entries.

## Validation Expectations

- Always verify both plain-root and `/content/` prefixed mirror builds.
- `scripts/check_mirror.py` and `scripts/e2e_mirror_smoke.py` are the canonical checks. They are not optional add-ons.
- Manual imports must use canonical slug filenames so sync overwrites them later instead of creating parallel copies.

## Environment Constraints

- Do not try to reconcile the repo's `python-substack` and `markitdown` dependency conflict during routine archive work. Use the working repo environment instead.
- Invalid workflow YAML can create failed `push` runs before jobs even start. If CI behavior looks wrong, check workflow syntax first.

## Cadence

- The repo converged on monthly scheduled sync plus manual dispatch, not frequent automatic runs.
