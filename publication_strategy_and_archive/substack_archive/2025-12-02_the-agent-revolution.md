# Autonomous AI Agents: Core Foundations and Recent Breakthroughs

Date: 2025-12-02
URL: https://lambpetros.substack.com/p/the-agent-revolution

This video is the TL;DR

**Now HIT PLAY at the AUDIO and skim the POST along with the HOSTS.**

*How LLM-based agents evolved from simple chatbots to autonomous researchers, collaborators, and problem-solvers*

## 

---

# **Part 0 — Introduction: How We Got Here**

Over the last three years, the word *agent* has gone from an aspirational buzzword to an uncomfortable fact of everyday engineering. A modern LLM is no longer just something you prompt for an answer. Increasingly, it’s something you delegate a task to — a system that plans, takes actions, makes observations, uses tools, revises its decisions, recovers from mistakes, and sometimes even collaborates with other agents. The transformation has been fast, uneven, and occasionally confusing. Yet the arc is unmistakable: language models are leaving the domain of pure prediction and entering the world of autonomous, goal-directed behavior.

If you’ve tried building an agent yourself, you’ve felt both sides of that shift. You’ve seen magical demos that collapse under real-world pressure. You’ve tried frameworks that promise autonomy but still require a forest of glue code. You’ve watched models take three brilliant steps followed by a catastrophic fourth. The literature, meanwhile, has exploded — dozens of papers a month, each proposing a new technique, a new architecture, a new benchmark, or a new story about how agents “should” work.

This deep dive is my attempt to make sense of that landscape — not by summarizing hype or listing frameworks, but by walking through the **research papers** that genuinely — and measurably — shifted the trajectory of agent development. These papers, taken together, form a coherent story: how we went from clever prompting tricks to purpose-trained agentic models, from scripted tool wrappers to latent-space coordination, from static datasets to continuous learning, from linear reasoning chains to complex multi-agent ecosystems.

To make this navigable, I’ll use a simple, consistent structure. For each paper, I’ll ask a few guiding questions: *What problem is this solving? Why did it matter at that moment? What’s the central idea? How does it work? And what changed afterward?* The answers will be narrative rather than bullet-driven — dense where needed, but always focused on helping you understand *why* this particular step mattered in the emergence of modern agents.

We begin at the most pivotal turning point of all: the moment when language models learned to separate **thinking** from **acting**.

## **The Scroll Map**

Here’s the path we’ll follow:

* **Part 1 — Foundations & Early Frameworks**

  ReAct, tool-use, and the first multi-agent frameworks that made agent systems feel real.
* **Part 2 — Scaling Agents via Pre-Training**

  Why “just chain tools together” stopped working, and how Agentic CPT tries to fix it.
* **Part 3 — Learning from Early Experience**

  Agents that learn from their own trajectories instead of relying only on static datasets.
* **Part 4 — The Agentic RL Revolution**

  A new subfield: reinforcement learning shaped around agents, not just single-step predictions.
* **Part 5 — Latent Space Collaboration**

  Multi-agent systems that collaborate in latent space instead of messy token logs.
* **Part 6 — World Models & Embodied Agents**

  Agents that live in simulated worlds and learn within scalable environments.
* **Part 7 — Scientific Discovery & Research Automation**

  AI scientists, automated theorem proving, and high-stakes reasoning.
* **Part 8 — Advanced Reasoning Systems**

  Continuous latent reasoning, hybrid approaches, and where “pure LLM reasoning” is giving way to new structures.
* **Part 9 — Synthesis & Future Directions**

  What all of this means for practitioners, researchers, and founders.

We’ll finish with a **reference section** you can use as a reading list.

---

# **Part 1 — Foundations: When Reasoning Learned to Touch the World**

## **ReAct (ICLR 2023)**

**ReAct: Synergizing Reasoning and Acting in Language Models**

<https://arxiv.org/abs/2210.03629>

*What problem does this solve?*

Before ReAct, LLMs were capable of reasoning or acting, but not both in a structured way. You could ask a model to reason step-by-step, or you could ask it to output some command to a tool, but the model had no disciplined way to interleave these behaviors. As soon as a task required several rounds of planning, tool use, and observation, the system fell apart. Tasks like web navigation or iterative code debugging simply didn’t fit the “single shot” paradigm.

*Why did this matter at that moment?*

ReAct created a simple but extremely powerful pattern: alternate explicit “Thought” steps with explicit “Action” steps, then feed the results back as “Observation.” Suddenly the model had a protocol — not just a prompt — for interacting with the world in a controlled, inspectable loop. It wasn’t just generating; it was behaving. That pattern quickly became the blueprint for nearly every agent architecture that followed.

*What’s the core intuition?*

Give the model a workspace in which it can think out loud, but force it to label its internal reasoning separately from the actions it intends to take. This separation turns the model’s output into an intelligible sequence of intentions and effects. A ReAct-style trace looks something like:

```
Thought: I need to check the weather in Athens today.
Action: web_search[”Athens weather forecast”]
Observation: Cloudy with temperatures around 22°C.
Thought: Now I can summarize the forecast accurately.
Final Answer: It’s cloudy in Athens today, around 22°C.
```

