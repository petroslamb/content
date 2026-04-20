---
workflow_id: package_normalization
workflow_group: package
runner_mode: guided
default_skill: null
approval_gate: none
---

# Package Normalization: The Scaffold Workflow

To maintain a high-fidelity "Content Factory" where research, prose, and multimedia can be iteratively refined, every publication package should adhere to a canonical structural "Scaffold".

This structure ensures that agents (like me) and authors (like you) always know where to find the evidence, the draft, and the production artifacts.

## The Canonical Scaffold

| Component | Directory / File | Purpose |
|:---|:---|:---|
| **Manifest** | `status.yaml` | Tracks lifecycle stage (`research`, `essay_iteration`, etc.), `revision` count, and package `config`. |
| **Live Draft** | `[slug].md` | The current working version of the essay. Pointed to by `config.markdown_path`. |
| **Evidence** | `sources/` or `papers/` | Local archive of research materials. Contains `sources/index.md` or `papers/index.md` plus a markdown conversion subtree. |
| **Multimedia** | `artifacts/` | Derived assets: NotebookLM bundles, podcast audio, YouTube cue sheets, and images. |
| **History** | `archive/` | Historical snapshots of the draft before a new Revision pass. |

## The "Scaffold Requirement" in `status.yaml`

A normalized package must have at least these keys in `status.yaml`:

```yaml
# Standard Stage Tracking
# done: true/false for paper_intake, research, essay_iteration, etc.

kind: leaf
publication: my-essay-slug
parent_package: my-umbrella-package # optional for top-level single-publication packages
revision: 2 # Tracks how many refinement cycles the package has survived

config:
  markdown_path: "publications/my-package/my-essay.md"
  substack_slug: "my-essay-slug"
  evidence_path: "publications/my-package/papers" # optional when the leaf reuses a shared source tree
  notebooklm_notebook_id: "00000000-0000-0000-0000-000000000000" # optional when a NotebookLM notebook exists
  # Optional: ignore_scaffold_audit: ["artifacts", "archive"]
```

## Normalization Process (Advisory)

If a package is flagged during a **Pre-Flight Check** (`npm run run`):
1. **Pointers**: Ensure `markdown_path` is correct. If the draft is in a subfolder (e.g. for umbrella packages), use the full path relative to the repo root.
2. **Sources**: If the essay cites external links, bring them into `sources/` or `papers/` using the `paper-intake` workflow. If a leaf package intentionally reuses a shared evidence tree in its umbrella, point `config.evidence_path` there instead of duplicating the library.
3. **Artifacts**: If creating a podcast or video, initialize the `artifacts/` folder.
4. **Suppression**: If a legacy folder structure is intentional, add it to `config.ignore_scaffold_audit`.

## Why Normalization?
Normalization allows for **Auditability**. If we know where the evidence library is, whether that is local `sources/` or a shared `config.evidence_path`, we can automatically verify if the latest prose still reflects the evidence.
