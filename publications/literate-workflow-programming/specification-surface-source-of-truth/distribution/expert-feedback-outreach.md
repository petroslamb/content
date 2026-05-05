# Expert Feedback Outreach Tracker

Package: `publications/literate-workflow-programming/specification-surface-source-of-truth`
Essay: The Specification Surface Is the New Source of Truth
Canonical URL: https://lambpetros.substack.com/p/the-specification-surface-is-the
Batch: 2026-05-05 specification-surface paper-author feedback
Hypothesis: A bounded paper-author batch will produce sharper objections, corrections, or weak ties than general social distribution because the essay makes explicit claims about how each cited paper contributes to the specification-surface argument.
Author-value hypothesis: Paper authors are more likely to engage when the note gives them a useful lens on their own work first, then uses the essay as the medium for a shared boundary question. The Linyue Pan reply suggests that framing the ask as a narrow objection useful to the author's next revision can create a stronger reason to respond than asking them to review or promote the essay.
Message variant: `paper_specific`
Success window: 14 days after each message send; default review date is 2026-05-19 if the batch is sent on 2026-05-05.
Decision after window: continue if at least one useful objection, correction, or weak-tie reply appears; revise message if connection acceptance happens but no replies arrive; pause if the batch feels promotional; retire any target type whose paper role is too thin to justify direct outreach.

## Run Context

- Workflow: `expert_feedback_outreach`
- Validation: `./content-agent validate --workflow expert_feedback_outreach --package literate-workflow-programming/specification-surface-source-of-truth` passed with no findings on 2026-05-05.
- Initial guided run record: `reviewable-runs/logs/run-2026-05-05T08-49-29Z-literate-workflow-programming-specification-surface-source-of-truth-expert-feedback-outreach.yaml`
- Corrected guided run record after workflow patch: `reviewable-runs/logs/run-2026-05-05T08-56-31Z-literate-workflow-programming-specification-surface-source-of-truth-expert-feedback-outreach.yaml`
- Existing distribution surfaces:
  - `../specification-surface-source-of-truth-distribution-plan-r3.md`
  - `../specification-surface-source-of-truth-distribution-log-r3.md`
- External mutation boundary: after explicit user green light on 2026-05-05, the in-app browser attempted no-note LinkedIn connection invites to Deepak Babu Piskala, Camilo Chacon Sartori, and Martin Monperrus, but LinkedIn's sent-invitations manager initially showed that those invites did not land. The user then manually sent connection invites to Deepak, Camilo, and Martin from their profile pages. LinkedIn's sent-invitations manager confirmed Deepak/Piskala, Camilo/Chacon, and Martin/Monperrus after a follow-up check. The user also manually sent no-link connection notes to Linyue Pan, Shraddha Barke, and Ben Zorn. No essay link, paper-specific message, comment, email, or DM was sent by the workflow. Brian Hempel was blocked at LinkedIn's invite confirmation modal and was not marked as invited.

## Target Map

