# Cold Email Drafts: Segment 2 (Product Builders)

**Context**: These emails are designed to be sent with `agent_architecture_map_v2.png` attached.
**Tone**: Helpful Auditor. "I found a way to save you money/headache."

---

## 9. Flo Crivello (Lindy)
**Subject**: Evaluation of Lindy's Persona Architecture (Audit)

Hi Flo,

I've been mapping the Agent Ecosystem (v2 attached) and analyzing how different products handle "Persona" definitions.

Lindy uses a strict definition model. While clean, my "ToolOrchestra" simulations suggest this is brittle at scale compared to a **Fluid Tool Portfolio** that evolves per user interaction.

I modeled this "Personalized Toolset" approach in **Dive 08**. It reduces the "context window waste" of unused persona instructions by ~30%.

Thought you might find the "User Alignment" section of my map relevant to Lindy’s next phase.

Best,
Petros

---

## 10. Div Garg (MultiOn)
**Subject**: Solving the "DOM State Explosion"

Hi Div,

Browser agents like MultiOn are the hardest to orchestrate because the DOM state is massive.

I’m arguing in my new technical series that we need **Visual State Value Functions**—using a lightweight vision model to prune the DOM *before* the planner sees it.

I mapped this "Visual Gateway" in the attached Architecture Map.

I wrote up the math for this "State Pruning" in **Dive 04**. I suspect this is the only way to get inference latency under 500ms for web agents.

Best,
Petros

---

## 11. Matt Shumer (Hyperwrite/Reflection)
**Subject**: Reflection 70B: Is it an Orchestrator?

Hi Matt,

The Reflection 70B launch was impressive.

My question is: Are you treating Reflection as the "Thinker" or the "Orchestrator"? My research suggests these should be **separate models**.

I wrote a breakdown of the "Planner vs Caller" separation in **Dive 10**. If you overload the Thinking model with Tool Calling syntax, performance on both drops (the "Interference" problem).

I’ve attached my 2026 Agent Architecture Map showing this split.

Best,
Petros

---

## 12. Kanjun Qiu (Imbue)
**Subject**: "Reasoning to Code" requires Sandboxing

Hi Kanjun,

I closely follow Imbue's "Reasoning" focus.

I believe we can't solve reasoning without **Sandboxed Reward Functions**. The agent must be able to run its own code in a safe environment to verify its reasoning *before* showing the user.

I mapped this "Verification Loop" in the attached Topology Map.

I detail the infrastructure for this "Sandboxed RL" in **Dive 12**. Would love to know if Imbue is building this internal verification layer.

Best,
Petros

---

## 13. Scott Wu (Cognition / Devin)
**Subject**: Modeling "Abandonment" as a Reward Signal

Hi Scott,

Devin’s ability to plan long-term is the benchmark.

I’ve been studying "Stop Criteria" in autonomous agents. My thesis is that we need to reward **Early Abandonment** (stopping a bad path) as highly as success.

I modeled this "Negative Result Reward" in **Dive 03**. It prevents the agent from digging 10-step rabbit holes.

I’ve attached the V2 Agent Map. I suspect Devin has a robust implementation of the "Kill Criteria" node I mapped here.

Best,
Petros

---

## 14. Gabriel Pereyra (Harvey)
**Subject**: Legal Hallucination is a "Constraint Violation"

Hi Gabriel,

Legal AI has the highest safety bar.

I argue in my series that "Safety" shouldn't be a prompt instructions, but a **Hard Constraint** in the Orchestrator's policy, enforced by a separate "Constitution" model.

I mapped this "Constitution Layer" in the attached architecture diagram.

I wrote up the failure modes of "Prompt-based Safety" vs "Constraint-based Safety" in **Dive 11**.

Best,
Petros

---

## 15. John Nay (Norm.ai)
**Subject**: Compliance as Code = RL Constraints

Hi John,

Norm.ai's mission of "Compliance Agents" aligns perfectly with the **Constraint-Based Orchestration** I advocate for.

I believe "Policy" (in the regulatory sense) and "Policy" (in the RL sense) are mathematically converging.

I mapped this convergence in the "Safety Layer" of the attached Agent Map. I’d love to send you my technical deep dive on "Hard Constraints" (Dive 11) if you're interested.

Best,
Petros

---

## 16. Serkan Piantino (Spell.so)
**Subject**: Agents are Distributed Systems (Non-Deterministic Nodes)

Hi Serkan,

I've been framing Agents not as "AI" but as **Distributed Systems**.

The "nodes" (LLMs) are non-deterministic, which means we need distributed systems patterns (circuit breakers, retries, eventual consistency) in the orchestration layer.

I mapped these patterns in the attached "Production Engineering" map (v2).

I wrote a full chapter on "Production Engineering for Agents" (Dive 12) that I think aligns with your worldview.

Best,
Petros
