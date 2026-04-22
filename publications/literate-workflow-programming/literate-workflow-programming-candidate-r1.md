# Literate Workflow Programming

The interesting change in agent systems is not that markdown suddenly became executable. It is that more of the system's real control surface now lives in human-readable workflow specifications: stage contracts, package manifests, tool policies, skill declarations, review gates, and packet scaffolds. Those surfaces are still too loose to call "code" in the ordinary sense. But calling them mere context files is now too weak. They increasingly behave like source artifacts for the parts of the system that matter most: what the agent is allowed to see, what it is allowed to do, what state can advance, and what failures can block promotion.

That narrower claim matters because the broader one collapses under pressure. Passive markdown is not a programming language. A free-floating `AGENTS.md` file is not execution. A run log is not source. A workflow note only becomes source-like when a runtime can interpret it, validators can check it, policy can enforce it, and debugging traces can map failures back to the governing clauses. The right frame is therefore not "markdown as code." It is workflow specification as the visible source surface, validation as the hinge, traces as derivative debugging records, and provenance as the next missing layer.

## What This Essay Will Not Claim

This essay will not claim that plain markdown is executable by itself. It will not claim that stricter formalization always improves agent behavior. It will not claim that reviewable runs are the source of truth, that current repo skills already form a portable production substrate, or that this repo has already solved claim-level provenance. It will also keep imports, package-as-object semantics, and repo-wide validator promotion out of scope. Those are interesting extensions, but they are not the claims the current evidence can carry.

## The Specification Surface

Agent workflows increasingly expose a surface that looks more like source than prompt glue. A package manifest says what the live draft is, what the governing brief is, and which stage is active. A workflow document says what the stage means, what contexts are required, and what transitions are valid. A packet manifest says which artifact is the candidate, which artifact is the live draft, which validators apply, and which moves are prohibited. These surfaces do not contain the whole program, but they do contain the human-readable specification of what the harness is supposed to do next.

This is why "context engineering" is too broad a label. Context engineering covers anything that helps the model act. Workflow specifications make a narrower and more useful claim: they are inspectable control surfaces that can be read by both humans and runtimes. They do not replace code. They externalize the part of the system that would otherwise remain buried in ad hoc prompts, local memory, or operator folklore.

The literature now gives that claim more support than the repo had at the start of this package. It is no longer only a local intuition that structured natural-language workflow layers can behave like source. Specification-oriented agent work is converging on the idea that the visible control surface should be explicit, inspectable, and executable enough for the runtime to honor it. That still does not make the specification sufficient on its own. It makes it the visible layer that later components can bind to.

## Validation Is The Hinge

Validation is what stops this from collapsing back into documentation. A workflow specification only becomes meaningful source when the system can check whether the world still matches the declared contract. That is why validation belongs in the center of the argument rather than at the tail end of implementation.

In practice, that validation layer is not one thing. It includes stage-resolution checks, package lifecycle checks, packet completeness checks, policy constraints on tools and transitions, contradiction checks on promoted claims, and bounded drift checks between source surfaces and local evidence. The common function is the same: validation turns a readable specification into an enforceable one.

This is also where the passive-markdown overclaim fails. A markdown file that nobody validates is still just a note. A markdown file that determines stage routing, points to the governing brief, blocks promotion when the packet is incomplete, and fails when evidence/index state drifts has crossed into a different category. It is still not executable in the same sense as a compiler target, but it is no longer accurate to describe it as only narrative support.

The repo's own lifecycle guardrails now make that clearer than before. `status.yaml` is no longer just metadata. It routes the next stage. `config.blueprint_path` is no longer just an optional pointer. It determines the governing brief that packet tooling and lifecycle checks should resolve first. The point is not that these files replaced code. The point is that the system now depends on them as declared control surfaces.

## Traces Are Not Source

The temptation once a repo gains good logs is to treat the logs as the real artifact. That is the wrong hierarchy. Reviewable runs, execution records, and debugging traces matter because they show what happened under a specification. They do not become the specification by being detailed.

That distinction matters for at least two reasons. First, logs are downstream artifacts. They inherit the ambiguities and omissions of the source surface. Second, the same log can be read very differently depending on whether the governing workflow contract was correct. A clean trace under a bad specification does not rescue the specification. A noisy trace under a good specification may still be diagnostically useful. The analytical job is to preserve the link between the two without collapsing them into one object.

This is the right place to understand Reviewable Runs. They are not the place where the repo should store truth about what a package is or what a stage means. They are the place where the repo should store inspectable evidence of how the harness interpreted those truths, where it drifted, and what validator or checker forced correction. That is why the best use of a proof run is not "the trace proves the policy." It is "the trace shows how the system behaved relative to the policy."

## `spec-diff` As A Bounded Local Proof

