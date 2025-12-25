# The Orchestration Paradigm Series: Dive 1
*Why can't we just prompt models to orchestrate?*

## Introduction

If you've used a frontier language model, you've probably noticed something frustrating. Ask GPT-5 or Claude to solve a complex problem, and they sometimes refuse to try, insisting the task is beyond their capabilities—even when you know they could handle it with a bit of effort. Other times, they confidently attempt problems far too hard for them, producing plausible-sounding but wrong answers. And if you give them access to tools, they often reach for expensive external models when simple calculation would suffice, or try everything themselves when delegation would be smarter.

This isn't a bug that prompting can fix. It's a fundamental limitation of how these models were trained. This dive explains why that limitation exists and why overcoming it requires a fundamentally different approach.

---

## 🌊 Surface Level: The Einstein Problem

Imagine Einstein evaluating PhD candidates. We might expect him to identify the most talented physicists, recognize subtle errors in their reasoning, and provide brilliant feedback. In many ways, he would excel at this. But consider: would Einstein be any less biased toward students who reminded him of his younger self? Would he naturally calibrate against his own blind spots—giving extra credit to experimentalists where he was weak, or recognizing talent in approaches he found philosophically distasteful?

The answer, historically, is no. Even geniuses make biased evaluations. Einstein's famous dismissal of quantum mechanics ("God does not play dice") reflected a systematic underweighting of a paradigm that turned out to be correct. His brilliance at physics did not automatically translate into brilliance at evaluating which kinds of physics to pursue.

This is the fundamental problem that ToolOrchestra addresses. A language model can be extraordinarily capable—the equivalent of Einstein in its domain—while remaining systematically biased in how it allocates that capability. It might be brilliant at solving problems but poor at deciding which problems to solve itself versus delegate. It might know vast amounts but misjudge which tasks require that knowledge versus simple lookup. The capability to do something and the capability to know when to do it are different capabilities.

ToolOrchestra trains the second capability explicitly. Rather than hoping that a capable model will spontaneously develop good orchestration judgment, it trains a smaller model specifically to make orchestration decisions—when to act directly, when to delegate, which tools to use, and how to balance trade-offs. The result is an orchestrator that, despite having less raw capability than the models it coordinates, makes better decisions about capability allocation.

---

## 🏊 Shallow Dive: Two Systematic Biases

The problem manifests as two distinct biases that the ToolOrchestra paper identifies and quantifies.

### Self-Enhancement Bias

When capable models are asked to coordinate tools, they tend to trust themselves too much. They'll attempt problems they should delegate, reason through questions they should look up, and compute answers they should verify with code. This is **self-enhancement bias**: a systematic overweighting of their own capabilities relative to external resources.

The intuition is clear. The model has been trained on billions of examples of generating good responses. Every time it generated a correct answer, that was reinforced. Every time it made a mistake, gradient updates pushed it toward better responses. But the training signal never distinguished between "this answer is good" and "attempting this answer was the right choice." The model learns to generate good outputs without learning meta-cognition about which outputs it should attempt.

Consider a math problem requiring integration by parts. A capable model might reason through the integration, make a sign error three steps in, and produce a confident wrong answer. An orchestrator with self-awareness would recognize: "This is a calculation I could do but might get wrong; let me delegate to a code interpreter for verification." But the model wasn't trained to reason about its own error rates, so it proceeds as if its internal reasoning is reliable.

**The evidence**: Table 6 in the paper shows that baseline models, when given access to tools, still heavily favor self-generated answers over tool outputs. Even when tools would provide better or cheaper solutions, the bias toward self-solving persists.

### Other-Enhancement Bias

The opposite bias also exists. When models do decide to call external tools, they tend to over-rely on the most capable (and expensive) options. They'll call GPT-5 for problems a specialized 7B model could handle. They'll use web search for facts in their own training data. They'll request expensive computation when simple heuristics would suffice. This is **other-enhancement bias**: a systematic overweighting of external capabilities once the model decides not to solve something itself.

This bias has a different origin. During training or alignment, models learn that deferring to authoritative sources is often correct. When unsure, cite the expert. When asked about recent events, search the web. These are generally good heuristics. But they don't come with nuance about cost-effectiveness. The model learns "when uncertain, defer" but not "when uncertain, defer to the minimum sufficient authority."

**The evidence**: Appendix E shows that naive orchestration strategies call expensive models far more often than necessary. GPT-5 is invoked for questions that smaller models answer correctly, incurring costs 10x higher than optimized strategies with no accuracy benefit.

