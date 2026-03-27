# Raw Artifact: Boundary Record

## Boundary

- boundary type: `submit`
- boundary state: `external playlist order changed and verified live`
- timestamp: `2026-03-27T18:14:58.014Z`

## Pending Action

- pending action if any: `none for this bounded run`

## Conditions

- condition: the course playlist must end in the intended chapter order
- condition: the TL;DR playlist must be checked and only changed if needed
- condition: the final result must be confirmed from live YouTube state, not just local script output

## Notes

- this run uses a third-party platform state-change boundary instead of a commit boundary
- the Studio interaction mattered because the API alone could not complete the reorder while the playlist stayed in automatic newest-first mode
