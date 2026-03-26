# Safety Companion

The public safety essay stayed on one line because it had to: safety is interface architecture. That is still the right public claim. It cuts past soft language about alignment and points at the places real systems break. But the safety chapters are broader than that line. They are a survey of how capable systems fail once they begin reading, remembering, and acting in the world. This companion is the place for that wider terrain.

What makes these chapters strong is not that they invent a new moral vocabulary. It is that they describe practical points of takeover and failure. A model that looks harmless in a chat box becomes a different kind of system once it reads web pages, stores durable state, executes code, triggers workflows, or accepts artifacts from other agents. The moment those surfaces come online, the safety question moves from "what might the model say?" to "what happens at each boundary where data, authority, and action meet?"

## Safety Gets Real At The Boundary, Not In The Prompt

The single most useful doctrine in this chapter cluster is that safety failures happen at interfaces.

They happen between instructions and untrusted content. They happen between the model and its tools. They happen between retrieval and memory. They happen between one agent and another. They happen between an output and an irreversible action.

That matters because it rules out a lot of shallow comfort. A safety prompt cannot solve a broken trust boundary. A classifier cannot substitute for least privilege. A post hoc monitor cannot undo a reckless action surface. The practical story of these chapters is that the system has to be partitioned correctly before it can be trusted.

## The Threat Model Is Broader Than Prompt Injection

Indirect prompt injection is the best-known entry point into the chapter, and rightly so. It forces a hard design realization: external content can contain instructions that try to steer the system, and those instructions can arrive through retrieval, browsing, documents, or messages without ever appearing in the privileged prompt.

But the chapter is wider than prompt injection. It also covers unsafe tool use, excessive permissions, supply-chain and environment risk, poisoned corpora, contaminated memory, and inter-agent artifact transfer. Once the system can read, remember, and act, any one of those layers can become the weak link.

This is why the chapter is better read as a map of attack surfaces than as a list of scary examples. The examples matter because they reveal what kind of boundary has to exist. The design lesson is more important than the novelty of the exploit.

## Retrieval And Memory Are Part Of The Security Perimeter

The essay touched this, but the broader chapter deserves to say it more bluntly: retrieval systems and memory stores are security infrastructure. They are not only relevance infrastructure.

If a corpus can be poisoned, jammed, or allowed to drift silently, then the grounding layer itself becomes a way to redirect behavior. If long-term memory can accept arbitrary writes and later be trusted during action, then state persistence becomes an attack vector.

That is why memory hygiene and retrieval curation belong in the default safety stack. Versioning, provenance, anomaly checks, and controlled ingestion are not optional extras once the system depends on stored knowledge to decide what to do.

## Reliability Becomes Safety Once Outputs Matter

Another strength of the broader chapter cluster is that it helps explain why reasoning controls show up again in a safety conversation. Hallucination is not only a quality problem. It becomes a safety problem the moment a false answer triggers a side effect, a decision, or a contaminated downstream state.

This is why Chain-of-Verification belongs here as well as in the reasoning chapter. Verification is not a complete defense against hostile input. But it is one of the simplest ways to reduce the number of unchecked errors that escape into real systems. The larger lesson is that safety and reliability start to overlap once output has consequences.

## The Threat Model Does Not End With Text

The chapter also widens the threat model beyond words. Agent Smith matters because it shows that screenshots, images, and other multimodal artifacts can become propagation channels across agent populations. That is not a side case. It is a warning about what happens once agents exchange files and observations across trust boundaries.

The same logic applies to dependencies and external execution environments. If the system depends on tools, packages, browser content, remote services, or outputs from other models, then the environment itself is part of the attack surface. That is why architectural safety has to include what surrounds the model, not just what the model says.

## What A Serious Safety Posture Looks Like

The chapter's practical posture is deliberately conservative. Label trust classes. Separate instructions from observations. Split read tools from write tools and high-impact tools from low-impact ones. Sandbox side effects. Require deterministic checks and human approval for irreversible actions. Curate retrieval inputs. Monitor memory writes. Treat inter-agent handoffs as untrusted until proven otherwise.

That is not glamorous, and it is exactly why it is useful. Most meaningful safety gains in current agent systems still come from containment, permission discipline, and reviewable boundaries rather than from speculative self-healing layers.

The same conservatism should extend to incident handling. A safe system is not only one with prevention layers. It is one where failures can be replayed, root-caused, and contained. Logs, typed handoffs, versioned memory, and explicit approval events are part of the safety architecture because they make accountability possible after something goes wrong.

## Resources And References

### [Safety Essay: Operating Agents V: The Attack Surface You Built](../safety/05-safety-v5.md)

Read the essay first for the narrow public claim. It keeps the focus on interface architecture, which is still the right practical frame for most deployment discussions.

