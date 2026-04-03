---
name: youtube-shorts-maintenance
description: Use when Codex needs to inspect or maintain the repo's Shorts drafts workflow on YouTube, including listing draft uploads by date, diagnosing playlist contents, checking duplicates, cleaning duplicate playlist entries, or updating draft/private descriptions from a shared template.
---

# YouTube Shorts Maintenance

Use this skill when the task is about the Shorts drafts playlist rather than the Operating Agents course. The underlying scripts live in `workflows/skills/youtube-data-api/scripts/`.

## Common Workflows

- List draft/private Shorts for a UTC date:
  `workflows/skills/youtube-data-api/scripts/list_draft_shorts_today.py`
- Inspect playlist status/date distribution:
  `workflows/skills/youtube-data-api/scripts/diagnose_shorts_playlist.py`
- Check duplicate video IDs:
  `workflows/skills/youtube-data-api/scripts/check_duplicates.py`
- Plan or apply duplicate cleanup:
  `workflows/skills/youtube-data-api/scripts/remove_duplicate_playlist_entries.py`
- Plan or apply description updates from a shared template:
  `workflows/skills/youtube-data-api/scripts/update_shorts_descriptions.py`

## Working Rules

- Keep playlist/date inputs explicit when the user provides them.
- Prefer JSON output when another step will consume the result programmatically.
- Use dry-run behavior first for duplicate cleanup and description rewrites; add `--apply` only after confirming scope.
- Treat the description template in `workflows/skills/youtube-data-api/references/shorts_description_template.md` as shared content, not an inline hardcoded constant.

## Reference Map

- `../../../workflows/youtube-channel-ops/README.md`: tracked canonical channel workflow for auth checks, playlist inspection, and Shorts maintenance.
- `../youtube-data-api/references/script-map.md`: script inventory and safety classification.
- `../youtube-data-api/references/rollout-lessons.md`: quota and operational constraints that also apply to Shorts maintenance.