The structure is almost trivial, yet transformative. The model is no longer expected to compress reasoning, planning, and acting into one opaque response. Instead, it proceeds step by step, with clear boundaries between cognition and interaction.

*How does it work in practice?*

The execution loop around the model is straightforward. At each step you build a prompt from the conversation history, let the model produce either a Thought or an Action, interpret the Action, and feed the Observation back into the next turn. A minimal version looks like this:

```
history = []

while True:
    prompt = render_prompt(history)
    reply = llm(prompt)

    if is_final(reply):
        break

    if is_action(reply):
        result = run_tool(parse_action(reply))
        history.append((”Observation”, result))
    else:
        history.append((”Thought”, reply))
```

This “thin wrapper” was enough to push LLMs into territory that previously required bespoke planning algorithms or RL policies.

*What changed after ReAct?*

The field finally had a **canonical control pattern**. Agent frameworks emerged almost immediately, each adding planners, critics, memory systems, or hierarchical controllers — but all built on top of the Thought-Action-Observation loop. Even today, when we train explicitly agentic models, you can still see the imprint of ReAct in their interface and behavior. It was the conceptual spark that lit the rest of the field.

---

## **AutoGen (NeurIPS 2023)**

**AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation**

<https://arxiv.org/abs/2308.08155>

*What problem does this solve?*

Once ReAct proved that a single model could reason and act in multiple steps, the natural next idea was collaboration. Could several LLMs — each with a role, a viewpoint, or a specialized capability — work together on a task? Early experiments suggested yes, but they were brittle and ad hoc. Teams of LLMs tended either to talk themselves into loops or to collapse after a few steps. What was missing was a structured programming model for multi-agent interactions.

*Why did this matter at that moment?*

AutoGen gave the field its first serious attempt at a **multi-agent architecture**. Instead of having a single LLM do everything, you could assign different responsibilities to different agents: a planner to produce the outline, a coder to generate and run code, a reviewer to catch mistakes, a user proxy to ensure alignment with the original intent. This division of labor made complex tasks more tractable and opened the door to genuinely collaborative behaviors.

*What’s the core intuition?*

Think of agents as characters in a play. Each has:

* a personality or role (e.g., “planner”, “coder”),
* a set of tools they may use,
* and policies governing when they decide to speak.

Then let them converse in a controlled graph until the task converges. The human gives an initial message to a “user proxy,” and the agents handle the rest.

A simple AutoGen program looks almost like pseudocode for a small organization:

```
planner = AssistantAgent(”planner”)
coder = AssistantAgent(”coder”)
user = UserProxyAgent(”user”, human_input_mode=”NEVER”)

user.initiate_chat(planner, message=”Build a Python script to summarize a CSV.”)
```

The planner interprets the request, the coder implements it, and the user proxy decides when the conversation has reached a satisfactory result.

*How does it change agent development?*

AutoGen made it normal — even expected — to break tasks into specialized roles. That, in turn, made people think more clearly about **coordination**, **intermediate artifacts**, **division of responsibility**, and **termination conditions**. It also set off a wave of successor frameworks that treat multi-agent setups as standard practice.

*Why wasn’t this enough on its own?*

Because despite the elegance of the design, the base models still weren’t “agentic” by nature. They could follow the protocol, but they didn’t have any inherent sense of persistence, strategy, or long-horizon coherence. The next leap required changing something deeper: the models themselves.

---

## **Transition: From Prompted Agents to Trained Agents**

The early frameworks — ReAct for single-agent control and AutoGen for multi-agent orchestration — showed that LLMs could be turned into agents through protocol and structure alone. But these systems were always a bit fragile. The models had no intrinsic understanding of what it meant to plan, to observe, to revise a decision, or to coordinate with others. They were being *guided* into acting like agents, not *trained* to be agents.

The research community soon reached a clear inflection point. If agents were going to scale — in reliability, in complexity, in generality — they needed **agentic priors baked into their weights**, not just into their prompts. This realization set off the next major phase: agentic continual pre-training.

---

# **Part 2 — Agentic Pre-Training: When Models Learn to Be Agents**

## **Scaling Agents via Continual Pre-Training (2025)**

**Scaling Agents via Continual Pre-Training**

<https://arxiv.org/abs/2509.13310>

*What problem does this solve?*

The early agent frameworks demonstrated that we could *force* an LLM to behave like an agent by wrapping it in structured prompting loops. But these systems all shared a quiet flaw: the base model had no inherent understanding of the behaviors we were trying to elicit. Every plan, every action, every tool call, every attempt at recovery was improvised on top of a model pre-trained purely for next-token prediction on internet text. As tasks became longer and more complex — multi-page browsing sessions, multi-step tool interactions, or lengthy code-debugging episodes — the model’s lack of internal structure became increasingly obvious. Agentic behavior felt bolted on, not natural.

*Why did this matter in the field?*

