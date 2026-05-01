# Candidate Draft

This bounded candidate must remain a sibling to the live draft. Do not overwrite `publications/literate-workflow-programming/literate-workflow-programming-flagship/literate-workflow-programming.md`.

Current doctrine brief: `publications/literate-workflow-programming/validation-lifecycle-infrastructure/validation-is-lifecycle-infrastructure.md`
Current governing blueprint: `publications/literate-workflow-programming/validation-lifecycle-infrastructure/iterations/r1/validation-is-lifecycle-infrastructure-blueprint-r1.md`

# Validation Is Lifecycle Infrastructure

When an agentic workflow fails, operators still reach first for the last visible artifact. They inspect the trace, scrutinize the tool call, and hunt for the hidden implementation bug. That habit belonged to systems where the real logic lived mostly in code and the surrounding files were commentary. Modern agent stacks already work differently. Workflow specs, policy files, package manifests, and evidence indexes now decide which tools can run, which stages count as complete, and which claims inherit source support. They remain human-readable, so people keep reading them as advice. Meanwhile the harness is already treating them as authority. That advisory-prose illusion is the architectural mistake. Validation matters because it is the layer that keeps those readable workflow surfaces attached to reality.

This is a narrower claim than the larger literate-workflow-programming frame, and that boundary is the point. The essay does not need to prove that markdown has become a general programming language. It only needs to show that once workflow surfaces begin governing coordination, policy, and evidence inheritance, they stop behaving like ordinary prose. They become source-like objects with a different operational requirement. A readable file is not source merely because it exists. It becomes source-like when the rest of the system can fail against it.

The first mechanism is constraint and policy enforcement. ContextCov matters because it turns instruction files into executable constraints instead of soft reminders. ALARA and Progent matter because they turn context and privilege files into blockable authority boundaries rather than safety commentary. AgentFixer matters because it treats failure as a lifecycle problem spanning prompt analysis, cross-stage checks, trace comparison, and repair loops rather than as a final-output inspection problem (Sharma, 2026; Agostino and D'Souza, 2026; Shi et al., 2025; Mulian et al., 2026). Put together, they show something specific. Once a workflow surface is already deciding what the agent may see, call, or inherit, a stale clause is no longer bad documentation. It is a live control failure. Validation belongs in the middle because that is where the governing surface can still be corrected before the runtime only looks guilty for obeying the wrong contract.

The second mechanism is drift in evidence-bearing surfaces. The local `spec-diff` proof in this package matters because it makes the doctrine concrete without exaggerating what one experiment can prove. The package looked coherent on a quick read. Declared status, evidence surfaces, and workflow state still drifted apart. The check did not reveal a philosophical mismatch between markdown and code. It revealed a more ordinary and more important failure: source inheritance had already broken while the package still appeared governable. That is the practical reason validation is infrastructure. It pushes the failure back toward the governing surface instead of leaving diagnosis buried in the eventual output, where the damage is visible but the cause is harder to localize.

Traces still matter, but they matter inside that hierarchy. AgentPex and FASTRIC are useful because they evaluate runs against declared rules and protocols, not because they make logs the deepest truth in the system (Sharma, Barke, and Zorn, 2026; Jin, 2025). Once the system starts promoting synthesized claims rather than only emitting actions, the same hierarchy pushes one step further. Claim-Level Auditability shows why execution logs stop being enough on their own: readers need to know which evidence supported a claim, where contradictions stayed live, and how much audit work remains before a result deserves trust (Rasheed et al., 2026). A synthesis can execute every visible step cleanly and still promote a claim whose evidence link is missing, whose contradiction state was never preserved, or whose audit burden was silently shifted to the reader. A clean trace can show compliance with a bad or stale governing surface. It cannot, by itself, show that the promoted claim deserved to inherit authority from that surface.

That is why validation has to be treated as infrastructure rather than terminal QA. This does not mean every readable workflow file is already a programming language, and it does not make runtime debugging obsolete. It means the real system boundary has moved. Workflow specs, policy surfaces, and evidence maps are already where authority, constraint, and inheritance are being declared. If validation stays framed as something that happens after the output exists, diagnosis will keep arriving after the real break has already happened. The runtime will look like the problem because it is the last visible layer. The governing surface will escape scrutiny because it still looks like prose. Validation is the maintenance layer for that new reality.

## Limits

This draft does not claim that markdown itself is a full programming language, that all readable workflow files are already portable execution substrate, or that current repo-local traces already satisfy claim-level provenance. It keeps the focus on one narrower doctrine: workflow specifications, policy surfaces, and evidence maps become governable only when validation spans the lifecycle. The larger flagship claim about literate workflow programming remains deliberately out of scope.

## References

Sharma, R. K. (2026). *ContextCov: Deriving and Enforcing Executable Constraints from Agent Instruction Files*.

Agostino, C. J., and D'Souza, N. (2026). *ALARA for Agents*.

Shi, T., He, J., Wang, Z., et al. (2025). *Progent: Programmable Privilege Control for LLM Agents*.

Mulian, H., Zeltyn, S., Levy, I., et al. (2026). *AgentFixer: From Failure Detection to Fix Recommendations in LLM Agentic Systems*.

Sharma, R. K., Barke, S., and Zorn, B. (2026). *Willful Disobedience: Automatically Detecting Failures in Agentic Traces*.

Jin, W.-L. (2025). *FASTRIC: Prompt Specification Language for Verifiable LLM Interactions*.

Rasheed, R. A., Banerjee, S., Mukherjee, A., and Hazra, R. (2026). *From Fluent to Verifiable: Claim-Level Auditability for Deep Research Agents*.
