# Most Multi-Agent Systems Are a Workaround, Not a Destination

*For many same-model production systems, multiple agents are a temporary way to manage routing, state, and coordination limits. The recent research wave matters not because it proves swarms are the future, but because it shows when to split, when to compress, and when to fold the system back into one model.*

---

In benchmark settings, a team at the University of British Columbia showed that many multi-agent systems can be transformed into a single agent with skills, cutting token use by 53.7% and latency by 49.5% while preserving comparable output quality.[^1] That is a strong result, but it is also easy to overread.

It does not mean multi-agent systems are fake. It does not mean one agent always wins. It means something narrower and more useful: for many same-model, tool-using production stacks, explicit multi-agent structure is often the operational price of unresolved routing, state, and coordination problems.

That reframes the design question. The question is not "how many agents should I build?" It is "which bottleneck am I compensating for?" Recent papers on agent systems, routing, memory, delegation, embodied cooperation, and latent communication point to the same practical conclusion: the important frontier is not adding more personas. It is organizing decomposition, memory, communication, and coordination under tight cost and error budgets.

The strongest version of that thesis is not universal. Some systems genuinely need multiple agents. Some will keep them. Some should. But the new literature makes it much harder to treat multi-agent design as the default mark of sophistication.

## 1. Why Multi-Agent Often Exists

