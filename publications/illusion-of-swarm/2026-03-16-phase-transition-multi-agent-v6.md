# Most Multi-Agent Systems Are a Compiler Workaround

*In many same-model production stacks, swarms are what you build when routing, memory, and coordination start to fail.*

---

A lot of multi-agent systems are overflow handling dressed up as architecture.

On benchmark tasks, a team at the University of British Columbia showed that many multi-agent systems can be transformed into a single agent with skills, cutting token use by 53.7% and latency by 49.5% while preserving comparable output quality.[^1] That is not a cute optimization. It is a warning shot. It suggests that in many systems, a large share of the extra computation is not deeper reasoning. It is coordination overhead.

That result is easy to overread, so scope it immediately. It does not mean multi-agent systems are fake. It does not mean one agent always wins. It does not mean all coordination can be folded back into one model. It means something narrower and more useful: for many same-model, tool-using production systems, explicit multi-agent structure is often the operational price of unresolved routing, state, and communication problems.

That is the useful thesis.

> **In many production stacks, multi-agent is not more intelligence. It is damage control for routing, state, and communication.**

Once you frame it that way, the research landscape looks different. The interesting question is not "how many agents should I build?" It is "which bottleneck forced the split?" Recent papers on skill routing, recursive decomposition, memory control, embodied cooperation, delegation, and latent communication do not add up to "swarms are the future." They add up to a harder and more practical claim: agentic performance depends on how well you organize decomposition, memory, communication, and coordination under tight cost and error budgets.

That claim is strong enough to matter and narrow enough to defend. Some systems genuinely need multiple agents. Some should keep them. Some only work because of them. But the last few months of research make it much harder to treat multi-agent design as the default mark of sophistication.

## 1. Why the Split Happens

The flattering story about multi-agent systems goes like this: the Planner plans, the Researcher researches, the Coder codes, the Reviewer reviews. A society of specialized minds.

Sometimes that story is true. Often it is a prettier description of a simpler problem. The base system is struggling to route tools, govern context, or keep intermediate state legible. Splitting the system into named agents is how we reduce local confusion.

That is why the UBC paper matters.[^1] It does not merely propose a better multi-agent framework. It asks a more uncomfortable question: when is the multi-agent graph necessary at all? Their answer is empirical. In the evaluated settings, a single agent with a skill library can reproduce the behavior of many multi-agent systems at much lower cost.[^1] The graph was helping, but not always for the reason practitioners like to say.

Two adjacent papers make that interpretation harder to dismiss. *Toward Efficient Agents* surveys recent work on memory, tool learning, and planning and finds the same recurring moves again and again: compress state, bound context, and avoid unnecessary actions.[^2] *Towards a Science of Scaling Agent Systems* runs a controlled study across 180 configurations, varying agent quantity, coordination topology, base model capability, and task type.[^3] Its conclusions are blunt. Multi-agent performance is highly task-dependent. Tool-heavy tasks suffer disproportionately from coordination overhead. Coordination yields diminishing or negative returns once single-agent baselines are already strong. Across the full set, the mean improvement is negative.[^3]

That does not mean multi-agent never helps. It means "more agents" is not an explanation. It is a bill.

If you split a system, you should be able to say what you bought with that bill. Did you buy better decomposition? Lower routing ambiguity? A real trust boundary? Parallel search? A memory controller the base model lacks? If you cannot answer that question, the graph is probably doing theater on top of a simpler failure mode.

## 2. Semantic Quarantine

The most important result in the UBC paper is not just that some multi-agent systems can be collapsed into one. It is where that collapse breaks.[^1]

When the authors scale up the single agent's skill library, performance does not degrade gracefully. It holds through 10, 30, even 60 skills. Then, in the tested models, it hits a collapse zone in roughly the 80 to 90 range. For GPT-4o-mini, the threshold is about 92 skills. For GPT-4o, it is 84.[^1] Beyond that point, selection accuracy drops sharply according to a super-linear decay law.[^1]

Not gradually. Catastrophically.

The paper ties that failure to semantic confusability.[^1] If too many nearby tool descriptions occupy the same action space, the selector starts colliding with itself. In their setup, adding a single semantically similar competitor skill can reduce selection accuracy by 7% to 30%.[^1] At large library sizes, flat selection for GPT-4o-mini falls to roughly 45%. Hierarchical routing pulls it back to about 83% to 85%, a recovery of 37 to 40 points.[^1]

That is not just a benchmark curiosity. It explains a huge amount of agent engineering in the wild.

> **An agent is not a persona. It is a namespace.**

That sentence is my interpretation, not the paper's. But it fits the evidence better than the folk psychology does. Your support bot does not need a separate database agent because SQL requires a different species of mind. It needs one because throwing `resolve_ticket`, `query_user_db`, `fetch_marketing_campaigns`, `refund_order`, and `check_entitlement` into one flat tool universe raises the odds of routing collisions. The boundary is there to keep similar actions from interfering with each other.

