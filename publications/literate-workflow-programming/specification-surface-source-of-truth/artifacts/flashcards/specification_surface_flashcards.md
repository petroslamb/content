# Specification Flashcards

## Card 1

**Q:** In the context of AI-assisted coding, what is the "quieter failure" underlying vibe coding?

**A:** Intent remains informal until generated code is treated as the only real object.

---

## Card 2

**Q:** Why is reviewing an agent-generated diff alone insufficient for governance?

**A:** The controlling intent of the change remains outside the governed system.

---

## Card 3

**Q:** Term: Specification surface

**A:** Definition: A written surface that gains operational force by controlling, maintaining, and validating agent behavior.

---

## Card 4

**Q:** What determines whether a written document functions as a "control plane" in a repository?

**A:** The document must be part of a governance loop that the system and team can act on.

---

## Card 5

**Q:** How does spec-driven development invert the traditional implementation hierarchy?

**A:** It treats specifications as the primary contracts that code must implement, verify, or derive from.

---

## Card 6

**Q:** The "lightest form" of spec-driven development uses the specification to do what?

**A:** Guide the implementation process before any code is actually written.

---

## Card 7

**Q:** What is the characteristic of the "strongest form" of spec-driven development?

**A:** Generated code becomes a derivative artifact of a human-edited specification.

---

## Card 8

**Q:** According to the "useful rule," how much specification is considered enough?

**A:** Enough to remove consequential ambiguity with enforcement to make drift visible.

---

## Card 9

**Q:** From where does a specification's authority derive?

**A:** The maintenance loop rather than the act of writing it down.

---

## Card 10

**Q:** What is the "specification gap" in multi-agent systems?

**A:** A coordination failure where separate workers cannot reliably infer unstated decisions from fragments.

---

## Card 11

**Q:** How does integration accuracy change when code agents move from full docstrings to bare signatures?

**A:** Multi-agent integration accuracy falls sharply compared to a single-agent baseline.

---

## Card 12

**Q:** What is required to recover performance in multi-agent systems when integration fails due to weak specs?

**A:** Restoring the full shared specification to carry integrated decisions.

---

## Card 13

**Q:** Why do agents make the costs of weak specification surfaces easier to see?

**A:** They generate plausible work faster than organizations can rediscover original intent.

---

## Card 14

**Q:** According to the study "Professional Software Developers Don't Vibe, They Control," how do experts use agents?

**A:** They use them for speed while preserving agency over design and implementation.

---

## Card 15

**Q:** List three mechanisms experienced developers use to control agent outputs.

**A:** Planning before implementation, supervising outputs, and validating changes.

---

## Card 16

**Q:** In the framework of professional control, what is "vibe" categorized as?

**A:** A source-of-truth error where intent is held privately by the model.

---

## Card 17

**Q:** Where must "control" live to be effective for a software team?

**A:** In inspectable artifacts such as plans, specifications, and tests.

---

## Card 18

**Q:** In "Bootstrapping Coding Agents," what is the relationship between the specification and the agent?

**A:** The specification is used to generate the agent and then used by that agent to generate implementation.

---

## Card 19

**Q:** Concept: AgentSPEX

**A:** Definition: A typed workflow language used for specifying steps, branches, state management, and verification.

---

## Card 20

**Q:** What distinguishes a "surface" from a chat prompt in agent execution?

**A:** A surface can be read before execution, versioned, and audited after execution.

---

## Card 21

**Q:** How does ContextCov transform agent instruction files (e.g., CLAUDE.md)?

**A:** It extracts constraints into executable checks like AST queries or architectural validators.

---

## Card 22

**Q:** What does a failure in a ContextCov check reveal about the instruction surface?

**A:** Ambiguity, staleness, or drift within the instructions themselves.

---

## Card 23

**Q:** What is the primary function of "Test-Driven AI Agent Definition"?

**A:** Generating visible and hidden tests from a natural-language product specification to drive refinement.

---

## Card 24

**Q:** What does FASTRIC provide for LLM interactions?

**A:** A prompt specification language for verifiable interactions and procedure checks.

---

## Card 25

**Q:** What does the tool AgentPex evaluate in agent traces?

**A:** Procedural violations that outcome-only scoring might miss.

---

## Card 26

