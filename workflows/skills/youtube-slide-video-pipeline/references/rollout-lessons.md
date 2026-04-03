# Rollout Lessons

These constraints came from the Operating Agents YouTube production rollout.

## Timing And Review

- Caption timestamps are the ground truth. OCR is only for drafting likely slide boundaries.
- Low match scores are review targets, not auto-accepted timings.
- Some decks diverge from spoken order. Favor semantic transcript order and record that deliberately in the verified cue sheet.
- Zero-byte local SRT files are not valid inputs. Recover a real subtitle file before building cues.

## API Limits And Fallbacks

- The YouTube Data API does not support modern end-screen editing. Use description cross-links and playlist order, not end-screen automation.
- Playlist reordering can fail with `manualSortRequired`; the playlist must be in manual sort mode in YouTube Studio before the write path succeeds.
- `quotaExceeded` is not a reason to stop local production work. Continue subtitle recovery, cue generation, and rendering while writes are blocked.

## Subtitle Recovery

- When the managed caption path is blocked, recover automatic subtitles with `yt-dlp` instead of waiting on the Data API.
- Watch-page transcript scraping is useful for inspection, but the best render path still uses a real timed `.srt` file when available.