I call this pattern **Semantic Quarantine**.

Multi-agent decomposition is often not what you build to increase reasoning depth. It is what you build when the action space becomes too crowded to govern cleanly. Once you cross the disambiguation threshold, splitting the system is a way of quarantining neighboring skills so the model can make smaller, cleaner decisions.

This is also why hierarchical routing works. It does not magically expand the model's intelligence. It factorizes one overloaded decision into several smaller ones. The selector becomes more reliable because the choice set becomes more separable.

ROMA is the strongest architecture answer to this problem in the current paper set.[^4] Its recursive Atomizer-Planner-Executor-Aggregator pattern keeps local decisions manageable and compresses intermediate outputs before passing them onward.[^4] On the paper's benchmarks, that design yields measurable gains, including a 9.9% improvement on SEAL-0 and strong performance on EQ-Bench.[^4] The important point is not that recursion is the final answer. It is that once your action space crosses the threshold, better decomposition usually beats louder prompting.

SkillOrchestra arrives at a similar conclusion from another angle.[^5] Instead of learning a mostly opaque routing policy end to end, it builds a reusable skill handbook of agent competence and cost, then routes using explicit performance-cost trade-offs.[^5] Again, the lesson is not "more agents." It is "more explicit structure around what each decision is for."

This is where many practical agent stacks should get less romantic. Flat persona committees are often an expensive way to solve a routing problem.

## 3. Where Multi-Agent Is Real

This thesis breaks in predictable places.

The first is heterogeneity. If your system genuinely needs different substrates, multiple agents are not a workaround for confusion. They are the system. A vision model, a code model, a planner, and a verifier may exist because the underlying capabilities are structurally different. That is exactly why papers like *The Vision Wormhole* are interesting: they take heterogeneous coordination seriously rather than pretending a single homogeneous model will absorb everything.[^6]

The second is trust and authority boundaries. *Intelligent AI Delegation* should be treated mainly as a conceptual framing paper, not as decisive empirical proof of superior system performance.[^7] But the requirement it names is real. Sometimes you want a reviewer that can challenge a proposal, a safety critic that is isolated from the system it monitors, or a delegate that behaves differently at high task criticality.[^7] Those boundaries are not just orchestration conveniences. They are governance mechanisms. You cannot always distill them away without erasing the reason they existed.

The third is embodied or distributed coordination. *EmCoop* does not prove a universal law of cooperation, but it does show why process-level measurement matters.[^8] In embodied settings, agents interrupt each other, replan at bad times, and pay real costs for communication and waiting. *MultiAgentBench* points in the same direction by treating coordination protocols, milestone-based metrics, and planning quality as first-class evaluation targets rather than afterthoughts.[^9] Once multiple actors share a physical or simulated environment, system-level interaction can be genuinely irreducible.

The fourth is exploration. Here *EMPO2* is useful by analogy rather than as a pure multi-agent result.[^10] It shows that external scaffolding and exploratory support can generate better trajectories that are only later internalized. Search has its own value. If the goal is to widen coverage over possible solutions rather than minimize latency on one request, multiple actors or multiple exploratory paths can be rational even if you later compress what they found.

The scaling paper keeps this section honest.[^3] Centralized coordination helps some parallelizable tasks dramatically. Decentralized coordination can help web navigation. Sequential reasoning tasks can degrade badly under multi-agent variants.[^3] That is the sane conclusion: multi-agent is neither fake nor fate. It is a conditional tool. The mistake is not using it. The mistake is pretending the same reason explains every case.

## 4. Text Is the Bottleneck, Not the Enemy

The papers do not justify "the death of English." They do justify something narrower and still consequential: text is increasingly the bottleneck in some multi-agent settings.

English is a great interface for humans. It is a mediocre place to park intermediate machine state.

*The Vision Wormhole* makes the most direct current case.[^6] Its argument is structural. When one model compresses a rich internal state into text and another reconstructs meaning from that text, the handoff is slow, bandwidth-limited, and lossy. Their workaround is to repurpose the visual pathway of vision-language models as a higher-bandwidth coordination channel. On the tested heterogeneous setups, that yields an average accuracy gain of 6.3 percentage points and about 1.87x faster execution.[^6] That is a real result. It is not a universal substrate theorem.

*Latent Collaboration in Multi-Agent Systems* strengthens the cluster story.[^11] Its LatentMAS design moves hidden-state information directly and reports large gains in speed and token efficiency relative to text-based collaboration on its evaluated benchmarks.[^11] Whether these methods survive production constraints is unresolved. What they do show is that serious groups are no longer treating text relay as the unquestioned default for inter-agent coordination.

