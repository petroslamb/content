# Strategic Plan: From Content Repo to Agentic Content SaaS

> _Based on repo audit, April 6, 2026. Starting point: Level 2 automation (tool-assisted, human-glued)._

---

## The Core Thesis

You are not building a content repo. You are — whether you intended to or not — building the **operating system for thoughtful, research-backed AI content production**. The workflows, skills, scripts, and vocabulary (`live draft`, `blueprint`, `claims`, `reviewable-runs`) are not just personal habits. They are the **primitives of a product**.

The path from here to SaaS is not a pivot. It is the same work, done in a way that separates "what you know" from "only you can run it."

This plan has four phases with explicit gates. You should not move through a gate until it is honest.

---

## Phase 1 — The Clean Machine _(0–3 months)_

**Goal**: Zero orphan scripts. One interface. Any article can be run start-to-finish by an agent — no hand-holding.

This is pure internal engineering. No new features. No SaaS thinking. Just turning your toolbox into a product you would trust someone else to run.

### Milestones

#### M1.1 — Kill the Root Scripts
Move every `.py` file from the project root (`render_illusion_of_swarm.py`, `upload_binding_gap_shorts.py`, `upload_binding_gap_tldrs.py`, `list_latest_videos.py`) into the `scripts/` folder or the relevant skill. No publication name may appear in a script filename. Publication name becomes a required CLI argument.

**Deliverable**: `git rm` + renamed/generalized versions committed.

#### M1.2 — Publication Lifecycle Manifest
Add a `status.yaml` to every publication package. Define the canonical stages from the 7-step lifecycle (paper-intake → research → draft → notebooklm → polish → publish → archive-sync). Each stage has a `done: true/false` flag and a `last_updated` timestamp.

**Deliverable**: `scripts/check_status.py` that prints a lifecycle table for all publications. `npm run status` entry point.

```yaml
# Example: publications/binding-gap/status.yaml
publication: binding-gap
stages:
  paper_intake: { done: true, last_updated: "2026-03-15" }
  alphaxiv_research: { done: true, last_updated: "2026-03-20" }
  essay_iteration: { done: true, last_updated: "2026-04-02" }
  notebooklm_artifacts: { done: true, last_updated: "2026-04-01" }
  article_polish: { done: true, last_updated: "2026-04-03" }
  substack_publish: { done: true, last_updated: "2026-04-04" }
  archive_sync: { done: false }
```

#### M1.3 — The Generic `run` Interface
Write a single `scripts/run_stage.py --package <name> --stage <stage>` dispatcher. It reads `status.yaml`, resolves the correct skill/script for the stage, runs it, and updates `status.yaml` on success.

**Deliverable**: You can say `python scripts/run_stage.py --package illusion-of-swarm --stage notebooklm_artifacts` and it executes without instructions.

#### M1.4 — Reviewable Runs Integration
Every `run_stage.py` execution should write a lightweight run record to `reviewable-runs/examples/proofs/` using your existing framework. This transforms the "Reviewable Runs" concept package into live operational infrastructure.

**Deliverable**: Every automated stage produces a `task_spec.md` + `execution_trace.md` pair automatically. The framework is no longer just a publication — it's the audit log.

---

### Phase 1 Gate Criteria
> [!IMPORTANT]
> **Do not enter Phase 2 until you can honestly answer YES to all of these:**
> 1. Can I describe the status of every publication in one command?
> 2. Can another agent (or a future employee) pick up any half-finished package and know exactly where it is?
> 3. Are there zero scripts that mention a specific essay name?

---

## Phase 2 — The Agentic Platform _(3–9 months)_

**Goal**: The agent runs the lifecycle. You review outcomes, not steps. Human-in-the-loop only at creative and quality gates.

This phase converts documentation-as-workflows into executable workflows with real agent orchestration. You start using the tools you've built about agents to *build agents*.

### Milestones

#### M2.1 — The `content-agent` CLI
Build a proper Python package (not a loose script) named `content-agent`. It wraps all existing scripts with a clean API surface:

```
content-agent run --package binding-gap --stage polish
content-agent status
content-agent init --package new-essay-name
content-agent publish --package binding-gap
```

This CLI becomes the **single interface** you and any future tool, agent, or integration communicates through.

#### M2.2 — Agent-Runnable Workflow Definitions
Convert each `workflows/*/README.md` human playbook into a machine-readable `workflow.yaml` alongside the doc. A `workflow.yaml` defines:
- steps (ordered)
- required tools/scripts for each step
- human approval gates (which steps require user sign-off)
- automated verification (what does "done" look like?)