The paper marks the moment when researchers stopped treating agentic behavior as a “prompt-time trick” and began treating it as a **property of the model itself**. Instead of leaning on ever more elaborate wrapper logic, “Scaling Agents via Continual Pre-Training” proposed to modify the model’s *own distribution* by feeding it large-scale trajectories of agents interacting with tools, browsers, code environments, and task-oriented workflows. In other words: teach the model to be an agent the same way we taught it to be a writer — through massive, diverse exposure.

*What’s the central intuition?*

Just as next-token prediction on text gives a model a general prior for language, continual pre-training on agentic trajectories gives it a prior for **acting**. The model doesn’t just observe sentences. It observes sequences like:

```
Thought: I need to filter rows where “status” is “active”.
Action: python_exec[”df = df[df.status == ‘active’]”]
Observation: DataFrame returned with 1,284 rows.
Thought: Now I can compute the summary statistics.
```

Over millions of such segments, the model internalizes patterns of planning, exploration, error recovery, tool sequencing, and intermediate state reasoning. Instead of being surprised by multi-step tasks, the model expects them.

*How does this work technically?*

The authors collect a large corpus of agent trajectories from a mixture of scripted agents, human-written demonstrations, synthetic rollouts, and environment interactions. The model is then continually pre-trained with a mixed objective combining language modeling and agentic prediction. A simple caricature of the training loop looks like:

```
for batch in dataloader:
    lm_loss = model.lm_loss(batch.text)

    # trajectory includes thoughts, actions, observations
    agent_loss = model.trajectory_loss(batch.trajectory)

    loss = lm_loss + λ * agent_loss
    loss.backward()
    optimizer.step()
```

The λ coefficient controls how strongly the model leans toward agent-like behavior versus general text modeling. This mixture proved essential: too much agentic data and the model overfits to procedural patterns; too little and it reverts to generic LLM behaviors.

*What did this actually change?*

The authors introduce a family of models around 30B parameters that achieve substantial improvements on several demanding agentic benchmarks. On **BrowseComp-en**, a genuinely challenging browser-use benchmark, the model reaches around 40% success — a major increase over wrapper-based approaches at the time. On **BrowseComp-zh**, it improves further. And on **HLE**, a household-environment benchmark requiring long-horizon reasoning, the model reaches around 31% Pass@1.

The exact percentages are less important than the qualitative shift: these models handled multi-step tasks with noticeably more coherence, stability, and willingness to revise their own intermediate steps.

*What changed after this?*

Once agentic behavior became something learned through pre-training, rather than something layered through prompting, the entire field reorganized itself. Framework developers could assume that models would already “understand” the concept of a plan, a tool, an observation, or a corrective step. Researchers began exploring whether the model could also learn from its **own** experiences, not just curated trajectories. And practitioners started seeing agentic behavior that used to require heavy scaffolding begin to emerge with far lighter wrappers.

This transition leads naturally to the next major chapter in agent development: agents that refine themselves based on early deployment experience.

---

# **Part 3 — Learning From Early Experience: Agents That Improve Themselves**

## **Agent Learning via Early Experience (2025)**

**Agent Learning via Early Experience**

<https://arxiv.org/abs/2510.08558>

*What problem does this solve?*

Even with agentic continual pre-training, all the trajectories come from a controlled, artificial corpus. But real agents encounter messy environments: users with inconsistent instructions, edge-case tool failures, stale web pages, misleading content, or instructions phrased in unexpected ways. A model that looks strong on pre-training data can still stumble dramatically in the first weeks of actual deployment. The authors ask a natural next question: *can we use those early failures and partial successes as high-value training data?*

*Why is this important?*

This paper is one of the earliest to treat the first phase of deployment as a **learning opportunity** instead of a risk to be minimized. If a thousand agents stumble differently across ten thousand initial tasks, those trajectories contain patterns no synthetic training set can capture. The idea is to harvest them — safely, systematically, selectively — and then fine-tune the model on the parts that lead to better behavior.

*What’s the key intuition?*

Early experience is high-signal because it exposes the mismatch between the training distribution and the real world. If you can filter these trajectories carefully enough — keeping those that show useful strategies or recoverable failure patterns — the model can close that gap far more efficiently than through brute-force synthetic data collection.

*How does this work under the hood?*

The pipeline is conceptually simple but operationally delicate. The system deploys agents with strict safety layers and logging. Each trajectory is annotated with success metrics, error types, recovery attempts, and user satisfaction signals when available. A curation step removes unsafe, uninformative, or misleading episodes. The remaining data serves as a fine-tuning set.

A simplified version of the refinement loop looks like:

```
episodes = collect_first_phase_episodes()

for ep in filter_high_quality(episodes):
    imitation_loss = model.imitation(ep)
    if ep.success:
        imitation_loss += success_bonus(ep)
    imitation_loss.backward()
    optimizer.step()
```

Notice that this is not RL yet — it’s imitation plus selective emphasis. But it already behaves like a feedback loop: deployment creates data, data improves the model, the improved model produces better deployments, and so on.

*What did this change?*