| Target | Paper | Paper role in essay | Why this person | Contact route | Invited | Accepted | Message sent | Reply | Useful outcome | Next action | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Deepak Babu Piskala | "Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants" | Software-engineering baseline for the specification-authority spectrum: spec-first, spec-anchored, and spec-as-source. | Single author of the paper that keeps the essay grounded in existing engineering practice rather than the claim that prose is code. | LinkedIn inspected 2026-05-05: `https://www.linkedin.com/in/prdeepak/`; user manually sent invite 2026-05-05; sent-invitations manager confirmed Deepak/Piskala. | yes, 2026-05-05 | pending | no | no | invite pending | Wait for acceptance; then send the prepared paper-specific message. | Direct Message route showed InMail/Premium upsell, so no message was sent. Initial browser invite attempt failed; manual profile action later landed. |
| Camilo Chacon Sartori | "The Specification Gap: Coordination Failure Under Partial Knowledge in Code Agents" | Hinge evidence for the coordination claim: weakened shared specifications cause multi-agent integration failures; restoring full specification is the stronger recovery. | The essay's strongest empirical hinge depends on this paper's result and its limits. | LinkedIn inspected 2026-05-05: `https://www.linkedin.com/in/camilo-chacon-sartori/`; user manually sent invite 2026-05-05; sent-invitations manager confirmed Camilo/Chacon; user reported acceptance 2026-05-05. | yes, 2026-05-05 | yes, 2026-05-05 | yes, 2026-05-05 | no | message sent; awaiting objection | Wait for reply; if he asks for context, send the short section first rather than the full paper. | User sent the precision-checked follow-up after rechecking the paper's abstract, recovery experiment, discussion, and conclusion. The message explicitly marks "shared authority" as the essay's extension to pressure-test. |
| Martin Monperrus | "Bootstrapping Coding Agents: The Specification Is the Program" | Strongest architectural edge case for specification-as-program and derived implementations. | The essay uses the paper to show a controlled inversion where specification becomes the durable object and implementations become downstream. | LinkedIn inspected 2026-05-05: `https://www.linkedin.com/in/martin-monperrus-369300a4/`; user manually sent invite 2026-05-05; sent-invitations manager confirmed Martin/Monperrus. | yes, 2026-05-05 | pending | no | no | invite pending | Wait for acceptance; then send the prepared paper-specific message. | Initial browser invite attempt failed; manual profile action later landed. Mutual connection Jose was visible before the attempt. |
| Brian Hempel | "Professional Software Developers Don't Vibe, They Control: AI Agent Use for Coding in 2025" | Professional-practice counterweight for the anti-vibe frame: experienced developers preserve agency through planning, supervision, validation, version control, and bounded delegation. | Coauthor of the practice paper that keeps `vibe` framed as a control-surface failure rather than a personality label. | LinkedIn inspected 2026-05-05: `https://www.linkedin.com/in/brianhempel/`; visible state after attempt: `Connect`, `Message`, `More`; profile is 3rd+. | no | n/a | no | no | blocked at confirmation | Retry manually or in a later browser pass; do not send essay link in invite. | Invite modal opened, but `Send without a note` would not submit through Playwright click, forced click, or keyboard activation. Since `Connect` remained visible, the invite is not marked sent. |
| Linyue Pan | "Natural-Language Agent Harnesses" | Runtime/harness evidence: natural-language descriptions become stronger when interpreted by a harness with decomposition, roles, state, adapters, contracts, verification, and artifacts. | First author of the paper used to distinguish loose prompts from natural-language surfaces that participate in governed execution. | LinkedIn inspected 2026-05-05: `https://www.linkedin.com/in/linyue-pan/`; user-reported manual note invite sent 2026-05-05 after browser confirmation block. | yes, 2026-05-05 | yes, 2026-05-05 | yes, 2026-05-05 | yes, 2026-05-05 | substantive boundary correction | Reply briefly, acknowledge the boundary, and ask to see or discuss v2 when ready. | Linyue's 18:02 reply sharpened the boundary: IHR+NLAH is not pure natural language; natural language becomes governing specification only when bound to executable lifecycle semantics, artifact contracts, state, adapters, validation, and recovery behavior. Otherwise it remains instruction/interface layer. |
| Shraddha Barke | "Willful Disobedience: Automatically Detecting Failures in Agentic Traces" | Trace-compliance evidence: procedural violations can be detected in traces when prompts or system instructions imply explicit behavioral rules. | Coauthor with a visible profile and directly relevant Microsoft Research background in trustworthy code generation and invariant generation. | LinkedIn inspected 2026-05-05: `https://www.linkedin.com/in/shraddha-barke-ph-d-111b4694/`; user-reported manual note invite sent 2026-05-05. | yes, 2026-05-05 | pending | no | no | invite pending | Wait for acceptance; then send the prepared paper-specific message. | Manual connection note used no essay link and asked whether the essay overconnects trace checks to specifications. |
| Ben Zorn | "Willful Disobedience: Automatically Detecting Failures in Agentic Traces" | Secondary trace/procedural-verification target for the downstream validation side of the essay. | Coauthor and visible Microsoft Research route; useful if the Shraddha route does not convert or if a broader prompt-as-program objection is wanted. | LinkedIn inspected 2026-05-05: `https://www.linkedin.com/in/ben-zorn-0a58554/`; user-reported manual note invite sent 2026-05-05; user reported acceptance 2026-05-05. | yes, 2026-05-05 | yes, 2026-05-05 | no | no | accepted; message not sent | Send the prepared paper-specific message first; if endorsement becomes necessary, confirm eligibility through arXiv's endorser page before asking. | Manual connection note used no essay link and asked about trace validation vs durable specification artifacts. Public arXiv author search under `Benjamin Zorn` shows three recent `cs.SE` papers in 2024-2026, making him a strong potential later endorser candidate, but actual endorser status still needs arXiv confirmation. |

