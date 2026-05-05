# Expert Feedback Outreach Tracker

Package: `publications/literate-workflow-programming/specification-surface-source-of-truth`
Essay: The Specification Surface Is the New Source of Truth
Canonical URL: https://lambpetros.substack.com/p/the-specification-surface-is-the
Batch: 2026-05-05 specification-surface paper-author feedback
Hypothesis: A bounded paper-author batch will produce sharper objections, corrections, or weak ties than general social distribution because the essay makes explicit claims about how each cited paper contributes to the specification-surface argument.
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
| Camilo Chacon Sartori | "The Specification Gap: Coordination Failure Under Partial Knowledge in Code Agents" | Hinge evidence for the coordination claim: weakened shared specifications cause multi-agent integration failures; restoring full specification is the stronger recovery. | The essay's strongest empirical hinge depends on this paper's result and its limits. | LinkedIn inspected 2026-05-05: `https://www.linkedin.com/in/camilo-chacon-sartori/`; user manually sent invite 2026-05-05; sent-invitations manager confirmed Camilo/Chacon. | yes, 2026-05-05 | pending | no | no | invite pending | Wait for acceptance; then send the prepared paper-specific message. | Initial browser invite attempt failed; manual profile action later landed. Ask whether "specification carries the shared decisions" overstates the paper's recovery setting after acceptance. |
| Martin Monperrus | "Bootstrapping Coding Agents: The Specification Is the Program" | Strongest architectural edge case for specification-as-program and derived implementations. | The essay uses the paper to show a controlled inversion where specification becomes the durable object and implementations become downstream. | LinkedIn inspected 2026-05-05: `https://www.linkedin.com/in/martin-monperrus-369300a4/`; user manually sent invite 2026-05-05; sent-invitations manager confirmed Martin/Monperrus. | yes, 2026-05-05 | pending | no | no | invite pending | Wait for acceptance; then send the prepared paper-specific message. | Initial browser invite attempt failed; manual profile action later landed. Mutual connection Jose was visible before the attempt. |
| Brian Hempel | "Professional Software Developers Don't Vibe, They Control: AI Agent Use for Coding in 2025" | Professional-practice counterweight for the anti-vibe frame: experienced developers preserve agency through planning, supervision, validation, version control, and bounded delegation. | Coauthor of the practice paper that keeps `vibe` framed as a control-surface failure rather than a personality label. | LinkedIn inspected 2026-05-05: `https://www.linkedin.com/in/brianhempel/`; visible state after attempt: `Connect`, `Message`, `More`; profile is 3rd+. | no | n/a | no | no | blocked at confirmation | Retry manually or in a later browser pass; do not send essay link in invite. | Invite modal opened, but `Send without a note` would not submit through Playwright click, forced click, or keyboard activation. Since `Connect` remained visible, the invite is not marked sent. |
| Linyue Pan | "Natural-Language Agent Harnesses" | Runtime/harness evidence: natural-language descriptions become stronger when interpreted by a harness with decomposition, roles, state, adapters, contracts, verification, and artifacts. | First author of the paper used to distinguish loose prompts from natural-language surfaces that participate in governed execution. | LinkedIn inspected 2026-05-05: `https://www.linkedin.com/in/linyue-pan/`; user-reported manual note invite sent 2026-05-05 after browser confirmation block. | yes, 2026-05-05 | pending | no | no | invite pending | Wait for acceptance; then send the prepared paper-specific message. | Manual connection note used no essay link and asked for one narrow objection on Natural-Language Agent Harnesses. |
| Shraddha Barke | "Willful Disobedience: Automatically Detecting Failures in Agentic Traces" | Trace-compliance evidence: procedural violations can be detected in traces when prompts or system instructions imply explicit behavioral rules. | Coauthor with a visible profile and directly relevant Microsoft Research background in trustworthy code generation and invariant generation. | LinkedIn inspected 2026-05-05: `https://www.linkedin.com/in/shraddha-barke-ph-d-111b4694/`; user-reported manual note invite sent 2026-05-05. | yes, 2026-05-05 | pending | no | no | invite pending | Wait for acceptance; then send the prepared paper-specific message. | Manual connection note used no essay link and asked whether the essay overconnects trace checks to specifications. |
| Ben Zorn | "Willful Disobedience: Automatically Detecting Failures in Agentic Traces" | Secondary trace/procedural-verification target for the downstream validation side of the essay. | Coauthor and visible Microsoft Research route; useful if the Shraddha route does not convert or if a broader prompt-as-program objection is wanted. | LinkedIn inspected 2026-05-05: `https://www.linkedin.com/in/ben-zorn-0a58554/`; user-reported manual note invite sent 2026-05-05. | yes, 2026-05-05 | pending | no | no | invite pending | Wait for acceptance; then send the prepared paper-specific message. | Manual connection note used no essay link and asked about trace validation vs durable specification artifacts. |

## Batch Pacing

Recommended first wave: Deepak Babu Piskala, Camilo Chacon Sartori, Martin Monperrus, Brian Hempel, and Linyue Pan.

Actual 2026-05-05 execution: Deepak, Camilo, Martin, Linyue, Shraddha, and Ben are invite-pending. Deepak, Camilo, and Martin initially failed through the in-app browser, then the user manually retried from the profile pages; LinkedIn's sent-invitations manager confirmed all three after the manual retry. Brian remains blocked and the correct UCSD-linked profile still needs verification.

