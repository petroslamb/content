# Candidate Draft

This bounded candidate must remain a sibling to the live draft. Do not overwrite `publications/literate-workflow-programming/literate-workflow-programming-flagship/literate-workflow-programming.md`.

Current doctrine brief: `publications/literate-workflow-programming/validation-lifecycle-infrastructure/validation-is-lifecycle-infrastructure.md`
Current governing blueprint: `publications/literate-workflow-programming/validation-lifecycle-infrastructure/iterations/r1/validation-is-lifecycle-infrastructure-blueprint-r1.md`

# Validation Is Lifecycle Infrastructure

When an agentic workflow fails, the old reflex is to search for the hidden implementation bug. Inspect the runtime. Read the trace. Debug the tool call. That reflex made sense when the real system lived mostly in code and the human-readable files around it were only guidance. It makes less sense now. In many modern agent systems, the workflow document, the policy file, the evidence map, and the stage contract already shape what the system is allowed to do. They are read by harnesses, checked by validators, and invoked by humans as if they were source. Yet operators still treat them like commentary. That mismatch is the real mistake. Validation matters because it is the layer that decides whether those human-readable workflow surfaces remain advisory prose or become governable objects.

That claim is narrower than the larger literate-workflow-programming frame, but it is also more useful. The interesting shift is not that markdown became code in some grand philosophical sense. The shift is that workflow specifications now occupy the stable layer operators edit, inspect, and hand off, while the runtime, the trace, and the generated output increasingly behave like derived artifacts. Interpretable Context Methodology organizes agent work around staged contracts and preserved folder structure. Natural-Language Agent Harnesses externalizes orchestration into editable natural-language contracts. AgentSPEX makes the workflow surface explicit through typed steps, branching, modules, state, replay, and verification hooks. Bootstrapping Coding Agents presses the point furthest: the specification should be the artifact of record, not the residue emitted by a run (Van Clief and McDermott, 2026; Pan et al., 2026; Wang et al., 2026; Monperrus, 2026). Once that layer is load-bearing, the question stops being whether it feels like programming language syntax. The real question becomes whether the system can keep that layer attached to reality.