## Batch Pacing

Recommended first wave: Deepak Babu Piskala, Camilo Chacon Sartori, Martin Monperrus, Brian Hempel, and Linyue Pan.

Actual 2026-05-05 execution: Deepak, Martin, and Shraddha are invite-pending. Camilo, Linyue, and Ben accepted. Deepak, Camilo, and Martin initially failed through the in-app browser, then the user manually retried from the profile pages; LinkedIn's sent-invitations manager confirmed all three after the manual retry. Brian remains blocked and the correct UCSD-linked profile still needs verification.

Connection requests should not include the essay link. If LinkedIn requires an invite rather than a message, use either no note or this no-link note:

```text
Hi <name> - I write Rooted Layers on AI systems and software practice. I used your paper in a recent essay and would value one narrow objection if you're open to it.
```

## 2026-05-05 First-Wave Execution Log

- Deepak Babu Piskala: attempted direct `Message`, but LinkedIn showed an InMail/Premium upsell. The browser then attempted a no-note connection invite, but the sent-invitations manager initially did not show Deepak/Piskala. The user manually retried from the profile page; a later sent-invitations check confirmed Deepak/Piskala.
- Camilo Chacon Sartori: browser attempted a no-note connection invite, but the sent-invitations manager initially did not show Camilo/Chacon/Chacon Sartori. The user manually retried from the profile page; a later sent-invitations check confirmed Camilo/Chacon. User reported that Camilo accepted on 2026-05-05 and manually sent the precision-checked author-centered follow-up the same day.
- Martin Monperrus: browser attempted a no-note connection invite, but the sent-invitations manager initially did not show Martin/Monperrus. The user manually retried from the profile page; a later sent-invitations check confirmed Martin/Monperrus.
- Brian Hempel: opened the connection invite dialog, but the `Send without a note` confirmation did not submit through the in-app browser. Post-attempt state still showed `Connect`; not marked invited.
- Linyue Pan: opened the connection invite dialog, but the `Send without a note` confirmation did not submit through the in-app browser. User later manually sent a no-link connection note. Linyue accepted and replied on 2026-05-05, saying she would be happy to discuss and that the narrow objection would be valuable feedback for their next revision. After the author-centered follow-up, she replied at 18:02 with a substantive boundary correction: IHR+NLAH is not pure natural language; IHR provides the code/runtime interfaces and execution semantics; natural language should be treated as governing specification only when bound to executable lifecycle semantics, artifact contracts, state, adapters, validation, and recovery behavior.
- Shraddha Barke: user manually sent a no-link connection note.
- Ben Zorn: user manually sent a no-link connection note.

No essay link or paper-specific message was sent in this execution pass. The next external action is a post-acceptance message only after a recipient accepts the connection.

## 2026-05-05 Outreach Lesson

