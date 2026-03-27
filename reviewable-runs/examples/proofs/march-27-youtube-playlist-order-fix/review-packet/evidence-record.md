# Runtime Record: Evidence Record

## Key Evidence

- the user explicitly reported that the course looked upside down
- the YouTube API inspection showed the current order before correction
- the run discovered a real platform constraint: the API path was blocked by playlist sort mode until Studio switched the playlist to manual ordering
- the final live order was read back directly from YouTube and matched the intended sequence
- the run also produced a reusable order-sync script for later replay

## What Actually Mattered

The run was justified by five visible facts:

- the problem was a real live ordering issue, not only a perception issue
- the API-only path was insufficient
- Studio intervention changed the control surface enough for the API reorder to work
- the final live order, not the local script, proved success
- the TL;DR playlist was checked and intentionally left unchanged

## What Was Omitted

The same session also contains the earlier description cross-linking run and the later video-rendering runs. Those were omitted so this packet represents only the bounded playlist-order correction.
