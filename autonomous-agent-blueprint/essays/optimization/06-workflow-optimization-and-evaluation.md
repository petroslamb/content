# Operating Agents Bonus: Workflow Optimization and Evaluation

*Part of the Operating Agents series, a builder-first run on how modern agent systems actually work once language leaves the prompt and starts acting inside software.*

#### Video TL;DR

[Optimizing AI Agents](./artifacts/video/Optimizing%20AI%20Agents.mp4)

## Once The Agent Works, The Workflow Becomes The Object

The first working agent is often where teams begin to lose discipline. The system performs well enough to feel magical, so improvement starts happening through scattered local edits: a prompt line is added after one bad result, a tool description is rewritten after a second, a retry loop appears after a third. A month later the workflow is more expensive and harder to debug, yet nobody can say which changes genuinely improved it. That is the reason optimization deserves its own chapter. Once an agent becomes a multi-step workflow, the unit that needs to be improved is no longer just the prompt. It is the workflow itself.

That shift sounds obvious once stated plainly, but it is easy to miss because most teams first learned to work with language models through chat interfaces. The prompt is the most visible control surface, so it becomes the default place to intervene. In a production agent, however, the prompt is only one surface among several. Retrieval, schemas, routing, tool definitions, approval logic, feedback loops, and even the graph structure of the workflow all influence the result. That is the optimization distillation taken here from the broader [foundation-agents survey](https://arxiv.org/abs/2504.01990) and the local [optimization blueprint](../../core/practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md). The practical lesson is that the workflow as a whole, rather than one prompt in isolation, is the object under improvement.

![Slide 2: The target has shifted](./artifacts/slides/Agentic%20Optimization%20Blueprint/slide-002.png)

One useful teaching move is to name the main improvement surfaces explicitly. A workflow can improve because a node prompt becomes clearer. It can improve because the topology changes. It can improve because a tool description or output contract becomes stricter. It can improve because a feedback loop corrects recurring failure. The value of this separation is that it gives error a place to land. Without it, every miss is treated as "prompt weakness," which is a very inefficient way to diagnose a graph-shaped system.

![Slide 3: Where to apply optimization pressure](./artifacts/slides/Agentic%20Optimization%20Blueprint/slide-003.png)

This also explains why workflow optimization belongs next to evaluation. A change is only an optimization if the team can show, against a stable objective, that the workflow became better in some defined way. Otherwise the system is only changing. The difference between those two states is where most real production drift begins.

One way to make this concrete is to think in node and edge terms. A classification node may be accurate enough in isolation but still damage the workflow because it emits an inconsistent schema that breaks the extraction node downstream. A retrieval step may look harmless until it increases latency enough that the approval queue misses its service objective. Optimization becomes clearer once the reader stops asking whether one step looks smarter and starts asking how a change alters the behavior of the whole graph.

## What The Main Research Threads Actually Teach

The optimization literature becomes more useful when read by improvement surface instead of by trend. [*OPRO*](https://arxiv.org/abs/2309.03409) is the clearest example for prompt-level search. It matters because it treats prompt editing as an optimization loop against an objective rather than as intuition. In practice, the paper teaches one important precondition: prompt search only makes sense once the objective is stable enough that "better" has a concrete meaning.

[*TextGrad*](https://arxiv.org/abs/2406.07496) extends that idea by turning textual critique into directional feedback that can affect earlier nodes in a workflow rather than only the final answer. The paper is useful because it helps readers see that optimization need not stop at a single prompt. If the workflow is a graph, then the feedback signal may need to travel across that graph in a structured way.

![Slide 4: The research landscape](./artifacts/slides/Agentic%20Optimization%20Blueprint/slide-004.png)

The lighter self-improvement family should be read a little differently. [*Self-Refine*](https://arxiv.org/abs/2303.17651) addresses local repair within one run. [*Reflexion*](https://arxiv.org/abs/2303.11366) addresses lessons that should persist across runs. [*Voyager*](https://arxiv.org/abs/2305.16291) goes a step farther by compiling repeated success into reusable skills. These papers are valuable not because they justify adding feedback everywhere, but because they help the reader classify what kind of improvement is being attempted. Is the workflow fixing a single output, learning from repeated failure, or promoting a stable behavior into a reusable capability.

The topology-search papers sit at the far end of the escalation path. [*AFLOW*](https://arxiv.org/abs/2410.10762) and [*GPTSwarm*](https://arxiv.org/abs/2402.16823) matter because they treat the workflow graph itself as something that can be searched or optimized: nodes can be inserted, edges rerouted, communication patterns altered. These are valuable ideas, but they are easy to romanticize. In practice, topology search is only as good as the objective and the baseline instrumentation around it. If the current workflow is noisy, the search process can produce a complicated graph that faithfully optimizes around noise.

![Slide 6: Escalation triggers](./artifacts/slides/Agentic%20Optimization%20Blueprint/slide-006.png)

Read together, these papers support a simple methodology. Fix local prompt or schema weaknesses first. Add bounded feedback loops when the workflow keeps making the same kind of recoverable mistake. Preserve lessons when recurrence appears across runs. Search topology only when simpler surfaces have been cleaned up and the remaining weakness is genuinely architectural. That reading order matters because it keeps optimization tied to diagnosis rather than ambition.

It also helps the reader assign each paper to a concrete engineering use. OPRO is for prompt search under a real objective. TextGrad is for propagating critique across a workflow. Self-Refine is for local repair. Reflexion is for carrying lessons across attempts. Voyager is for promoting repeated success into a reusable routine. AFLOW and GPTSwarm are for cases where the graph itself may be wrong. Once the methods are organized that way, the literature feels much less like a list of fashionable names and much more like a toolbox with different cost profiles.

## Measurement Before Improvement

The most important optimization rule is that measurement comes before modification. Without a stable evaluation set and a clear scorecard, improvement work turns into drift. One case gets better, another quietly gets worse, and the team keeps moving because the system feels more tuned than it did yesterday. That feeling is not enough. A workflow can become busier, longer, or more elaborate while getting less reliable in the aggregate.

![Slide 8: Instrumentation over intuition](./artifacts/slides/Agentic%20Optimization%20Blueprint/slide-008.png)

This is why the build order begins with instrumentation. Freeze an evaluation set that covers the important task patterns and failure modes. Measure the baseline across task quality, latency, cost, tool-call accuracy, retrieval quality, stability, and regression rate. Only then decide where the next improvement attempt should land. This order is intentionally conservative because it protects the team from optimizing the wrong thing or from treating anecdotal wins as system-wide progress.

The next design move is to fix the cheapest surfaces first. Many workflow problems do not require another model call at all. A stricter schema can eliminate parsing failures. A better tool description can reduce argument mistakes. A cleaner stop condition can remove loops. A clearer retrieval filter can prevent irrelevant context from reaching later nodes. These changes are often more valuable than new reflective layers because they remove ambiguity the model should not have been forced to resolve in the first place.

That priority order is easy to underestimate because cheap fixes rarely make dramatic demos. Yet they often have the highest return. If a downstream parser keeps failing, a schema fix is usually better than another reflective critique pass. If a node keeps looping because it lacks a clear terminal condition, no amount of prompt flourish is as useful as an explicit stop rule. Good optimization work often looks ordinary because it reduces uncertainty rather than adding new behavior.

![Slide 7: The recommended build order](./artifacts/slides/Agentic%20Optimization%20Blueprint/slide-007.png)

Only after those cheap surfaces are reasonably clean should feedback loops enter. A critique pass is useful if it raises quality enough to justify its latency and token cost. A stored lesson is useful if recurrence really drops afterward. A reusable skill is useful if the workflow is repeatedly paying for the same successful reasoning path. The broader lesson is that feedback is not valuable because it sounds adaptive. It is valuable when the system can show that the extra loop improved the measured objective.

LLM judges deserve special care here. Judge models can be excellent for scaling evaluation across open-ended outputs, and [*MT-Bench and Chatbot Arena*](https://arxiv.org/abs/2306.05685) is a useful reference for understanding that evaluation turn. But judges also have biases toward verbosity, ordering, style, and presentation. A workflow can therefore learn to please the judge without becoming meaningfully better for the user. That is why judge-based evaluation should be calibrated against human spot checks rather than treated as a self-authenticating source of truth.

## Bounded Self-Improvement

Optimization becomes riskier when the system is allowed to change itself. The main question is not whether self-improvement is possible. It is which surfaces the optimizer is allowed to touch. There is a major difference between letting a workflow propose a better extraction prompt and letting it rewrite approval policy, broaden its own permissions, or alter the evaluation set. One kind of self-improvement is a controlled engineering loop. The other collapses governance into the object being optimized.

![Slide 5: Method comparison matrix](./artifacts/slides/Agentic%20Optimization%20Blueprint/slide-005.png)

The safest rule here is that the optimizer should not control the evaluation that decides whether it succeeded. If the system can influence both the work and the measure of the work, it may discover that lowering the standard is easier than improving the workflow. This is the same reason Goodhart-like failure appears so often in optimization settings. Push one metric too hard and the workflow may damage another objective that was not held strongly enough in view. Chase judge scores too aggressively and the system may optimize for style. Chase cost too aggressively and reliability can erode first on the edge cases that matter most.

The safe methodology is therefore bounded. Keep the evaluation set and governance rules outside the optimizer's reach. Limit self-modification to clearly named surfaces such as prompts, schemas, local routing policies, or reusable skills inside a controlled environment. Require regression checks before changes are promoted. Use human review for changes that affect approval logic, permissions, policy interpretation, or other governance surfaces. Optimization remains useful precisely because it is not allowed to redefine the standard by which usefulness is judged.

![Slide 9: The pragmatic standard](./artifacts/slides/Agentic%20Optimization%20Blueprint/slide-009.png)

The course-level takeaway is deliberately plain. Optimize an agent workflow the way you would optimize any other distributed production system. Lock the objective. Measure the baseline honestly. Repair contracts before adding new reasoning layers. Add feedback where repeated failure proves it is worth the cost. Search topology only when simpler causes have been ruled out. Keep the optimizer away from the governance layer. That discipline is less exciting than endless prompt folklore, but it is the discipline that prevents a system from becoming more complicated while only appearing to become better.

## References

[Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to Evolutionary, Collaborative, and Safe Systems](../../advances-and-challenges-in-foundation-agents.md) ([arXiv](https://arxiv.org/abs/2504.01990)) is the broad survey behind this series. It is useful here because it places optimization after the rest of the stack already exists, which is exactly when improvement becomes a workflow problem rather than a prompting hobby.

[Optimization and Self-Improvement blueprint](../../core/practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md) is the practical reference for this chapter. It turns the topic into a usable build order: freeze evaluation, instrument broadly, fix cheap surfaces first, add bounded feedback second, and treat topology search as a late escalation.

[*OPRO: Large Language Models as Optimizers*](https://arxiv.org/abs/2309.03409) is the clearest reference for prompt search under a defined objective. Read it when a team needs to stop treating prompt editing as intuition and start treating it as a measurable loop.

[*TextGrad: Automatic "Differentiation" via Text*](https://arxiv.org/abs/2406.07496) matters because it treats critique as a signal that can move across a workflow rather than ending at the final response. It is especially useful when earlier nodes need to be improved based on downstream performance.

[*SELF-REFINE: Iterative Refinement with Self-Feedback*](https://arxiv.org/abs/2303.17651), [*Reflexion: Language Agents with Verbal Reinforcement Learning*](https://arxiv.org/abs/2303.11366), and [*Voyager: An Open-Ended Embodied Agent with Large Language Models*](https://arxiv.org/abs/2305.16291) form a useful learning ladder: local repair, persistent lessons, and compiled skills. Read them together to understand different scopes of bounded self-improvement.

[*Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*](https://arxiv.org/abs/2306.05685) is the key evaluation-method reference in this chapter. It helps the reader understand both the power and the calibration risks of judge-based scoring for open-ended outputs.

[*AFLOW: Automating Agentic Workflow Generation*](https://arxiv.org/abs/2410.10762) and [*GPTSwarm: Language Agents as Optimizable Graphs*](https://arxiv.org/abs/2402.16823) are the right references when the architecture itself may need to change. Their teaching value is partly positive and partly cautionary: topology can be optimized, but only after the objective and the lower-level contracts are already stable enough to support that search.