Connection requests should not include the essay link. If LinkedIn requires an invite rather than a message, use either no note or this no-link note:

```text
Hi <name> - I write Rooted Layers on AI systems and software practice. I used your paper in a recent essay and would value one narrow objection if you're open to it.
```

## 2026-05-05 First-Wave Execution Log

- Deepak Babu Piskala: attempted direct `Message`, but LinkedIn showed an InMail/Premium upsell. The browser then attempted a no-note connection invite, but the sent-invitations manager initially did not show Deepak/Piskala. The user manually retried from the profile page; a later sent-invitations check confirmed Deepak/Piskala.
- Camilo Chacon Sartori: browser attempted a no-note connection invite, but the sent-invitations manager initially did not show Camilo/Chacon/Chacon Sartori. The user manually retried from the profile page; a later sent-invitations check confirmed Camilo/Chacon.
- Martin Monperrus: browser attempted a no-note connection invite, but the sent-invitations manager initially did not show Martin/Monperrus. The user manually retried from the profile page; a later sent-invitations check confirmed Martin/Monperrus.
- Brian Hempel: opened the connection invite dialog, but the `Send without a note` confirmation did not submit through the in-app browser. Post-attempt state still showed `Connect`; not marked invited.
- Linyue Pan: opened the connection invite dialog, but the `Send without a note` confirmation did not submit through the in-app browser. User later manually sent a no-link connection note.
- Shraddha Barke: user manually sent a no-link connection note.
- Ben Zorn: user manually sent a no-link connection note.

No essay link or paper-specific message was sent in this execution pass. The next external action is a post-acceptance message only after a recipient accepts the connection.

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
Status: manual connection invite pending as of 2026-05-05; confirmed in LinkedIn sent-invitations manager after the browser attempt failed; post-acceptance message prepared, not sent.

```text
Hi Camilo - I write Rooted Layers, a publication about how AI systems, software practice, and research ideas turn into operational constraints.

I used your paper, "The Specification Gap: Coordination Failure Under Partial Knowledge in Code Agents," as the hinge evidence in a recent essay on specification surfaces.

The essay argues that your result makes weak specifications visible as a coordination failure: when independent code agents lose shared decisions, post-hoc conflict detection helps diagnose the break, but the full specification is what carries the decisions that let the work converge.

I would value one objection or correction, especially if you think that reading overstates what the recovery result supports.

Essay: https://lambpetros.substack.com/p/the-specification-surface-is-the
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
Status: manual no-link connection note sent by user on 2026-05-05; post-acceptance message prepared, not sent.

```text
Hi Linyue - I write Rooted Layers, a publication about how AI systems, software practice, and research ideas turn into operational constraints.

I used your paper, "Natural-Language Agent Harnesses," in a recent essay on specification surfaces.

The essay uses the paper to argue that natural language becomes more than a loose prompt when it participates in a harness with decomposition, roles, state, adapters, contracts, verification, and durable artifacts.

I would value one objection or correction, especially if "specification surface" feels like too broad a term for what your harness work actually shows.

Essay: https://lambpetros.substack.com/p/the-specification-surface-is-the
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
Status: manual no-link connection note sent by user on 2026-05-05; post-acceptance message prepared, not sent.

```text
Hi Ben - I write Rooted Layers, a publication about how AI systems, software practice, and research ideas turn into operational constraints.

I used "Willful Disobedience: Automatically Detecting Failures in Agentic Traces" in a recent essay on specification surfaces.

The essay uses the paper to argue that trace validation is the downstream half of specification authority: not just whether an agent produced a plausible output, but whether the run respected the rules the system was supposed to preserve.

I would value one objection or correction, especially if that reading blurs too much between prompt-derived behavioral rules and more durable specification artifacts.

Essay: https://lambpetros.substack.com/p/the-specification-surface-is-the
```

## Manual-Send Boundary

No external paper-specific message was sent by this workflow. The confirmed pending connection invites are Deepak Babu Piskala, Camilo Chacon Sartori, Martin Monperrus, Linyue Pan, Shraddha Barke, and Ben Zorn. Sending the prepared messages still requires acceptance plus explicit action-time approval naming the exact target and exact copy, or manual user execution from the prepared copy above.

Do not send more than five first-wave LinkedIn actions in one day unless the user explicitly accepts the account-risk tradeoff. Do not put the essay link in the connection request note.

## Outcome Retrospective

Review date: 2026-05-19 for first-wave invite acceptance and replies if post-acceptance messages are sent quickly after acceptance.
Success window elapsed: no.
Reply count: 0.
Objections or corrections: none yet.
Useful weak ties: none yet.
Traffic notes, if observed: not a success metric for this experiment.
Decision: first wave partially executed; wait for acceptances before any essay links or paper-specific messages.
Rationale: LinkedIn's sent-invitations manager confirms six pending invites: Deepak, Camilo, Martin, Linyue, Shraddha, and Ben. The browser-attempted invites to Deepak, Camilo, and Martin did not land initially, but the user completed those invite actions manually and they later appeared in the sent-invitations manager. The batch preserved the expert-feedback posture because no essay link was included in workflow-sent actions and no paper-specific message was sent before acceptance.
Next batch or stop condition: Monitor Deepak, Camilo, Martin, Linyue, Shraddha, and Ben for acceptance. Do not add more LinkedIn outreach targets until this batch produces acceptances, replies, or a 14-day no-reply signal. Keep Brian Hempel blocked unless the correct UCSD-linked profile is verified.
