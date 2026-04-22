# Explainer Shorts Wave Run

Run date: 2026-04-22
Status: local prep complete, channel upload blocked by YouTube Data API quota

## Prepared Shorts

| Publication | Clip | Scheduled publish | Related explainer video | Related URL | Local folder |
| --- | --- | --- | --- | --- | --- |
| Neural Architecture | What AI Architects Design Now | 2026-04-30 19:00 UTC | `BSwFQTIrAmQ` | `https://www.youtube.com/watch?v=BSwFQTIrAmQ` | `publications/neural-architectures/neural-architecture-design-as-a-compositional-32e/artifacts/video/explainer-wave-2026-04-30/` |
| Binding Gap | Hallucination Is Like Calling Every Illness a Fever | 2026-05-01 19:00 UTC | `NGFObh96z8k` | `https://www.youtube.com/watch?v=NGFObh96z8k` | `publications/binding-gap/artifacts/video/explainer-wave-2026-04-30/` |
| Neural Architecture | Why Identical AI Blocks Learn Different Jobs | 2026-05-02 19:00 UTC | `BSwFQTIrAmQ` | `https://www.youtube.com/watch?v=BSwFQTIrAmQ` | `publications/neural-architectures/neural-architecture-design-as-a-compositional-32e/artifacts/video/explainer-wave-2026-04-30/` |

## Local Verification

- All 3 portrait masters passed preflight at `1080x1920` with AAC audio and durations under 60 seconds.
- No zero-byte files were left in the explainer-wave folders.
- Dry-run upload plans resolved the expected titles, publish timestamps, related explainer video IDs, and target playlist `PL8lPx5mgRhhbMQQ70d-C4dAKKKPzCd5Hd`.

## Channel Mutation Blocker

- The YouTube Data API returned `quotaExceeded` on the first upload attempt for both the Neural and Binding batches.
- Because upload mutations are quota-blocked, no live or scheduled YouTube Shorts IDs exist yet for this explainer wave.

## Next Action

- Retry the exact prepared upload commands after the daily quota reset.
