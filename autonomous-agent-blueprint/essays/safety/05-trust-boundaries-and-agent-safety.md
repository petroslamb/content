# Operating Agents V: Trust Boundaries and Agent Safety

*Part of the Operating Agents series, a builder-first run on how modern agent systems actually work once language leaves the prompt and starts acting inside software.*

#### Video TL;DR

[AI Agent Safety Blueprint](./artifacts/video/AI%20Agent%20Safety%20Blueprint.mp4)

The easiest way to misread agent safety is to make it a prompt problem. A model should be careful. A policy string should be stronger. A refusal clause should be more explicit. The transcript for this chapter starts somewhere much less flattering. Once an agent can read, remember, and act, the practical question is where control can be taken. Not in theory. In the workflow. Through untrusted content, unsafe tools, poisoned retrieval, over-broad permissions, weak approval boundaries, and cross-agent handoffs. That is the safety claim carried here from the broader [foundation-agents survey](https://arxiv.org/abs/2504.01990), tightened in the local [safety blueprint](../../core/practical-chapter-blueprints/06-safety-blueprint.md), and rebuilt from the transcript's interface-by-interface progression.

![Slide 2: Where control can be taken](./artifacts/slides/Agent%20Safety%20Architecture/slide-002.png)

## Safety Starts At The Interfaces

The transcript makes one framing move that matters more than any individual paper it cites. It refuses the old alignment conversation as the main entry point. That does not make alignment irrelevant. It makes it secondary to the practical attack surface a deployed agent actually presents. Useful systems do not live in a clean lab prompt. They read external content, call APIs, write files, query memory, and pass artifacts to other components. The dangerous places are the interfaces where those transitions happen.

![Slide 3: The practical attack surface map](./artifacts/slides/Agent%20Safety%20Architecture/slide-003.png)

That is why the transcript keeps describing the system as a house with doors and windows. Every channel that lets outside data enter or internal action leave becomes part of the threat model. A safety posture that ignores those interfaces and focuses only on the final output tone is not incomplete by a little. It is looking in the wrong place. The workflow does not become dangerous when the model says something alarming. It becomes dangerous when bad influence acquires reach it should never have had.

## Untrusted Content Is Not Passive Data

The first boundary is the one between instructions and data. [*Not What You've Signed Up For*](https://arxiv.org/abs/2302.12173) remains foundational because it made indirect prompt injection concrete. The core problem is architectural, not rhetorical. A language model does not inherit the hard separation between code and data that older software systems enjoyed. System instructions and retrieved text both arrive as tokens in one stream. That means untrusted content can start behaving like instruction if the architecture lets it.

![Slide 4: The poisoned context window](./artifacts/slides/Agent%20Safety%20Architecture/slide-004.png)

The transcript uses the email-summary example because it is brutally clear. A helpful assistant reads a message body that contains a hidden instruction, and the hidden instruction now lives in the same context as the original task. The developer may hope the system prompt has priority. The model may still weight the later content heavily, especially when that content sounds explicit and authoritative. The lesson is not "write a better system prompt." It is "treat external content as fundamentally untrusted by design."

That is where [*InjecAgent*](https://arxiv.org/abs/2403.02691) sharpens the story. Indirect prompt injection stops being a curious prompt hack and becomes a benchmark against real tool-using agents. The issue is no longer whether the model can be tricked into saying something odd. It is whether content arriving through normal workflows can steer actual tool calls. That is the point where language-level confusion becomes an operational security problem.

## Tools Turn Language Into Consequence

The transcript's next move is exactly right. Once tools are attached, prompt injection is no longer the whole story. Tool scope and containment become safety architecture in their own right. [*ToolEmu*](https://arxiv.org/abs/2309.15817) matters here because it gives builders a way to inspect risky tool behavior inside an emulated environment before the workflow is allowed near the real one. That contribution is more practical than it first sounds. It turns "wait and see in production" from a bad instinct into an avoidable design error.

![Slide 5: From text to side effects](./artifacts/slides/Agent%20Safety%20Architecture/slide-005.png)

The transcript keeps the design rule severe. Separate read tools from write tools. Separate low-impact tools from destructive, financial, or legally sensitive ones. Give each agent or workflow stage the smallest authority envelope that still lets it do the job. That is ordinary least privilege translated into agent systems. A summarizer should not quietly hold the same keys as a payment processor. A drafting tool should not also be able to mutate production state.

Approval gates belong in the same architectural layer. Deterministic checks help, but they do not understand the meaning of the action payload. They can tell you whether the amount is under a threshold. They cannot tell you whether the payload was justified, hallucinated, or reputationally ruinous. That is why the transcript insists that irreversible, financially meaningful, legally sensitive, or reputationally expensive actions still need a human approval boundary. The point is not nostalgia for human supervision. It is accountable consequence control.

## Memory And Retrieval Are Liability Surfaces

The middle of the transcript makes another important correction. Retrieval and memory are usually introduced to teams as quality layers. They should also be read as safety layers. [*AGENT POISON*](https://arxiv.org/abs/2407.12784) matters because it makes durable memory look less like a harmless convenience and more like a delayed influence channel. If an attacker or a bad process can get malicious or misleading state written into the store, the store itself becomes part of the attack path.

[*PoisonedRAG*](https://arxiv.org/abs/2402.07867) and [*BadRAG*](https://arxiv.org/abs/2406.00083) sharpen the same lesson from the retrieval side. A very small amount of poisoned content can distort what the system sees, when it sees it, and how much authority that content appears to carry. The field still underrates this because it keeps imagining the corpus as a neutral grounding layer. The transcript does not allow that comfort. Once the workflow acts on retrieved knowledge, the corpus has become an integrity-sensitive part of the control loop.

![Slide 6: The memory liability](./artifacts/slides/Agent%20Safety%20Architecture/slide-006.png)

[*Machine Against the RAG*](https://arxiv.org/abs/2406.05870) pushes the threat further by showing that the danger is not only false content. Retrieval can also be jammed. A blocker document can prevent the system from reaching the right material at the moment it needs it. That matters because availability and coverage failures can be just as damaging as explicit misinformation when the workflow is supposed to catch compliance issues, safety incidents, or critical evidence.

The transcript's response is not exotic. Memory hygiene means versioning, provenance, audits, curation, and the ability to inspect who or what wrote state into the store. A knowledge base cannot be treated as a magical extension of the model. It has to be treated as monitored infrastructure.

## More Agents Can Spread Risk Faster

The transcript becomes most vivid when it reaches multi-agent contamination. [*Agent Smith*](https://arxiv.org/abs/2402.08567) matters because it turns a vague fear into a propagation model. One compromised multimodal artifact can move through agent interactions, summaries, screenshots, or shared files and infect later stages without any second intervention from the attacker. That is a very different mental model from the single compromised chat window.

![Slide 7: Inter-agent contamination flow](./artifacts/slides/Agent%20Safety%20Architecture/slide-007.png)

This is why the chapter's fifth boundary is inter-agent skepticism. Internal messages are not trustworthy merely because they are internal. A screenshot one agent sends to another is still an untrusted artifact. A JSON payload is still just a payload. Structured formats can reduce ambiguity. They do not create trust by themselves. The receiving stage still needs the same trust separation it would apply to outside inputs.

That point matters because the industry keeps reaching for a false comfort here. More voices do not automatically make the system safer. If the roles are sharing contaminated artifacts and inheriting trust from each other by default, the topology amplifies the attack surface instead of reducing it.

## Reliability Controls Sit Inside The Safety Stack

The transcript is also careful about where verification belongs. [*Chain-of-Verification*](https://arxiv.org/abs/2309.11495) does not solve adversarial control of the system. It does something more limited and still very important. It reduces unchecked factual error before that error becomes action, memory, or downstream instruction. That is why it belongs in the safety architecture even though it started as a reliability method.

![Slide 8: Safety failures happen at interfaces](./artifacts/slides/Agent%20Safety%20Architecture/slide-008.png)

The key is placement. Verification belongs before outputs with real consequence. It should not be treated as a decorative suffix or a vague self-check. If a generated summary can trigger a refund, publish to a client-facing portal, or contaminate a later decision, the workflow needs a real stage where claims are checked against source material before consequence arrives.

This does not make debate between agents a substitute for containment. The transcript is direct on that as well. A debate loop between two equally exposed models cannot replace hard access boundaries, tool restrictions, or approval gates. Logic is too soft a final line of defense when the system can still physically take the wrong action.

## The Blueprint Is Six Walls, Not One Filter

The transcript's synthesis section is the chapter's real payoff. Safety is an interface architecture. Failures happen between instructions and data, between model and tool, between retrieval and memory, between one agent and another, and between output and irreversible action. That is why the blueprint resolves into six boundaries rather than one magic safety classifier: trust separation, tool containment, action approval, memory hygiene, inter-agent skepticism, and verification.

![Slide 14: The control matrix](./artifacts/slides/Agent%20Safety%20Architecture/slide-014.png)

The suggested build order is severe in exactly the right way. Define trust classes for every input channel. Separate read, write, and destructive tools by policy. Add approval gates for high-impact actions. Curate and monitor retrieval and memory. Add verification loops for important outputs. Then red-team the whole workflow before widening autonomy. The order is conservative because the field is still getting hurt by preventable boundary failures long before it reaches the speculative frontier of self-healing or self-governing agents.

The evaluation section follows naturally from that architecture. Injection resistance tests, tool-abuse drills, retrieval poisoning simulations, cross-agent contamination exercises, permission reviews, approval-bypass tests, and incident replay are not side exercises. They are how the team learns whether the boundaries actually exist outside the design document.

![Slide 15: Evaluating the architecture](./artifacts/slides/Agent%20Safety%20Architecture/slide-015.png)

The anti-patterns are therefore easy to name. Mixing instructions and retrieved content into one undifferentiated prompt. Treating safety as a suffix prompt. Letting agents write into stores they later trust without control. Using debate as a stand-in for access control. Relying on post hoc monitoring where active containment was required. None of these are subtle design failures. They are ways of refusing to build the wall until after the breach.

![Slide 17: Architectural anti-patterns](./artifacts/slides/Agent%20Safety%20Architecture/slide-017.png)

The closing move in the transcript is the one worth preserving. Greater autonomy does not mean thinner walls. It means thicker ones. The more seamlessly these systems can move through real environments, the more carefully their permissions, trust classes, memory writes, and handoffs have to be bounded. Without those walls, autonomy is not a feature. It is just an unpriced liability.

![Slide 18: Agent safety is architecture](./artifacts/slides/Agent%20Safety%20Architecture/slide-018.png)

## References

[Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to Evolutionary, Collaborative, and Safe Systems](../../advances-and-challenges-in-foundation-agents.md) ([arXiv](https://arxiv.org/abs/2504.01990)) is the source booklet from which this chapter was ultimately distilled. Its key contribution is scope. It places safety after action, memory, reasoning, and coordination, which is exactly where it belongs if the goal is to understand what the earlier capabilities make dangerous once they are combined.

[Safety blueprint](../../core/practical-chapter-blueprints/06-safety-blueprint.md) is the builder-facing backbone for this chapter. Its key contribution is the interface model. It turns a broad safety literature into six concrete boundary types and a conservative deployment order.

[The Architecture of AI Agent Safety transcript](./artifacts/transcript_The%20Architecture%20of%20AI%20Agent%20Safety_full.txt) is the direct structural source behind this draft. Its key contribution is progression. It moves from indirect prompt injection to tool containment, memory liability, inter-agent contamination, verification, and finally the claim that the real safety layer is the interface architecture itself.

[*Not What You've Signed Up For*](https://arxiv.org/abs/2302.12173) matters because it established indirect prompt injection as a practical attack against real integrated systems. Its key contribution is the trust-boundary insight that external content cannot be treated as though it were merely passive data once the model is reading it alongside its instructions.

[*InjecAgent*](https://arxiv.org/abs/2403.02691) matters because it brought indirect prompt injection into tool-integrated evaluation. Its key contribution is operationalizing the attack against agents that can actually do things, not just say things.

[*ToolEmu*](https://arxiv.org/abs/2309.15817) matters because it gives teams a practical sandbox-first safety evaluation pattern. Its key contribution is letting risky tool behavior surface before the workflow is trusted in the real environment.

[*AGENT POISON*](https://arxiv.org/abs/2407.12784) matters because it shows that memory and knowledge stores are attack surfaces, not just capability layers. Its key contribution is turning durable state into an explicit part of the threat model.

[*PoisonedRAG*](https://arxiv.org/abs/2402.07867) matters because it demonstrated how a small amount of malicious content can distort retrieval and downstream behavior. Its key contribution is making knowledge corruption measurable rather than hypothetical.

[*BadRAG*](https://arxiv.org/abs/2406.00083) matters because it reinforces the same lesson from a different angle. Its key contribution is showing how retrieval corpora themselves become a practical vulnerability surface rather than a neutral grounding layer.

[*Machine Against the RAG*](https://arxiv.org/abs/2406.05870) matters because it expands the threat model beyond false facts. Its key contribution is the blocker-document idea, which shows that retrieval availability can be attacked even when the attacker is not directly poisoning the answer content.

[*Agent Smith*](https://arxiv.org/abs/2402.08567) matters because it makes inter-agent contamination concrete. Its key contribution is showing how one adversarial multimodal artifact can propagate across agent populations through routine collaboration.

[*Chain-of-Verification*](https://arxiv.org/abs/2309.11495) matters in this chapter because it places factual checking before consequence. Its key contribution is not full containment. It is making unchecked hallucination less likely to become action, memory, or propagated state.