### The Combination Trap

The two biases combine pathologically. A model either over-trusts itself or over-trusts expensive external resources. The middle ground—cheap but effective tools, targeted delegation, efficient verification—requires a kind of meta-cognitive calibration that standard training doesn't provide.

Standard prompting helps marginally. You can instruct models to "use tools when appropriate" or "consider cost-effectiveness." But these instructions don't change the underlying probability distributions that determine behavior. The model might comply superficially while still favoring the same actions. Real change requires changing what's reinforced—which means reinforcement learning with rewards that explicitly capture orchestration quality.

---

## 🤿 Deep Dive: Formalizing the Problem

To make progress, the paper formalizes orchestration as a sequential decision problem. This formalization isn't just mathematical elegance—it enables the application of reinforcement learning techniques that have proven successful in other sequential decision domains.

### The Sequential Decision Frame

An orchestration episode unfolds as follows:

**Turn 0**: The orchestrator receives a task and a set of available tools with their descriptions and costs.

**Turn 1**: The orchestrator chooses an action—either attempt to answer directly, call a tool (search, code execution, another model), or request clarification. If it calls a tool, it observes the tool's response.

**Turn 2**: Given the original task plus the Turn 1 action and observation, the orchestrator chooses the next action. Perhaps it needs to call another tool to verify, or it's ready to produce a final answer, or it needs to synthesize information from multiple sources.

**Turns 3-N**: The process continues until the orchestrator produces a final answer or exceeds a turn limit.

**Reward**: After the episode ends, the trajectory is evaluated. Was the final answer correct? How much did the tool calls cost? How long did the process take? Did it respect user preferences?

This framing makes visible several key aspects:

**State space**: Each state is the full history—the original task, every previous action, and every observation. This is an enormous state space, but language models are trained to handle long contexts.

**Action space**: The set of possible tool calls, parameterized by tool selection and input specification. This is also enormous—essentially any text could be provided per tool call.

**Horizon**: Episodes can span 50+ turns. Long horizons make credit assignment challenging—which early decisions contributed to eventual success or failure?

**Partial observability**: The orchestrator doesn't directly observe correct answers or true difficulty levels. It must infer these from tool responses and self-assessment.

### Why Prompting Cannot Solve This

The sequential decision framing reveals why prompting is inadequate. Prompts can provide initial instructions, but they cannot:

**Adapt to feedback**: A prompt cannot change the model's behavior based on the outcome of Turn 1. If the first tool call fails, the model's subsequent behavior is still determined by the same weights processing the new context.

**Learn from experience**: A prompt cannot improve over thousands of episodes. Each conversation starts fresh.

**Optimize trade-offs**: A prompt can instruct "be cost-effective" but cannot calibrate the precise trade-off between cost and accuracy that maximizes reward in expectation.

**Develop implicit strategies**: The best orchestration strategies may be strategies that no human would think to specify—subtle patterns about when to escalate, how to sequence verification, which failures to retry. Reinforcement learning can discover these; prompting cannot.

The gap is not between good prompts and bad prompts. It's between instruction-following and learning-from-environment-feedback. These are fundamentally different capabilities.

---

## 🔬 Research Depth: Connections to Broader Problems

The orchestration problem connects to several deep questions in AI research.

### Agency Versus Capability

The distinction between "can do X" and "knows when to do X" generalizes beyond orchestration. It's the distinction between capability and agency—between having skills and deploying them wisely.

A model might have the capability to refuse harmful requests but not always recognize which requests are harmful. It might have the capability to admit uncertainty but not always know when uncertainty is appropriate. It might have the capability to ask clarifying questions but not always recognize ambiguity.

ToolOrchestra addresses one instance of this gap: the capability to solve problems versus knowing which problems to solve oneself versus delegate. The broader research program is developing models with genuine agency—models that can evaluate their own capabilities, recognize their limitations, and make wise decisions about how to act.

### Exploration Versus Exploitation

The bias toward self-enhancement can be understood as an exploitation problem: the model exploits its own capabilities rather than exploring whether external tools might be better. Conversely, other-enhancement bias is an exploration problem: the model explores expensive external options rather than exploiting cheaper ones that might suffice.

The exploration-exploitation trade-off is a core challenge in reinforcement learning. ToolOrchestra addresses it implicitly through its diverse training distribution—the model sees many configurations and many outcomes, naturally calibrating when to use what. More explicit solutions (curiosity-driven exploration, uncertainty-aware decision-making) remain future work.

