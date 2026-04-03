# NotebookLM-Py Playbook

This folder documents the `notebooklm-py` workflow used in this repository:

- how we authenticate and call the CLI
- how we create notebooks
- how we add and wait for sources
- which artifacts we generate
- which prompt texts we use for artifact generation
- how we download the resulting artifacts

## Environment

Use the repo-local virtual environment:

```bash
.venv/bin/notebooklm --help
```

If login is needed:

```bash
.venv/bin/notebooklm login
```

## Artifact Bundle We Use

Our standard bundle is:

- audio overview: `deep-dive`, `long`
- slide deck: `detailed`
- flashcards: `more`, `hard`
- quiz: `more`, `hard`
- video overview: `explainer`

Prompt files used for the text-customized artifacts:

- [prompts/audio.txt](prompts/audio.txt)
- [prompts/slide_deck.txt](prompts/slide_deck.txt)
- [prompts/video.txt](prompts/video.txt)

## Create A Notebook

Create a notebook:

```bash
.venv/bin/notebooklm create --json "Notebook Title"
```

Typical response shape:

```json
{
  "notebook": {
    "id": "NOTEBOOK_ID",
    "title": "Notebook Title"
  }
}
```

## Add A Source

Add a local markdown file:

```bash
.venv/bin/notebooklm source add -n NOTEBOOK_ID --json path/to/file.md
```

Wait for indexing:

```bash
.venv/bin/notebooklm source wait -n NOTEBOOK_ID --json SOURCE_ID
```

List sources:

```bash
.venv/bin/notebooklm source list -n NOTEBOOK_ID --json
```

## Generate Artifacts

### Whole Notebook

Generate the standard bundle from all sources in a notebook:

```bash
.venv/bin/notebooklm generate audio -n NOTEBOOK_ID --retry 3 --json --format deep-dive --length long "$(cat workflows/skills/notebooklm-artifact-bundle/references/prompts/audio.txt)"
.venv/bin/notebooklm generate slide-deck -n NOTEBOOK_ID --retry 3 --json --format detailed "$(cat workflows/skills/notebooklm-artifact-bundle/references/prompts/slide_deck.txt)"
.venv/bin/notebooklm generate flashcards -n NOTEBOOK_ID --retry 3 --json --quantity more --difficulty hard
.venv/bin/notebooklm generate quiz -n NOTEBOOK_ID --retry 3 --json --quantity more --difficulty hard
.venv/bin/notebooklm generate video -n NOTEBOOK_ID --retry 3 --json --format explainer "$(cat workflows/skills/notebooklm-artifact-bundle/references/prompts/video.txt)"
```

### Single Source Only

Generate the same bundle from exactly one source:

```bash
.venv/bin/notebooklm generate audio -n NOTEBOOK_ID -s SOURCE_ID --retry 3 --json --format deep-dive --length long "$(cat workflows/skills/notebooklm-artifact-bundle/references/prompts/audio.txt)"
.venv/bin/notebooklm generate slide-deck -n NOTEBOOK_ID -s SOURCE_ID --retry 3 --json --format detailed "$(cat workflows/skills/notebooklm-artifact-bundle/references/prompts/slide_deck.txt)"
.venv/bin/notebooklm generate flashcards -n NOTEBOOK_ID -s SOURCE_ID --retry 3 --json --quantity more --difficulty hard
.venv/bin/notebooklm generate quiz -n NOTEBOOK_ID -s SOURCE_ID --retry 3 --json --quantity more --difficulty hard
.venv/bin/notebooklm generate video -n NOTEBOOK_ID -s SOURCE_ID --retry 3 --json --format explainer "$(cat workflows/skills/notebooklm-artifact-bundle/references/prompts/video.txt)"
```

Typical response shape:

```json
{
  "task_id": "ARTIFACT_ID",
  "status": "pending"
}
```

List generated artifacts:

```bash
.venv/bin/notebooklm artifact list -n NOTEBOOK_ID --json
```

## Download Artifacts

Download by artifact ID is the cleanest approach.

### Audio

```bash
.venv/bin/notebooklm download audio -n NOTEBOOK_ID -a ARTIFACT_ID output.mp3
```

### Slide Deck

PDF:

```bash
.venv/bin/notebooklm download slide-deck -n NOTEBOOK_ID -a ARTIFACT_ID output.pdf
```

PPTX:

```bash
.venv/bin/notebooklm download slide-deck -n NOTEBOOK_ID -a ARTIFACT_ID --format pptx output.pptx
```

### Flashcards

JSON:

```bash
.venv/bin/notebooklm download flashcards -n NOTEBOOK_ID -a ARTIFACT_ID --format json flashcards.json
```

Markdown:

```bash
.venv/bin/notebooklm download flashcards -n NOTEBOOK_ID -a ARTIFACT_ID --format markdown flashcards.md
```

HTML:

```bash
.venv/bin/notebooklm download flashcards -n NOTEBOOK_ID -a ARTIFACT_ID --format html flashcards.html
```

### Quiz

JSON:

```bash
.venv/bin/notebooklm download quiz -n NOTEBOOK_ID -a ARTIFACT_ID --format json quiz.json
```

Markdown:

```bash
.venv/bin/notebooklm download quiz -n NOTEBOOK_ID -a ARTIFACT_ID --format markdown quiz.md
```

HTML:

```bash
.venv/bin/notebooklm download quiz -n NOTEBOOK_ID -a ARTIFACT_ID --format html quiz.html
```

### Video

```bash
.venv/bin/notebooklm download video -n NOTEBOOK_ID -a ARTIFACT_ID output.mp4
```

## Handy Status Commands

Check notebooks:

```bash
.venv/bin/notebooklm list --json
```

Check one notebook's artifacts:

```bash
.venv/bin/notebooklm artifact list -n NOTEBOOK_ID --json
```

Check one notebook's sources:

```bash
.venv/bin/notebooklm source list -n NOTEBOOK_ID --json
```
