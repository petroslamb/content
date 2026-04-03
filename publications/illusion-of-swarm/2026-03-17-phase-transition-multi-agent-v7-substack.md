# Most Multi-Agent Systems Are a Compiler Workaround

*In many same-model production stacks, swarms are what you build when routing, memory, and coordination start to fail.*

---

Most production multi-agent systems are not acts of architectural genius. They are repair jobs.

When routing gets messy, tool choice gets noisy, or context starts leaking across tasks, teams split one agent into several and call the result a swarm. Sometimes that is the right move. Just as often, it is a way to keep the underlying system from tripping over its own action space.

The sharpest recent evidence comes from [When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail](https://arxiv.org/abs/2601.04748). In benchmark settings, the authors show that many multi-agent systems can be compiled into a single agent with skills, cutting token use by 53.7% and latency by 49.5% while preserving comparable output quality. That is not proof that multi-agent is fake. It is proof that a lot of what looks like architectural sophistication is really coordination overhead.

That needs to be scoped carefully. This is not an argument that one agent always wins. It is not an argument that all coordination can be flattened back into a single prompt. It is a narrower claim, and a more useful one: for many same-model, tool-using production systems, explicit multi-agent structure is often the operating cost of unresolved routing, state, and communication problems.

> In many production stacks, multi-agent is not extra intelligence. It is damage control for routing, state, and communication.

Once you look at the field through that lens, the recent paper trail starts to line up. The interesting question is not "how many agents should I build?" It is "what bottleneck forced the split?" Papers on skill routing, recursive decomposition, memory control, embodied cooperation, delegation, and latent communication do not add up to "swarms are the future." They add up to a harder claim: agent performance depends on how well you organize decomposition, memory, communication, and coordination under tight cost and error budgets.

That claim is strong enough to matter and narrow enough to defend.

## 1. Why the Split Happens

The flattering version of a multi-agent system sounds like this: the Planner plans, the Researcher researches, the Coder codes, the Reviewer reviews. A tidy little society of specialized minds.

Sometimes that is what is happening. Often it is a prettier story for a simpler problem. The base system is struggling to route tools, govern context, or keep intermediate state legible. Splitting the system into named agents is how we reduce local confusion.

That is why [When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail](https://arxiv.org/abs/2601.04748) matters. The paper does not just propose a better orchestration framework. It asks a more uncomfortable question: when is the multi-agent graph necessary at all? In the settings they test, a single agent with a skill library reproduces the behavior of many multi-agent systems at much lower cost. The graph was helping, but not always for the reason practitioners like to say.

Two adjacent papers make that interpretation harder to dismiss. [Toward Efficient Agents: Memory, Tool Learning, and Planning](https://arxiv.org/abs/2601.14192) surveys recent work on memory, tool learning, and planning and finds the same moves coming up again and again: compress state, bound context, and avoid unnecessary actions. [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296) runs a controlled study across 180 configurations, varying agent quantity, coordination topology, base model capability, and task type. Its conclusion is not that multi-agent is bad. It is that the payoff is highly task-dependent, tool-heavy tasks suffer from coordination overhead, and stronger single-agent baselines often leave less room for extra agents to help.

That is the part a lot of agent discourse still skips over. "More agents" is not an explanation. It is a bill. If you split a system, you should be able to say what you bought with that bill.

Did you buy better decomposition? Lower routing ambiguity? A real trust boundary? Parallel search? A memory controller the base model does not have? If you cannot answer that, the graph is probably doing theater on top of a simpler failure mode.

## 2. Semantic Quarantine

The most useful result in the UBC paper is not just that some multi-agent systems can be collapsed into one. It is where that collapse breaks.

As the authors scale up a single agent's skill library, performance does not degrade gracefully. It stays solid through 10, 30, even 60 skills. Then it hits a collapse zone in the 80 to 90 range. For GPT-4o-mini, the threshold is about 92 skills. For GPT-4o, it is 84. Beyond that point, selection accuracy drops sharply. The paper attributes that failure to semantic confusability: too many nearby tool descriptions occupying the same action space.

That is not just a benchmark curiosity. It explains a lot of agent engineering in the wild.

> An agent is not a persona. It is a namespace.

That sentence is my interpretation, not the paper's. But it fits the evidence better than the folk psychology does. Your support stack does not need a separate database agent because SQL requires a different species of mind. It often needs one because throwing `resolve_ticket`, `query_user_db`, `fetch_marketing_campaigns`, `refund_order`, and `check_entitlement` into one flat tool universe raises the odds of routing collisions.

I think of this as semantic quarantine.

Multi-agent decomposition is often not what you build to increase reasoning depth. It is what you build when the action space becomes too crowded to govern cleanly. Once you cross the disambiguation threshold, splitting the system is a way to quarantine neighboring skills so the model can make smaller, cleaner decisions.

That is also why hierarchical routing works. It does not magically expand the model's intelligence. It factorizes one overloaded decision into several smaller ones.

[ROMA: Recursive Open Meta-Agent Framework for Long-Horizon Multi-Agent Systems](https://arxiv.org/abs/2602.01848) is the strongest architecture answer to this problem in the current set of papers. Its recursive Atomizer-Planner-Executor-Aggregator structure keeps local decisions manageable and compresses intermediate outputs before passing them onward. On the paper's benchmarks, that design improves SEAL-0 by 9.9% and posts strong results on EQ-Bench. The main lesson is not that recursion is always best. It is that once the action space crosses the threshold, better decomposition usually beats louder prompting.

[SkillOrchestra: Learning to Route Agents via Skill Transfer](https://arxiv.org/abs/2602.19672) reaches a similar destination from a different direction. Instead of training an opaque routing policy end to end, it builds a reusable skill handbook of agent competence and cost, then routes using explicit performance-cost tradeoffs. Again, the lesson is not "more agents." It is "more structure around what each decision is for."

That is where a lot of production stacks should get less romantic. Flat persona committees are often an expensive way to solve a routing problem.

## 3. Where Multi-Agent Is Real

The compiler-workaround framing breaks in predictable places, and it is important to be explicit about them.

You can compile away a routing workaround. You cannot compile away a trust boundary.

You can simplify a noisy tool graph. You cannot wish away genuine heterogeneity if the system really does need different substrates.

That is why [The Vision Wormhole: Latent-Space Communication in Heterogeneous Multi-Agent Systems](https://arxiv.org/abs/2602.15382) is interesting. It does not assume that one homogeneous model will absorb everything. It takes heterogeneity seriously and asks how different models should communicate when their internals do not naturally line up.

The same goes for governance. [Intelligent AI Delegation](https://arxiv.org/abs/2602.11865) is better treated as a framing paper than as decisive empirical proof of better system performance. But the problem it names is real. Sometimes you want a reviewer that can challenge a proposal, a safety critic that is isolated from the system it monitors, or a delegate that behaves differently when the task becomes high stakes. Those are not just orchestration conveniences. They are institutional boundaries.

Embodied and distributed coordination also break the shortcut. [EmCoop: A Framework and Benchmark for Embodied Cooperation Among LLM Agents](https://arxiv.org/abs/2603.00349) shows why process-level measurement matters once multiple actors share a world. Agents interrupt each other, replan at bad times, and pay real costs for waiting and communication. [MultiAgentBench: Evaluating the Collaboration and Competition of LLM Agents](https://arxiv.org/abs/2503.01935) points in the same direction by treating coordination protocols, milestone tracking, and planning quality as first-class evaluation targets.

Exploration is the last big exception. [Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization (EMPO2)](https://arxiv.org/abs/2602.23008) is useful here by analogy more than by strict category. It shows that external scaffolding can produce better trajectories that are only later internalized. If your goal is to widen coverage over possible solutions rather than minimize latency on a single request, multiple actors or multiple exploratory paths can make sense even if you later compress what they discovered.

That is the sane middle ground. Multi-agent is neither fake nor fate. It is a conditional tool. The mistake is not using it. The mistake is pretending the same reason explains every case.

## 4. Text Is the Bottleneck, Not the Enemy

The first half of this story is about why systems split. The second half is about what they pay once they do.

The recent papers do not justify "the death of English." They do justify a narrower claim that matters in practice: text is becoming the bottleneck in some multi-agent settings.

[The Vision Wormhole](https://arxiv.org/abs/2602.15382) makes the cleanest current case. When one model compresses a rich internal state into text and another reconstructs meaning from that text, the handoff is slow, bandwidth-limited, and lossy. Their workaround is to repurpose the visual pathway of vision-language models as a higher-bandwidth coordination channel. On the setups they test, that yields an average accuracy gain of 6.3 percentage points and about 1.87x faster execution.

[Latent Collaboration in Multi-Agent Systems](https://arxiv.org/abs/2511.20639) pushes in the same direction. Its LatentMAS design moves hidden-state information directly and reports large gains in speed and token efficiency relative to text-based collaboration on the benchmarks it evaluates. Whether those methods survive production constraints is still open. What they show is that serious groups are no longer treating text relay as the unquestioned default for machine-to-machine coordination.

[EmCoop](https://arxiv.org/abs/2603.00349) attacks the same problem from the other side. Instead of inventing a new channel, it measures what happens when teams communicate under different topologies. In MA-Crafter with GPT-5.2 on 3-agent teams, the paper reports:

- Independent: 0 messages, 1.65 decision overhead.
- Centralized: 39 messages, 2.55 decision overhead, 0.49 plan coherence.
- Debate: 25 messages, 2.84 decision overhead, 0.04 plan coherence.
- Decentralized: 103 messages, 3.90 decision overhead, 0.00 plan coherence.

More talk, in other words, does not automatically produce more coordination.

The deeper issue is that text messages are propositions. They invite evaluation, disagreement, clarification, and revision. The moment one agent says "I found three endpoints," the receiver has new options: verify, revise, query, object, wait, or replan. A typed state transfer can still trigger disagreement, but it does not automatically drag the same discursive overhead behind it.

That is why the strongest practical lesson is simpler than "go latent." Stop treating long natural-language handoffs as a free abstraction. If agents have to talk, make them exchange the smallest useful state. Prefer typed fields over paragraphs. Prefer compact plans over autobiographies. Prefer bounded schemas over self-important debate transcripts.

The frontier may be latent. The immediate win is almost always less chatter.

## 5. The Swarm as Training Rig

The most promising pattern in this literature is not that multi-agent systems disappear. It is that some of their benefits can be pushed into training, adaptation, or policy design somewhere else.

That is where the second claim in this essay earns its keep:

> A swarm is often a training rig, not a destination.

[EMPO2](https://arxiv.org/abs/2602.23008) gives the clearest mechanism. During training, the agent receives external memory tips generated from prior episodes. Those tips are not vague reflections. They are concrete failure analyses and corrective hints. The rollouts improve because the agent is using external scaffolding.

Then the paper does the interesting part: it updates the policy so the useful behavior gets absorbed even when the tips are no longer present. In plain language, the agent learns from the scaffold instead of depending on it forever. That is why the result matters. Some external guidance is valuable precisely because it creates trajectories worth distilling.

The benchmark numbers are not small. EMPO2 reports a 128.6% improvement over GRPO on ScienceWorld, an 11.3% gain on WebShop, and a 136% average improvement in out-of-distribution transfer within 10 steps. Those are benchmark results, not a universal law. But the mechanism is suggestive.

[Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for LLM Agents](https://arxiv.org/abs/2601.01885) tells a related story for state management. Instead of treating long-term and short-term memory as separate external modules, it exposes STORE, RETRIEVE, UPDATE, SUMMARIZE, FILTER, and DELETE as actions inside the policy itself. On the paper's benchmarks, that unified memory policy improves both performance and context efficiency over strong baselines. If your current system has a separate memory agent mainly because the base agent cannot govern memory cleanly, this is exactly the kind of result that should make you revisit that boundary.

[AgentArk: Distilling Multi-Agent Intelligence into a Single LLM Agent](https://arxiv.org/abs/2602.03955) belongs in the same bucket, but with careful wording. It does not prove that all multi-agent intelligence can be transferred into one model with negligible loss. What it does show is that distilling multi-agent reasoning traces into a single agent can improve single-agent performance, and that process-aware distillation is the strongest of the paper's tested strategies.

What makes AgentArk and EMPO2 interesting together is the direction they point. AgentArk distills social scaffolding: debate, critique, and correction across multiple agents. EMPO2 distills personal scaffolding: tips and reflective guidance attached to one agent's own exploration. Both suggest that some of the value in scaffolds belongs in the traces they generate, not in the permanent runtime structure.

That does not justify a grand prophecy that every swarm will be compiled away. It does justify a much healthier engineering loop:

1. Prototype with scaffolds.
2. Log the debates, routing decisions, memory operations, and corrections that actually help.
3. Ask which parts are valuable because they create better trajectories and which parts are just expensive inference-time ceremony.
4. Internalize what you can.
5. Keep the scaffold only where it remains genuinely load-bearing because of trust, heterogeneity, or real distributed coordination.

That is not a law of history. It is a better default workflow.

## What To Build Differently On Monday

If you ship agent systems, the practical playbook from this literature is pretty direct.

1. Start with a single agent when the system is one model plus tools. Do not add personas until you can name the bottleneck you are fixing.
2. When routing starts to fail, think in namespaces and local action spaces. Better decomposition usually beats more theatrical prompting.
3. If you split the system, avoid flat committees. Use recursive or skill-aware routing that keeps each decision below the confusion threshold.
4. Treat communication as a design surface. Minimize natural-language handoffs first. Experiment with richer internal channels only where the cost is justified.
5. Measure process, not just outcomes. If you cannot see interruptions, communication load, plan coherence, or routing collapse, you do not actually know why the system works.
6. Internalize the scaffolding when you can. External memory, review passes, debate loops, and exploratory helpers may belong in training, adaptation, or fallback paths instead of the hot path of every production request.

The one-sentence version is simple: multi-agent systems are often useful, but their value usually comes from specific coordination mechanisms, and many of those mechanisms can be simplified, compressed, or internalized once you understand what problem they were solving.

## Two Bets For March 2027

Only two predictions are worth making from this set, and both should be embarrassing if wrong.

**Prediction 1:** By March 31, 2027, at least one major agent framework or hosted agent platform will ship graph-simplification or evaluator tooling that explicitly recommends collapsing some multi-agent workflows into a single-agent-plus-tools configuration. This is falsified if mainstream platforms still treat multi-agent graphs as design-time artifacts only, with no first-class simplification or optimization pass.

**Prediction 2:** By March 31, 2027, at least two publicly described production compound-AI systems from major vendors or labs will use non-text intermediate handoffs for selected internal coordination paths, whether via typed state transfer, model-native state transfer, or latent channels. This is falsified if public production descriptions still rely exclusively on natural-language or JSON relay for internal multi-model coordination.

Those are narrow predictions on purpose. The literature here is strong enough to change how builders think. It is not strong enough to support prophecy.

The next frontier is not more agents. It is better answers to four questions: when should a system split, what should stay local, how should state move, and which scaffolds deserve to survive deployment. If multi-agent is often a compiler workaround, the real job is not to admire the workaround. It is to understand exactly what it is compensating for.

## Reference Notes

All links below point to the underlying paper or paper PDF, not to summaries or secondary commentary.

### 1. [When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail](https://arxiv.org/abs/2601.04748) ([PDF](https://arxiv.org/pdf/2601.04748.pdf))

This is the anchor source for the whole essay. I cite it for the main empirical claim that many multi-agent systems can be compiled into a single agent with skills at much lower cost, for the 53.7% token reduction and 49.5% latency reduction figures, and for the more interesting failure mode: the collapse in skill selection once the library becomes too semantically crowded. The paper is doing two jobs here. It supports the "compiler workaround" thesis, and it supplies the evidence behind the semantic-quarantine argument.

### 2. [Toward Efficient Agents: Memory, Tool Learning, and Planning](https://arxiv.org/abs/2601.14192) ([PDF](https://arxiv.org/pdf/2601.14192.pdf))

I use this survey as field context rather than as a source of one marquee number. Its value in the essay is that it keeps the main thesis from sounding like a one-paper extrapolation. The survey shows that efficient agent work keeps converging on the same operational themes: memory control, tool selection, bounded context, and planning efficiency.

### 3. [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296) ([PDF](https://arxiv.org/pdf/2512.08296.pdf))

This paper is the main reality check against simplistic pro-agent or anti-agent takes. I cite it for the controlled 180-configuration study, for the claim that multi-agent payoff depends heavily on task structure and coordination topology, and for the broader point that stronger single-agent baselines can erase much of the marginal value of extra coordination. It is the essay's best source for "conditional tool, not destiny."

### 4. [ROMA: Recursive Open Meta-Agent Framework for Long-Horizon Multi-Agent Systems](https://arxiv.org/abs/2602.01848) ([PDF](https://arxiv.org/pdf/2602.01848.pdf))

ROMA is the counterweight to the essay's skepticism. I cite it because it shows what a genuinely useful multi-agent architecture looks like when the system really does need structured decomposition and aggregation. The paper supports the discussion of recursive breakdown, compressed intermediate state, and the 9.9% gain on SEAL-0. It is the cleanest example in this piece of multi-agent design earning its keep rather than just masking routing confusion.

### 5. [SkillOrchestra: Learning to Route Agents via Skill Transfer](https://arxiv.org/abs/2602.19672) ([PDF](https://arxiv.org/pdf/2602.19672.pdf))

SkillOrchestra is cited to support the claim that explicit routing structure is often more valuable than a vaguely "smart" orchestrator. The paper models agent competence and cost by skill, then routes using an explicit performance-cost tradeoff. That is why it appears in the semantic-quarantine section: it reinforces the idea that better routing formalisms often matter more than adding more personas.

### 6. [The Vision Wormhole: Latent-Space Communication in Heterogeneous Multi-Agent Systems](https://arxiv.org/abs/2602.15382) ([PDF](https://arxiv.org/pdf/2602.15382.pdf))

This is the central source for the essay's communication argument. I use it for two distinct claims: first, that heterogeneity can make multi-agent structure genuinely necessary; second, that text handoffs can be a serious systems bottleneck. The cited numbers in the article, including the 6.3 percentage point accuracy gain and roughly 1.87x speedup, come from this paper's comparison between text-based and latent-space coordination.

### 7. [Intelligent AI Delegation](https://arxiv.org/abs/2602.11865) ([PDF](https://arxiv.org/pdf/2602.11865.pdf))

I cite this paper carefully and narrowly. It is not doing heavy empirical lifting in the essay. Instead, it gives language and framing for delegation, authority, and governance boundaries. Its role is to support the claim that some agent boundaries exist for institutional reasons, not because the base model failed a routing test.

### 8. [EmCoop: A Framework and Benchmark for Embodied Cooperation Among LLM Agents](https://arxiv.org/abs/2603.00349) ([PDF](https://arxiv.org/pdf/2603.00349.pdf))

EmCoop is the main process-measurement source in the piece. I cite it for the message counts, decision-overhead metrics, and plan-coherence comparisons across independent, centralized, debate, and decentralized topologies. Those measurements matter because they show that communication design is not cosmetic. It changes the control flow of the system and can actively degrade performance when the topology gets noisy.

### 9. [MultiAgentBench: Evaluating the Collaboration and Competition of LLM Agents](https://arxiv.org/abs/2503.01935) ([PDF](https://arxiv.org/pdf/2503.01935.pdf))

This citation supports the essay's argument that evaluation itself is becoming a serious part of the agent stack. I use it to back the claim that milestone tracking, coordination protocol quality, and process-level observability deserve to be measured directly rather than inferred from a final task score.

### 10. [Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization (EMPO2)](https://arxiv.org/abs/2602.23008) ([PDF](https://arxiv.org/pdf/2602.23008.pdf))

EMPO2 is the anchor source for the "swarm as training rig" section. I cite it for the idea that external scaffolding can improve trajectories during training and then be partially absorbed into the base policy. The benchmark numbers in the article, including the 128.6% ScienceWorld improvement and the 136% average transfer gain, come from this paper. Its importance here is mostly conceptual: it gives a concrete mechanism for turning scaffolds into learned behavior.

### 11. [Latent Collaboration in Multi-Agent Systems](https://arxiv.org/abs/2511.20639) ([PDF](https://arxiv.org/pdf/2511.20639.pdf))

This paper reinforces the communication argument from a second angle. I use it to support the claim that moving hidden-state information directly can outperform text-based collaboration in both speed and token efficiency. In the essay it functions as corroboration, not as the sole pillar of the claim.

### 12. [Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for LLM Agents](https://arxiv.org/abs/2601.01885) ([PDF](https://arxiv.org/pdf/2601.01885.pdf))

Agentic Memory is cited to support the argument that some components often split into separate agents, especially memory controllers, may be better internalized as policy-level actions. Its contribution to the essay is the unified-memory framing: storing, retrieving, filtering, summarizing, and deleting memory can be part of the agent's action repertoire rather than outsourced to a separate orchestration layer.

### 13. [AgentArk: Distilling Multi-Agent Intelligence into a Single LLM Agent](https://arxiv.org/abs/2602.03955) ([PDF](https://arxiv.org/pdf/2602.03955.pdf))

AgentArk is the clearest direct citation for distilling multi-agent traces into a single model. I use it to support the narrower claim that some multi-agent value can be transferred into weights, especially when the distillation process preserves reasoning traces and interaction structure. It is intentionally not cited as proof that every useful swarm can be compiled away. The paper supports a conditional engineering workflow, not a universal law.