### Weak-to-Strong Generalization

A curious inversion exists between ToolOrchestra and the "weak-to-strong generalization" research program. Weak-to-strong asks: can a weak supervisor train a strong model? ToolOrchestra asks: can a weak model supervise the deployment of strong models?

The answer to both appears to be yes, under the right conditions. A weak teacher can elicit strong capability if the capability already exists and just needs activation. A weak orchestrator can deploy strong capability if it learns when each capability is worth using. In both cases, meta-cognitive skills (what to teach, when to call) are partially orthogonal to object-level skills (solving problems).

This suggests a research agenda: systematically mapping which skills are orthogonal. Can a 1B model orchestrate 100B models? Can a specialized orchestrator for coding learn to orchestrate orchestrators for other domains? The limits of weak-to-strong coordination are not yet known.

### Reflective Cognition

Ultimately, the orchestration problem is a problem of reflective cognition—a system's ability to reason about its own reasoning. Humans do this naturally (though imperfectly): we know when we're confused, when we should look something up, when we're likely to make mistakes.

Language models have limited reflective cognition. They can sometimes express uncertainty ("I'm not sure, but…") but can't reliably calibrate it. They can follow meta-instructions ("verify your answer") but can't spontaneously recognize when verification is needed. They can use tools when prompted but can't assess when tools are worth their cost.

ToolOrchestra improves reflective cognition in one domain—tool use—through reinforcement learning on orchestration outcomes. Whether this approach generalizes to other aspects of reflection remains to be seen. But the principle seems sound: if you want a model to reason about its own reasoning, train it on outcomes of its own reasoning, not just on outputs.

---

## Conclusion

The fundamental problem addressed by ToolOrchestra is not that language models lack capability—frontier models are extraordinarily capable. The problem is that they lack meta-cognitive judgment about when and how to deploy that capability. They trust themselves when they should delegate. They defer to expensive resources when cheap ones would suffice. And no amount of prompting fundamentally changes these biases because prompts cannot adjust the learned probabilities that determine behavior.

Reinforcement learning can. By training on orchestration outcomes—rewarding good coordination and penalizing poor coordination—ToolOrchestra develops an orchestrator with genuine meta-cognitive ability in this domain. It learns when to act, when to delegate, and how to trade off conflicting objectives.

The next dive examines how this reinforcement learning works in practice. What is GRPO, and why is it well-suited to the orchestration problem? The answer involves policy gradients, relative advantage estimation, and a training loop that turns raw model capability into orchestration wisdom.

---

## References

### Coordination and Agency

1. **Self-Enhancement and Biases in AI Systems**
   - The ToolOrchestra paper, Section 4.1
   - https://arxiv.org/abs/2511.21689

2. **Weak-to-Strong Generalization**
   - Burns, C., et al. (2023). "Weak-to-strong Generalization: Eliciting Strong Capabilities With Weak Supervision." *arXiv:2312.09390*
   - https://arxiv.org/abs/2312.09390

3. **Metacognition in Language Models**
   - Kadavath, S., et al. (2022). "Language Models (Mostly) Know What They Know." *arXiv:2207.05221*
   - https://arxiv.org/abs/2207.05221

### Exploration and Exploitation

4. **Exploration-Exploitation Tradeoff**
   - Sutton, R.S., & Barto, A.G. (2018). "Reinforcement Learning: An Introduction." 2nd Edition
   - http://incompleteideas.net/book/the-book-2nd.html

5. **Curiosity-Driven Exploration**
   - Pathak, D., et al. (2017). "Curiosity-driven Exploration by Self-supervised Prediction." *ICML 2017*
   - https://arxiv.org/abs/1705.05363

### Calibration and Uncertainty

6. **Calibration in Language Models**
   - Desai, S., & Durrett, G. (2020). "Calibration of Pre-trained Transformers." *EMNLP 2020*
   - https://arxiv.org/abs/2003.07892

7. **Language Model Cascades**
   - Chen, Y., et al. (2024). "FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance." *arXiv:2305.05176*
   - https://arxiv.org/abs/2305.05176

### Sequential Decision Making

8. **Decision Transformers**
   - Chen, L., et al. (2021). "Decision Transformer: Reinforcement Learning via Sequence Modeling." *NeurIPS 2021*
   - https://arxiv.org/abs/2106.01345

---
