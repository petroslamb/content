# Workflows

This directory contains reusable workflows that guide task execution. These workflows were migrated from [Claude Skills](https://github.com/petekp/claude-skills) to make them accessible to Antigravity.

## How to Use Workflows

To use a workflow, reference it by name in your request to the AI assistant. For example:
- "Use the model-first-reasoning workflow to build this feature"
- "Apply the design-critique workflow to this UI"
- "Follow the tutorial-writing workflow to create a guide for X"

## Available Workflows

### 🧠 Thinking & Reasoning

#### `model-first-reasoning.md`
Apply Model-First Reasoning (MFR) methodology for complex code generation. Creates explicit problem models before implementation to reduce hallucinations and ensure correctness.

**Use for:** State machines, constraint systems, complex business logic, safety-critical features

#### `stress-testing.md`
Stress-test plans, proposals, and strategies through pre-mortems and devil's advocate analysis.

**Use for:** Evaluating business ideas, identifying failure modes, risk registers, assumption audits

#### `dreaming.md`
Think expansively and imaginatively without practical constraints. Break assumptions and envision ideal futures.

**Use for:** Brainstorming, challenging assumptions, exploring possibilities, breaking out of incremental thinking

#### `wise-novice.md`
Approach problems with beginner's mind while asking penetrating questions.

**Use for:** Fresh perspectives, simplifying complexity, challenging expert assumptions

---

### 🎨 Design & UX

#### `design-critique.md`
Critique UI/UX designs for clarity, hierarchy, interaction, accessibility, and craft.

**Use for:** Design reviews, PR feedback on UI, evaluating mockups, checking if components are ship-ready

#### `interaction-design.md`
Apply interaction design principles for intuitive, responsive interfaces.

**Use for:** Component behaviors, micro-interactions, loading states, transitions, user flows

####`typography.md`
Apply professional typography principles for readable, hierarchical, refined interfaces.

**Use for:** Type scales, font selection, spacing, text-heavy layouts, readability

#### `ux-writing.md`
Write clear, helpful, human interface copy.

**Use for:** Microcopy, error messages, button labels, empty states, onboarding flows, tooltips

#### `cognitive-foundations.md`
Apply cognitive science and HCI research to design decisions.

**Use for:** Understanding user behavior, evaluating cognitive load, grounding designs in research

---

### 🛠️ Product & Strategy

#### `startup-wisdom.md`
Apply startup execution wisdom to product, strategy, and business decisions.

**Use for:** Feature prioritization, build-vs-buy decisions, go-to-market planning, reality-checking timelines

#### `oss-product-manager.md`
Navigate open source product strategy, community dynamics, and sustainable maintenance.

**Use for:** OSS releases, managing contributors, community expectations, balancing commercial/community interests

---

### 📚 Learning & Teaching

#### `tutorial-writing.md`
Generate comprehensive implementation tutorial documents with deep background, context, and step-by-step milestones.

**Use for:** Creating guides instead of direct code changes, enabling learning-by-building

**Philosophy:** Addresses the pain of reviewing AI-generated PRs by creating teaching documents that keep developers connected to their work.

---

### 🔧 Technical Expertise

#### `unix-macos-engineer.md`
Expert Unix and macOS systems engineering for shell scripting, system administration, and command-line tools.

**Use for:** Shell scripts, system configuration, process management, networking, troubleshooting

---

## Workflow Structure

Workflows come in two formats:

### Simple Workflows
Single markdown files in the root directory:
```
.agent/workflows/
├── dreaming.md
├── startup-wisdom.md
└── ...
```

### Workflows with Supporting Materials
Subdirectories containing the main workflow and reference files:
```
.agent/workflows/
├── cognitive-foundations/
│   ├── workflow.md          # Main workflow
│   ├── PSYCHOLOGY.md         # Deep-dive on cognitive psychology
│   └── HCI-THEORY.md         # Human-Computer Interaction theory
├── design-critique/
│   ├── workflow.md           # Main workflow
│   ├── CHECKLIST.md          # Quick review checklist
│   └── PRINCIPLES.md         # Detailed critique principles
└── model-first-reasoning/
    ├── workflow.md           # Main workflow
    ├── MODEL_TEMPLATE.json   # JSON template for formal models
    ├── Model-First Reasoning LLM Agents.md  # Research paper
    └── scripts/
        └── validate-model.py # Model validation script
```

### Workflow Format
Each workflow file follows this structure:

```markdown
---
description: [When and how to use this workflow]
---

# Workflow Title

[Detailed guidance, principles, frameworks, and examples]
```

## Creating Custom Workflows

To add your own workflow:

1. Create a new file in `.agent/workflows/your-workflow-name.md`
2. Add YAML frontmatter with a `description` field
3. Write detailed, actionable guidance for the workflow
4. Reference the workflow in your AI assistant requests

## Credits

These workflows were adapted from the [claude-skills repository](https://github.com/petekp/claude-skills) created by [@petekp](https://github.com/petekp).

## License

MIT (inherited from source repository)
