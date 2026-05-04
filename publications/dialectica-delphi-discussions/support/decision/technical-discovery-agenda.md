# Technical Discovery Agenda

Working agenda for the first technical conversations with Pere and Dialectica.

## Discovery Frame

The technical question is not "what platform should we build?" The better first question is: what operating loop should exist after every Delphi session?

If the loop is clear, the platform can be designed around it. If the loop is unclear, a platform will only automate confusion.

Michael Petychakis should be included in discovery as a technical sponsor/context source. His AI ROI discussion suggests that the Delphi platform should be evaluated through operating leverage: baseline the current workflow, identify the bottleneck, prototype the smallest useful loop, measure adoption and operator time, and avoid building commodity surfaces without evidence.

The current materials suggest this loop:

An expert is invited into a timely Delphi session. The session generates attendance, chat, transcript, claims, disagreement, and follow-up intent. Dialectica turns those signals into anonymized content, expert enrichment, selective introductions, and next-best-action emails. The expert receives value, Dialectica learns more, and future sessions become better targeted.

## Data To Map

Start by finding where these records already live:

- expert profile and biography
- expert sector, role, seniority, geography, and language
- consultation history
- Delphi invitation history
- Zoom attendance
- chat contribution
- transcript speaker turns
- questions asked before, during, and after sessions
- email opens, clicks, replies, and unsubscribes
- content sent to each expert
- introductions proposed, accepted, and completed
- client demand by topic
- compliance constraints and consent status

The main architectural task is connecting these records without pretending they are cleaner than they are.

## Core Data Objects

The first data model probably needs a small set of durable objects.

Expert: the person, their public profile, internal tags, eligibility, and consent constraints.

Topic: the issue Delphi is convening around, such as Claude Mythos, AI ROI, or Hormuz fallout.

Session: the live Zoom event, its invite list, attendance, source files, and outputs.

Contribution: a chat message, spoken claim, question, resource link, or follow-up signal.

Claim: a normalized statement extracted from discussion, with evidence, confidence, disagreement, and source boundaries.

Offer: what Dialectica gives the expert, such as a recap, intro, community access, visibility, or topic brief.

Ask: what Dialectica requests, such as profile enrichment, tracker input, follow-up answer, referral, or session participation.

Action: the next email, intro, review task, content artifact, or operator decision.

Consent: what can be stored, used internally, shared with attendees, shared with clients, or used publicly.

## MVP Architecture

The first useful architecture should be thin and observable.

It can probably start as:

- source intake for Zoom transcript, chat, audio/video metadata, and attendance
- a structured session record
- transcript/chat processing into claims, questions, resources, and participant signals
- operator review before any artifact or follow-up is sent
- a small give/get offer library
- rules or prompts that recommend follow-up actions
- email template generation
- a dashboard for Pere showing session outputs and next actions

The key principle is operator-in-the-loop. Fully automated community engagement is premature until the team understands what good judgment looks like.

## dbt To Emailing Interpretation

Pere's phrase "dbt -> emailing" should be treated as a clue about the desired spine.

The likely pattern is:

1. model expert and engagement data in a structured layer
2. compute segment, eligibility, and next-best-action fields
3. pass those fields into email or journey tools
4. capture responses and completions
5. write those outcomes back into the model

The hard part is not sending email. The hard part is making sure the email is based on correct expert state, fair value exchange, consent, and a clear reason for contact.

## Early Technical Decisions

The first technical decisions should be explicit.

Buy existing tools for video hosting, email delivery, CRM primitives, and basic community surfaces unless there is a strong reason to build.

Build or own the expert intelligence layer, because that is where Delphi's defensibility lives.

Keep raw transcripts and chats stable. Create derived artifacts separately.

Make every AI-generated summary traceable to source lines or reviewed source artifacts.

Separate internal intelligence from attendee recaps, client briefs, and public teasers.

Avoid putting sensitive expert context into tools without a clear data-processing agreement and consent boundary.

## Measurement Questions

The platform should be judged by compounding behavior, not vanity activity.

Useful measures:

- repeat attendance by expert segment
- response rate to follow-up asks
- completion rate for give/get offers
- number and quality of accepted introductions
- useful claims extracted per session
- attendee-rated value of recaps
- client pull for anonymized briefs
- topic-to-topic reactivation
- operator time per session artifact
- percentage of AI-generated artifacts requiring major correction

If these metrics do not improve, the system may be producing content without building a network.

## Discovery Questions For Internal Teams

- For Michael: what would count as ROI for Delphi's technical system after 45 days, six months, and one year?
- For Michael: which parts of the system should Dialectica own because they create expert-intelligence advantage?
- For Michael: what should be bought, integrated, or left manual?
- For Michael: who evaluates technical success, and what decision rights come with that evaluation?
- What is the current expert data schema?
- Is dbt already used, and what models exist?
- What CRM or expert-management system owns the source of truth?
- What email tooling is used for expert communication?
- Can journey logic be triggered from modeled data?
- Who owns consent and compliance review?
- Are Zoom attendance, chat, and transcript data currently stored?
- What is the policy on using session transcripts for internal analysis?
- What client-facing outputs are allowed from anonymized Delphi sessions?
- What security review is required before integrating LLM processing?
- Which workflows must remain manually approved?

## First Prototype Candidate

The safest first prototype is a post-session operator console.

For one Delphi session, it should ingest transcript and chat, generate a reviewed session record, extract claims and questions, suggest three follow-up offers, draft an anonymized recap, and propose a small number of expert introductions with reasons.

That prototype would test the whole operating loop without requiring a full community platform.