That is where validation enters as infrastructure rather than cleanup. A workflow file does not become source-like because it is readable. It becomes source-like because other parts of the system can constrain it, test it, and fail against it. ContextCov derives executable constraints from instruction files. ALARA and Progent turn context and permission surfaces into enforceable control points rather than soft reminders. Test-Driven AI Agent Definition pushes the same pressure into hidden checks and regression logic. AgentFixer treats failure diagnosis as a lifecycle loop spanning prompt analysis, input checks, cross-stage consistency, output validation, trace comparison, root-cause analysis, and repair (Sharma, 2026; Agostino and D'Souza, 2026; Shi et al., 2025; Rehan, 2026; Mulian et al., 2026). Read together, these systems make a blunt architectural point: if the workflow layer is already shaping authority, constraints, and downstream execution, then validation is not arriving at the end to inspect a finished artifact. Validation is what keeps the workflow layer from drifting away from the evidence, policies, and boundaries it claims to govern.

That shift changes what a failure means. If validation is treated as terminal QA, the system can drift for a long time before anyone notices where the real break occurred. Constraint drift looks like runtime breakage even when the root cause lives in a stale workflow contract. A policy boundary looks like a safety footnote until it silently determines which tools the agent could call at all. A package evidence index looks like bookkeeping until a later synthesis promotes claims that no longer line up with the source surface they were supposed to inherit. ContextCov is useful here because it shows that natural-language instructions become operational liabilities once a runtime depends on them without executable checks. AgentFixer is useful because it shows how failures propagate across stages when diagnosis begins only after the visible output goes bad. ALARA and Progent widen the same point into context and privilege boundaries: if those file-backed surfaces are treated as commentary, operators will keep misunderstanding where permission, containment, and failure are actually determined.

Traces matter in this picture, but they matter in a different way than most current discourse suggests. It is tempting to treat the trace as deepest truth because it shows what the system actually did. That is the wrong hierarchy. AgentPex and FASTRIC are helpful precisely because they evaluate behavior against source-derived rules and protocols, not because they elevate the trace above the source (Sharma, Barke, and Zorn, 2026; Jin, 2025). The local `spec-diff` proof in this package makes the same point in a smaller form. It did not prove semantic equivalence. It caught something more ordinary and more important: package state, evidence surfaces, and declared workflow status can drift apart while still looking superficially coherent. The value of the finding was that it linked the drift back to the governing surface. That is why traces belong here as debugging surfaces. They tell you what happened relative to a declared source. They do not replace the need for that source, and they do not excuse operators from maintaining it.

The same hierarchy explains why provenance now pushes beyond traces. Once a system begins promoting synthesized claims rather than only structured outputs, it is not enough to know which steps executed. You also need to know which evidence supported a claim, where contradictions remained live, and how much audit work is still required to trust the result. Claim-Level Auditability makes that shift explicit. The bottleneck is no longer generation alone. The bottleneck is whether a later reader can reconstruct the claim-evidence relation in a way that survives scrutiny (Rasheed et al., 2026). That demand lands naturally on top of the validation story. Workflow surfaces become governable through validation. Traces make violations visible against those surfaces. Provenance becomes the next layer once the system has to defend promoted claims rather than merely explain execution. This repo does not fully satisfy that standard yet. It has validators, contradiction surfaces, and bounded drift checks, but not full claim-level provenance graphs. That is not a reason to retreat from the doctrine. It is evidence that the doctrine is pointing toward the next genuine engineering requirement.

The argument for skills belongs under the same discipline. Skills are often described as reusable procedures, and the recent literature supports that framing only conditionally. AgentSPEX and the broader skills-as-code line make externalized capability surfaces increasingly plausible. Single-Agent With Skills and SkVM show the limit at the same time: a skill is not a portable unit merely because it is written down. It needs routing, capability binding, namespace discipline, and some way to verify whether the runtime still honored the intended behavior (Li, 2026; Chen et al., 2026). That matters because it repeats the same architectural lesson. Human-readable workflow assets become real system surfaces only when the rest of the stack treats them as something stronger than memo text.

This is why the wrong-layer accusation still matters, but only as a wrapper. The point is not that runtime debugging became useless. The point is that the runtime is no longer the only place where the system becomes real. In governed agent workflows, the source-like layer is already spread across stage contracts, policy files, evidence maps, and skill surfaces that other layers load, enforce, and validate. If we keep acting as if those files remain advisory while validators and policy checks already depend on them, we will keep diagnosing failures too late and in the wrong place. Validation is the infrastructure that makes those workflow surfaces real. Treat it as terminal QA and the system will keep drifting before anyone notices what actually broke.

## Limits

This draft does not claim that markdown itself is a full programming language, that all readable workflow files are already portable execution substrate, or that current repo-local traces already satisfy claim-level provenance. It keeps the focus on one narrower doctrine: workflow specifications, policy surfaces, and evidence maps become governable only when validation spans the lifecycle. The larger flagship claim about literate workflow programming remains deliberately out of scope.

## References

Van Clief, J., and McDermott, D. (2026). *Interpretable Context Methodology: Folder Structure as Agentic Architecture*.  
Anchor for staged contracts, preserved workflow artifacts, and filesystem-level workflow structure.

Pan, L., Zou, L., Guo, S., Ni, J., and Zheng, H.-T. (2026). *Natural-Language Agent Harnesses*.  
Shows orchestration logic externalized into editable natural-language contracts and adapters.

Wang, P., Huang, J., Yao, J., et al. (2026). *AgentSPEX: An Agent SPecification and EXecution Language*.  
Strongest direct support for explicit workflow source surfaces with state, branching, replay, and verification hooks.

Monperrus, M. (2026). *Bootstrapping Coding Agents: The Specification Is the Program*.  
Makes the philosophical correction explicit: the specification should remain the artifact of record.

Rehan, T. (2026). *Test-Driven AI Agent Definition*.  
Provides the strongest direct bridge from agent specification to generated checks and regression discipline.

Sharma, R. K. (2026). *ContextCov: Deriving and Enforcing Executable Constraints from Agent Instruction Files*.  
Shows that instruction files become operational surfaces once the runtime depends on them and guardrails are generated from them.

Agostino, C. J., and D'Souza, N. (2026). *ALARA for Agents*.  
Supplies least-privilege context engineering as a governed control layer.

Shi, T., He, J., Wang, Z., et al. (2025). *Progent: Programmable Privilege Control for LLM Agents*.  
Shows policy-backed privilege control as a real runtime enforcement surface.

Mulian, H., Zeltyn, S., Levy, I., et al. (2026). *AgentFixer: From Failure Detection to Fix Recommendations in LLM Agentic Systems*.  
Strongest local anchor for validation as a lifecycle loop rather than an end-stage test.

Sharma, R. K., Barke, S., and Zorn, B. (2026). *Willful Disobedience: Automatically Detecting Failures in Agentic Traces*.  
Useful because trace evaluation is grounded in source-derived rules.

Jin, W.-L. (2025). *FASTRIC: Prompt Specification Language for Verifiable LLM Interactions*.  
Extends the same logic to protocol conformance and trace-level checking.

Rasheed, R. A., Banerjee, S., Mukherjee, A., and Hazra, R. (2026). *From Fluent to Verifiable: Claim-Level Auditability for Deep Research Agents*.  
Shows why traces alone are insufficient once claim-level provenance becomes the real bottleneck.

Li, X. (2026). *When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail*.  
Useful pressure against naïve skills-as-code claims.

Chen, L., Feng, E., Xia, Y., and Chen, H. (2026). *SkVM: Revisiting Language VM for Skills across Heterogenous LLMs and Harnesses*.  
Clarifies why externalized skills still require capability binding and runtime discipline.