Systems trained with early-experience learning showed noticeably better robustness to unpredictable inputs, better recovery from tool failures, and improved ability to generalize task structure. More interestingly, they sometimes developed *fallback strategies* that did not appear in the initial synthetic trajectories — evidence that the model was absorbing structure from real-world interactions, not just memorizing.

*Where does this lead the field?*

This work is the conceptual bridge to full **agentic reinforcement learning**, where models not only imitate good behavior but optimize toward explicit multi-step reward signals. To understand that step, we need a map of how researchers formalized the RL landscape for agents — which brings us to a major survey.

---

# **Part 4 — Agentic Reinforcement Learning: Optimizing Behavior, Not Just Imitating It**

## **The Landscape of Agentic Reinforcement Learning for LLMs (2025)**

**The Landscape of Agentic Reinforcement Learning for LLMs: A Survey**

<https://arxiv.org/abs/2509.02547>

*What problem does this survey address?*

By late 2025, many groups were experimenting with reinforcement learning on top of LLM agents. Some optimized tool-use accuracy, others tuned planning strategies, still others trained agents inside simulated environments where success or failure yielded a reward. The result was a chaotic collection of methods, each claiming improvements on some benchmark, with little clarity about how they related or which ideas actually generalized. This survey set out to impose order on the chaos and to define what “agentic RL” even means in the context of LLMs.

*Why is this important in the agent story?*

Earlier phases focused on *pre-training on trajectories* and *learning from early experience* in an essentially supervised fashion. Reinforcement learning introduces something different: explicit optimization for long-horizon success, guided by scalar rewards. For agents, this matters because many real tasks do not have clean step-by-step supervision. You know if the whole episode ultimately worked; you don’t always know which intermediate action was good or bad. This survey explains how different works handled that challenge, which in turn shapes how we think about training robust, goal-directed agents.

*What is the central intuition of the survey?*

The authors organize agentic RL methods along a set of axes that capture the design decisions you have to make:

* What is the **action space**? Free-form text? Structured tool calls? Low-level environment actions?
* Where do **rewards** come from? Human preferences? Automatic metrics (like accuracy or latency)? Environment signals (win/lose, success/failure)?
* How is **credit** assigned? Are rewards attributed to individual actions, whole trajectories, or something in between?
* What does the **policy** look like? A raw LLM? An LLM planner supervising a non-LLM controller? A multi-agent system sharing a global reward?

Seen through this lens, many disparate-looking papers turn out to be close cousins. That realization helps cut through the noise.

*How does agentic RL typically look in code?*

At its core, the RL loop for an LLM agent still resembles classic RL:

```
state = env.reset()
trajectory = []

while not done:
    action = agent.act(state)  # may involve prompting an LLM, choosing tools, etc.
    next_state, reward, done = env.step(action)
    trajectory.append((state, action, reward))
    state = next_state

agent.update_policy(trajectory)
```

The complexity lives inside agent.act and agent.update\_policy: they might involve multiple calls to an LLM, intermediate planning steps, or latent states. But structurally, the story is the same: explore, collect rewards, adjust.

*What are the main insights from the survey?*

A few patterns stand out. First, RL alone does not rescue a poorly pre-trained base model; it needs to operate on top of a strong agentic prior. Second, reward design is everything: narrow, brittle reward signals can produce impressive benchmark scores but agents that generalize poorly or game the metric. Third, curriculum matters: agents learn more effectively when tasks, tools, and environments are introduced in a staged fashion rather than all at once.

Most importantly, the survey highlights that the most promising methods tend to *combine* supervised trajectory learning, early-experience adaptation, and carefully designed RL — not treat them as mutually exclusive alternatives.

*How does this move us forward?*

With this taxonomy in place, it becomes easier to evaluate new proposals and to understand what is truly novel about them. It also sets the stage for more exotic directions: instead of having agents talk entirely in text and receive sparse textual rewards, what if they could coordinate in richer ways, share latent internal information, or learn inside simulated worlds? Those ideas motivate the next phase.

---

# **Part 5 — Latent Collaboration: When Agents Talk in Vectors, Not Only in Text**

## **LatentMAS: Latent Collaboration in Multi-Agent Systems (2025)**

**Latent Collaboration in Multi-Agent Systems (LatentMAS)**

<https://arxiv.org/abs/2511.20639>

*What problem does this paper solve?*

Most multi-agent systems up to this point have communicated via plain text messages. One agent writes a message, another reads it as part of its prompt, and so on. This is simple and interpretable, but it is also expensive and noisy. Text-based communication forces agents to pack their internal state into words over and over again, and it introduces a lot of redundancy. The authors of LatentMAS ask whether agents can instead communicate in a more compact, structured form: through **latent representations** that never surface as text.

*Why does this matter?*

If agents can collaborate via latent vectors, several things become possible. They can share rich internal information without bloating prompts. They can reason jointly about a task while keeping communication overhead low. And they can potentially learn more nuanced interaction patterns that are not constrained by linguistic surface form. In effect, agent conversations become operations in a shared representation space, rather than long chains of messages in natural language.

*What is the main intuition?*