Then there is *EmCoop*, which attacks the same problem from the opposite side.[^8] Instead of building a new channel, it measures what happens when teams communicate under different topologies. In MA-Crafter with GPT-5.2 on 3-agent teams, the paper reports:

- Independent: 0 messages, 1.65 decision overhead.
- Centralized: 39 messages, 2.55 decision overhead, 0.49 plan coherence.
- Debate: 25 messages, 2.84 decision overhead, 0.04 plan coherence.
- Decentralized: 103 messages, 3.90 decision overhead, 0.00 plan coherence.[^8]

More talk. Less coordination.

The important point is not that every text message is bad. It is that communication design is a first-class systems variable. In EmCoop's loop, agents can be interrupted by incoming messages and forced into replanning.[^8] That means messages are not passive facts. They are new branches in the control flow.

This is the deeper problem with text handoffs in machine coordination. Text messages are propositions. They invite evaluation, disagreement, clarification, and revision. The moment one agent says "I found three endpoints," the receiver has new options: verify, revise, query, object, wait, or replan. A typed state transfer can still trigger disagreement, but it does not automatically carry the same discursive burden. That is one reason latent or model-native handoffs are interesting even before they are mature: they promise a way to move state without turning every transfer into a miniature debate.

That is why the strongest practical lesson is simpler than "go latent." Stop treating verbose natural-language handoffs as a free abstraction. If agents must talk, make them exchange the smallest useful state. Prefer typed fields over paragraphs. Prefer compact plans over autobiographies. Prefer bounded schemas over self-important debate transcripts. The frontier may be latent. The immediate win is almost always less chatter.

## 5. The Swarm as Training Rig

The most promising long-run pattern in this literature is not that multi-agent systems disappear. It is that some of their benefits can be pushed into training, adaptation, or policy design elsewhere.

This is where the second named concept earns its keep:

> **A swarm is often a training rig, not a destination.**

EMPO2 gives the clearest mechanism.[^10] During training, the agent receives external memory tips generated from prior episodes. Those tips are not vague reflections. They are concrete failure analyses and corrective hints. Rollouts produced with those tips are better because the agent is benefiting from externalized scaffolding.[^10]

Then the paper does something more interesting than simply keeping the memory around forever. In the off-policy update, the action was generated by the old policy with tips available, but the new policy is updated using probabilities recomputed without the tips.[^10] In plain English: the trajectory is produced with scaffolding, but the learning signal asks the base policy to absorb the useful behavior as if the scaffolding were gone. That conditioning mismatch is the point. It is how the agent internalizes what the scaffold was teaching it.[^10]

The results are not small. EMPO2 reports a 128.6% improvement over GRPO on ScienceWorld, moving from 33.2 to 75.9 average score, and an 11.3% gain on WebShop, from 79.4 to 88.3.[^10] On the paper's out-of-distribution transfer scenarios, memory-assisted adaptation improves average performance by 136% within 10 steps.[^10] Those are benchmark results, not a universal law. But the mechanism is extremely suggestive: some external guidance is valuable precisely because it creates trajectories worth distilling.

*Agentic Memory* tells a related story for state management.[^12] Instead of treating long-term and short-term memory as separate external components, it exposes STORE, RETRIEVE, UPDATE, SUMMARIZE, FILTER, and DELETE as tool-like actions inside the policy itself.[^12] On the evaluated benchmarks, that unified memory policy improves both performance and context efficiency over strong baselines.[^12] If your current architecture requires a separate memory agent mostly because the base agent cannot govern memory cleanly, this is exactly the kind of result that should make you reexamine the boundary.

The training design matters here too. AgeMem uses a three-stage RL curriculum: first the agent learns what deserves long-term storage, then it learns to manage short-term noise and distraction, then it learns to coordinate both under task pressure.[^12] That is a useful corrective to a lot of agent hype. Better agency is often not one magic architecture choice. It is better learned control over what to keep, what to discard, and what to retrieve at the right moment.

*AgentArk* belongs in this section too, but only with narrow wording.[^13] It does not prove that all multi-agent intelligence can be transferred into one model with negligible loss. It does show that distilling multi-agent reasoning traces into a single agent can improve single-agent performance, and that process-aware distillation is the strongest of the paper's tested strategies.[^13]

What makes AgentArk and EMPO2 interesting together is not that they prove one grand law. It is that they point in the same engineering direction from opposite sides. AgentArk distills social scaffolding: debates, critiques, and corrections across multiple agents.[^13] EMPO2 distills personal scaffolding: tips and reflective guidance attached to one agent's own exploration.[^10] Both suggest that some of the value in scaffolds belongs in the traces they generate, not in the permanent runtime structure.