**Deliverable**: `content-agent run` executes all non-gated steps autonomously and pauses at gate points.

#### M2.3 — The Review Gate Protocol
Define the human-in-the-loop contract explicitly. Two classes:
- **Auto-run gates**: Script runs, output stored, stage marked done. (e.g., paper conversion, archive sync)
- **Human review gates**: Agent runs the work, presents a diff/preview, waits for approval. (e.g., essay draft review, cue sheet alignment, Substack publish)

The "waiting" mechanism should be a local web dashboard (a minimal Next.js/Flask app showing pending reviews), not a terminal prompt you have to babysit.

#### M2.4 — The Local Dashboard (v0)
A minimal web UI at `localhost:3001` that shows:
- Publication fleet status (lifecycle stage per essay)
- Pending human-review gates
- Last 5 run records from reviewable-runs

This is **not** a SaaS yet. This is your own cockpit. It runs locally, talks to the local filesystem.

#### M2.5 — Voice + Style Automation
AutoCheck: On every essay at the Article Polish stage, the agent must automatically score the draft against `voice_consistency_guide.md` and produce a structured violation report (ban list violations, rhythm deviations). No more manual audits.

**Deliverable**: `content-agent run --stage voice_check` produces a machine-readable compliance report.

---

### Phase 2 Gate Criteria
> [!IMPORTANT]
> **Do not enter Phase 3 until you can honestly answer YES to all of these:**
> 1. Can you go from "I have an idea and a title" to "draft ready for final review" without touching a command line?
> 2. Are pending reviews visible in a dashboard — not buried in terminal logs?
> 3. Has the agent successfully completed at least 3 full essay lifecycles, start to finish, with no process errors?

---

## Phase 3 — The Multi-Tenant Infrastructure _(9–18 months)_

**Goal**: What works for one creator (you) works for ten creators. The system can handle multiple publication identities, separate authentication, and isolated content spaces.

This is the architectural pivot. You are no longer building "my content tool." You are building "the content tool."

### Milestones

#### M3.1 — Workspace Isolation
Refactor the `content-agent` package to be **workspace-aware**. A workspace is not a git repo — it is a configuration object with:
- API credentials (Substack, YouTube, NotebookLM)
- Voice guide
- Publication map
- Storage path (local or cloud)

One agent instance can manage multiple workspaces (i.e., one person with multiple Substacks, or multiple team members).

#### M3.2 — Cloud Execution Layer
Replace local `.venv` execution with a stateless execution runtime (AWS Lambda, Google Cloud Run, or a self-hosted Celery queue). The agent jobs are no longer tied to your laptop.

**Deliverable**: `content-agent run --package binding-gap --stage polish` submits a job to a queue that runs without your machine being on.

#### M3.3 — The Credential Vault
Implement proper per-workspace credential management (not `.env` files). Use a standard secrets manager (AWS Secrets Manager / local Vault in self-hosted mode). This is the prerequisite for multi-user — your API keys must be isolated from someone else's.

#### M3.4 — The Web Dashboard (v1 — Multi-User)
Evolve the local dashboard into a proper web application:
- User accounts (email + password or GitHub OAuth)
- Per-user workspace management
- Publication fleet view (all essays, all stages)
- Job queue visibility (running, queued, failed)
- Review gates with approve/reject UI (replacing the terminal prompt)

Stack decision: FastAPI (Python, reusing your existing scripts) + Next.js frontend is the natural choice given your existing Python infrastructure.

#### M3.5 — The Third-Party Integration Layer
Expose the core lifecycle as webhooks or a REST API. Target integrations:
- **Zapier/Make**: "When I add a paper to Dropbox, trigger paper-intake"
- **GitHub Actions**: "On push to `drafts/`, run voice check"
- **Notion/Obsidian webhook**: "When status changes to Ready, push to Substack"

This is what turns the product from "a content tool" into "the content backbone."

---

### Phase 3 Gate Criteria
> [!IMPORTANT]
> **Do not enter Phase 4 until:**
> 1. You (or a trusted beta user) has successfully onboarded a second writer onto the platform without you helping them run commands.
> 2. The system runs without your laptop being online.
> 3. At least one third-party integration works end-to-end.

---

## Phase 4 — The SaaS Product _(18–30 months)_

**Goal**: Charging money. The platform runs itself. You are a product builder, not an operator.

