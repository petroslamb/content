# Publication Package Orientation Audit - 2026-04-17

Archive note, 2026-05-06: this audit is retained as Phase 1 package-orientation evidence. Any command examples using retired compatibility surfaces are historical, not current operator guidance. Use `./content-agent` and the current package `status.yaml`/README surfaces for live work.

## Purpose

This audit tests whether a future agent or operator can pick up each publication package and answer the basic orientation questions without asking for repo-specific explanation:

1. What package is this?
2. Where is the live draft?
3. Where is the lifecycle state?
4. Where is the evidence surface?
5. Where are artifacts and archive history?
6. What is the next valid action?
7. Is the next action executable, approval-gated, or blocked by missing context?

This is not an editorial-quality review, publishing approval, evidence sufficiency review, or artifact-quality review. It is a Phase 1 machine-orientation audit.

## Commands Run

```bash
npm run status
for sf in $(find publications -name status.yaml | sort); do
  pkg=${sf#publications/}
  pkg=${pkg%/status.yaml}
  .venv/bin/python scripts/audit_package.py --package "$pkg"
done
for sf in $(find publications -name status.yaml | sort); do
  pkg=${sf#publications/}
  pkg=${pkg%/status.yaml}
  npm run --silent stage:next -- --package "$pkg" --format json
done
npm run check:harness
npm run check:repo-links
git diff --check
```

## Immediate Fixes Made During Audit

| Package | Fix |
| :--- | :--- |
| `confidence-debt` | Changed `status.yaml` from `kind: umbrella` to `kind: leaf` so `npm run status` shows the active flagship package. Donor provenance remains in the manifest. |
| `evidence-governance/archive/measuring-trust-the-gap-between-ai` | Fixed stale `config.markdown_path` after archive relocation. |
| `evidence-governance/archive/the-five-component-pattern-for-ai` | Fixed stale `config.markdown_path` after archive relocation. |
| `autonomous-agents` | Added configured evidence path plus top-level artifact/archive orientation surfaces. |
| `hardware-friction` | Added configured evidence path plus top-level artifact/archive orientation surfaces. |
| `orchestration-paradigm` | Added configured evidence path plus top-level artifact/archive orientation surfaces. |
| `evidence-governance` | Added configured umbrella evidence path and top-level artifact orientation surface. |

After those fixes:

- `npm run status` lists 15 leaf packages.
- `evidence-governance` remains excluded from the status table because it is an umbrella manifest.
- `npm run check:harness` passes.
- `npm run check:repo-links` passes.

## Summary

| Category | Count | Packages |
| :--- | ---: | :--- |
| Fully oriented by structural audit | 14 | `autonomous-agents`, `binding-gap`, `clean-interface-illusion`, `confidence-debt`, `corrective-competence`, `evidence-governance`, `evidence-governance/archive/measuring-trust-the-gap-between-ai`, `evidence-governance/archive/the-five-component-pattern-for-ai`, `evidence-governance/your-ai-is-confidently-wrong-and`, `hardware-friction`, `moltbook-phenomenon`, `neural-architectures/neural-architecture-design-as-a-compositional-32e`, `orchestration-paradigm`, `programmable-thinking` |
| Oriented, but needs non-umbrella backfill | 2 | `autonomy-tax`, `illusion-of-swarm` |
| Fatal orientation failures after fixes | 0 | none |

## Package Findings

| Package | Orientation Status | Next Action | Notes |
| :--- | :---: | :--- | :--- |
| `autonomous-agents` | `PASS` | `distribution` | Normalized with configured evidence path and top-level artifact/archive orientation surfaces. |
| `autonomy-tax` | `PARTIAL` | `youtube_production` | Evidence exists under `sources/`, but generic audit sees no artifacts/archive. It is a submodule exception, not an umbrella exception. |
| `binding-gap` | `PASS` | none | Fully complete by lifecycle table and structural audit. |
| `clean-interface-illusion` | `PASS` | `notebooklm_artifacts` | Structural orientation is good. Next action is blocked by missing NotebookLM notebook identity and approval policy. |
| `confidence-debt` | `PASS` | `paper_intake` | Structural orientation is good after changing the lifecycle kind to `leaf`. Next action is guided paper-intake resolution. |
| `corrective-competence` | `PASS` | `essay_iteration` | Structural orientation is good. Next action is executable through the essay-iteration scaffold. |
| `evidence-governance` | `PASS` | `essay_iteration` | Umbrella manifest now resolves shared evidence, default leaf, leaf package, archive, and artifacts. It does not require `config.markdown_path`. |
| `evidence-governance/archive/measuring-trust-the-gap-between-ai` | `PASS` | `notebooklm_artifacts` | Structural orientation is good after markdown path fix. Next action needs NotebookLM notebook identity and approval. |
| `evidence-governance/archive/the-five-component-pattern-for-ai` | `PASS` | `notebooklm_artifacts` | Structural orientation is good after markdown path fix. Next action needs NotebookLM notebook identity and approval. |
| `evidence-governance/your-ai-is-confidently-wrong-and` | `PASS` | `essay_iteration` | Structural orientation is good. Next action is executable through the essay-iteration scaffold. |
| `hardware-friction` | `PASS` | `youtube_production` | Normalized with configured evidence path and top-level artifact/archive orientation surfaces. |
| `illusion-of-swarm` | `PARTIAL` | `distribution` | Scaffold is present, but audit reports evidence drift: draft cites 13 external links while only one local source markdown file exists. |
| `moltbook-phenomenon` | `PASS` | `youtube_production` | Structural orientation is good. Next action is blocked by missing media-production inputs, not by package navigation. |
| `neural-architectures/neural-architecture-design-as-a-compositional-32e` | `PASS` | `substack_publishing` | Structural orientation is good. Next action is external mutation and approval-gated. |
| `orchestration-paradigm` | `PASS` | `youtube_production` | Normalized with configured evidence path and top-level artifact/archive orientation surfaces. |
| `programmable-thinking` | `PASS` | `youtube_production` | Structural orientation is good. Next action is blocked by missing media-production inputs, not by package navigation. |

## Open Work

1. Backfill evidence markdown or classify evidence drift.
   - `illusion-of-swarm` has enough orientation to operate, but its evidence surface is thin relative to external links in the draft.
   - `autonomy-tax` has source material, but not in the generic markdown count expected by `audit_package.py`.

2. Treat media-stage blockers separately from orientation blockers.
   - Missing NotebookLM IDs, audio narration, slide inputs, and publishing approval are stage-execution blockers.
   - They do not mean the package is hard to orient in the repo.

## Phase 1 Read

The package-orientation gate is closed for umbrella-package normalization.

The important improvement from this audit is that there are no remaining fatal live-draft path failures after the two archive-path fixes, the active `confidence-debt` package is now visible in `npm run status`, and old umbrella packages now expose configured evidence plus top-level artifact/archive orientation surfaces.

The remaining work is non-umbrella backfill and stage-execution context, not package orientation.
