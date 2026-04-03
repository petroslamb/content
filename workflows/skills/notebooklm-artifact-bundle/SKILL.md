---
name: notebooklm-artifact-bundle
description: Use when Codex needs to generate the repository's standard NotebookLM artifact bundle for a notebook, inspect artifact/task status, reuse the established audio/slide/video prompt texts, or upload generated audio back into NotebookLM to recover a transcript.
---

# NotebookLM Artifact Bundle

Use the repo-local NotebookLM workflow in `.venv/bin/notebooklm`. This skill is for repeated artifact generation and transcript recovery, not for generic NotebookLM brainstorming.

## Working Rules

1. Use the repo-local binary: `.venv/bin/notebooklm`.
2. Verify auth first with `.venv/bin/notebooklm auth check --test`.
3. Resolve the target notebook before generating artifacts. Accept either notebook ID or exact title.
4. Submit the standard bundle first, then poll in batches instead of serially waiting on each task.
5. Reuse the established prompt texts for audio, slide deck, and video unless the user explicitly asks for a different tone.
6. When the user wants a transcript of generated audio, upload the MP3 back as a source, wait until it is ready, then export the indexed full text.

## Standard Bundle

- Audio overview: `deep-dive`, `long`
- Slide deck: `detailed`
- Flashcards: `more`, `hard`
- Quiz: `more`, `hard`
- Video overview: `explainer`

## Reference Map

- `../../../workflows/notebooklm-artifacts/README.md`: tracked canonical artifact-generation and transcript-recovery workflow.
- `references/workflows.md`: notebook resolution, standard bundle generation, polling, and transcript round-trip.
- `references/prompts.md`: canonical prompt files and the voice constraints they encode.