Each agent has both an external-facing interface (which produces or consumes text when interacting with humans or tools) and an internal latent interface for communicating with other agents. Instead of typing to each other, agents exchange vectors. A collaboration might look like this conceptually:

```
# agent A encodes its beliefs into a latent vector
z_A = agentA.encode_state(task_context)

# agent B receives the latent message and updates its own state
agentB_state = agentB.update_from_latent(z_A)

# agent B decides on an action or a textual output
response = agentB.decode_action(agentB_state)
```

The important shift is that the “conversation” no longer clutters the prompt; it happens in a learned hidden space.

*How does it work technically?*

LatentMAS introduces architecture components that map textual or environmental information into latent representations, perform transformations on them, and then decode decisions or messages back out. Training involves multi-agent objectives where success depends on the quality of coordination mediated through these latent channels. The collaboration protocol is learned end-to-end under these objectives, rather than hand-specified.

*What does this change in practice?*

Latent collaboration reduces prompt size and cost, improves scalability as the number of agents grows, and opens the door to more sophisticated coordination strategies. It also blurs the line between “one big model with multiple modules” and “a team of models” — when collaboration happens in latent space, the distinction becomes more architectural than conceptual.

*How does this connect to the broader evolution?*

Once you allow agents to live and talk in latent spaces, it becomes natural to embed them in **latent worlds** as well: simulated environments that are not literally rendered text or pixels, but structured state spaces. This is the direction taken by research on world models and embodied agents, which we consider next.

---

# **Part 6 — World Models and Embodied Agents: Learning Inside Scalable Simulated Worlds**

## **Scalable World Models (Representative line of work)**

*What problem does this line of work address?*

Text-based tasks and browser environments are valuable, but they only cover a slice of what agents might do. Many challenges — robotics, complex games, logistics, scientific simulation, long-horizon planning — unfold in structured environments with states, actions, and dynamics that are not naturally expressed as linear text. Training agents directly in those environments is often expensive or unsafe. World models offer an alternative: train a model of the environment itself and let agents learn *inside* that model.

*Why is this important for agents?*

For language-based agents, world models expand the training domain from “documents and websites” to arbitrary interactive worlds. Agents can practice complex strategies cheaply and at scale, without touching real users or real infrastructure. They can explore many hypothetical futures, refine plans, and test policies in simulation. Even when the final deployment happens in a textual or browser environment, the intuitions learned from world model training can transfer.

*What is the core idea?*

A world model is a learned function that predicts the next state of the environment given the current state and action. Once trained, it becomes a kind of internal simulator:

```
state = world_model.encode(observation)

for t in range(horizon):
    action = agent.policy(state)
    state = world_model.predict_next(state, action)
```

The agent can unroll this imaginary trajectory to evaluate possible futures and choose actions that look promising — all without incurring the cost of running those actions in a real or expensive environment.

*How does this change agent training?*

Agents can now learn through a mixture of real and simulated experience. A typical pattern is to collect some real data, fit a world model, and then train agents inside that model with RL or imitation. Over time, improved policies can trigger collection of more diverse real data, which in turn refines the world model. This interplay between real and simulated experience tightens the feedback loop between data, model, and policy.

*How does this tie back to language-based agents?*

Even for agents that mainly operate through language and tools, world models provide a template: instead of reacting greedily at each step, agents can build internal rollouts of possible tool sequences, web navigation paths, or code execution trajectories. Some recent works explicitly cast planning as “imagining” sequences in a latent space and then choosing among them, blurring the boundary between symbolic planning and learned simulation.

---

## **Transition: From Acting in Text to Acting in Structured Worlds**

At this point in the story, the concept of an “agent” has expanded dramatically. We started with LLMs that simply alternated thoughts and actions in text. We then trained models that internalized agentic structure through continual pre-training and early-experience learning. We added reinforcement learning to optimize behavior, latent channels for collaboration, and world models to scale training beyond textual environments.

The natural next question is: if we can embed agents in richer worlds and coordinate them more efficiently, can we also push them into **richer intellectual domains**? Can they generate new knowledge, not just retrieve it? Can they discover proofs, conjectures, or experiments? The next phase of the evolution focuses on exactly that: agents as scientists and high-level reasoners.

---

# **Part 7 — AI Scientists and High-Level Reasoning: Agents That Generate Knowledge**

The previous stages gave agents the capacity to plan, to act, to learn from experience, to cooperate, and even to train within imagined worlds. But scientific and mathematical domains impose a new level of difficulty. These tasks aren’t just long-horizon; they demand rigor, abstraction, and the ability to manipulate structures that have no immediate sensory grounding. Agents must synthesize ideas, test hypotheses, correct mistakes, and produce artifacts—proofs, experiments, insights—that can withstand scrutiny. This is where the agent story shifts from *acting* to *reasoning at scale*.

Below we examine several representative lines of work: agents developing scientific hypotheses, agents solving formal reasoning tasks, and systems for self-directed research.

---

## **LUMINE (2025)**

**LUMINE: AI Scientist for Scientific Discovery**

<https://arxiv.org/abs/2511.16832>

*What problem does LUMINE solve?*