*Anchor paper:* [When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail](https://arxiv.org/abs/2601.04748). *Corroborating papers:* [Toward Efficient Agents](https://arxiv.org/abs/2601.14192), [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296).

The usual story about multi-agent systems is flattering. We say a Planner, Researcher, Coder, and Reviewer represent different modes of intelligence. A society of specialized minds. Sometimes that is true. Often it is a prettier description of a simpler problem: the base system is struggling to route tools, manage context, or keep intermediate state legible.

The UBC paper is important because it directly tests that suspicion.[^1] Instead of assuming the multi-agent graph is load-bearing, the authors apply a formal compilation function from multi-agent systems to a single agent with a skill library. On their benchmarks, the compiled system uses far fewer tokens and lower latency while matching the original system closely.[^1] That is not a philosophical objection to multi-agent design. It is an engineering result. In some settings, a large share of the extra computation is coordination overhead rather than indispensable reasoning.

Two adjacent papers sharpen the point. The efficiency survey *Toward Efficient Agents* argues that memory, planning, and tool-learning research keeps converging on the same higher-level moves: bound context, compress intermediate state, and reduce unnecessary tool invocations.[^2] *Towards a Science of Scaling Agent Systems* goes further by controlling for agent quantity, topology, model capability, and task type across 180 configurations.[^3] Its headline is not that more agents win. It is that outcomes depend on a tool-coordination trade-off, capability saturation, and topology-specific error amplification.[^3] Under fixed budgets, some multi-agent variants help. Some hurt. Across the full set, the mean improvement is negative.[^3]

Put differently: multi-agent often appears when a single agent has become brittle, but brittleness can come from multiple sources. Sometimes the answer is decomposition. Sometimes it is memory. Sometimes it is better routing. Sometimes it is simply not asking one model to narrate every internal handoff in English.

That is why the right default for skeptical builders is not "start with a swarm." It is "start with the smallest system that can express the task, then identify the specific failure mode before you split it."

## 2. The Disambiguation Threshold

*Anchor paper:* [When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail](https://arxiv.org/abs/2601.04748). *Corroborating papers:* [ROMA](https://arxiv.org/abs/2602.01848), [SkillOrchestra](https://arxiv.org/abs/2602.19672). *Field context:* [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296).

The most useful result in the UBC paper is not just that some multi-agent systems can be collapsed into one. It is where that collapse stops working.[^1] Skill selection does not degrade gracefully as the action library grows. On the tested models, it stays stable and then breaks in a collapse zone around 80 to 90 skills.[^1] The paper connects that breakdown to semantic confusability: if too many nearby tool descriptions occupy the same action space, the selector starts colliding with itself.[^1] In their setup, even adding one semantically similar competitor can reduce selection accuracy materially.[^1]

This is the point where "agent" stops meaning persona and starts meaning namespace.

That line is an interpretation, not a sentence from the paper. But it fits the evidence better than the folk story does. In many production systems, we do not create a database agent because querying a database requires a mystical new cognitive faculty. We create it because mixing `resolve_ticket`, `query_user_db`, `fetch_marketing_campaigns`, `refund_order`, and `check_entitlement` in one flat tool universe increases routing confusion. The boundary is there to keep similar actions from interfering with each other.

That interpretation also explains why hierarchical routing works. In the UBC experiments, flat selection at large library sizes collapses badly, while hierarchical routing recovers much of the lost accuracy by replacing one overloaded decision with several smaller ones.[^1] The model did not become more intelligent. The choice became more separable.

*ROMA* is the best direct architecture answer to that problem in the current set.[^4] Its recursive Atomizer-Planner-Executor-Aggregator structure keeps local decisions manageable and compresses intermediate outputs before passing them onward.[^4] On the paper's benchmarks, that design produces measurable gains, including a 9.9% improvement on SEAL-0 and strong performance on EQ-Bench.[^4] The key point is not that recursion is always best. It is that once your action space crosses a disambiguation threshold, better decomposition is often more valuable than louder prompting.

*SkillOrchestra* reaches a similar conclusion from a different direction.[^5] Instead of learning an opaque routing policy end to end, it builds a reusable skill handbook of agent competence and cost, then routes based on explicit performance-cost trade-offs.[^5] That is not the same method as UBC or ROMA, but it supports the same broader idea: orchestration gets more defensible when it is tied to explicit skills and competence profiles rather than vague personas.

This is where many practical agent stacks should change course. If your multi-agent design exists mainly to prevent tool confusion, say so. That is not a weakness. It is a clearer problem statement. Once you name the problem correctly, you can ask better questions: Do I need a real multi-agent system? A hierarchical router? A smaller skill library per stage? Better tool descriptions? A cost-aware handbook like SkillOrchestra? The bad version of this conversation is "we needed more agents because the task was hard." The useful version is "we needed less ambiguity per decision."

## 3. Where Multi-Agent Is Actually Load-Bearing

*Anchor paper:* [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296). *Corroborating papers:* [Intelligent AI Delegation](https://arxiv.org/abs/2602.11865), [EmCoop](https://arxiv.org/abs/2603.00349), [The Vision Wormhole](https://arxiv.org/abs/2602.15382), [EMPO2](https://arxiv.org/abs/2602.23008).

A good rewrite needs to make the objections early, not as an appendix. Multi-agent systems are not just ceremony. They are genuinely load-bearing in at least four situations.

First, heterogeneity. If your system genuinely needs different substrates, multiple agents are not a workaround for confusion. They are the system. A vision model, a code model, a planner, and a verifier may each exist because the underlying capabilities differ materially. *The Vision Wormhole* matters partly because it takes this case seriously rather than pretending a single homogeneous model will absorb everything.[^6]

Second, trust and authority boundaries. *Intelligent AI Delegation* is mostly a conceptual paper, not the kind of empirical proof you should lean on for performance claims.[^7] But it is still useful because it names a real requirement: sometimes the reason to separate agents is not capability but governance. You may want a verifier that can challenge a proposal, a safety critic that is structurally isolated from the system it monitors, or a delegate that behaves differently depending on task criticality.[^7] Those boundaries are hard to "distill away" without also erasing the trust boundary that made them valuable.

Third, embodied or distributed coordination. *EmCoop* does not prove a universal law of cooperation, but it does show why process-level measurement matters.[^8] In embodied tasks, agents can interrupt, replan, block each other, and communicate at the wrong times. That is not the same problem as routing tools in a text-only workflow. *MultiAgentBench* points in the same direction by treating coordination protocols and milestone-based metrics as first-class evaluation objects rather than side effects of task completion.[^9] Once multiple actors must coordinate in space, time, or shared environment state, the system-level interaction can be genuinely irreducible.

Fourth, exploration. Here *EMPO2* is useful by analogy rather than as a pure multi-agent result.[^10] It shows that external scaffolding, reflective tips, and exploration support can create better trajectories that are only later internalized. Search itself has value. If the point of your system is to widen coverage over possible solutions, not just minimize latency, multiple actors or multiple trajectories can be rational even when you later distill what they discovered.

The scaling paper is valuable because it keeps all of this from turning into metaphysics.[^3] Centralized coordination helps some parallelizable tasks dramatically. Decentralized coordination can help web navigation. Sequential reasoning tasks can degrade badly under multi-agent variants.[^3] That is the sane conclusion: multi-agent is not fake, and it is not fate. It is a conditional tool.

## 4. Communication Is a Frontier, Not a Law

*Anchor paper:* [The Vision Wormhole](https://arxiv.org/abs/2602.15382). *Corroborating papers:* [Latent Collaboration in Multi-Agent Systems](https://arxiv.org/abs/2511.20639), [EmCoop](https://arxiv.org/abs/2603.00349). *Field context:* [MultiAgentBench](https://arxiv.org/abs/2503.01935).

The weakest part of the earlier draft was claiming too much too soon about communication. The papers do not justify "the death of English." They do justify something narrower and still important: text is increasingly the bottleneck in some multi-agent settings.

*The Vision Wormhole* makes the strongest current case.[^6] Its argument is structural. When one model converts a rich internal state into text and another model reconstructs meaning from that text, the handoff is slow, bandwidth-limited, and lossy. Their workaround is to repurpose the visual pathway of vision-language models as a higher-bandwidth coordination channel. On the tested heterogeneous setups, that produces an average accuracy gain of 6.3 percentage points and roughly 1.87x faster execution.[^6] That is a real result, but it is still a result on selected systems, not a universal substrate theorem.

*Latent Collaboration in Multi-Agent Systems* makes the cluster story stronger.[^11] Its LatentMAS setup is training-free, moves hidden-state information directly, and reports large gains in speed and token efficiency relative to text-based collaboration on its benchmarks.[^11] Whether those methods survive contact with production constraints is unresolved. But together they establish something more modest and credible than a grand manifesto: researchers are no longer treating text relay as the unquestioned default for inter-agent communication.

*EmCoop* adds a different kind of evidence.[^8] In its experiments, more communication is not automatically better. Unstructured, high-volume communication can destroy plan coherence and increase decision overhead. Structured coordination outperforms noisy debate. That does not prove latent channels are the answer. It does show that communication design is not a cosmetic implementation detail. It is a central systems variable.

For builders, the near-term implication is not "install a latent bus." It is much simpler: stop treating verbose natural-language handoffs as a free abstraction. If agents must talk, make them exchange the smallest useful state. Prefer typed fields over paragraphs. Prefer compact plans over autobiographies. Prefer bounded schemas over self-important debates. The frontier may be latent. The immediate win is almost always less chatter.

## 5. The Swarm as Training Rig

*Anchor papers:* [EMPO2](https://arxiv.org/abs/2602.23008), [Agentic Memory](https://arxiv.org/abs/2601.01885). *Corroborating paper:* [AgentArk](https://arxiv.org/abs/2602.03955).

The most interesting long-run pattern in this literature is not that multi-agent systems will disappear. It is that some of their benefits can be turned into training or policy improvements elsewhere.

*EMPO2* gives the cleanest mechanism.[^10] During training, the agent gets external memory tips that improve exploration. During off-policy updates, the system recomputes probabilities without those tips so the base policy can absorb the useful behavior.[^10] On ScienceWorld and WebShop, that hybrid approach materially outperforms the reported GRPO baselines, and it also helps on the paper's out-of-distribution evaluations.[^10] The lesson is not "memory is solved." It is that external scaffolding can be useful precisely because it produces trajectories worth internalizing.

*Agentic Memory* makes a related point for state management.[^12] Instead of treating long-term and short-term memory as separate controllers, it exposes memory operations as tool-like actions inside the policy itself and trains the agent to decide when to store, retrieve, update, summarize, filter, or delete.[^12] On the evaluated benchmarks, that unified memory policy improves performance and context efficiency over strong baselines.[^12] If your current architecture requires a separate memory agent mainly because the base agent cannot govern memory well, this is exactly the kind of result that should make you rethink the boundary.

Now that *AgentArk* is verified, it belongs here too, but with narrower wording than before.[^13] It does not prove that all multi-agent intelligence can be transferred into one model with negligible loss. It does show that distilling multi-agent reasoning traces into a single agent can produce better single-agent performance, and that process-aware distillation is the strongest of the paper's tested strategies.[^13] That is enough to support an emerging pattern.

The pattern is this: a swarm can be a training rig.

That is the second coined frame worth keeping, because it is operationally useful. Prototype with scaffolds. Log good debates, routing decisions, memory operations, and corrections. Ask which parts are valuable because they generate diverse or corrective trajectories, and which parts are just expensive inference-time ceremony. Internalize what you can. Keep the scaffolding when it is genuinely load-bearing because of trust, heterogeneity, or real distributed coordination.

This is not a law of history. It is a healthier engineering loop.

## What to Build Differently Starting Monday

If you ship agent systems, the practical playbook from this literature is straightforward.

1. Start with a single agent when the system is one model plus tools. Do not add personas until you can name the specific bottleneck you are fixing.
2. When routing starts to fail, think in namespaces and local action spaces. Better decomposition usually beats more theatrical prompting.
3. If you do split the system, avoid flat committees. Use recursive or skill-aware routing that keeps each decision below the confusion threshold.[^1][^4][^5]
4. Treat communication as a design surface. Minimize natural-language handoffs first; experiment with richer internal channels only where the cost is justified.[^6][^8][^11]
5. Measure process, not just outcomes. If you cannot see interruptions, communication load, plan coherence, or routing collapse, you do not really know why your system works.[^3][^8][^9]
6. Treat scaffolds as candidates for internalization. External memory, review passes, multi-agent debates, and exploratory helpers may belong in training, adaptation, or fallback paths rather than the hot path of every production request.[^10][^12][^13]

A skeptical engineer should be able to summarize the whole thesis in one sentence: multi-agent systems are often useful, but their value usually comes from specific coordination mechanisms, and many of those mechanisms can be simplified, compressed, or internalized once you know what problem they were solving.

## Two Predictions for Q1 2027

I would make only two predictions from this set, and both are falsifiable.

**Prediction 1:** By March 31, 2027, at least one major agent framework or hosted agent platform will ship built-in graph simplification or evaluator tooling that recommends collapsing some multi-agent workflows into a single-agent-plus-tools configuration. This is falsified if, by that date, mainstream platforms still treat multi-agent graphs as design-time artifacts only, with no first-class optimization or simplification pass.

**Prediction 2:** By March 31, 2027, at least two publicly described production compound-AI systems from major vendors or labs will use non-text intermediate handoffs for selected internal coordination paths, whether via typed state transfer, model-native state transfer, or latent channels. This is falsified if public production descriptions still rely exclusively on natural-language or JSON relay for internal multi-model coordination.

Those are narrower predictions than the earlier draft made. That is intentional. The research here is good enough to change how builders think. It is not yet good enough to support prophecy.

The next frontier is not "more agents." It is better answers to four questions: when should a system split, what should be kept local, how should state move, and which scaffolds deserve to survive deployment.

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
