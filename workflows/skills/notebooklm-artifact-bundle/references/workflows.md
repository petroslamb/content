# NotebookLM workflows

Use this file for the concrete command sequences behind the artifact-bundle skill.

## Resolve The Notebook

- Prefer an exact notebook ID when the user provides it.
- If the user gives a title, list notebooks and map the title to the notebook ID before generating anything.

Useful commands:

```bash
.venv/bin/notebooklm auth check --test
.venv/bin/notebooklm list --json
.venv/bin/notebooklm use NOTEBOOK_ID
```

## Generate The Standard Bundle

Submit all five artifact jobs first:

```bash
.venv/bin/notebooklm generate audio -n NOTEBOOK_ID --retry 3 --json --format deep-dive --length long "$(cat workflows/skills/notebooklm-artifact-bundle/references/prompts/audio.txt)"
.venv/bin/notebooklm generate slide-deck -n NOTEBOOK_ID --retry 3 --json --format detailed "$(cat workflows/skills/notebooklm-artifact-bundle/references/prompts/slide_deck.txt)"
.venv/bin/notebooklm generate flashcards -n NOTEBOOK_ID --retry 3 --json --quantity more --difficulty hard
.venv/bin/notebooklm generate quiz -n NOTEBOOK_ID --retry 3 --json --quantity more --difficulty hard
.venv/bin/notebooklm generate video -n NOTEBOOK_ID --retry 3 --json --format explainer "$(cat workflows/skills/notebooklm-artifact-bundle/references/prompts/video.txt)"
```

If the user wants to constrain generation to one source, add `-s SOURCE_ID` to each command.

## Poll Efficiently

- Snapshot task state with `.venv/bin/notebooklm artifact list -n NOTEBOOK_ID --json`.
- Poll only non-completed task IDs.
- Return current status if long-running jobs stop changing rather than spinning indefinitely.

## Preserve The Editorial Boundary

Downloading artifacts is not article polish. Raw outputs can be placed in `artifacts/latest/`, `artifacts/previous/`, or the package's declared artifact home, but publishable article images and markdown embeds are owned by the article-polish workflow.

Before committing a bundle refresh, run a quick continuity check:

```bash
git diff --name-status -- publications/<package>/
git diff -- publications/<package>/<draft>.md | rg '^-!\['
find publications/<package>/artifacts publications/<package>/archive -type f -size 0 2>/dev/null
git status --ignored --short publications/<package>/ | rg 'Library/|__pycache__|\.pyc' || true
```

If deleted image files, removed embeds, zero-byte outputs, or stray cache trees appear, stop unless the user explicitly requested that editorial change and the artifacts have been verified.

## Upload Generated Audio Back For Transcript Recovery

This is a reusable flow recovered from real repo usage.

1. Generate or download the NotebookLM audio artifact.
2. Upload the MP3 back into the notebook as a source.
3. Wait until the source is `ready`.
4. Export the source full text into the target artifact folder.

Commands:

```bash
.venv/bin/notebooklm source add -n NOTEBOOK_ID --type file --mime-type audio/mpeg --json /path/to/audio.mp3
.venv/bin/notebooklm source wait -n NOTEBOOK_ID --json SOURCE_ID
.venv/bin/notebooklm source fulltext -n NOTEBOOK_ID SOURCE_ID -o /path/to/transcript.txt
```

Use `-o` for full transcripts. The terminal output can be a preview that ends with a message telling the caller to use `-o`; redirecting that preview creates a misleading partial transcript.

## Failure Modes

- If `auth check --test` fails, rerun `.venv/bin/notebooklm login`.
- If upload or generation fails immediately, confirm the repo `.venv` is active and the CLI is not being resolved globally.
- If many tasks hang, capture the current `artifact list --json` output and stop polling aggressively.