Classical LLMs are good at summarizing scientific papers or generating hypotheses on demand, but they are brittle when asked to **extend** scientific knowledge: forming new conjectures, evaluating competing explanations, or designing experiments that differentiate them. Scientific reasoning is inherently multi-step and self-reflective, requiring a structured loop of hypothesize → simulate → evaluate → revise. LLMs, when used naively, fall apart after one or two cycles.

LUMINE attempts to solve this by embedding an LLM inside a full research workflow: it plans research steps, executes simulations, reads and critiques its own logs, and iteratively refines hypotheses.

*Why does it matter in the agent timeline?*

LUMINE moves beyond “agents as tool users” toward “agents as researchers.” It treats scientific discovery not as a single generation task but as a long-horizon pipeline driven by iterative improvement. This opens the door to AI systems that perform exploratory intellectual work instead of merely responding to prompts.

*What’s the core intuition?*

Break scientific discovery into modular components—hypothesis generation, experiment planning, simulation execution, result interpretation—and assign these to specialized agent roles. Each agent uses domain tools (e.g., physics simulators, molecular dynamics engines) and exchanges intermediate representations. Critically, the system also includes agents whose job is to *criticize* and *stress-test* proposals.

A conceptual sketch of part of its loop might look like:

```
while not converged:
    hypothesis = generator.propose(context)
    plan = planner.design_experiment(hypothesis)
    results = simulator.run(plan)
    critique = reviewer.evaluate(hypothesis, results)
    context = updater.integrate(hypothesis, critique)
```

The agents are not simply chatting; they are manipulating structured scientific artifacts.

*What changed because of LUMINE?*

The system demonstrated early success in generating plausible hypotheses, designing discriminative experiments, and iteratively refining them. It didn’t solve science, but it showed that **scientific workflows can be decomposed into agentic primitives**, making them more tractable for LLM-based systems. LUMINE also inspired several follow-up projects that apply similar patterns to chemistry, climatology, and materials science.

---

## **Kosmos (2025)**

**Kosmos: AI Theorem Prover and Mathematical Researcher**

<https://arxiv.org/abs/2511.03848>

*What problem does Kosmos solve?*

Mathematics is even less forgiving than empirical science. A theorem is either true or false; a proof is either valid or invalid. Language models can sketch informal arguments but struggle to maintain formal correctness over long sequences, especially when multiple lemmas interact. Kosmos addresses this by embedding LLM reasoning inside a formal proving environment and treating theorem proving as a structured interaction between different agent roles.

*Why does it matter?*

Where LUMINE shows agents can scaffold scientific discovery, Kosmos shows they can scaffold **formal reasoning**. Mathematics requires tight control of logical structure, not just conceptual understanding. Coordinating multiple agents—such as a lemma generator, a proof planner, a tactic selector, and a verifier—turns out to be an effective strategy. Each role focuses on a different aspect of the problem, reducing the cognitive load on any single model.

*What’s the core intuition?*

Structure the proof search using multiple loops: a high-level planner decomposes the theorem into subgoals; subordinate agents propose candidate lemmas; a tactic agent transforms goals inside a proof assistant; and a verifier checks correctness.

The workflow resembles a branching, self-correcting search:

```
goal = theorem
stack = [goal]

while stack:
    current = stack.pop()
    plan = planner.decompose(current)
    candidates = lemma_generator.suggest(plan)
    for lem in candidates:
        if verifier.check(lem):
            stack.extend(lem.subgoals)
            break
```

The agents systematically explore the structure of the problem, guided by the verifier’s feedback.

*What changed because of Kosmos?*

Kosmos significantly increased the fraction of theorems solved from standard libraries. More importantly, it demonstrated that **formal reasoning benefits from agent decomposition** in the same way scientific research does. The idea that a single LLM should perform planning, lemma generation, tactic selection, and proof checking gave way to the idea that agents, properly specialized, can collaborate to produce rigorous results.

---

## **Aristotle (2025)**

**Aristotle: Deliberate Multi-Hop Reasoning with Agentic Self-Revision**

<https://arxiv.org/abs/2511.07229>

*What problem does Aristotle solve?*

General question answering tasks, particularly those requiring multi-step reasoning, challenge even strong models. They may propose plausible but incorrect chains of logic. Aristotle introduces a system where agents not only reason but *re-evaluate* their own intermediate steps, revising sub-answers as needed.

*Why does this matter?*

Aristotle is an example of a pattern that would become common: **self-revision as an explicit agentic subroutine**. Instead of emitting a chain of thought and hoping it’s right, the agent repeatedly scrutinizes its own reasoning, correcting earlier steps that no longer make sense in light of new evidence.

*What’s the core intuition?*

The system decomposes a question into sub-questions, answers them individually, and then reassembles the results into a coherent whole. Crucially, it doesn’t treat sub-answers as final. Instead, it repeatedly runs critique loops that evaluate individual reasoning steps:

```
subqs = planner.decompose(question)
answers = {q: solver.answer(q) for q in subqs}

for q in subqs:
    critique = critic.review_step(q, answers[q])
    if critique.requires_revision:
        answers[q] = solver.answer(q, critique.hints)
```