Use this companion when you want the larger threat map around that claim, especially the links between prompt injection, tool risk, retrieval poisoning, memory hygiene, and multimodal contamination.

### [Builder Blueprint: Safety](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/core/practical-chapter-blueprints/06-safety-blueprint.md)

The blueprint is the operator-facing summary of the safety chapters. It turns the literature into a layered control stack: trust classes, tool containment, approval gates, memory hygiene, inter-agent skepticism, and evaluation.

It is the best file to read when you need design choices and build order rather than the broader public explanation.

### [Foundation Agents: Practical Chapters Guide](https://github.com/petroslamb/content/blob/main/autonomous-agent-blueprint/reference/chapters-guide.md)

The guide is the booklet-scale interpretation. It keeps the focus on the three production risks most teams still underestimate: indirect injection through external content, unsafe tool use, and poisoned retrieval or memory.

It is also the clearest place to see how safety moves from secondary concern to central architecture issue as soon as the rest of the capability stack becomes real.

### [Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) (2023)

This is the foundational trust-boundary paper for modern agent safety. Its enduring contribution is not merely naming indirect prompt injection. It shows that hostile instructions can hide inside retrieved or external content and steer the system without ever appearing in the privileged prompt.

That changes how content should be treated. The practical lesson is severe and durable: external text must stay data, not instructions, no matter how naturally it reads.

### [InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents](https://arxiv.org/abs/2403.02691) (2024)

InjecAgent matters because it operationalizes the injection story against tool-using systems rather than chat-only setups. It makes the risk measurable in the exact kind of environment builders now deploy.

That is why it belongs here. It is not primarily a mitigation paper. It is an evaluation paper that forces the field to stop treating injection as a speculative edge case.

### [Identifying the Risks of LM Agents with an LM-Emulated Sandbox](https://arxiv.org/abs/2309.15817) (2024)

ToolEmu is one of the strongest practical papers in the safety cluster because it shifts attention from exhortation to testing. Instead of waiting for incidents, it argues for emulated tool environments where risky behavior can be surfaced before deployment.

That is a major architectural lesson. If an agent can take meaningful actions, the environment used to test those actions is itself part of the safety design.

### [AGENT POISON: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases](https://arxiv.org/abs/2407.12784) (2024)

Agent Poison matters because it expands the threat model from prompts to durable state. Memory and knowledge stores are not only capability layers. They are also candidate backdoors.

This is why memory hygiene belongs so centrally in the chapter. Once the system writes and later trusts long-term state, the store itself needs curation, versioning, and inspection.

### [PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models](https://arxiv.org/abs/2402.07867) (2024)

PoisonedRAG is one of the clearest demonstrations that retrieval systems create a real knowledge-corruption surface. A small number of malicious documents can materially redirect answers.

Its importance is that it forces builders to stop treating the corpus as a neutral substrate. Once the agent relies on retrieval for reasoning or action, the corpus is part of the security model.

### [BadRAG: Identifying Vulnerabilities in Retrieval Augmented Generation of Large Language Models](https://arxiv.org/abs/2406.00083) (2024)

BadRAG reinforces the same lesson from another angle: even a tiny poisoned fraction can heavily distort retrieval behavior. That makes large knowledge bases look less like passive grounding layers and more like vulnerable infrastructure.

It belongs in the companion because it makes the retrieval-security case harder to dismiss as an exotic corner case.

### [Machine Against the RAG: Jamming Retrieval-Augmented Generation with Blocker Documents](https://arxiv.org/abs/2406.05870) (2025)

Jamming matters because it expands the retrieval threat model beyond falsehood. Retrieval can be degraded or blocked, not only poisoned with misleading content.

That matters in practice because availability is part of safety. A system that cannot retrieve the needed evidence at the right moment can fail just as dangerously as one that retrieves the wrong evidence.

### [Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast](https://arxiv.org/abs/2402.08567) (2024)

Agent Smith is the strongest concrete source for multimodal and inter-agent contamination in this package. Its key contribution is to show how one adversarial image can propagate across agents through memory and message exchange.

That widens the trust model beyond text. In multi-agent and computer-use systems, screenshots, image attachments, and visual artifacts need the same distrust that safety-conscious builders already apply to outside text.

### [Chain-of-Verification Reduces Hallucination in Large Language Models](https://arxiv.org/abs/2309.11495) (2023)

CoVe appears here because factual reliability becomes a safety issue once wrong claims can trigger external effects or contaminate downstream state. It is not a full defense against hostile inputs, but it is one of the cleanest ways to reduce unchecked output error.

That is why the chapter treats verification as a boundary-supporting control rather than a separate reasoning nicety. Once outputs matter, reliability feeds directly into safety.