The first reply came from a productive ambiguity: "one narrow objection" sounded useful to the author as feedback for a future revision. Preserve the mechanism, not the confusion. Future notes should be value-first and paper-centered: give the author one concrete lens on their own paper, name the boundary or implication that may matter to their work, then use the essay as the medium where that question appears.

Working rule: help the author first. The essay should enter as context for a shared research question, not as the object they are being asked to promote or review.

## Message Pack

### Deepak Babu Piskala

Paper: "Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants"
Paper role: baseline for the specification-authority spectrum.
Contact route: LinkedIn `https://www.linkedin.com/in/prdeepak/`
Status: manual connection invite pending as of 2026-05-05; confirmed in LinkedIn sent-invitations manager after the browser attempt failed; post-acceptance message prepared, not sent.

```text
Hi Deepak - I write Rooted Layers, a publication about how AI systems, software practice, and research ideas turn into operational constraints.

I used your paper, "Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants," as the software-engineering baseline for a recent essay on specification surfaces.

The essay uses your spec-first / spec-anchored / spec-as-source spectrum to argue that AI-assisted work becomes governable when intent moves from private prompts into maintained surfaces that teams and tools can inspect, validate, trace, and repair.

I would value one objection or correction, especially if you think I compressed spec-driven development into "source of truth" language too aggressively.

Essay: https://lambpetros.substack.com/p/the-specification-surface-is-the
```

### Camilo Chacon Sartori

Paper: "The Specification Gap: Coordination Failure Under Partial Knowledge in Code Agents"
Paper role: hinge evidence for specification as a coordination contract.
Contact route: LinkedIn `https://www.linkedin.com/in/camilo-chacon-sartori/`
Status: manual connection invite accepted as of 2026-05-05; precision-checked author-centered follow-up sent by user on 2026-05-05.

```text
Hi Camilo - thank you for connecting. I'm Petros; I write Rooted Layers, where I work through AI systems and software practice from an engineering-governance angle.

Your paper is central to something I'm trying to get right.

The part of The Specification Gap that stood out to me is the distinction between diagnosis and repair. The AST conflict detector can identify structural mismatches, especially when specifications are weakest, but in your recovery experiment the full specification is what restores performance. That makes the specification more than documentation: it functions as the coordination contract that carries the shared decisions independent agents need.

The boundary question I'm trying to handle carefully is this: should that result stay framed mainly as coordination under partial knowledge, or is it fair to extend it into a broader software-engineering claim that multi-agent coding needs maintained specification surfaces as the shared authority for integration?

I wrote that reading into a paper draft / essay, but I don't want to send a manuscript cold. The useful question for me is narrower:

Where does that interpretation overreach from your point of view?

If useful, I can send either the short section where I use The Specification Gap or the paper version.
```

### Martin Monperrus

Paper: "Bootstrapping Coding Agents: The Specification Is the Program"
Paper role: strongest architectural edge case for specification-as-program.
Contact route: LinkedIn `https://www.linkedin.com/in/martin-monperrus-369300a4/`
Status: manual connection invite pending as of 2026-05-05; confirmed in LinkedIn sent-invitations manager after the browser attempt failed; post-acceptance message prepared, not sent.

```text
Hi Martin - I write Rooted Layers, a publication about how AI systems, software practice, and research ideas turn into operational constraints.

I used your paper, "Bootstrapping Coding Agents: The Specification Is the Program," as the strongest architectural edge case in a recent essay on specification surfaces.

The essay uses it to show a controlled inversion: the specification becomes the durable object, while implementations become downstream products that can be compared against it and repaired through it.

I would value one objection or correction, especially if you think I should draw a harder line between your paper's controlled setting and the broader claim about governed specification surfaces.

Essay: https://lambpetros.substack.com/p/the-specification-surface-is-the
```

### Brian Hempel

