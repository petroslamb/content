# Proof: Phase 2 Primary Topic Discovery

**Status:** `flagship proof`

This folder indexes the first Phase 2 governed `content-agent` proof pass that starts from `topic_discovery`, admits runtime inputs, produces declared discovery packet surfaces, passes the `topic_viability` packet check, continues after explicit user approval, initializes the approved package, and stops again at the next durable lifecycle review gate.

## Scenario

The run starts from the user instruction to begin at topic discovery and continue until a gate. It uses the existing `literate-workflow-programming` umbrella as package context and tests whether the next publishable object should be opened around governed proof runs.

The first stop was the `topic_viability` lifecycle gate for `proof-runs-as-source-surface`. The user then approved that gate, the run resumed, the package was initialized from the handoff packet, and the research pass continued until the pending `research_exit` lifecycle gate.

## Why This Proof Matters

This is the first retained proof for the new Phase 2 local governed-runtime baseline. It adds evidence for:

- `content-agent run` admitting runtime inputs through `--input`
- declared workflow contracts rendering output targets with the resolved `run_id`
- deterministic topic discovery with alphaXiv before handoff
- `topic_viability` packet validation through `content-agent gate check`
- durable resolved-run, run-record, and review-gate YAML evidence
- a hard stop at lifecycle approval instead of unapproved package initialization
- explicit gate approval and resume evidence before package initialization
- a second governed stop at `research_exit` before essay iteration

## Source Evidence

- Resolved run: [`../../../resolved-runs/phase-2-primary-topic-discovery-proof.yaml`](../../../resolved-runs/phase-2-primary-topic-discovery-proof.yaml)
- Run record: [`../../../logs/phase-2-primary-topic-discovery-proof.yaml`](../../../logs/phase-2-primary-topic-discovery-proof.yaml)
- Review gate: [`../../../gates/gate-phase-2-primary-topic-discovery-proof-topic-viability.yaml`](../../../gates/gate-phase-2-primary-topic-discovery-proof-topic-viability.yaml)
- Gate check log: [`../../../logs/2026-05-06_20-14-02_no-package_topic_viability_gate-check.json`](../../../logs/2026-05-06_20-14-02_no-package_topic_viability_gate-check.json)
- Approval run record: [`../../../logs/run-2026-05-06T19-55-02Z-literate-workflow-programming-review-approve-topic-viability-2026-05-06t17-14-12z.yaml`](../../../logs/run-2026-05-06T19-55-02Z-literate-workflow-programming-review-approve-topic-viability-2026-05-06t17-14-12z.yaml)
- Resume run record: [`../../../logs/run-2026-05-06T19-55-11Z-literate-workflow-programming-resume-topic-viability-2026-05-06t17-14-12z.yaml`](../../../logs/run-2026-05-06T19-55-11Z-literate-workflow-programming-resume-topic-viability-2026-05-06t17-14-12z.yaml)
- Topic vocabulary map: [`../../../logs/phase-2-primary-topic-discovery-proof-topic-vocabulary-map.md`](../../../logs/phase-2-primary-topic-discovery-proof-topic-vocabulary-map.md)
- Candidate paper pool: [`../../../logs/phase-2-primary-topic-discovery-proof-candidate-paper-pool.md`](../../../logs/phase-2-primary-topic-discovery-proof-candidate-paper-pool.md)
- Candidate essay slate: [`../../../logs/phase-2-primary-topic-discovery-proof-candidate-essay-slate.md`](../../../logs/phase-2-primary-topic-discovery-proof-candidate-essay-slate.md)
- Handoff packet: [`../../../logs/phase-2-primary-topic-discovery-proof-topic-discovery-handoff.md`](../../../logs/phase-2-primary-topic-discovery-proof-topic-discovery-handoff.md)
- Initialized package: [`../../../../publications/proof-runs-as-source-surface/README.md`](../../../../publications/proof-runs-as-source-surface/README.md)
- Research resolved run: [`../../../resolved-runs/phase-2-primary-research-exit-proof.yaml`](../../../resolved-runs/phase-2-primary-research-exit-proof.yaml)
- Research run record: [`../../../logs/phase-2-primary-research-exit-proof.yaml`](../../../logs/phase-2-primary-research-exit-proof.yaml)
- Research review gate: [`../../../gates/gate-phase-2-primary-research-exit-proof-research-exit.yaml`](../../../gates/gate-phase-2-primary-research-exit-proof-research-exit.yaml)
- Research gate check log: [`../../../logs/2026-05-06_22-59-28_proof-runs-as-source-surface_research_exit_gate-check.json`](../../../logs/2026-05-06_22-59-28_proof-runs-as-source-surface_research_exit_gate-check.json)

## Run Outcome

- Runtime inputs were admitted and recorded:
  - `discovery_trigger=primary proof for autonomous content-agent publication workflows and specification-surface governed runtime`
  - `target_publication_ambition=north_star_flagship`
- The handoff decision is `package_init_ready`.
- The proposed package slug is `proof-runs-as-source-surface`.
- `./content-agent gate check --gate topic_viability --packet <handoff>` passed.
- `./content-agent run --workflow topic_discovery ... --start-at decide_handoff` wrote a pending review gate and stopped with `terminal_status: gated`.
- `./content-agent review approve --gate topic_viability-2026-05-06T17-14-12Z ...` recorded explicit lifecycle approval.
- `./content-agent resume --gate topic_viability-2026-05-06T17-14-12Z` recorded the resume boundary.
- `npm run package:init -- --from-topic-packet <handoff>` initialized `publications/proof-runs-as-source-surface/`.
- `./content-agent run --workflow research ... --start-at settle_research_exit_gate` wrote a pending `research_exit` review gate and stopped with `terminal_status: gated`.

## What This Proves

This proves that the Phase 2 runtime can support a real governed topic-discovery-to-research pass using the new primary surfaces: `workflow.yaml`, package `status.yaml`, root policy/profile/gate YAMLs, and Reviewable Runs evidence.

It does not prove full autonomous publication reliability, external mutation safety, or automatic essay iteration. Those remain gated follow-on claims.
