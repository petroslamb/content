# How We Tried to Break the Hardware Friction Map

> **Companion to:** *“The Hardware Friction Map”* and *“The Hardware Friction Scorecard”*  
> **Goal:** Show the sharpest critiques, what changed because of them, and where the map is still deliberately a **strong bet**, not scripture.

Most frameworks die when someone pokes them hard. The Hardware Friction Map almost did — and is better for it.

This note is the public version of the internal review cycle behind the essay and scorecard. It distills three sets of critiques:

- **Gemini 3 Pro High on the original “Hardware Compatibility Filter” essay.**  
- **GPTi‑5.1 + Gemini 3 Pro High on the v2 Friction Map rewrite.**  
- **The scorecard scope critique on Gate‑1 overreach.**

Instead of hiding those attacks, we’re going to surface them and show exactly what they changed.

---

## 1. From “Physics Filter” to Economic Friction Map

**Original sin:** The v1 essay framed hardware as a quasi‑physical law:

- “computations silicon can efficiently express”  
- “rejected them”  
- “fight the GPU”

The critique (Gemini 3 Pro High) was blunt:

- Hardware **doesn’t reject** anything; it just charges a **100× tax**.  
- You can run KANs and Neural ODEs; they just cost $10M instead of $100K.  
- The right lens is **economics**, not physics envy: “Can you afford it?” not “Is it possible?”

**What changed:**

- The v2 essay opens on economics: *“Hardware rejects nothing. It just charges a tax.”*  
- The “Compatibility Filter” metaphor was replaced with a **Friction Map**: a gradient, not a binary gate.  
- KANs / ODEs moved from “forbidden” to “prohibitively expensive per token on 2025 GPUs.”

Net: the thesis shifted from physics absolutism to **tokens‑per‑dollar realism**.

---

## 2. Killing the Binary Trap (Filter → Map)

The first article spoke in survival absolutes: winners vs failures; aligned vs rejected.

The critique:

- MoE didn’t “pass” a clean filter; it sat in **Red‑Zone friction** for years until capital forced infra to adapt.  
- Pure SSMs aren’t “dead”; they’re just stalled in a high‑friction zone where only hybrids make sense at scale.  
- The map needs zones, not a cliff.

**What changed:**

- The Friction Map essay is explicitly built around **four zones**:  
  - Green (RoPE, GQA, RMSNorm)  
  - Yellow (FlashAttention, quantization)  
  - Orange (MoE, pure SSM frontier)  
  - Red (KANs, Neural ODEs, etc.)  
- The scorecard formalizes this as **H/E + zone interpretation** rather than a single pass/fail label.

The “Filter” metaphor died so the **gradient of friction** could live.

---

## 3. The Startup Heuristic and the Capital Hammer

Early drafts treated all actors symmetrically — as if a startup and Google faced the same risk curve.

The critique:

- For **Google / Meta / DeepSeek**, high friction is a **moat**: they can spend three years rewriting kernels and schedulers.  
- For a **product startup**, high friction is **death**: you burn runway debugging CUDA before proving your product.  
- Any serious heuristic must say who it’s for.

**What changed:**

- The essay added the explicit **Startup Heuristic**:  
  - “If it’s not in PyTorch upstream, don’t build your company on it” (for product teams).  
  - Infra startups are the exception because *their product is the friction*.  
- The scorecard introduction is now overtly targeted at **non‑Google labs and startups**, not everyone.

This is why the Friction Map works as a field manual: it’s calibrated to the **resource‑constrained practitioner**, not the lab that prints chips.

---

## 4. Gate‑1 Only: The Scorecard Scope Critique

The scorecard, left unchecked, wanted to answer too much: which architectures win, not just which ones are viable.

The scope critique boiled down to:

- The H/E table is **only Gate 1**: “Can this idea survive contact with 2023–2025 GPUs and infra?”  
- LSTMs/GRUs show the limitation: they would look green on many axes but are obviously losing bets for modern LLMs.  
- Real selection among low‑friction designs happens at Gates 2–3 (training dynamics, scaling, data).

**What changed:**

