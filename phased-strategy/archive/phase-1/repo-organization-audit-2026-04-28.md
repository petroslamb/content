# Repo Organization Audit - 2026-04-28

Archive note, 2026-05-06: this audit is retained as historical authority-cleanup evidence. It describes the pre-closeout skew between Phase 2 surfaces and the old compatibility layer. The `harness_contract.yaml` rollup and legacy npm adapters have since been retired; see [`../../../AUTHORITY.md`](../../../AUTHORITY.md) and [`../../phase-2/`](../../phase-2/README.md) for the current baseline.

Scope: root orientation files, publication/package map, workflow map, script map, authority/policy contracts, reviewable-run stores, ignored local surfaces, and active experiment folders.

This audit is about organization and source-of-truth drift. It does not judge article quality.

## Executive Verdict

The repo is much cleaner after the Phase 2 authority migration, but it is not fully converged.

The biggest remaining issue is not folder chaos. The top-level tree is readable, hidden/local folders are ignored correctly, and the major package/workflow indexes cover their directories. The real problem is authority skew: `AUTHORITY.md`, `workflow.yaml`, `content-agent`, `pipeline_profiles.yaml`, `harness_contract.yaml`, and `harness_policy.yaml` do not all describe the same operating layer yet.

Brutally: the repo now has a high-level authority layer, but some compatibility files still think the old README-frontmatter/stage-runner model is the main machine truth. That is the primary cleanup target.

## Remediation Status

Resolved in the follow-up migration on 2026-04-28:

- `harness_contract.yaml` is now generated as a Phase 2 compatibility index with `AUTHORITY.md`, `workflow.yaml`, `content-agent`, `content-cockpit`, npm aliases, and report-only editorial surfaces represented.
- `harness_policy.yaml` now separates runtime writes from governance-maintenance writes.
- `workflow.yaml` contracts now exist for `evidence_authorization`, `release_gate`, `distribution`, `topic_discovery`, and `post_ceiling_pivot`.
- `publications/security-research/` is classified as a research bucket/support package instead of a single-publication package.
- `experiments/` and active experiment folders are indexed.
- `scripts/README.md` covers every root Python script currently present.
- root brand assets and `tests/` now have orientation docs.
- stale `literate-workflow-programming` pivot links found during validation now point to the archived no-successor and validation-doctrine records.

## What Is Clean

- `README.md`, `AGENTS.md`, `AUTHORITY.md`, `workflows/README.md`, `scripts/README.md`, and `reviewable-runs/README.md` now agree on `content-agent` as the preferred governed surface.
- Every top-level publication folder is referenced in `publications/README.md`.
- Every workflow folder is referenced in `workflows/README.md`.
- Hidden local activation/cache folders are ignored and not tracked: `.agents/`, `.codex/`, `.youtube/`, `.notebooklm_local/`, `.playwright-*`, `.DS_Store`, `output/`, `tmp/`, and `node_modules/`.
- `reviewable-runs/gates/README.md` documents retained examples, and `content-agent review list --include-retained` exists.
- `CLAUDE.md` is a harmless shim to `AGENTS.md`, not a competing policy file.

## Findings

### P1 - `harness_contract.yaml` Still Treats README Frontmatter As Workflow Truth

Evidence:

- `AUTHORITY.md` says source authority is `workflows/*/workflow.yaml`, root policy/profile/gate YAMLs, and package `status.yaml`.
- `harness_contract.yaml` still lists `workflow_frontmatter: workflows/*/README.md` under `sources_of_truth`.
- `harness_contract.yaml` exposes only the older `stage:*`, `workflow:*`, `gate:check`, and package-init interfaces. It does not list `content-agent`, `agent:*`, `content-cockpit`, or `editorial:report`.

Why it matters:

The generated/compatibility contract is still presenting the old operating model as the machine-readable contract. That makes `npm run check:harness` useful for legacy coherence, but weak as a Phase 2 authority check.

Fix:

