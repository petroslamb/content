# Rollout Lessons

These notes came from the actual Operating Agents publication rollouts.

## Publishing Behavior

- The sync script is the canonical path for keeping the live preface and essays aligned with repo markdown.
- It should preserve the `Video TL;DR` embed block while updating the rest of the post body.
- Published essay links should remain Substack-first. The script now rewrites repo-relative links for known published posts into their live Substack URLs.

## Operational Constraints

- Rate limiting happens in practice. Keep `PYTHONUNBUFFERED=1` on runs so progress and retries are visible.
- The script currently republishes the full post set in `POST_SPECS`; there is no dedicated single-slug CLI yet.
- Authentication depends on `/tmp/substack_cookie_string.txt`. Missing or stale cookies are the first thing to check.

## Archive Coordination

- After live publication changes, rerun `npm run sync:substack` so `publication_strategy_and_archive/substack_archive/` reflects the new live state.
- If the archive workflow fails in CI because of feed blocking, do the archive refresh locally and validate the mirror there.