- The scorecard is now explicitly labeled “**Table 1: Hardware/Infra Viability**.”  
- Later gates are called out in‑text:  
  - Gate 2: training dynamics (e.g., vanishing gradients, stability).  
  - Gate 3: scaling laws (does performance scale smoothly with compute?).  
- LSTMs and Mamba are used as **negative case studies**: hardware‑viable yet strategically weak.

The result is a scorecard that’s honest about being **necessary but incomplete**.

---

## 5. The SSM Ceiling and Overconfident Bets

The Friction Map makes a strong claim:

- Pure SSMs are competitive up to ~7B (Falcon Mamba, etc.).  
- There are **no pure SSM frontier models ≥13B** in the wild; all serious deployments are hybrids.  
- The essay bets that pure SSM frontier models will not dominate without attention‑like components.

The critique (GPTi‑5.1):

- This is the most vulnerable part of the map.  
- It rests on **non‑observation + mechanism vibe**: we haven’t seen a 40B pure SSM, and the parallelism gaps suggest it’s hard — but that’s not proof.  
- One strong lab shipping a 20–40B pure SSM with competitive performance would blow this claim up.

**What changed:**

- The SSM section now carries a **timestamp** (“Status (Dec 2025)”) and an explicit admission that this is a bet, not a theorem.  
- The appendix (SSM Scale and Hybrid Dominance) lays out the actual evidence: concrete model sizes, where SSMs do exist, and where the record goes dark.

This is the sharpest fault line left on purpose. If the future contradicts it, the map gets to update in public.

---

## 6. Static Map vs Moving Hardware

Another critique: the map reads like a timeless law, but it’s really a snapshot of a very specific world.

- 2023–2025 is **NVIDIA‑dominated**: A100/H100, CUDA, PyTorch 2.x, vLLM.  
- Hardware is already co‑evolving with workloads: sparse accelerators, custom attention chips, inference ASICs.  
- If we ever get cheap, mainstream hardware that *loves* KANs or pure SSMs, today’s Red Zone could become tomorrow’s Green.

**What changed:**

- The scorecard now pins its scope up front: 2023–2025 NVIDIA GPU stacks, CUDA 12.x, specific frameworks.  
- The essay treats the Friction Map as a **contingent equilibrium** of this hardware era, not a universal law of neural networks.

In other words: this is a map of **today’s silicon monopoly**, not a prophecy.

---

## 7. Utility vs Rigor: Where the Map Deliberately Stays Spiky

Not every critique led to a change. Some tensions are deliberate.

### 7.1 KANs and Neural ODEs as “Do Not Touch”

- Critics: The treatment of KANs/ODEs is a bit straw‑manny — it doesn’t dwell on their theoretical appeal.  
- Author stance: Nuance is expensive; *“Do not touch this”* is cheap and useful for the intended reader.

Result: The essay keeps the **“Don’t touch”** framing for high‑friction primitives, trusting that specialists who truly care about them will read the detailed references instead.

### 7.2 The Startup Heuristic’s Over‑Generality

- Critics: “If it’s not in PyTorch upstream, don’t build your company on it” is obviously false for infra startups.  
- Author stance: That’s fine; the rule is not aimed at infra startups.

Result: The heuristic remains — with an explicit carve‑out that if you *are* the infra company, your product *is* the friction.

### 7.3 Overclaimy Opening Lines

- Critics: “Economics determines what survives” overstates Gate‑1’s role while later sections admit it’s only one gate.  
- Author stance: It’s a blog post, not a legal contract; the hook can be punchier than the caveats.

Result: The essay keeps the strong opening, but the Gate‑1 disclaimer and scorecard scope box exist to keep the rigor honest.

---

## 8. Why Publish the Stress Tests at All?

Because the only useful heuristics are the ones you invite people to break.

The Hardware Friction Map and Scorecard are designed to be:

- **High‑utility:** They save startups from betting the company on Red‑Zone architectures.  
- **Falsifiable:** A single 40B pure SSM or Titans‑style memory model that dominates on real workloads would force an update.  
- **Honest about scope:** Gate‑1 only, on NVIDIA‑dominated 2023–2025 stacks.

If you buy the frame but hate specific scores or bets, that’s the best possible outcome: it means there’s something concrete to argue with.

When that happens, the right move isn’t to defend the map — it’s to redraw it.
