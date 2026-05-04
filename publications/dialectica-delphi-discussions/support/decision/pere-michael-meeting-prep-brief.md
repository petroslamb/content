# Pere And Michael Meeting Prep Brief

Use this before the final offer conversations. The goal is to collect enough concrete answers to fill [`offer-evaluation-scorecard.md`](offer-evaluation-scorecard.md) and decide whether to accept, negotiate, continue discovery, or decline.

Start from [`career-alignment-and-role-demands.md`](career-alignment-and-role-demands.md). That is the demands-first surface. Do not send the full scorecard. Keep that as a private decision tool. Send a short note that frames the conversation and names the charter you want to test.

## Decision Objective

The conversations should answer one question:

Is Dialectica offering Petros real technical ownership of the Delphi operating loop, with enough access, authority, sponsorship, and discovery time to make the project work?

If the answer is yes, the role can be attractive. If the answer is vague, the offer should be negotiated before acceptance.

## Posture

Do not ask Pere and Michael to define the role from scratch.

Put a charter on the table:

- Petros owns technical discovery and architecture.
- Pere owns product/community direction.
- Michael or another named sponsor owns technical sponsorship and evaluation.
- Compliance owns consent and reuse boundaries.
- The first milestone is paid 30-45 day discovery plus a thin operator prototype.

Then use the questions below to test whether Dialectica can support that charter.

## What To Send Pere

Send Pere a short note focused on product/community shape and first milestone.

```text
Pere, before I make a final decision, I would like one focused conversation on the Delphi operating model and the role boundary.

The main thing I want to understand is whether we are trying to build a platform first, or whether the first step is to define and test the operating loop behind Delphi: expert invitation, session capture, content creation, profile enrichment, give/get follow-up, and repeat engagement.

It would help if we could cover:

1. What would make Delphi successful six months from now?
2. What is the first expert/community loop we want to prove?
3. What does the "dbt -> emailing" flow mean in actual systems and ownership?
4. What value do experts get back for participating beyond the Zoom itself?
5. What would you expect me to own in the first 30-45 days?

My current instinct is that the first milestone should be a thin operator workflow around existing systems, not a full member-facing platform. I want to test whether that matches how you are thinking about it.
```

## Questions For Pere

Use these in the call. The important answers are not abstract agreement. You need concrete examples.

### Product And Community

- What would make Delphi successful six months from now?
- Is the first objective expert engagement, client insight products, public content, internal data enrichment, or a sequence of these?
- Which expert segments matter first?
- What behavior do we want experts to repeat?
- What would make an expert feel that Delphi is worth returning to?
- What are the first three give/get offers you want to test?
- Which sessions should become expert-only recaps, client briefs, public teasers, or internal intelligence?

### Operating Loop

- What happens before, during, and after a Delphi session today?
- Where does the process currently break or depend on manual effort?
- What is the minimum useful post-session workflow?
- Should the first prototype be an operator console, a signup/profile flow, an email journey, or something else?
- Which part of the loop should be tested first with real users?

### Data And Systems

- What does "dbt -> emailing" mean concretely?
- Is dbt already in place, and who owns those models?
- What systems hold expert profiles, CRM state, consultation history, email activity, Zoom attendance, transcript files, and chat?
- Can journey logic be triggered from modeled expert data today?
- Who owns data quality and segmentation?

### Role Boundary With Pere

- What decisions would Pere own?
- What decisions would Petros own?
- What decisions require Michael, engineering leadership, compliance, or another approver?
- What would Pere want delivered in the first 30-45 days?
- Would Pere be comfortable starting with an operator-in-the-loop prototype before a member-facing platform?

## What You Need From Pere Before Deciding

By the end of the call, try to get clear answers to:

- Pere owns product/community direction.
- The first milestone is discovery plus a thin workflow, not a full platform.
- The first expert/community loop is named.
- The first give/get offers are concrete.
- The data-to-email spine is either real and accessible or still needs discovery.
- Pere supports Petros owning technical discovery and architecture.

If Pere cannot define the first loop or expects a platform without discovery, that is a negotiation issue.

## What To Send Michael

Send Michael a short note focused on sponsorship, technical bar, ROI, and access.

