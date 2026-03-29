# Operating Agents V: Trust Boundaries and Agent Safety

*Part of the Operating Agents series, a builder-first run on how modern agent systems actually work once language leaves the prompt and starts acting inside software.*

#### Video TL;DR

[AI Agent Safety Blueprint](./artifacts/video/AI%20Agent%20Safety%20Blueprint.mp4)

## Safety Begins Where The Workflow Touches The World

A chatbot that produces a bad sentence inside a browser tab may be frustrating. An agent that can read email, retrieve a customer record, write a note, and issue a refund belongs to a different class of system. Once the workflow can read, remember, and act, a mistake no longer ends on the screen. It can pass through memory, tool calls, and handoffs until it becomes a state change someone else has to repair. That is why agent safety cannot be taught mainly as a matter of refusal style or abstract alignment language. It has to be taught as architecture.

The central question is therefore not whether the model is "safe" in the abstract. The central question is what a bad input, a bad retrieval, or a bad inference can reach inside the system. That framing follows the broader [foundation-agents survey](https://arxiv.org/abs/2504.01990) and the local [safety blueprint](../../core/practical-chapter-blueprints/06-safety-blueprint.md). The practical focus is trust boundaries: the interfaces that determine how far hostile or mistaken content can travel before a harder control stops it.

![Slide 2: Where control can be taken](./artifacts/slides/Agent%20Safety%20Architecture/slide-002.png)

This way of teaching the topic is useful because it converts a diffuse fear into a design exercise. For each input channel, tool, store, and handoff, ask three things. Is the content trusted, semi-trusted, or untrusted. What action surface can it influence. What hard boundary prevents that influence from reaching a more dangerous part of the system. If those questions do not have concrete answers, the workflow is already depending on soft language where it should depend on structure.

The first interface to inspect is usually the prompt boundary itself. In conventional software, code and data are separate categories. In language-model systems, instructions, retrieved passages, emails, screenshots, and logs all enter as tokens in one context window. That is what makes agent safety distinct from earlier software security patterns. The system does not naturally know that some text should govern behavior while other text should be treated as evidence only.

## Separate Instructions From Untrusted Data

[*Not What You've Signed Up For*](https://arxiv.org/abs/2302.12173) remains one of the most important papers in this area because it established the modern prompt-injection problem in practical terms. The lesson is simple but severe: untrusted content does not remain passive just because the developer intended it to be passive. If the architecture places hostile or semi-trusted data in the same reasoning stream as the system's operating instructions, the model may start following that content as if it were part of the control plane.

![Slide 4: The poisoned context window](./artifacts/slides/Agent%20Safety%20Architecture/slide-004.png)

This matters even more once an agent has tools. A malicious email, PDF, webpage, or customer note no longer needs to manipulate a human reader. It only needs to redirect the model's next decision or next tool call. [*InjecAgent*](https://arxiv.org/abs/2403.02691) is useful because it evaluates that threat in tool-integrated settings, where hidden instructions can influence action rather than just language. In a course context, the paper helps the reader see that indirect prompt injection is not a curiosity. It is a systems problem created by mixing trust classes inside the same control loop.

The practical methodology here begins with trust labeling. Every source of content should be assigned a trust class before it enters the workflow. System instructions and approved internal policies are one class. Retrieved business records may be another. Customer messages, web content, and uploaded files are usually another again. Once those classes are defined, the architecture can decide what each class is allowed to influence. Untrusted data may be summarized, filtered, or quoted as evidence, but it should not be allowed to rewrite policy, override control logic, or directly trigger privileged actions.

That does not mean soft prompts are useless. They can help shape behavior, but they should not be treated as boundaries. A suffix such as "ignore malicious content" is still just more text inside the same stream. It competes with recency, salience, and the immediate phrasing of the hostile input. The safer design move is to keep the categories apart as much as the architecture allows instead of asking the model to preserve the distinction by interpretation alone.

A simple customer-support example makes the point concrete. Suppose an incoming email asks for a refund and includes a hidden instruction telling the model to skip approval because the customer is "pre-cleared." If the workflow allows raw email text to sit beside system instructions and policy rules as one undifferentiated input, the model is being asked to preserve the trust boundary by interpretation alone. A safer system keeps the email in an explicitly untrusted channel, extracts the customer request as data, and requires the approval rule to come from a trusted policy surface instead.

## Tools, Memory, And Other Agents Expand The Risk

Once the prompt boundary is understood, the next interface is the tool boundary. This is the point where a bad inference becomes an external consequence. Least privilege is therefore not a detail. It is the vocabulary of blast radius. If the workflow needs read access, give it read access. If it needs code execution, use a sandbox. If a financial or irreversible action is at stake, approval must happen before execution, not after. The architecture should assume that some bad instructions will make it into the reasoning loop and should therefore ensure that the loop has limited authority.

![Slide 5: From text to side effects](./artifacts/slides/Agent%20Safety%20Architecture/slide-005.png)

[*ToolEmu*](https://arxiv.org/abs/2309.15817) is useful in this section because it shows how to make risky behavior observable before it reaches production. The paper's practical teaching value is that it normalizes sandboxing and emulated testing as part of the build path rather than as a last-minute extra. If an agent can write code, invoke tools, or perform external actions, then the team should expect to learn about risky trajectories in a contained environment first.

Memory creates another boundary problem. A durable store is not only a capability layer. It is also a place where hostile influence can persist across time. [*AGENT POISON*](https://arxiv.org/abs/2407.12784), [*PoisonedRAG*](https://arxiv.org/abs/2402.07867), [*BadRAG*](https://arxiv.org/abs/2406.00083), and [*Machine Against the RAG*](https://arxiv.org/abs/2406.05870) are helpful as a cluster because they show different versions of the same teaching point: retrieval can be compromised not only by false content but also by blocking, jamming, and strategically placed interference. The safest assumption is that anything written into a store today may later return with authority unless the system actively constrains how memory is admitted, versioned, and retrieved.

![Slide 6: The memory liability](./artifacts/slides/Agent%20Safety%20Architecture/slide-006.png)

The multi-agent case extends the same logic. Extra agents do not create safety if they trust one another blindly. Internal summaries, images, files, and artifacts can all carry contamination forward. [*Agent Smith*](https://arxiv.org/abs/2402.08567) matters because it makes this propagation problem vivid in multimodal settings, but the lesson is broader than the specific attack. In a multi-agent workflow, "internal" does not mean "trusted." A handoff from one agent to another still needs structure, validation, and limits on what the artifact can influence next.

![Slide 7: Inter-agent contamination flow](./artifacts/slides/Agent%20Safety%20Architecture/slide-007.png)

Verification belongs in this section too, but it needs to be taught carefully. [*Chain-of-Verification*](https://arxiv.org/abs/2309.11495) is useful because it lowers the chance that unsupported claims become action or durable memory. But verification is not containment. It does not stop indirect prompt injection or replace access control. Its role is narrower and still important: check whether important claims are warranted before those claims are allowed to move deeper into the workflow.

## A Practical Safety Build Order

The safest way to build an agent is to thicken the walls before widening autonomy. In practical terms that means starting with a boundary map. List the input channels, tools, stores, and agent-to-agent handoffs. Assign trust classes. Assign permission scopes. Mark which actions are reversible, costly, or externally visible. Then place hard controls where consequence begins to rise: sanitization or isolation for untrusted content, least privilege for tools, approval for high-impact actions, admission policy for durable memory, and validation for cross-agent handoffs.

![Slide 14: The control matrix](./artifacts/slides/Agent%20Safety%20Architecture/slide-014.png)

This build order is intentionally sequential. First separate trusted instructions from untrusted or semi-trusted data. Then constrain tool permissions and execution surfaces. Then control what can be written durably and how stale or poisoned content is prevented from regaining authority later. Then harden inter-agent handoffs so that internal movement does not become a blind trust channel. Add verification where unsupported claims can create downstream cost. Only after those controls are in place should the workflow widen its autonomy or increase the number of actions it can take without human approval.

It also helps to separate approval from verification because they answer different questions. Verification asks whether a claim is supported. Approval asks whether the supported action should be allowed to proceed. A refund may be factually justified and still require human approval because it crosses a financial threshold. A deployment note may be accurate and still need policy review before release. Treating verification as a substitute for approval is one of the fastest ways to let a technically correct output create an organizationally unsafe action.

![Slide 15: Evaluating the architecture](./artifacts/slides/Agent%20Safety%20Architecture/slide-015.png)

Evaluation should follow the same map. Run prompt-injection tests across every input class. Simulate retrieval poisoning and jamming. Exercise approval-bypass attempts. Inspect permission scopes for each tool. Replay cross-agent contamination paths. Test whether the system can localize the broken interface when something goes wrong. A safety review that only checks the final answer is too shallow. Safety failures travel through the architecture, so the tests have to do the same.

Several anti-patterns become obvious once the method is stated clearly. Mixing instructions and retrieved data in one prompt creates a direct trust collision. Giving an agent broad permissions because "it usually behaves" turns soft language into a substitute for access control. Letting agents write into stores they later trust creates a self-poisoning path. Using a reviewer agent as the main safety control mistakes more language for stronger containment. Relying on monitoring alone means the workflow is discovering its safety failures only after consequence has already happened.

The course-level conclusion is not that agents are uniquely dangerous or impossible to secure. It is that they need the same seriousness we apply to any system that can read untrusted input and perform meaningful side effects. Safety becomes much more concrete when phrased as a boundary question: what can this input reach, what can this node write, and what exactly stops influence from crossing into a more powerful layer. Once that question is answered rigorously, the architecture becomes easier to trust because the trust is attached to walls rather than to optimism.

![Slide 18: Agent safety is architecture](./artifacts/slides/Agent%20Safety%20Architecture/slide-018.png)

For the wider threat taxonomies, contamination paths, retrieval and memory risks, and the deeper literature around safety architecture, continue with the [Safety Companion](./companion.md).

## References

[Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to Evolutionary, Collaborative, and Safe Systems](../../advances-and-challenges-in-foundation-agents.md) ([arXiv](https://arxiv.org/abs/2504.01990)) is the broad survey behind this series. It is useful here because it places safety after the rest of the stack becomes real, which is exactly when the topic stops being abstract and becomes a question of operational consequence.

[Safety blueprint](../../core/practical-chapter-blueprints/06-safety-blueprint.md) is the practical design reference for this chapter. It translates the safety literature into boundary categories, control surfaces, and a conservative deployment order that builders can apply directly during architecture review.

[*Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*](https://arxiv.org/abs/2302.12173) is essential reading for the instruction-versus-data problem. It teaches why untrusted content can become a control channel inside an LLM workflow.

[*InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents*](https://arxiv.org/abs/2403.02691) extends that lesson into tool-using systems. Read it to understand how hidden instructions can redirect actions once the model has access to external interfaces.

[*Identifying the Risks of LM Agents with an LM-Emulated Sandbox*](https://arxiv.org/abs/2309.15817) is the best reference in this chapter for containment-first testing. Its value is practical: it shows how to expose risky tool behavior before it reaches a live environment.

[*AGENT POISON: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases*](https://arxiv.org/abs/2407.12784), [*PoisonedRAG*](https://arxiv.org/abs/2402.07867), [*BadRAG*](https://arxiv.org/abs/2406.00083), and [*Machine Against the RAG*](https://arxiv.org/abs/2406.05870) belong together because they teach the reader how retrieval can fail as a security layer. Their shared lesson is that memory and grounding stores are also attack surfaces.

[*Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast*](https://arxiv.org/abs/2402.08567) is useful for understanding contamination across agents and modalities. Its core value in this chapter is the reminder that internal propagation paths deserve the same scrutiny as external ones.

[*Chain-of-Verification Reduces Hallucination in Large Language Models*](https://arxiv.org/abs/2309.11495) matters here as a verification reference. Read it to understand how factual checking can reduce the chance that unsupported claims become action, memory, or downstream instruction, while remembering that verification is only one layer in a broader safety architecture.
