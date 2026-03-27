# Raw Artifact: Session Excerpt

`2026-03-27T18:11:44Z` User

> i think the series of classes in the operating agents course is upside down. i suspect the same might be happening in the tldr playlist can you fix this?

`2026-03-27T18:11:56Z` Assistant

> I’m checking the current item order in both playlists first so I can confirm whether they’re reversed before I rewrite positions.

`2026-03-27T18:13:37Z` Assistant

> The library-only path is exhausted here: the course playlist is effectively being rendered in newest-published-first order, which is why it appears upside down, and the API won’t let me override positions unless the playlist is switched to `Manual` in Studio first.

`2026-03-27T18:13:57Z` Tool output

> Playwright opened YouTube Studio playlist management.

`2026-03-27T18:14:57Z` Assistant

> The course playlist was reversed and is now fixed. The TL;DR playlist was already in the correct order, so I left it unchanged.

`2026-03-27T18:14:57Z` Assistant

> I had to do this in two steps because the YouTube API would not reorder the course playlist while its sort mode was set to `Date published (newest)`. I switched that playlist to manual ordering in Studio, then applied the reorder through the API.

`2026-03-27T18:14:57Z` Assistant

> I verified the final live order directly from YouTube:
>
> 1. `Operating Agents I`
> 2. `Operating Agents II`
> 3. `Operating Agents III`
> 4. `Operating Agents IV`
> 5. `Operating Agents V`
> 6. `Operating Agents Bonus`

`2026-03-27T18:14:57Z` Assistant

> I also added a reusable sync script at `youtube_data_api_playbook/scripts/sync_operating_agents_playlist_order.py`.
