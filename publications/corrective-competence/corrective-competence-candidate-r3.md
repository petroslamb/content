# Corrective Competence

The revealing moment came after the assistant disappeared.

In a set of randomized trials, people spent roughly ten minutes using AI help on fraction problems and reading-comprehension questions. While the assistant was available, the bargain looked good. Once it was removed, the same people solved fewer problems and gave up more often. The system had not failed in the usual sense. It had helped. The failure appeared in the residue it left behind.

That is the part of AI collaboration we still do not measure well. We know how to ask whether a system raises output, whether users trust it too much, whether the interface should expose uncertainty, whether the recommendation is accurate enough to deserve reliance. Those questions are useful, but they inspect the answer surface. The harder issue is whether the workflow preserves corrective competence: the human ability to notice, contest, and repair what has gone wrong once assistance becomes normal.

Corrective competence hides inside success. When the model answers quickly, the draft gets produced, the diagnosis gets nudged in the right direction, or the code compiles on the first pass, the interaction looks productive. Productivity is a poor proxy for oversight. A workflow can raise assisted performance while weakening the person who is still supposed to supervise it.

The cross-domain claim has to stay narrow. These papers do not prove one universal law that applies identically to students, junior developers, radiologists, pathologists, and safety engineers. What they support is more specific. Once AI becomes the first generator of candidate moves and the human shifts toward reacting to machine proposals, the maintenance competence required to detect and correct errors starts to decay faster than output quality improves. The exact symptoms differ by domain. The underlying asymmetry is stable: assistance strengthens generation before it strengthens correction.

The persistence study matters because it shows how quickly that asymmetry can appear. A short exposure to an always-helpful assistant was enough to reduce later unassisted performance and make people skip more often. Persistence matters because it sits upstream of learning. A person who stops working through the problem no longer gets the repetitions that build judgment. They do not just know less. They stop exercising the very capacity that later oversight will need.

The skill-formation evidence makes the same point with a more explicit mechanism. In a study of developers learning a new asynchronous Python library, AI assistance reduced conceptual understanding, code reading, and debugging performance. The important distinction was not simply AI versus no AI. It was interaction pattern. The strongest patterns preserved learning by forcing the user to stay cognitively engaged, ask for explanations, and work with concepts rather than simply accept generated code. The weakest patterns treated the model like a contractor and the human like a reviewer of finished work. That is the exact handoff where corrective competence begins to erode.

The pedagogical version of that erosion has been described as epistemic debt. In a study of novice programmers, unrestricted AI assistance and scaffolded AI produced similar short-term productivity, but they diverged sharply once the system was removed. In the subsequent maintenance task, the unrestricted condition collapsed far more often. The lesson is not that friction is inherently good. It is that some kinds of friction are carrying competence-preserving load. If the workflow removes every point where the person has to reconstruct, explain, or debug the reasoning, it borrows against the correction capacity that will be needed later.

This is what makes corrective competence the right public term. The question is not whether users retain abstract understanding in some educational sense. The question is whether they retain enough maintenance competence to intervene well when the system is partly right, impressively wrong, or wrong in a way that conceals its own error. The safety-engineering literature sharpens that point. The competence shadow is not just a metaphor for overreliance. It is a structural claim about compounding loss. Once AI narrows the set of hazards, scenarios, or mitigations that get considered, downstream human review only inspects what survived that narrowing. The omission compounds. The human is not correcting the whole problem space anymore. They are correcting within a machine-pruned one.

That formal move matters because it explains why the damage can exceed the visible error rate. If the system proposes the initial search space, the human evaluates that reduced space, and later review checks the outputs of that already-reduced process, the losses are not additive. They stack. What disappears early cannot be recovered by careful inspection later because it never reaches inspection. That is the strongest contribution of the competence-shadow paper. It turns a vague fear about oversight erosion into a workflow argument about where correction power gets removed.

The best rival frame is still appropriate reliance. Calibration matters. Under-reliance and over-reliance are both real. In prostate cancer MRI diagnosis, radiologists still under-relied on a stronger AI, and performance feedback did not cleanly solve the problem. In computational pathology, researchers can measure automation bias, anchoring, confirmation effects, and time-pressure amplification. Those findings matter because they show that reliance failure does not have one direction. The reason they do not dislodge the deeper frame is that they still operate at the behavioral surface. They tell us that people weight machine advice badly. Corrective competence asks what capacity remains available to weight it well in the first place.

That distinction becomes clearer when the system is designed differently. Evaluative AI proposes hypothesis-driven decision support that offers evidence for or against a candidate judgment instead of simply issuing a recommendation. This is not a cosmetic interface choice. Recommendation-driven systems organize the human around reacting to the machine's answer. Hypothesis-driven systems preserve more of the structure that correction actually needs: comparison across alternatives, visibility into reasons, and room to reject the machine without leaving the task entirely.

This should change what counts as readiness. A model that improves the next answer while weakening the next act of correction is not simply helpful. It is spending the operator. It turns the person in the loop into a place where responsibility lands after the real search has already happened somewhere else.

That is the dangerous version of delegation. The human remains visible in the process, but the competence that made the human meaningful has been thinned out beforehand. The signature is not dramatic collapse. It is a quieter substitution: generation moves to the machine, correction becomes a reaction to machine-shaped possibilities, and supervision survives as ritual after it has weakened as an ability.

So the evaluation standard has to move. Not every domain needs the same safeguards, and not every task demands a full independent first pass. High-consequence workflows need some preserved capacity to generate alternatives, inspect evidence, challenge outputs, and reconstruct the reasoning when the model is absent or suspect. Before calling a system safe to delegate through, ask what the workflow preserves in the human, not only what it extracts from the model. The person in the loop is not a checkpoint. It is a competence that can be kept, trained, drained, or quietly spent.

## Limits

This essay does not claim that AI assistance always reduces competence, that every domain needs identical safeguards, or that calibration and interface design are secondary concerns. It argues for a narrower point: delegation becomes unsafe when assistance erodes the maintenance competence needed to catch and repair errors faster than it improves output.

## References

- `2604.04721` `AI Assistance Reduces Persistence and Hurts Independent Performance`
- `2601.20245` `How AI Impacts Skill Formation`
- `2602.20206` `Mitigating "Epistemic Debt" in Generative AI-Scaffolded Novice Programming using Metacognitive Scripts`
- `2603.25197` `The Competence Shadow: Theory and Bounds of AI Assistance in Safety Engineering`
- `2502.03482` `Can Domain Experts Rely on AI Appropriately? A Case Study on AI-Assisted Prostate Cancer MRI Diagnosis`
- `2603.11821` `Stuck on Suggestions: Automation Bias, the Anchoring Effect, and the Factors That Shape Them in Computational Pathology`
- `2411.01007` `When Two Wrongs Don't Make a Right: Examining Confirmation Bias and the Role of Time Pressure During Human-AI Collaboration in Computational Pathology`
- `2402.01292` `From Evidence to Decision: Exploring Evaluative AI`
