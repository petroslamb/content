# Twitter Thread: The Transformer Attractor

**Post link:** https://open.substack.com/pub/lambpetros/p/the-transformer-attractor

---

**Tweet 1/5**

The "Transformer killer" research program is a $500M graveyard.

Not because the math was wrong. Because the architectures couldn't run efficiently on NVIDIA GPUs. And no one is building GPUs optimized for anything else.

---

**Tweet 2/5**

Mamba rewrote its core algorithm to use matrix multiplications after discovering parallel scans achieved only 10-20% Tensor Core utilization. The architecture bent to fit the silicon.

RetNet was abandoned by its own authors at Microsoft five months after publication. They shipped Phi-2 instead.

---

**Tweet 3/5**

NVIDIA's Blackwell has a "Second-Generation Transformer Engine." Rubin promises "3x faster Transformer layer performance."

Conspicuously absent from the 2024-2027 roadmap: any silicon support for non-GEMM primitives.

That's a $30B bet that Transformers win through 2028.

---

**Tweet 4/5**

The trap is scale-dependent. At 14B parameters, community persistence can absorb a 2-3x compute penalty. RWKV proved this.

At 70B-400B, that same penalty is the difference between $50M and $150M training runs. No lab will pay it without proof.

---

**Tweet 5/5**

Three falsifiable predictions for 2028:

No pure non-GEMM architecture ranks top-tier at 30B+ scale.

No external-memory architecture ships as a flagship model.

Cerebras/Groq/SambaNova stay below 10% market share without a frontier lab partnership.

https://open.substack.com/pub/lambpetros/p/the-transformer-attractor