The most useful local proof in this package is the `spec-diff` line, precisely because it is bounded. The validator did not prove broad behavioral conformance. It proved something narrower and more defensible: that a declared evidence surface and the package's local intake state can drift, that the drift can be detected from the source side, and that the repaired state can then be revalidated.

That narrower result is exactly what a source-linked debugging tool should do. In `literate-workflow-programming`, it exposed mismatch in the paper-intake surface. In `illusion-of-swarm`, it caught orientation drift across mixed local evidence forms and verified the repaired index state without pretending to validate the essay itself. That is a useful proof because it shows the role of traces and validators in a workflow-specification stack. It does not show that stricter specs always improve agents. It shows that source-linked drift can be caught and explained.

This is also why the source/trace distinction has to stay sharp. The `spec-diff` report is not the source artifact. The package manifest, paper index, and declared evidence surface are the source side. The report is a derivative debugging surface that tells you where those source surfaces no longer match local state.

## Provenance Is The Next Missing Layer

Once specification and validation are treated seriously, the next pressure point is provenance. A repo can know which stage is active, which candidate is authorized, and which validator failed without yet knowing which promoted claim is backed by which evidence and where a contradiction entered the system. That is the gap this package kept running into.

The claim ledger, contradiction register, and scorecard improved that situation locally. They made it possible to say which claims were article-ready, which were caveated, and which tensions remained unresolved. But that is still not full claim-level provenance. It is a claim-state surface, not a complete claim-evidence graph. That distinction should remain explicit, because the current system benefits more from naming the missing layer honestly than from pretending it is already present.

So the next layer in literate workflow programming is not "more markdown." It is provenance attached tightly enough to the workflow stack that promoted claims can carry their evidence state, contradiction state, and validation history with them. That is the point where semantic debugging becomes much more than rerunning validators. It becomes the ability to explain why a claim was allowed to travel.

## Skills As A Bounded Support Layer

Skills belong in the story, but not at the center. The evidence here is strong enough to say that skills are code-like workflow units: reusable, composable, and often closer to a callable capability than a paragraph of guidance. But raw markdown skills are still not portable production substrate. They depend on capability binding, routing, verification, and namespace control that the current repo only partially supplies.

That is why the skills bridge should remain bounded. It helps explain why literate workflow programming is not only about stage docs and manifests. It does not justify turning the essay into a generalized claim that markdown skills are already equivalent to software modules. The correct claim is narrower: skills make the workflow stack more modular, but the portability and enforcement layer is still incomplete.

## Conclusion

Literate workflow programming is a useful label only if it stays narrow. The point is not that markdown became code. The point is that agent workflow systems increasingly expose a readable source-like layer, and that this layer becomes meaningful only when validators, policy checks, and debugging traces bind it to actual behavior. Specification is the visible surface. Validation is the hinge. Traces are derivative debugging records. Provenance is the next layer the current stack still lacks.

That frame is stronger than the original metaphor because it fits both the literature and the repo. It explains why workflow files, manifests, and stage contracts matter without pretending they are sufficient by themselves. It explains why Reviewable Runs matter without mistaking them for the source of truth. And it explains why the right engineering question is no longer whether markdown is executable. The right question is whether the specification surface, validation layer, and trace layer are coherent enough to make workflow behavior inspectable, enforceable, and debuggable.

## Limits

- This candidate does not claim that passive markdown is executable.
- It does not claim that current repo skills are portable runtime substrate.
- It treats `spec-diff` only as a bounded local proof of source/evidence drift detection.
- It treats claim-level provenance as the next missing layer, not as a current repo capability.
- It leaves import semantics, package-as-object semantics, and repo-wide validator promotion parked.

## References

- Package surfaces:
  - `publications/literate-workflow-programming/claim-ledger.md`
  - `publications/literate-workflow-programming/contradiction-register.md`
  - `publications/literate-workflow-programming/claim-scorecard.md`
  - `publications/literate-workflow-programming/literate-workflow-programming-blueprint-r1.md`
  - `publications/literate-workflow-programming/research-notes/2026-04-20-spec-diff-experiment.md`
  - `publications/literate-workflow-programming/research-notes/2026-04-21-p2a-local-intake-trace-provenance.md`
- Local proof records:
  - `reviewable-runs/logs/2026-04-22_literate-workflow-programming_manifest-first-proof-run.md`
  - `reviewable-runs/logs/2026-04-22_literate-workflow-programming_claim-provenance-step.md`
- Paper set:
  - `2603.25723`
  - `2604.13346`
  - `2603.17399`
  - `2603.00822`
  - `2510.04173`
  - `2512.19769`
  - `2512.18940`
  - `2603.20380`
  - `2504.11703`
  - `2603.23806`
  - `2603.29848`
  - `2602.13855`