**Q:** What is the goal of AgentFixer after detecting a failure?

**A:** Turning failure detection into specific repair suggestions through root-cause analysis.

---

## Card 27

**Q:** Why is polished output insufficient according to "From Fluent to Verifiable"?

**A:** Verification requires the ability to reconstruct claim-evidence relations.

---

## Card 28

**Q:** When does a context file become part of a specification surface?

**A:** When it is maintained and connected to evaluation or enforcement mechanisms.

---

## Card 29

**Q:** What is the "operational test" for determining if a file belongs to the specification surface?

**A:** Does the file change what the agent is allowed to do or what outputs count as valid?

---

## Card 30

**Q:** In AI-assisted work, what is typically the most visible downstream artifact?

**A:** The generated code implementation.

---

## Card 31

**Q:** What is the danger of a team treating a code diff as the "whole truth"?

**A:** The team ends up reviewing symptoms rather than the governing intent.

---

## Card 32

**Q:** What property must a specification surface have to avoid being just "markdown in a repository"?

**A:** Governed authority through maintenance and active validation loops.

---

## Card 33

**Q:** How do human teams already model the "specification surface" pattern?

**A:** Through API contracts, BDD scenarios, schemas, and interface definitions.

---

## Card 34

**Q:** What specific coordination failure occurs when specifications are weak for multi-agent systems?

**A:** Separate workers do not reliably converge on unstated decisions.

---

## Card 35

**Q:** Why should a specification surface be "short enough to audit"?

**A:** To ensure humans can effectively review and maintain the governing authority.

---

## Card 36

**Q:** Which paper explores the spectrum of spec-driven development as a software practice?

**A:** arXiv 2602.00180 (Piskala).

---

## Card 37

**Q:** According to the source, why is "vibe" a source-of-truth error?

**A:** It asks the generated code to stand as the public record while intent remains private to the model.

---

## Card 38

**Q:** What are "evidence surfaces" in the context of agent execution?

**A:** Traces and audits that show if execution respected the specification surface.

---

## Card 39

**Q:** What is the result of using a "maintained specification surface" during a code review?

**A:** Reviewers can ask if the implementation drifted from the surface or if the surface failed to carry a decision.

---

## Card 40

**Q:** A specification surface is not necessarily code; what are some alternative formats it might take?

**A:** YAML, markdown with conventions, tests, schemas, or claim-evidence ledgers.

---

## Card 41

**Q:** If a file only describes a project for human orientation, it is categorized as _____ rather than a specification surface.

**A:** Documentation

---

## Card 42

**Q:** The core problem of "separate workers not converging on unstated decisions" is known as the _____ gap.

**A:** Specification

---

## Card 43

**Q:** The ability of an agent to use a specification to generate another implementation is demonstrated in "_____ Coding Agents."

**A:** Bootstrapping

---

## Card 44

**Q:** In professional practice, developers preserve _____ over design even when using speed-enhancing agents.

**A:** Agency

---

## Card 45

**Q:** A README full of advice lacks _____ and therefore is not a control plane.

**A:** Governance

---

## Card 46

**Q:** In the Sartori study, integration accuracy falls when docstrings are stripped to bare _____.

**A:** Signatures

---

## Card 47

**Q:** ContextCov uses _____ queries or architectural validators to enforce constraints.

**A:** AST (Abstract Syntax Tree)

---

## Card 48

**Q:** AgentFixer moves from failure detection to providing _____ recommendations.

**A:** Fix

---

## Card 49

**Q:** Trace and audit systems function as _____ surfaces.

**A:** Evidence

---

## Card 50

**Q:** When generated parts fail to integrate, better _____ inspection is not enough to fix the root cause.

**A:** Post-hoc

---

## Card 51

**Q:** Professional control moves the burden of intent into _____, such as plans and specifications.

**A:** Artifacts

---

## Card 52

**Q:** The specification surface must be "close enough to execution" that _____ hurt.

**A:** Violations

---

## Card 53

**Q:** Agent SPEX is described as a _____ workflow language.

**A:** Typed

---

## Card 54

**Q:** In spec-driven development, specifications are treated as _____ that code implements.

**A:** Contracts

---

## Card 55

**Q:** The decisive property that makes a written surface "operational" is _____.

**A:** Governance

---

## Card 56

