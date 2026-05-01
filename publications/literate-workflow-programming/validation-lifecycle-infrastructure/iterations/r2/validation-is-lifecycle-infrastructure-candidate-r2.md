# Candidate Draft

This bounded candidate must remain a sibling to the live draft. Do not overwrite `publications/literate-workflow-programming/literate-workflow-programming-flagship/literate-workflow-programming.md`.

Current doctrine brief: `publications/literate-workflow-programming/validation-lifecycle-infrastructure/validation-is-lifecycle-infrastructure.md`
Current governing blueprint: `publications/literate-workflow-programming/validation-lifecycle-infrastructure/iterations/r1/validation-is-lifecycle-infrastructure-blueprint-r1.md`

# Validation Is Lifecycle Infrastructure

When an agentic workflow fails, operators still reach first for the runtime artifact. They inspect the trace, scrutinize the tool call, and hunt for the hidden implementation bug. That habit belongs to systems where the real logic lived mostly in code and the surrounding files were commentary. Modern agent stacks already work differently. Workflow specs, policy files, package manifests, and evidence indexes now decide which tools can run, which stages count as complete, and which claims inherit source support. They remain human-readable, so people keep reading them as advice. Meanwhile the harness is already treating them as authority. That advisory-prose illusion is the architectural mistake. Validation matters because it is the layer that decides whether those readable workflow surfaces stay attached to reality.

This is a narrower claim than the larger literate-workflow-programming frame, and that is exactly its strength. The point is not to prove that markdown has become a general programming language. The point is that the stable layer operators edit, inspect, and hand off has moved outward into workflow documents and governing surfaces. Interpretable Context Methodology makes folder structure and stage contracts load-bearing. Natural-Language Agent Harnesses externalize orchestration into editable natural-language artifacts. AgentSPEX goes further with typed steps, branching, state, and replay. Bootstrapping Coding Agents states the correction directly: the specification should remain the artifact of record (Van Clief and McDermott, 2026; Pan et al., 2026; Wang et al., 2026; Monperrus, 2026). Once that layer is carrying coordination and authority, the practical question changes. Can the system keep those source-like surfaces synchronized with the evidence, policies, and constraints they claim to govern?

That is why validation belongs in the middle of the lifecycle rather than at the end. A readable workflow file does not become source-like by looking structured. It becomes source-like when other parts of the system can fail against it. ContextCov is useful because it turns instruction files into executable constraints instead of soft reminders. ALARA and Progent do the same for privilege and policy boundaries. AgentFixer shows why that pressure cannot wait for terminal QA: by the time a bad output appears, the failure may already have spread across stages, inputs, checks, traces, and repair loops (Sharma, 2026; Agostino and D'Souza, 2026; Shi et al., 2025; Mulian et al., 2026). Once validators and policy layers are already acting on the workflow surface, calling validation "cleanup" understates the job. It is the infrastructure that keeps the governing layer governable.

The consequences are larger than better hygiene. Drift in a workflow contract becomes runtime-visible process breakage. A policy file that looked like documentation turns out to be the place where tool authority was actually declared. An evidence index that seemed like bookkeeping becomes the point where later synthesis quietly lost its source inheritance. The local `spec-diff` proof in this package matters for exactly that reason. It did not demonstrate some heroic semantic theorem. It exposed a humbler and more important fact: declared package state, evidence surfaces, and workflow status can drift apart while still looking coherent to a reader skimming the package. The value of the check was that it pushed the failure back toward the governing surface instead of leaving diagnosis buried in the eventual output.

Traces help here, but only inside the right hierarchy. They are useful because they can be checked against declared source, rules, and protocols. AgentPex and FASTRIC matter for that reason. They do not make traces the deepest truth in the system. They make traces legible relative to a prior contract (Sharma, Barke, and Zorn, 2026; Jin, 2025). Once the system starts promoting synthesized claims rather than only emitting actions, the same hierarchy pushes one step further. Claim-Level Auditability shows why execution logs stop being enough on their own: readers need to know which evidence supported a claim, where contradictions stayed live, and how much audit work remains before a result deserves trust (Rasheed et al., 2026). That is not a retreat from the validation doctrine. It is what the doctrine demands once the workflow surface begins governing claims as well as actions.

The operational consequence is plain. Builders can no longer treat workflow specs, policy surfaces, and evidence maps as if they were commentary simply because a human can read them. Those files are already where authority, constraint, and inheritance are being declared. If validation stays framed as terminal QA, diagnosis will keep arriving after the real break has already happened. The runtime will look guilty because it is the last visible layer. The governing surface will escape scrutiny because it still looks like prose. Validation is the infrastructure that closes that gap. It is what makes source-like workflow surfaces real enough to trust, contest, and repair.

## Limits

This draft does not claim that markdown itself is a full programming language, that all readable workflow files are already portable execution substrate, or that current repo-local traces already satisfy claim-level provenance. It keeps the focus on one narrower doctrine: workflow specifications, policy surfaces, and evidence maps become governable only when validation spans the lifecycle. The larger flagship claim about literate workflow programming remains deliberately out of scope.

## References

Van Clief, J., and McDermott, D. (2026). *Interpretable Context Methodology: Folder Structure as Agentic Architecture*.

Pan, L., Zou, L., Guo, S., Ni, J., and Zheng, H.-T. (2026). *Natural-Language Agent Harnesses*.

Wang, P., Huang, J., Yao, J., et al. (2026). *AgentSPEX: An Agent SPecification and EXecution Language*.

Monperrus, M. (2026). *Bootstrapping Coding Agents: The Specification Is the Program*.

Sharma, R. K. (2026). *ContextCov: Deriving and Enforcing Executable Constraints from Agent Instruction Files*.

Agostino, C. J., and D'Souza, N. (2026). *ALARA for Agents*.

Shi, T., He, J., Wang, Z., et al. (2025). *Progent: Programmable Privilege Control for LLM Agents*.

Mulian, H., Zeltyn, S., Levy, I., et al. (2026). *AgentFixer: From Failure Detection to Fix Recommendations in LLM Agentic Systems*.

Sharma, R. K., Barke, S., and Zorn, B. (2026). *Willful Disobedience: Automatically Detecting Failures in Agentic Traces*.

Jin, W.-L. (2025). *FASTRIC: Prompt Specification Language for Verifiable LLM Interactions*.

Rasheed, R. A., Banerjee, S., Mukherjee, A., and Hazra, R. (2026). *From Fluent to Verifiable: Claim-Level Auditability for Deep Research Agents*.