Paper: "Professional Software Developers Don't Vibe, They Control: AI Agent Use for Coding in 2025"
Paper role: professional-practice counterweight for the anti-vibe frame.
Contact route: LinkedIn `https://www.linkedin.com/in/brianhempel/`
Status: invite blocked at confirmation on 2026-05-05; correct UCSD-linked profile still needs verification; post-acceptance message prepared, not sent.

```text
Hi Brian - I write Rooted Layers, a publication about how AI systems, software practice, and research ideas turn into operational constraints.

I used your paper, "Professional Software Developers Don't Vibe, They Control: AI Agent Use for Coding in 2025," as the professional-practice counterweight in a recent essay on specification surfaces.

The essay uses the paper to argue that "vibe" is best understood as a control-surface failure: intent stays private while generated code becomes the only visible artifact under review.

I would value one objection or correction, especially if you think the essay turns your descriptive finding about experienced developers into too strong a normative claim.

Essay: https://lambpetros.substack.com/p/the-specification-surface-is-the
```

### Linyue Pan

Paper: "Natural-Language Agent Harnesses"
Paper role: natural-language harness evidence for runtime-interpreted specification surfaces.
Contact route: LinkedIn `https://www.linkedin.com/in/linyue-pan/`
Status: manual no-link connection note sent by user on 2026-05-05; accepted and replied on 2026-05-05; author-centered follow-up sent by user on 2026-05-05; substantive boundary reply received at 18:02.

```text
Hi Linyue - thank you, and yes, I would like to make this useful from your side too.

The part of Natural-Language Agent Harnesses that stood out to me is that the harness gives natural language operational force. Decomposition, roles, state, adapters, contracts, verification, and artifacts make the description part of execution rather than just a prompt.

The boundary question I think your paper exposes is this: once natural language is interpreted by a harness, when should it still be treated as an interface to the system, and when does it become part of the system's governing specification?

That boundary feels important for how people will extend harness work into software engineering practice. If the boundary is drawn too loosely, everything becomes a "spec"; if it is drawn too narrowly, we miss the fact that the harness is already making natural language enforceable.

I used your paper in this essay as one case for that broader question.

The narrow objection I would value is: where does this framing overreach from your point of view?

Essay context: https://lambpetros.substack.com/p/the-specification-surface-is-the
```

#### Reply Draft After Linyue Boundary Correction

```text
Hi Linyue - this is exactly the boundary I was hoping you would sharpen. Thank you.

The distinction between an instruction/interface layer and a governing specification is the key correction for me. I will not treat "natural language interpreted by a harness" as sufficient by itself. The stronger line is: natural language becomes part of the governing specification only when it is bound to executable lifecycle semantics, artifact contracts, state, adapters, validation, and recovery behavior.

That also clarifies my reading of IHR + NLAH: the natural language is powerful because the IHR supplies the harness, interfaces, and execution semantics that make it operational, not because natural language alone becomes code.

I would be very interested in v2 when it is ready. This boundary is useful for my own framing, and I will keep it explicit if I develop the paper version further.
```

### Shraddha Barke

Paper: "Willful Disobedience: Automatically Detecting Failures in Agentic Traces"
Paper role: trace-compliance evidence for checking procedural violations against explicit behavioral rules.
Contact route: LinkedIn `https://www.linkedin.com/in/shraddha-barke-ph-d-111b4694/`
Status: manual no-link connection note sent by user on 2026-05-05; post-acceptance message prepared, not sent.

```text
Hi Shraddha - I write Rooted Layers, a publication about how AI systems, software practice, and research ideas turn into operational constraints.

I used "Willful Disobedience: Automatically Detecting Failures in Agentic Traces" in a recent essay on specification surfaces.

The essay uses AgentPex as evidence for the downstream validation layer: traces become useful when they can be checked against explicit behavioral rules rather than judged only by final outcome quality.

I would value one objection or correction, especially if you think I overconnect trace checking to the broader idea of maintained specification surfaces.

Essay: https://lambpetros.substack.com/p/the-specification-surface-is-the
```

### Ben Zorn

