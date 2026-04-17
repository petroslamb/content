# Autonomous Agents Scripts

This folder holds umbrella-local automation for the Autonomous Agents / Operating Agents package.

Scripts here are not root repo automation. They are allowed to be series-specific because they operate on the internal structure of this umbrella package.

## Scripts

| Script | Role | Normal Entry Point |
| :--- | :--- | :--- |
| [`sync_operating_agents_substack.py`](sync_operating_agents_substack.py) | Republishes the Operating Agents preface and essay set to their existing Substack posts, preserves embedded video blocks, rewrites cross-links to Substack URLs, and retries on rate limits. | `PYTHONUNBUFFERED=1 .venv/bin/python publications/autonomous-agents/scripts/sync_operating_agents_substack.py` |

## Safety

This is a mutating external-publishing adapter. Run it only after the Operating Agents markdown has been reviewed and the user has explicitly approved a whole-series Substack sync.
