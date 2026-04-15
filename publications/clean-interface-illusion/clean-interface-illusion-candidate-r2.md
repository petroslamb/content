# The Clean Interface Illusion

A model that solves retail support tasks 61 percent of the time sounds close to useful. In `tau-bench`, that same result looks different once you ask a less flattering question: what happens when you run the task again and again? The best model reaches 61 percent in retail and 35 percent in airline, then the retail pass-to-the-eighth falls below 25 percent. The agent did not forget how to do the job between the first attempt and the eighth. What changed was the reading. The topline score sounded like capability. The repeated-run score starts to sound like operations.

That gap is why the old benchmark argument is no longer enough. For a while it was useful to say that agent evaluations were too clean, too scripted, or too toy-like to matter. Serious benchmark builders already heard that complaint and moved. `REAL` rebuilt real sites into deterministic replicas. `WebForge` attacked the realism, reproducibility, and scalability trilemma directly. `WebSuite` replaced one opaque web score with a taxonomy that makes failure localizable. `LiveMCPBench` moved tool use into a large MCP ecosystem where retrieval and composition are part of the task. The field did not stand still. Benchmark realism improved. Benchmark interpretation did not improve at the same speed.

A point score still travels through the field as a trust signal. It begins life as a bounded measurement inside a particular environment and ends up sounding like a statement about deployment readiness in the large. That is the live mistake. The adaptation paper that names the clean-interface problem is useful here because it spells out what often gets hidden by that inflation: underspecified rules, shifting environments, implicit objectives, and unreliable signals. Richer benchmarks already contain more structure than simple pass rates suggest. We keep flattening that structure back into one number and then asking the number to authorize claims it was never built to carry.

The reliability literature makes the cost of that flattening visible. `Towards a Science of AI Agent Reliability` separates consistency, robustness, predictability, and safety because accuracy alone cannot tell you whether behavior stays within useful bounds. Its central pattern matters because it is so hard to dismiss: accuracy rises across models while reliability trails behind. A field can therefore publish stronger-looking benchmark results while leaving the operational meaning of those results unresolved. That is not a bookkeeping defect. It is the whole governance problem.

Once that distinction is in view, average scores stop looking like a complete summary of the object. An agent that fails on a stable subset of tasks is a very different deployment target from one that alternates between brilliance and collapse across repeated runs, prompt perturbations, or environment changes. The average score may look similar. The downstream decision should not. One case invites routing, scope control, and targeted repair. The other contaminates planning because nobody can say where the failure boundary really lives.

The clearest turn in the current literature appears when `WebSuite` and `WebForge` are read together instead of as separate benchmark releases. `WebSuite` says the engineering value of evaluation rises when failures become localizable. A flat web score is less useful than learning that the agent breaks on complex forms, ambiguous link selection, or another repeatable interaction class. `WebForge`, from the opposite direction, argues that browser evaluation needs richer environments, injected noise, and multidimensional difficulty control because aggregate numbers hide capability profiles. Taken together, these papers are not building better publicity surfaces. They are building finer decision surfaces. The benchmark gets richer at exactly the moment the topline score becomes less sufficient on its own.

`LiveMCPBench` pushes the same lesson into tool use. Inside a large MCP ecosystem, the hard part is not only calling a known function. The hard part is finding the right tool inside a noisy distributed surface, then composing multiple steps without losing the thread. That is much closer to deployment than the early tool-use demos that made function calling look almost solved. It still does not settle the trust question. A score earned in a large toolspace can tell you that an agent sometimes retrieves and sequences tools under that benchmark's assumptions. It does not yet tell you how confidently to delegate the surrounding workflow when recovery, restraint, and repeated reliability still sit outside the topline.

`REAL` and `TheAgentCompany` make the same point from another angle. They are already difficult to dismiss as toy settings. `REAL` still tops out around 41.07 percent on deterministic simulations of real websites. `TheAgentCompany` finds 30.3 percent autonomous completion on consequential office tasks and 39.3 percent on a partial-credit metric. Those numbers establish bounded usefulness, which matters. They do not rescue the broader reading. If anything, they make the interpretive problem sharper. Even when realism improves, the right conclusion gets narrower, not broader.

The rule that follows is plain enough to travel. A benchmark score should license only the confidence its design actually measured. If the benchmark measures task completion in a bounded environment, then it supports claims about bounded-environment task completion. If it measures repeated-run stability, then it supports claims about consistency. If it measures failure localization, then it supports engineering diagnosis. If it measures tool retrieval at scale, then it supports claims about retrieval discipline in a large toolspace. Everything beyond that is narrative inflation.

This is not an argument against benchmark ambition. It is an argument against asking one number to play every role at once. Evaluation becomes more useful when it feeds deployment review, permission design, routing policy, and fallback planning instead of collapsing all of them into a readiness story. The clean interface illusion was never only about tidy interfaces. It was about how much confidence gets imagined after the measurement ends. The benchmark builders have done enough to move the field past the toy-benchmark complaint. The next correction belongs to the readers.

## Limits

- This essay does not claim that modern agent benchmarks are still trapped in toy settings.
- This essay does not claim that aggregate scores are useless. It claims they are routinely overread.
- This essay does not claim that current agents lack bounded practical value.
- This essay does not attempt to deliver a full certification framework for deployment or procurement.

## References

- `2406.01623` WebSuite: Systematically Evaluating Why Web Agents Fail
- `2412.14161` TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks
- `2504.11543` REAL: Benchmarking Autonomous Agents on Deterministic Simulations of Real Websites
- `2508.01780` LiveMCPBench: Can Agents Navigate an Ocean of MCP Tools?
- `2602.02760` From Task Solving to Robust Real-World Adaptation in LLM Agents
- `2602.16666` Towards a Science of AI Agent Reliability
- `2604.10988` WebForge: Breaking the Realism-Reproducibility-Scalability Trilemma in Browser Agent Benchmark
- `2406.12045` τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains
