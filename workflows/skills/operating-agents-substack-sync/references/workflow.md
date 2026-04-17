# Operating Agents Substack Workflow

Use this file for the repo-specific Substack publishing path for the Operating Agents series.

## Prerequisites

- repo root as working directory
- repo-local environment: `.venv/bin/python`
- `/tmp/substack_cookie_string.txt` populated with a valid authenticated cookie string

## Source Set

`publications/autonomous-agents/scripts/sync_operating_agents_substack.py` republishes the markdown listed in its `POST_SPECS` table:

- `operating-agents-preface-a-field`
- `operating-agents-i-when-language`
- `operating-agents-ii-memory-needs`
- `operating-agents-iii-diagnose-the`
- `operating-agents-iv-the-second-agent`
- `operating-agents-v-the-attack-surface`
- `operating-agents-bonus-the-workflow`

## Publish Sequence

Run the live sync:

```bash
PYTHONUNBUFFERED=1 .venv/bin/python publications/autonomous-agents/scripts/sync_operating_agents_substack.py
```

Then refresh the tracked public archive so repo snapshots match the live posts:

```bash
npm run sync:substack
```

## Script Behavior

- Resolves repo-relative links and rewrites links to already-published Operating Agents markdown as Substack URLs.
- Preserves the existing embedded video node when the markdown still includes the `#### Video TL;DR` section.
- Publishes from the repo markdown itself, not from a detached export file.
- Retries Substack API calls on `429` with exponential backoff.

## When Not To Use This Skill

- Do not use it for general archive refreshes without live post changes. Use `substack-archive-sync`.
- Do not use it when the user only wants local markdown edits and has not asked for published Substack changes.
