# r/MachineLearning - Self-Promo Thread Comment

**Post type:** Top-level comment in the official bi-weekly self-promotion thread
**Thread URL:** `{{ML_SELF_PROMO_THREAD_URL}}`
**When:** Thursday March 19, 2026, 4-5pm EET / 10-11am EDT

---

## Link Placement

Keep the link at the end of the comment. Do not make a standalone submission for the article.

---

## Comment

**Most Multi-Agent Systems Are a Workaround, Not a Destination**

I pulled together a short synthesis around a recent UBC result: many multi-agent systems can be compiled into a single agent with skills while cutting token usage and latency substantially.

The claim is narrower than "multi-agent does not work." For many same-model, tool-using systems, the extra structure seems to be compensating for routing ambiguity, crowded action spaces, memory handling, and coordination overhead. In that setting, the agent boundary is often giving the model a cleaner local action space rather than a genuinely different capability.

I connect that paper to ROMA, SkillOrchestra, the scaling paper, Vision Wormhole, EmCoop, Agentic Memory, EMPO2, and AgentArk. The practical question I end up with is when the agent boundary is carrying real capability, and when it is mostly helping with routing and state organization.

Would be interested in pushback, especially from people running these systems in production.

Write-up: {{SUBSTACK_URL}}
