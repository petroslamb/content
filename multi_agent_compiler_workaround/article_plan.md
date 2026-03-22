# Multi-Agent Substack Article Plan

## Source Material

5 shortlisted papers from the last 90 days of multi-agent systems research, surfaced via alphaXiv CLI and ranked by novelty, practical impact, and lasting relevance.

| # | Paper | Core Contribution |
|---|---|---|
| 1 | [ROMA](https://arxiv.org/abs/2602.01848) | Recursive modular architecture for long-horizon multi-agent systems |
| 2 | [Single-Agent with Skills vs MAS](https://arxiv.org/abs/2601.04748) | When multi-agent structure is unnecessary—and when it fails |
| 3 | [EmCoop](https://arxiv.org/abs/2603.00349) | Benchmark for embodied cooperation among LLM agents |
| 4 | [Vision Wormhole](https://arxiv.org/abs/2602.15382) | Latent-space communication replacing text in heterogeneous MAS |
| 5 | [Intelligent AI Delegation](https://arxiv.org/abs/2602.11865) | Governance/trust framework for delegation in agent networks |

---

## Brainstorm: 6 Candidate Article Angles

### Angle A: "The Compiler Thesis"
**Headline idea:** *Multi-Agent Systems Are a Compile Target, Not an Architecture*

**Core argument:** The most important recent finding in multi-agent research isn't a new framework—it's that multi-agent systems can be *compiled away*. Paper `2601.04748` shows that MAS can be faithfully reduced to a single agent with a skill library, cutting 54% of tokens and 50% of latency. But the compiler breaks: skill selection hits a cognitive phase transition at ~80–90 skills, governed by semantic confusability, not complexity. This means MAS structure isn't about capability—it's about *disambiguation at scale*. Multi-agent architectures are the compiler's escape hatch for when the single-agent action space gets too crowded.

**Why it's fresh:** Everyone writes about how to build better multi-agent systems. Almost nobody asks *when you should delete them instead*. This inverts the default narrative: MAS is the cost you pay when your skill library gets too big, not a feature you add when your task gets too hard.

**Evidence density:** Strong. `2601.04748` provides concrete numbers (53.7% token reduction, phase transition at κ≈83–92, 7–30% accuracy drop per semantic competitor). ROMA provides the counterpoint: when you *do* need MAS, recursive decomposition is the pattern that scales. The tension between these two papers is the article's engine.

**Reading the paper gives you:** A new mental model. Instead of "should I use multi-agent?", the question becomes "has my action space crossed the disambiguation threshold?"

---

### Angle B: "The Five Unsolved Problems"
**Headline idea:** *Five Problems That Will Define Multi-Agent AI in 2026*

**Core argument:** Map each of the 5 papers to one *unsolved problem* in multi-agent systems, and argue that these five problems form a complete stack—from architecture to evaluation:
1. **The Horizon Problem** (ROMA) — How do you scale reasoning depth without context collapse?
2. **The Identity Problem** (Single-Agent vs MAS) — When is agent structure load-bearing and when is it ceremony?
3. **The Measurement Problem** (EmCoop) — How do you evaluate cooperation quality, not just task completion?
4. **The Babel Problem** (Vision Wormhole) — Can agents communicate without text, and should they?
5. **The Trust Problem** (Intelligent AI Delegation) — Who delegates, who is accountable, who verifies?

**Why it's fresh:** Most "research roundups" list papers sequentially. This one synthesizes them into a single argument about what the field's actual frontier looks like as a *system design stack*.

**Risk:** Could feel listicle-ish if not executed with strong narrative connective tissue.

---

### Angle C: "The Multi-Agent Tax, Revisited"
**Headline idea:** *The Multi-Agent Tax: What 90 Days of Research Tells Us About the Real Cost of Agent Collaboration*

**Core argument:** This is a sequel/companion to the "Autonomy Tax" series. The thesis: multi-agent collaboration has three hidden costs, and recent research has started to *quantify* them.

1. **The Communication Tax** — Text-based inter-agent chatter costs 54% more tokens than internalized skills (`2601.04748`). Vision Wormhole shows the first credible alternative: latent-space telepathy that achieves +6.3pp accuracy at 1.87× speedup.
2. **The Coordination Tax** — Long-horizon tasks fail not because agents are bad, but because orchestration is brittle. ROMA's recursive decomposition is the first framework to attack this systematically with empirical evidence (+9.9% on SEAL-0).
3. **The Legibility Tax** — We can't measure cooperation quality (EmCoop) and we can't verify delegation chains (Intelligent AI Delegation). The cost here isn't compute—it's trust and accountability.

**Why it's fresh:** Connects directly to your previous Autonomy Tax work. Uses the "tax" framing to make abstract systems costs feel tangible. Grounded in concrete numbers from multiple papers.

**Evidence density:** Very high—every claim has a citation with real numbers.

---

### Angle D: "Agents Are Learning to Be Quiet"
**Headline idea:** *The End of Chatty Agents: Why Multi-Agent AI Is Moving Beyond Language*

**Core argument:** A provocative, single-thesis essay. The argument: the defining move in recent multi-agent research is the *retreat from language as the communication substrate*. Three strands of evidence:

1. **Skill internalization** (`2601.04748`): If you can compile agent communication into skill selection, talking was overhead all along.
2. **Latent telepathy** (`2602.15382`): Vision Wormhole replaces text with continuous latent injection through the visual pathway—agents communicating without ever generating a token.
3. **Recursive aggregation** (`2602.01848`): ROMA doesn't just decompose tasks—it *compresses* intermediate results. The aggregation step is explicitly about reducing the information that flows between layers.

**Thesis:** Language was the MVP communication protocol for multi-agent AI. The next generation is post-linguistic. And that changes everything about debugging, trust, and legibility.

**Why it's fresh:** This is genuinely novel angle. No one is framing the MAS research frontier as a *communication substrate shift*. It's the kind of article that gives readers a new lens they can apply to everything they read afterward.

**Risk:** Needs careful handling to avoid being too sci-fi. Must be grounded in the specific mechanisms from each paper.

---

### Angle E: "The Cognitive Phase Transition"
**Headline idea:** *There Is a Phase Transition in AI Skill Selection—And It Changes How We Should Build Agents*

**Core argument:** A deep-dive article centered entirely on the most surprising finding from the research: the phase transition in skill selection (`2601.04748`). Accuracy doesn't degrade linearly—it holds steady, then collapses at ~80–90 skills. This mirrors cognitive capacity limits in humans (Miller's law, but for LLMs). Then use the other papers to contextualize what this means:

- ROMA is what you build *on the other side* of the phase transition—recursive decomposition as the answer to disambiguation failure.
- Vision Wormhole is an attempt to *expand the bandwidth* before the transition hits (richer signals → more disambiguation capacity).
- EmCoop asks: can we even *detect* when the transition is happening in embodied multi-agent settings?

**Why it's fresh:** Phase transitions are a deeply powerful metaphor (and literal mechanism) that almost no one in the practitioner AI audience has internalized. This would be memorably novel—the kind of article people screenshot and share.

**Strongest quotable insight:** *"Your multi-agent system doesn't fail because your agents are dumb. It fails because somewhere in your skill routing, you crossed a disambiguation threshold that no amount of prompt engineering can recover from."*

---

### Angle F: "How to Decide: Multi-Agent or Not?"
**Headline idea:** *The Decision Framework: When Multi-Agent Is the Right Architecture (And When It's Expensive Ceremony)*

**Core argument:** A practitioner-focused guide that synthesizes the research into a decision framework. The research now gives us enough evidence to build a concrete rubric:

1. **Count your skills.** If your agent needs <80 skills, compile to single-agent (citing `2601.04748`).
2. **Measure your horizon.** If your task requires multi-step reasoning with dependency chains, recursive MAS (ROMA) outperforms flat orchestration.
3. **Check your heterogeneity.** If your agents are from different model families, you need a shared communication substrate. Text works but costs 1.87× more time; latent channels (Vision Wormhole) are the emerging alternative.
4. **Define your accountability chain.** If tasks involve delegation across trust boundaries, you need the governance layer (Intelligent AI Delegation).
5. **Measure cooperation, not just success.** EmCoop's process metrics let you diagnose *why* agents succeed or fail, not just whether they did.

**Why it's fresh:** Gives the reader a concrete rubric backed by recent evidence. Most multi-agent advice is vibes; this is grounded.

**Risk:** Could feel too prescriptive without enough narrative.

---

## Recommended Article: Angle E + elements of A and D

### Why this combination wins

**Angle E** ("The Cognitive Phase Transition") is the strongest *idea-anchor* because it:
- Has a genuinely surprising, empirically grounded core finding
- Creates a memorable mental model readers will carry with them
- Naturally lets you organize the other 4 papers as responses to the phase transition
- Is the most "screenshot-worthy" — the phase transition chart and the quotable thesis

**Steal from Angle A:** The "compiler" framing for the opening—start with the provocation that MAS can be compiled away, *then* reveal the phase transition as the reason it can't always be.

**Steal from Angle D:** The "post-linguistic communication" section as the article's speculative forward-look, grounding it in Vision Wormhole's concrete results.

---

## Proposed Article Structure

### Title (working)
**"The Phase Transition in Multi-Agent AI: Why Your Agent System Breaks at 80 Skills"**

*Subtitle: Recent research reveals a cognitive cliff in LLM skill selection—and it rewrites the rules for when multi-agent architecture is actually necessary.*

### Target
- ~4,000–5,000 words
- Substack format with footnoted citations (matching Autonomy Tax series style)
- Bold thesis, evidence-defended, anti-listicle

---

### Section 1: The Compiler's Wager (~800 words)
**Open with the provocation:** A team at UBC just showed you can *delete* your multi-agent system. Compile it into a single agent with skills. Save 54% of your tokens, halve your latency, lose nothing on accuracy.

This is not a theoretical exercise. They formalized a compilation function Φ: M → S, ran it across multiple benchmarks, and the compiled single agent was *as good or better*. The implication is uncomfortable: if your multi-agent system can be faithfully compiled away, then all that agent structure was ceremony—organizational overhead dressed up as architecture.

**The tension:** So why does anyone still need multi-agent systems? The answer is the most interesting finding in the paper, and possibly the most important finding in recent multi-agent research.

**Bridge to Section 2:** The compiler breaks. And the way it breaks tells you something profound.

### Section 2: The Phase Transition (~1,200 words)
**The core finding:** Skill selection accuracy doesn't degrade linearly as the skill library grows. It holds steady—and then it collapses. The capacity parameter κ is ~92 for GPT-4o-mini and ~84 for GPT-4o. Beyond that threshold, accuracy drops to half. This is not noise. It is a phase transition governed by a super-linear decay law.

**The cognitive parallel:** The authors connect this to bounded rationality in human cognition—Miller's law and Hick's law applied to LLMs. Semantic confusability, not execution complexity, is the driver. Adding one semantic competitor per skill reduces accuracy by 7–30%.

**The design implication:** The question isn't "how many agents do I need?" It's "have I crossed the disambiguation threshold?" Multi-agent architecture is the decomposition pattern you adopt *after* single-agent skill routing fails—because it reduces each agent's action space below the critical threshold.

**Counter from ROMA:** When you *do* need multi-agent structure, the strongest recent answer is recursive decomposition. ROMA's four-role architecture (Atomizer, Planner, Executor, Aggregator) is explicitly designed to keep each agent's local complexity below the break point. Its +9.9% on SEAL-0 and matching closed-model performance on EQ-Bench are the empirical evidence that this pattern works.

### Section 3: The Communication Substrate Shift (~1,000 words)
**The second big story:** Even when you accept that multi-agent structure is necessary, recent research says the *way agents communicate* is wrong. Text was the MVP protocol. It's now the bottleneck.

**Vision Wormhole:** Repurposes VLM visual encoders as continuous communication channels. Hub-and-spoke topology reduces alignment from O(N²) to O(N). Results: +6.3pp accuracy, 1.87× speedup, robust with <100 anchor texts for training. The metaphor of "agent telepathy" through the visual pathway is memorable, but the engineering insight is structural: if you treat the visual encoder as a universal port, heterogeneous agents can share high-bandwidth latent state without ever generating a token.

**Connect to the phase transition:** Why does latent communication help? Because richer signal means more disambiguation capacity per interaction. Text quantizes information. Latent channels preserve it. This doesn't eliminate the phase transition, but it may raise the threshold.

**ROMA's aggregation:** ROMA also attacks the communication problem, but from the other direction—by *compressing* what flows between layers. The Aggregator role is explicitly about reducing information volume, not increasing bandwidth. These are two complementary strategies for the same underlying bottleneck.

### Section 4: The Measurement Gap (~600 words)
**The uncomfortable truth:** We can barely measure multi-agent cooperation. EmCoop's contribution is making this legible: a benchmark framework that separates high-level cognition from low-level embodied interaction and introduces *process-level metrics* for cooperation quality.

**Why this matters for the phase transition thesis:** If you can't measure cooperation quality—only task completion—you can't tell whether your multi-agent system is collaborating efficiently or just stumbling into the right answer through brute force. The phase transition in skill selection suggests that systems can *appear* stable right up until they collapse. Process metrics are the early warning system.

**Delegation and trust:** Intelligent AI Delegation extends this to governance—who delegates, who verifies, who is liable. It's the most conceptual paper in the set, but it articulates a real gap: as agents delegate to other agents, accountability chains need cryptographic verification, not just logging.

### Section 5: The New Decision Framework (~400 words)
**Synthesis:** Pull the threads together into a practical rubric:
1. **Start with single-agent.** Compile your MAS. If it works, you're done.
2. **Watch for the phase transition.** When skill selection accuracy drops, decompose—don't prompt-engineer harder.
3. **Use recursive architectures.** ROMA-style decomposition gives each agent a manageable action space.
4. **Upgrade your communication substrate.** Text is the legacy protocol. Latent channels are the frontier.
5. **Measure cooperation, not just outcomes.** EmCoop's process metrics are the early warning system for collaboration failure.

### Section 6: What This Means (~400 words)
**Forward look:** The phase transition finding reframes the entire multi-agent debate. It's not about whether agents should collaborate—it's about *where the disambiguation boundary sits* for a given model and task. Everything else—architecture, communication, measurement, governance—is infrastructure for staying on the right side of that boundary.

**Closing provocation:** *The next frontier in multi-agent AI isn't building more agents. It's understanding the cognitive physics of why agent systems break—and engineering around it.*

---

## Key Evidence Table

| Claim | Source | Evidence |
|---|---|---|
| MAS can be compiled to single-agent | `2601.04748` | 53.7% token reduction, 49.5% latency reduction, comparable accuracy |
| Phase transition in skill selection | `2601.04748` | κ ≈ 92 (GPT-4o-mini), 84 (GPT-4o); super-linear decay law |
| Semantic confusability drives failure | `2601.04748` | +1 semantic competitor → 7–30% accuracy drop |
| Hierarchical routing mitigates | `2601.04748` | +9–40% accuracy improvement over flat selection |
| Recursive decomposition scales | `2602.01848` | ROMA +9.9% on SEAL-0; DeepSeek-V3 matches Claude Sonnet 4.5 on EQ-Bench |
| Latent communication outperforms text | `2602.15382` | +6.3pp accuracy, 1.87× speedup; O(N) vs O(N²) alignment |
| Process metrics for cooperation | `2603.00349` | EmCoop separates cognitive/embodied layers; process-level failure diagnosis |
| Delegation needs cryptographic trust | `2602.11865` | ZKP-based monitoring, contract-first decomposition, transitive liability |

---

## Tone & Style Notes

- Match the **Autonomy Tax** voice: analytical, research-driven, medium-density paragraphs, footnoted citations
- **Bold falsifiable claims** defended with evidence within the same paragraph
- **Inverted pyramid**: lead with the most counterintuitive finding (MAS can be compiled away), then reveal why it only works sometimes (phase transition)
- Avoid listicle energy—the five papers are woven into a single narrative, not presented sequentially
- Quotable sentences every ~500 words
- Caveats are honest but inline, not defensive appendices