- Reclassify `harness_contract.yaml` as a generated compatibility/index view.
- Update `scripts/harness.py` and `scripts/check_harness.py` so generated contract output includes the Phase 2 surfaces:
  - `AUTHORITY.md`
  - `workflow_yaml: workflows/*/workflow.yaml`
  - `content-agent`
  - `content-cockpit`
  - `agent:*` npm aliases
  - `editorial:report`
- Keep `workflow_frontmatter` only as a doc/index compatibility source, not source authority.

### P1 - Pipeline Profiles Reference Workflows Without `workflow.yaml`

Evidence:

`pipeline_profiles.yaml` declares `route_authority: workflow_yaml_and_package_status`, but profile routes include workflow ids that do not yet have executable contracts:

- `evidence_authorization`
- `release_gate`
- `distribution`
- `topic_discovery`
- `post_ceiling_pivot`

Existing `workflow.yaml` contracts currently exist only for:

- `research`
- `paper_intake`
- `essay_iteration`
- `article_polish`
- `substack_publishing`
- `archive_sync`

Why it matters:

The profile file now claims workflow-YAML authority, but some routes can only resolve to README docs. That is fine if marked transitional; it is misleading if treated as governed executable routing.

Fix:

- Add minimal `workflow.yaml` contracts for the five missing profile workflows.
- Or add explicit `profile_only` / `manual_only` / `readme_only` posture to those route entries until contracts exist.
- Make `content-agent validate --workflow <id>` fail clearly when a profile route is not yet executable.

### P2 - `harness_policy.yaml` Write Scope Is Too Narrow For The New Authority Layer

Evidence:

`harness_policy.yaml` allows writes to `publications/`, `publication_strategy_and_archive/`, `README.md`, `scripts/`, and `reviewable-runs/*`. It does not name:

- `AUTHORITY.md`
- `AGENTS.md`
- `workflows/`
- `phased-strategy/`
- `package.json`
- root `pipeline_profiles.yaml`
- root `gate_contracts.yaml`
- `harness_contract.yaml`

Why it matters:

The policy is currently coherent for package/runtime execution, but not for governance migration work. Phase 2 made those root policy/workflow surfaces part of the editable source authority.

Fix:

- Split the policy into two scopes:
  - `governed_runtime_write_allowed`
  - `governance_maintenance_write_allowed`
- Add explicit authority-maintenance paths to the second scope.
- Keep runtime writes narrow so `content-agent run` does not gain broad repo mutation rights by accident.

### P2 - `publications/security-research/` Is Classified Like A Publication But Says It Is Not One

Evidence:

- `publications/README.md` lists `security-research/` as `Single-publication | Active / unpublished`.
- `publications/security-research/README.md` says it is preliminary research material, not tied to a specific published article.
- It has no `status.yaml`, unlike the other publication-package folders.

Why it matters:

This breaks the package-class model. It is either a research bucket/support package or it needs a real package manifest.

Fix:

- Preferred: reclassify it in `publications/README.md` as `Research bucket / support package`, not `Single-publication`.
- If it is expected to become an article package, add a lightweight `status.yaml` and a live-draft/plan surface.

### P2 - Active Experiment State Is Not Indexed

Evidence:

`experiments/` has active state but no root README:

- `experiments/youtube-cinematic-pilot/`
- `experiments/youtube-cinematic-rollout/`
- `experiments/youtube-explainer-shorts/`
- `experiments/youtube-analytics/`

The rollout and analytics folders have active manifests, ledgers, or decision rules, including dirty/untracked local state in the current worktree.

Why it matters:

The root README has a strong Start Here table, but experiments are an unindexed island. For YouTube/cinematic work, important operating truth lives outside the normal publication/workflow/reviewable-run hierarchy.

Fix:

- Add `experiments/README.md` with:
  - experiment name
  - owner workflow
  - state files
  - publication/package dependencies
  - whether it is temporary, evergreen, or retired
- Add a short README to each active experiment folder, or move durable state into the corresponding workflow or package-local artifact surface.

### P2 - Script Map Is Missing Several Current Scripts

Evidence:

`scripts/README.md` does not mention these root scripts:

- `essay_iteration_support.py`
- `research_exit_support.py`
- `build_youtube_decision_report.py`
- `fetch_youtube_analytics.py`
- `prepare_overlay_remaster_backfill.py`
- `mark_overlay_remaster_studio_verified.py`
- `sync_overlay_remaster_uploads.py`
- `unlist_overlay_remaster_old_shorts.py`

Why it matters:

The scripts README claims to explain what each script in the folder does. Missing helper modules are tolerable if marked support-only; missing active YouTube/analytics scripts are not.

Fix:

- Add `essay_iteration_support.py` and `research_exit_support.py` as support modules in the lifecycle section.
- Add `fetch_youtube_analytics.py` and `build_youtube_decision_report.py` to YouTube/channel operations with their ledger, rules, and report paths.
- Add overlay-remaster scripts as a named temporary experiment toolchain, or move them under an experiment/workflow-local script folder if they are not generic root automation.

### P3 - Root Asset Files Are Not Indexed

Evidence:

Root contains image assets such as:

- `petroslamb.png`
- `RootedLayers.png`
- `RootedLayers_inverted.png`

Why it matters:

This is not dangerous, but root assets should be identified as brand/mirror assets. Otherwise they look like loose files in an otherwise policy-heavy root.

Fix:

- Add a short `assets` note to `README.md`, or move them under a tracked `assets/brand/` folder if all references can be updated cleanly.

### P3 - Tests Have No Orientation File

Evidence:

`tests/` exists but has no README.

Why it matters:

Low risk, but the repo now has multiple validation layers. A short tests README would help distinguish unit-style tests from npm validation scripts and workflow proof fixtures.

Fix:

- Add `tests/README.md` explaining what belongs in tests versus `scripts/check_*`, `reviewable-runs/examples/proofs/`, and package-local validation artifacts.

## Redundancies

### Acceptable Redundancy

- `CLAUDE.md` -> `AGENTS.md`: acceptable compatibility shim.
- `README.md`, `AGENTS.md`, and `AUTHORITY.md` all mention source-of-truth order: acceptable if `AUTHORITY.md` remains the canonical detailed map and the others point to it.
- `reviewable-runs/logs/` and `reviewable-runs/gates/` retain real YAML examples: acceptable because they are marked `retained_example: true`.

### Risky Redundancy

- `harness_contract.yaml` duplicates old lifecycle/interface truth while `AUTHORITY.md` defines the new one.
- `pipeline_profiles.yaml` names workflows that exist as README playbooks but not as governed `workflow.yaml` contracts.
- Active YouTube experiment state is split across `workflows/`, `experiments/`, package artifacts, root scripts, and skill scripts without one experiment index.

## Completed Fix Order

1. Bring `harness_contract.yaml` generation/checking up to the Phase 2 authority model.
2. Add `workflow.yaml` contracts or transitional posture markers for the five profile-referenced README-only workflows.
3. Split `harness_policy.yaml` write scopes into runtime writes and governance-maintenance writes.
4. Reclassify or manifest `publications/security-research/`.
5. Add an `experiments/README.md` and per-experiment state index.
6. Update `scripts/README.md` for missing helper, analytics, and overlay-remaster scripts.
7. Add `tests/README.md`.
8. Index or relocate root brand assets.

## Commands Run

```bash
git status --short
find . -maxdepth 2 -type f \( -name README.md -o -name status.yaml -o -name workflow.yaml \) | sort
find workflows -maxdepth 2 -name workflow.yaml -print | sort
git check-ignore -v .DS_Store publications/.DS_Store output tmp .agents .codex .youtube .notebooklm_local .playwright-cli .playwright-mcp node_modules
git ls-files | rg '(^|/)\.DS_Store$|^output/|^tmp/|__pycache__|^node_modules/|^\.agents/|^\.codex/|^\.youtube/|^\.notebooklm|^\.playwright'
python3 - <<'PY'
from pathlib import Path
readme = Path('scripts/README.md').read_text(errors='replace')
scripts = sorted(p.name for p in Path('scripts').glob('*.py'))
print([s for s in scripts if s not in readme])
PY
```
