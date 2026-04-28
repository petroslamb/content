# Tests

This directory holds Python tests for reusable script behavior and contract helpers.

Use this layer for focused assertions that can run without external services. Repo-wide operational validation still lives in the npm/check surfaces documented in [`../scripts/README.md`](../scripts/README.md), and retained proof runs still belong in [`../reviewable-runs/`](../reviewable-runs/README.md).

## Current Tests

- `test_essay_iteration_packet.py`: essay-iteration packet helpers and validation behavior
- `test_harness_phase15.py`: harness/package lifecycle compatibility behavior
- `test_youtube_analytics.py`: YouTube analytics parsing and recommendation helpers

## Boundary

- Do not put live publication sync, YouTube mutation, NotebookLM browser auth, or Substack network checks here.
- Prefer deterministic fixtures and local temp paths.
- Use `scripts/check_*` validators for repo policy checks that are intended to be operator-facing commands.
