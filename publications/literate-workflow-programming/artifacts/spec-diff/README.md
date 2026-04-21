# Spec-Diff Artifacts

This folder stores prototype outputs for the package-local `spec-diff` experiment.

Current prototype:

- Script: [`../../scripts/spec_diff_paper_intake.py`](../../scripts/spec_diff_paper_intake.py)
- Latest report: [`paper-intake-latest.json`](paper-intake-latest.json)
- P1 pre-index drift report: [`paper-intake-p1-preindex.json`](paper-intake-p1-preindex.json)

Run from the repo root:

```bash
.venv/bin/python publications/literate-workflow-programming/scripts/spec_diff_paper_intake.py
.venv/bin/python publications/literate-workflow-programming/scripts/spec_diff_paper_intake.py --format json --write-report publications/literate-workflow-programming/artifacts/spec-diff/paper-intake-latest.json
```

This is a research artifact, not a promoted repo-wide validator.
