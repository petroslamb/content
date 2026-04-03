# r/artificial - Text Post

**Post type:** Text post
**Flair:** Discussion
**When:** Wednesday March 18, 2026, 6-7pm EET / 12-1pm EDT

---

## Title

I think a lot of multi-agent stacks are really routing workarounds

## Link Placement

Safer default: put the link in the final line of the OP.

If your account is borderline on self-promo history, remove the last line from the OP and use the starter comment instead.

---

## Post Body

I spent the last few days reading recent multi-agent papers, and one result changed how I think about a lot of agent demos.

A UBC team showed that many multi-agent systems can be compiled into a single agent with skills, with much lower token use and latency and similar output quality.

That does not mean multi-agent is useless. It means some of what we call specialization is really a way to keep routing under control.

The part I found most useful is where that simplification stops working. Once the tool library gets crowded enough, the model starts confusing nearby actions. At that point, an "agent" can be less like a role and more like a clean namespace.

That fits a lot of production stacks I have seen. Planner, researcher, coder, reviewer can be real specialization. Sometimes it is. But sometimes it just means one model gets messy when it has to manage too many tools and too much state in one place.

I read a wider batch of papers after that one, including ROMA, SkillOrchestra, Vision Wormhole, EmCoop, Agentic Memory, EMPO2, and the scaling paper. My takeaway is simple: before adding more agents, ask what problem they are actually fixing.

There are still cases where multi-agent looks real to me, especially mixed-model setups, trust boundaries, embodied coordination, and exploration. But a lot of same-model tool stacks look more like temporary scaffolding than an end state.

I wrote up the full argument here: {{SUBSTACK_URL}}

---

## Starter Comment

The point is narrower than "agents are over." I am mostly arguing that the boundary is often doing routing and state-management work that gets described as specialization. Curious how many people here have seen the same thing in real systems.
