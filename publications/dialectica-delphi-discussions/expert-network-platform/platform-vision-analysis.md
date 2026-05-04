# Engagement Platform Vision Analysis

First-pass analysis of [`engagement-platform-vision.srt`](sources/raw/2026-05-04-engagement-platform-vision/engagement-platform-vision.srt).

The transcript is noisy, but the product idea is coherent: Dialectica wants a generalized engagement platform that can capture structured expert data and route the right value proposition to the right expert at the right point in the journey.

## Pere's Framing

Pere later described this transcript as "a walkthrough of the evolution of the dbt -> emailing thing."

That changes the emphasis. The recording should be read as a walkthrough of how a data-backed segmentation or knowledge-mapping layer becomes an engagement system that can trigger emails and other touchpoints. The product surface may look like profile boosts, thank-you pages, post-consultation emails, or community signup prompts, but the underlying motion is:

- expert data is modeled or transformed somewhere upstream
- rules or prompts compute relevant give/get value propositions
- those propositions are inserted into email or journey touchpoints
- expert responses feed back into the data layer
- future engagement becomes more targeted

Until the internal architecture is clarified, treat "dbt" as Pere's shorthand for the data-modeling side of the flow, not as a confirmed implementation detail.

## Core Concept

The platform should manage "give/get" value propositions for experts.

"Give" means what Dialectica offers the expert:

- access to a curated expert community
- status as part of a top expert cohort
- profile improvement or profile boost
- topic-specific insights, such as CTO insights
- future introductions, opportunities, or visibility

"Get" means what Dialectica asks from the expert:

- vendor usage data
- additional insight on vendors or market categories
- contributions to trackers, such as a SaaS disruption tracker
- regional or commercial coverage information
- profile enrichment
- participation in the community layer

The important move is that these are paired. Dialectica should not simply ask experts for more data. It should offer a concrete value proposition in exchange for each additional contribution.

## Journey Logic

The transcript describes multiple moments where a value proposition could be shown:

- profile boost page
- thank-you page
- post-consultation email
- other expert journey touchpoints

The platform should know what the expert has already completed. If the expert already answered vendor questions and joined the community flow, the next touchpoint should not repeat the same ask. It should compute the next relevant give/get offer.

This implies a stateful engagement engine:

- expert profile and experience
- known incentives
- completed asks
- pending asks
- available offers
- journey stage
- eligibility rules
- prompt-generated recommendations

## Example From Transcript

The example expert is a CTO in Switzerland. Based on that person's experience, Dialectica may want vendor data and insight for a SaaS disruption tracker. In return, Dialectica could offer access to a top expert community, CTO insights, or profile improvement.

The exact wording in the transcript is imperfect, but the shape is clear: role, region, sector, and prior behavior determine both the ask and the offer.

## Why This Matters For Delphi

Delphi is the live community format. This platform is the infrastructure that could make Delphi repeatable.

Without this layer, a Zoom session is just an event. With it, each session becomes one point in a broader expert journey:

- invite experts based on what they know
- learn more from how they participate
- ask for structured contributions after the session
- offer community access, insights, or introductions in return
- route them into future sessions or content workflows
- accumulate a richer map of expertise over time

This connects directly to the Boardy, World 50, and CEB reference models:

- Boardy: use network memory to make better introductions
- World 50: give members a premium peer community worth returning to
- CEB: turn repeated expert input into reusable research products and tools

## Product Requirements Implied By The Transcript

- A dbt or dbt-adjacent modeled data layer that represents expert attributes, eligibility, completed asks, and possible next actions.
- A rule or prompt layer that maps expert attributes to eligible give/get offers.
- A persistent state model for completed and pending expert engagement actions.
- Email templates or campaign hooks that can render the selected give/get proposition.
- A content and community platform where experts can receive the promised value.
- Integration with existing expert profile and consultation flows.
- Integration with AI interviewer work and other team-owned systems.
- A way for operators to define, test, and revise value propositions without hard-coding every flow.
- Measurement of conversion, completion, quality of data captured, and downstream value.

## Cross-Team Complexity

The transcript explicitly says this cuts across three teams or systems:

- AI interviewer
- Stefan's technical area or team
- the new community platform Pere is building

The transcript also mentions alignment with Rekka and Stefan, though the names are transcript-derived and should be confirmed.

This is not a simple landing page. It is a coordination project across data capture, expert identity, content/community, and internal workflow ownership.

## Strategic Reading

Pere's idea is stronger than a signup page. The signup page is only the visible surface. The underlying system is an expert engagement exchange:

- Dialectica identifies what it wants to learn from each expert.
- Dialectica identifies what the expert is likely to value.
- The platform presents the right exchange at the right time.
- The expert gives more data, insight, or participation because the value is explicit.
- Dialectica gradually turns isolated experts into a live, segmented, measurable network.

That is the connective tissue between the current expert-network business and the proposed Delphi community model.

In Pere's "dbt -> emailing" framing, the strategic point is that email is not just outbound marketing. It becomes the delivery surface for computed expert engagement. The intelligence should live upstream in the data and rules layer, while email becomes one channel where the next best give/get offer reaches the expert.

## Risks And Design Questions

- The "top 1% of experts" promise needs careful wording; status claims can feel hollow if the experience behind them is weak.
- The platform must avoid over-asking. Experts should not feel like they are being mined for unpaid data.
- The offer has to be concrete. "Profile boost" may be too abstract unless experts can see actual benefits.
- Community access only works as an incentive if the community already has useful experts, content, or introductions.
- Compliance needs to define which captured data can be reused, aggregated, or commercialized.
- Operators need control over the rules; otherwise each new tracker or community flow becomes an engineering dependency.

## Next Artifacts To Create

- Cleaned transcript.
- Give/get value proposition table.
- Expert journey map.
- Minimal product requirements document.
- Data model sketch for expert state, asks, offers, completions, and outcomes.
- dbt-to-email flow diagram.
- Delphi integration workflow: before session, during session, after session, long-term follow-up.