Taken together, these papers do not justify a grand prophecy that every swarm will be compiled away. They do justify a more practical workflow:

1. Prototype with scaffolds.
2. Log the debates, routing decisions, memory operations, and corrections that actually help.
3. Ask which parts are valuable because they generate good trajectories and which parts are just expensive inference-time ceremony.
4. Internalize what you can.
5. Keep the scaffold only where it remains genuinely load-bearing because of trust, heterogeneity, or real distributed coordination.

That is not a law of history. It is a healthier engineering loop.

## What to Build Differently Starting Monday

If you ship agent systems, the playbook from this literature is straightforward.

1. Start with a single agent when the system is one model plus tools. Do not add personas until you can name the bottleneck you are fixing.
2. When routing starts to fail, think in namespaces and local action spaces. Better decomposition usually beats more theatrical prompting.
3. If you do split the system, avoid flat committees. Use recursive or skill-aware routing that keeps each decision below the confusion threshold.[^1][^4][^5]
4. Treat communication as a design surface. Minimize natural-language handoffs first; experiment with richer internal channels only where the cost is justified.[^6][^8][^11]
5. Measure process, not just outcomes. If you cannot see interruptions, communication load, plan coherence, or routing collapse, you do not really know why your system works.[^3][^8][^9]
6. Treat scaffolds as candidates for internalization. External memory, review passes, multi-agent debate, and exploratory helpers may belong in training, adaptation, or fallback paths rather than in the hot path of every production request.[^10][^12][^13]

The one-sentence version is simple: multi-agent systems are often useful, but their value usually comes from specific coordination mechanisms, and many of those mechanisms can be simplified, compressed, or internalized once you know what problem they were solving.

## Two Predictions for Q1 2027

Only two predictions are worth making from this set, and both should be embarrassing if wrong.

**Prediction 1:** By March 31, 2027, at least one major agent framework or hosted agent platform will ship built-in graph simplification or evaluator tooling that recommends collapsing some multi-agent workflows into a single-agent-plus-tools configuration. This is falsified if, by that date, mainstream platforms still treat multi-agent graphs as design-time artifacts only, with no first-class optimization or simplification pass.

**Prediction 2:** By March 31, 2027, at least two publicly described production compound-AI systems from major vendors or labs will use non-text intermediate handoffs for selected internal coordination paths, whether via typed state transfer, model-native state transfer, or latent channels. This is falsified if public production descriptions still rely exclusively on natural-language or JSON relay for internal multi-model coordination.

Those are narrow predictions on purpose. The literature here is strong enough to change how builders think. It is not yet strong enough to support prophecy.

The next frontier is not more agents. It is better answers to four questions: when should a system split, what should stay local, how should state move, and which scaffolds deserve to survive deployment. If multi-agent is often a compiler workaround, the real job now is not to admire the workaround. It is to understand exactly what it is compensating for.

---

### References

[^1]: [When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail](https://arxiv.org/abs/2601.04748). University of British Columbia. (2026).
[^2]: [Toward Efficient Agents: Memory, Tool learning, and Planning](https://arxiv.org/abs/2601.14192). (2026).
[^3]: [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296). Google Research / Google DeepMind / MIT. (2025).
[^4]: [ROMA: Recursive Open Meta-Agent Framework for Long-Horizon Multi-Agent Systems](https://arxiv.org/abs/2602.01848). Sentient / Virginia Tech. (2026).
[^5]: [SkillOrchestra: Learning to Route Agents via Skill Transfer](https://arxiv.org/abs/2602.19672). (2026).
[^6]: [The Vision Wormhole: Latent-Space Communication in Heterogeneous Multi-Agent Systems](https://arxiv.org/abs/2602.15382). Purdue / CMU / Georgia Tech. (2026).
[^7]: [Intelligent AI Delegation](https://arxiv.org/abs/2602.11865). Google DeepMind. (2026).
[^8]: [EmCoop: A Framework and Benchmark for Embodied Cooperation Among LLM Agents](https://arxiv.org/abs/2603.00349). Carnegie Mellon / USC. (2026).
[^9]: [MultiAgentBench: Evaluating the Collaboration and Competition of LLM agents](https://arxiv.org/abs/2503.01935). (2025).
[^10]: [Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization (EMPO2)](https://arxiv.org/abs/2602.23008). Microsoft Research / KAIST. ICLR 2026.
[^11]: [Latent Collaboration in Multi-Agent Systems](https://arxiv.org/abs/2511.20639). Princeton / UIUC / Stanford. (2025).
[^12]: [Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for LLM Agents](https://arxiv.org/abs/2601.01885). Alibaba / Wuhan University. (2026).
[^13]: [AgentArk: Distilling Multi-Agent Intelligence into a Single LLM Agent](https://arxiv.org/abs/2602.03955). (2026).
