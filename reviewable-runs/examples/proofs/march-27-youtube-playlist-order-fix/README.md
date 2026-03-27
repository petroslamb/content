# Proof: March 27 YouTube Playlist Order Fix

**Status:** `real captured run`

This folder reconstructs the bounded YouTube run that detected a reversed course playlist, switched to a mixed Studio-and-API control path, reordered the playlists, verified the live final order, and added a reusable sync script.

## Scenario

The run starts from the user reporting that the `Operating Agents` course looked upside down. It ends when the course playlist is reordered live, the TL;DR playlist is confirmed correct, and the final order is verified.

## Why This Proof Matters

This is the framework's first flagship proof for a real external-action run on a third-party platform. It adds:

- a live platform state change
- mixed API and browser/UI control
- explicit state verification against YouTube itself
- a non-commit approval boundary

## Folder Map

- `raw-artifacts/`: curated session evidence, changed-surface summary, live verification outputs, boundary record, and platform-state note
- `review-packet/`: the reconstructed six-record surface
- `comparison.md`: what the packet makes clearer than the raw trace

## Run Outcome

- the `Operating Agents` course playlist was corrected to the intended chapter order
- the `Operating Agents TL;DR` playlist was checked and left unchanged
- a reusable order-sync script landed at `youtube_data_api_playbook/scripts/sync_operating_agents_playlist_order.py`
- the decisive boundary was the live YouTube playlist state, not a git commit

## What This Proves

This proof shows that Reviewable Runs can handle an external-action workflow where the most important boundary is a third-party platform state change verified live, not a code merge or release.
