# Two-Page Spine — *Why Transformers Work: A Convergent Synthesis*

This is the “read this first” spine extracted from `why_transformers_work_a_convergent_synthesis.md`.

---

## The one-line claim (capability, not dominance)

In the current decoder-only regime, LLM capability is best explained by a **small set of discoverable bottlenecks** implementing a minimal **Retrieve → Compile → Execute** pipeline (plus the training dynamics that reliably find and stabilize those bottlenecks).

## What “regime” means here (substrate assumptions)

This note is conditional on the mainstream setup:

- a **causal autoregressive decoder** (tokens only access prior tokens; generation is next-token sampling/decoding);
- **next-token prediction** training at every position;
- a deep residual stack (the **residual stream as a per-token workspace/highway**) + a tokenwise nonlinear “executor” step;
- gradient-based training via backprop (Adam/SGD-family);
- practical constraints where throughput/latency and GPU kernels shape what survives.

These are not “requirements” in the R-sense; they define the playing field.

## The core capability bundle (what must be implemented on top of the substrate)

We use four core requirements. Each is intended to be **implementation-agnostic** (Transformers are one implementation).

| Capability | What it must do (operational) | Why we think it’s load-bearing |
|---|---|---|
| **R0 — Executor + parametric substrate** | perform high-capacity **tokenwise rewrites** on a persistent workspace, using learned features/skills stored in weights | without a strong executor substrate, “mixed” information doesn’t reliably become brittle, correct outputs |
| **R1 — Sharp contextual readout** | retrieve/extract/copy from token-indexed in-prompt memory with **low-entropy selection** (G&A / sharp aggregation) | small probability leaks become format errors; evidence localizes to sparse causal heads |
| **R2 — Prompt compiler** | infer a task/hypothesis/program from in-prompt examples/instructions and make it causally drive behavior (FV/task-vector-like mechanisms) | few-shot behavior is not just copying; it requires a control signal that modulates execution |
| **R4 — Discoverability** | training reliably finds/stabilizes the sparse bottlenecks implementing R0–R2 (phase structure / circuit selection) | explains why these mechanisms appear late, concentrate in small circuits, and become causal |

**R3 (Extended):** “meso-level switchboard / subroutine switching” is kept as an extended hypothesis until it has a distinct causal signature beyond (a) token routing in R1 and (b) feature gating in R0.

## The working model families (F1–F3) and our current best-effort choice

We do not claim the causal pipeline is proven. We adopt a working model because it yields **distinct diagnostics** and **switch conditions**.

- **F1 (current default):** **Two-interface bottleneck** — an **evidence interface** (R1) plus a **program interface** (R2) feed an executor (R0).  
  *Signature:* **double dissociation + selective rescue** should exist (evidence can fail while program holds, and vice versa).
- **F2:** **Unified online update** — retrieval + adaptation are one primitive; robust double dissociation should fail.
- **F3:** **Parametric-first executor** — capability deltas mostly track R0 interventions/capacity allocation rather than sharp contextual readout bottlenecks.

Within F1, we use the minimal spine **Retrieve → Compile → Execute**, while explicitly noting that “Retrieve” often decomposes into **Gather → Select (aggregate)** (per the G&A evidence).

## The strongest empirical anchors (what the evidence bundle forces)

If you read nothing else, these are the load-bearing constraints:

- **R1 is sparse and causal:** a small subset of retrieval/G&A heads dominate long-context factuality and strict-format extraction; targeted interventions can collapse accuracy to random baselines. (Wu et al., 2024; Bick et al., 2025)
- **R2 has a concrete circuit family:** FV heads are a main causal driver of few-shot performance at scale, emerging later than induction scaffolding. (Yin & Steinhardt, 2025)
- **Memory scaling matters:** Transformers can implement copying/retrieval behaviors that fixed-state models cannot without memory scaling with length. (Jelassi et al., 2024)
- **Dominance ≠ capability:** the ecosystem has made attention kernels extremely efficient; this explains lock-in, not mechanistic necessity. (Dao et al., 2023)

## What would change our minds (pre-registered switch conditions)

- **Against F1 (toward F2):** repeated attempts to produce a clean **double dissociation** fail (program/evidence failures always track), and FV effects collapse into pure retrieval/copy accounts under better probes.
- **Against F1 (toward F3):** context-only tasks show weak sensitivity to contextual-readout bottlenecks but strong, selective sensitivity to executor/parametric interventions (beyond generic language degradation).
- **Against the bundle as a discriminator:** a non-attention family matches strict-format retrieval/extraction *and* shows no sharp aggregation bottleneck under G&A-style interventions without reintroducing an attention-like lookup elsewhere.

## Minimal diagnostic suite (what we need next)

- **R0:** **TODO** retrieval-intact / execution-broken dissociation (context-only), plus matched-budget executor-path interventions.
- **R1:** G&A-style aggregation probes (answer-letter-only multiple choice; strict extraction; needle-in-haystack), plus retrieval-head masking vs random masking.
- **R2:** few-shot probes with FV/induction controls; measure both few-shot accuracy and token-loss difference.
- **R4:** checkpoint runs and track circuit emergence timelines; test whether pruning/regularization shifts when bottlenecks appear.
- **R3 (promotion tests):** only after R0/R1/R2 are nailed down.

## How to read the rest

- §0 is the evidence-forced executive summary.
- §3 lists the **bottlenecks we can actually point to** and introduces the working model families.
- §4 defines the **core bundle** (R0/R1/R2/R4) and keeps R3 explicitly extended.
- §7 lists the falsification suite (what would make the story die).