### The Market Position

The honest answer to "what is this?" is not "a Substack tool" or "a writing tool." It is:

> **"The end-to-end production system for research-backed technical content creators — from paper intake to published post, with an auditable agent doing the heavy lifting."**

The market gap is real: tools like Jasper, Copy.ai, and Beehiiv's AI features target marketing copy writers. **No product seriously serves the niche of technically rigorous, research-driven independent writers** who currently cobble together their own pipelines. You will have had 18 months of live battle-testing to prove otherwise.

Your wedge is the **"Reviewable Runs" framework** — the idea that an agent should be auditable, not a black box. This is a genuine philosophical differentiator that resonates with technical creators who are rightly skeptical of fully automated AI content.

### Milestones

#### M4.1 — Pricing Architecture
Three tiers that match your three user archetypes (from `future_publication_strategy.md`):

| Tier | Price | Target | What They Get |
| :--- | :--- | :--- | :--- |
| **Solo** | $49/mo | Individual technical writers | 3 publications, all lifecycle stages, 50 agent-hours/month |
| **Studio** | $199/mo | Small editorial teams / agencies | 20 publications, team seats, priority queue, API access |
| **Enterprise** | Custom | VC firms, research labs, media companies | Unlimited, SSO, custom voice guides, SLA |

#### M4.2 — The GTM Thesis

**Primary channel: your own publication.** The product demonstrates itself. You write the "Engineering My Own Content Platform" series. Every essay produced through the platform includes a byline: *"This essay was produced using Rooted Layers Agent."* You are the first and best case study.

**Secondary channels:**
- Substack Notes + X threads on "how I wrote X essay in 2 hours with an agent"
- HN Show HN: "I built an agent that turns academic papers into published essays"
- Conference talks at AI/ML conferences (NeurIPS, MLSys) on "Auditable AI Content Production"

**Distribution leverage**: The `reviewable-runs` framework should be open-sourced separately as a standalone library. This is the engineering community hook — it generates GitHub stars and inbound interest from a different audience than your Substack.

#### M4.3 — The Content Moat
The platform generates proprietary data:
- **Voice quality benchmarks**: How does a draft score against `voice_consistency_guide.md` before and after revision? This is trainable.
- **Source quality signals**: Which papers get cited in essays that score well? This is a dataset.
- **Lifecycle velocity data**: What is the median time from paper intake to published post? This is a benchmark no one else has.

You own this data. No competitor has 18+ months of real agentic content production runs with outcome labels.

#### M4.4 — The Exit or Sustain Decision
At this point, the business is making revenue and has defensible moat. Three realistic futures:

1. **Sustain as an indie product** (~$500K ARR, owner-operated, low stress — aligns with Option 1/2 from your `future_publication_strategy.md`)
2. **Raise a seed round** and go full platform (aligns with Option 3 — requires hiring)
3. **Acquisition target** by an existing media/publishing tools company (Ghost, Beehiiv, Substack itself) — the platform's infrastructure is directly acqui-hireable

---

## Brutally Honest Risk Assessment

| Risk | Severity | Mitigation |
| :--- | :--- | :--- |
| **You never finish Phase 1** | High | Phase 1 is internal-only. No market pressure. The only risk is losing motivation. Time-box it to 90 days. |
| **The market is "just for you"** | Medium | Validate with 3 beta users in Phase 2 before building multi-tenant. If no one else wants it, you still have a great personal tool. |
| **The third-party API problem** | High | Substack, YouTube, and NotebookLM APIs are all unofficial or limited. Any one of them can break. Abstract behind your own service layer so a broken API is a skill swap, not a product failure. |
| **AI commoditizes writing assistance** | Medium | The moat is not "AI writes essays." The moat is "research-grounded, auditable, voice-consistent production." That's a process moat, not a model moat. |
| **You compete with Cursor/Windsurf for developers** | Low | Different user. You are targeting the writer who thinks like an engineer, not the engineer who wants to write. |

---

## The Single Most Important Next Step

Start Phase 1, milestone M1.2 — the `status.yaml` per publication.

It costs you 2 hours. It gives you immediate operational clarity. It is the seed from which every downstream automation grows. Nothing in Phase 2 or beyond is possible without knowing "where is each essay in the lifecycle?"

The `reviewable-runs` framework you already have tells you *how* an agent should be audited. The `status.yaml` system tells you *what* there is to run. Together they form the nucleus of the product.
