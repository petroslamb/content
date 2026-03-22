# r/LocalLLaMA - Optional Text Post

**Status:** Optional / higher-risk
**Post type:** Text post only
**When:** Friday March 20, 2026, 4-5pm EET / 10-11am EDT

---

## Link Placement

Do not put the Substack link in the OP.

If someone asks for the full write-up, reply with the short link reply at the bottom of this file. If you want a lower-risk launch, skip this subreddit entirely.

---

## Title

I think a lot of local multi-agent stacks are really routing scaffolds

## Post Body

I have been reading a run of recent agent-system papers, and one result keeps sticking with me: many multi-agent systems can be compiled into a single agent with a skill library while preserving similar quality and cutting latency and token cost.

That maps pretty well onto a lot of open-weight agent demos. We split systems into planner, researcher, coder, reviewer, memory agent, and so on, but a lot of that split seems to exist because one model gets sloppy when it has to route too many tools, too many memory operations, or too many similar actions.

The useful detail in the UBC paper is where this breaks. Skill selection stays stable and then falls apart once the action space gets too crowded. At that point, "agent" starts to look less like a persona and more like a namespace that keeps similar actions from colliding.

That does not mean multi-agent is useless. I still think it is real when the setup is genuinely mixed-model, when you need verifier or trust boundaries, when the agents are coordinating in an environment, or when you are using search and exploration on purpose. But for same-model local stacks, I think the default should be one agent plus tools first, then split only when you can name the exact failure mode.

Curious how much of the multi-agent structure people here are keeping because it is actually load-bearing, and how much is there to keep routing and context under control.

---

## Short Link Reply

I wrote up the full version here if useful: {{SUBSTACK_URL}}
