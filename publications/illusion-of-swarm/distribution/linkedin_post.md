# LinkedIn Post - Most Multi-Agent Systems Are a Workaround, Not a Destination

**Post link:** `{{SUBSTACK_URL}}`

---

A recent UBC paper gave a clear result that matches something many builders have felt in practice: many multi-agent systems can be compiled into a single agent with skills while preserving comparable output quality and cutting both token use and latency substantially.

I do not think this means multi-agent is over. I think it means the design conversation has to get more precise.

In many same-model production systems, the extra agents are compensating for routing ambiguity, tool confusion, memory pressure, and coordination overhead. In other words, the graph is often carrying structure that the base model cannot manage cleanly on its own. That distinction matters because it changes what you optimize.

The practical question is simple: what problem is the boundary solving?

If it is handling tool confusion or keeping local action spaces small, there may be a simpler architecture. If it is enforcing trust boundaries, coordinating different model types, or managing real distributed interaction, the split may be justified.

My practical takeaway is to start with the smallest system that can express the task, then split only when you can name the exact failure mode.

I wrote up a longer synthesis of the recent papers here: {{SUBSTACK_URL}}