This iterative refinement stabilizes the reasoning chain and reduces error propagation.

*What changed after Aristotle?*

Self-revision became recognized as a core ingredient in robust reasoning systems. Many later agent frameworks embedded critiques, revision loops, or counterfactual reasoning modules directly into their architecture. Aristotle belongs to a lineage of systems that treat reasoning as *process*, not output.

---

## **CoCoNuT (2025)**

**CoCoNuT: Coordinated Control of Multiple Agents for Nonlinear Reasoning Tasks**

<https://arxiv.org/abs/2511.15593>

*What problem does CoCoNuT solve?*

Some reasoning tasks, particularly those involving nonlinear dependencies between subproblems, require coordination beyond simple decomposition. A rigid tree of sub-questions often fails because the solution to one subproblem depends intricately on the evolving solutions to others. CoCoNuT introduces a more dynamic form of agentic coordination, where multiple agents operate simultaneously on different parts of the problem but exchange intermediate states as needed.

*Why does this matter?*

It shows how agent collaboration can go beyond linear or even hierarchical decomposition. Instead of a clear step-by-step sequence, reasoning becomes a flexible dance involving shared context, mutual updates, and opportunistic jumps between ideas.

*What’s the central intuition?*

Allow agents to work in parallel on different aspects of a problem, but provide mechanisms for them to synchronize through shared intermediate structures. CoCoNuT maintains a workspace where each agent writes partial insights and reads others’ contributions. The system resembles a distributed research meeting rather than a strict pipeline.

```
workspace = {}

while not converged:
    for agent in agents:
        update = agent.contribute(workspace)
        workspace.update(update)
```

Agents coordinate implicitly through shared memory rather than explicit messaging.

*What changed because of CoCoNuT?*

It broadened the conception of what “multi-agent reasoning” means. Instead of sequential roles or tidy hierarchies, we saw the emergence of **collaborative reasoning ecosystems** where agents negotiate meaning through shared structures. This pattern has since influenced both software frameworks and architectural designs for next-generation models.

---

## **Transition: From Structured Reasoning to Integrated Agent Architectures**

At this stage, the field reached an intriguing point. We had systems for scientific discovery, theorem proving, and collaborative reasoning. We had agents that could critique themselves, refine sub-answers, coordinate through latent spaces, and train inside imagined worlds. But these capabilities were fragmented across different architectures and frameworks. The next natural step was synthesis: pulling these ingredients into unified agent platforms that developers could actually use at scale.

This brings us to the notion of the **Agent Stack** — the layered architecture that underlies modern agent systems.

---

# **Part 8 — The Agent Stack: The Architecture Beneath Modern Agents**

By this point in the story, agents have accumulated a remarkable range of abilities: structured thought-action loops, multi-agent collaboration, learned agentic priors from continual pre-training, adaptation from early deployment, reinforcement learning for long-horizon performance, latent communication channels, and even facility with world models and formal reasoning. But as these abilities multiplied, so did the architectural complexity required to manage them. In practice, no single model or paper-defined system could organize all these behaviors on its own.

The field began converging on a layered architecture — not a formal standard, but an emergent structure that appeared across frameworks and research efforts. This arrangement is widely referred to as **the Agent Stack**. It is the conceptual map that shows how all the contributions we’ve discussed align and interact.

---

## **1. The Foundation Layer: Pre-Trained Agentic Models**

At the base of the stack sits the model itself, enriched not only by language pre-training but also by exposure to agent trajectories, tool traces, simulated interactions, and early deployment data. The shift from generic language models to **agentic foundation models** represents the deepest structural change of the era. These models come equipped with powerful priors:

* that tasks often unfold over multiple steps,
* that observations constrain reasoning,
* that tools matter,
* that recovery from failure is itself a learned pattern.

An agent built on such a model begins with a significant advantage. It does not have to be taught the meaning of a plan or an observation through prompting alone; it has seen these patterns during training.

---

## **2. The Reasoning Layer: Planning, Self-Revision, and Multi-Hop Structure**

Above the foundation lies the reasoning layer—where systems like Aristotle, Kosmos, and CoCoNuT live. This layer contains algorithmic scaffolding that guides the model through complex tasks:

* planners that break problems into sub-tasks,
* critics that evaluate intermediate steps,
* revision loops that allow the system to correct itself,
* shared workspaces for nonlinear coordination.

This layer is not fixed; different tasks invoke different scaffolds. But the pattern is consistent: rich reasoning emerges not just from the model, but from the orchestration around it. The most successful systems treat the model as a participant in an algorithmic loop rather than an oracle.

---

## **3. The Environment Layer: Tools, Browsers, Simulators, and Worlds**

Agents act in environments. Early systems treated environments as a thin wrapper around Python or a few APIs. Later systems expanded this dramatically:

* browser automation environments,
* operating system interfaces,
* structured scientific simulators,
* formal verification tools,
* latent world models.

Each environment imposes constraints and opportunities. The agent must reason not only about text but about state, action, and consequence. This layer is where the model’s agentic prior meets the real world—or the simulated one.

