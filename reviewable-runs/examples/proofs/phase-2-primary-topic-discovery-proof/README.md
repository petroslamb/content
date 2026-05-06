# Proof: Phase 2 Primary Topic Discovery

**Status:** `flagship proof`

This folder indexes the first Phase 2 governed `content-agent` proof pass that starts from `topic_discovery`, admits runtime inputs, produces declared discovery packet surfaces, passes the `topic_viability` packet check, continues after explicit user approval, initializes the approved package, clears research and prewrite gates, writes a bounded essay-iteration packet, and stops at the next durable promotion-aware review gate.

## Scenario

The run starts from the user instruction to begin at topic discovery and continue until a gate. It uses the existing `literate-workflow-programming` umbrella as package context and tests whether the next publishable object should be opened around governed proof runs.

The first stop was the `topic_viability` lifecycle gate for `proof-runs-as-source-surface`. The user then approved that gate, the run resumed, the package was initialized from the handoff packet, and the research pass stopped at `research_exit`. After that approval, the package admitted the primary paper shortlist locally, seeded an essay-iteration packet, cleared `essay_prewrite`, wrote a bounded candidate and review packet, and stopped at the pending `replacement_north_star` gate. That final gate is intentionally not approved in this proof packet because it carries lifecycle and promotion dimensions while the packet decision remains `draft_only`.

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
- package-local paper intake and claim-boundary evidence before drafting
- essay-iteration scaffold, prewrite validation, gate approval, and resume evidence
- a bounded candidate packet that passes `replacement_north_star` checks while still stopping before promotion

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
- Research approval run record: [`../../../logs/run-2026-05-06T20-33-55Z-proof-runs-as-source-surface-review-approve-research-exit-2026-05-06t19-59-47z.yaml`](../../../logs/run-2026-05-06T20-33-55Z-proof-runs-as-source-surface-review-approve-research-exit-2026-05-06t19-59-47z.yaml)
- Research resume run record: [`../../../logs/run-2026-05-06T20-34-00Z-proof-runs-as-source-surface-resume-research-exit-2026-05-06t19-59-47z.yaml`](../../../logs/run-2026-05-06T20-34-00Z-proof-runs-as-source-surface-resume-research-exit-2026-05-06t19-59-47z.yaml)
- Paper index with local intake links: [`../../../../publications/proof-runs-as-source-surface/papers/index.md`](../../../../publications/proof-runs-as-source-surface/papers/index.md)
- Claim-boundary ledger: [`../../../../publications/proof-runs-as-source-surface/proof-runs-as-source-surface-claim-boundary-ledger-r1.md`](../../../../publications/proof-runs-as-source-surface/proof-runs-as-source-surface-claim-boundary-ledger-r1.md)
- Essay scaffold resolved run: [`../../../resolved-runs/phase-2-primary-essay-scaffold-proof.yaml`](../../../resolved-runs/phase-2-primary-essay-scaffold-proof.yaml)
- Essay scaffold run record: [`../../../logs/phase-2-primary-essay-scaffold-proof.yaml`](../../../logs/phase-2-primary-essay-scaffold-proof.yaml)
- Essay prewrite resolved run: [`../../../resolved-runs/phase-2-primary-essay-prewrite-proof.yaml`](../../../resolved-runs/phase-2-primary-essay-prewrite-proof.yaml)
- Essay prewrite run record: [`../../../logs/phase-2-primary-essay-prewrite-proof.yaml`](../../../logs/phase-2-primary-essay-prewrite-proof.yaml)
- Essay prewrite review gate: [`../../../gates/gate-phase-2-primary-essay-prewrite-proof-essay-prewrite.yaml`](../../../gates/gate-phase-2-primary-essay-prewrite-proof-essay-prewrite.yaml)
- Essay prewrite gate check log: [`../../../logs/2026-05-06_23-42-21_proof-runs-as-source-surface_essay_prewrite_gate-check.json`](../../../logs/2026-05-06_23-42-21_proof-runs-as-source-surface_essay_prewrite_gate-check.json)
- Essay prewrite approval run record: [`../../../logs/run-2026-05-06T20-42-45Z-proof-runs-as-source-surface-review-approve-essay-prewrite-2026-05-06t20-42-36z.yaml`](../../../logs/run-2026-05-06T20-42-45Z-proof-runs-as-source-surface-review-approve-essay-prewrite-2026-05-06t20-42-36z.yaml)
- Essay prewrite resume run record: [`../../../logs/run-2026-05-06T20-42-50Z-proof-runs-as-source-surface-resume-essay-prewrite-2026-05-06t20-42-36z.yaml`](../../../logs/run-2026-05-06T20-42-50Z-proof-runs-as-source-surface-resume-essay-prewrite-2026-05-06t20-42-36z.yaml)
- Candidate draft: [`../../../../publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md`](../../../../publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-candidate-r1.md)
- Replacement review: [`../../../../publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-replacement-review-r1.md`](../../../../publications/proof-runs-as-source-surface/iterations/r1/proof-runs-as-source-surface-replacement-review-r1.md)
- Replacement gate check log: [`../../../logs/2026-05-06_23-46-22_proof-runs-as-source-surface_replacement_north_star_gate-check.json`](../../../logs/2026-05-06_23-46-22_proof-runs-as-source-surface_replacement_north_star_gate-check.json)
- Replacement resolved run: [`../../../resolved-runs/phase-2-primary-replacement-north-star-proof.yaml`](../../../resolved-runs/phase-2-primary-replacement-north-star-proof.yaml)
- Replacement run record: [`../../../logs/phase-2-primary-replacement-north-star-proof.yaml`](../../../logs/phase-2-primary-replacement-north-star-proof.yaml)
- Replacement review gate: [`../../../gates/gate-phase-2-primary-replacement-north-star-proof-replacement-north-star.yaml`](../../../gates/gate-phase-2-primary-replacement-north-star-proof-replacement-north-star.yaml)

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
- `./content-agent review approve --gate research_exit-2026-05-06T19-59-47Z ...` recorded explicit research-exit approval, and `./content-agent resume --gate research_exit-2026-05-06T19-59-47Z` recorded the resume boundary.
- The primary paper shortlist was downloaded into the package and converted to markdown under `papers/markdown/`.
- `./content-agent run --workflow essay_iteration ...` seeded the essay packet and deferred before blueprint hardening.
- `npm run check:essay-prewrite -- --package proof-runs-as-source-surface` and `./content-agent gate check --gate essay_prewrite --package proof-runs-as-source-surface` passed.
- `./content-agent run --workflow essay_iteration ... --start-at settle_prewrite_gate` wrote a pending `essay_prewrite` gate; approval and resume were recorded before candidate drafting.
- `npm run check:essay-iteration -- --package proof-runs-as-source-surface` and `./content-agent gate check --gate replacement_north_star --package proof-runs-as-source-surface` passed.
- `./content-agent run --workflow essay_iteration ... --start-at stop_at_replacement_decision` wrote a pending `replacement_north_star` gate and stopped with `terminal_status: gated`.

## What This Proves

This proves that the Phase 2 runtime can support a real governed topic-discovery-to-essay-packet pass using the new primary surfaces: `workflow.yaml`, package `status.yaml`, root policy/profile/gate YAMLs, and Reviewable Runs evidence.

It does not prove full autonomous publication reliability, external mutation safety, or automatic promotion. The current proof stops at a pending promotion-aware `replacement_north_star` gate, with the packet decision still blocking live-draft replacement under `judgment_policy: draft_only`.
