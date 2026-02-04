# Paper-to-Article Playbook

> **Purpose:** A reusable methodology for transforming any research paper into a publication-ready, multi-part article series—avoiding the mistakes made during the ToolOrchestra project.

---

## The 6-Phase Process

```
Phase 1: RESEARCH      → Build the knowledge foundation
Phase 2: STRATEGY      → Lock structure, voice, and distribution
Phase 3: MODELING      → Outline before writing
Phase 4: DRAFTING      → Write against the rubric
Phase 5: VERIFICATION  → Audit before publishing
Phase 6: DISTRIBUTION  → Execute promotion plan
```

---

## Phase 1: RESEARCH (Week 1)

**Goal:** Understand the paper deeply before writing a single word.

### Checklist
- [ ] Download the paper and all references
- [ ] Create a `papers/` directory with PDFs and markdown conversions
- [ ] Read the paper 2-3 times, annotating key claims
- [ ] Identify: What's novel? What's incremental? What's missing?
- [ ] Create an Annotated Bibliography (v0)

**Artifacts:**
- `papers/` directory with all source material
- `annotated_bibliography.md` (initial version)

---

## Phase 2: STRATEGY (Week 1, Parallel)

**Goal:** Lock all structural decisions BEFORE drafting.

### Checklist
- [ ] Define Target Audience (persona, expertise level)
- [ ] Define Distribution Channels (Substack, YouTube, LinkedIn, etc.)
- [ ] Define Series Structure (# of parts, bundling strategy)
- [ ] Define Voice/Persona (use `rigor_rubric_template.md`)
- [ ] Define Promotion Plan (use `promotion_checklist.md`)

**Artifacts:**
- `rigor_rubric.md` (adapted from template)
- `series_structure.md` (parts, bundles, target per bundle)
- `promotion_plan.md` (channels, timing, targets)

**CRITICAL:** Do not proceed to Phase 3 until structure is locked.

---

## Phase 3: MODELING (Week 2)

**Goal:** Outline every part before writing prose.

### Checklist
- [ ] Write detailed outline for each Part (sections, key claims, diagrams needed)
- [ ] Map dependencies between Parts
- [ ] Identify where diagrams/visuals are required
- [ ] Complete the Skeptic's Checklist for each major claim
- [ ] Review structure one final time—no changes after this

**Artifacts:**
- `outline/part_XX_outline.md` for each part
- `skeptics_checklist.md` (one per part or one master file)

---

## Phase 4: DRAFTING (Weeks 3-4)

**Goal:** Write against the rubric. No structural changes.

### Checklist
- [ ] Write each Part following its outline
- [ ] Apply the Rigor Rubric to every paragraph
- [ ] Insert diagrams/visuals as placeholders if not ready
- [ ] Avoid LLM-tell language, em-dashes, and fluff
- [ ] Mark sections requiring citation verification

**Rules:**
- No new Parts added
- No structural reorganization
- If you find a structural problem, log it—don't fix it mid-draft

---

## Phase 5: VERIFICATION (Week 5)

**Goal:** Audit for accuracy, style, and completeness.

### Checklist
- [ ] Citation audit: verify all claims against source papers
- [ ] Skeptic's Checklist review: did you address failure modes?
- [ ] Style pass: apply rubric, remove violations
- [ ] Bundling: combine parts into publishable Issues
- [ ] Polish pass: final read for coherence

**Artifacts:**
- `synthesis_assessment.md` (honest self-evaluation)
- `final_bundles/` (ready-to-publish files)

---

## Phase 6: DISTRIBUTION (Week 5, Parallel)

**Goal:** Execute the pre-planned promotion.

### Checklist
- [ ] Publish to primary platform (Substack, etc.)
- [ ] Cross-post summaries (LinkedIn, Twitter, etc.)
- [ ] Execute author outreach (if applicable)
- [ ] Execute community posting (Reddit, HN, Discord)
- [ ] Track traction and iterate

**Artifacts:**
- `promotion_log.md` (what was sent, responses received)

---

## Templates (Companion Files)

| File | Purpose |
|---|---|
| `rigor_rubric_template.md` | Define your voice and evaluation signals |
| `skeptics_checklist_template.md` | Challenge every major claim |
| `bundling_strategy_template.md` | Define how parts combine into Issues |
| `promotion_checklist_template.md` | Pre-plan distribution channels |

---

## Lessons Learned (From ToolOrchestra)

| Mistake | Prevention |
|---|---|
| Wrote 13 parts before bundling | Lock structure in Phase 2 |
| Rubric created mid-project | Create rubric as Step 0 |
| Citations verified late | Build `papers/` in Phase 1 |
| Promotion was an afterthought | Plan promotion in Phase 2 |
| Tool migrations mid-stream | Freeze tooling before Phase 4 |

---

*This playbook is derived from the ToolOrchestra post-mortem. Adapt as needed for your project.*