A typical environment loop looks something like:

```
while not done:
    thought = llm(reason(history))
    action = decode_action(thought)
    observation = env.step(action)
    history.append((thought, action, observation))
```

This loop appears in many guises, but its essence remains constant: observe → think → act → observe again.

---

## **4. The Coordination Layer: Multi-Agent Collaboration**

Whether through text messages as in AutoGen or latent vectors as in LatentMAS, the coordination layer governs how multiple agents interact. Tasks that exceed the capacity of a single agent—scientific discovery, theorem proving, code synthesis—often require distributed expertise. The coordination layer provides the mechanisms for that distribution:

* role assignment (planner, critic, solver, verifier),
* shared memory or latent workspaces,
* iterative negotiation of intermediate representations,
* stable termination conditions.

The most advanced systems in 2025 treat this layer almost as a micro-economy of specialists. Each agent has strengths and weaknesses; the architecture encourages them to collaborate efficiently.

---

## **5. The Learning Layer: Continual Improvement**

This layer closes the loop between deployment and training. It incorporates early-experience learning, agentic RL signals, preference feedback, and trajectory distillation. Every large-scale agent system in production eventually needs this layer, because static behavior quickly erodes in dynamic environments.

The learning layer answers questions like:

* How does the agent adapt when encountering new tools?
* How does it recover from systematic errors?
* How can we safely harvest real-world trajectories?
* How do we prevent reward hacking or degenerate strategies?

This layer is conceptually closest to applied machine learning, but its importance to agents cannot be overstated. Without continual learning, an agent plateaus; with it, agents can improve well beyond what pre-training alone yields.

---

## **6. The Orchestration Layer: Frameworks and Infrastructure**

Finally, at the top of the stack live the developer-facing frameworks: LangGraph, AutoGen, CrewAI, and a proliferation of specialized agentic toolkits. This layer deals with:

* dataflow between agents,
* execution graphs,
* observability and logging,
* error handling,
* and deployment across cloud, edge, or hybrid environments.

The orchestration layer is what transforms research insights into usable software. It hides the complexity of the stack beneath a programmable interface, allowing developers to build agent workflows without re-implementing theoretical constructs from scratch.

---

## **Transition: From Fragmentation to Integration**

By 2025, these layers began to cohere into unified systems. Researchers no longer viewed tools, plans, and collaboration as isolated techniques; they became interdependent components of a comprehensive agent architecture. Pre-trained agentic models informed planning; planning structured tool use; tool use produced experience; experience refined the model; and the cycle repeated. The field matured from a collection of promising tricks into an emerging engineering discipline.

The final task is to understand what all this progress means—and what comes next.

---

# **Part 9 — Synthesis: Where Agents Stand Today and What Comes Next**

We can now look back over the trajectory and see a clear arc. Agents started life as clever prompt loops wrapped around generic LLMs, then graduated into increasingly structured reasoning systems, and finally became models that are trained to act, learn, and collaborate from the start. Each stage built on the last:

* Thought-action loops (ReAct) made it possible for LLMs to touch the world.
* Multi-agent frameworks (AutoGen) showed the power of specialization.
* Agentic continual pre-training baked these behaviors directly into the weights.
* Early-experience learning made agents sensitive to real-world nuance.
* Agentic RL optimized them for long-horizon success.
* Latent collaboration removed the bottleneck of textual communication.
* World models gave them scalable training grounds beyond static web text.
* Scientific and mathematical agents demonstrated the reach of structured agentic workflows.
* The Agent Stack unified these ingredients into a model of how modern agents are built.

Each layer strengthened the others, producing agents that are more robust, more efficient, and more capable of sustained reasoning.

Yet the story is not complete. Several key challenges remain open:

* How far can agent models scale before coordination costs outweigh benefits?
* Can world models accurately represent domains too intricate for direct simulation?
* How can we guarantee safety and alignment in agents that learn autonomously?
* What formal tools will help verify the correctness of agentic systems at scale?
* And perhaps most fundamentally: will the future of agents be dominated by many small specialized models or a few large, deeply agentic ones?

Our current architectures suggest a hybrid world. Foundation agent models will continue growing in depth, while specialized reasoning agents—planners, critics, solvers, verifiers—coordinate on top of them. Frameworks will become more modular and more declarative. And environments—whether browsers, operating systems, laboratories, or world models—will increasingly shape agent capabilities.

If the last three years have taught us anything, it is that the pace of agent evolution accelerates precisely when models stop behaving as isolated predictors and start behaving as participants in structured computational workflows. The next wave of breakthroughs will likely come from refining those workflows, not replacing them.

We have moved beyond the age of single-shot reasoning. We have entered the age of agency.

---

*This blog post synthesizes research from hundreds of papers published between 2022-2025. All papers cited are peer-reviewed or from reputable preprint servers.*

Thanks for reading Petros's Substack! Subscribe for free to receive new posts and support my work.

## **Need help with AI Agents?**

Get my professional servicesatpetroslamb.github.io/peterlamb/