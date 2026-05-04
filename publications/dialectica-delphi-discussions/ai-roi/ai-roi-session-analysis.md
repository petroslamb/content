# AI ROI Session Analysis

First-pass analysis of the April 23, 2026 Delphi discussion on AI ROI.

Primary raw sources:

- [`transcript.vtt`](sources/raw/2026-04-23-discussion/transcript.vtt)
- [`chat.txt`](sources/raw/2026-04-23-discussion/chat.txt)

## Source Framing

The session was framed as a Delphi Enterprise Tech Leaders Cohort discussion on AI ROI. The moderator positioned Delphi as a closed-door, invite-only alternative to vendor-led thought leadership: a room for "radical honesty" about second-order impacts, failed projects, hidden costs, and the numbers vendors do not usually admit.

The specific prompt was the gap between AI hype and realized business value. The room moved from "AI makes engineers faster" to a more useful question: where does the ROI disappear once code generation is no longer the main bottleneck?

User context changes the weight of this source: Michael Petychakis is not only a session voice. He is Dialectica's CTO, Petros's first Dialectica contact, and the person who connected Petros with Pere. His comments should therefore be read as company-context evidence for the proposed role: what Dialectica's technical leadership notices, how it talks about ROI, and what kind of technical judgment may be valued.

## Core Session Thesis

AI ROI is not primarily a tooling question. It is an operating-model question.

The strongest claim from the session is that a high percentage of AI-written code does not automatically translate into equivalent business productivity. The practical gap sits in process, governance, review, testing, security, deployment, team design, token budgeting, and adoption.

The session's most useful frame is this: AI has compressed the act of producing code, but it has not automatically compressed the rest of the system that turns work into business value.

## Why Michael Matters For The Role

Michael's AI ROI framing is probably more important for Petros than a normal expert comment because it may reveal the executive lens behind the opportunity. The recurring concerns are not "use AI everywhere" or "build a community platform quickly." They are measurement, process drag, token cost, adoption, review, governance, buy-versus-build, and the distinction between local acceleration and company-level ROI.

For the proposed Delphi role, that suggests a useful alignment point. Petros should frame the technical work as an operating system with measured loops, review gates, and cost controls, not as a speculative member portal. The strongest pitch to Michael and Pere is likely: start with the smallest operator workflow that proves the Delphi network compounds, then build only the surfaces that the evidence justifies.

Michael's session also gives Petros a vocabulary for the offer conversation:

- compare Delphi's expert-community metrics to its own baseline, not to abstract platform claims
- measure operator time, recap value, repeat attendance, intro acceptance, and client pull
- keep AI-assisted synthesis traceable and reviewed
- treat token spend and model choice as governance issues
- buy commodity tooling unless the feature is part of Dialectica's defensible expert-intelligence layer
- avoid building software that does not change expert behavior or internal operating cadence

The next conversation with Michael should test whether this interpretation is right. If Michael sees Delphi as an ROI-disciplined operating-model experiment, the role can be senior and strategic. If he sees it mainly as a platform implementation request, the boundary needs to be much tighter.

## Main Insight Threads

**1. AI-Written Code Does Not Equal Business Productivity**

The headline contrast was roughly: internal tooling may show very high AI involvement in code generation, but measured cycle-time improvement is much smaller. The useful lesson is not whether the exact percentage generalizes. It is that local productivity metrics can diverge sharply from the feeling of individual acceleration.

**2. Initial Adoption Can Make Teams Slower**

The transcript describes an adoption phase where engineers felt faster but delivery metrics got worse. One cause was using AI for tasks where direct manual action would have been faster, such as trivial configuration changes. This is an important counterweight to naive ROI claims: AI training and usage discipline matter.

**3. The Missing ROI Is In The Process**

The session repeatedly returned to dead time in the software delivery lifecycle: ticket creation, triage, grooming, allocation, review, QA, compliance, security, and deployment. If those steps stay slow, faster code production only creates upstream pressure.

**4. Smaller Teams May Fit The AI-Native SDLC Better**

One experiment described was breaking larger engineering teams into smaller units, including two-person teams with enough authority to communicate directly with product or business stakeholders. The stated hypothesis is that AI reduces the need for coordination-heavy team structures and increases the value of small, high-context teams.

**5. AI Review Changes The Review Bottleneck**

The discussion described a shift from two human reviewers toward one AI reviewer plus one human reviewer. This is a concrete process change rather than an abstract productivity claim. It suggests a path to ROI where AI is used to reduce wait states in review, not only to write code.

**6. QA Moves Earlier And Becomes Continuous**

The session positioned QA less as a final gate before release and more as a continuous engineering counterpart. CI/CD, automated checks, and security checks become more important as output volume rises.

**7. Token Spend Is A Governance Problem**

