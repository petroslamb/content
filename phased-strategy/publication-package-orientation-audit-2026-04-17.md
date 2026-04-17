# Publication Package Orientation Audit - 2026-04-17

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

After those fixes:

- `npm run status` lists 15 leaf packages.
- `evidence-governance` remains excluded from the status table because it is an umbrella manifest.
- `npm run check:harness` passes.
- `npm run check:repo-links` passes.

## Summary

| Category | Count | Packages |
| :--- | ---: | :--- |
| Fully oriented by structural audit | 10 | `binding-gap`, `clean-interface-illusion`, `confidence-debt`, `corrective-competence`, `evidence-governance/archive/measuring-trust-the-gap-between-ai`, `evidence-governance/archive/the-five-component-pattern-for-ai`, `evidence-governance/your-ai-is-confidently-wrong-and`, `moltbook-phenomenon`, `neural-architectures/neural-architecture-design-as-a-compositional-32e`, `programmable-thinking` |
| Oriented, but needs exception classification or backfill | 6 | `autonomous-agents`, `autonomy-tax`, `evidence-governance`, `hardware-friction`, `illusion-of-swarm`, `orchestration-paradigm` |
| Fatal orientation failures after fixes | 0 | none |

## Package Findings

| Package | Orientation Status | Next Action | Notes |
| :--- | :---: | :--- | :--- |
| `autonomous-agents` | `PARTIAL` | `distribution` | Live draft resolves, but the root package lacks configured local/shared evidence, artifacts, and archive under the generic scaffold. Likely umbrella exception; should be documented or normalized. |
| `autonomy-tax` | `PARTIAL` | `youtube_production` | Evidence exists under `sources/`, but generic audit sees no artifacts/archive and no local source markdown. It is a submodule exception and should be documented as such. |
| `binding-gap` | `PASS` | none | Fully complete by lifecycle table and structural audit. |
| `clean-interface-illusion` | `PASS` | `notebooklm_artifacts` | Structural orientation is good. Next action is blocked by missing NotebookLM notebook identity and approval policy. |
| `confidence-debt` | `PASS` | `paper_intake` | Structural orientation is good after changing the lifecycle kind to `leaf`. Next action is guided paper-intake resolution. |
| `corrective-competence` | `PASS` | `essay_iteration` | Structural orientation is good. Next action is executable through the essay-iteration scaffold. |
| `evidence-governance` | `PARTIAL` | `essay_iteration` | Umbrella manifest lacks a live draft and direct evidence path by the generic audit. Likely should stay an umbrella, but its `status.yaml` should not pretend to be a runnable leaf. |
| `evidence-governance/archive/measuring-trust-the-gap-between-ai` | `PASS` | `notebooklm_artifacts` | Structural orientation is good after markdown path fix. Next action needs NotebookLM notebook identity and approval. |
| `evidence-governance/archive/the-five-component-pattern-for-ai` | `PASS` | `notebooklm_artifacts` | Structural orientation is good after markdown path fix. Next action needs NotebookLM notebook identity and approval. |
| `evidence-governance/your-ai-is-confidently-wrong-and` | `PASS` | `essay_iteration` | Structural orientation is good. Next action is executable through the essay-iteration scaffold. |
| `hardware-friction` | `PARTIAL` | `youtube_production` | Live draft resolves, but generic audit sees no local/shared evidence, artifacts, or archive. This appears to be an older umbrella-style package needing either normalization or explicit audit ignores. |
| `illusion-of-swarm` | `PARTIAL` | `distribution` | Scaffold is present, but audit reports evidence drift: draft cites 13 external links while only one local source markdown file exists. |
| `moltbook-phenomenon` | `PASS` | `youtube_production` | Structural orientation is good. Next action is blocked by missing media-production inputs, not by package navigation. |
| `neural-architectures/neural-architecture-design-as-a-compositional-32e` | `PASS` | `substack_publishing` | Structural orientation is good. Next action is external mutation and approval-gated. |
| `orchestration-paradigm` | `PARTIAL` | `youtube_production` | Live draft resolves, but generic audit sees no local/shared evidence, artifacts, or archive. Needs normalization or explicit umbrella exception. |
| `programmable-thinking` | `PASS` | `youtube_production` | Structural orientation is good. Next action is blocked by missing media-production inputs, not by package navigation. |

## Open Work

1. Decide how to classify old umbrella packages.
   - `autonomous-agents`, `hardware-friction`, and `orchestration-paradigm` have useful custom structures but do not satisfy the generic scaffold audit.
   - Either add package-local `ignore_scaffold_audit` entries with rationale, or normalize evidence/artifact/archive pointers.

2. Clarify `evidence-governance` root status.
   - It is correctly an umbrella, but its lifecycle stages still look like a runnable leaf.
   - Prefer making the umbrella manifest explicit about leaf packages and shared evidence while avoiding a misleading next-action result.

3. Backfill evidence markdown or classify evidence drift.
   - `illusion-of-swarm` has enough orientation to operate, but its evidence surface is thin relative to external links in the draft.
   - `autonomy-tax` has source material, but not in the generic markdown count expected by `audit_package.py`.

4. Treat media-stage blockers separately from orientation blockers.
   - Missing NotebookLM IDs, audio narration, slide inputs, and publishing approval are stage-execution blockers.
   - They do not mean the package is hard to orient in the repo.

## Phase 1 Read

The package-orientation gate is mostly closed, but not perfectly clean.

The important improvement from this audit is that there are no remaining fatal live-draft path failures after the two archive-path fixes, and the active `confidence-debt` package is now visible in `npm run status`.

The remaining work is classification and normalization, not discovery from scratch.
