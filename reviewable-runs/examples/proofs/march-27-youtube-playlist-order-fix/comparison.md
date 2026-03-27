# Raw Trace Vs Review Packet

Use this file to compare the March 27 YouTube playlist-order fix in two modes:

1. curated raw session artifacts
2. reconstructed review packet

## Raw Trace Only

The raw trace shows the user complaint, the playlist inspection, the failed library-only path, the Studio intervention, the API reorder, and the final confirmation. That is enough to reconstruct the broad story, but three things still take extra reviewer effort:

- separating this playlist-order run from the earlier cross-link run and the later video-rendering runs in the same session
- understanding why the stop boundary is a live YouTube state change rather than a repo commit
- seeing which evidence actually proves success versus which evidence only shows that the script ran

## Review Packet

The packet makes these things explicit:

- the bounded objective: correct the playlist order on YouTube
- the mixed control path: API inspection, Studio mode change, API reorder, live read-back verification
- the fact that final verification depends on the live observed playlist order
- the operational approval boundary: the external playlist state was changed successfully
- the most plausible failure: partial reorder or future sort-mode drift

## Practical Difference

| Question | Raw trace only | Review packet |
| --- | --- | --- |
| What was the task? | mixed with adjacent YouTube work | explicit playlist-order correction |
| What happened? | reconstructable with effort | explicit mixed-control execution trace |
| What did it rely on? | spread across API probes, Studio interaction, and script output | explicit evidence record |
| How was it checked? | visible but fragmented | explicit live verification summary |
| Who approved impact? | operationally implied by the live change | explicit external-action boundary |
| What failed or could fail? | mostly implied | explicit sort-mode and partial-order risk |

## Bottom Line

For this run, the packet earns its cost by making an external third-party state change reviewable without collapsing back into “it seems like it worked.”