**Q:** Why does AI coding increase the pressure to rediscover intent?

**A:** Implementation can now appear faster than the intent behind it can be recovered.

---

## Card 57

**Q:** What happens when a team reviews a pull request where the agent-generated diff is the only object treated as real?

**A:** Every later question about the feature must be reconstructed from symptoms.

---

## Card 58

**Q:** According to the text, a one-off chat prompt is not a source of truth because it is not _____.

**A:** Durable (or reviewable/repairable)

---

## Card 59

**Q:** What is the relationship between guidance and drift in spec-as-source models?

**A:** Guidance that is only consulted up front can drift; it needs tests and contract checks to stay alive.

---

## Card 60

**Q:** How does a single-agent baseline react to the stripping of specifications compared to multi-agent teams?

**A:** The single-agent baseline degrades more gracefully.

---

## Card 61

**Q:** What does the paper "Natural-Language Agent Harnesses" focus on?

**A:** Execution structure, roles, state, and verification interpreted by a runtime.

---

## Card 62

**Q:** What is a "claim ledger" in the context of generated research?

**A:** A surface used to maintain and check the validity of claims and evidence.

---

## Card 63

**Q:** Why is formality in specifications considered to "earn its place"?

**A:** When it provides the team with something specific to test and repair.

---

## Card 64

**Q:** What is the "professional-practice" finding regarding the role of vibe coding?

**A:** Experienced developers reject vibe in favor of infrastructural control and artifact-based design.

---

## Card 65

**Q:** What specific items might be contained in a "claim-evidence ledger"?

**A:** Claims made by an agent and the specific evidence used to support them for auditability.

---

## Card 66

**Q:** Why is "better post-hoc inspection" insufficient for multi-agent coordination failures?

**A:** It cannot replace the shared decisions that must be present in the governing surface.

---

## Card 67

**Q:** In the context of ContextCov, what are "LLM-based judgments" used for?

**A:** Enforcing constraints where deterministic checks (like AST queries) are not enough.

---

## Card 68

**Q:** Which paper discusses claim-level auditability for deep research agents?

**A:** arXiv 2602.13855 (Rasheed et al.).

---

## Card 69

**Q:** What is the risk of a "long instruction file" that is not connected to a control loop?

**A:** It can be stale, contradictory, ignored, or only useful for narrow tasks.

---

## Card 70

**Q:** How does the specification surface affect the questions a reviewer asks about a PR?

**A:** It shifts focus from the code diff to whether the intended behavior was specified and checked.

---

## Card 71

**Q:** True or False: Natural language is always equivalent to code in a specification surface.

**A:** False (The surface can be natural language, YAML, or other formats, but it must be governed).

---

## Card 72

**Q:** What role does "domain expertise" play for experienced developers using agents?

**A:** It allows them to decide where agents are suitable and to supervise their outputs.

---

## Card 73

**Q:** In the ContextCov framework, what are "shell shims" used for?

**A:** Extracting and enforcing executable constraints from instruction files.

---

## Card 74

**Q:** What defines a "repair target" in spec-driven development when a divergence is found?

**A:** The target is the specification and its interpretation, not just the changed code file.

---

## Card 75

**Q:** According to the text, what prevents separate workers from reliably converging on unstated decisions?

**A:** The specification gap.

---

## Card 76

**Q:** What is the "practical burden" for teams adopting specification surfaces?

**A:** Deciding which surfaces deserve authority and keeping them structured enough to parse/test.

---

## Card 77

**Q:** Which paper identifies "Willful Disobedience" in agentic traces?

**A:** arXiv 2603.23806 (Sharma et al.).

---

## Card 78

**Q:** What does the "source-of-truth claim under pressure" refer to?

**A:** The governing surface must contain the shared decisions that independent work requires to integrate.

---

## Card 79

**Q:** What is the significance of the year 2025 in the study of professional software developers?

**A:** It is the year cited in the paper title regarding how developers use AI agents (arXiv 2512.14012).

---

## Card 80

**Q:** What is the relationship between "trace violations" and the specification surface?

**A:** Trace violations reveal where execution failed to respect the governing specification.

---

## Card 81

**Q:** How does "FASTRIC" improve LLM interactions?

**A:** By providing a prompt specification language that makes interactions verifiable.

---