```text
Michael, before I make a final decision on the Delphi role, I would like one focused conversation on technical sponsorship, ROI, and first-phase scope.

The AI ROI discussion was useful because it framed AI work as an operating-model problem, not just a tooling problem. I want to understand whether the Delphi expert-community work should be approached the same way: baseline the current workflow, identify the bottleneck, prototype a thin loop, and measure adoption before building a larger platform.

It would help if we could cover:

1. What would count as ROI for the Delphi technical system after 45 days and after six months?
2. Are you the sponsor, technical evaluator, hiring decision-maker, or mainly the connector to Pere?
3. Which parts of Delphi should Dialectica own as core IP, and which should be bought or integrated?
4. What systems and data would I be able to inspect in the first month?
5. What decision rights would come with the role?

I am interested if this is technical ownership of the operating loop, not just implementation of a pre-decided platform.
```

## Questions For Michael

Use these to determine whether the role has real sponsorship and technical shape.

### Sponsorship And Evaluation

- Are you the executive sponsor, technical evaluator, hiring decision-maker, or mainly the connector to Pere?
- Who would evaluate whether my work is successful?
- Who would I report to?
- Who can unblock access to systems, data, engineering support, and compliance review?
- What would make you say after 45 days that the technical discovery was successful?

### ROI And Success Metrics

- How should Delphi's technical system be judged?
- Is this a productivity tool, a data asset, a client-insight product, a community engine, or a new business line?
- What baseline exists today for session operations, content production, expert follow-up, and repeat engagement?
- What metrics would matter most: operator time, repeat attendance, intro acceptance, recap usefulness, client pull, revenue, or another measure?
- What would make leadership stop, pivot, or invest more?

### Build Versus Buy

- Which parts of Delphi would you consider core IP?
- Which parts should be bought, integrated, or left manual?
- Would a thin operator workflow around existing tools be preferred before a full platform?
- What existing Dialectica systems should be extended rather than replaced?
- What security or certification constraints make "just build it" risky?

### AI, Data, And Governance

- What is Dialectica's policy for using transcripts, chats, and expert data with AI tools?
- What AI vendors or internal tools are already approved?
- What needs human review before being sent to experts, attendees, clients, or the public?
- Who owns consent, retention, anonymization, and client-facing reuse?
- How should token spend and model choice be governed?

### Role Boundary With Michael

- Would I own technical discovery and architecture, or mainly implementation?
- Would I have authority to recommend not building a full platform yet?
- What engineering, data, product design, and compliance support would be attached?
- What would need to be written into the offer or first-45-days plan?

## What You Need From Michael Before Deciding

By the end of the call, try to get clear answers to:

- Michael's role in sponsorship and evaluation.
- The first 45-day technical success criteria.
- Access to systems and data.
- Build-versus-buy decision rights.
- Compliance/security ownership.
- Whether the role is senior technical ownership or platform implementation.

If Michael cannot name the sponsor/evaluator, cannot guarantee access, or expects delivery commitments before discovery, the role is under-scoped.

## Optional Joint Alignment

If Pere and Michael give compatible answers, propose one short joint alignment call.

Use this agenda:

1. Confirm the first Delphi operating loop to test.
2. Confirm first 30-45 day deliverables.
3. Confirm product/community ownership, technical ownership, and compliance ownership.
4. Confirm what will not be built in phase one.
5. Confirm success metrics and decision point after the first phase.

The outcome should be a written role charter, not just verbal alignment.

## Role Boundary To Test

Use this language in both conversations:

"I am interested if the role is technical ownership of the Delphi operating loop, not just implementation of a platform. My proposed first phase would be 30-45 days of discovery and thin prototyping: current-system map, expert journey map, data inventory, consent map, first data model, build-versus-buy recommendation, and a post-session operator workflow prototype. Pere would own product/community direction, I would own technical discovery and architecture, Michael or another named sponsor would define the technical evaluation bar, and compliance would own reuse and consent boundaries."

Watch how they respond. If they sharpen it, that is good. If they dilute it into "we just need someone to build," that is a warning.

## After The Calls

Immediately fill:

1. [`offer-evaluation-scorecard.md`](offer-evaluation-scorecard.md)
2. Decision Snapshot
3. Non-Negotiables table
4. Scorecard
5. Red Flag Log
6. Final Decision Memo

Then decide:

- accept if the role is explicit and well-sponsored
- negotiate if the idea is strong but the boundary is not written down
- continue discovery if key owners are missing
- decline if responsibility is high and authority is low
