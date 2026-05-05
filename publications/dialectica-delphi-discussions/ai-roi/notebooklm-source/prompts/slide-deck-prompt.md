# NotebookLM Slide Deck Prompt

Create a short private decision deck for Pere Molisn Ayuso and Michael Petychakis at Dialectica.

Use only the uploaded AI ROI Delphi prototype sources. Do not bring in external AI ROI frameworks, vendor claims, or generic AI adoption advice.

The deck should help them understand the opportunity without reading multiple markdown files. It should be useful to them even if they are not evaluating Petros. Petros's work is the medium; the goal is to help Pere and Michael reason about their own Delphi problem.

## Format

Create 7 or 8 slides. Prefer 7 if the story holds.

Use short slide titles and sparse text. Avoid dense bullets. Each slide should have one job.

Do not include raw participant quotes, participant names, private company details, pricing, title negotiation, or client-facing language.

Do not make this a generic presentation on AI ROI. AI ROI is the worked example for Delphi's operating loop.

## Required Story

Slide 1: Title

Title: `From AI ROI Session To Delphi Operating Loop`

Subtitle: `A worked example of how one Delphi session can become structured memory and follow-up`

Slide 2: Why this exists

Explain that Pere shared Delphi session material, and this deck shows how one session was operationalized. It is not a platform pitch yet.

Slide 3: The problem

Delphi sessions are high-signal, but without an operating layer they decay into recordings, notes, summaries, and generic follow-up.

Slide 4: The AI ROI insight

Show the core insight from the session: AI ROI often disappears after code generation, in review, QA, security, deployment, token governance, and adoption. Keep this short.

Slide 5: What one session becomes

Show the loop:

```text
source record -> claim map -> artifact map -> give/get actions -> expert memory -> better next room
```

Explain that this is the operating layer around Delphi.

Slide 6: Example artifacts

Show concrete examples from the packet. Include one short example each:

- one reviewed claim
- one artifact option
- one give/get action
- one data model object or field group

This slide should make the prototype feel tangible without overwhelming the reader.

Slide 7: Michael's evaluation

Explain the 30-45 day technical test:

- baseline current workflow
- find the bottleneck
- keep operator, review, and compliance in the loop
- measure operator time, correction rate, artifact usefulness, follow-up response, and next-room quality
- decide build-versus-buy from evidence

Slide 8: Pere's community loop and the decision

Explain the give/get loop:

- give participants an anonymized AI ROI map or short memo
- ask where AI ROI disappears in their organization
- segment follow-up
- invite the right people into a smaller room

End with the decision:

```text
Do we test one real Delphi session end to end inside Dialectica's systems before discussing a full platform?
```

## Tone

Calm, direct, operational. This is a decision aid, not a sales deck.

Avoid promotional claims. Avoid exaggerated language. Do not make Delphi sound finished. The whole point is to decide whether the loop is worth testing.

