# X Thread - Most Multi-Agent Systems Are a Workaround, Not a Destination

**Post link:** `{{SUBSTACK_URL}}`

---

**Post 1/6**

Spent the last few days reading recent multi-agent papers.

My takeaway is pretty simple: a lot of multi-agent systems look like workarounds for routing and state problems, not the end state.

---

**Post 2/6**

A UBC paper showed that many multi-agent systems can be compiled into a single agent with skills while cutting token use by 53.7% and latency by 49.5%, with comparable output quality.

That is not proof that one agent always wins.

It is a clue about what the extra agents were doing.

---

**Post 3/6**

The useful part is where the simplification breaks.

Once the action library gets crowded, the model starts confusing nearby tools.

At that point, an "agent" often acts more like a clean namespace than a separate mind.

---

**Post 4/6**

That matches a lot of real systems.

Planner, researcher, coder, reviewer can be real specialization. Sometimes it is.

But sometimes it is one model struggling to manage too many tools, too much state, and too many handoffs in one place.

---

**Post 5/6**

Multi-agent is still real in some cases. Mixed-model systems, verifier and trust boundaries, embodied coordination, and deliberate exploration all still look real to me.

So this is not an anti-agent argument.

It is just a call to be more specific about what the graph is actually solving.

---

**Post 6/6**

I wrote up the full argument here, including where the case for multi-agent is still strong and where it looks more like temporary scaffolding:

{{SUBSTACK_URL}}