Paper: "Willful Disobedience: Automatically Detecting Failures in Agentic Traces"
Paper role: secondary trace/procedural-verification target.
Contact route: LinkedIn `https://www.linkedin.com/in/ben-zorn-0a58554/`
Status: manual no-link connection note sent by user on 2026-05-05; accepted 2026-05-05; post-acceptance message prepared, not sent.

```text
Hi Ben - I write Rooted Layers, a publication about how AI systems, software practice, and research ideas turn into operational constraints.

I used "Willful Disobedience: Automatically Detecting Failures in Agentic Traces" in a recent essay on specification surfaces.

The essay uses the paper to argue that trace validation is the downstream half of specification authority: not just whether an agent produced a plausible output, but whether the run respected the rules the system was supposed to preserve.

I would value one objection or correction, especially if that reading blurs too much between prompt-derived behavioral rules and more durable specification artifacts.

Essay: https://lambpetros.substack.com/p/the-specification-surface-is-the
```

## Manual-Send Boundary

Two external paper-specific messages have been sent manually by the user: Camilo Chacon Sartori and Linyue Pan on 2026-05-05. The confirmed pending connection invites are Deepak Babu Piskala, Martin Monperrus, and Shraddha Barke. Ben Zorn accepted on 2026-05-05 and is ready for the prepared paper-specific message if the user wants to continue the trace-validation thread. Linyue Pan has provided a substantive boundary correction; the next manual action is the short acknowledgement draft above. Any additional sends still require acceptance plus explicit action-time approval naming the exact target and exact copy, or manual user execution from the prepared copy above.

Do not send more than five first-wave LinkedIn actions in one day unless the user explicitly accepts the account-risk tradeoff. Do not put the essay link in the connection request note.

## Outcome Retrospective

Review date: 2026-05-19 for first-wave invite acceptance and replies if post-acceptance messages are sent quickly after acceptance.
Success window elapsed: no.
Reply count: 2.
Objections or corrections: Linyue Pan objected to the broad reading that every natural-language instruction interpreted by a harness is a governing specification. Her boundary: natural language becomes governing only when bound to executable lifecycle semantics, artifact contracts, state, adapters, validation, and recovery behavior; otherwise it remains instruction/interface layer.
Useful weak ties: Linyue Pan accepted the connection and invited discussion; Camilo Chacon Sartori accepted and is reachable for a paper-centered follow-up; Ben Zorn accepted and is reachable for a trace-validation paper-specific message.
Paper revision signal: Linyue framed the narrow objection as potentially useful feedback for their next revision and later said v2 of the NLAH paper will explain the IHR+NLAH mechanism more clearly.
Author value signal: The strongest engagement mechanism was not "please read my essay" but "your paper exposes a boundary that may matter for your next revision and for how the field uses the work." Linyue's answer confirms this by turning the exchange into a mechanism/boundary discussion about her own v2.
Traffic notes, if observed: not a success metric for this experiment.
Decision: first wave has one substantive correction and one precision-checked paper-centered message sent; acknowledge Linyue's boundary, wait for Camilo's response, and do not add more targets today.
Rationale: Linyue's reply validates the expert-feedback workflow and sharpens the essay's natural-language boundary. The live essay already mostly respects this boundary because it rejects loose prose, one-off prompts, and passive markdown as source-of-truth artifacts, but the paper route should preserve Linyue's stricter language: instruction/interface layer is not governing specification unless bound to lifecycle semantics and executable harness behavior.
Next batch or stop condition: Monitor Deepak, Martin, and Shraddha for acceptance. For Camilo, wait for an objection, correction, or request for the section/paper. For Linyue, wait for her later essay comments or v2 discussion. For Ben, send the prepared paper-specific message before any administrative endorsement ask. Do not add more LinkedIn outreach targets until this batch produces either another substantive reply or a 14-day no-reply signal. Keep Brian Hempel blocked unless the correct UCSD-linked profile is verified.