The cost discussion was blunt: unlimited token experiments can jump from modest spend to much larger monthly numbers. Non-engineers can burn more tokens because they iterate more, use stronger models unnecessarily, and lack the engineering judgment to guide the model efficiently.

**8. Vanity Projects Are Not Pure Waste**

The session did not argue for killing every off-roadmap experiment. Some "vanity" projects burn credits, but they also teach the organization how AI works, expose business users to engineering complexity, and sometimes become core products. The better stance is not "department of no" but "department of rules."

**9. Buy Versus Build Is Shifting But Not Vanishing**

The discussion surfaced a tension: AI makes internal building cheaper and faster, but security, compliance, maintenance, certification, and user experience still matter. The main CTO stance in the session remained "prefer buy unless it is core IP," especially for generic tools where security overhead can erase the apparent savings.

**10. Adoption Is The Real ROI Gate**

The room pushed beyond productivity as a burst metric. A product can be built quickly and still fail if people do not adopt it. AI ROI needs to include usage, workflow change, maintainability, knowledge transfer, team resilience, and whether the tool changes business behavior.

**11. Distribution Becomes More Valuable When Building Gets Easier**

One participant made a strong market point: if everyone can build faster, distribution, marketing, trust, and launch channels become more important. The bottleneck shifts from making software to getting it used.

**12. Tool Choice Is Less Durable Than Context Discipline**

The chat surfaced a recurring theme: Claude, OpenAI, Gemini, Kimi, and other models will trade places in the race. The durable skill is context engineering, prompt discipline, knowledge-base design, and the ability to keep organizational context portable rather than locked into one provider.

## Delphi Format Analysis

This session shows a different kind of Delphi value than the Claude Mythos session.

The Mythos session was reactive crisis sensemaking. The AI ROI session was operational truth-seeking: it created value by putting a practicing CTO's internal metrics and failures in front of peers who could challenge, compare, and add their own numbers.

The operating pattern:

- start with a clear commercial pain point
- invite a senior operator willing to discuss failed expectations and imperfect metrics
- frame the room around honest numbers rather than vendor claims
- let participants challenge the premise early
- pull live examples from the chat into the discussion
- capture the gap between individual productivity, team productivity, and business ROI
- turn the output into a practical operating memo rather than a replay

This is highly relevant to Pere's community/content work. AI ROI is a topic where experts get value from hearing what others are actually seeing because the public market is full of exaggerated claims.

## Content Assets This Session Can Produce

- An anonymized executive brief: "Why AI-written code does not equal AI ROI."
- A CTO memo: "The 70% gap between coding speed and business productivity."
- A financial governance checklist for AI token spend.
- An AI-native SDLC redesign note covering teams, PR review, QA, CI/CD, and security.
- A build-versus-buy decision framework for the AI era.
- A metric map: DORA, DevEx, cycle time, adoption, token spend, defect rate, and business value.
- A Delphi case study: using peer challenge to turn internal AI metrics into reusable executive insight.

## Suggested Claim Map

- AI ROI disappears when only coding is accelerated and the rest of delivery is unchanged.
- AI adoption can initially slow teams if usage patterns are undisciplined.
- The right comparison is not "AI versus no AI" in the abstract, but team-by-team improvement against prior baselines.
- Token spend needs governance because experimentation, model choice, and non-engineer usage can make costs unpredictable.
- Small, high-context teams may outperform larger coordination-heavy teams in AI-assisted engineering.
- AI review and continuous QA are more concrete ROI levers than generic "developer acceleration."
- Vanity projects can be useful if they are bounded and treated as organizational learning.
- Buy-versus-build should still privilege core IP, security cost, maintenance burden, and user experience.
- Distribution and adoption become more valuable as building becomes easier.

## Risks And Design Questions

- Which productivity numbers are sufficiently grounded to publish, even anonymously?
- How should Delphi distinguish AI-generated code percentage from actual productivity metrics?
- What are the right token-spend guardrails for engineers, product people, and business users?
- Can a repeatable "AI ROI teardown" template be created for future Delphi sessions?
- Should AI ROI become a standing cohort topic, separate from AI security?
- How can Pere's platform route participants into follow-up groups based on whether they care about engineering productivity, token governance, build-versus-buy, or workforce redesign?
- Does Michael expect the Delphi platform work to follow the same ROI discipline he described: measured baselines, small-team ownership, buy-versus-build restraint, and adoption metrics?
- Who will evaluate whether Petros's technical work is successful: Michael, Pere, a product leader, an engineering manager, or a cross-functional group?

## Next Artifacts To Create

- Clean transcript.
- Anonymized role map of participants and claims.
- AI ROI metric taxonomy.
- Token budget and usage-governance checklist.
- AI-native SDLC operating model.
- Build-versus-buy framework for AI-enabled internal tools.
- Short public-safe teaser about the "missing ROI" without exposing room details.
