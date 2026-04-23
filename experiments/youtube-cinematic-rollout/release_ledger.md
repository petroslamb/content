# Daily Cinematic Rollout Ledger

Created: 2026-04-23
Timezone: Europe/Athens
Automation target: daily at 10:00 local time

## Purpose

This ledger is the evergreen run record for the daily cinematic rollout lane.
It replaces the bounded pilot-follow-through ledger as the canonical record for:

- backlog discovery
- hard blockers such as NotebookLM auth expiry or global cinematic quota
- per-package cinematic and Shorts state transitions
- daily release scheduling decisions

The historical pilot remains in `experiments/youtube-cinematic-pilot/`.

## Current Backlog

Initial rollout order from `backlog_manifest.yaml`:

1. `illusion_of_swarm`
2. `the_agent_revolution`
3. `operating_agents_action`
4. `operating_agents_memory`
5. `operating_agents_reasoning`
6. `operating_agents_multi_agent`
7. `operating_agents_safety`
8. `operating_agents_optimization`
9. `moltbook_phenomenon`
10. `programmable_thinking`

## Existing Mapped Cinematics Excluded From Backlog

- `neural_architecture`
- `autonomy_tax`
- `confidence_debt`
- `binding_gap`

## Carried Blockers

- `illusion_of_swarm` is already the front-of-queue item.
- Last known cinematic-create failure on 2026-04-23: `API rate limit or quota exceeded. Please wait before retrying.`
- NotebookLM auth is a hard gate for new cinematic generation and must be refreshed manually with `.venv/bin/notebooklm login` whenever it expires.

## Run Entries

### 2026-04-23 bootstrap

- Created the evergreen backlog manifest and rollout workflow surface.
- Preserved the existing pilot map as the exclusion source for already-mapped cinematic uploads.
- Fixed the initial secondary-link policy:
  - use YouTube long-form links when known
  - use the essay URL fallback for `programmable_thinking`

### 2026-04-23T13:27:27.576994+00:00

- NotebookLM auth: `ok`
- Auth detail: `Authentication is valid.`
- Next generation candidates: `illusion_of_swarm`, `the_agent_revolution`
